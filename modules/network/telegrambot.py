#!/usr/bin/env python
# pylint: disable=unused-argument
import logging
import os
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
        self.update = None
        self.admin = os.getenv('TELEGRAM_USER_ID', None)
        
        self.user_whitelist = kwargs.get('user_whitelist', [])
        
        self.user_whitelist.append(int(self.admin)) # Ensure admin is in the whitelist
        print(f"User whitelist: {self.user_whitelist}")

        # Create the Application and pass it your bot's token
        self.application = Application.builder().token(self.token).build()

        # Set up command handlers
        self.application.add_handler(CommandHandler("start", TelegramBot.start))
        self.application.add_handler(CommandHandler("help", TelegramBot.help_command))

        # Set up message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_publish))
        
        
        
    def setup_messaging(self):
        """Set up messaging for the module."""
        def response_wrapper(user_id, message):
            import asyncio
            asyncio.create_task(self.handle_response(user_id, message))
        self.subscribe('telegram/respond', response_wrapper)
        self.subscribe('telegram/received', response_wrapper) # Test echoing received messages back to the user
        print('polling... script execution will block here until the bot is stopped')
        self.application.run_polling()

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
        
        # Save the update for response handling
        self.update = update
        
        # Publish the message to other parts of the application
        self.publish('telegram/received', user_id=user_id, message=message)
        print(f"Published message from user {user_id}: {message} on topic telegram/received")

    async def handle_response(self, user_id: int, message: str) -> None:
        """Handle responses from the application and send them back to the user."""
        if (user_id not in self.user_whitelist):
            print(f"User {user_id} not in whitelist, skipping response")
            return
        print(f"Handling response for user {user_id}: {message}")
        # Send the response back to the user on Telegram
        if self.update and self.update.effective_user.id == user_id:
            await self.update.message.reply_text(message)

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
    
    