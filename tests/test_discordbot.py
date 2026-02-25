import asyncio
import sys
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, Mock, patch, PropertyMock

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

# Minimal discord.HTTPException
class _HTTPException(Exception):
    pass

discord_stub.Intents = _Intents
discord_stub.Thread = _Thread
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
        return bot


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
        self.mock_ms = Mock()
        self.bot._messaging_service = self.mock_ms

    def test_setup_messaging_subscribes_to_topics(self):
        with patch.object(self.bot, "subscribe") as mock_sub:
            self.bot.setup_messaging()
            topics = [call[0][0] for call in mock_sub.call_args_list]
            self.assertIn("ai/response", topics)
            self.assertIn("discord/send", topics)
            self.assertIn("system/exit", topics)

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
    """Tests for the synchronous AI-request helper."""

    def setUp(self):
        self.bot = _make_bot()

    def test_returns_none_when_no_subscriber(self):
        with patch.object(self.bot, "publish"):
            result = self.bot._get_ai_response("question")
        self.assertIsNone(result)

    def test_returns_none_when_ai_responds_with_none(self):
        """Bot handles a None response from the AI module gracefully."""

        def fake_publish(topic, **kwargs):
            if topic == "ai/input":
                self.bot.handle_ai_response(response=None)

        with patch.object(self.bot, "publish", side_effect=fake_publish):
            result = self.bot._get_ai_response("question?")
        self.assertIsNone(result)

    def test_returns_empty_string_when_ai_responds_with_empty(self):
        """Bot returns an empty string when the AI module yields one."""

        def fake_publish(topic, **kwargs):
            if topic == "ai/input":
                self.bot.handle_ai_response(response="")

        with patch.object(self.bot, "publish", side_effect=fake_publish):
            result = self.bot._get_ai_response("question?")
        self.assertEqual(result, "")

    def test_returns_response_set_during_publish(self):
        """Simulate ChatGPT setting the response synchronously during publish."""

        def fake_publish(topic, **kwargs):
            if topic == "ai/input":
                self.bot.handle_ai_response(response="AI says hello")

        with patch.object(self.bot, "publish", side_effect=fake_publish):
            result = self.bot._get_ai_response("hello?")
        self.assertEqual(result, "AI says hello")

    def test_lock_serialises_requests(self):
        """The _ai_lock context manager must be entered and exited."""
        mock_lock = MagicMock()
        self.bot._ai_lock = mock_lock
        with patch.object(self.bot, "publish"):
            self.bot._get_ai_response("test")
        mock_lock.__enter__.assert_called_once()
        mock_lock.__exit__.assert_called_once()


class TestDiscordBotOnMessage(unittest.TestCase):
    """Tests for the async _on_message handler."""

    def setUp(self):
        self.bot = _make_bot()

    def _run(self, coro):
        return asyncio.run(coro)

    def _make_message(self, content="hello", in_thread=False, from_bot=False):
        msg = MagicMock()
        msg.content = content
        # Use the actual bot user object so that identity comparisons work.
        msg.author = self.bot._bot.user if from_bot else MagicMock()
        msg.mentions = [self.bot._bot.user]
        msg.reply = AsyncMock()
        if in_thread:
            msg.channel = MagicMock(spec=discord_stub.Thread)
            msg.channel.send = AsyncMock()
            msg.channel.history = MagicMock(return_value=_async_iter([]))
        else:
            msg.channel = MagicMock()
            msg.create_thread = AsyncMock(return_value=MagicMock(send=AsyncMock()))
        msg.id = 1
        return msg

    def test_ignores_own_messages(self):
        msg = self._make_message(from_bot=True)
        with patch.object(self.bot, "publish") as mock_pub:
            self._run(self.bot._on_message(msg))
            mock_pub.assert_not_called()

    def test_ignores_messages_without_mention(self):
        msg = self._make_message()
        msg.mentions = []  # bot not mentioned
        with patch.object(self.bot, "publish") as mock_pub:
            self._run(self.bot._on_message(msg))
            mock_pub.assert_not_called()

    def test_empty_content_after_mention_sends_greeting(self):
        msg = self._make_message(content=f"<@{self.bot._bot.user.id}>")
        self._run(self.bot._on_message(msg))
        msg.reply.assert_called_once()

    def test_publishes_ai_input_when_mentioned(self):
        msg = self._make_message(content=f"<@{self.bot._bot.user.id}> What is this?")

        def fake_publish(topic, **kwargs):
            if topic == "ai/input":
                self.bot._current_response = "The answer."

        with patch.object(self.bot, "publish", side_effect=fake_publish):
            self._run(self.bot._on_message(msg))

    def test_creates_thread_for_channel_message(self):
        msg = self._make_message(
            content=f"<@{self.bot._bot.user.id}> Tell me more."
        )
        mock_thread = MagicMock()
        mock_thread.send = AsyncMock()
        msg.create_thread = AsyncMock(return_value=mock_thread)

        def fake_publish(topic, **kwargs):
            if topic == "ai/input":
                self.bot._current_response = "Sure!"

        with patch.object(self.bot, "publish", side_effect=fake_publish):
            self._run(self.bot._on_message(msg))

        msg.create_thread.assert_called_once()
        mock_thread.send.assert_called_once_with("Sure!")

    def test_replies_in_existing_thread(self):
        msg = self._make_message(
            content=f"<@{self.bot._bot.user.id}> Explain.", in_thread=True
        )

        def fake_publish(topic, **kwargs):
            if topic == "ai/input":
                self.bot._current_response = "Explanation here."

        with patch.object(self.bot, "publish", side_effect=fake_publish):
            self._run(self.bot._on_message(msg))

        msg.channel.send.assert_called_once_with("Explanation here.")

    def test_thread_context_included_in_ai_prompt(self):
        """Previous thread messages must be forwarded to the AI as context."""
        # Build a prior message in the thread.
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

        published_texts = []

        def capture_publish(topic, **kwargs):
            if topic == "ai/input":
                published_texts.append(kwargs.get("text", ""))
                self.bot._current_response = "Sure!"

        with patch.object(self.bot, "publish", side_effect=capture_publish):
            self._run(self.bot._on_message(msg))

        self.assertEqual(len(published_texts), 1)
        self.assertIn("Alice: What is modular-biped?", published_texts[0])
        self.assertIn("Can you elaborate?", published_texts[0])


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

    def test_creates_thread_in_channel(self):
        msg = MagicMock()
        msg.content = "short question"
        msg.channel = MagicMock()  # Not a Thread
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
