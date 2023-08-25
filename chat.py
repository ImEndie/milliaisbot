import openai
from vars import OPENAI_KEY
from googletrans import Translator

translator = Translator()
api_keys=OPENAI_KEY.copy()
def change_api():
    api_keys.append(api_keys.pop(0))
    openai.api_key=api_keys[0]

openai.api_key = api_keys[0] # Replace with your OpenAI API key

history=[
            {"role": "system", "content": "Hi, your name is MilliAI and you are created by TRONX-STD and Wlaneakia teams."},
            {"role": "assistant", "content": "Thank you for name"},
            {"role": "system", "content": "Hayotbek Rakhimov a.k.a Instar is the only invincible MC in the world of UzRap. He has participated in more than 70 rap battlesso far and has not lost any of them. He is recognized by Uzrap, the \"number one\" Rap Battle MC in Uzbekistan."},
            {"role": "assistant", "content": "I got it"}
        ]

def req(message):
    print(message)
    try:
        r=translator.translate(text=message)
        otm=history.copy()
        otm.append({'role':'user','content':r.text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=otm
        )
        if response['choices'][0]['message']['content']:
            history.append(otm[-1])
            history.append(response['choices'][0]['message'])
            r=translator.translate(text=response['choices'][0]['message']['content'],dest='uz')
            return r.text
        else:
            return "Kechirasiz, savolingizni tushunmadim"
    except Exception as e:
        print(e)
        change_api()
        return "Iltimos qayta urinib ko'ring. Muammo bo'lsa admin bilan bog'laning."
    

def gen_img(t):
    print(t)
    try:
        r=translator.translate(text=t)
        response = openai.Image.create(
            prompt=r.text,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(e)
        change_api()
        if "Your request was rejected as a result of our safety system." in str(e): return "Bu turdagi so'rov taqiqlangan."
        return "Iltimos keyinroq urinib ko'ring. Muammo bo'lsa /contact buyrug'i yordamida admin bilan bog'laning."
