from bot import bot
from chat import gen_img, req
from filters import IsAdmin , IsSubscribed
from database import ins,get_all,get_count
from vars import ADMINS
from keyboards import Keyboards
from telebot.types import Message,CallbackQuery

keyboards=Keyboards(bot)

@bot.message_handler(content_types=['new_chat_members'])
def new_chat_members(m: Message):
    for i in m.new_chat_members:
        bot.send_chat_action(m.chat.id,'typing')
        bot.send_message(m.chat.id,f"Assalomu alaykum {i.first_name}!\nGuruhga xush kelibsiz.")
    try:
        bot.delete_message(m.chat.id,m.id)
    except Exception as e:
        print(e)

@bot.message_handler(is_subscribed=True,commands=['start'])
def start(m: Message):
    ins(m.from_user.id)
    bot.send_chat_action(m.chat.id,'typing')
    bot.send_message(
        m.chat.id,
        f"Assalomu alaykum {m.from_user.first_name}! Botdan foydalanish uchun /help buyrug'idan foydalaning.",
        reply_markup=keyboards.getMainButtons() if m.chat.type=='private' else None
    )

@bot.message_handler(is_subscribed=True,commands=['help'])
def help(m: Message):
    bot.send_chat_action(m.chat.id,'typing')
    bot.reply_to(m,"/ask — savollarga javob topishda va ko'plab boshqa muammolarni yechishda yordam beradi. Foydalanish uchun /ask buyrug'i bilan birgalikda xabar kiriting.\nMasalan: ``` /ask Salom milliai!``` \n/photo — rasmlarni osongina yaratish uchun yordam beradi. Foydalanish uchun /photo buyrug'i bilan birgalikda xabarni kiriting.\nMasalan: ``` /photo offisda ishlayotgan mushuk ```")

@bot.message_handler(chat_types=['private'],content_types=['text'],func=keyboards.statsFilter)
def stats(m: Message): keyboards.statsFunc(m)

@bot.message_handler(commands=['ad'])
def ad(m: Message):
    if str(m.from_user.id) in ADMINS:
        bot.send_chat_action(m.chat.id,'typing')
        msg=bot.reply_to(m,f"Reklama uchun postni menga yuboring.")
        bot.register_next_step_handler(msg,ad2)

def ad2(m: Message):
    for i in get_all():
        try:
            bot.copy_message(i[0],m.chat.id,m.id)
        except Exception as e:
            print(e)

@bot.message_handler(chat_types=['private'],content_types=['text'],func=keyboards.contactFilter)
def contact(m: Message): keyboards.contactFunc(m)

@bot.message_handler(is_subscribed=True,content_types=['text'],func=lambda m: m.text.startswith('/photo'),chat_types=['group','supergroup'])
def rasm(m: Message):
    keyboards.genFunc2(m)

@bot.message_handler(is_subscribed=True,content_types=['text'],func=keyboards.genFilter)
def rasm_pr(m: Message): keyboards.genFunc(m)

@bot.message_handler(is_subscribed=True,content_types=['text'],func=lambda m: m.text.startswith('/ask'),chat_types=['group','supergroup'])
def rec_gr(m: Message):
    bot.send_chat_action(m.chat.id,'typing')
    r=req(' '.join(m.text.split()[1:]))
    try:
        bot.reply_to(m,r)
    except:
        bot.send_message(m.chat.id,r)

@bot.message_handler(is_subscribed=True,content_types=['text'],chat_types=['private'],func=keyboards.askFilter)
def rec_pr(m: Message): keyboards.askFunc(m)

@bot.message_handler(content_types=['text'],chat_types=['private'],func=keyboards.requestFilter)
def reqhandler(m: Message): keyboards.requestFunc(m)

@bot.message_handler(chat_types=['private'],func=keyboards.replyFilter)
def reply(m: Message): keyboards.reply(m)

@bot.callback_query_handler(keyboards.checkFilter)
def check_subscription(cb: CallbackQuery): keyboards.checkFunc(cb)

@bot.message_handler(func=lambda m: True,chat_types=['private'])
def check(m: Message):
    if not IsSubscribed.check(m):
        try:
            bot.delete_message(m.chat.id,m.id)
        except Exception as e:
            print(e)
        bot.send_chat_action(m.chat.id,'typing')
        bot.send_message(m.chat.id,f"Assalomu alaykum {m.from_user.first_name}!\n⚠️ @milliaibot dan foydalanishdan oldin bizning rasmiy telegram sahifamizga va homiy telegram kanaliga obuna bo'ling. Soʻng botni qayta boshlashni unutmang!",reply_markup=keyboards.getChannelButton())


bot.add_custom_filter(IsSubscribed())
bot.add_custom_filter(IsAdmin())

if __name__=='__main__':
    bot.infinity_polling()
