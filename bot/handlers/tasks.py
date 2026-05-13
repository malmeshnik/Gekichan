from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.utils.renderers import render_tasks_grouped, render_task_detail
from bot.utils.keyboards import (
    get_tasks_list_keyboard,
    get_task_detail_keyboard,
    get_confirmation_keyboard,
    get_priority_keyboard,
    get_deadline_date_keyboard,
    get_deadline_time_keyboard,
    get_assignee_keyboard,
)
from bot.states.task_states import TaskStates
from bot.utils.filters import I18nTextFilter
from bot.utils.navigation import safe_edit_or_answer
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime

router = Router()


@router.message(I18nTextFilter("menu-tasks"))
async def list_all_tasks(
    message: types.Message, api_client: APIClient, i18n: I18nContext
):
    tasks = await api_client.get_tasks(message.from_user.id)
    text = render_tasks_grouped(tasks, i18n)

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-create"), callback_data="task_create_none"
        )
    )
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(F.data.startswith("project_tasks_"))
async def list_project_tasks(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    project_id = callback.data.split("_")[-1]
    tasks = await api_client.get_tasks(callback.from_user.id, project=project_id)
    text = render_tasks_grouped(tasks, i18n)
    await safe_edit_or_answer(
        callback, text, reply_markup=get_tasks_list_keyboard(project_id, i18n, tasks)
    )


@router.callback_query(F.data.startswith("tasks_page_"))
async def tasks_page_handler(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    _, _, project_id, page = callback.data.split("_")

    page = int(page)

    tasks = await api_client.get_tasks(callback.from_user.id, project=project_id)

    await callback.message.edit_reply_markup(
        reply_markup=get_tasks_list_keyboard(
            project_id=project_id, i18n=i18n, tasks=tasks, page=page
        )
    )

    await callback.answer()


@router.callback_query(F.data.startswith("task_view_"))
async def view_task(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    task_id = callback.data.split("_")[-1]
    task = await api_client.get_task(callback.from_user.id, task_id)

    if "project" in task and task["project"]:
        project = await api_client.get_project(callback.from_user.id, task["project"])
        task["project_name"] = project["name"]

    text = render_task_detail(task, i18n)
    await safe_edit_or_answer(
        callback,
        text,
        reply_markup=get_task_detail_keyboard(task_id, task["project"], i18n),
    )


# --- HELPERS ---


async def go_to_assignee_selection(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    data = await state.get_data()
    project = await api_client.get_project(message.chat.id, data["project_id"])
    members = project.get("members", [])
    await message.answer(
        i18n.get("tasks-select-assignee"),
        reply_markup=get_assignee_keyboard(members, i18n),
    )
    await state.set_state(TaskStates.waiting_for_assignee)


async def view_task_internal(
    message: types.Message, task_id: str, api_client: APIClient, i18n: I18nContext
):
    task = await api_client.get_task(message.from_user.id, task_id)
    if "project" in task and task["project"]:
        project = await api_client.get_project(message.from_user.id, task["project"])
        task["project_name"] = project["name"]
    text = render_task_detail(task, i18n)
    await message.answer(
        text,
        reply_markup=get_task_detail_keyboard(task_id, task["project"], i18n),
        parse_mode="HTML",
    )


# --- CREATE TASK FLOW ---


@router.callback_query(F.data.startswith("task_create_"))
async def start_task_creation(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    project_id = callback.data.split("_")[-1]
    if project_id == "none":
        projects = await api_client.get_projects(callback.from_user.id)
        if not projects:
            await callback.answer(
                i18n.get("tasks-create-first-project"), show_alert=True
            )
            return
        builder = InlineKeyboardBuilder()
        for p in projects:
            builder.row(
                types.InlineKeyboardButton(
                    text=p["name"], callback_data=f"task_create_{p['id']}"
                )
            )
        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("common-back"), callback_data="projects_list"
            )
        )
        await safe_edit_or_answer(
            callback, i18n.get("tasks-select-project"), reply_markup=builder.as_markup()
        )
        return
    await state.clear()
    await state.update_data(project_id=project_id)
    await callback.message.answer(i18n.get("tasks-enter-title"))
    await state.set_state(TaskStates.waiting_for_title)
    await callback.answer()


@router.message(TaskStates.waiting_for_title)
async def process_task_title(
    message: types.Message, state: FSMContext, i18n: I18nContext
):
    await state.update_data(title=message.text)
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-skip"), callback_data="skip_description"
        )
    )
    await message.answer(
        i18n.get("tasks-enter-description"), reply_markup=builder.as_markup()
    )
    await state.set_state(TaskStates.waiting_for_description)


@router.message(TaskStates.waiting_for_description)
async def process_task_description(
    message: types.Message, state: FSMContext, i18n: I18nContext
):
    await state.update_data(description=message.text)
    await message.answer(
        i18n.get("tasks-enter-priority"), reply_markup=get_priority_keyboard(i18n)
    )
    await state.set_state(TaskStates.waiting_for_priority)


@router.callback_query(TaskStates.waiting_for_description, F.data == "skip_description")
async def skip_task_description(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    await state.update_data(description=None)
    await callback.message.answer(
        i18n.get("tasks-enter-priority"), reply_markup=get_priority_keyboard(i18n)
    )
    await state.set_state(TaskStates.waiting_for_priority)
    await callback.answer()


@router.callback_query(TaskStates.waiting_for_priority, F.data.startswith("priority_"))
async def process_task_priority(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    priority = callback.data.split("_")[-1]
    await state.update_data(priority=priority)
    await callback.message.answer(
        i18n.get("tasks-enter-deadline-date"),
        reply_markup=get_deadline_date_keyboard(i18n),
    )
    await state.set_state(TaskStates.waiting_for_deadline_date)
    await callback.answer()


@router.callback_query(TaskStates.waiting_for_deadline_date, F.data.startswith("date_"))
async def process_task_deadline_date(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    choice = callback.data.split("_")[-1]
    now = datetime.datetime.now(datetime.timezone.utc)
    if choice == "skip":
        await state.update_data(deadline_date=None)
        return await go_to_assignee_selection(callback.message, state, api_client, i18n)
    if choice == "custom":
        await callback.message.answer(i18n.get("tasks-enter-custom-date"))
        await callback.answer()
        return
    date = now.date()
    if choice == "tomorrow":
        date = (now + datetime.timedelta(days=1)).date()
    elif choice == "weekend":
        days_ahead = 5 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        date = (now + datetime.timedelta(days=days_ahead)).date()
    elif choice == "nextweek":
        date = (now + datetime.timedelta(days=7 - now.weekday())).date()

    await state.update_data(deadline_date=date.isoformat())
    await callback.message.answer(
        i18n.get("tasks-enter-deadline-time"),
        reply_markup=get_deadline_time_keyboard(i18n),
    )
    await state.set_state(TaskStates.waiting_for_deadline_time)
    await callback.answer()


@router.message(TaskStates.waiting_for_deadline_date)
async def process_custom_date(
    message: types.Message, state: FSMContext, i18n: I18nContext
):
    try:
        date = datetime.datetime.strptime(message.text, "%Y-%m-%d").date()
        await state.update_data(deadline_date=date.isoformat())
        await message.answer(
            i18n.get("tasks-enter-deadline-time"),
            reply_markup=get_deadline_time_keyboard(i18n),
        )
        await state.set_state(TaskStates.waiting_for_deadline_time)
    except ValueError:
        await message.answer(i18n.get("tasks-invalid-date-format"))


@router.callback_query(TaskStates.waiting_for_deadline_time, F.data.startswith("time_"))
async def process_task_deadline_time(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    choice = callback.data.split("_")[-1]
    now = datetime.datetime.now(datetime.timezone.utc)
    if choice == "custom":
        await callback.message.answer(i18n.get("tasks-enter-custom-time"))
        await callback.answer()
        return
    time_str = "12:00"
    if choice == "plus1":
        time_str = (now + datetime.timedelta(hours=1)).strftime("%H:%M")
    elif choice == "plus2":
        time_str = (now + datetime.timedelta(hours=2)).strftime("%H:%M")
    elif choice == "morning":
        time_str = "09:00"
    elif choice == "evening":
        time_str = "18:00"

    await state.update_data(deadline_time=time_str)
    await go_to_assignee_selection(callback.message, state, api_client, i18n)
    await callback.answer()


@router.message(TaskStates.waiting_for_deadline_time)
async def process_custom_time(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    try:
        time_obj = datetime.datetime.strptime(message.text, "%H:%M").time()
        await state.update_data(deadline_time=time_obj.strftime("%H:%M"))
        await go_to_assignee_selection(message, state, api_client, i18n)
    except ValueError:
        await message.answer(i18n.get("tasks-invalid-time-format"))


@router.callback_query(TaskStates.waiting_for_assignee, F.data.startswith("assignee_"))
async def process_task_assignee(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    choice = callback.data.split("_")[-1]
    if choice == "skip":
        await state.update_data(
            assignee_id=None, assignee_name=i18n.get("common-unassigned")
        )
    else:
        await state.update_data(assignee_id=choice)
        data = await state.get_data()
        project = await api_client.get_project(
            callback.from_user.id, data["project_id"]
        )
        assignee_name = i18n.get("common-unassigned")
        for m in project.get("members", []):
            if str(m["user_detail"]["id"]) == choice:
                assignee_name = m["user_detail"]["first_name"]
                break
        await state.update_data(assignee_name=assignee_name)

    data = await state.get_data()
    project = await api_client.get_project(callback.from_user.id, data["project_id"])
    deadline_str = i18n.get("common-none")
    if data.get("deadline_date"):
        deadline_str = f"{data['deadline_date']} {data.get('deadline_time', '')}"

    text = i18n.get(
        "tasks-confirm-create",
        title=data["title"],
        project=project["name"],
        priority=i18n.get(f"priority-{data['priority']}"),
        deadline=deadline_str,
        assignee=data.get("assignee_name", i18n.get("common-unassigned")),
    )
    await safe_edit_or_answer(
        callback,
        text,
        reply_markup=get_confirmation_keyboard(
            "task_confirm_yes", "task_confirm_no", i18n
        ),
    )
    await state.set_state(TaskStates.waiting_for_confirmation)
    await callback.answer()


@router.callback_query(
    TaskStates.waiting_for_confirmation, F.data == "task_confirm_yes"
)
async def task_confirm_yes(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    data = await state.get_data()
    deadline = None
    if data.get("deadline_date"):
        deadline = f"{data['deadline_date']}T{data.get('deadline_time', '12:00')}:00Z"
    try:
        task = await api_client.create_task(
            callback.from_user.id,
            title=data["title"],
            project_id=data["project_id"],
            description=data.get("description"),
            priority=data["priority"],
            deadline=deadline,
            assignee=data.get("assignee_id"),
        )
        await callback.message.answer(i18n.get("tasks-created"))

        # Move to attachment step instead of clearing state
        await state.update_data(task_id=task["id"])
        await state.set_state(TaskStates.waiting_for_attachment)

        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("common-skip"), callback_data=f"task_view_{task['id']}"
            )
        )
        await callback.message.answer(
            i18n.get("tasks-upload-instruction"), reply_markup=builder.as_markup()
        )
    except Exception:
        await callback.message.answer(i18n.get("tasks-create-failed"))
        await state.clear()
    await callback.answer()


@router.callback_query(TaskStates.waiting_for_confirmation, F.data == "task_confirm_no")
async def task_confirm_no(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    await state.clear()
    await callback.answer(i18n.get("common-cancel"))
    await callback.message.edit_text(i18n.get("tasks-creation-cancelled"))


# --- ATTACHMENTS ---


@router.callback_query(F.data.startswith("task_attachments_"))
async def list_attachments(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    task_id = callback.data.split("_")[-1]
    attachments = await api_client.get_attachments(callback.from_user.id, task_id)
    lines = [f"📎 <b>{i18n.get('tasks-attachments')}</b>\n"]
    builder = InlineKeyboardBuilder()
    for a in attachments:
        lines.append(f"• {a['file_name']} ({a['file_size']} bytes)")
        builder.row(
            types.InlineKeyboardButton(
                text=f"❌ {a['file_name']}",
                callback_data=f"task_attach_del_{a['id']}_{task_id}",
            )
        )
    text = "\n".join(lines)
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-add-attachment"),
            callback_data=f"task_attach_start_{task_id}",
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=f"task_view_{task_id}"
        )
    )
    await safe_edit_or_answer(callback, text, reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("task_attach_del_"))
async def delete_attachment(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    parts = callback.data.split("_")
    attach_id, task_id = parts[3], parts[4]
    try:
        await api_client._request(
            "DELETE", f"/api/attachments/{attach_id}/", user_id=callback.from_user.id
        )
        await callback.answer(i18n.get("tasks-attachment-deleted"))
        await list_attachments(callback, api_client, i18n)
    except Exception:
        await callback.answer(i18n.get("tasks-attachment-delete-failed"))


@router.callback_query(F.data.startswith("task_attach_start_"))
async def start_attachment_upload(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    task_id = callback.data.split("_")[-1]
    await state.update_data(task_id=task_id)
    await state.set_state(TaskStates.waiting_for_attachment)
    await callback.message.answer(i18n.get("tasks-upload-instruction"))
    await callback.answer()


@router.message(
    TaskStates.waiting_for_attachment,
    F.content_type.in_({"document", "photo", "audio", "voice", "video"}),
)
async def process_attachment(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    data = await state.get_data()
    task_id = data["task_id"]
    file_id, file_name, mime_type, file_size = (
        None,
        "attachment",
        "application/octet-stream",
        0,
    )
    if message.document:
        file_id, file_name, mime_type, file_size = (
            message.document.file_id,
            message.document.file_name,
            message.document.mime_type,
            message.document.file_size,
        )
    elif message.photo:
        file_id, file_name, mime_type, file_size = (
            message.photo[-1].file_id,
            f"photo_{message.photo[-1].file_id}.jpg",
            "image/jpeg",
            message.photo[-1].file_size,
        )
    if file_id:
        await api_client.add_attachment(
            message.from_user.id, task_id, file_id, file_name, mime_type, file_size
        )
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-finish"), callback_data=f"task_view_{task_id}"
        )
    )
    await message.answer(
        i18n.get("tasks-attachment-added"), reply_markup=builder.as_markup()
    )


# --- ACTIONS ---


@router.callback_query(F.data.startswith("task_delete_confirm_"))
async def confirm_delete_task(callback: types.CallbackQuery, i18n: I18nContext):
    task_id = callback.data.split("_")[-1]
    await safe_edit_or_answer(
        callback,
        i18n.get("tasks-delete-confirm"),
        reply_markup=get_confirmation_keyboard(
            f"task_delete_final_{task_id}", f"task_view_{task_id}", i18n
        ),
    )


@router.callback_query(F.data.startswith("task_delete_final_"))
async def delete_task_final(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    task_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id
    try:
        task = await api_client.get_task(user_id, task_id)
        project_id = task["project"]
        await api_client.delete_task(user_id, task_id)
        await callback.answer(i18n.get("tasks-deleted"))
        tasks = await api_client.get_tasks(user_id, project=project_id)
        text = render_tasks_grouped(tasks, i18n)
        await safe_edit_or_answer(
            callback, text, reply_markup=get_tasks_list_keyboard(project_id, i18n)
        )
    except Exception:
        await callback.answer(i18n.get("tasks-delete-failed"))


@router.callback_query(F.data.startswith("focus_start_"))
async def start_focus_from_task(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    task_id = callback.data.split("_")[-1]
    from bot.handlers.focus import start_timer_callback_logic

    await start_timer_callback_logic(
        callback, api_client, i18n, task_id=task_id, duration=1500
    )


@router.callback_query(F.data.startswith("task_complete_"))
async def complete_task_callback(
    callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    task_id = callback.data.split("_")[-1]
    try:
        await api_client.update_task(callback.from_user.id, task_id, status="done")
        await callback.answer(i18n.get("timer-task-done"))
        task = await api_client.get_task(callback.from_user.id, task_id)
        if "project" in task and task["project"]:
            project = await api_client.get_project(
                callback.from_user.id, task["project"]
            )
            task["project_name"] = project["name"]
        text = render_task_detail(task, i18n)
        await safe_edit_or_answer(
            callback,
            text,
            reply_markup=get_task_detail_keyboard(task_id, task["project"], i18n),
        )
    except Exception:
        await callback.answer(i18n.get("tasks-status-update-failed"))


# --- EDITING ---


@router.callback_query(F.data.startswith("task_edit_"))
async def show_edit_options(callback: types.CallbackQuery, i18n: I18nContext):
    task_id = callback.data.split("_")[-1]
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Title", callback_data=f"task_edfield_title_{task_id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Description", callback_data=f"task_edfield_desc_{task_id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Priority", callback_data=f"task_edfield_prio_{task_id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Deadline", callback_data=f"task_edfield_dead_{task_id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Assignee", callback_data=f"task_edfield_ass_{task_id}"
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=f"task_view_{task_id}"
        )
    )
    await safe_edit_or_answer(
        callback, i18n.get("tasks-edit-select-field"), reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith("task_edfield_"))
async def start_edit_field(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    parts = callback.data.split("_")
    field, task_id = parts[2], parts[3]
    await state.update_data(edit_task_id=task_id)
    if field == "title":
        await callback.message.answer(i18n.get("tasks-enter-new-title"))
        await state.set_state(TaskStates.editing_title)
    elif field == "desc":
        await callback.message.answer(i18n.get("tasks-enter-new-description"))
        await state.set_state(TaskStates.editing_description)
    elif field == "prio":
        await callback.message.answer(
            i18n.get("tasks-select-new-priority"),
            reply_markup=get_priority_keyboard(i18n, prefix="editprio"),
        )
        await state.set_state(TaskStates.editing_priority)
    elif field == "dead":
        await callback.message.answer(
            i18n.get("tasks-select-new-deadline-date"),
            reply_markup=get_deadline_date_keyboard(i18n),
        )
        await state.set_state(TaskStates.editing_deadline_date)
    elif field == "ass":
        task = await api_client.get_task(callback.from_user.id, task_id)
        project = await api_client.get_project(callback.from_user.id, task["project"])
        await callback.message.answer(
            i18n.get("tasks-select-new-assignee"),
            reply_markup=get_assignee_keyboard(project["members"], i18n),
        )
        await state.set_state(TaskStates.editing_assignee)
    await callback.answer()


@router.message(TaskStates.editing_title)
async def process_edit_title(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    data = await state.get_data()
    await api_client.update_task(
        message.from_user.id, data["edit_task_id"], title=message.text
    )
    await message.answer(i18n.get("tasks-title-updated"))
    await state.clear()
    await view_task_internal(message, data["edit_task_id"], api_client, i18n)


@router.message(TaskStates.editing_description)
async def process_edit_description(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    data = await state.get_data()
    await api_client.update_task(
        message.from_user.id, data["edit_task_id"], description=message.text
    )
    await message.answer(i18n.get("tasks-description-updated"))
    await state.clear()
    await view_task_internal(message, data["edit_task_id"], api_client, i18n)


@router.callback_query(TaskStates.editing_priority, F.data.startswith("editprio_"))
async def process_edit_priority(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    priority = callback.data.split("_")[-1]
    data = await state.get_data()
    await api_client.update_task(
        callback.from_user.id, data["edit_task_id"], priority=priority
    )
    await callback.message.answer(i18n.get("tasks-priority-updated"))
    await state.clear()
    await view_task_internal(callback.message, data["edit_task_id"], api_client, i18n)
    await callback.answer()


@router.callback_query(TaskStates.editing_deadline_date, F.data.startswith("date_"))
async def process_edit_deadline_date(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    choice = callback.data.split("_")[-1]
    now = datetime.datetime.now(datetime.timezone.utc)
    if choice == "skip":
        data = await state.get_data()
        await api_client.update_task(
            callback.from_user.id, data["edit_task_id"], deadline=None
        )
        await callback.message.answer(i18n.get("tasks-deadline-removed"))
        await state.clear()
        return await view_task_internal(
            callback.message, data["edit_task_id"], api_client, i18n
        )
    if choice == "custom":
        await callback.message.answer(i18n.get("tasks-enter-custom-date"))
        await callback.answer()
        return
    date = now.date()
    if choice == "tomorrow":
        date = (now + datetime.timedelta(days=1)).date()
    elif choice == "weekend":
        days_ahead = 5 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        date = (now + datetime.timedelta(days=days_ahead)).date()
    elif choice == "nextweek":
        date = (now + datetime.timedelta(days=7 - now.weekday())).date()
    await state.update_data(edit_deadline_date=date.isoformat())
    await callback.message.answer(
        i18n.get("tasks-enter-deadline-time"),
        reply_markup=get_deadline_time_keyboard(i18n),
    )
    await state.set_state(TaskStates.editing_deadline_time)
    await callback.answer()


@router.message(TaskStates.editing_deadline_date)
async def process_edit_custom_date(
    message: types.Message, state: FSMContext, i18n: I18nContext
):
    try:
        date = datetime.datetime.strptime(message.text, "%Y-%m-%d").date()
        await state.update_data(edit_deadline_date=date.isoformat())
        await message.answer(
            i18n.get("tasks-enter-deadline-time"),
            reply_markup=get_deadline_time_keyboard(i18n),
        )
        await state.set_state(TaskStates.editing_deadline_time)
    except ValueError:
        await message.answer(i18n.get("tasks-invalid-date-format"))


@router.callback_query(TaskStates.editing_deadline_time, F.data.startswith("time_"))
async def process_edit_deadline_time(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    choice = callback.data.split("_")[-1]
    now = datetime.datetime.now(datetime.timezone.utc)
    if choice == "custom":
        await callback.message.answer(i18n.get("tasks-enter-custom-time"))
        await callback.answer()
        return
    time_str = "12:00"
    if choice == "morning":
        time_str = "09:00"
    elif choice == "evening":
        time_str = "18:00"
    elif choice == "plus1":
        time_str = (now + datetime.timedelta(hours=1)).strftime("%H:%M")
    elif choice == "plus2":
        time_str = (now + datetime.timedelta(hours=2)).strftime("%H:%M")
    data = await state.get_data()
    deadline = f"{data['edit_deadline_date']}T{time_str}:00Z"
    await api_client.update_task(
        callback.from_user.id, data["edit_task_id"], deadline=deadline
    )
    await callback.message.answer(i18n.get("tasks-deadline-updated"))
    await state.clear()
    await view_task_internal(callback.message, data["edit_task_id"], api_client, i18n)
    await callback.answer()


@router.message(TaskStates.editing_deadline_time)
async def process_edit_custom_time(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    try:
        time_obj = datetime.datetime.strptime(message.text, "%H:%M").time()
        data = await state.get_data()
        deadline = f"{data['edit_deadline_date']}T{time_obj.strftime('%H:%M')}:00Z"
        await api_client.update_task(
            message.from_user.id, data["edit_task_id"], deadline=deadline
        )
        await message.answer(i18n.get("tasks-deadline-updated"))
        await state.clear()
        await view_task_internal(message, data["edit_task_id"], api_client, i18n)
    except ValueError:
        await message.answer(i18n.get("tasks-invalid-time-format"))


@router.callback_query(TaskStates.editing_assignee, F.data.startswith("assignee_"))
async def process_edit_assignee(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
):
    choice = callback.data.split("_")[-1]
    assignee_id = None if choice == "skip" else choice
    data = await state.get_data()
    await api_client.update_task(
        callback.from_user.id, data["edit_task_id"], assignee=assignee_id
    )
    await callback.message.answer(i18n.get("tasks-assignee-updated"))
    await state.clear()
    await view_task_internal(callback.message, data["edit_task_id"], api_client, i18n)
    await callback.answer()
