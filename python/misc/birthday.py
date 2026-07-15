import sqlite3
from datetime import datetime
from config.config import bot, db_path



conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS birthday (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT NOT NULL,
        day TEXT NOT NULL,
        chat_id INT NOT NULL
    )
''')
conn.commit()

# Birthday list
async def birthday_real(event):
    if (event.is_private):
        await bot.send_message(event.chat.id, "Ця команда потрібна для груп, щоб Пумба вітав її участників в їх день народження!")
        return
    
    message = '<b>📜 Список днів народжень групи:</b>\n\n'

    try:
        cursor.execute('SELECT tag, day FROM birthday WHERE chat_id = ?', (event.chat.id,))
        birthday_group = cursor.fetchall()

        if birthday_group:
            i = 1
            for tag, day in birthday_group:
                message += f'{i}. {tag} - <i>{day}</i>\n'
                i += 1
        else:
            message += "<b><u>Список пустий</u></b>"
    except:
        pass

    message += f'<b>\n\n<b>✅ Додати день народження:</b>\n\
@tag дд.мм <i>(Наприклад: @PumbaBoarBot 20.05)</i>\n\n\
<b>❎ Видалити день народження:</b>\n\
@tag 00.00 <i>(Наприклад: @PumbaBoarBot 00.00)</i>'
					
    await bot.send_message(event.chat.id, message, parse_mode='html')

# Delete birthday
async def birthday_add_delete(event):
    message_text = event.text

    if len(message_text) > 5:
        if (message_text[0] == '@' and message_text[-3] == '.' and message_text[-6] == ' ' and message_text.count(' ') == 1):
            
            month_birthday = message_text[-2:]
            day_birthday = message_text[-5:-3]

            try:
                month = int(month_birthday)
                day = int(day_birthday)
            except ValueError:
                return
            
            space_index = message_text.find(' ')
            tag = message_text[1:space_index]
            
            if (month == 00 and day == 00):
                cursor.execute('DELETE FROM birthday WHERE tag = ?', (tag,))
                conn.commit()
                if cursor.rowcount >= 1:
                    await event.reply(f'День народження <i><b>@{tag}</i></b> видалено!', parse_mode = 'html')
                else:
                    await event.reply(f'День народження <i><b>@{tag}</i></b> не було зареєстровано.', parse_mode = 'html')
                    return
                
            if (month <= 12 and month >=1 and day <= 31 and day >= 1):
                    cursor.execute('SELECT tag FROM birthday WHERE chat_id = ?', (event.chat.id,))
                    tags_group = cursor.fetchall()

                    for tag_group in tags_group:
                        if (tag_group[0] == tag):
                            await event.reply(f'День народження <i><b>@{tag}</i></b> вже зареєстровано!', parse_mode = 'html')
                            return
                    
                    if (day < 10):
                        day_to_str = '0' + str(day)
                    else:
                        day_to_str = day

                    if (month < 10):
                        month_to_str = '0' + str(month)
                    else:
                        month_to_str = month

                    date_of_birthday = f"{day_to_str}.{month_to_str}"

                    cursor.execute('INSERT INTO birthday (tag, day, chat_id) VALUES (?, ?, ?)', (tag, date_of_birthday, event.chat.id))
                    conn.commit()

                    await event.reply(f'День народження зареєстровано:\n<b><i>@{tag}</i></b> - <i>{date_of_birthday}</i>', parse_mode = 'html')

# Birthday message
async def birthday_time():
    today = datetime.now().strftime('%d.%m')

    cursor.execute('SELECT tag, day, chat_id FROM birthday')
    birthdays = cursor.fetchall()

    for tag, day, chat_id in birthdays:
        if day == today:
            await bot.send_message(chat_id, f'🎉🎂 Вітаємо з днем народження <b>@{tag}</b>! 🎂🎉', parse_mode='html')