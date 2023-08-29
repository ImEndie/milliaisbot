import openai
from vars import OPENAI_KEY,HF_API_TOKEN,HOST
from googletrans import Translator
import requests

translator = Translator()
api_keys=OPENAI_KEY.copy()
def change_api():
    api_keys.append(api_keys.pop(0))
    openai.api_key=api_keys[0]

openai.api_key = api_keys[0]
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

history=[
            {"role": "system", "content": "Hi, your name is MilliAI and you are created by TRONX-STD and Wlaneakia teams.Hayotbek Rakhimov a.k.a Instar is the only invincible MC in the world of UzRap. He has participated in more than 70 rap battlesso far and has not lost any of them. He is recognized by Uzrap, the \"number one\" Rap Battle MC in Uzbekistan."},
            {"role": "assistant", "content": "I got it. Thank you for name"},
        ]

def req(m):
    if type(m)==type(''):
        message=m
    else:
        message=m.text
    try:
        if "kod" in message or "cod" in message or "dastur" in message:
            otm=history.copy()
            otm.append({'role':'user','content':message})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=otm
            )
            response=response['choices'][0]['message']['content']
            return response
        r=translator.translate(text=message).text
        print(r)
        otm=history.copy()
        otm.append({'role':'user','content':r})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=otm
        )
        
        response=response['choices'][0]['message']['content']
        print(response)
        r=translator.translate(text=response,dest='uz').text
        print(r)
        return r
    except Exception as e:
        print(e)
        change_api()
        return "Botda so'rovlar soni cheklangan. Iltimos birozdan so'ng qayta urinib ko'ring. Muammo bo'lsa admin bilan bog'laning."

def replace_wrapped_text(string: str,start_marker,end_marker):
    new_text='teht'
    replaceds=[]
    start_index = string.find(start_marker)
    # print(start_index)
    while start_index != -1:
        end_index = string.find(end_marker, start_index + 1)
        
        if end_index != -1:
            wrapped_text = string[start_index: end_index+1]
            replaceds.append(wrapped_text)
            string = string.replace(wrapped_text, new_text)
        start_index = string.find(start_marker, start_index + 1)
    
    return [string,replaceds]

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
    t=translator.translate(text=txt,dest='en').text
    try:
        fname=f"{msg.chat.id}_{msg.id}.png"
        response = requests.request("POST", HF_API_URL, headers=HF_HEADERS, data=t)
        with open(fname,"wb") as f:
            f.write(response.content)
        return fname
    except Exception as e:
        print(e)
        return "No'malum xatolik yuz berdi. Iltimos admin bilan bog'laning."

# def gen_img(msg):
#     t=msg.text
#     print(t)
#     try:
#         r=translator.translate(text=t)
#         response = openai.Image.create(
#             prompt=r.text,
#             n=1,
#             size="1024x1024"
#         )
#         image_url = response['data'][0]['url']
#         return image_url
#     except Exception as e:
#         print(e)
#         change_api()
#         if "Your request was rejected as a result of our safety system." in str(e): return "Bu turdagi so'rov taqiqlangan."
#         return "Botda so'rovlar soni cheklangan. Iltimos birozdan so'ng qayta urinib ko'ring. Muammo bo'lsa admin bilan bog'laning."
