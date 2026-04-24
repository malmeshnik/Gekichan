from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu():
    keyboard = [
        [KeyboardButton(text="Dashboard"), KeyboardButton(text="Projects")],
        [KeyboardButton(text="Tasks"), KeyboardButton(text="Start Focus")],
        [KeyboardButton(text="Stats")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
