import json
import sqlite3
from telethon import types
import os

from config.config import bot,my_id,chat_id_souz,Pumba,chat_id_pumba, db_path
from misc.support import handle_support,page_support_back,page_start,page_start_admin
from misc.weather import send_weather_srazu, send_weather_katowice
from misc.swear import load_data_word
from misc.birthday import birthday_add_delete
from misc.all_rates import send_rates,send_crypto,send_petrol
from misc.other_func import send_rnumb,send_rcoin,send_alert,gruz200,send_random_user
from misc.admin_func import forward_send_message,answer_message,load_data_adm,load_data_ban
from misc.hello_buy import save_data_all,load_data_all



# Database SQL
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS word_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        response TEXT NOT NULL
    )
''')
conn.commit()



# Dictionary for translation from English to Ukrainian keyboard layout
eng_to_ukr = {
    'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
    '[': 'х', ']': 'ї', 'a': 'ф', 's': 'і', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
    'l': 'д', ';': 'ж', "'": 'є', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
    ',': 'б', '.': 'ю'
}



# All words
async def all_message(event,events):
	message_text = event.text.lower()
	if(message_text):
		if (message_text[0] == '!'):
			return

	eng_to_ukr_mes = ''.join(eng_to_ukr.get(char, char) for char in event.message.message).lower()

	if event.is_channel and not event.is_group:
		return
	
	banned = await load_data_ban()
	if event.sender_id in banned:
		#await bot.send_message(event.chat.id, "<b>Вас забанили за спам!</b>", parse_mode = 'html')
		return
	
	if event.photo or event.video:
		if event.media.spoiler:
			await event.reply('⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️\n❗️Можливий треш контент❗️')
			return
		
	if message_text == 'тревога' or message_text == 'тривога' or eng_to_ukr_mes == 'тривога' or eng_to_ukr_mes == 'тревога':
		await send_alert(event)
		
	if message_text == 'погода' or eng_to_ukr_mes == 'погода':
		await send_weather_srazu(event)
	
	if message_text == 'курс' or eng_to_ukr_mes == 'курс':
		await send_rates(event)
	
	if message_text == 'крипта' or eng_to_ukr_mes == 'крипта':
		await send_crypto(event)
	
	if message_text == 'бензин' or eng_to_ukr_mes == 'бензин':
		await send_petrol(event)

	if message_text == 'втрати' or eng_to_ukr_mes == 'втрати':
		await gruz200(event)

	if message_text == 'монетка' or message_text == 'монета' or eng_to_ukr_mes == 'монетка' or eng_to_ukr_mes == 'монета':
		await send_rcoin(event)	
	
	if message_text == 'число' or message_text == 'цифра' or eng_to_ukr_mes == 'число' or eng_to_ukr_mes == 'цифра':
		await send_rnumb(event)
	
	if  message_text == 'хтось' or message_text == 'хто небудь' or message_text == 'хто-небудь' or eng_to_ukr_mes == 'хтось' or eng_to_ukr_mes == 'хто небудь' or eng_to_ukr_mes == 'хто-небудь':
		await send_random_user(event)
	
	if message_text == 'слава украине' or message_text == 'слава україні':
		await event.reply('Героям слава!🇺🇦')	
	if message_text == 'слава нации' or message_text == 'слава нації':
		await event.reply('Смерть ворогам!🇺🇦')	
	if message_text == 'україна' or message_text == 'украина':
		await event.reply('Понад усе!🇺🇦')	
	if message_text == 'путин' or message_text == 'путін':
		await event.reply('Хуйло!🇺🇦')	
	


	await birthday_add_delete(event)



	if event.chat_id < 0:

		people = await bot.get_entity(event.sender_id)

		if people.bot:
			return
		
		if people.username:

			all_chats = await load_data_all()
			chat_id = event.chat_id

			if chat_id not in all_chats:
				all_chats.append(chat_id)
				await save_data_all(all_chats)

			directory = 'chats'
			os.makedirs(directory, exist_ok=True) 
			chat_chat = f'{directory}/{event.chat_id}.json'

			try:
				with open(chat_chat, 'r') as file:
					users = json.load(file)
			except FileNotFoundError:
				users = []
			
			if not any(user['id'] == people.id for user in users):
				users.append({'id': people.id, 'username': people.username, 'word_count': 0})
				with open(chat_chat, 'w') as file:
					json.dump(users, file)
					
			for user in users:
				if user['id'] == people.id:
					try:
						words = event.text.split()
						word_count = 0
						for word in words:
							if len(word) >= 2:
								word_count += 1
						user['word_count'] += word_count
					except KeyError:
						users.append({'id': people.id, 'username': people.username, 'word_count': 0})
				
			for user in users:
				if user['id'] == people.id:
					user['username'] = people.username
					with open(chat_chat, 'w') as file:
						json.dump(users, file)
					break
				
			print(people.username + ": " + event.text)



# Enabled words
		enabled_chats = await load_data_word()
		if event.chat_id in enabled_chats:

			if message_text == 'вумен' or message_text == 'woman':
				await bot.send_file(event.chat.id, 'fixtures/photo_woman.webp', reply_to=event._message_id)
				return
				
			if message_text == 'гений' or message_text == 'геній':
				await bot.send_file(event.chat.id, "fixtures/video_genius.mp4", reply_to=event._message_id)
				return
			
			# if message_text == 'расписание' or message_text == 'розклад' or message_text == 'пары':
			# 	if event.chat_id == chat_id_souz:
			# 		await bot.send_file(event.chat.id, 'fixtures/photo_only_rest.png', reply_to=event._message_id)
			# 	return
				
			if message_text == 'катовице' or message_text == 'катовіце' or message_text == 'katowice' or message_text == 'като':
				if event.chat_id == chat_id_pumba:
					await send_weather_katowice(event)
					return

# 			if message_text == 'расписание' or message_text == 'розклад' or message_text == 'пары':
# 				if event.chat_id == chat_id_souz:
# 					await bot.send_message(event.chat.id, f"<b>Понеділок:</b>\n\
# <i>1⃣ Спеціалізація з програмування <u>(Дейнега В.Р.)</u>\n\
# 2⃣ Чисельні методи <u>(Ялова О.О.)</u>\n\
# 3⃣ Чисельні методи <u>(Ялова О.О.)</u> / Основи охорони праці <u>(Безсонов Д.М.)</u>\n\
# 4⃣ Українське ділове мовлення <u>(Кеда В.С.)</u></i>\n\
# \n\
# <b>Вівторок:</b>\n\
# <i>1⃣ Основи охорони праці <u>(Безсонов Д.М.)</u>\n\
# 2⃣ Системи штучного інтелекту <u>(Слободяник О.О.)</u>\n\
# 3⃣ Фізичне виховання (Секції з виду спорту) <u>(Джунь Ю.В.)</u>\n\
# 4⃣ —</i>\n\
# \n\
# <b>Середа:</b>\n\
# <i>1⃣ Спеціалізація з програмування <u>(Дейнега В.Р.)</u>\n\
# 2⃣ Імітаційне моделювання <u>(Боровик Ю.А.)</u>\n\
# 3⃣ Проєктний менеджмент <u>(Щербаков О.В.)</u>\n\
# 4⃣ —</i>\n\
# \n\
# <b>Четвер:</b>\n\
# <i>1⃣ Українське ділове мовлення <u>(Кеда В.С.)</u>\n\
# 2⃣ Імітаційне моделювання <u>(Боровик Ю.А.)</u>\n\
# 3⃣ Комплексна курсова робота <u>(Щукін О.В.)</u>\n\
# 4⃣ —</i>\n\
# \n\
# <b>П'ятниця:</b>\n\
# <i>1⃣ Проєктний менеджмент <u>(Щербаков О.В.)</u>\n\
# 2⃣ Системи штучного інтелекту <u>(Слободяник О.О.)</u>\n\
# 3⃣ Чисельні методи <u>(Ялова О.О.)</u>\n\
# 4⃣ —</i>"
# , parse_mode='html')
# 					return

			# if message_text == 'звонки':
			# 	if event.chat_id == chat_id_souz:
			# 		await event.reply('<b>1 пара:</b> <i>08:30-09:50</i>\n<b>2 пара:</b> <i>10:00-11:20</i>\n<b>3 пара:</b> <i>12:00-13:20</i>\n<b>4 пара:</b> <i>13:30-14:50</i>', parse_mode = 'html')	
			# 		return
			
			if message_text == 'кубик' or message_text == 'куб':
				await bot.send_file(event.chat.id, types.InputMediaDice(''), reply_to=event._message_id)
				return
			
			if message_text == 'пони':
				await event.reply('🦄')
				return



			# Search for a word in the database
			cursor.execute('SELECT response FROM word_responses WHERE word = ?', (message_text,))
			result = cursor.fetchone()

			# If the word is found, we respond with the saved answer
			if result:
				await event.reply(result[0])
				return
			
			if len(event.text) >= 5:
				uppercase_percentage = sum(1 for char in event.text if char.isalpha() and char.isupper()) / len(event.text)
				if uppercase_percentage >= 0.7:
					await event.reply("НЕ КРИЧИ ДИБІЛ!")



# Personal messages
	if event.chat_id > 0:
		
		if event.text == '🐗Pumba🐗':
			await bot.send_message(event.chat.id, 'Тут я хотів би детальніше розповісти про бота, якого я написав на <b>🐍Python🐍</b> на першому курсі коледжа.\n\n\
<b>Пумба</b> — це бот-помічник зроблений виключно з розважальними цілями. В нього є як корисні функції (Мапа тривог, зазивала, курс, погода та інше...) так і не дуже...\n\n\
Спочатку бот був лише для моїх друзів та оточення, а потім понеслося... тому ви мене можете навіть не знати.\n\n\
Бот буде оновлюватися весь час <i>(поки мені це цікаво і подобається іншим)</i>.\n\n\
Здебільшого я робив Пумбу сам, по гайдам на Ютубі і таке інше, звісно без <b>ChatGPT</b> теж не обійшлося... \n\n\
В багатьох моментах мені допомагали мої друзі, підказували як краще зробити та просто давали ідеї. Також протягом всього часу зі мною була моя подруга, яка дуже допомагала як морально так і фізично😏. \n\n\
Якщо ви дочитали до цього моменту — вам не начхати на Пумбу та мене особисто, я це дуже ціную). І на останок — <b>Поважайте Пумбу😊.</b>', parse_mode = 'html')
			return 
		
		if event.text == '📝Підтримка🤔':
			bot.add_event_handler(handle_support, events.NewMessage(from_users=event.sender_id, chats=event.chat_id))
			await bot.send_message(event.chat.id, '<i>Якщо ти знайшов якийсь баг, в тебе з`явилася ідея щодо боту, щось пішло не так, чи ти просто хочешь сказати мені, який я крутий)</i> — <b>Пиши або відправляй фото чи відео</b>', parse_mode = 'html', buttons=await page_support_back())
			return 

		admins = await load_data_adm()
		
		if event.text == '◀️Назад':
			if event.chat.id in admins:
				await bot.send_message(event.chat.id, "Ви повернулись на <b>головну сторінку😈</b>", parse_mode = 'html', buttons=await page_start_admin())
				return
			await bot.send_message(event.chat.id, "Ви повернулись на <b>головну сторінку</b>", parse_mode = 'html', buttons=await page_start())
			return
		
		if event.text == '🔊Розсилка📢':
			if event.chat.id in admins:
				bot.add_event_handler(forward_send_message, events.NewMessage(from_users=event.sender_id, chats=event.chat_id))
				await bot.send_message(event.chat.id, "Можеш писати повідомлення для розсилки😈", buttons=await page_support_back())
				return
		
		if event.text == '❔Відповідь❓':
			if event.chat.id in admins:
				bot.add_event_handler(answer_message, events.NewMessage(from_users=event.sender_id, chats=event.chat_id))
				await bot.send_message(event.chat.id, "Можеш писати відповідь користувачу😈\n(Приклад: \"id* text\")", buttons=await page_support_back())
				return