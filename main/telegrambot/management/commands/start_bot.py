from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from decouple import config
from user.models import User
from asgiref.sync import sync_to_async

# Синхронная версия функции для работы с базой данных
@sync_to_async
def save_user_to_db(username, chat_id):
    # Прежде чем сохранить пользователя, ищем его в базе
    try:
        user = User.objects.get(telegram=username)
        user.telegram_chat_id = chat_id
        user.save()
    except User.DoesNotExist:
        return 404

# Асинхронный обработчик команды /start
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = user.id
    username = user.username

    # Сохранить данные в базе данных асинхронно
    await save_user_to_db(username, chat_id)
    
    if save_user_to_db == 404:
        await update.message.reply_text("Вы не зарегестрированы на сайте!")
    
    # Ответить пользователю
    await update.message.reply_text("Ваш chat_id успешно сохранен!")

class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **kwargs):
        # Инициализируем бота
        application = ApplicationBuilder().token(config('TELEGRAM_TOKEN')).build()

        # Добавляем обработчик команды /start
        application.add_handler(CommandHandler("start", start))

        # Запускаем бота
        application.run_polling()
