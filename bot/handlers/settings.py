from aiogram import Router, types, F
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.utils.filters import I18nTextFilter
from bot.utils.navigation import safe_edit_or_answer
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(I18nTextFilter("menu-settings"))
async def open_settings(message: types.Message, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("settings-language"), callback_data="settings_lang"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("settings-timezone"), callback_data="settings_tz"))

    await message.answer(i18n.get("menu-settings"), reply_markup=builder.as_markup())

@router.callback_query(F.data == "settings_lang")
async def select_language(callback: types.CallbackQuery, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🇺🇸 English", callback_data="set_lang_en"),
        types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data="set_lang_uk"),
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru")
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data="settings_main"))
    await safe_edit_or_answer(callback, i18n.get("lang-select"), reply_markup=builder.as_markup())

@router.callback_query(F.data == "settings_main")
async def back_to_settings(callback: types.CallbackQuery, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("settings-language"), callback_data="settings_lang"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("settings-timezone"), callback_data="settings_tz"))
    await safe_edit_or_answer(callback, i18n.get("menu-settings"), reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("set_lang_"))
async def change_language(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    new_lang = callback.data.split("_")[-1]
    # SimpleJWT uses 'ru', 'en', 'uk'. Bot uses same.
    # Fluent uses 'en', 'uk', 'ru'.
    await api_client.update_user(callback.from_user.id, language=new_lang)
    await i18n.set_locale(new_lang)
    await callback.answer(i18n.get("lang-changed"))
    # Refresh settings menu with new language
    await back_to_settings(callback, i18n)

@router.callback_query(F.data == "settings_tz")
async def settings_timezone(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)
