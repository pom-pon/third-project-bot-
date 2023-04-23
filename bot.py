import logging
import asyncio
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup
from datastore import DataStore


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.datastore = DataStore()
        self.application = Application.builder().token('6064234183:AAE-AmwaQUmii7vUbZRVnw83LrpMcxZg0S0').build()
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("rating", self.rating))
        first_conversation = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                1: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.registration)],
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        )
        second_conversation = ConversationHandler(
            # Точка входа в диалог.
            # В данном случае — команда /start. Она задаёт первый вопрос.
            entry_points=[CommandHandler('email', self.teacher_email)],

            # Состояние внутри диалога.
            # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
            states={
                1: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_email)],
            },

            # Точка прерывания диалога. В данном случае — команда /stop.
            fallbacks=[CommandHandler('stop', self.stop)]
        )

        self.application.add_handler(first_conversation)
        self.application.add_handler(second_conversation)

        
    def start_bot(self):
        self.application.run_polling()
    
    async def rating(self, update, context):
        username = update.effective_user.username
        if self.datastore.check_studying(username):
            result = str(self.datastore.get_rating(username))
        else:
            result = 'Вы еще не верифицированы.'
        await update.message.reply_text(result)
    
    async def registration(self, update, context):
        name, surname, patronymic, cls = update.message.text.split()
        if self.datastore.check_user(name, surname, patronymic, cls) is True:
            result =  'Вы уже зарегестрированы. Если вы хотите сменить аккаунт - обратитесь за этим к вашему преподавателю.'
        else:
            result = 'Запрос на верификацию отправлен. Мы сообщим вам о результатах.'
            username = update.effective_user.username
            self.datastore.add_user(name, surname, patronymic, cls, username)
        await update.message.reply_text(result)
        return ConversationHandler.END

    async def start(self, update, context):
        reply_keyboard = [['/help'],
                    ['/rating', '/email']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        user = update.effective_user
        await update.message.reply_html(
            rf"Привет {user.mention_html()}! Я чат-бот лицея № 590. Вам нужно авторизоваться для дальнейшего использования. Введите свое имя, фамилию, отчество и класс через пробелы",
            reply_markup=markup
        )
        return 1

    async def help_command(self, update, context):
        username = update.effective_user.username
        if self.datastore.check_studying(username):
            await update.message.reply_text("Я чат-бот лицея №590. Я буду присылать вам важную информацию от ваших учителей, а также могу прислать вам ваш внутришкольный рейтинг, почту вашего учителя или ваше раписание.")
        else:
            await update.message.reply_text('Вы еще не верифицированы.')
    
    async def stop(self, update, context):
        await update.message.reply_text("")
        return ConversationHandler.END
    
    async def teacher_email(self, update, context):
        username = update.effective_user.username
        if self.datastore.check_studying(username):
            result = 'Введите фамилию, имя и отчество учителя, почту которого вы хотите получить. Вы можете заменить имя-отчество на предмет, который ведет ваш учитель.'
            await update.message.reply_text(result)
            return 1
        else:
            result = 'Вы еще не верифицированы.'
            await update.message.reply_text(result)
            return ConversationHandler.END
    
    async def get_email(self, update, context):
        if len(update.message.text.split()) == 3:
           surname, nme, ptronymic = update.message.text.split()
           email = self.datastore.get_email(surname, name=nme, patronymic=ptronymic)
        else:
            surname, sbject = update.message.text.split()
            email = self.datastore.get_email(surname, subject=sbject)
        if bool(len(email)) is True:
            result = str(email[0][0])
        else:
            result = 'Почта не найдена. Проверьте достоверность введенных вами данных.'
        await update.message.reply_text(result)
        return ConversationHandler.END

    async def send_message(self, user_id, message):
        await self.application.bot.send_message(user_id, message)


if __name__ == '__main__':
    bot = Bot()
    bot.start_bot()