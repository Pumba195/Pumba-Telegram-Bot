import schedule
from telethon import events
import asyncio

import sys
import os

# ------------------------------------------------------------------ import files ------------------------------------------------------------------

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.dont_write_bytecode = True

from config.config import bot
from games.tic_tac_toe import tictactoe_main,tictactoe
from games.rock_paper_scissors import start_game
from misc.weather import send_weather,send_weather_srazu
from misc.count_word import my_words,top_ten
from misc.swear import enable_greetings,disable_greetings
from misc.callback import button
from misc.birthday import birthday_real,birthday_time
from misc.hello_buy import welcome_new_members,goodbye_member
from misc.all_rates import send_rates,send_crypto,send_petrol
from misc.other_func import send_rnumb,send_rcoin,send_alert,gruz200,send_info,send_callall_message,send_start,excel_realized
from misc.other_func import send_random_user
from misc.all_word import all_message
from misc.admin_func import register_admin_real,delate_admin_real,admin_panel,admin_info_real,all_chats_real,register_word,delete_word,list_words,ban_user,unban_user,ban_user_list,enabled_chats_real
# from misc.other_func import send_schedule_0830,send_schedule_1000,send_schedule_1200,send_schedule_1330

# ----------------------------------------------------------------------- commands -----------------------------------------------------------------------



#Start
@bot.on(events.NewMessage(pattern='/start'))
async def send_start_command(event):
	await send_start(event)



# ---------------------------- Tic tac toe ----------------------------
# Start game
@bot.on(events.NewMessage(pattern='/tictactoe'))
async def tictactoe_main_command(event):
	await tictactoe_main(event)

# Delete game
@bot.on(events.NewMessage(pattern='/delete_game'))
async def tictactoe_command(event):
	await tictactoe(event)



# Rock paper scissors 👊✌️✋
@bot.on(events.NewMessage(pattern='/rps'))
async def start_command(event):
	await start_game(event)



# ---------------------------- Weather ----------------------------
# Set weather  
@bot.on(events.NewMessage(pattern='/set_weather'))
async def send_weather_command(event):
	await send_weather(event)
	
# Show weather  
@bot.on(events.NewMessage(pattern='/weather'))
async def send_weather_srazu_command(event):
	await send_weather_srazu(event)



# Handling button presses
@bot.on(events.CallbackQuery)
async def button_command(event):
	await button(event)



# ---------------------------- Words count ----------------------------
# Show my words
@bot.on(events.NewMessage(pattern='/my_words'))
async def my_words_command(event):
	await my_words(event)

# Show top 10 user
@bot.on(events.NewMessage(pattern='/top_ten'))
async def top_ten_command(event):
	await top_ten(event)



# ---------------------------- Swear ----------------------------
# Swear on
@bot.on(events.NewMessage(pattern='/matuki_on'))
async def enable_greetings_command(event):
    await enable_greetings(event)

# Swear off
@bot.on(events.NewMessage(pattern='/matuki_off'))
async def disable_greetings_command(event):
    await disable_greetings(event)



# Hello/Buy
@bot.on(events.ChatAction)
async def chat_action(event):
	if event.action_message:
		if event.user_joined or event.user_added:
			await welcome_new_members(event)
			return
		if event.user_left or event.user_kicked:
			await goodbye_member(event)



# ---------------------------- Rates ----------------------------
# Rates of currency
@bot.on(events.NewMessage(pattern='/rates'))
async def send_rates_command(event):
	await send_rates(event)

# Rates of crypto
@bot.on(events.NewMessage(pattern='/crypto'))
async def send_crypto_command(event):
	await send_crypto(event)

# Rates of fuel
@bot.on(events.NewMessage(pattern='/petrol'))
async def send_petrol_command(event):
	await send_petrol(event)



# ---------------------------- Misc ----------------------------
# Excel
@bot.on(events.NewMessage(pattern='/excel'))
async def excel_command(event):
	await excel_realized(event)

# Random number
@bot.on(events.NewMessage(pattern='/number'))
async def send_rnumb_command(event):
	await send_rnumb(event)

# Random coin
@bot.on(events.NewMessage(pattern='/coin'))
async def send_rcoin_command(event):
	await send_rcoin(event)	

# Alert
@bot.on(events.NewMessage(pattern='/alert'))
async def send_support_command(event):
	await send_alert(event)

# Losses
@bot.on(events.NewMessage(pattern='/losses'))
async def gruz200_command(event):
	await gruz200(event)

# Informations
@bot.on(events.NewMessage(pattern='/info'))
async def send_info_command(event):
	await send_info(event)

# Callall
@bot.on(events.NewMessage(pattern='/callall'))
async def send_callall_command(event):
	await send_callall_message(event)

# Random user
@bot.on(events.NewMessage(pattern='/random_user'))
async def send_random_user_command(event):
	await send_random_user(event)

# Birthday
@bot.on(events.NewMessage(pattern='/birthday'))
async def birthday_command(event):
	await birthday_real(event)



# ---------------------------- Admin ----------------------------
# Registration new admin
@bot.on(events.NewMessage(pattern='/register_admin'))
async def register_admin_command(event):
	await register_admin_real(event)

# Removing admins
@bot.on(events.NewMessage(pattern='/delete_admin'))
async def delate_admin_command(event):
	await delate_admin_real(event)

# Dismiss all admins
@bot.on(events.NewMessage(pattern='/id_admin'))
async def admin_info_command(event):
	await admin_info_real(event)

# Display a message for admins
@bot.on(events.NewMessage(pattern='/admin'))
async def admin_panel_command(event):
	await admin_panel(event)

# Display all chats
@bot.on(events.NewMessage(pattern='/all_chats'))
async def all_chats_command(event):
	await all_chats_real(event)

# Display all chats where swear words are enabled
@bot.on(events.NewMessage(pattern='/chats_enabled'))
async def enabled_chats_real_command(event):
	await enabled_chats_real(event)

# Adding trigger words
@bot.on(events.NewMessage(pattern='/register_word'))
async def register_word_command(event):
	await register_word(event)

# Removing trigger words
@bot.on(events.NewMessage(pattern='/delete_word'))
async def delete_word_command(event):
   await delete_word(event)

# Display all swear words
@bot.on(events.NewMessage(pattern='/list_words'))
async def list_words_command(event):
   await list_words(event)

# Ban users
@bot.on(events.NewMessage(pattern='/ban'))
async def ban_user_comand(event):
   await ban_user(event)

# Unban users
@bot.on(events.NewMessage(pattern='/unban'))
async def unban_user_command(event):
   await unban_user(event)

# List of IDs of all banned users
@bot.on(events.NewMessage(pattern='/users_ban_list'))
async def ban_user_list_command(event):
   await ban_user_list(event)

   

# # Test
# @bot.on(events.NewMessage(pattern='/test'))
# async def send_test_message(event):
#    await send_test_message(event)



# All words
@bot.on(events.NewMessage)
async def all_message_command(event):
	await all_message(event,events)


# ---------------------------- Time message ----------------------------
async def main():
	#Schedule
	# schedule.every().day.at("08:30").do(lambda: asyncio.create_task(send_schedule_0830()))
	# schedule.every().day.at("10:00").do(lambda: asyncio.create_task(send_schedule_1000()))
	# schedule.every().day.at("12:00").do(lambda: asyncio.create_task(send_schedule_1200()))
	# schedule.every().day.at("13:30").do(lambda: asyncio.create_task(send_schedule_1330()))

	#Birthday
	schedule.every().day.at("12:00").do(lambda: asyncio.create_task(birthday_time()))

	while True:
		schedule.run_pending()
		await asyncio.sleep(1)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(bot.disconnect())
        loop.close()