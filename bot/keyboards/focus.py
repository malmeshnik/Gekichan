from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext

def get_focus_keyboard(session_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text=i18n.timer.pause(), callback_data=f"focus_pause_{session_id}"),
            InlineKeyboardButton(text=i18n.timer.stop(), callback_data=f"focus_stop_{session_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_focus_resume_keyboard(session_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text=i18n.timer.resume(), callback_data=f"focus_resume_{session_id}"),
            InlineKeyboardButton(text=i18n.timer.stop(), callback_data=f"focus_stop_{session_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_timer_options_keyboard(task_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text="25 min", callback_data=f"timer_start_{task_id}_1500"),
            InlineKeyboardButton(text="50 min", callback_data=f"timer_start_{task_id}_3000")
        ],
        [
            InlineKeyboardButton(text=i18n.timer.start() + " (Stopwatch)", callback_data=f"timer_start_{task_id}_0")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_post_timer_keyboard(task_id, i18n: I18nContext):
    buttons = [
        [InlineKeyboardButton(text=i18n.timer.task_done(), callback_data=f"task_done_{task_id}")],
        [InlineKeyboardButton(text=i18n.timer.continue_(), callback_data=f"timer_resume_{task_id}")],
        [InlineKeyboardButton(text=i18n.timer.need_more(), callback_data=f"timer_more_{task_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
