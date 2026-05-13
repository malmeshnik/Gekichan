from math import ceil
from typing import List, Dict, Any

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from aiogram_i18n import I18nContext


def get_main_menu_keyboard(i18n: I18nContext):
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text=i18n.get("menu-home")),
        types.KeyboardButton(text=i18n.get("menu-projects")),
    )
    builder.row(
        types.KeyboardButton(text=i18n.get("menu-tasks")),
        types.KeyboardButton(text=i18n.get("menu-focus")),
    )
    builder.row(
        types.KeyboardButton(text=i18n.get("menu-stats")),
        types.KeyboardButton(text=i18n.get("menu-settings")),
    )
    return builder.as_markup(resize_keyboard=True)


def get_projects_list_keyboard(
    projects: List[Dict[str, Any]], i18n: I18nContext, page: int = 1, page_size: int = 5
):
    builder = InlineKeyboardBuilder()
    start = (page - 1) * page_size
    end = start + page_size
    current_projects = projects[start:end]
    for p in current_projects:
        builder.row(
            types.InlineKeyboardButton(
                text=p["name"], callback_data=f"project_view_{p['id']}"
            )
        )
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️", callback_data=f"projects_list_page_{page-1}"
            )
        )
    if end < len(projects):
        nav_buttons.append(
            types.InlineKeyboardButton(
                text="➡️", callback_data=f"projects_list_page_{page+1}"
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("projects-create"), callback_data="project_create"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("projects-search"), callback_data="project_search"
        ),
    )
    return builder.as_markup()


def get_project_dashboard_keyboard(project_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("projects-tasks-btn"),
            callback_data=f"project_tasks_{project_id}",
        ),
        types.InlineKeyboardButton(
            text=i18n.get("projects-new-task-btn"),
            callback_data=f"task_create_{project_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("projects-members-btn"),
            callback_data=f"project_members_{project_id}",
        ),
        types.InlineKeyboardButton(
            text=i18n.get("projects-analytics-btn"),
            callback_data=f"project_analytics:{project_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data="projects_list"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-delete"),
            callback_data=f"project_delete_confirm_{project_id}",
        ),
    )
    return builder.as_markup()


def get_tasks_list_keyboard(
    project_id: str,
    i18n: I18nContext,
    tasks: list = None,
    page: int = 1,
    per_page: int = 5,
):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-create"), callback_data=f"task_create_{project_id}"
        )
    )

    tasks = tasks or []

    total_tasks = len(tasks)
    total_pages = max(1, ceil(total_tasks / per_page))

    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page

    current_tasks = tasks[start:end]

    # Список задач
    for task in current_tasks:
        builder.row(
            types.InlineKeyboardButton(
                text=task["title"], callback_data=f"task_view_{task['id']}"
            )
        )

    pagination_buttons = []

    if page > 1:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️", callback_data=f"tasks_page_{project_id}_{page - 1}"
            )
        )

    pagination_buttons.append(
        types.InlineKeyboardButton(text=f"{page}/{total_pages}", callback_data="ignore")
    )

    if page < total_pages:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="➡️", callback_data=f"tasks_page_{project_id}_{page + 1}"
            )
        )

    builder.row(*pagination_buttons)

    # Назад
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=f"project_view_{project_id}"
        )
    )

    return builder.as_markup()


def get_task_detail_keyboard(task_id: str, project_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-start-focus"), callback_data=f"focus_start_{task_id}"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-complete"), callback_data=f"task_complete_{task_id}"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-edit"), callback_data=f"task_edit_{task_id}"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-attachments-btn"),
            callback_data=f"task_attachments_{task_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=f"project_tasks_{project_id}"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-delete"),
            callback_data=f"task_delete_confirm_{task_id}",
        ),
    )
    return builder.as_markup()


def get_confirmation_keyboard(
    callback_data: str, cancel_callback: str, i18n: I18nContext
):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-confirm"), callback_data=callback_data
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-cancel"), callback_data=cancel_callback
        ),
    )
    return builder.as_markup()


def get_priority_keyboard(i18n: I18nContext, prefix: str = "priority"):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("priority-high"), callback_data=f"{prefix}_high"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("priority-medium"), callback_data=f"{prefix}_medium"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("priority-low"), callback_data=f"{prefix}_low"
        ),
    )
    return builder.as_markup()


def get_deadline_date_keyboard(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-today"), callback_data="date_today"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-tomorrow"), callback_data="date_tomorrow"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-weekend"), callback_data="date_weekend"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-next-week"), callback_data="date_nextweek"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-custom"), callback_data="date_custom"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"), callback_data="date_skip"
        )
    )
    return builder.as_markup()


def get_deadline_time_keyboard(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="+1h", callback_data="time_plus1"),
        types.InlineKeyboardButton(text="+2h", callback_data="time_plus2"),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-morning"), callback_data="time_morning"
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-evening"), callback_data="time_evening"
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-custom"), callback_data="time_custom"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"), callback_data="time_skip"
        )
    )
    return builder.as_markup()


def get_assignee_keyboard(members: List[Dict[str, Any]], i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    for m in members:
        user = m["user_detail"]
        builder.row(
            types.InlineKeyboardButton(
                text=user["first_name"], callback_data=f"assignee_{user['id']}"
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"), callback_data="assignee_skip"
        )
    )
    return builder.as_markup()
