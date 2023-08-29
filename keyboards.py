from telebot.types import Message,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery
from telebot import TeleBot
from chat import gen_img, req
from database import get_count
from filters import IsSubscribed
from vars import ADMINS

class Keyboards:
    def __init__(self,bot: TeleBot):
        self.bot=bot
    def getMainButtons(self):
        markup=ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(
            KeyboardButton("Savol berish ❔")
        )
        markup.add(
            KeyboardButton("Rasm generatsiya qilish 🖼")
        )
        markup.add(
            KeyboardButton("Aloqa ☎️"),
            KeyboardButton("Murojaat 📝")
        )
        markup.add(
            KeyboardButton("Statistika 📊")
        )
        return markup
    def getChannelButton(self):
        markup=InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("milli ai","https://t.me/milliai"),row_width=1)
        markup.add(InlineKeyboardButton("TRONX-STD","https://t.me/tronx_std"),row_width=1)
        markup.add(InlineKeyboardButton("Tekshirish 🔁",callback_data="check"),row_width=1)
        return markup
    def anotherFilter(self,m):
        if m.text.startswith("/"):
            return True
        if self.askFilter(m): 
            self.askFunc(m)
            return True
        if self.contactFilter(m):
            self.contactFunc(m)
            return True
        if self.genFilter(m):
            self.genFunc(m)
            return True
        if self.requestFilter(m):
            self.requestFunc(m)
            return True
        if self.statsFilter(m):
            self.statsFunc(m)
            return True
        return False
    def checkFunc(self,cb: CallbackQuery):
        subscribed = IsSubscribed.check(cb)
        if subscribed:
            self.bot.delete_message(cb.message.chat.id,cb.message.id)
            self.bot.send_chat_action(cb.message.chat.id,'typing')
            self.bot.send_message(cb.message.chat.id,"🖥 Asosiy menyudasiz",reply_markup=self.getMainButtons())
        else:
            self.bot.send_chat_action(cb.message.chat.id,'typing')
            self.bot.answer_callback_query(cb.id,"⚠️ Botdan foydalanish uchun kanallarga obuna bo'ling.",show_alert=True)
    
    def askFunc(self,m: Message):
        self.bot.send_chat_action(m.chat.id,'typing')
        msg=self.bot.send_message(m.chat.id,"""Bu bo'lim sizga savollarga javob topishda va ko'plab boshqa muammolarni yechishda yordam beradi. Foydalanish uchun biron bir matn kiriting.

Masalan:  ``` Salom milliai! ```""")
        self.bot.register_next_step_handler(msg,self.askFunc2)
    def askFunc2(self,m: Message):
        if self.anotherFilter(m):
            return
        self.bot.send_chat_action(m.chat.id,'typing')
        msg=self.bot.send_message(m.chat.id,"🤔 Oʻylayapman. \nBiroz kuting...")
        r=req(m)
        try:
            self.bot.send_chat_action(m.chat.id,'typing')
            msg2=self.bot.send_message(m.chat.id,r,reply_to_message_id=m.id)
            self.bot.register_next_step_handler(msg2,self.askFunc2)
        except:
            self.bot.send_chat_action(m.chat.id,'typing')
            msg2=self.bot.send_message(m.chat.id,r)
            self.bot.register_next_step_handler(msg2,self.askFunc2)
        try:
            self.bot.delete_message(m.chat.id,msg.id)
        except Exception as e:
            print(e)
    def genFunc(self,m: Message):
        self.bot.send_chat_action(m.chat.id,'typing')
        msg=self.bot.send_message(m.chat.id,"""Bu bo'lim sizga rasmlarni osongina yaratish uchun yordam beradi. 
Foydalanish uchun rasm haqidagi matnni kiriting.

Masalan:  ``` Offisda ishlayotgan mushuk. ```""")
        self.bot.register_next_step_handler(msg,self.genFunc2)
    def genFunc2(self,m: Message):
        if self.anotherFilter(m):
            return
        self.bot.send_chat_action(m.chat.id,'typing')
        msg=self.bot.send_message(m.chat.id,"✏️ Rasm chizyapman.\nBiroz kuting.")
        r=gen_img(m)
        print(r)
        try:
            try:
                self.bot.send_chat_action(m.chat.id,'upload_photo')
                msg2=self.bot.send_photo(m.chat.id,photo=open(r,"rb"),reply_to_message_id=m.id)
                self.bot.register_next_step_handler(msg2,self.genFunc2)
            except:
                msg2=self.bot.send_photo(m.chat.id,photo=open(r,"rb"))
                self.bot.register_next_step_handler(msg2,self.genFunc2)
        except Exception as e:
            self.bot.send_chat_action(m.chat.id,'typing')
            self.bot.send_message(m.chat.id,r)
            print(e)
        try:
            self.bot.delete_message(msg.chat.id,msg.id)
        except Exception as e:
            print(e)
    def contactFunc(self,m: Message):
        self.bot.send_chat_action(m.chat.id,'typing')
        msg=self.bot.reply_to(m,f"📧 Xabaringiz va foydalanuvchi nomingizni yozib qoldiring. Adminlar tez orada aloqaga chiqishadi.")
        self.bot.register_next_step_handler(msg,self.contactFunc2)
    def contactFunc2(self,m: Message):
        if self.anotherFilter(m):
            return
        for i in ADMINS:
            try:
                self.bot.forward_message(i,m.chat.id,m.id)
            except Exception as e:
                print(e)
    def reply(self,m: Message):
        try:
            self.bot.copy_message(m.reply_to_message.forward_from.id,m.chat.id,m.id,reply_to_message_id=m.reply_to_message.forward_from_message_id)
        except Exception as e:
            print(e)
            self.bot.copy_message(m.reply_to_message.forward_from.id,m.chat.id,m.id)
    def requestFunc(self,m: Message):
        self.bot.send_chat_action(m.chat.id,'typing')
        self.bot.send_message(m.chat.id,"📨 Reklama va takliflar uchun murojaat:\n@Naruzzo\n@ImEndie")
    def statsFunc(self,m: Message):
        self.bot.send_chat_action(m.chat.id,'typing')
        self.bot.send_message(m.chat.id,f"📊 Botda ayni paytda {get_count()}ta obunachi mavjud.")
    
    def checkFilter(self,cb: CallbackQuery):
        return cb.data=="check"
    def askFilter(self,m: Message):
        return m.text=="Savol berish ❔"
    def genFilter(self,m: Message):
        return m.text=="Rasm generatsiya qilish 🖼"
    def contactFilter(self,m: Message):
        return m.text=="Aloqa ☎️"
    def replyFilter(self,m: Message):
        cond = m.reply_to_message is not None and str(m.chat.id) in ADMINS
        return m.reply_to_message.forward_from if cond else False
    def requestFilter(self,m: Message):
        return m.text=="Murojaat 📝"
    def statsFilter(self,m: Message):
        return m.text=="Statistika 📊"
