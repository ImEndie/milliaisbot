import time
from telebot import types
from bot import bot
from chat import gen_img, req
from filters import IsAdmin , IsSubscribed
from database import ins,get_all,get_count
from vars import ADMINS

markup=types.InlineKeyboardMarkup()
markup.add(types.InlineKeyboardButton("MILLI AI kanali","https://t.me/milliai"))

@bot.message_handler(content_types=['new_chat_members'])
def new_chat_members(m):
    for i in m.new_chat_members:
        bot.send_message(m.chat.id,f"Salom {i.first_name}!\nGuruxga xush kelibsiz.")
    bot.delete_message(m.chat.id,m.id)

@bot.message_handler(is_subscribed=True,commands=['start'])
def start(m):
    ins(m.from_user.id)
    bot.reply_to(m,f"Assalomu alaykum {m.from_user.first_name}! Botdan foydalanish uchun /help buyrug'idan foydalaning.")

@bot.message_handler(is_subscribed=True,commands=['help'])
def help(m):
    bot.reply_to(m,"/ask — savollarga javob topishda va ko'plab boshqa muammolarni yechishda yordam beradi. Foydalanish uchun /ask buyrug'i bilan birgalikda xabar kiriting.\nMasalan: ``` /ask Salom milliai!``` \n/photo — rasmlarni osongina yaratish uchun yordam beradi. Foydalanish uchun /photo buyrug'i bilan birgalikda xabarni kiriting.\nMasalan: ``` /photo offisda ishlayotgan mushuk ```\n /stats — Bot statistikasi")

@bot.message_handler(is_subscribed=True,commands=['stats'])
def stats(m):
    bot.reply_to(m,f"Botdan hozirda {get_count()}ta foydalanuvchi foydalanadi.")

@bot.message_handler(commands=['ad'])
def ad(m):
    if str(m.from_user.id) in ADMINS:
        bot.reply_to(m,f"Reklama uchun postni menga yuboring.")
        bot.register_next_step_handler(m,ad2)

def ad2(m):
    for i in get_all():
        try:
            bot.copy_message(i[0],m.chat.id,m.id)
        except Exception as e:
            print(e)
# @bot.message_handler(is_admin=True,commands=['ban'])
# def ban(m):
#     bot.ban_chat_member(m.chat.id,m.reply_to_message.from_user.id)
#     bot.delete_message(m.chat.id,m.id)

# @bot.message_handler(is_admin=True,content_types=['text'],func=lambda m: m.text.startswith('/mute'))
# def mute(m):
#     s=m.text.split()
#     bot.restrict_chat_member(m.chat.id,m.reply_to_message.from_user.id,time.time()+int(s[1]) if len(s)>0 else None)
#     bot.delete_message(m.chat.id,m.id)

# @bot.message_handler(is_admin=True,content_types=['text'],func=lambda m: m.text.startswith('/unmute'))
# def unmute(m):
#     s=m.text.split()
#     bot.restrict_chat_member(m.chat.id,m.reply_to_message.from_user.id,time.time()+5)
#     bot.delete_message(m.chat.id,m.id)

@bot.message_handler(is_subscribed=True,content_types=['text'],func=lambda m: m.text.startswith('/photo'))
def rasm(m):
    try:
        bot.send_photo(m.chat.id,photo=gen_img(' '.join(m.text.split()[1:])),reply_to_message_id=m.id)
    except:
        bot.send_photo(m.chat.id,photo=gen_img(' '.join(m.text.split()[1:])))

@bot.message_handler(is_subscribed=True,content_types=['text'],func=lambda m: m.text.startswith('/ask'),chat_types=['group','supergroup'])
def rec_gr(m):
    try:
        bot.reply_to(m,req(' '.join(m.text.split()[1:])))
    except:
        bot.send_mess(m,req(' '.join(m.text.split()[1:])))

@bot.message_handler(is_subscribed=True,content_types=['text'],chat_types=['private'])
def rec_pr(m):
    bot.reply_to(m,req(m.text))

@bot.message_handler(func=lambda m: True)
def check(m):
    if bot.get_chat_member("@milliai",m.from_user.id).status not in ['administrator','creator','member']:
        bot.delete_message(m.chat.id,m.id)
        bot.send_message(m.chat.id,f"Assalomu alaykum {m.chat.first_name} @milliaibot dan foydalanishdan oldin bizning rasmiy telegram sahifamizga va homiy telegram kanaliga obuna bo'ling",reply_markup=markup)


bot.add_custom_filter(IsSubscribed())
bot.add_custom_filter(IsAdmin())

if __name__=='__main__':
    bot.infinity_polling()
