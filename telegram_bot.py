import telebot

TELEGRAM_BOT_TOKEN: str = "7043047188:AAHm7qvRAeDwI9brIuOzjn9EW-KKXEzbkfQ"
TELEGRAM_BOT_USERNAME: str = "@LiraryBot"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=["start", "hello"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
