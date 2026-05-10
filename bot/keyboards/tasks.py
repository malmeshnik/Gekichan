from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_i18n import I18nContext

def get_tasks_keyboard(tasks, i18n: I18nContext):
    buttons = []
    for t in tasks:
        status_icon = "✅" if t['status'] == 'done' else "🕒"
        buttons.append([InlineKeyboardButton(text=f"{status_icon} {t['title']}", callback_data=f"task_view_{t['id']}")])

    buttons.append([InlineKeyboardButton(text=i18n.get("tasks-create"), callback_data="task_create")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_task_detail_keyboard(task_id, current_status, i18n: I18nContext):
    buttons = []
    if current_status != 'done':
        buttons.append([InlineKeyboardButton(text="✅ " + i18n.get("tasks-status-done"), callback_data=f"task_status_{task_id}_done")])
    if current_status != 'in_progress':
        buttons.append([InlineKeyboardButton(text="🕒 " + i18n.get("tasks-status-in-progress"), callback_data=f"task_status_{task_id}_in_progress")])
    if current_status != 'todo':
        buttons.append([InlineKeyboardButton(text="📝 " + i18n.get("tasks-status-todo"), callback_data=f"task_status_{task_id}_todo")])

    buttons.append([InlineKeyboardButton(text="⏱ " + i18n.get("menu-start-focus"), callback_data=f"focus_start_{task_id}")])
    buttons.append([InlineKeyboardButton(text="⬅️ " + i18n.get("common-back"), callback_data="tasks_list")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_project_select_keyboard(projects):
    buttons = []
    for p in projects:
        buttons.append([InlineKeyboardButton(text=p['name'], callback_data=f"task_project_{p['id']}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_deadline_keyboard(i18n: I18nContext):
    buttons = [
        [InlineKeyboardButton(text="⏭ " + i18n.get("common-skip"), callback_data="task_deadline_skip")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
