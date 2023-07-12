from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardRemove
from configs import TOKEN, get_key
from googletrans import Translator
from keyboard import generate_lang
import sqlite3


bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'about', 'history'])
def command_start(message: Message):
    chat_id = message.chat.id
    user_info = message.from_user.first_name
    if message.text == '/start':
        msg = f'Здравствуйте {user_info} вас приветствует бот переводчик'
        bot.send_message(chat_id, msg)
    elif message.text == '/help':
        msg = f'Здравствуйте {user_info} нужна помощь обратитесь к разработчику @duuuuke'
        bot.send_message(chat_id, msg)
    elif message.text == '/about':
        msg = f'Здравствуйте {user_info} данный бот может переводить с любого языка на русский, и так же с русского'
        bot.send_message(chat_id, msg)
    elif message.text == '/history':
        get_history(message)
    start_questions(message)


def get_history(message: Message):
    chat_id = message.chat.id
    database = sqlite3.connect('translation.db')
    cursor = database.cursor()
    cursor.execute('''
        SELECT src, dest, original, translated FROM history
        WHERE telegram_id = ?
    ''', (chat_id, ))
    history = cursor.fetchall()
    history = history[::-1]
    for src, dest, original, translated in history[:5]:
        bot.send_message(chat_id, f'''Вы переводили
С языка: {src}
На язык: {dest}
Ваш текст: {original}
Бот перевёл: {translated}''')

    database.close()


def start_questions(message: Message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'С какого языка перевести', reply_markup=generate_lang())
    bot.register_next_step_handler(msg, confirm_src_ask_dest)


def confirm_src_ask_dest(message: Message):
    chat_id = message.chat.id
    text_src = message.text
    if text_src == '/start' or text_src == '/help' or text_src == '/about' or text_src == '/history':
        command_start(message)
    else:
        msg = bot.send_message(chat_id, 'На какой язык вам перевести', reply_markup=generate_lang())
        bot.register_next_step_handler(msg, ask_leng, text_src)


def ask_leng(message, text_src):
    chat_id = message.chat.id
    text_dest = message.text
    if text_dest == '/start' or text_dest == '/help' or text_dest == '/about' or text_dest == '/history':
        command_start(message)
    else:
        msg = bot.send_message(chat_id, 'Введите текст для перевода', reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, text_translate, text_src, text_dest)


def text_translate(message, text_src, text_dest):
    chat_id = message.chat.id
    text = message.text
    if text == '/start' or text == '/help' or text == '/about' or text == '/history':
        command_start(message)
    else:
        teacher = Translator()
        msg = teacher.translate(text=text, src=get_key(text_src), dest=get_key(text_dest)).text

        database = sqlite3.connect('translation.db')
        cursor = database.cursor()
        cursor.execute('''
            INSERT INTO history(telegram_id, src, dest, original, translated)
            VALUES(?, ?, ?, ?, ?)
        ''', (chat_id, text_src, text_dest, text, msg))

        database.commit()
        database.close()

        bot.send_message(chat_id, msg)
        command_start(message)


bot.polling(none_stop=True)