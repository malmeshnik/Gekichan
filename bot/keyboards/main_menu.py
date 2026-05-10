from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_i18n import I18nContext

def get_main_menu(i18n: I18nContext):
    keyboard = [
        [KeyboardButton(text=i18n.get("nav-home")), KeyboardButton(text=i18n.get("nav-projects"))],
        [KeyboardButton(text=i18n.get("nav-tasks")), KeyboardButton(text=i18n.get("nav-focus"))],
        [KeyboardButton(text=i18n.get("nav-stats")), KeyboardButton(text=i18n.get("common-settings"))]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
