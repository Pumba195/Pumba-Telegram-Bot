import json
import os

from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback
from config.config import bot



#TIC TAC TOE
# Function for formatting the board
async def format_board(game_board):
    board_str = ''
    for row in game_board:
        board_str += ' | '.join(row) + '\n'
    return board_str

# Function for creating a new game
async def new_game(chat_id):
    game_board = [['     ' for _ in range(3)] for _ in range(3)]
    current_player = '❌'
    last_player = None
    players = []
    game_data = {'board': game_board, 'current_player': current_player, 'last_player': last_player, 'players': players}
    await save_game_data(chat_id, game_data)

# Function to get data of the current game
async def get_game_data(chat_id):
    try:
        with open(f'tic_tac_toe/TT{chat_id}.json', 'r') as f:
            game_data = json.load(f)
        return game_data
    except FileNotFoundError:
        return None

# Function for saving the current game data
async def save_game_data(chat_id, game_data):
    directory = 'tic_tac_toe'
    os.makedirs(directory, exist_ok=True) 
    file_path = f'{directory}/TT{chat_id}.json'
    with open(file_path, 'w') as f:
        json.dump(game_data, f)

# Processing the /tictactoe command
async def tictactoe_main(event):
    if event.chat_id > 0:
        await event.reply('Це гра як мінімум для двох людей!\nЗ ботом грати не можна, нажаль :(', parse_mode = 'html')
        return
	    
    chat_id = event.chat_id
    game_data = await get_game_data(chat_id)

    if not game_data:
        await new_game(chat_id)
        game_data = await get_game_data(chat_id)

    game_board = game_data['board']
    current_player = game_data['current_player']
    last_player = game_data['last_player']
    players = game_data['players']

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
	    
    await bot.send_message(chat_id, "--------------------------------------------\n\
Хід гравця: " + current_player + ' ' + playy + ' ' + current_player + "\
\n--------------------------------------------\
\nГравці:\n\
" + "❌ " + sec1 + " ❌" + "\n\
" + "⭕️ " + sec2 + " ⭕️" +  "\n\n\
" + await format_board(game_board), parse_mode = 'html', buttons=keyboard)

# Function to check the winner
async def check_winner(game_board):
    for i in range(3):
        if game_board[i][0] == game_board[i][1] == game_board[i][2] and game_board[i][0] != '     ':
            return game_board[i][0]
        if game_board[0][i] == game_board[1][i] == game_board[2][i] and game_board[0][i] != '     ':
            return game_board[0][i]
    if game_board[0][0] == game_board[1][1] == game_board[2][2] and game_board[0][0] != '     ':
        return game_board[0][0]
    if game_board[0][2] == game_board[1][1] == game_board[2][0] and game_board[0][2] != '     ':
        return game_board[0][2]
    return None

# Buttons
async def tictactoe_button(game_board):
    return ReplyInlineMarkup(
			[
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = game_board[0][0],
							data = b"0,0"
						),
						KeyboardButtonCallback(
							text = game_board[0][1],
							data = b"0,1"
						),
						KeyboardButtonCallback(
							text = game_board[0][2],
							data = b"0,2"
						)
					]
				),
                KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = game_board[1][0],
							data = b"1,0"
						),
						KeyboardButtonCallback(
							text = game_board[1][1],
							data = b"1,1"
						),
						KeyboardButtonCallback(
							text = game_board[1][2],
							data = b"1,2"
						)
					]
				),
                    KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = game_board[2][0],
							data = b"2,0"
						),
						KeyboardButtonCallback(
							text = game_board[2][1],
							data = b"2,1"
						),
						KeyboardButtonCallback(
							text = game_board[2][2],
							data = b"2,2"
						)
					]
				)
			]
		)
    
# Delete a previous game
async def tictactoe(event):
	if event.chat_id > 0:
		await event.reply("Ця команда працює лише в групах, вона потрібна для видалення минулої гри в хрестики-нулики")
		return
	try:
		os.remove(f'tic_tac_toe/TT{event.chat_id}.json')
		await event.reply('Минулу партію було видалено, <b>можете починати нову!</b>', parse_mode = 'html')
		return
	except FileNotFoundError:
		await event.reply('Минулої партії не існує, <b>можете починати нову!</b>', parse_mode = 'html')