import logging
import datetime
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from datastore import DataStore


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TIMER = 5  # таймер на 5 секунд


class Bot:
    def __init__(self):
        self.datastore = DataStore()
        application = Application.builder().token('6064234183:AAE-AmwaQUmii7vUbZRVnw83LrpMcxZg0S0').build()
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("rating", self.rating))
        conv_handler = ConversationHandler(
            # Точка входа в диалог.
            # В данном случае — команда /start. Она задаёт первый вопрос.
            entry_points=[CommandHandler('start', self.start)],

            # Состояние внутри диалога.
            # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
            states={
                1: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.registration)],
            },

            # Точка прерывания диалога. В данном случае — команда /stop.
            fallbacks=[CommandHandler('stop', self.stop)]
        )

        application.add_handler(conv_handler)

        application.run_polling()
    
    async def rating(self, update, context):
        username = update.effective_user.username
        result = self.datastore.get_rating(username)
        await update.message.reply_text(str(result))
    
    async def registration(self, update, context):
        name, surname, patric, cls = update.message.text.split()
        if self.datastore.check_user(name, surname, patric, cls) is True:
            result =  'Вы уже зарегестрированы. Если вы хотите сменить аккаунт - обратитесь за этим к вашему преподавателю.'
        else:
            result = 'Запрос на верификацию отправлен. Мы сообщим вам о результатах.'
        await update.message.reply_text(result)
        return ConversationHandler.END

    async def start(self, update, context):
        reply_keyboard = [['/help'],
                    ['/date', '/time']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я чат-бот лицея № 590. Вам нужно авторизоваться для дальнейшего использования. Введите свое имя, фамилию, отчество и класс через пробелы",
            reply_markup=markup
        )
        return 1

    async def help_command(self, update, context):
        await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")
    
    async def stop(self, update, context):
        await update.message.reply_text("Вы авторизованы.")
        return ConversationHandler.END


if __name__ == '__main__':
    Bot()