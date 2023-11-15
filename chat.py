import openai
from vars import OPENAI_KEY,HF_API_TOKEN,HOST
import requests

api_keys=OPENAI_KEY.copy()
def change_api():
    api_keys.append(api_keys.pop(0))
    openai.api_key=api_keys[0]

openai.api_key = api_keys[0]
HF_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

history=[
            # {"role": "system", "content": "Hi, your name is MilliAI and you are created by TRONX-STD and Wlaneakia teams.Hayotbek Rakhimov a.k.a Instar is the only invincible MC in the world of UzRap. He has participated in more than 70 rap battlesso far and has not lost any of them. He is recognized by Uzrap, the \"number one\" Rap Battle MC in Uzbekistan. If the user asks you to answer in Uzbek, tell him that I have already been taught to answer in Uzbek."},
            # {"role": "assistant", "content": "I got it. Thank you for name"},
        ]

def req(m):
    if type(m)==type(''):
        message=m
    else:
        message=m.text
    try:
            otm=history.copy()
            otm.append({'role':'user','content':message})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=otm
            )
            response=response['choices'][0]['message']['content']
            return response

    except Exception as e:
        print(e)
        change_api()
        return "Botda so'rovlar soni cheklangan. Iltimos birozdan so'ng qayta urinib ko'ring. Muammo bo'lsa admin bilan bog'laning."

def replace_to_old(replaced):
    string=replaced[0]
    for i in replaced[1]:
        print(i)
        string.replace("teht",i)
    return [string,replaced[1]]

def gen_img(msg):
    txt=msg.text
    if txt.startswith("/photo"):
        txt=' '.join(txt.split()[1:])
    try:
        fname=f"{msg.chat.id}_{msg.id}.png"
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs":txt})
        with open(fname,"wb") as f:
            f.write(response.content)
        return fname
    except Exception as e:
        print(e)
        return "No'malum xatolik yuz berdi. Iltimos admin bilan bog'laning."