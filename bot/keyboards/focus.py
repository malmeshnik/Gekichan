from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from bot.utils.callbacks import (
    FocusActionCb,
    TimerStartCb,
    FocusPostTimerCb,
    TimerAddCb,
    TaskViewCb,
)

def get_focus_keyboard(session_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text=i18n.get("timer-pause"), callback_data=FocusActionCb(action="p", id=session_id).pack()),
            InlineKeyboardButton(text=i18n.get("timer-stop"), callback_data=FocusActionCb(action="s", id=session_id).pack())
        ],
        [
            InlineKeyboardButton(text=i18n.get("timer-refresh"), callback_data=FocusActionCb(action="ref", id=session_id).pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_focus_resume_keyboard(session_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text=i18n.get("timer-resume"), callback_data=FocusActionCb(action="r", id=session_id).pack()),
            InlineKeyboardButton(text=i18n.get("timer-stop"), callback_data=FocusActionCb(action="s", id=session_id).pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_timer_options_keyboard(task_id, i18n: I18nContext):
    buttons = [
        [
            InlineKeyboardButton(text="25 min", callback_data=TimerStartCb(task_id=task_id, duration=1500).pack()),
            InlineKeyboardButton(text="50 min", callback_data=TimerStartCb(task_id=task_id, duration=3000).pack())
        ],
        [
            InlineKeyboardButton(text=i18n.get("timer-start") + " (Stopwatch)", callback_data=TimerStartCb(task_id=task_id, duration=0).pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_post_timer_keyboard(task_id, i18n: I18nContext, session_id: str = None):
    buttons = [
        [InlineKeyboardButton(text=i18n.get("timer-task-done"), callback_data=FocusPostTimerCb(action="d", id=task_id).pack())],
        [InlineKeyboardButton(text=i18n.get("timer-continue"), callback_data=FocusPostTimerCb(action="c", id=task_id).pack())],
        [InlineKeyboardButton(text=i18n.get("timer-take-break"), callback_data=FocusActionCb(action="b").pack())],
        [InlineKeyboardButton(text=i18n.get("timer-need-more"), callback_data=FocusPostTimerCb(action="m", id=task_id).pack())],
        [InlineKeyboardButton(text=i18n.get("timer-back-to-task"), callback_data=TaskViewCb(id=task_id).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_add_time_keyboard(task_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="+5m", callback_data=TimerAddCb(task_id=task_id, seconds="300").pack()),
        types.InlineKeyboardButton(text="+15m", callback_data=TimerAddCb(task_id=task_id, seconds="900").pack()),
        types.InlineKeyboardButton(text="+30m", callback_data=TimerAddCb(task_id=task_id, seconds="1800").pack())
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-custom"), callback_data=TimerAddCb(task_id=task_id, seconds="custom").pack()))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=TaskViewCb(id=task_id).pack()))
    return builder.as_markup()
