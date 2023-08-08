from telebot import TeleBot
from telebot import apihelper
from vars import BOT_TOKEN

apihelper.ENABLE_MIDDLEWARE = True
apihelper.API_URL='0.0.0.0'
bot=TeleBot(token=BOT_TOKEN,parse_mode="MARKDOWN",threaded=False)
