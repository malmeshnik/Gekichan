from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_tasks_keyboard(tasks):
    buttons = []
    for t in tasks:
        status_icon = "✅" if t['status'] == 'done' else "🕒"
        buttons.append([InlineKeyboardButton(text=f"{status_icon} {t['title']}", callback_data=f"task_view_{t['id']}")])

    buttons.append([InlineKeyboardButton(text="➕ Create task", callback_data="task_create")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_task_detail_keyboard(task_id, current_status):
    buttons = []
    if current_status != 'done':
        buttons.append([InlineKeyboardButton(text="✅ Mark Done", callback_data=f"task_status_{task_id}_done")])
    if current_status != 'in_progress':
        buttons.append([InlineKeyboardButton(text="🕒 Set In Progress", callback_data=f"task_status_{task_id}_in_progress")])
    if current_status != 'todo':
        buttons.append([InlineKeyboardButton(text="📝 Set To Do", callback_data=f"task_status_{task_id}_todo")])

    buttons.append([InlineKeyboardButton(text="⏱ Start Focus", callback_data=f"focus_start_{task_id}")])
    buttons.append([InlineKeyboardButton(text="⬅️ Back", callback_data="tasks_list")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_project_select_keyboard(projects):
    buttons = []
    for p in projects:
        buttons.append([InlineKeyboardButton(text=p['name'], callback_data=f"task_project_{p['id']}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_deadline_keyboard():
    buttons = [
        [InlineKeyboardButton(text="⏭ Skip", callback_data="task_deadline_skip")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
