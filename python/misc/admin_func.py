import json
import sqlite3
import os

from config.config import bot,my_id,chat_id_pumba,db_path
from misc.support import page_start_admin
from misc.hello_buy import load_data_all
from misc.swear import load_data_word



# Distribution
async def forward_send_message(event):
	if event.text == '🔊Розсилка📢':
		return
	
	bot.remove_event_handler(forward_send_message)

	admins = await load_data_adm()
	
	if event.chat.id in admins:
		if event.text == '◀️Назад':
			return

		if event.text:
			user = await bot.get_entity(event.sender_id)
			await bot.send_message(chat_id_pumba, f"Адмін <b>{user.first_name} ({user.id})</b> <u>ЗАПУСТИВ РОЗСИЛКУ</u> повідомлення:\n\n<i>{event.text}</i>", parse_mode = 'html')

			try:
				all_chats = await load_data_all()
				textt = event.text

				for chats in all_chats:
					try:
						chat_idd = int(chats)
						await bot.send_message(chat_idd, textt)
					except:
						continue
				await bot.send_message(event.chat.id, "Повідомлення розіслано, все добре!😈", buttons=await page_start_admin())
				return
			except:
				await bot.send_message(event.chat.id, "Щось пішло не так👿!", buttons=await page_start_admin())

				return
		else:
			await bot.send_message(event.chat.id, "Розсилати мажна лише текстові повідомлення!👿", buttons=await page_start_admin())
			return

# Answer
async def answer_message(event):
	if event.text == '❔Відповідь❓':
		return
	
	admins = await load_data_adm()
	bot.remove_event_handler(answer_message)
	
	if event.chat.id in admins:
		if event.text == '◀️Назад':
			return
		
		try:
			message_text = event.text.split(' ', 1)

			idd = int(message_text[0])
			text = f"<b>Відповідь від адміністратора бота:</b>\n\n<i>{message_text[1]}</i>"
			await bot.send_message(idd, text, parse_mode = 'html')
			await bot.send_message(event.chat.id, "Відповідь було відправлено😈", buttons=await page_start_admin())

			user = await bot.get_entity(event.sender_id)
			await bot.send_message(chat_id_pumba, f"Адмін <b>{user.first_name} ({user.id})</b> <u>ВІДПОВІВ КОРИСТУВАЧУ</u> <i>{str(idd)}</i> повідомленням:\n\n<i>{event.text[11:]}</i>", parse_mode = 'html')

			return
		except:
			await bot.send_message(event.chat.id, "Щось пішло не так👿!", buttons=await page_start_admin())
			return

# Function for saving data to a file
async def save_data_adm(data):
	directory = 'support'
	os.makedirs(directory, exist_ok=True) 
	chat = f'{directory}/admins.json'

	with open(chat, 'w') as f:
		json.dump(data, f)

# Function for loading data from a file
async def load_data_adm():
    try:
        with open('support/admins.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Registration of admins
async def register_admin_real(event):
	admins = await load_data_adm()
	if event.chat.id == my_id:
		try:
			id_new = int(event.text[16:])
			if id_new not in admins:
				admins.append(id_new)
				await save_data_adm(admins)
				await bot.send_message(my_id, "Нового адміна зареєстровано😈!")
				
				await bot.send_message(chat_id_pumba, f"Адмін <b>Максімка</b> <u>ЗАРЕЄСТРУВАВ</u> нового адміністратора - <i>{id_new}</i>", parse_mode = 'html')
			else:
				await bot.send_message(my_id, "Цей адмін вже зареєстрований😈!")
		except:
			await bot.send_message(my_id, "Щось пішло не так👿!")
	return

# Removing admins
async def delate_admin_real(event):
	admins = await load_data_adm()
	if event.chat.id == my_id:
		try:
			id_new = int(event.text[14:])
			if id_new in admins:
				admins.remove(id_new)
				await save_data_adm(admins)
				await bot.send_message(my_id, "Адміна було видалено😈!")
				
				await bot.send_message(chat_id_pumba, f"Адмін <b>Максімка</b> <u>ВИДАЛИВ</u> адміністратора - <i>{id_new}</i>", parse_mode = 'html')
			else:
				await bot.send_message(my_id, "Цієї людини і не було в адмінах😈!")
		except:
			await bot.send_message(my_id, "Щось пішло не так👿!")
	return

# Admin message
async def admin_panel(event): 
	admins = await load_data_adm()
	if event.chat.id in admins:
		await bot.send_message(event.chat.id, "Якщо ти це читаєш, то вітаю, <b>ти адміністратор бота Pumba😈</b>, а це означає що я тобі довіряю!\n\
<i><u>Ось, до речі, група адмінів:</u> <u>https://t.me/+nLfnHnfbQak0YTUy</u></i>\n\n\
Відтепер, в особистих повідомленнях Пумби, <b>у тебе стали доступними наступні функції:</b>\n\n\
<b>🟣 🔊Розсилка📢</b> — <i>Повідомлення, яке ти надіслиш після натискання цієї кнопки, буде розіслано по абсолютно всім групам.</i>\n\n\
<b>🟣 ❔Відповідь❓</b> — <i>Ця функція дозволяє відповідати користувачам, котрі звернулися за допомогою технічної підтримки Пумби.</i>\n\n\
<i><u>Якщо натиснути кнопку \"◀️Назад\" то функція скасується.</u></i>\n\n\n\
<b>🟣 /admin</b> — <i>Команда, яка показує це повідомлення).</i>\n\n\
<b>🟣 /id_admin</b> — <i>Команда, яка показує ID всіх адмінів Пумби.</i>\n\n\
<b>🟣 /all_chats</b> — <i>Команда, яка показує ID всіх чатів, де присутній Пумба (на які діє розсилка).</i>\n\n\
<b>🟣 /chats_enabled</b> — <i>Команда, яка показує ID всіх чатів, де увімкнено <b>matuki_on</b>.</i>\n\n\n\
<b>🟣 /register_word text*</b> — <i>Команда, яка додає слово тригер, та відповідь бота на нього.\n(Приклад застосування: \"/register_word да - пізда\")</i>\n\n\
<b>🟣 /delete_word text*</b> — <i>Команда, яка видаляє слово тригер, та відповідь бота на нього.\n(Приклад застосування: \"/delete_word да\", після цього тригер слово \"да\" видалиться разом з відповіддю на нього - \"пізда\")</i>\n\n\
<b>🟣 /list_words</b> — <i>Команда, яка показує всі зареєстровані слова і відповіді.</i>\n\n\n\
<b>🟣 /ban</b> — <i>Команда, для бану кнопки \"📝Підтримка🤔\" дибілам.\n(Приклад застосування: \"/ban id*\")</i>\n\n\
<b>🟣 /unban</b> — <i>Команда, для розбану кнопки \"📝Підтримка🤔\" дибілам.\n(Приклад застосування: \"/unban id*\")</i>\n\n\
<b>🟣 /users_ban_list</b> — <i>Команда, яка показує ID всіх забанених дибілів.</i>\n\n\n\n\
Ще дві команди, але <b>вони доступні лише розробнику бота:</b>\n\n\
<b>🔵 /register_admin id*</b> — <i>Команда для додавання адмінів.</i>\n\n\
<b>🔵 /delete_admin id*</b> — <i>Команда для видалення адмінів.</i>\n\n\
", parse_mode = 'html', buttons=await page_start_admin())

# List of all admin IDs
async def admin_info_real(event): 
	admins = await load_data_adm()
	if event.chat.id in admins:
		text = ''
		count = 1
		for admin in admins:
			text += str(count) + ". " + str(admin) + '\n'
			count += 1

		await bot.send_message(event.chat.id, f"<b>ID всіх адмінів Пумби:\n\n</b><i>{text}</i>", parse_mode = 'html')

# List of all chat IDs
async def all_chats_real(event): 
	admins = await load_data_adm()
	if event.chat.id in admins:
		text = ''
		all_chats = await load_data_all()
		count = 1
		for chats in all_chats:
			text += str(count) + ". " + str(chats) + '\n'
			count += 1
		
		await bot.send_message(event.chat.id, f"<b>ID всіх чатів, де присутній Пумба:\n\n</b><i>{text}</i>", parse_mode = 'html')

# List of chat IDs where /matuki_on
async def enabled_chats_real(event): 
	admins = await load_data_adm()
	if event.chat.id in admins:
		enabled_chats = await load_data_word()
		text = ''
		count = 1
		for chats in enabled_chats:
			text += str(count) + ". " + str(chats) + '\n'
			count += 1

		await bot.send_message(event.chat.id, f"<b>ID всіх чатів з <b><i>matuki_on</b></i>:\n\n</b><i>{text}</i>", parse_mode = 'html')



conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create a table to store words and answers
cursor.execute('''
    CREATE TABLE IF NOT EXISTS word_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        response TEXT NOT NULL
    )
''')
conn.commit()

# Registering words and answers
async def register_word(event):
	admins = await load_data_adm()
	if event.chat.id in admins:
		args = event.text.split(' - ', 1)

		# Check the correctness of the command format
		if len(args) == 2:
			word = args[0].split(' ', 1)[1].lower()
			response = args[1]

			cursor.execute('SELECT response FROM word_responses WHERE word = ?', (word,))
			result = cursor.fetchone()

			if result:
				await event.reply(f'Слово <i>"{word}"</i> вже було зареєстровано раніше, <b>не можна повторюватись!</b>', parse_mode = 'html')
				return

			cursor.execute('INSERT INTO word_responses (word, response) VALUES (?, ?)', (word, response))
			conn.commit()

			await event.reply(f'Тригер разом з відповіддю було зареєстровано:\n\n <b>{word}</b> - <i>{response}</i>', parse_mode = 'html')

			user = await bot.get_entity(event.sender_id)
			await bot.send_message(chat_id_pumba, f"Адмін <b>{user.first_name} ({user.id})</b> <u>ЗАРЕЄСТРУВАВ</u> слово з відповіддю:\n\n<b>{word}</b> - <i>{response}</i>", parse_mode = 'html')
		else:
			await event.reply('<b>Неправильний формат команди</b>.\n<i>(Приклад застосування: \"/register_word да - пізда\")</i>', parse_mode = 'html')

# Deleting words and answers
async def delete_word(event):
	admins = await load_data_adm()
	if event.chat.id in admins:
		try:
			word_to_delete = event.text.split(' ', 1)[1].lower()

			cursor.execute('DELETE FROM word_responses WHERE word = ?', (word_to_delete,))
			conn.commit()
			if cursor.rowcount >= 1:
				await event.reply(f'Слово <i>"{word_to_delete}"</i> <u>ВИДАЛЕНО</u>!', parse_mode = 'html')

				user = await bot.get_entity(event.sender_id)
				await bot.send_message(chat_id_pumba, f"Адмін <b>{user.first_name} ({user.id})</b> <u>ВИДАЛИВ</u> тригер <i><b>\"{word_to_delete}\"</b></i> разом з відповіддю.", parse_mode = 'html')
			else:
				await event.reply(f'Слово <i>"{word_to_delete}"</i> не було зареєстровано.', parse_mode = 'html')
		except:
			await event.reply('<b>Неправильний формат команди</b>.\n<i>(Приклад застосування: \"/delete_word да\")</i>', parse_mode = 'html')

async def list_words(event):
    enabled_chats = await load_data_word()
    admins = await load_data_adm()
    if event.chat_id in enabled_chats or event.chat.id in admins:
        cursor.execute('SELECT word, response FROM word_responses')
        word_responses = cursor.fetchall()

        grouped_words = {}
        for word, response in word_responses:
            grouped_words.setdefault(response, []).append(word)

        message = '<b>Список словесних тригерів і відповідей на них:</b>\n\n\
<b>🔴 кубик, куб</b> - <i><u>🎲</u></i>\n<b>🔴 пони</b> - <i><u>🦄</u></i>\n\n'
        if grouped_words:
            for response, words in grouped_words.items():
                words_str = ', '.join(f'<b>{word}</b>' for word in words)
                message += f'🟡 {words_str} - <i>{response}</i>\n'
        message += f'<b>\n🔵 вумен, woman</b> - <i><u>sticker</u></i>\n\n\
<b>🟢 гений, геній</b> - <i><u>gif</u></i>\n\n\
<u><b>КАПС*</b> - <i>НЕ КРИЧИ ДИБІЛ!</i></u>'

        await event.respond(message, parse_mode='html')



# Function for saving data to a file
async def save_data_ban(data):
	directory = 'support'
	os.makedirs(directory, exist_ok=True) 
	chat = f'{directory}/ban_users.json'
	with open(chat, 'w') as f:
		json.dump(data, f)

# Function for loading data from a file
async def load_data_ban():
    try:
        with open('support/ban_users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Ban users
async def ban_user(event):
	admins = await load_data_adm()
	if event.chat.id in admins:
		banned = await load_data_ban()
		try:
			id_ban = int(event.text[5:])
			if id_ban not in banned:
				banned.append(id_ban)
				await save_data_ban(banned)
				await bot.send_message(event.chat.id, f"Користувача <i>{id_ban}</i> <b>забанено😈!</b>", parse_mode = 'html')
				
				user = await bot.get_entity(event.sender_id)
				await bot.send_message(chat_id_pumba, f"Адмін <b>{user.first_name} ({user.id})</b> <u>ЗАБАНИВ</u> користувача: <i><b>{id_ban}</b></i>", parse_mode = 'html')
			else:
				await bot.send_message(event.chat.id, f"Користувач <i>{id_ban}</i> вже був <b>забанений раніше😈!</b>", parse_mode = 'html')
		except:
			await bot.send_message(event.chat.id, "Щось пішло не так👿!\n<i>(Приклад застосування: \"/ban id*\")</i>", parse_mode = 'html')
		return

# Unban users
async def unban_user(event):
	admins = await load_data_adm()
	if event.chat.id in admins:
		banned = await load_data_ban()
		try:
			id_ban = int(event.text[7:])
			if id_ban in banned:
				banned.remove(id_ban)
				await save_data_ban(banned)
				await bot.send_message(event.chat.id, f"Користувача <i>{id_ban}</i> <b>розбанено😈!</b>", parse_mode = 'html')

				user = await bot.get_entity(event.sender_id)
				await bot.send_message(chat_id_pumba, f"Адмін <b>{user.first_name} ({user.id})</b> <u>РОЗБАНИВ</u> користувача: <i><b>{id_ban}</b></i>", parse_mode = 'html')
			else:
				await bot.send_message(event.chat.id, f"Користувач <i>{id_ban}</i> <b>не був в бані😈!</b>", parse_mode = 'html')
		except:
			await bot.send_message(event.chat.id, "Щось пішло не так👿!\n<i>(Приклад застосування: \"/unban id*\")</i>", parse_mode = 'html')
		return

# List of IDs of all banned users
async def ban_user_list(event): 
	admins = await load_data_adm()
	if event.chat.id in admins:
		banned = await load_data_ban()
		text = ''
		for users in banned:
			text += str(users) + '\n'

		await bot.send_message(event.chat.id, f"<b>ID всіх забанених користувачів:\n\n</b><i>{text}</i>", parse_mode = 'html')