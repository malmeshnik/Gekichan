from aiogram import Router, types, F
from aiogram_i18n import I18nContext
from aiogram.fsm.context import FSMContext

from bot.services.api_client import APIClient
from bot.utils.filters import I18nTextFilter
from bot.utils.navigation import safe_edit_or_answer
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.callbacks import SettingsCb, SetLangCb

router = Router()

@router.message(I18nTextFilter("menu-settings"))
@router.callback_query(SettingsCb.filter(F.action == "main"))
async def open_settings(event: types.Message | types.CallbackQuery, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("settings-language"), callback_data=SettingsCb(action="lang").pack()))
    builder.row(types.InlineKeyboardButton(text=i18n.get("settings-timezone"), callback_data=SettingsCb(action="tz").pack()))

    if isinstance(event, types.Message):
        await event.answer(i18n.get("menu-settings"), reply_markup=builder.as_markup())
    else:
        await safe_edit_or_answer(event, i18n.get("menu-settings"), reply_markup=builder.as_markup())

@router.callback_query(SettingsCb.filter(F.action == "lang"))
async def select_language(callback: types.CallbackQuery, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="🇺🇸 English", callback_data=SetLangCb(lang="en").pack()),
        types.InlineKeyboardButton(text="🇺🇦 Українська", callback_data=SetLangCb(lang="uk").pack()),
        types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data=SetLangCb(lang="ru").pack())
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=SettingsCb(action="main").pack()))
    await safe_edit_or_answer(callback, i18n.get("lang-select"), reply_markup=builder.as_markup())

@router.callback_query(SetLangCb.filter())
async def change_language(callback: types.CallbackQuery, state: FSMContext, api_client: APIClient, i18n: I18nContext, callback_data: SetLangCb):
    new_lang = callback_data.lang
    await api_client.update_user(callback.from_user.id, language=new_lang)
    await i18n.set_locale(new_lang)
    await callback.answer(i18n.get("lang-changed"))

    # Reset FSM state
    await state.clear()

    # Fully regenerate main menu
    from bot.utils.keyboards import get_main_menu_keyboard
    await callback.message.answer(i18n.get("lang-changed"), reply_markup=get_main_menu_keyboard(i18n))

    # Back to settings
    await open_settings(callback, i18n)

@router.callback_query(SettingsCb.filter(F.action == "tz"))
async def settings_timezone(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)
