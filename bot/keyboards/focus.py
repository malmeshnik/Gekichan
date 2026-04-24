from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_focus_keyboard(session_id):
    buttons = [
        [
            InlineKeyboardButton(text="⏸ Pause", callback_data=f"focus_pause_{session_id}"),
            InlineKeyboardButton(text="⏹ Stop", callback_data=f"focus_stop_{session_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_focus_resume_keyboard(session_id):
    # Backend doesn't have resume, pause just increments interruptions but keeps it active.
    # So we just show the same controls.
    return get_focus_keyboard(session_id)
