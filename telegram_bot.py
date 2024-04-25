import os
from datetime import datetime
import django
import telebot
import sqlite3
from library_service_project import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_service_project.settings')
django.setup()

from users.models import User
from borrowings.models import Borrowing

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

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
            user.telegram_chat_id = chat_id
            user.save()
            if user.check_password(password):
                bot.reply_to(message, "Login successful.")
                check_borrowings(message, user)
            else:
                bot.reply_to(message, "Invalid email or password.")
        except User.DoesNotExist:
            bot.reply_to(message, "User does not exist.")


@bot.message_handler(commands=['borrowings'])
def check_borrowings(message, user):
    borrowings = Borrowing.objects.filter(borrower_id=user.id)
    if borrowings:
        response = "Your borrowings:\n"
        for borrowing in borrowings:
            response += f"- Book: {borrowing.book}\n"
            response += f"- Borrow date: {borrowing.borrow_date}\n"
            response += f"- Expected return date: {borrowing.expected_return_date}\n"

            days_overdue = (datetime.now() - datetime.combine(borrowing.expected_return_date, datetime.min.time())).days
            if days_overdue > 0:
                fee = borrowing.book.daily_fee * days_overdue
                response += f"- fee: {fee}"
            else:
                response += "- No fee\n"
            response += "##############################\n"
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "You don't have any borrowings.")


################################################
# TO DO Integrate sending notifications on new
# borrowing creation (provide info about this
# borrowing in the message)
#################################################

bot.polling()
