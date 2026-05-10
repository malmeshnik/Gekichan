from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.keyboards.main_menu import get_main_menu
from bot.services.api_client import APIClient
from aiogram_i18n import I18nContext

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, api_client: APIClient, i18n: I18nContext):
    user_id = message.from_user.id
    try:
        await api_client.authenticate(user_id)
        await message.answer(
            f"Welcome back, {message.from_user.first_name}! I'm your productivity assistant.",
            reply_markup=get_main_menu(i18n)
        )
    except Exception as e:
        await message.answer("Failed to authenticate with the backend. Please try again later.")
