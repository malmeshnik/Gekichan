from aiogram import types
from aiogram.exceptions import TelegramBadRequest
import logging

logger = logging.getLogger(__name__)

async def safe_edit_or_answer(event: types.Message | types.CallbackQuery, text: str, reply_markup: types.InlineKeyboardMarkup | types.ReplyKeyboardMarkup = None, parse_mode: str = "HTML"):
    """
    Safely edits a message if it's a callback query, or answers/sends a new message.
    Handles 'message is not modified' and other common Telegram errors.
    """
    if isinstance(event, types.CallbackQuery):
        try:
            await event.message.edit_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
        except TelegramBadRequest as e:
            if "message is not modified" in str(e).lower():
                await event.answer()
            else:
                logger.warning(f"Failed to edit message: {e}")
                await event.message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)
        except Exception as e:
            logger.error(f"Error in safe_edit_or_answer (edit): {e}")
            await event.message.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)
    else:
        await event.answer(text, reply_markup=reply_markup, parse_mode=parse_mode)
