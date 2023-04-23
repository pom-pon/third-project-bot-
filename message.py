import logging
import asyncio
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from datastore import DataStore


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class Message:
    def __init__(self):
        self.datastore = DataStore()
        self.application = Application.builder().token('6064234183:AAE-AmwaQUmii7vUbZRVnw83LrpMcxZg0S0').build()

    async def send_message(self, user_id, message):
        await self.application.bot.send_message(user_id, message)

    async def send_message_to_class(self, cls, message):
        datastore = DataStore()
        bot = Message()
        user_id = datastore.get_users_id(cls)
        for id in user_id:
            await bot.send_message(id[0], message)


if __name__ == '__main__':
    asyncio.run(Message().send_message_to_class('10А', 'Завтра ко второму уроку.'))