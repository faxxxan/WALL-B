import asyncio
import sys
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch

# ---------------------------------------------------------------------------
# Stub out the 'discord' package so tests run without installing it.
# ---------------------------------------------------------------------------
discord_stub = types.ModuleType("discord")

# Minimal flag-container used for Intents.default()
class _Intents:
    message_content = False

    @staticmethod
    def default():
        return _Intents()

# Minimal discord.Thread sentinel
class _Thread:
    pass

# Minimal discord.DMChannel sentinel
class _DMChannel:
    pass

# Minimal discord.HTTPException
class _HTTPException(Exception):
    pass

discord_stub.Intents = _Intents
discord_stub.Thread = _Thread
discord_stub.DMChannel = _DMChannel
discord_stub.HTTPException = _HTTPException

# discord.Client used inside DiscordBot.__init__
class _Client:
    def __init__(self, intents=None):
        self.user = Mock()
        self.user.id = 999
        self._events = {}

    def event(self, coro):
        """Decorator that records event coroutines."""
        self._events[coro.__name__] = coro
        return coro

    def get_channel(self, channel_id):
        return None

    async def start(self, token):
        pass

    async def close(self):
        pass

discord_stub.Client = _Client

sys.modules["discord"] = discord_stub

# ---------------------------------------------------------------------------
# Now import the module under test (with discord already stubbed).
# ---------------------------------------------------------------------------
from modules.network.discordbot import DiscordBot  # noqa: E402


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_bot(prompt="Test prompt", knowledge_sources=None, token="fake-token"):
    """Return a DiscordBot instance with background thread suppressed."""
    with patch("threading.Thread") as mock_thread, \
         patch.dict("os.environ", {"DISCORD_BOT_TOKEN": token}):
        mock_thread.return_value = Mock()
        bot = DiscordBot(
            prompt=prompt,
            knowledge_sources=knowledge_sources or [],
        )
        bot._loop = asyncio.new_event_loop()
        # Provide a messaging service so log() calls don't raise.
        bot._messaging_service = Mock()
        return bot


def _make_ai_mock(return_value="AI response"):
    """Return a mock ChatGPT instance whose completion() returns *return_value*."""
    mock_ai = Mock()
    mock_ai.completion.return_value = return_value
    return mock_ai


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestDiscordBotInit(unittest.TestCase):
    """Tests for __init__ and configuration."""

    def test_raises_without_token(self):
        with patch.dict("os.environ", {}, clear=True), \
             patch("threading.Thread"):
            # Remove DISCORD_BOT_TOKEN if it happens to be set in the env.
            env = {k: v for k, v in __import__("os").environ.items()
                   if k != "DISCORD_BOT_TOKEN"}
            with patch.dict("os.environ", env, clear=True), \
                 patch("threading.Thread"):
                with self.assertRaises(RuntimeError):
                    DiscordBot()

    def test_token_from_env(self):
        bot = _make_bot(token="env-token")
        self.assertEqual(bot.token, "env-token")

    def test_system_prompt_no_sources(self):
        bot = _make_bot(prompt="Hello", knowledge_sources=[])
        self.assertEqual(bot.system_prompt, "Hello")

    def test_system_prompt_with_sources(self):
        sources = ["https://example.com/wiki", "https://example.com/repo"]
        bot = _make_bot(prompt="Help me", knowledge_sources=sources)
        self.assertIn("https://example.com/wiki", bot.system_prompt)
        self.assertIn("https://example.com/repo", bot.system_prompt)
        self.assertIn("Help me", bot.system_prompt)

    def test_ai_instance_defaults_to_none(self):
        bot = _make_bot()
        self.assertIsNone(bot.ai_instance)

    def test_background_thread_started(self):
        with patch("threading.Thread") as mock_thread_cls, \
             patch.dict("os.environ", {"DISCORD_BOT_TOKEN": "tok"}):
            mock_thread = Mock()
            mock_thread_cls.return_value = mock_thread
            DiscordBot(prompt="p")
            mock_thread.start.assert_called_once()


class TestDiscordBotMessaging(unittest.TestCase):
    """Tests for pubsub subscription and messaging helpers."""

    def setUp(self):
        self.bot = _make_bot()

    def test_setup_messaging_subscribes_to_topics(self):
        with patch.object(self.bot, "subscribe") as mock_sub:
            self.bot.setup_messaging()
            topics = [call[0][0] for call in mock_sub.call_args_list]
            self.assertIn("discord/send", topics)
            self.assertIn("system/exit", topics)
            self.assertNotIn("ai/response", topics)

    def test_handle_ai_response_stores_response(self):
        self.bot.handle_ai_response(response="Great answer!")
        self.assertEqual(self.bot._current_response, "Great answer!")

    def test_handle_send_missing_args_logs_warning(self):
        with patch.object(self.bot, "log") as mock_log:
            self.bot.handle_send(channel_id=None, message=None)
            mock_log.assert_called_once()
            _, kwargs = mock_log.call_args
            self.assertEqual(kwargs.get("level"), "warning")

    def test_handle_send_schedules_coroutine(self):
        with patch("asyncio.run_coroutine_threadsafe") as mock_rtf:
            self.bot.handle_send(channel_id=123, message="hi")
            mock_rtf.assert_called_once()

    def test_shutdown_wrapper_schedules_close(self):
        with patch("asyncio.run_coroutine_threadsafe") as mock_rtf:
            self.bot._shutdown_wrapper()
            mock_rtf.assert_called_once()


class TestDiscordBotGetAiResponse(unittest.TestCase):
    """Tests for the direct AI-request helper."""

    def setUp(self):
        self.bot = _make_bot()

    def test_returns_error_when_no_ai_instance(self):
        """When ai_instance is not set, returns an error string."""
        result = self.bot._get_ai_response("question")
        self.assertIn("[Error:", result)

    def test_calls_ai_instance_and_returns_response(self):
        """Calls ai_instance.completion() with the text and returns the result."""
        self.bot.ai_instance = _make_ai_mock("AI says hello")
        result = self.bot._get_ai_response("hello?")
        self.bot.ai_instance.completion.assert_called_once_with("hello?")
        self.assertEqual(result, "AI says hello")

    def test_returns_none_when_ai_returns_none(self):
        """Propagates None from ai_instance.completion()."""
        self.bot.ai_instance = _make_ai_mock(None)
        result = self.bot._get_ai_response("q")
        self.assertIsNone(result)

    def test_returns_empty_string_when_ai_returns_empty(self):
        """Propagates empty string from ai_instance.completion()."""
        self.bot.ai_instance = _make_ai_mock("")
        result = self.bot._get_ai_response("q")
        self.assertEqual(result, "")

    def test_handles_exception_from_ai_instance(self):
        """Returns an error string when ai_instance.completion() raises."""
        mock_ai = Mock()
        mock_ai.completion.side_effect = Exception("boom")
        self.bot.ai_instance = mock_ai
        result = self.bot._get_ai_response("q")
        self.assertIn("[Error:", result)


class TestDiscordBotOnMessage(unittest.TestCase):
    """Tests for the async _on_message handler."""

    def setUp(self):
        self.bot = _make_bot()
        self.bot.ai_instance = _make_ai_mock("AI response")

    def _run(self, coro):
        return asyncio.run(coro)

    def _make_message(self, content="hello", in_thread=False, from_bot=False,
                      is_dm=False):
        msg = MagicMock()
        msg.content = content
        # Use the actual bot user object so that identity comparisons work.
        msg.author = self.bot._bot.user if from_bot else MagicMock()
        msg.mentions = [] if is_dm else [self.bot._bot.user]
        msg.reply = AsyncMock()
        if in_thread:
            msg.channel = MagicMock(spec=discord_stub.Thread)
            msg.channel.send = AsyncMock()
            msg.channel.history = MagicMock(return_value=_async_iter([]))
        elif is_dm:
            msg.channel = MagicMock(spec=discord_stub.DMChannel)
            msg.channel.send = AsyncMock()
        else:
            msg.channel = MagicMock()
            msg.create_thread = AsyncMock(return_value=MagicMock(send=AsyncMock()))
        msg.id = 1
        return msg

    def test_ignores_own_messages(self):
        msg = self._make_message(from_bot=True)
        self._run(self.bot._on_message(msg))
        self.bot.ai_instance.completion.assert_not_called()

    def test_ignores_messages_without_mention(self):
        msg = self._make_message()
        msg.mentions = []  # bot not mentioned
        self._run(self.bot._on_message(msg))
        self.bot.ai_instance.completion.assert_not_called()

    def test_calls_ai_when_mentioned(self):
        msg = self._make_message(content=f"<@{self.bot._bot.user.id}> What is this?")
        self._run(self.bot._on_message(msg))
        self.bot.ai_instance.completion.assert_called_once()

    def test_creates_thread_for_channel_message(self):
        msg = self._make_message(
            content=f"<@{self.bot._bot.user.id}> Tell me more."
        )
        mock_thread = MagicMock()
        mock_thread.send = AsyncMock()
        msg.create_thread = AsyncMock(return_value=mock_thread)
        self.bot.ai_instance = _make_ai_mock("Sure!")
        self._run(self.bot._on_message(msg))
        msg.create_thread.assert_called_once()
        # The response should contain the AI's answer (plus the footer).
        sent_text = mock_thread.send.call_args[0][0]
        self.assertIn("Sure!", sent_text)

    def test_replies_in_existing_thread(self):
        msg = self._make_message(
            content=f"<@{self.bot._bot.user.id}> Explain.", in_thread=True
        )
        self.bot.ai_instance = _make_ai_mock("Explanation here.")
        self._run(self.bot._on_message(msg))
        sent_text = msg.channel.send.call_args[0][0]
        self.assertIn("Explanation here.", sent_text)

    def test_thread_context_included_in_ai_prompt(self):
        """Previous thread messages must be forwarded to the AI as context."""
        prior_msg = MagicMock()
        prior_msg.author = MagicMock()
        prior_msg.author.display_name = "Alice"
        prior_msg.content = "What is modular-biped?"
        prior_msg.id = 0  # Different from the current message id (1).

        msg = self._make_message(
            content=f"<@{self.bot._bot.user.id}> Can you elaborate?",
            in_thread=True,
        )
        msg.channel.history = MagicMock(return_value=_async_iter([prior_msg]))

        self._run(self.bot._on_message(msg))

        call_text = self.bot.ai_instance.completion.call_args[0][0]
        self.assertIn("Alice: What is modular-biped?", call_text)
        self.assertIn("Can you elaborate?", call_text)

    def test_empty_content_after_mention_still_calls_ai(self):
        """Empty content after stripping the @mention is still sent to the AI."""
        msg = self._make_message(content=f"<@{self.bot._bot.user.id}>")
        self._run(self.bot._on_message(msg))
        self.bot.ai_instance.completion.assert_called_once()
        call_text = self.bot.ai_instance.completion.call_args[0][0]
        self.assertIn("Question:", call_text)

    # ------------------------------------------------------------------
    # DM (private message) tests
    # ------------------------------------------------------------------

    def test_responds_to_dm_without_mention(self):
        """DMs should be responded to without requiring a @mention."""
        msg = self._make_message(content="What is modular-biped?", is_dm=True)
        self.bot.ai_instance = _make_ai_mock("It is a robot project.")
        self._run(self.bot._on_message(msg))
        self.bot.ai_instance.completion.assert_called_once()
        msg.channel.send.assert_called_once()

    def test_dm_response_contains_ai_answer(self):
        """The response sent to a DM should contain the AI-generated text."""
        msg = self._make_message(content="Hello there!", is_dm=True)
        self.bot.ai_instance = _make_ai_mock("Hello human!")
        self._run(self.bot._on_message(msg))
        sent_text = msg.channel.send.call_args[0][0]
        self.assertIn("Hello human!", sent_text)

    def test_dm_does_not_create_thread(self):
        """DM responses must be sent directly to the channel, not via a thread."""
        msg = self._make_message(content="A question", is_dm=True)
        self.bot.ai_instance = _make_ai_mock("An answer")
        self._run(self.bot._on_message(msg))
        # create_thread should not have been called on the message.
        self.assertFalse(
            hasattr(msg, "create_thread") and msg.create_thread.called
        )
        msg.channel.send.assert_called_once()

    def test_ignores_own_dm(self):
        """The bot should ignore its own DM messages."""
        msg = self._make_message(content="test", is_dm=True, from_bot=True)
        self._run(self.bot._on_message(msg))
        self.bot.ai_instance.completion.assert_not_called()

    def test_dm_content_not_stripped_of_mentions(self):
        """DM content should be passed to the AI as-is (no mention stripping)."""
        msg = self._make_message(content="What is @someone doing?", is_dm=True)
        self._run(self.bot._on_message(msg))
        call_text = self.bot.ai_instance.completion.call_args[0][0]
        # The original question text should be preserved in the prompt.
        self.assertIn("What is @someone doing?", call_text)


class TestDiscordBotSendResponse(unittest.TestCase):
    """Tests for _send_response."""

    def setUp(self):
        self.bot = _make_bot()

    def _run(self, coro):
        return asyncio.run(coro)

    def test_send_to_existing_thread(self):
        msg = MagicMock()
        msg.channel = MagicMock(spec=discord_stub.Thread)
        msg.channel.send = AsyncMock()
        self._run(self.bot._send_response(msg, "reply text"))
        msg.channel.send.assert_called_once_with("reply text")

    def test_send_to_dm_channel(self):
        """DM channel responses should be sent directly, not via a thread."""
        msg = MagicMock()
        msg.channel = MagicMock(spec=discord_stub.DMChannel)
        msg.channel.send = AsyncMock()
        self._run(self.bot._send_response(msg, "dm reply"))
        msg.channel.send.assert_called_once_with("dm reply")

    def test_creates_thread_in_channel(self):
        msg = MagicMock()
        msg.content = "short question"
        msg.channel = MagicMock()  # Not a Thread or DMChannel
        mock_thread = MagicMock()
        mock_thread.send = AsyncMock()
        msg.create_thread = AsyncMock(return_value=mock_thread)
        self._run(self.bot._send_response(msg, "answer"))
        msg.create_thread.assert_called_once()
        mock_thread.send.assert_called_once_with("answer")

    def test_fallback_on_http_exception(self):
        msg = MagicMock()
        msg.content = "question"
        msg.channel = MagicMock()
        msg.create_thread = AsyncMock(side_effect=discord_stub.HTTPException("err"))
        msg.reply = AsyncMock()
        self._run(self.bot._send_response(msg, "fallback"))
        msg.reply.assert_called_once_with("fallback")

    def test_long_content_truncated_in_thread_name(self):
        msg = MagicMock()
        msg.content = "x" * 200
        msg.channel = MagicMock()
        mock_thread = MagicMock()
        mock_thread.send = AsyncMock()
        msg.create_thread = AsyncMock(return_value=mock_thread)
        self._run(self.bot._send_response(msg, "resp"))
        call_kwargs = msg.create_thread.call_args[1]
        self.assertLessEqual(len(call_kwargs["name"]), 100)


class TestDiscordBotSendToChannel(unittest.TestCase):
    """Tests for _send_to_channel."""

    def setUp(self):
        self.bot = _make_bot()

    def _run(self, coro):
        return asyncio.run(coro)

    def test_sends_when_channel_found(self):
        mock_channel = MagicMock()
        mock_channel.send = AsyncMock()
        self.bot._bot.get_channel = Mock(return_value=mock_channel)
        self._run(self.bot._send_to_channel(123, "hello"))
        mock_channel.send.assert_called_once_with("hello")

    def test_logs_warning_when_channel_not_found(self):
        self.bot._bot.get_channel = Mock(return_value=None)
        with patch.object(self.bot, "log") as mock_log:
            self._run(self.bot._send_to_channel(999, "msg"))
            mock_log.assert_called_once()
            _, kwargs = mock_log.call_args
            self.assertEqual(kwargs.get("level"), "warning")


# ---------------------------------------------------------------------------
# Async iterator helper used in tests
# ---------------------------------------------------------------------------

class _async_iter:
    """Minimal async iterator for mocking discord channel history."""

    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration


if __name__ == "__main__":
    unittest.main()
