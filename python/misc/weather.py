import json
import os

from config.config import bot,owm
from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback



# Weather 
# Function for saving data to a file
async def save_data_weather(data):
	directory = 'support'
	os.makedirs(directory, exist_ok=True) 
	file_path = f'{directory}/weather_chats.json'

	with open(file_path, 'w') as f:
		json.dump(data, f)

# Function for loading data from a file
async def load_data_weather():
    try:
        with open('support/weather_chats.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}



# Commands
# Buttons
async def send_weather(event):
	murkup_inline = ReplyInlineMarkup(
			[
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Вінниця',
							data = b'Vinnytsia'
						),
						KeyboardButtonCallback(
							text = 'Дніпро',
							data = b'Dnipro'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Донецьк',
							data = b'Donetsk'
						),
						KeyboardButtonCallback(
							text = 'Житомир',
							data = b'Zhytomyr'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Запоріжжя',
							data = b'Zaporizhzhia'
						),
						KeyboardButtonCallback(
							text = 'Івано-Франківськ',
							data = b'Ivano-Frankivsk'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Київ',
							data = b'Kyiv'
						),
						KeyboardButtonCallback(
							text = 'Кропивницький',
							data = b'Kropyvnytskyi'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Луганськ',
							data = b'Luhansk'
						),
						KeyboardButtonCallback(
							text = 'Луцьк',
							data = b'Lutsk'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Львів',
							data = b'Lviv'
						),
						KeyboardButtonCallback(
							text = 'Миколаїв',
							data = b'Mykolaiv'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Далі➡️',
							data = b'Enter'
						)
					]
				)
			]
		)
	await bot.send_message(event.chat.id,"Оберіть місто для перегляду погоди в ньому", buttons = murkup_inline)
	return

# Comand weather
async def send_weather_srazu(event):
	weather_chats = await load_data_weather()
	chat_id = str(event.chat_id)
	x = weather_chats.get(chat_id, 'хуй')
	city = x
	if x == 'хуй':
		await send_weather(event)
		return
	if x == 'Vinnytsia, UA':
		city = 'Вінниця'
	if x == 'Dnipro, UA':
		city = 'Дніпро'
	if x == 'Donetsk, UA':
		city = 'Донецьк'
	if x == 'Zhytomyr, UA':
		city = 'Житомир'
	if x == 'Zaporizhzhia, UA':
		city = 'Запоріжжя'
	if x == 'Ivano-Frankivsk, UA':
		city = 'Івано-Франківськ'
	if x == 'Kyiv, UA':
		city = 'Київ'
	if x == 'Kropyvnytskyi, UA':
		city = 'Кропивницький'
	if x == 'Luhansk, UA':
		city = 'Луганськ'
	if x == 'Lutsk, UA':
		city = 'Луцьк'
	if x == 'Lviv, UA':
		city = 'Львів'
	if x == 'Mykolaiv, UA':
		city = 'Миколаїв'
	if x == 'Odessa, UA':
		city = 'Одеса'
	if x == 'Poltava, UA':
		city = 'Полтава'
	if x == 'Rivne, UA':
		city = 'Рівне'
	if x == 'Sumy, UA':
		city = 'Суми'
	if x == 'Ternopil, UA':
		city = 'Тернопіль'
	if x == 'Uzhgorod, UA':
		city = 'Ужгород'
	if x == 'Kharkiv, UA':
		city = 'Харків'
	if x == 'Kherson, UA':
		city = 'Херсон'
	if x == 'Khmelnytskyi, UA':
		city = 'Хмельницький'
	if x == 'Cherkasy, UA':
		city = 'Черкаси'
	if x == 'Chernivtsi, UA':
		city = 'Чернівці'
	if x == 'Chernihiv, UA':
		city = 'Чернігів'
	await send_weather_city_srazu(event,city,x)



# Weather continue
async def send_weather_city_srazu(event,city,place):
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(place)
	w = observation.weather
	temper = w.temperature('celsius')['temp']
	wind = w.wind()['speed']
	
	uapog = w.detailed_status

	try:
		uapog = await weather_ua(str(w.detailed_status))
	except:
		uapog = w.detailed_status

	await bot.send_message(event.chat.id, f'\
	<b><i>🇺🇦{city}🇺🇦</i></b>\
	\n☀️<b>Погода:</b> <i>{uapog}</i>\
	\n🌡<b>Середня температура:</b> <i>{temper}</i>\
	\n💨<b>Швидкість вітру:</b> <i>{wind}</i>\
	\n💧<b>Вологість:</b> <i>{w.humidity}</i>\
	\n☁️<b>Хмарність:</b> <i>{w.clouds}</i>',
	parse_mode = 'html')
	return

# Send weather after click
async def send_weather_city(event,city,place):
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(place)
	w = observation.weather
	temper = w.temperature('celsius')['temp']
	wind = w.wind()['speed']
	
	uapog = w.detailed_status

	try:
		uapog = await weather_ua(str(w.detailed_status))
	except:
		uapog = w.detailed_status

	await bot.edit_message(event.chat.id, event._message_id,
	text = f'\
	<b><i>🇺🇦{city}🇺🇦</i></b>\
	\n☀️<b>Погода:</b> <i>{uapog}</i>\
	\n🌡<b>Середня температура:</b> <i>{temper}</i>\
	\n💨<b>Швидкість вітру:</b> <i>{wind}</i>\
	\n💧<b>Вологість:</b> <i>{w.humidity}</i>\
	\n☁️<b>Хмарність:</b> <i>{w.clouds}</i>',
	parse_mode = 'html')
	return



# Weather translation
async def weather_ua(weather):
	# rain
	if weather == "heavy intensity rain":
		uapog = '⛈ Сильний дощ ⛈'
	if weather == 'moderate rain':
		uapog = '🌧 помірний дощ 🌧'
	if weather == 'light rain':
		uapog = '🌧 невеликий дощ 🌧'

	# cloudy
	if weather == "overcast clouds":
		uapog = '☁️ похмурі хмари ☁️'
	if weather == "broken clouds":
		uapog = '☁️ розірвані хмари ☁️'
	if weather == "few clouds":
		uapog = '🌤 трохи хмарно 🌤'
	if weather == "cloudy":
		uapog = '☁️ хмарно ☁️'
	if weather == "scattered clouds":
		uapog = '☁️ розсіяні хмари ☁️'

	# snow
	if weather == "heavy intensity snow":
		uapog = '☃️ сильний сніг ☃️'
	if weather == 'moderate snow':
		uapog = '🌨 помірний сніг 🌨'
	if weather == "light snow":
		uapog = '🌨 невеликий сніг 🌨'
	if weather == "rain and snow":
		uapog = '🌧 дощ та сніг 🌨'
	if weather == "snow":
		uapog = '❄️ сніжок ❄️'
	

	# sunny
	if weather == "clear sky":
		uapog = '☀ безхмарно ☀'

	return uapog



# Weather Katowice
async def send_weather_katowice(event):
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place("Katowice, PL")
	w = observation.weather
	temper = w.temperature('celsius')['temp']
	wind = w.wind()['speed']

	uapog = w.detailed_status

	try:
		uapog = await weather_ua(str(w.detailed_status))
	except:
		uapog = w.detailed_status

	await bot.send_message(event.chat.id, f'\
	<b><i>🇵🇱Katowice🇵🇱</i></b>\
	\n☀️<b>Погода:</b> <i>{uapog}</i>\
	\n🌡<b>Середня температура:</b> <i>{temper}</i>\
	\n💨<b>Швидкість вітру:</b> <i>{wind}</i>\
	\n💧<b>Вологість:</b> <i>{w.humidity}</i>\
	\n☁️<b>Хмарність:</b> <i>{w.clouds}</i>',
	parse_mode = 'html')
	return