from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
from decouple import config
import django
from django.conf import settings
from user import user_defaults

settings.configure(default_settings=user_defaults, DEBUG=True)
django.setup()

from user.models import User

# Инициализируем бота
bot = Bot(token=config('TELEGRAM_TOKEN'))
application = Application.builder().token(config('TELEGRAM_TOKEN')).build()

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = user.id
    username = user.username

    # Сохранить chat_id и username пользователя в базе данных
    user, created = User.objects.get_or_create(username=username)
    user.telegram_chat_id = chat_id
    user.save()
    
    update.message.reply_text("Ваш chat_id успешно сохранен!")

# Регистрация команды
application.add_handler(CommandHandler("start", start))

# Запуск бота
if __name__ == "__main__":
    application.run_polling()
