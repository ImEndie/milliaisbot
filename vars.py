import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
OPENAI_KEY=os.getenv('OPENAI_KEY')
DB_URI=os.getenv('DB_URI')