from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.utils.renderers import render_tasks_grouped, render_task_detail
from bot.utils.keyboards import (
    get_tasks_list_keyboard, get_task_detail_keyboard,
    get_confirmation_keyboard, get_priority_keyboard
)
from bot.states.task_states import TaskStates
from bot.utils.filters import I18nTextFilter

router = Router()

@router.message(I18nTextFilter("menu-tasks"))
async def list_all_tasks(message: types.Message, api_client: APIClient, i18n: I18nContext):
    tasks = await api_client.get_tasks(message.from_user.id)
    text = render_tasks_grouped(tasks, i18n)
    # Generic task list might not have a "Back" to a specific project
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("tasks-create"), callback_data="task_create_none"))
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("project_tasks_"))
async def list_project_tasks(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    tasks = await api_client.get_tasks(callback.from_user.id, project=project_id)
    text = render_tasks_grouped(tasks, i18n)
    await callback.message.edit_text(text, reply_markup=get_tasks_list_keyboard(project_id, i18n), parse_mode="HTML")

@router.callback_query(F.data.startswith("task_view_"))
async def view_task(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    task_id = callback.data.split("_")[-1]
    task = await api_client.get_task(callback.from_user.id, task_id)
    text = render_task_detail(task, i18n)
    await callback.message.edit_text(text, reply_markup=get_task_detail_keyboard(task_id, task['project'], i18n), parse_mode="HTML")

@router.callback_query(F.data.startswith("task_create_"))
async def start_task_creation(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await state.update_data(project_id=project_id)
    await callback.message.answer(i18n.get("tasks-enter-title"))
    await state.set_state(TaskStates.waiting_for_title)
    await callback.answer()

@router.message(TaskStates.waiting_for_title)
async def process_task_title(message: types.Message, state: FSMContext, i18n: I18nContext):
    await state.update_data(title=message.text)
    await message.answer(i18n.get("tasks-enter-priority"), reply_markup=get_priority_keyboard(i18n))
    await state.set_state(TaskStates.waiting_for_priority)

@router.callback_query(TaskStates.waiting_for_priority, F.data.startswith("priority_"))
async def process_task_priority(callback: types.CallbackQuery, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    priority = callback.data.split("_")[-1]
    data = await state.get_data()
    try:
        await api_client.create_task(
            callback.from_user.id,
            title=data['title'],
            project_id=data['project_id'] if data['project_id'] != "none" else None,
            priority=priority
        )
        await callback.message.answer(i18n.get("tasks-created"))
        await state.clear()
        # Refresh tasks
        tasks = await api_client.get_tasks(callback.from_user.id, project=data['project_id'] if data['project_id'] != "none" else None)
        text = render_tasks_grouped(tasks, i18n)
        await callback.message.answer(text, reply_markup=get_tasks_list_keyboard(data['project_id'], i18n), parse_mode="HTML")
    except Exception:
        await callback.message.answer(i18n.get("tasks-create-failed"))
    await callback.answer()

@router.callback_query(F.data.startswith("task_attachments_"))
async def list_attachments(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    task_id = callback.data.split("_")[-1]
    attachments = await api_client.get_attachments(callback.from_user.id, task_id)

    lines = [f"📎 <b>{i18n.get('tasks-attachments')}</b>\n"]
    for a in attachments:
        lines.append(f"• {a['file_name']} ({a['file_size']} bytes)")

    text = "\n".join(lines)
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("tasks-add-attachment"), callback_data=f"task_attach_start_{task_id}"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"task_view_{task_id}"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("task_attach_start_"))
async def start_attachment_upload(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    task_id = callback.data.split("_")[-1]
    await state.update_data(task_id=task_id)
    await state.set_state(TaskStates.waiting_for_attachment)
    await callback.message.answer(i18n.get("tasks-upload-instruction"))
    await callback.answer()

@router.message(TaskStates.waiting_for_attachment, F.content_type.in_({'document', 'photo', 'audio', 'voice', 'video'}))
async def process_attachment(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    data = await state.get_data()
    task_id = data['task_id']

    file_id = None
    file_name = "attachment"
    mime_type = "application/octet-stream"
    file_size = 0

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        mime_type = message.document.mime_type
        file_size = message.document.file_size
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_name = f"photo_{file_id}.jpg"
        mime_type = "image/jpeg"
        file_size = message.photo[-1].file_size
    # Handle others...

    if file_id:
        await api_client.add_attachment(message.from_user.id, task_id, file_id, file_name, mime_type, file_size)

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-finish"), callback_data=f"task_view_{task_id}"))
    await message.answer(i18n.get("tasks-attachment-added"), reply_markup=builder.as_markup())
