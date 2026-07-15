import json
import os

from config.config import bot



# Eneble swear words
# Function for saving data to a file
async def save_data_word(data):
    directory = 'support'
    os.makedirs(directory, exist_ok=True) 
    file_path = f'{directory}/enabled_chats.json'

    with open(file_path, 'w') as f:
        json.dump(data, f)

# Function for loading data from a file
async def load_data_word():
    try:
        with open('support/enabled_chats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
	
# Command to enable word responses
async def enable_greetings(event):
    enabled_chats = await load_data_word()
    chat_id = event.chat_id
    if chat_id < 0:
        if chat_id not in enabled_chats:
            enabled_chats.append(chat_id)
            await save_data_word(enabled_chats)
            await bot.send_message(chat_id, "Відповіді та підйоби увімкнені😁\nАктивні слова — <i>\"/list_words\"</i>", parse_mode = 'html')
        else:
            await bot.send_message(chat_id, "Відповіді і так були увімкнені😁\nАктивні слова — <i>\"/list_words\"</i>")
    else:
        await bot.send_message(chat_id, "Ця команда працює лише в групах")
	
# Command to disable word responses
async def disable_greetings(event):
    enabled_chats = await load_data_word()
    chat_id = event.chat_id
    if chat_id < 0:
        if chat_id in enabled_chats:
            enabled_chats.remove(chat_id)
            await save_data_word(enabled_chats)
            await bot.send_message(chat_id, "Відповіді та підйоби вимкнені😒")
        else:
            await bot.send_message(chat_id, "Відповіді і так були вимкнені😒")
    else:
        await bot.send_message(chat_id, "Ця команда працює лише в групах")