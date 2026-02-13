#!/usr/bin/env python
# pylint: disable=unused-argument
import asyncio
import logging
import os
import threading
from modules.base_module import BaseModule

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class TelegramBot(BaseModule):
    def __init__(self, **kwargs):
        """
        Telegram Bot
        :param kwargs: token

        Create a bot via Telegram's BotFather and get the token.
        
        Set the token as an environment variable 'TELEGRAM_BOT_TOKEN' (preferred) or pass it as a keyword argument.
        
        1. Search for BotFather in Telegram
        2. Start the BotFather
        3. Type /newbot
        4. Follow the instructions
        5. Copy the token (DON'T SHARE IT WITH ANYONE)
        6. Create an environment variable called TELEGRAM_BOT_TOKEN and set it to the token (can also be set in the config yaml)
        7. Run the script
        
        """
        # Get token from environment variable
        self.token = os.getenv('TELEGRAM_BOT_TOKEN', kwargs.get('token', None))
        # print(self.token)
        # Topics for pubsub communication
        raw_whitelist = kwargs.get('user_whitelist', [])
        normalized_whitelist = set()
        for candidate in raw_whitelist:
            try:
                normalized_whitelist.add(int(candidate))
            except (TypeError, ValueError):
                print(f"Skipping non-numeric whitelist entry '{candidate}'")

        admin_env = os.getenv('TELEGRAM_USER_ID', None)
        self.admin = None
        if admin_env is not None:
            try:
                self.admin = int(admin_env)
                normalized_whitelist.add(self.admin)
            except (TypeError, ValueError):
                print(f"Invalid TELEGRAM_USER_ID value '{admin_env}', skipping admin whitelist entry")

        self.user_whitelist = normalized_whitelist
        if not self.user_whitelist:
            print("User whitelist disabled; allowing responses to any chat")
        else:
            print(f"User whitelist: {sorted(self.user_whitelist)}")

        # Create the Application and pass it your bot's token
        self.application = Application.builder().token(self.token).build()

        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(target=self._run_event_loop, name="TelegramBotLoop", daemon=True)
        self._loop_thread.start()
        self._startup_future = None
        self._application_started = False
        self._bot_ready = threading.Event()
        self._chat_ids = {}
        self._updater_started = False

        # Set up command handlers
        self.application.add_handler(CommandHandler("start", TelegramBot.start))
        self.application.add_handler(CommandHandler("help", TelegramBot.help_command))

        # Set up message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_publish))
        
    def setup_messaging(self):
        self.subscribe('telegram/respond', self.handle_response_wrapper)
        # self.subscribe('telegram/received', self.handle_response_wrapper) # Test echoing received messages back to the user
        self._ensure_application_started()
        
    def handle_response_wrapper(self, user_id=None, message=None):
        """Test method to verify the bot is working."""
        print(f"Received response to send to user {user_id}: {message}")
        if user_id is None or message is None:
            print("Missing user_id or message in response_wrapper; setting to admin")
            user_id = self.admin
        asyncio.run_coroutine_threadsafe(self.handle_response(user_id, message), self._loop)

    def _run_event_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _ensure_application_started(self):
        if self._startup_future is not None:
            return

        async def start_application():
            await self.application.initialize()
            await self.application.start()
            if self.application.updater is not None:
                await self.application.updater.start_polling()
                self._updater_started = True
            self._application_started = True
            self._bot_ready.set()

        self._startup_future = asyncio.run_coroutine_threadsafe(start_application(), self._loop)
        self._startup_future.add_done_callback(self._handle_startup_result)

    def _handle_startup_result(self, future):
        exc = future.exception()
        if exc is not None:
            print(f"Failed to start Telegram application: {exc}")

    async def shutdown(self):
        if not self._application_started:
            return
        if self._updater_started and self.application.updater is not None:
            await self.application.updater.stop()
            self._updater_started = False
        await self.application.stop()
        await self.application.shutdown()
        self._application_started = False
        self._loop.call_soon_threadsafe(self._loop.stop)

    async def _wait_until_ready(self):
        while not self._application_started:
            await asyncio.sleep(0.05)

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    @staticmethod
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def handle_publish(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Publish the user's message to the application via pubsub."""
        user_id = update.effective_user.id
        message = update.message.text
        print(f"Received message from user {user_id}: {message}")

        chat = update.effective_chat
        if chat is not None:
            self._chat_ids[user_id] = chat.id
        
        # Save the update for response handling
        # Publish the message to other parts of the application
        self.publish('telegram/received', user_id=user_id, message=message)
        print(f"Published message from user {user_id}: {message} on topic telegram/received")

    async def handle_response(self, user_id: int, message: str) -> None:
        """Handle responses from the application and send them back to the user."""
        await self._wait_until_ready()
        if (user_id not in self.user_whitelist):
            print(f"User {user_id} not in whitelist, skipping response")
            return
        print(f"Handling response for user {user_id}: {message}")
        chat_id = self._chat_ids.get(user_id)
        if chat_id is None:
            print(f"No chat history for user {user_id}; cannot deliver message")
            return
        await self.application.bot.send_message(chat_id=chat_id, text=message)

    # def async_handle_wrapper(self, user_id: int, response: str) -> None:
    #     """Wrapper to handle asynchronous calling of the handle coroutine."""
    #     print(f"Scheduling async handling for user {user_id}")
    #     asyncio.create_task(self.handle(user_id, response))

if __name__ == "__main__":
    # Enable logging
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    # Set higher logging level for httpx to avoid all GET and POST requests being logged
    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)

    async def main():
        bot = TelegramBot()
        bot.user_whitelist = []

        # Define the simulate_echo function, which will be triggered on 'publish_received'
        def simulate_echo(user_id, message):
            print(f"Simulating echo for user {user_id} with message: {message}")
            # This would echo back as a response to the handle method
            bot.publish('telegram/respond', user_id=user_id, response=message)

        # Subscribe the simulate_echo function to the publish_received topic
        bot.subscribe('telegram/received', simulate_echo)
        print("Subscribed to 'telegram/received' topic")

        await bot.start()

        # Keep the main task alive so background polling continues
        while True:
            await asyncio.sleep(3600)

    asyncio.run(main())
    
    