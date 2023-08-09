import openai
from vars import OPENAI_KEY
import random
from googletrans import Translator
translator = Translator()

openai.api_key = random.choice(OPENAI_KEY)  # Replace with your OpenAI API key

history=[
            {"role": "system", "content": "Hi, your name is MilliAI and you are created by TRONX-STD and Wlaneakia teams."},
            {"role": "assistant", "content": "Thank you for name"},
        ]

def req(message):
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
    

def gen_img(t):
    r=translator.translate(text=t)
    response = openai.Image.create(
        prompt=r.text,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url
