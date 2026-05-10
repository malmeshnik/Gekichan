from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.services.ui_renderer import UIRenderer
from bot.keyboards.builders import KeyboardBuilder, TaskCallback, ProjectCallback
from bot.states.task_states import TaskStates

router = Router()

@router.message(F.text.in_(["📝 Tasks", "📝 Завдання", "📝 Задачи"]))
@router.callback_query(TaskCallback.filter(F.action == "list"))
async def list_tasks(event: types.Message | types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: TaskCallback = None):
    user_id = event.from_user.id
    project_id = callback_data.project_id if callback_data else None

    tasks = await api_client.get_tasks(user_id, project_id=project_id)

    # Group tasks
    grouped = {
        "overdue": [t for t in tasks if t.get('is_overdue')],
        "in_progress": [t for t in tasks if t.get('status') == 'in_progress' and not t.get('is_overdue')],
        "todo": [t for t in tasks if t.get('status') == 'todo' and not t.get('is_overdue')],
        "done": [t for t in tasks if t.get('status') == 'done']
    }

    text = ""
    if project_id:
        text += f"<b>📁 Projects > Task List</b>\n\n" # Placeholder breadcrumb
    else:
        text += f"<b>📝 {i18n.get('nav-tasks')}</b>\n\n"

    for key, group_tasks in grouped.items():
        if group_tasks:
            text += f"<b>{i18n.get(f'tasks-grouped-{key.replace(\'_\', \'-\')}')}</b>\n"
            for t in group_tasks[:5]: # Show first 5 per group
                text += f"• {t['title']} (/{t['id']})\n"
            text += "\n"

    if not tasks:
        text += i18n.get("tasks-empty")

    # In a real app, we'd use a more sophisticated keyboard with pagination and filters
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    for t in tasks[:10]: # Quick access buttons
        builder.button(text=t['title'], callback_data=TaskCallback(action="view", id=str(t['id']), project_id=project_id or "0"))
    builder.adjust(1)

    if project_id:
        builder.row(InlineKeyboardBuilder().button(text=i18n.get("common-back"), callback_data=ProjectCallback(action="view", id=project_id)).export()[0])

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")
    else:
        await event.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(TaskCallback.filter(F.action == "view"))
async def view_task(callback: types.CallbackQuery, callback_data: TaskCallback, api_client: APIClient, i18n: I18nContext):
    task_id = callback_data.id
    user_id = callback.from_user.id

    # Fetch all tasks and find the one we need (again, for MVP/simplicity without changing backend)
    tasks = await api_client.get_tasks(user_id)
    task = next((t for t in tasks if str(t['id']) == task_id), None)

    if not task:
        await callback.answer(i18n.get("task-not-found"))
        return

    text = UIRenderer.render_task_card(task, i18n)
    project_id = str(task['project'])
    await callback.message.edit_text(text, reply_markup=KeyboardBuilder.task_detail(task_id, project_id, i18n), parse_mode="HTML")

@router.callback_query(TaskCallback.filter(F.action == "attachments"))
async def list_task_attachments(callback: types.CallbackQuery, callback_data: TaskCallback, api_client: APIClient, i18n: I18nContext):
    task_id = callback_data.id
    user_id = callback.from_user.id

    attachments = await api_client.get_attachments(user_id, task_id)

    text = f"<b>{i18n.get('task-btn-attachments')}</b>\n\n"
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()

    if not attachments:
        text += "No attachments yet. Send a file to add one."
    else:
        for a in attachments:
            text += f"• {a['file_name'] or 'Attachment'}\n"
            builder.button(text=f"📄 {a['file_name'] or 'File'}", callback_data=f"file_view_{a['telegram_file_id']}")

    builder.adjust(1)
    builder.row(InlineKeyboardBuilder().button(text=i18n.get("common-back"), callback_data=TaskCallback(action="view", id=task_id)).export()[0])

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
