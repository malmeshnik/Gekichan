from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram_i18n import I18nContext

class ProjectCallback(CallbackData, prefix="proj"):
    action: str
    id: str = "0"
    page: int = 0

class TaskCallback(CallbackData, prefix="task"):
    action: str
    id: str = "0"
    project_id: str = "0"
    status: str = "all"

class KeyboardBuilder:
    @staticmethod
    def project_list(projects, page: int, total_pages: int, i18n: I18nContext):
        builder = InlineKeyboardBuilder()
        for p in projects:
            builder.button(text=p['name'], callback_data=ProjectCallback(action="view", id=str(p['id'])))

        builder.adjust(1)

        # Pagination
        nav_btns = []
        if page > 0:
            nav_btns.append(InlineKeyboardBuilder().button(text="⬅️", callback_data=ProjectCallback(action="list", page=page-1)).export()[0])
        if page < total_pages - 1:
            nav_btns.append(InlineKeyboardBuilder().button(text="➡️", callback_data=ProjectCallback(action="list", page=page+1)).export()[0])

        if nav_btns:
            builder.row(*nav_btns)

        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("projects-create"), callback_data=ProjectCallback(action="create")).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("common-search"), callback_data=ProjectCallback(action="search")).export()[0]
        )
        builder.row(InlineKeyboardBuilder().button(text=i18n.get("projects-archive"), callback_data=ProjectCallback(action="archive")).export()[0])

        return builder.as_markup()

    @staticmethod
    def project_dashboard(project_id: str, i18n: I18nContext):
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("project-btn-tasks"), callback_data=TaskCallback(action="list", project_id=project_id)).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("project-btn-new-task"), callback_data=TaskCallback(action="create", project_id=project_id)).export()[0]
        )
        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("project-btn-members"), callback_data=ProjectCallback(action="members", id=project_id)).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("project-btn-analytics"), callback_data=ProjectCallback(action="stats", id=project_id)).export()[0]
        )
        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("project-btn-focus"), callback_data=ProjectCallback(action="focus", id=project_id)).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("project-btn-settings"), callback_data=ProjectCallback(action="settings", id=project_id)).export()[0]
        )
        builder.row(InlineKeyboardBuilder().button(text=i18n.get("common-delete"), callback_data=ProjectCallback(action="delete_confirm", id=project_id)).export()[0])
        builder.row(InlineKeyboardBuilder().button(text=i18n.get("common-back"), callback_data=ProjectCallback(action="list")).export()[0])
        return builder.as_markup()

    @staticmethod
    def task_detail(task_id: str, project_id: str, i18n: I18nContext):
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("task-btn-start-focus"), callback_data=TaskCallback(action="focus", id=task_id)).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("task-btn-complete"), callback_data=TaskCallback(action="complete", id=task_id)).export()[0]
        )
        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("common-edit"), callback_data=TaskCallback(action="edit", id=task_id)).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("task-btn-reassign"), callback_data=TaskCallback(action="reassign", id=task_id)).export()[0]
        )
        builder.row(
            InlineKeyboardBuilder().button(text=i18n.get("task-btn-attachments"), callback_data=TaskCallback(action="attachments", id=task_id)).export()[0],
            InlineKeyboardBuilder().button(text=i18n.get("common-delete"), callback_data=TaskCallback(action="delete", id=task_id)).export()[0]
        )
        builder.row(InlineKeyboardBuilder().button(text=i18n.get("common-back"), callback_data=TaskCallback(action="list", project_id=project_id)).export()[0])
        return builder.as_markup()
