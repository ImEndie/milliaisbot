import telebot
from bot import bot

class IsSubscribed(telebot.custom_filters.SimpleCustomFilter):
    key='is_subscribed'
    @staticmethod
    def check(message):
        subscribed1 = bot.get_chat_member("@codes1gn",message.from_user.id).status in ['administrator','creator','member'] 
        try:
            return (subscribed1 ) or message.chat.type!='private'
        except:
            return (subscribed1 ) or message.message.chat.type!='private'
class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return bot.get_chat_member(message.chat.id,message.from_user.id).status in ['administrator','creator']
