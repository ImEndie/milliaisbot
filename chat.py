import openai
from vars import OPENAI_KEY
from googletrans import Translator
translator = Translator()

openai.api_key = OPENAI_KEY  # Replace with your OpenAI API key

history=[
            {"role": "system", "content": "Hi, your name is MilliAI and you are created by Wlaneakia team."},
            {"role": "assistant", "content": "Thank you for name"},
        ]

def req(message):
    otm=history.copy()
    otm.append({'role':'user','content':translator.translate(message)})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=otm
    )
    if response['choices'][0]['message']['content']:
        history.append(otm[-1])
        history.append(response['choices'][0]['message'])
        return translator.translate(response['choices'][0]['message']['content'],dest='uz')
    else:
        return "Kechirasiz, savolingizni tushunmadim"

def gen_img(t):
    response = openai.Image.create(
        prompt=translator.translate(t),
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url
