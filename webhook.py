from flask import Flask,request,send_file
from bot import bot
import telebot
from vars import BOT_TOKEN
from main import *

app=Flask(__name__)


@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@app.route("/")
def index():
    return "!", 200

@app.route("/images/{fname}")
def image(fname):
    try:
        return send_file(fname)
    except Exception as e:
        print(e)
        return "error"

if __name__=='__main__':
    app.run('0.0.0.0',8080,debug=False)