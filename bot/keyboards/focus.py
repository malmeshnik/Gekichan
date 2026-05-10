from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def get_focus_keyboard(session_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text=i18n.get("timer-pause"), callback_data=f"focus_pause_{session_id}"),
            InlineKeyboardButton(text=i18n.get("timer-stop"), callback_data=f"focus_stop_{session_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_focus_resume_keyboard(session_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text=i18n.get("timer-resume"), callback_data=f"focus_resume_{session_id}"),
            InlineKeyboardButton(text=i18n.get("timer-stop"), callback_data=f"focus_stop_{session_id}")
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
            InlineKeyboardButton(text=i18n.get("timer-start") + " (Stopwatch)", callback_data=f"timer_start_{task_id}_0")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_post_timer_keyboard(task_id, i18n: I18nContext, session_id: str = None):
    buttons = [
        [InlineKeyboardButton(text=i18n.get("timer-task-done"), callback_data=f"task_done_{task_id}_{session_id}")],
        [InlineKeyboardButton(text=i18n.get("timer-continue"), callback_data=f"timer_resume_{task_id}_{session_id}")],
        [InlineKeyboardButton(text=i18n.get("timer-take-break"), callback_data="focus_break")],
        [InlineKeyboardButton(text=i18n.get("timer-need-more"), callback_data=f"timer_more_{task_id}")],
        [InlineKeyboardButton(text=i18n.get("timer-back-to-task"), callback_data=f"task_view_{task_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_add_time_keyboard(task_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="+5m", callback_data=f"timer_add_{task_id}_300"),
        types.InlineKeyboardButton(text="+15m", callback_data=f"timer_add_{task_id}_900"),
        types.InlineKeyboardButton(text="+30m", callback_data=f"timer_add_{task_id}_1800")
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-custom"), callback_data=f"timer_add_{task_id}_custom"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"task_view_{task_id}"))
    return builder.as_markup()
