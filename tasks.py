import os

from celery import shared_task
import telebot
from django.conf import settings
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service_project.settings')
django.setup()
from users.models import User


bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@shared_task
def send_notification():
    users = User.objects.all()
    message = "Don't forget to check your borrowings, to do it, pls login"
    for user in users:
        chat_id = user.telegram_chat_id
        bot.send_message(chat_id, message, parse_mode="html")
