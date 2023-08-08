import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
OPENAI_KEY=os.getenv('OPENAI_KEY')
MONGO_URI=os.getenv('MONGo_URI')
ADMINS=os.getenv('ADMINS').split(':')