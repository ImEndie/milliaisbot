import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
OPENAI_KEY=os.getenv('OPENAI_KEY').split('.')
PG_URI=os.getenv('PG_URI')
ADMINS=os.getenv('ADMINS').split(':')
HF_API_TOKEN=os.getenv("HF_API_TOKEN")
HOST=os.getenv("HOST")