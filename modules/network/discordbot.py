import asyncio
import os
import threading

import discord
from modules.base_module import BaseModule

# Discord thread names are limited to 100 characters.  We reserve 3 for the
# trailing ellipsis ("...") so the effective content limit is 97 characters.
_MAX_THREAD_NAME_CONTENT = 97


class DiscordBot(BaseModule):
    """
    Discord Bot module.

    Hosts a Discord bot that monitors for mentions and answers questions
    using the ChatGPT module directly (via ``ai_instance``) with
    GitHub-hosted knowledge sources specified in the config YAML.

    The bot responds to:
    - Private messages (DMs): every message in a DM channel is processed
      without requiring the bot to be @mentioned.
    - Server channels / threads: the bot must be explicitly @mentioned.

    Any time the bot is triggered it will:
      1. Collect the thread context (if the post is already inside a thread).
      2. Forward the question together with the system prompt and knowledge
         sources to the AI module via ``ai_instance.completion()``.
      3. Post the reply back:
         - In a DM: directly in the DM channel.
         - In a thread: directly in that thread.
         - In a regular channel: create a new thread from the original post.

    Requires the environment variable ``DISCORD_BOT_TOKEN``.
    The ``ai_instance`` attribute must be set to a ``ChatGPT`` instance
    (e.g. via ``main.py``) before the bot will be able to answer questions.

    Subscribes to:
      - ``discord/send``    – allows other modules to send a message to a
                              specific channel (kwarg: channel_id, message)
      - ``system/exit``     – gracefully shuts down the bot

    Publishes to:
      - ``log/*``           – standard logging (via BaseModule.log)

    Example config (config/discordbot.yml):

        discordbot:
          enabled: true
          path: modules.network.discordbot.DiscordBot
          config:
            prompt: "You are a helpful assistant for the modular-biped project..."
            knowledge_sources:
              - https://github.com/makerforgetech/modular-biped/wiki
              - https://github.com/makerforgetech/modular-biped/discussions
    """

    def __init__(self, **kwargs):
        """
        Initialise the Discord bot.

        :kwarg prompt: System prompt sent to the AI for every request.
        :kwarg knowledge_sources: List of URLs the AI should reference when
            answering questions.
        :kwarg token: Bot token (falls back to DISCORD_BOT_TOKEN env var).
        """
        self.token = os.getenv("DISCORD_BOT_TOKEN", kwargs.get("token", None))
        if not self.token:
            raise RuntimeError(
                "DiscordBot: No DISCORD_BOT_TOKEN provided. "
                "Set it as an environment variable or pass it as a keyword argument."
            )

        self.ai_instance = None  # Will be set via set_chatgpt()

        self.prompt = kwargs.get(
            "prompt",
            "You are a helpful assistant. Answer questions clearly and concisely.",
        )
        self.knowledge_sources = kwargs.get("knowledge_sources", [])

        # Build the system prompt once, including any knowledge-source URLs.
        if self.knowledge_sources:
            sources_str = "\n".join(f"- {s}" for s in self.knowledge_sources)
            self.system_prompt = (
                f"{self.prompt}\n\nParse and reference the following knowledge sources "
                f"when answering questions:\n{sources_str}"
            )
        else:
            self.system_prompt = self.prompt

        # Serialise AI requests so that concurrent Discord mentions do not
        # interleave their pubsub publish/subscribe calls.
        self._ai_lock = threading.Lock()
        self._current_response = None

        # Set up Discord gateway intents.
        intents = discord.Intents.default()
        intents.message_content = True
        self._bot = discord.Client(intents=intents)

        # Register event handlers via decorators.
        @self._bot.event
        async def on_ready():
            self.log(f"Discord bot logged in as {self._bot.user}.")
            self.log(f"GPT instance set: {self.ai_instance is not None}")

        @self._bot.event
        async def on_message(message):
            await self._on_message(message)

        # Run the Discord client in a dedicated background thread so it does
        # not block the main system loop.
        self._loop = asyncio.new_event_loop()
        self._bot_thread = threading.Thread(
            target=self._run_bot,
            name="DiscordBotLoop",
            daemon=True,
        )
        self._bot_thread.start()

    # ------------------------------------------------------------------
    # BaseModule interface
    # ------------------------------------------------------------------

    def setup_messaging(self):
        """Subscribe to pubsub topics after the messaging service is set."""
        # self.subscribe("ai/response", self.handle_ai_response)
        self.subscribe("discord/send", self.handle_send)
        self.subscribe("system/exit", self._shutdown_wrapper)

    # ------------------------------------------------------------------
    # Bot lifecycle
    # ------------------------------------------------------------------
    
    def _run_bot(self):
        """Entry point for the background thread running the Discord event loop."""
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._bot.start(self.token))

    def _shutdown_wrapper(self, *args, **kwargs):
        """Schedule a clean shutdown of the Discord client."""
        self.log("Shutting down Discord bot...", level="info")
        asyncio.run_coroutine_threadsafe(self._bot.close(), self._loop)

    # ------------------------------------------------------------------
    # Incoming Discord messages
    # ------------------------------------------------------------------

    async def _on_message(self, message):
        """
        Called by discord.py for every message the bot can see.

        Responds to:
        - Any message in a private DM channel (no @mention required).
        - Messages in servers/threads where the bot is explicitly @mentioned.
        Does not respond to its own messages.
        """
        print(f"Received message: {message.content} (mentions: {[m.display_name for m in message.mentions]})")

        if message.author == self._bot.user:
            return

        # Private messages: respond to everything without requiring a mention.
        is_dm = isinstance(message.channel, discord.DMChannel)

        if not is_dm and self._bot.user not in message.mentions:
            return

        print("Processing message...")

        # Strip @mentions from content (only relevant for channel/thread messages).
        content = message.content
        if not is_dm:
            for mention in message.mentions:
                content = content.replace(f"<@{mention.id}>", "")
                content = content.replace(f"<@!{mention.id}>", "")
        content = content.strip()

        # If the message is already inside a thread, collect recent context.
        if isinstance(message.channel, discord.Thread):
            thread_lines = []
            async for msg in message.channel.history(limit=20, oldest_first=True):
                if msg.id != message.id:
                    thread_lines.append(
                        f"{msg.author.display_name}: {msg.content}"
                    )
            if thread_lines:
                context = "\n".join(thread_lines)
                full_text = (
                    f"{self.system_prompt}\n\n"
                    f"Thread context:\n{context}\n\n"
                    f"Question: {content}"
                )
            else:
                full_text = f"{self.system_prompt}\n\nQuestion: {content}"
        else:
            full_text = f"{self.system_prompt}\n\nQuestion: {content}"

        # Offload the synchronous AI call to a thread-pool executor so the
        # Discord event loop is not blocked while waiting for the AI.
        
        print(f"Full text sent to AI:\n{full_text}")
        
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None, self._get_ai_response, full_text
        )

        if response:
            footer = "\n\n*I am a bot and currently in beta.*"
            footer += "\n\n*If you want to help support the project, buy me a coffee: https://buymeacoffee.com/makerforgetech*"
            response += footer
            print (f"AI response:\n{response}")
            await self._send_response(message, response)

    # ------------------------------------------------------------------
    # AI integration (pubsub)
    # ------------------------------------------------------------------

    def _get_ai_response(self, text):
        """
        Call the ChatGPT module's completion() method directly.
        """
        if not self.ai_instance:
            self.log("ChatGPT instance not set in DiscordBot.", level="error")
            return "[Error: ChatGPT module not available]"
        try:
            return self.ai_instance.completion(text)
        except Exception as e:
            self.log(f"Error calling ChatGPT completion: {e}", level="error")
            return f"[Error: {e}]"

    def handle_ai_response(self, response):
        """
        Receive an AI-generated response via the ``ai/response`` pubsub topic.

        :param response: The text generated by the AI module.
        """
        self._current_response = response

    # ------------------------------------------------------------------
    # Sending responses back to Discord
    # ------------------------------------------------------------------

    async def _send_response(self, message, response):
        """
        Send *response* back to Discord.

        - DM channels and existing threads: reply directly in the channel.
        - Regular server channels: create a new thread from the message so
          the conversation stays organised.
        """
        if isinstance(message.channel, (discord.Thread, discord.DMChannel)):
            await message.channel.send(response)
        else:
            thread_name = (message.content[:_MAX_THREAD_NAME_CONTENT] + "...") if len(message.content) > _MAX_THREAD_NAME_CONTENT else message.content
            thread_name = thread_name.strip() or "Discussion"
            try:
                thread = await message.create_thread(name=thread_name)
                await thread.send(response)
            except discord.HTTPException:
                # Fallback: reply inline if thread creation fails.
                await message.reply(response)

    def handle_send(self, channel_id=None, message=None):
        """
        Send a message to a Discord channel from another module via pubsub.

        Publish ``discord/send`` with kwargs ``channel_id`` (int) and
        ``message`` (str) to use this handler.
        """
        if channel_id is None or message is None:
            self.log(
                "handle_send: channel_id and message are required",
                level="warning",
            )
            return
        asyncio.run_coroutine_threadsafe(
            self._send_to_channel(int(channel_id), message),
            self._loop,
        )

    async def _send_to_channel(self, channel_id, message):
        """Send *message* to the Discord channel identified by *channel_id*."""
        channel = self._bot.get_channel(channel_id)
        if channel:
            await channel.send(message)
        else:
            self.log(f"Channel {channel_id} not found", level="warning")
