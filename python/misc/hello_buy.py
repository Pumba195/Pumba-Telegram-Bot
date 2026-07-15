import json
import os

from misc.weather import save_data_weather,load_data_weather
from misc.swear import save_data_word,load_data_word
from config.config import Pumba,bot



# Hello/Buy
# Function for saving data to a file
async def save_data_all(data):
	directory = 'support'
	os.makedirs(directory, exist_ok=True) 
	file_path = f'{directory}/all_chats.json'
	
	with open(file_path, 'w') as f:
		json.dump(data, f)

# Function for loading data from a file
async def load_data_all():
    try:
        with open('support/all_chats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Hello
async def welcome_new_members(event):
	new_member = event.user

	directory = 'chats'
	os.makedirs(directory, exist_ok=True) 
	chat = f'{directory}/{event.chat_id}.json'

	if new_member.id == Pumba:

		all_chats = await load_data_all()
		chat_id = event.chat_id

		if chat_id < 0:
			if chat_id not in all_chats:
				all_chats.append(chat_id)
				await save_data_all(all_chats)
		try:
			try:
				with open(chat, 'r') as file:
					users = json.load(file)
			except FileNotFoundError:
				users = []

			participants = await bot.get_participants(chat_id)
			
			for people in participants:
				if people.bot:
					for user in users:
						if user['id'] == people.id:
							time_users = [user for user in users if user['id'] != people.id]
							with open(chat, 'w') as file:
								json.dump(time_users, file)
							with open(chat, 'r') as file:
								users = json.load(file)
				else:
					if not any(user['id'] == people.id for user in users):
						users.append({'id': people.id, 'username': people.username, 'word_count': 0})
						with open(chat, 'w') as file:
							json.dump(users, file)
						with open(chat, 'r') as file:
							users = json.load(file)
					for user in users:
						if user['id'] == people.id:
							user['username'] = people.username
							with open(chat, 'w') as file:
								json.dump(users, file)
							with open(chat, 'r') as file:
								users = json.load(file)

			left_people = True
			for user in users:
				for people in participants:
					if user['id'] == people.id:
						left_people = False

				if left_people == True:
					kik_id = user['id']
					time_users = [user for user in users if user['id'] != kik_id]
					with open(chat, 'w') as file:
						json.dump(time_users, file)
					with open(chat, 'r') as file:
						users = json.load(file)
						
				left_people = True
		except:
			pass
		await bot.send_message(event.chat.id, f"Привіт всім, я <b>бот-помічник <i>Пумба</i></b>😊! \
Для більш детального ознайомлення з моїм функціоналом скористайтеся командою <b>\"/info\"</b>. \
<b>Перед початком експлуатації — назначте мене адміністратором чату😏</b>\n👇<i>Телеграм канал Пумби👇\nhttps://t.me/pumba_news_channel </i>", parse_mode = 'html')
		return
	
	if new_member.id:
		if new_member.bot:
			await bot.send_message(event.chat.id, f"У нас поповненя, до чату додали бота <b>{new_member.first_name}</b>!😒", parse_mode = 'html')
			return
		
		directory = 'chats'
		os.makedirs(directory, exist_ok=True) 
		chat_chat = f'{directory}/{event.chat_id}.json'

		try:
			with open(chat_chat, 'r') as file:
				users = json.load(file)
		except FileNotFoundError:
			users = []
		
		if not any(user['id'] == new_member.id for user in users):
			users.append({'id': new_member.id, 'username': new_member.username, 'word_count': 0})
			with open(chat_chat, 'w') as file:
				json.dump(users, file)
			
		for user in users:
			if user['id'] == new_member.id:
				user['username'] = new_member.username
				with open(chat_chat, 'w') as file:
					json.dump(users, file)
				break
	
	if event.user_joined:
		await bot.send_message(event.chat.id, f"У нас поповнення, увійшов ще один участник👋! Його ім`я — <b>{new_member.first_name}</b>, знайомтеся!😉", parse_mode = 'html')
	if event.user_added:
		await bot.send_message(event.chat.id, f"У нас поповнення, додали ще одного учатника👋! Його ім`я — <b>{new_member.first_name}</b>, знайомтеся!😉", parse_mode = 'html')

# Buy
async def goodbye_member(event):
	chat_id = event.chat_id

	left_chat_member = event.user

	if left_chat_member.id == Pumba:
		enabled_chats = await load_data_word()
		weather_chats = await load_data_weather()
		all_chats = await load_data_all()

		try:
			os.remove(f'chats/{chat_id}.json')
		except FileNotFoundError:
			print("Error ID")

		try:
			os.remove(f'tic_tac_toe/TT{chat_id}.json')
		except FileNotFoundError:
			print("Error TT-ID")
		
		try:
			enabled_chats.remove(chat_id)
			await save_data_word(enabled_chats)
		except ValueError:
			print("Error enabled_chats")

		try:
			del weather_chats[str(chat_id)]
			await save_data_weather(weather_chats)
		except KeyError:
			print("Error weather_chats")

		try:
			all_chats.remove(chat_id)
			await save_data_all(all_chats)
		except ValueError:
			print("Error all_chats")

		return
	
	if left_chat_member.id:
		if left_chat_member.bot:
			await bot.send_message(event.chat.id, f"Нас покинув бот <b>{left_chat_member.first_name}</b>, мінус конкурент!😁", parse_mode = 'html')
			return
		
		directory = 'chats'
		os.makedirs(directory, exist_ok=True) 
		chat_chat = f'{directory}/{event.chat_id}.json'
		
		user_id_to_remove = left_chat_member.id

		with open(chat_chat, 'r') as file:
			users = json.load(file)
		
		users = [user for user in users if user['id'] != user_id_to_remove]

		with open(chat_chat, 'w') as file:
			json.dump(users, file)
			
	if event.user_left:
		await bot.send_message(event.chat.id, f"<b>{left_chat_member.first_name}</b> покинув нас!😢", parse_mode = 'html')
	if event.user_kicked:
		await bot.send_message(event.chat.id, f"Участника <b>{left_chat_member.first_name}</b> було вигнано!😢", parse_mode = 'html')