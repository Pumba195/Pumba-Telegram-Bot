from telethon.tl.types import ReplyInlineMarkup, KeyboardButtonRow, KeyboardButtonCallback
from config.config import bot



# Rock paper scissors 👊✌️✋
async def start_game(event):
    inline_markup = ReplyInlineMarkup(
			[
				KeyboardButtonRow(
					[
						KeyboardButtonCallback(
							text = "👊",
							data = b'stone'
						),
						KeyboardButtonCallback(
							text = "✌️",
							data = b'scissors'
						),
						KeyboardButtonCallback(
							text = "✋",
							data = b'paper'
						)
					]
				)
			]
		)
    
    await bot.send_message(event.chat.id,"<b>👊Камінь,✌️Ножиці,✋Папір</b>\nГотовий програти <b>Пумбі?</b>\nНу тоді <b>обирай)</b>", parse_mode = 'html', buttons=inline_markup)

# Result
async def get_result(user_choice, bot_choice, username):
    if user_choice == bot_choice:
        return "Нічия!"
    elif (user_choice == '👊Камінь👊' and bot_choice == '✌️Ножиці✌️') or \
         (user_choice == '✌️Ножиці✌️' and bot_choice == '✋Папір✋') or \
         (user_choice == '✋Папір✋' and bot_choice == '👊Камінь👊'):
        return f"{username} переміг!"
    else:
        return "Пумба переміг!"