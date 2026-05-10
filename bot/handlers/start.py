from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram_i18n import I18nContext
from bot.keyboards.main_menu import get_main_menu
from bot.services.api_client import APIClient

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, api_client: APIClient, i18n: I18nContext):
    user_id = message.from_user.id
    try:
        # Pass all user info for registration/update
        await api_client.authenticate(
            telegram_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code
        )
        await message.answer(
            i18n.get("start-welcome", name=message.from_user.first_name),
            reply_markup=get_main_menu(i18n)
        )
    except Exception as e:
        await message.answer("Failed to authenticate with the backend. Please try again later.")
