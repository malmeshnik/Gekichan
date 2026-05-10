from aiogram import Router, types, F
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.utils.filters import I18nTextFilter

router = Router()

@router.message(I18nTextFilter("menu-settings"))
async def settings_menu(message: types.Message, i18n: I18nContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=i18n.settings.language(), callback_data="settings_lang")]
    ])
    await message.answer(i18n.menu.settings(), reply_markup=keyboard)

@router.callback_query(F.data == "settings_lang")
async def select_lang(callback: types.CallbackQuery, i18n: I18nContext):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="English", callback_data="set_lang_en")],
        [types.InlineKeyboardButton(text="Українська", callback_data="set_lang_uk")],
        [types.InlineKeyboardButton(text="Русский", callback_data="set_lang_ru")],
    ])
    await callback.message.edit_text(i18n.lang.select(), reply_markup=keyboard)

@router.callback_query(F.data.startswith("set_lang_"))
async def set_lang(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    new_lang = callback.data.split("_")[-1]
    await api_client.update_user(callback.from_user.id, language=new_lang)

    # We need to refresh the i18n context for the current request too if we want immediate change
    await i18n.set_locale(new_lang)

    await callback.answer(i18n.lang.changed())
    # Back to settings or main menu? Let's go to settings
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text=i18n.settings.language(), callback_data="settings_lang")]
    ])
    await callback.message.edit_text(i18n.menu.settings(), reply_markup=keyboard)
