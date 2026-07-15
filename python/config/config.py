import os
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from pyowm import OWM

# Load environment variables from .env file
load_dotenv()

# OpenWeatherMap API key
OWM_API = OWM(os.getenv('OWM_API_KEY'))

# Telegram API credentials
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')

# Telegram Bot credentials
BOT_ID = int(os.getenv('BOT_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')

#  Your personal Telegram account ID
MY_ID = int(os.getenv('MY_ID'))

# Chat and channel IDs
ADMIN_CHAT_ID = int(os.getenv('ADMIN_CHAT_ID'))

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