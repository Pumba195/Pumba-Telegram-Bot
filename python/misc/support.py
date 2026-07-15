import json

from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButtonRow, KeyboardButton
from config.config import bot,chat_id_pumba,my_id



# Support menu
async def handle_support(event):
	user = await bot.get_entity(event.sender_id)

	if event.text == '📝Підтримка🤔':
		return
	
	bot.remove_event_handler(handle_support)
	
	if event.text == '◀️Назад':
		return

	if event.chat_id > 0:
		user = await bot.get_entity(event.sender_id)

		await bot.send_message(chat_id_pumba, f"<b>Зворотній зв`язок від користувача:</b>\n\n\
<b>Ім`я:</b> <i>{user.first_name}</i>\n\
<b>Тег:</b> <i>@{user.username}</i>\n\
<b>ID:</b> <i>{user.id}</i>\n\n\
<i>Повідомлення:</i>", parse_mode = 'html')
		
		await bot.forward_messages(chat_id_pumba, event._message_id, event.chat.id)

		try:
			with open('support/admins.json', 'r') as f:
				admin = json.load(f)
		except FileNotFoundError:
			admin = []
		
		if event.chat.id in admin:
			await bot.send_message(event.chat.id, "<b>Дякую за зворотній зв`язок</b>, з вами зв`яжуться за потреби😉😈!", parse_mode = 'html', buttons=await page_start_admin())
		else:
			await bot.send_message(event.chat.id, "<b>Дякую за зворотній зв`язок</b>, з вами зв`яжуться за потреби😉!", parse_mode = 'html', buttons=await page_start())
	return



# Pages
async def page_support_back():
	return ReplyKeyboardMarkup(
		[
			KeyboardButtonRow(
				[
					KeyboardButton(text = "◀️Назад")
				]
			)
		],
		resize=True
	)

async def page_start():
	return ReplyKeyboardMarkup(
		[
			KeyboardButtonRow(
				[
					KeyboardButton(text = "🐗Pumba🐗"),
					KeyboardButton(text = "📝Підтримка🤔")
				]
			)
		],
		resize=True
	)

async def page_start_admin():
	return ReplyKeyboardMarkup(
		[
			KeyboardButtonRow(
				[
					KeyboardButton(text = "🐗Pumba🐗"),
					KeyboardButton(text = "📝Підтримка🤔")
				]
			),
			KeyboardButtonRow(
				[
					KeyboardButton(text = "🔊Розсилка📢"),
	 				KeyboardButton(text = "❔Відповідь❓")
				]
			)
		],
		resize=True
	)