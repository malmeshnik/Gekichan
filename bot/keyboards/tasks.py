from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.callbacks import (
    TaskViewCb,
    TaskCreateCb,
    ProjectTasksCb,
    TaskDeadlineDateCb,
)

def get_tasks_keyboard(tasks, i18n):
    buttons = []
    for t in tasks:
        status_icon = "✅" if t['status'] == 'done' else "📌"
        buttons.append([InlineKeyboardButton(text=f"{status_icon} {t['title']}", callback_data=TaskViewCb(id=t['id']).pack())])

    buttons.append([InlineKeyboardButton(text=i18n.get("tasks-create"), callback_data=TaskCreateCb().pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_task_projects_keyboard(projects):
    buttons = []
    for p in projects:
        buttons.append([InlineKeyboardButton(text=p['name'], callback_data=ProjectTasksCb(project_id=p['id']).pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_task_deadline_keyboard(i18n):
    buttons = [
        [InlineKeyboardButton(text=i18n.get("common-today"), callback_data=TaskDeadlineDateCb(choice="today").pack())],
        [InlineKeyboardButton(text=i18n.get("common-tomorrow"), callback_data=TaskDeadlineDateCb(choice="tomorrow").pack())],
        [InlineKeyboardButton(text="⏭ " + i18n.get("common-skip"), callback_data=TaskDeadlineDateCb(choice="skip").pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
