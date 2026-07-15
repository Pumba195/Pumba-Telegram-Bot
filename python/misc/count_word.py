import json
from config.config import bot,BOT_ID
import os


# Command to display the user's word count
async def my_words(event):
	if event.chat_id < 0:
		people = await bot.get_entity(event.sender_id)
		try:
			directory = 'chats'
			os.makedirs(directory, exist_ok=True) 
			chat = f'{directory}/{event.chat_id}.json'

			try:
				with open(chat, 'r') as file:
					users = json.load(file)
			except FileNotFoundError:
				pass

			for user in users:
				if user['id'] == people.id:
					await event.reply(f"Ти написав <b>{user['word_count']}</b> слів, так тримати😀!", parse_mode = 'html')
		except UnboundLocalError:
			await bot.send_message(event.chat.id, f"Ви не написали жодго слова, або не видали права адміністратора, виправляйтесь😉")
	else:
		await event.reply("Ця команда працює лише в групах!")

# Command to display the top 10 users by word count
async def top_ten(event):
	if event.chat_id < 0:
		try:
			directory = 'chats'
			os.makedirs(directory, exist_ok=True) 
			chat = f'{directory}/{event.chat_id}.json'

			try:
				with open(chat, 'r') as file:
					users = json.load(file)
			except FileNotFoundError:
				users = []


			iter = 0
			emoji = '🟡'
			top_users= ''

			sorted_users = sorted(users, key=lambda x: x['word_count'], reverse=True)

			for user in users:

				if sorted_users[iter]['username']:
					people = sorted_users[iter]['username']
				else:
					people = sorted_users[iter]['id']
					
				if iter < 10:
					top_users += f"\n<b>{emoji}{people}:</b> <i>{sorted_users[iter]['word_count']} слів</i>" 
					iter += 1
				if iter <= 11:
					emoji = '🔴'
				if iter <= 4:
					emoji = '🟠'
			
			if top_users != '':
				await bot.send_message(event.chat.id, f"<b>🏆Топ-10</b> найактивніших людей з цього чату:\n{top_users}", parse_mode = 'html')

		except UnboundLocalError:
			await bot.send_message(event.chat.id, f"Ви не написали жодного слова, або не видали права адміністратора, виправляйтесь😉")
		
		try:
			try:
				with open(chat, 'r') as file:
					users = json.load(file)
			except FileNotFoundError:
				users = []
			participants = await bot.get_participants(event.chat_id)
			
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
	else:
		await event.reply("Ця команда працює лише в групах!")