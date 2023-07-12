from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES


def generate_lang():
    markup = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    buttons = []

    for lang in LANGUAGES.values():
        btn = KeyboardButton(text=lang)
        buttons.append(btn)
    markup.add(*buttons)
    return markup






