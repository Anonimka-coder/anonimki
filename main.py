import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
import sqlite3
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram import types


connection1 = sqlite3.connect('present.db')
cursor1 = connection1.cursor()

cursor1.execute('''
CREATE TABLE IF NOT EXISTS present (
id INTEGER PRIMARY KEY,
user_id TEXT NOT NULL,
arg TEXT
)
''')

connection = sqlite3.connect('users.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
user_id TEXT NOT NULL,
username TEXT NOT NULL,
arg TEXT NOT NULL,
sec INTEGER NOT NULL,
amount_of_mess INTEGER,
rang TEXT NOT NULL,
admin INTEGER
)
''')



cursor.execute('SELECT id, user_id, username, arg, sec FROM users')
users = cursor.fetchall()

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)

bot = Bot(token="6139558598:AAG5HZkc4ao75_W6WBU4FfNOOyx4OXgopj8")
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def handler(message: Message, bot: Bot,command: Command = None):
  if command:
    args = command.args
    try: 
        reference = decode_payload(args)
    except:
        reference = ''
    print(reference)
    cursor.execute('SELECT user_id, sec FROM users')
    users = cursor.fetchall()
    ides = [el[0] for el in users]
    cursor.execute('SELECT user_id FROM users WHERE sec = -1')
    names = [el[0] for el in cursor.fetchall()]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Отменить" , callback_data = "back")
    )
    builder.row(types.InlineKeyboardButton(
        text="Профиль 👤" , callback_data = "profile")
    )
    builder1 = InlineKeyboardBuilder()
    builder1.row(types.InlineKeyboardButton(
        text="Профиль 👤" , callback_data = "profile")
    )
    if str(message.from_user.id) in names:
        await message.answer(f"Просим прощения, бот находится на тех. обслуживании. Следите за сообщениями!")
    elif str(message.from_user.id) not in ides and reference == '':
        cursor.execute('INSERT INTO users (user_id, username, arg, sec, rang, amount_of_mess) VALUES (?, ?, ?, ?, ?, ?)', (f'{message.from_user.id}', f'{message.from_user.username}', f'{reference}', 1, 'Бронзовый', 0))
        connection.commit()
        cursor1.execute('INSERT INTO present (user_id, arg) VALUES(?, ?)', (f'{message.from_user.id}', ''))
        connection1.commit()
        link = await create_start_link(bot,(message.from_user.id), encode=True)
        await message.answer(f"👹 А теперь и ты начни получать <b>анонимные сообщения</b>!\n\nВот твоя <b>ссылка</b>:\n👉🏿 {link}\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", parse_mode=ParseMode.HTML, reply_markup=builder1.as_markup())
    elif str(message.from_user.id) not in ides and reference != '':
        cursor1.execute('INSERT INTO present (user_id, arg) VALUES(?, ?)', (f'{message.from_user.id}', ''))
        connection1.commit()
        cursor.execute('INSERT INTO users (user_id, username, arg, sec, rang, amount_of_mess) VALUES (?, ?, ?, ?, ?, ?)', (f'{message.from_user.id}', f'{message.from_user.username}', f'{reference}', 1, 'Бронзовый', 0))
        connection.commit()
        link = await create_start_link(bot,(message.from_user.id), encode=True)
        await message.answer(f"👹 Здесь можно отправить <b>анонимный вопрос</b> человеку, который опубликовал ссылку\n\n✍️ Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение <b>анонимно</b>\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
    elif str(message.from_user.id) in ides and reference != '':
        cursor.execute('UPDATE users SET arg = ? WHERE user_id = ?', (f'{reference}', f'{message.from_user.id}'))
        cursor.execute('UPDATE users SET sec = ? WHERE user_id = ?', (1, f'{message.from_user.id}'))
        connection.commit()
        await message.answer(f"👹 Здесь можно отправить <b>анонимный вопрос</b> человеку, который опубликовал ссылку\n\n✍️ Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение <b>анонимно</b>\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", reply_markup=builder.as_markup(), parse_mode=ParseMode.HTML)
    else:
        link = await create_start_link(bot,(message.from_user.id), encode=True)
        await message.answer(f"👹 А теперь и ты начни получать <b>анонимные сообщения</b>!\n\nВот твоя <b>ссылка</b>:\n👉🏿 {link}\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", parse_mode=ParseMode.HTML, reply_markup=builder1.as_markup())
@dp.message(Command("admin"))
async def handler(message: Message, bot: Bot,command: Command = None):
    cursor1.execute(f"SELECT * FROM present")
    users = [el for el in cursor1.fetchall()]
    await message.answer(f"участн {users}")


@dp.callback_query(F.data == "back")
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    cursor.execute('UPDATE users SET sec = ? WHERE user_id = ?', (0, f'{callback_query.from_user.id}'))
    link = await create_start_link(bot,str(callback_query.from_user.id), encode=True)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Профиль 👤" , callback_data = "profile")
    )
    await callback_query.message.answer(f"👹 А теперь и ты начни получать <b>анонимные сообщения</b>!\n\nВот твоя <b>ссылка</b>:\n👉🏿 {link}\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
    
@dp.callback_query(F.data == "stats")
async def callback_query_handler(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    cursor.execute(f"SELECT username FROM users")
    user = ["@" + el[0] for el in cursor.fetchall()]
    last15 = ", ".join(user[len(user) - 15: len(user)])
    await callback_query.message.answer(f"Всего {len(user)} пользователей\n\nласт 15: {last15}")
        
        
@dp.message(F.text)
async def enter_volume(message: types.Message):
    answer = message.text
    cursor.execute(f"SELECT sec, arg, username, amount_of_mess FROM users WHERE user_id = {str(message.from_user.id)}")
    user = list(cursor.fetchall()[0])
    mes_id = str(message.from_user.id)
    user_sec = user[0]
    user_arg = user[1]
    user_name = user[2]
    user_mess = user[3]
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Профиль 👤" , callback_data = "profile")
    )
    if user_arg == str(message.chat.id):
        await bot.send_message(user_arg, f"Нельзя отправлять сообщение самому себе!", reply_to_message_id=message.message_id)
    elif user_sec == -1:
        await message.answer(f"Просим прощения, бот находится на тех. обслуживании. Следите за сообщениями!")
    elif user_sec == 1 and user_arg != '':
        cursor.execute(f"SELECT user_id FROM users WHERE admin = 1")
        admins = [el[0] for el in cursor.fetchall()]
        if user_arg in admins:
            text = f"❗️<b>У тебя новое анонимное сообщение!</b>\n\n<span class='tg-spoiler'>{answer}</span>"
            message = await bot.send_message(user_arg, text, parse_mode=ParseMode.HTML)
            await bot.send_message(user_arg, f"От: @{user_name}", reply_to_message_id=message.message_id)
        else:
            text = f"❗️<b>У тебя новое анонимное сообщение!</b>\n\n<span class='tg-spoiler'>{answer}</span>"
            message = await bot.send_message(user_arg, text, parse_mode=ParseMode.HTML)
            cursor1.execute(f'SELECT arg FROM present WHERE user_id = {user_arg}')
            useeri = ''.join(list(cursor1.fetchall()[0])).split(", ")
            useeri.append(str(message.chat.id))
            print(useeri)
            cursor1.execute('UPDATE present SET arg = ? WHERE user_id = ?', (f'{", ".join(list(set(useeri)))}', f'{user_arg}'))
        cursor.execute('UPDATE users SET sec = ? WHERE user_id = ?', (0, f'{mes_id}'))
        cursor.execute('UPDATE users SET amount_of_mess = ? WHERE user_id = ?', (user_mess + 1, f'{mes_id}'))
        if user_mess >= 49 and user_mess < 199:
            cursor.execute('UPDATE users SET rang = ? WHERE user_id = ?', ('Серебряный 🪨', f'{mes_id}'))
        if user_mess >= 199 and user_mess < 999:
            cursor.execute('UPDATE users SET rang = ? WHERE user_id = ?', ('Золотой 🧈', f'{mes_id}'))
        if user_mess >= 999 and user_mess < 4999:
            cursor.execute('UPDATE users SET rang = ? WHERE user_id = ?', ('Алмазный 🔷', f'{mes_id}'))
        if user_mess >= 4999:
            cursor.execute('UPDATE users SET rang = ? WHERE user_id = ?', ('Бриллиантовый 💎', f'{mes_id}'))
        connection.commit()
        link = await create_start_link(bot,(mes_id), encode=True)
        await bot.send_message(mes_id, f"<b>Сообщение отправлено, ожидайте ответ!</b>", parse_mode=ParseMode.HTML)
        await bot.send_message(mes_id, f"👹 А теперь и ты начни получать <b>анонимные сообщения</b>!\n\nВот твоя <b>ссылка</b>:\n👉🏿 {link}\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
    elif user_sec == 0 or user_arg == '':
        link = await create_start_link(bot,(mes_id), encode=True)
        await message.answer(f"👹 А теперь и ты начни получать <b>анонимные сообщения</b>!\n\nВот твоя <b>ссылка</b>:\n👉🏿 {link}\n\n👤Недавно в боте появился профиль, чтобы воспользоваться им пропишите команду <b>/profile</b> или воспользуйтесь <b>Menu</b> в левом нижнем углу", parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
    connection.commit()
    connection1.commit()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


