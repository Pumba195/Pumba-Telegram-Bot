import random
import os
import openpyxl
import json 
import re

from bs4 import BeautifulSoup
from cloudscraper import create_scraper
from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback
from telethon import Button
from misc.swear import load_data_word
from misc.support import page_start,page_start_admin
from config.config import bot,chat_id_ss,my_id,chat_id_pumba,chat_id_souz,chat_id_answars
from misc.admin_func import load_data_adm,load_data_ban
from rates.rates_of_crypto import Currency_bit
from rates.rates_of_currency import Currency
from rates.alert import AlertScreenshotter

import asyncio
from playwright.async_api import async_playwright
from PIL import Image
from io import BytesIO



# Start
async def send_start(event):
	banned = await load_data_ban()
	if event.sender_id in banned:
		#await bot.send_message(event.chat.id, "<b>Вас забанили за спам!</b>", parse_mode = 'html')
		return
	user = await bot.get_entity(event.sender_id)
	admins = await load_data_adm()
	if event.chat.id in admins:
		await bot.send_message(chat_id_answars, f'{event.chat.id}', parse_mode = 'html')
		await bot.send_message(event.chat.id, f'Добрий день😈, <b>{user.first_name}</b>! Цей бот розроблений здебільшого для спільних чатів, тому не гальмуй і додавай його до всіх груп😏. Детальніша інформація про функціонал бота — <b>\"/info\"</b>', parse_mode = 'html', buttons=await page_start_admin())
		return

	if event.chat_id > 0:
		await bot.send_message(chat_id_answars, f'{event.chat.id}', parse_mode = 'html')
		await bot.send_message(event.chat.id, f'Добрий день, <b>{user.first_name}</b>! Цей бот розроблений здебільшого для спільних чатів, тому не гальмуй і додавай його до всіх груп😏. Детальніша інформація про функціонал бота — <b>\"/info\"</b>', parse_mode = 'html', buttons=await page_start())
		return



# Random number
async def send_rnumb(event):
	await event.reply(str(random.randint(0,100)))



# Random coin
async def send_rcoin(event):
	if random.randint(1,2) == 1:
		await event.reply('Орел')
		return
	await event.reply('Решка')
	return		



# Random user
async def send_random_user(event):
    if event.chat_id >= 0:
        await event.reply("Ця команда працює лише в групах!")
        return

    participants = await bot.get_participants(event.chat_id)
    humans = [user for user in participants if not user.bot]

    if not humans:
        await event.reply("У цьому чаті немає учасників, яких можна обрати 🤔")
        return

    chosen_user = random.choice(humans)
    await event.reply(
        f'<a href="tg://user?id={chosen_user.id}">❓</a>',
        parse_mode='html'
    )

# Alert
alert_screenshotter = AlertScreenshotter()

async def send_alert(event):
    png_bytes = await alert_screenshotter.get_png_bytes()

    img = Image.open(BytesIO(png_bytes))
    webp_buffer = BytesIO()
    img.save(webp_buffer, format="webp")
    webp_buffer.seek(0)
    webp_buffer.name = "alert.webp"

    await bot.send_file(
        event.chat_id,
        webp_buffer,
        reply_to=event._message_id
    )

# Losses
CASUALTY_LABELS = {
    'personnel': 'Особовий склад',
    'bbm': 'ББМ',
    'tanks': 'Танки',
    'artillery': 'Артилерійські системи',
    'aircraft': 'Літаки',
    'helicopters': 'Гелікоптери',
    'ships': 'Кораблі (катери)',
}

def _extract_value(text, label):
    pattern = re.compile(
        re.escape(label) + r'\s*[—-]\s*(?:близько\s*)?(\d+)(?:\s*осіб)?\s*(\(\+\d+\))?'
    )
    match = pattern.search(text)
    if not match:
        return None
    number = match.group(1)
    delta = match.group(2) or ''
    return f'{number} {delta}'.strip()


async def gruz200(event):
    try:
        scraper = create_scraper(delay=10, browser='chrome')
        url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
        page = scraper.get(url).text
        soup = BeautifulSoup(page, 'html.parser')
        text = soup.get_text('\n')

        date_match = re.search(r'\d{2}\.\d{2}\.\d{4}', text)
        if not date_match:
            raise ValueError('Дату не знайдено на сторінці')
        date_str = date_match.group(0)

        values = {}
        for key, label in CASUALTY_LABELS.items():
            value = _extract_value(text, label)
            if value is None:
                raise ValueError(f'Не вдалося знайти показник: {label}')
            values[key] = value

        titlee = '🧟\u200d♂ Втрати <s>гандонів</s> русні на ' + date_str
        title = f'<b>{titlee}</b>'

        await bot.send_message(
            event.chat.id,
            title +
            f'<b>\n\n\u2620\uFE0F Вбито:</b> <i>{values["personnel"]}</i>'
            f'<b>\n\U0001F690 ББМ:</b> <i>{values["bbm"]}</i>'
            f'<b>\n\U0001F69C Танки:</b> <i>{values["tanks"]}</i>'
            f'<b>\n\U0001F525 Артилерія:</b> <i>{values["artillery"]}</i>'
            f'<b>\n\u2708\uFE0F Літаки:</b> <i>{values["aircraft"]}</i>'
            f'<b>\n\U0001F681 Гелікоптери:</b> <i>{values["helicopters"]}</i>'
            f'<b>\n\U0001F6A2 Кораблі та катери:</b> <i>{values["ships"]}</i>',
            parse_mode='html'
        )
    except Exception:
        await event.reply(
            'Щось пішло не так, ось сайт:\n <i>index.minfin.com.ua/ua/russian-invading/casualties</i>',
            parse_mode='html'
        )


# Informations
async def send_info(event):
	await bot.send_message(event.chat_id, '<a href="https://telegra.ph/Pumba-07-15-2">Функціонал Пумби</a>', parse_mode = 'html', link_preview=True)
	
# 	await event.reply('<b>📜Більш детальна інформація щодо команд та функціоналу бота</b> <i>(в дужках (одразу після команди) написано слова, які можна використовувати замість самих команд)</i>:\n\n\
# <b>🔴 /alert</b> (тривога, тревога) — <i>Ця команда кидає стікер карти України з повітряними тривогами.\n<u>(взято з Telegram-Random_UAbot)</u></i>\n\n\
# <b>🔴 /weather</b> (погода) — <i>Пумба відправляє погоду в обраному місті, щоб переобрати місто є команда /set_weather.</i>\n\n\
# <b>🔴 /set_weather</b> — <i>Пумба кидає повідомлення зі списком міст, які є обласними центрами України. В залежності від обраного міста бот змінює повідомлення на погоду в обраному населеному пункті. В майбутньому по команді /weather бот буде відправляти погоду в цьому місті.</i>\n\n\
# <b>🔴 /rates</b> (курс) — <i>Бот відправляє повідомлення з курсом валют(євро, долар, злотий, рубль) до гривні(НБУ) та доларом до рубля. <u>Дані виводяться поступово.</u></i>\n\n\
# <b>🔴 /crypto</b> (крипта) — <i>Бот кидає список криптовалюти(BTC, ETH, BNB, XRP, ADA, DOGE) та її курс до долара. <u>Дані виводяться поступово.</u></i>\n\n\
# <b>🔴 /petrol</b> (бензин) — <i>З`являється повідомлення з середніми цінами на пальне по Україні(Бензин А-95 преміум, А-95, А-92, дизель та газ). <u>Дані виводяться поступово.</u></i>\n\n\
# <b>🔴 /losses</b> (втрати) — <i>Пумба відправляє повідомлення з кількістю втрат росії в ході бойових дій проти України, починаючи з 24 лютого 2022 року.\n<u>(взято з Telegram-Random_UAbot)</u></i>\n\n\
# <b>🔴 /mywords</b> — <i>Бот-помічник шле повідомлення в якому вказана кількість всіх відправленних вами слів в чат за час перебування Пумби у групі.</i>\n\n\
# <b>🔴 /topten</b> — <i>Відправляэться повідомлення з топ-10 найактивнішими користувачами в чаті.</i>\n\n\
# <b>🔴 /info</b> — <i>Відображає список команд та пояснення до них (зараз).</i>\n\n\
# <b>🔴 /rps</b> — <i>Rock-paper-scissors (👊Камінь,✌️Ножиці,✋Папір). Класична гра в Цу-є-фа проти Пумби.</i>\n\n\
# <b>🔴 /tictactoe</b> — <i>З`являється повідомлення з грою хрестики-нулики, в яку можна повноцінно грати з іншими учасниками групи.</i>\n\n\
# <b>🔴 /delete_game</b> — <i>Команда, котра видаляє ми	нулу партію гри хрестики-нулики, це зроблено для того щоб, якщо щось пішло не так, в чаті загубилася минула партія або активні гравці оффлайн, інші теж могли пограти.</i>\n\n\
# <b>🔴 /callall</b> — <i>Видаляє повідомлення з командою з чату та відправляє повідомлення з двома кнопками: Активувати - запускає призив всіх участників групи; Скасувати - скасувати призив (повідомлення видалиться).</i>\n\n\
# <b>🔴 /random_user</b> (хтось, хто небудь, хто-небудь) — <i>Пінгує випадкового участника чату.</i>\n\n\
# <b>🔴 /excel</b> — <i>Пумба відправляю файл <u>members.xlsx</u> в таблиці якого знаходяться всі користувачі чату, іноді може знадобитися.</i>\n\n\
# <b>🔴 /number</b> (число, цифра) — <i>Пумба кидає повідомлення з випадковим числом (0 — 100).</i>\n\n\
# <b>🔴 /coin</b> (монета, монетка) — <i>Бот відправляє повідомлення "Орел" або "Решка".</i>\n\n\
# <i>*Якщо якась команда не спрацювала, або спрацювала, але не до кінця — зачекайте ±30 секунд і напишіть її знову. Це відбувається через спам командами.</i>', 
# parse_mode = 'html')



# Callall ask
async def send_callall_message(event):
	if event.chat_id < 0:
		try:
			await bot.delete_messages(event.chat.id, event._message_id)

			inline_markup = ReplyInlineMarkup(
				[
					KeyboardButtonRow(
						[
							KeyboardButtonCallback(
								text = "Активувати",
								data = b'baza'
							),
							KeyboardButtonCallback(
								text = "Скасувати",
								data = b'back'
							)
						]
					)
				]
			)
		
			await bot.send_message(event.chat.id, 'Призвати всіх користувачів чату?', parse_mode = 'html', buttons=inline_markup)
		except:
			await send_callall_baza(event)
	else:
		await event.reply('Призив працює лише в групах!')

# Send callall 
async def send_callall_baza(event):
	if event.chat_id < 0:
		people = await bot.get_entity(event.sender_id)
		enabled_chats = await load_data_word()
		if event.chat_id in enabled_chats:
			await bot.send_message(event.chat.id, f'<b>{people.first_name}</b> призиває клоунів:', parse_mode = 'html')
			emoji = '🤡'
		else:
			await bot.send_message(event.chat.id, f'<b>{people.first_name}</b> призиває всіх живих:', parse_mode = 'html')
			emoji = '😇'

		participants = await bot.get_participants(event.chat_id)
		text = ""
		user_on_line = 5
		current_user = 0

		for user in participants:
			if user.bot:
				pass
			else:
				text += f'<a href="tg://user?id={user.id}">'+emoji+'</a>'
				current_user += 1
				if current_user == user_on_line:
					await bot.send_message(event.chat_id, text, parse_mode='html')
					text = ""
					current_user = 0
		if text != "":
			await bot.send_message(event.chat.id, text, parse_mode='html')

	else:
		await event.reply('Призив працює лише в групах!')



# Excel
async def excel_realized(event):
	if event.chat_id < 0:

		participants = await bot.get_participants(event.chat_id)
		excel_file_path = 'members.xlsx'

		if os.path.exists(excel_file_path):
			os.remove(excel_file_path)

		if not os.path.exists(excel_file_path):
			wb = openpyxl.Workbook()
			ws = wb.active
			ws.append(['Number', 'Name', 'Tag'])
		
		number = 1
		
		for user in participants:
			if user.bot:
				pass
			else:
				name = user.first_name
				if name == None:
					name = 'None'
				tag = user.username
				if tag == None:
					tag = 'None'

				ws.append([str(number), name, tag])
				wb.save(excel_file_path)
				number += 1

		await bot.send_file(event.chat_id, 'members.xlsx', reply_to = event._message_id)
		
		os.remove(excel_file_path)

	else:
		await event.reply("Ця команда працює лише в групах!")



# ---------------------------- Time message ----------------------------

#SS	
async def send_silence_message():
	await bot.send_message(chat_id_ss, "ПОЗАКРИВАЛИ ПИЗДАКИ! Хвилина мовчання...")



# Function for saving data to a file
async def save_data_schedule(data):
	directory = 'support'
	os.makedirs(directory, exist_ok=True) 
	file_path = f'{directory}/schedule.json'
	
	with open(file_path, 'w') as f:
		json.dump(data, f)

# Function for loading data from a file
async def load_data_schedule():
    try:
        with open('suppor/schedule.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


"""
# Schedule
async def send_schedule_0830():	
	if (datetime.now().weekday() == 0):
		schedule_json = await load_data_schedule()
		if (schedule_json["week"] == 0):
			schedule_json['week'] = 1
		else:
			schedule_json['week'] = 0

		await save_data_schedule(schedule_json)
		
		await bot.send_message(chat_id_souz, f"╭─ <b>1 пара</b> <i>(8:30 - 9:50)</i>\n\
│ <b>•  Предмет:</b> <i>Спеціалізація з програмування</i>\n\
│ <b>•  Вчитель:</b> <i>Дейнега В.Р.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("special"))

	if (datetime.now().weekday() == 1):
		await bot.send_message(chat_id_souz, f"╭─ <b>1 пара</b> <i>(8:30 - 9:50)</i>\n\
│ <b>•  Предмет:</b> <i>Основи охорони праці</i>\n\
│ <b>•  Вчитель:</b> <i>Безсонов Д.М.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("bezpeka"))

# 	if (datetime.now().weekday() == 2):
# 		await bot.send_message(chat_id_souz, f"╭─ <b>1 пара</b> <i>(8:30 - 9:50)</i>\n\
# │ <b>•  Предмет:</b> <i>Спеціалізація з програмування</i>\n\
# │ <b>•  Вчитель:</b> <i>Дейнега В.Р.</i>\n\
# ╰───────", parse_mode='html', buttons=await link_button("special"))

	if (datetime.now().weekday() == 3):
		await bot.send_message(chat_id_souz, f"╭─ <b>1 пара</b> <i>(8:30 - 9:50)</i>\n\
│ <b>•  Предмет:</b> <i>Українське ділове мовлення</i>\n\
│ <b>•  Вчитель:</b> <i>Кеда В.С.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("ukrmova"))
		
	if (datetime.now().weekday() == 4):
		await bot.send_message(chat_id_souz, f"╭─ <b>1 пара</b> <i>(8:30 - 9:50)</i>\n\
│ <b>•  Предмет:</b> <i>Проєктний менеджмент</i>\n\
│ <b>•  Вчитель:</b> <i>Щербаков О.В.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("manager"))
	return



async def send_schedule_1000():	
	if (datetime.now().weekday() == 0):
		await bot.send_message(chat_id_souz, f"╭─ <b>2 пара</b> <i>(10:00 - 11:20)</i>\n\
│ <b>•  Предмет:</b> <i>Чисельні методи</i>\n\
│ <b>•  Вчитель:</b> <i>Ялова О.О.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("chiselni1"))

	if (datetime.now().weekday() == 1):
		await bot.send_message(chat_id_souz, f"╭─ <b>2 пара</b> <i>(10:00 - 11:20)</i>\n\
│ <b>•  Предмет:</b> <i>Системи штучного інтелекту</i>\n\
│ <b>•  Вчитель:</b> <i>Слободяник О.О.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("ai"))

	if (datetime.now().weekday() == 2):
		await bot.send_message(chat_id_souz, f"╭─ <b>2 пара</b> <i>(10:00 - 11:20)</i>\n\
│ <b>•  Предмет:</b> <i>Імітаційне моделювання</i>\n\
│ <b>•  Вчитель:</b> <i>Боровик Ю.А.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("imit"))

	if (datetime.now().weekday() == 3):
		await bot.send_message(chat_id_souz, f"╭─ <b>2 пара</b> <i>(10:00 - 11:20)</i>\n\
│ <b>•  Предмет:</b> <i>Імітаційне моделювання</i>\n\
│ <b>•  Вчитель:</b> <i>Боровик Ю.А.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("imit"))

	if (datetime.now().weekday() == 4):
		await bot.send_message(chat_id_souz, f"╭─ <b>2 пара</b> <i>(10:00 - 11:20)</i>\n\
│ <b>•  Предмет:</b> <i>Системи штучного інтелекту</i>\n\
│ <b>•  Вчитель:</b> <i>Слободяник О.О.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("ai"))
	return



async def send_schedule_1200():	
	if (datetime.now().weekday() == 0):
		schedule_json = await load_data_schedule()
		if(schedule_json["week"] == 0):
			await bot.send_message(chat_id_souz, f"╭─ <b>3 пара</b> <i>(12:00 - 13:20)</i>\n\
│ <b>•  Предмет:</b> <i>Чисельні методи</i>\n\
│ <b>•  Вчитель:</b> <i>Ялова О.О.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("chiselni1"))
		else:
			await bot.send_message(chat_id_souz, f"╭─ <b>3 пара</b> <i>(12:00 - 13:20)</i>\n\
│ <b>•  Предмет:</b> <i>Основи охорони праці</i>\n\
│ <b>•  Вчитель:</b> <i>Безсонов Д.М.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("bezpeka"))

	if (datetime.now().weekday() == 1):
		await bot.send_message(chat_id_souz, f"╭─ <b>3 пара</b> <i>(12:00 - 13:20)</i>\n\
│ <b>•  Предмет:</b> <i>Фізичне виховання</i>\n\
│ <b>•  Вчитель:</b> <i>Джунь Ю.В.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("fizra"))

	if (datetime.now().weekday() == 2):
		await bot.send_message(chat_id_souz, f"╭─ <b>3 пара</b> <i>(12:00 - 13:20)</i>\n\
│ <b>•  Предмет:</b> <i>Проєктний менеджмент</i>\n\
│ <b>•  Вчитель:</b> <i>Щербаков О.В.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("manager"))

	if (datetime.now().weekday() == 3):
		await bot.send_message(chat_id_souz, f"╭─ <b>3 пара</b> <i>(12:00 - 13:20)</i>\n\
│ <b>•  Предмет:</b> <i>Комплексна курсова робота</i>\n\
│ <b>•  Вчитель:</b> <i>Щукін О.В.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("kr"))

	if (datetime.now().weekday() == 4):
		await bot.send_message(chat_id_souz, f"╭─ <b>3 пара</b> <i>(12:00 - 13:20)</i>\n\
│ <b>•  Предмет:</b> <i>Чисельні методи</i>\n\
│ <b>•  Вчитель:</b> <i>Ялова О.О.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("chiselni2"))
	return



async def send_schedule_1330():	
	if (datetime.now().weekday() == 0):
		await bot.send_message(chat_id_souz, f"╭─ <b>4 пара</b> <i>(13:30 - 14:50)</i>\n\
│ <b>•  Предмет:</b> <i>Українське ділове мовлення</i>\n\
│ <b>•  Вчитель:</b> <i>Кеда В.С.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("ukrmova"))
		
	if (datetime.now().weekday() == 3):
		await bot.send_message(chat_id_souz, f"╭─ <b>4 пара</b> <i>(13:30 - 14:50)</i>\n\
│ <b>•  Предмет:</b> <i>Спеціалізація з програмування</i>\n\
│ <b>•  Вчитель:</b> <i>Дейнега В.Р.</i>\n\
╰───────", parse_mode='html', buttons=await link_button("special"))
	return
	


async def link_button(subject):
	#1. Спеціалізація з програмування
	if (subject == "special"):
		return Button.url("Приєднатися", "https://meet.google.com/dag-dprn-pbk")

	#2.1 Чисельні методи
	if (subject == "chiselni1"):
		return Button.url("Приєднатися", "https://us02web.zoom.us/j/81823619116?pwd=g5XFzRLzDdDKI7sP2P4DvhAOJroitp.1")
	
	#2.2 Чисельні методи
	if (subject == "chiselni2"):
		return Button.url("Приєднатися", "https://us02web.zoom.us/j/87342168934?pwd=Q1mcvVCEzNk2L6b9cr9Llu9q5ABaEa.1")

	#3. Основи охорони праці
	if (subject == "bezpeka"):
		return Button.url("Приєднатися", "https://meet.google.com/ywu-wjkw-cbm")

	#4. Українське ділове мовлення
	if (subject == "ukrmova"):
		return Button.url("Приєднатися", "https://meet.google.com/pvv-nqpm-iiy")

	#5. Системи штучного інтелекту
	if (subject == "ai"):
		return Button.url("Приєднатися", "https://meet.google.com/msr-xpxj-qmj")

	#6. Фізичне виховання
	if (subject == "fizra"):
		return Button.url("Приєднатися", "https://meet.google.com/osu-rrnw-vwa")

	#7. Імітаційне моделювання
	if (subject == "imit"):
		return Button.url("Приєднатися", "https://meet.google.com/uqj-cute-eif")

	#8. Проєктний менеджмент
	if (subject == "manager"):
		return Button.url("Приєднатися", "https://meet.google.com/ecm-dysj-npc")

	#9. Комплексна курсова робота
	if (subject == "kr"):
		return Button.url("Приєднатися", "https://meet.google.com/frd-kntf-brh")



# TEST
async def send_test_message(event):	
	return
"""


# Questions
"""
@bot.message_handler(commands=['questions'])
def send_rtrue(message):
	enabled_chats = load_data_word()
	if message.chat.id in enabled_chats:
		if message.chat.id < 0:
			a = random.randint(0,107)
			if a == 0:
				bot.reply_to(message, 'Ломал ли ты что то (руку, ногу...)?')	
			if a == 1:
				bot.reply_to(message, 'Что ты последний раз искал(а) в инете?')	
			if a == 2:
				bot.reply_to(message, 'Какую твою тайну не знает твоя семья, чему ты очень рад(а)?')	
			if a == 3:
				bot.reply_to(message, 'Что самое стыдное ты делал(а)?')	
			if a == 4:
				bot.reply_to(message, 'Что было худшим поступком в твоей жизни?')	
			if a == 5:
				bot.reply_to(message, 'Что самое странное ты когда-либо ел(а)?')	
			if a == 6:
				bot.reply_to(message, 'В каком реалити-шоу ты бы хотел(а) поучаствовать?')	
			if a == 7:
				bot.reply_to(message, 'Ты дружил(а) с кем-нибудь ради выгоды?')	
			if a == 8:
				bot.reply_to(message, 'Что было самой большой ошибкой в твоей жизни?')	
			if a == 9:
				bot.reply_to(message, 'Какой самый отвратительный поступок по отношению к тебе совершали другие люди?')	
			if a == 10:
				bot.reply_to(message, 'Что самое лучшее делали для тебя близкие?')	
			if a == 11:
				bot.reply_to(message, 'О чем был твой самый странный сон?')	
			if a == 12:
				bot.reply_to(message, 'О чем ты больше всего сожалеешь?')	
			if a == 13:
				bot.reply_to(message, 'Какое самое большое заблуждение о тебе есть у других людей?')	
			if a == 14:
				bot.reply_to(message, 'Что ты хотел(а) бы, чтобы все знали о тебе?')	
			if a == 15:
				bot.reply_to(message, 'Какой совет из тех, что тебе дали, был лучшим?')	
			if a == 16:
				bot.reply_to(message, 'Если бы тебе надо было вычеркнуть из жизни одного человека, кого ты выбрал(а) бы?')	
			if a == 17:
				bot.reply_to(message, 'Какой была самая глупая причина твоего опоздания?')	
			if a == 18:
				bot.reply_to(message, 'Кому ты пишешь сообщения чаще всего?')	
			if a == 19:
				bot.reply_to(message, 'Какой самый безумный поступок вы делали в общественном месте?')	
			if a == 20:
				bot.reply_to(message, 'Вы когда-нибудь лгали своему лучшему другу, говоря, что вы плохо себя чувствуете, чтобы не тусоваться?')	
			if a == 21:
				bot.reply_to(message, 'У тебя было обидное детское прозвище? Если да то какое?')	
			if a == 22:
				bot.reply_to(message, 'Вы обманывали в этом тесте?')	
			if a == 23:
				bot.reply_to(message, 'Какая ваша наименее любимая книга и почему?')	
			if a == 24:
				bot.reply_to(message, 'Есть ли у вас любимые братья и сестры, и если да, то почему они ваши любимые?')	
			if a == 25:
				bot.reply_to(message, 'Вы когда-нибудь притворялись, что вам понравился подарок?')	
			if a == 26:
				bot.reply_to(message, 'Был ли у вас неловкий момент перед школой?')	
			if a == 27:
				bot.reply_to(message, 'Вы когда-нибудь симулировали болезнь, чтобы не ходить в школу?')	
			if a == 28:
				bot.reply_to(message, 'Вы когда-нибудь преследовали кого-либо в социальных сетях?')	
			if a == 29:
				bot.reply_to(message, 'Вы когда-нибудь тренировались целоваться перед зеркалом?')	
			if a == 30:
				bot.reply_to(message, 'Если бы вам пришлось удалить одно приложение со своего телефона, какое бы вы выбрали?')	
			if a == 31:
				bot.reply_to(message, 'Какой был твой первый мобильный телефон?')
			if a == 32:
				bot.reply_to(message, 'Какую самую большую шалость ты совершил(а) в детстве и как тебя за нее наказали?')
			if a == 33:
				bot.reply_to(message, 'Какую самую худшую работу тебе приходилось делать?')
			if a == 34:
				bot.reply_to(message, 'Какого известного человека ты встречал?')
			if a == 35:
				bot.reply_to(message, 'Есть такая еда, который ты б не стал(а) делиться?')
			if a == 36:
				bot.reply_to(message, 'Если бы ты мог изменить страну проживания, куда б отправил(а)ся?')
			if a == 37:
				bot.reply_to(message, 'Если б ты выступал в цирке, кем бы ты был?')
			if a == 38:
				bot.reply_to(message, 'Если б тебе пришлось прочитать целую энциклопедию, какую б букву ты выбрал?')
			if a == 39:
				bot.reply_to(message, 'Какое насекомое тебе больше всего не нравится?')
			if a == 40:
				bot.reply_to(message, 'Какая была твоя первая любимая песня?')
			if a == 41:
				bot.reply_to(message, 'Кто-нибудь когда-нибудь спасал твою жизнь? А ты?')
			if a == 42:
				bot.reply_to(message, 'Что для тебя личный ад и рай?')
			if a == 43:
				bot.reply_to(message, 'Какой персонаж из фильмов ужасов, по-твоему, самый страшный?')
			if a == 44:
				bot.reply_to(message, 'Какой персонаж из фильмов, по-твоему, больше всего похож на тебя?')
			if a == 45:
				bot.reply_to(message, 'Если б твоим дальним родственником оказался король, ты б стал этим гордиться?')
			if a == 46:
				bot.reply_to(message, 'Какую страну ты не хотел(а) бы посещать?')
			if a == 47:
				bot.reply_to(message, 'Какую страну ты хотел(а) бы посетить?')
			if a == 48:
				bot.reply_to(message, 'Если б тебе предложили оказаться на обложке любого журнала, какой бы ты выбрал(а)?')
			if a == 49:
				bot.reply_to(message, 'Какая из диснеевских принцесс самая красивая?')
			if a == 50:
				bot.reply_to(message, 'Что из прошлого в истории ты б хотел(а) изменить?')
			if a == 51:
				bot.reply_to(message, 'Если б тебе предложили стать президентом на день, чтоб ты изменил(а)?')
			if a == 52:
				bot.reply_to(message, 'Какую самую смешную комедию ты знаешь?')
			if a == 53:
				bot.reply_to(message, 'В какой стране ты бы ни за что не стал(а) жить?')
			if a == 54:
				bot.reply_to(message, 'Какой последний ужин ты б заказал(а) перед смертной казнью?')
			if a == 55:
				bot.reply_to(message, 'По шкале от 1 до 10 какую боль ты когда-либо испытывал(а)?')
			if a == 56:
				bot.reply_to(message, 'Есть ли у тебя шрамы, и как они появились?')
			if a == 57:
				bot.reply_to(message, 'Если б ты выиграл миллион, что бы купил(а) в первую очередь?')
			if a == 58:
				bot.reply_to(message, 'Какой твой самый любимый вид спорта?')
			if a == 59:
				bot.reply_to(message, 'Если б ты попал на необитаемый остров, смог(ла) бы выжить?')
			if a == 60:
				bot.reply_to(message, 'Какой твой самый нелюбимый запах?')
			if a == 61:
				bot.reply_to(message, 'Если б ты мог(ла) побить мировой рекорд, что за рекорд это был бы?')
			if a == 62:
				bot.reply_to(message, 'Ты бы смог(ла) жить на Марсе, если б это было возможно?')
			if a == 63:
				bot.reply_to(message, 'Какой самый странный сон ты видел(а)?')
			if a == 64:
				bot.reply_to(message, 'Если б тебе надо было отказаться от одного из чувств, чтоб ты выбрал(а)?')
			if a == 65:
				bot.reply_to(message, 'Если б тебе предложили остаться в одном возрасте навсегда, какой бы ты выбрал(а)?')
			if a == 66:
				bot.reply_to(message, 'Ты бы хотел(а) быть бессмертным?')
			if a == 67:
				bot.reply_to(message, 'Сколько максимально ты б хотел(а) иметь детей?')
			if a == 68:
				bot.reply_to(message, 'Закончи реплику: «От меня можно ожидать чего угодно, когда я…»')
			if a == 69:
				bot.reply_to(message, 'Главное и самое значимое событие в этом году?')
			if a == 70:
				bot.reply_to(message, 'От какой вредной привычки, по твоему мнению, отказаться сложнее всего?')
			if a == 71:
				bot.reply_to(message, 'Какими делами ты готов(а) заниматься круглосуточно?')
			if a == 72:
				bot.reply_to(message, 'Что тебя изматывает и опустошает больше всего?')
			if a == 73:
				bot.reply_to(message, 'Причина, по которой ты общаешься с лучшими друзьями?')
			if a == 74:
				bot.reply_to(message, 'О чем ты думаешь больше всего в последнее время?')
			if a == 75:
				bot.reply_to(message, 'Какие ситуации или события своей жизни ты хотел(а) бы забыть навсегда?')
			if a == 76:
				bot.reply_to(message, 'Твоя главная победа за последнее время?')
			if a == 77:
				bot.reply_to(message, 'Какой из дней за последнее время был самым эффективным?')
			if a == 78:
				bot.reply_to(message, 'С какой мыслью ты чаще всего просыпаешься?')
			if a == 79:
				bot.reply_to(message, 'Самый бесполезный твой талант?')
			if a == 80:
				bot.reply_to(message, 'Ты хотел(а) бы жить в другой стране?')
			if a == 81:
				bot.reply_to(message, 'Твоя самая бесполезная покупка за год?')
			if a == 82:
				bot.reply_to(message, 'Во что ты верил в прошлом году, но перестал верить в этом?')
			if a == 83:
				bot.reply_to(message, 'Какие фильмы ты считаешь самыми лучшими?')
			if a == 84:
				bot.reply_to(message, 'Что было самым сложным для тебя на этой неделе?')
			if a == 85:
				bot.reply_to(message, 'Считаешь ли ты кого-то своим врагом?')
			if a == 86:
				bot.reply_to(message, 'Что тебя сегодня рассмешило?')
			if a == 87:
				bot.reply_to(message, 'Если бы можно было провести год жизни в любом месте мира, то в каком?')
			if a == 88:
				bot.reply_to(message, 'Каким было твое лучшее решение за год?')
			if a == 89:
				bot.reply_to(message, 'Назови одну маленькую вещь, которая может радовать тебя каждый день?')
			if a == 90:
				bot.reply_to(message, 'Какая твоя большая мечта?')
			if a == 91:
				bot.reply_to(message, 'Если бы можно было избавиться от одной привычки, то от какой?')
			if a == 92:
				bot.reply_to(message, 'Чем ты гордишься больше всего к этому моменту?')
			if a == 93:
				bot.reply_to(message, 'Если бы о твоей жизни снимали фильм, то какого он был бы жанра и как назывался?')
			if a == 94:
				bot.reply_to(message, 'Какое событие развернуло твою жизнь на 180 градусов?')
			if a == 95:
				bot.reply_to(message, 'О чем ты подумал(а), проснувшись сегодня утром?')
			if a == 96:
				bot.reply_to(message, 'Был ли в этом году день, после которого можно было бы сказать: «Так здорово, что можно уже и умирать»? Если да, то какой?')
			if a == 97:
				bot.reply_to(message, 'Тебя пугает старость?')
			if a == 98:
				bot.reply_to(message, 'На кого из родителей ты больше всего похож(а)?')
			if a == 99:
				bot.reply_to(message, 'Если бы ты сейчас попал(а) в прошлое, что бы ты сказал(а) себе-маленькому?')
			if a == 100:
				bot.reply_to(message, 'Как ты думаешь, что важнее: талант или трудолюбие?')
			if a == 101:
				bot.reply_to(message, 'Что ты делаешь, когда хочешь успокоиться?')
			if a == 102:
				bot.reply_to(message, 'На что бы ты никогда в жизни не пошел(а) даже за очень большие деньги?')
			if a == 103:
				bot.reply_to(message, 'Ты любишь делать или получать подарки?')
			if a == 104:
				bot.reply_to(message, 'Какой твой любимый праздник? ')
			if a == 105:
				bot.reply_to(message, 'Как ты видишь свою жизнь после выхода на пенсию?')
			if a == 106:
				bot.reply_to(message, 'Что ты должен(а) сделать в своей жизни такого, чтобы перед смертью подумать «да, жизнь удалась»?')
			if a == 107:
				bot.reply_to(message, 'Что заставляет тебя чувствовать себя лучше даже после очень ужасного дня?')
"""