import os
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from pyowm import OWM

# Load environment variables from .env file
load_dotenv()

# OpenWeatherMap API key
owm = OWM(os.getenv('OWM_API_KEY'))

# Telegram API credentials
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

# Telegram Bot credentials
Pumba = int(os.getenv('PUMBA_BOT_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')

#  Your personal Telegram account ID
my_id = int(os.getenv('MY_ID'))

# Chat and channel IDs
chat_id_pumba = int(os.getenv('CHAT_ID_PUMBA'))
chat_id_souz = int(os.getenv('CHAT_ID_SOUZ'))
chat_id_ss = int(os.getenv('CHAT_ID_SS'))
chat_id_answars = int(os.getenv('CHAT_ID_ANSWARS'))

# Path to database
directory = 'database'
os.makedirs(directory, exist_ok=True) 
db_path = f'{directory}/bot_database.db'

# Directories
os.makedirs('chats', exist_ok=True) 

# Initialize Telegram client
session_path = 'telethon/telethon'
session_file = Path(session_path)

# Create sessions directory if it doesn't exist
session_file.parent.mkdir(parents=True, exist_ok=True)

bot = TelegramClient(str(Path(session_path)), API_ID, API_HASH).start(bot_token=BOT_TOKEN)