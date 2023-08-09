import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
OPENAI_KEY=os.getenv('OPENAI_KEY')
PG_URI=os.getenv('PG_URI')
ADMINS=os.getenv('ADMINS').split(':')