import openai
from vars import OPENAI_KEY,HF_API_TOKEN,HOST
import requests

client=openai.OpenAI()

HF_API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

def req(m):
    if type(m)==type(''):
        message=m
    else:
        message=m.text
    try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{'role':'user','content':message}]
            )
            response=response.choices[0].message.content
            return response

    except Exception as e:
        print(e)
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