import os
import django
import telebot
import sqlite3

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service_project.settings')
django.setup()

# Import Django models after setup
from users.models import User

TELEGRAM_BOT_TOKEN: str = "7043047188:AAHm7qvRAeDwI9brIuOzjn9EW-KKXEzbkfQ"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

conn = sqlite3.connect("db.sqlite3.users")
cursor = conn.cursor()

# Dictionary to store email temporarily
user_email = {}


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome! Please send your email address.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in user_email:
        user_email[chat_id] = message.text
        bot.reply_to(message, "Email received. Please send your password.")
    else:
        email = user_email.pop(chat_id)
        password = message.text
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                bot.reply_to(message, "Login successful.")
            else:
                bot.reply_to(message, "Invalid email or password.")
        except User.DoesNotExist:
            bot.reply_to(message, "User does not exist.")


bot.polling()
