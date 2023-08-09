from telebot import TeleBot
from vars import BOT_TOKEN

bot=TeleBot(token=BOT_TOKEN,parse_mode="MARKDOWN",threaded=False)
