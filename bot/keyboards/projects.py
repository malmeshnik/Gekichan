from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_projects_keyboard(projects):
    buttons = []
    for p in projects:
        buttons.append([InlineKeyboardButton(text=p['name'], callback_data=f"project_view_{p['id']}")])

    buttons.append([InlineKeyboardButton(text="➕ Create project", callback_data="project_create")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_project_detail_keyboard(project_id):
    buttons = [
        [InlineKeyboardButton(text="🗑 Delete project", callback_data=f"project_delete_{project_id}")],
        [InlineKeyboardButton(text="⬅️ Back", callback_data="projects_list")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
