import random
import os

from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback

from config.config import bot
from games.tic_tac_toe import format_board,get_game_data,save_game_data,check_winner,tictactoe_button
from games.rock_paper_scissors import get_result
from misc.weather import save_data_weather,load_data_weather,send_weather_city
from misc.other_func import send_callall_baza



# Click Button
async def button(event):
# Callall
    if event.data == b'baza':
        await bot.delete_messages(event.chat.id, event._message_id)
        await send_callall_baza(event)
        return
    
    if event.data == b'back':
        await bot.delete_messages(event.chat.id, event._message_id)
        return
    
# Rock paper scissors 👊✌️✋
    if event.data == b'stone' or event.data == b'scissors' or event.data == b'paper':
        options = ['👊Камінь👊', '✌️Ножиці✌️', '✋Папір✋']

        if event.data == b'stone':
            user_choice = '👊Камінь👊'
        if event.data == b'scissors':
            user_choice = '✌️Ножиці✌️'
        if event.data == b'paper':
            user_choice = '✋Папір✋'

        bot_choice = random.choice(options)
        user = await bot.get_entity(event.sender_id)
        username = user.first_name
        result = await get_result(user_choice, bot_choice, username) 
        response = f"<i>{username} обрав:</i> <b>{user_choice}</b>\n<i>Пумба обрав:</i> <b>{bot_choice}</b>\n<i>Результат:</i> <b>{result}</b>"
    
        await bot.edit_message(event.chat.id, event._message_id, text=response, parse_mode = 'html')
        return


# Weather
    if event.data == b'Enter':
        murkup_inline = ReplyInlineMarkup(
			[
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Одеса',
							data = b'Odesa'
						),
						KeyboardButtonCallback(
							text = 'Полтава',
							data = b'Poltava'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Рівне',
							data = b'Rivne'
						),
						KeyboardButtonCallback(
							text = 'Суми',
							data = b'Sumy'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Тернопіль',
							data = b'Ternopil'
						),
						KeyboardButtonCallback(
							text = 'Ужгород',
							data = b'Uzhhorod'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Харків',
							data = b'Kharkiv'
						),
						KeyboardButtonCallback(
							text = 'Херсон',
							data = b'Kherson'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Хмельницький',
							data = b'Khmelnytskyi'
						),
						KeyboardButtonCallback(
							text = 'Черкаси',
							data = b'Cherkasy'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = 'Чернівці',
							data = b'Chernivtsi'
						),
						KeyboardButtonCallback(
							text = 'Чернігів',
							data = b'Chernihiv'
						)
					]
				),
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = '⬅️Назад',
							data = b'Behined'
						)
					]
				)
			]
		)
        await bot.edit_message(event.chat.id, event._message_id,text = 'Оберіть місто для перегляду погоди в ньому', buttons = murkup_inline)
        return
    
    if event.data == b'Behined':
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
        await bot.edit_message(event.chat.id, event._message_id,text = 'Оберіть місто для перегляду погоди в ньому', buttons = murkup_inline)
        return

    weather_chats = await load_data_weather()
    
    if event.data == b'Vinnytsia':
        city = 'Вінниця'
        place = 'Vinnytsia, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Dnipro':
        city = 'Дніпро'
        place = 'Dnipro, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Donetsk':
        city = 'Донецьк'
        place = 'Donetsk, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Zhytomyr':
        city = 'Житомир'
        place = 'Zhytomyr, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Zaporizhzhia':
        city = 'Запоріжжя'
        place = 'Zaporizhzhia, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Ivano-Frankivsk':
        city = 'Івано-Франківськ'
        place = 'Ivano-Frankivsk, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Kyiv':
        city = 'Київ'
        place = 'Kyiv, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Kropyvnytskyi':
        city = 'Кропивницький'
        place = 'Kropyvnytskyi, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Luhansk':
        city = 'Луганськ'
        place = 'Luhansk, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Lutsk':
        city = 'Луцьк'
        place = 'Lutsk, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Lviv':
        city = 'Львів'
        place = 'Lviv, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Mykolaiv':
        city = 'Миколаїв'
        place = 'Mykolaiv, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Odesa':
        city = 'Одеса'
        place = 'Odessa, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Poltava':
        city = 'Полтава'
        place = 'Poltava, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Rivne':
        city = 'Рівне'
        place = 'Rivne, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Sumy':
        city = 'Суми'
        place = 'Sumy, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Ternopil':
        city = 'Тернопіль'
        place = 'Ternopil, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Uzhhorod':
        city = 'Ужгород'
        place = 'Uzhgorod, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Kharkiv':
        city = 'Харків'
        place = 'Kharkiv, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Kherson':
        city = 'Херсон'
        place = 'Kherson, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Khmelnytskyi':
        city = 'Хмельницький'
        place = 'Khmelnytskyi, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Cherkasy':
        city = 'Черкаси'
        place = 'Cherkasy, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Chernivtsi':
        city = 'Чернівці'
        place = 'Chernivtsi, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    
    if event.data == b'Chernihiv':
        city = 'Чернігів'
        place = 'Chernihiv, UA'
        chat_id = str(event.chat_id)
        x = weather_chats.get(chat_id)
        if x != place:
            weather_chats[chat_id] = place
        await save_data_weather(weather_chats)
        await send_weather_city(event,city,place)
        return
    


    try:
        chat_id = event.chat_id
        game_data = await get_game_data(chat_id)
        last_player = game_data['last_player']
        players = game_data['players']
    except TypeError:
        await bot.edit_message(event.chat.id, event._message_id,text='Цієї партії більше не існує, <b>починайте нову!</b>', parse_mode = 'html')
        return
    
    user = await bot.get_entity(event.sender_id)

    if len(players) < 2:
        if user.username not in players:
            players.append(user.username)
            game_data['players'] = players
	    
    if not game_data:
        await event.answer("Щось пішло не так, спробуй ще раз /tictactoe")
        return

    i, j = map(int, event.data.split(b','))

    game_board = game_data['board']
    current_player = game_data['current_player']
    last_player = game_data['last_player']
    players = game_data['players']

    # Check if the player belongs to the current game
    if user.username not in players:
        await event.answer("Місця для гри закінчилися, почекай.")
        return

    # Check that the player can make a move (no more than once in a row)
    if user.username == last_player:
       await event.answer("Почекай, твій абонент тугодум!")
       return

    # Check that the cell is free
    if game_board[i][j] == '     ':
        game_board[i][j] = current_player

        # Checking if there is a winner
        winner = await check_winner(game_board)
        if winner:
            if last_player == players[0]:
                winn = players[1]
                loser = players[0]
            else:
                winn = players[0]
                loser = players[1]
		
            if winner == '❌':
                log = '⭕️'
            else:
                log = '❌'
		
            await bot.edit_message(event.chat.id, event._message_id,
                text=f"Гравець {winner} <b>{winn}</b> {winner} переміг🏆!\nА {log} <b>{loser}</b> {log} програв🙁\n\n{await format_board(game_board)}",
                parse_mode = 'html'
            )
            # Delete the game data file
            os.remove(f'tic_tac_toe/TT{chat_id}.json')
            return

        # Check that there are available moves
        if '     ' not in sum(game_board, []):
            await bot.edit_message(event.chat.id, event._message_id,
                text="Ніхто не переміг, сили виявилися рівними💪!\n\n" + await format_board(game_board),
                parse_mode = 'html'
            )
            # Delete the game data file
            os.remove(f'tic_tac_toe/TT{chat_id}.json')
            return

        # Change player
        current_player = '❌' if current_player == '⭕️' else '⭕️'

        # Updating the current game data
        game_data['board'] = game_board
        game_data['current_player'] = current_player
        game_data['last_player'] = user.username
        await save_game_data(chat_id, game_data)

        # Updating the keyboard with a new move
        keyboard = await tictactoe_button(game_board)
		
        if len(players) == 0:
            sec1 = ' — '
            sec2 = ' — '

        if len(players) == 1:
            sec1 = '@' + players[0]
            sec2 = ' — '

        if len(players) == 2:
            sec1 = '@' + players[0]
            sec2 = '@' + players[1]
		
        playy = ' — '
        if len(players) == 2:
            if last_player == players[0]:
                playy = players[0]
            else:
                playy = players[1]
		
        await bot.edit_message(event.chat.id, event._message_id,
            text="--------------------------------------------\nХід гравця: " + current_player + ' ' + playy + ' ' + current_player + "\n--------------------------------------------\
\nГравці:\n" + "❌ " + sec1 + " ❌" + "\n" + "⭕️ " + sec2 + " ⭕️" +  "\n\n" + await format_board(game_board),
            parse_mode = 'html',
            buttons=keyboard
        )