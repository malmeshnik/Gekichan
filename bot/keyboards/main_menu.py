from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram_i18n import I18nContext

def get_main_menu(i18n: I18nContext):
    keyboard = [
        [
            KeyboardButton(text="📝"), # Use stable emojis for routing or handle text flexible
            KeyboardButton(text="📁")
        ],
        [
            KeyboardButton(text="📊"),
            KeyboardButton(text="⚙️")
        ]
    ]
    # Actually, aiogram-i18n can handle localized text if we use it correctly in routers.
    # But for MVP, let's keep it simple.
    # A better way is to use a custom filter that checks the localized string.

    keyboard = [
        [
            KeyboardButton(text=i18n.menu.tasks()),
            KeyboardButton(text=i18n.menu.projects())
        ],
        [
            KeyboardButton(text=i18n.menu.stats()),
            KeyboardButton(text=i18n.menu.settings())
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
