from math import ceil
from typing import List, Dict, Any

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from aiogram_i18n import I18nContext

from bot.utils.callbacks import (
    ProjectListCb,
    ProjectViewCb,
    ProjectActionCb,
    TaskViewCb,
    TaskCreateCb,
    ProjectTasksCb,
    ProjectMembersCb,
    AnalyticsPeriodCb,
    CommonBackCb,
    CommonIgnoreCb,
    FocusStartCb,
    TaskActionCb,
    TaskAttachmentCb,
    TaskPriorityCb,
    TaskDeadlineDateCb,
    TaskDeadlineTimeCb,
    TaskAssigneeCb,
    TasksHubCb,
)


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
                text=p["name"], callback_data=ProjectViewCb(id=p["id"]).pack()
            )
        )
    nav_buttons = []
    if page > 1:
        nav_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️", callback_data=ProjectListCb(page=page - 1).pack()
            )
        )
    if end < len(projects):
        nav_buttons.append(
            types.InlineKeyboardButton(
                text="➡️", callback_data=ProjectListCb(page=page + 1).pack()
            )
        )
    if nav_buttons:
        builder.row(*nav_buttons)
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("projects-create"),
            callback_data=ProjectActionCb(action="c").pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("projects-search"),
            callback_data=ProjectActionCb(action="s").pack(),
        ),
    )
    return builder.as_markup()


def get_project_dashboard_keyboard(project_id: str, i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("projects-tasks-btn"),
            callback_data=ProjectTasksCb(project_id=project_id).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("projects-new-task-btn"),
            callback_data=TaskCreateCb(project_id=project_id).pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("projects-members-btn"),
            callback_data=ProjectMembersCb(project_id=project_id).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("projects-analytics-btn"),
            callback_data=AnalyticsPeriodCb(period="day", project_id=project_id).pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"),
            callback_data=ProjectListCb(page=1).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-delete"),
            callback_data=ProjectActionCb(
                action="dc", id=project_id
            ).pack(),
        ),
    )
    return builder.as_markup()


def get_tasks_list_keyboard(
    project_id: str,
    i18n: I18nContext,
    tasks: list = None,
    page: int = 1,
    per_page: int = 5,
    back_callback: str = None,
    show_create: bool = True,
):
    builder = InlineKeyboardBuilder()

    if show_create:
        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("tasks-create"),
                callback_data=TaskCreateCb(project_id=project_id).pack(),
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
        task_id = task["id"]
        builder.row(
            types.InlineKeyboardButton(
                text=task["title"], callback_data=TaskViewCb(id=task_id).pack()
            )
        )

    pagination_buttons = []

    if page > 1:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="⬅️",
                callback_data=ProjectTasksCb(
                    project_id=project_id or "null", page=page - 1
                ).pack(),
            )
        )

    pagination_buttons.append(
        types.InlineKeyboardButton(
            text=f"{page}/{total_pages}", callback_data=CommonIgnoreCb().pack()
        )
    )

    if page < total_pages:
        pagination_buttons.append(
            types.InlineKeyboardButton(
                text="➡️",
                callback_data=ProjectTasksCb(
                    project_id=project_id or "null", page=page + 1
                ).pack(),
            )
        )

    builder.row(*pagination_buttons)

    # Назад
    if back_callback:
        if back_callback == "tasks_hub":
            back_data = TasksHubCb().pack()
        else:
            back_data = back_callback
    else:
        back_data = ProjectViewCb(id=project_id).pack()

    builder.row(
        types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=back_data)
    )

    return builder.as_markup()


def get_task_detail_keyboard(
    task_id: str, project_id: str, i18n: I18nContext, back_callback: str = None
):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-start-focus"),
            callback_data=FocusStartCb(task_id=task_id).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-complete"),
            callback_data=TaskActionCb(action="c", id=task_id).pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-edit"),
            callback_data=TaskActionCb(action="e", id=task_id).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-attachments-btn"),
            callback_data=TaskAttachmentCb(action="l", id=task_id).pack(),
        ),
    )

    if back_callback:
        if back_callback == "tasks_hub":
            back_data = TasksHubCb().pack()
        else:
            back_data = back_callback
    else:
        back_data = ProjectTasksCb(project_id=project_id or "null").pack()

    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=back_data
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-delete"),
            callback_data=TaskActionCb(action="dc", id=task_id).pack(),
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
    is_edit = prefix == "editprio"
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("priority-high"),
            callback_data=TaskPriorityCb(priority="high", is_edit=is_edit).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("priority-medium"),
            callback_data=TaskPriorityCb(priority="medium", is_edit=is_edit).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("priority-low"),
            callback_data=TaskPriorityCb(priority="low", is_edit=is_edit).pack(),
        ),
    )
    return builder.as_markup()


def get_deadline_date_keyboard(i18n: I18nContext, is_edit: bool = False):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-today"),
            callback_data=TaskDeadlineDateCb(choice="today", is_edit=is_edit).pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-tomorrow"),
            callback_data=TaskDeadlineDateCb(choice="tomorrow", is_edit=is_edit).pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-weekend"),
            callback_data=TaskDeadlineDateCb(choice="weekend", is_edit=is_edit).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-next-week"),
            callback_data=TaskDeadlineDateCb(choice="nextweek", is_edit=is_edit).pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-custom"),
            callback_data=TaskDeadlineDateCb(choice="custom", is_edit=is_edit).pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"),
            callback_data=TaskDeadlineDateCb(choice="skip", is_edit=is_edit).pack(),
        )
    )
    return builder.as_markup()


def get_deadline_time_keyboard(i18n: I18nContext, is_edit: bool = False):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="+1h",
            callback_data=TaskDeadlineTimeCb(choice="plus1", is_edit=is_edit).pack(),
        ),
        types.InlineKeyboardButton(
            text="+2h",
            callback_data=TaskDeadlineTimeCb(choice="plus2", is_edit=is_edit).pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-morning"),
            callback_data=TaskDeadlineTimeCb(choice="morning", is_edit=is_edit).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("common-evening"),
            callback_data=TaskDeadlineTimeCb(choice="evening", is_edit=is_edit).pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-custom"),
            callback_data=TaskDeadlineTimeCb(choice="custom", is_edit=is_edit).pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"),
            callback_data=TaskDeadlineTimeCb(choice="skip", is_edit=is_edit).pack(),
        )
    )
    return builder.as_markup()


def get_assignee_keyboard(
    members: List[Dict[str, Any]], i18n: I18nContext, is_edit: bool = False
):
    builder = InlineKeyboardBuilder()
    for m in members:
        user = m["user_detail"]
        builder.row(
            types.InlineKeyboardButton(
                text=user["first_name"],
                callback_data=TaskAssigneeCb(id=str(user["id"]), is_edit=is_edit).pack(),
            )
        )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"),
            callback_data=TaskAssigneeCb(id="skip", is_edit=is_edit).pack(),
        )
    )
    return builder.as_markup()


def get_tasks_hub_keyboard(i18n: I18nContext):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-my"),
            callback_data=TasksHubCb(section="my").pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-no-project"),
            callback_data=TasksHubCb(section="no-project").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-today"),
            callback_data=TasksHubCb(section="today").pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-tomorrow"),
            callback_data=TasksHubCb(section="tomorrow").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-week"),
            callback_data=TasksHubCb(section="week").pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-overdue"),
            callback_data=TasksHubCb(section="overdue").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-by-projects"),
            callback_data=TasksHubCb(section="by-projects").pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("tasks-hub-completed"),
            callback_data=TasksHubCb(section="completed").pack(),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-create"),
            callback_data=TaskCreateCb(project_id="none").pack(),
        )
    )
    return builder.as_markup()


def get_analytics_period_keyboard(i18n: I18nContext, project_id: str = None):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("analytics-period-day"),
            callback_data=AnalyticsPeriodCb(period="day", project_id=project_id).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("analytics-period-week"),
            callback_data=AnalyticsPeriodCb(period="week", project_id=project_id).pack(),
        ),
        types.InlineKeyboardButton(
            text=i18n.get("analytics-period-month"),
            callback_data=AnalyticsPeriodCb(period="month", project_id=project_id).pack(),
        ),
    )
    if project_id:
        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("common-back"),
                callback_data=ProjectViewCb(id=project_id).pack(),
            )
        )
    return builder.as_markup()
