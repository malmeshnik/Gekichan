from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from aiogram_i18n import I18nContext
from typing import List, Dict, Any

def get_main_menu_keyboard(i18n: I18nContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=i18n.get("menu-home")),
        types.KeyboardButton(text=i18n.get("menu-projects"))
    )
    builder.row(
        types.KeyboardButton(text=i18n.get("menu-tasks")),
        types.KeyboardButton(text=i18n.get("menu-focus"))
    )
    builder.row(
        types.KeyboardButton(text=i18n.get("menu-stats")),
        types.KeyboardButton(text=i18n.get("menu-settings"))
    )
    return builder.as_markup(resize_keyboard=True)

def get_projects_list_keyboard(projects: List[Dict[str, Any]], i18n: I18nContext, page: int = 1, page_size: int = 5):
    builder = InlineKeyboardBuilder()

    # Pagination logic
    start = (page - 1) * page_size
    end = start + page_size
    current_projects = projects[start:end]

    for p in current_projects:
        builder.row(types.InlineKeyboardButton(text=p['name'], callback_data=f"project_view_{p['id']}"))

    # Pagination buttons
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton(text="⬅️", callback_data=f"projects_list_page_{page-1}"))
    if end < len(projects):
        nav_buttons.append(types.InlineKeyboardButton(text="➡️", callback_data=f"projects_list_page_{page+1}"))

    if nav_buttons:
        builder.row(*nav_buttons)

    builder.row(
        types.InlineKeyboardButton(text=i18n.get("projects-create"), callback_data="project_create"),
        types.InlineKeyboardButton(text=i18n.get("projects-search"), callback_data="project_search")
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("projects-archive"), callback_data="projects_archive"))

    return builder.as_markup()

def get_project_dashboard_keyboard(project_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("projects-tasks-btn"), callback_data=f"project_tasks_{project_id}"),
        types.InlineKeyboardButton(text=i18n.get("projects-new-task-btn"), callback_data=f"task_create_{project_id}")
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("projects-members-btn"), callback_data=f"project_members_{project_id}"),
        types.InlineKeyboardButton(text=i18n.get("projects-analytics-btn"), callback_data=f"project_analytics_{project_id}")
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("projects-focus-btn"), callback_data=f"project_focus_{project_id}"),
        types.InlineKeyboardButton(text=i18n.get("projects-settings-btn"), callback_data=f"project_settings_{project_id}")
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data="projects_list"),
        types.InlineKeyboardButton(text=i18n.get("common-delete"), callback_data=f"project_delete_confirm_{project_id}")
    )
    return builder.as_markup()

def get_tasks_list_keyboard(project_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    # Simplified: in real app we might want to paginate or filter
    builder.row(types.InlineKeyboardButton(text=i18n.get("tasks-create"), callback_data=f"task_create_{project_id}"))
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("tasks-filter"), callback_data=f"tasks_filter_{project_id}"),
        types.InlineKeyboardButton(text=i18n.get("tasks-sort"), callback_data=f"tasks_sort_{project_id}")
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"project_view_{project_id}"))
    return builder.as_markup()

def get_task_detail_keyboard(task_id: str, project_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("tasks-start-focus"), callback_data=f"focus_start_{task_id}"),
        types.InlineKeyboardButton(text=i18n.get("tasks-complete"), callback_data=f"task_complete_{task_id}")
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("common-edit"), callback_data=f"task_edit_{task_id}"),
        types.InlineKeyboardButton(text=i18n.get("tasks-reassign"), callback_data=f"task_reassign_{task_id}")
    )
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("tasks-attachments-btn"), callback_data=f"task_attachments_{task_id}"),
        types.InlineKeyboardButton(text=i18n.get("common-delete"), callback_data=f"task_delete_confirm_{task_id}")
    )
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"project_tasks_{project_id}"))
    return builder.as_markup()

def get_confirmation_keyboard(callback_data: str, cancel_callback: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("common-confirm"), callback_data=callback_data),
        types.InlineKeyboardButton(text=i18n.get("common-cancel"), callback_data=cancel_callback)
    )
    return builder.as_markup()

def get_priority_keyboard(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text=i18n.get("priority-high"), callback_data="priority_high"),
        types.InlineKeyboardButton(text=i18n.get("priority-medium"), callback_data="priority_medium"),
        types.InlineKeyboardButton(text=i18n.get("priority-low"), callback_data="priority_low")
    )
    return builder.as_markup()
