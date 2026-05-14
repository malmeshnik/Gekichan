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
from bot.utils.callbacks import (
    TasksHubCb,
    ProjectTasksCb,
    TaskViewCb,
    TaskCreateCb,
    TaskActionCb,
    TaskEditCb,
    TaskPriorityCb,
    TaskDeadlineDateCb,
    TaskDeadlineTimeCb,
    TaskAssigneeCb,
    TaskAttachmentCb,
    CommonConfirmCb,
    ProjectActionCb,
    FocusStartCb,
)
import datetime

router = Router()


@router.message(I18nTextFilter("menu-tasks"))
@router.callback_query(TasksHubCb.filter(F.section == None))
async def tasks_hub(
    event: types.Message | types.CallbackQuery, api_client: APIClient, i18n: I18nContext
):
    user_id = event.from_user.id
    # Fetch some stats for counters
    overdue_tasks = await api_client.get_tasks(user_id, overdue="true")
    active_tasks = await api_client.get_tasks(user_id, status="todo")
    today = datetime.datetime.now().date().isoformat()
    completed_today = await api_client.get_tasks(
        user_id, status="done", deadline_date=today
    )

    text = (
        f"<b>{i18n.get('menu-tasks')}</b>\n\n"
        f"{i18n.get('tasks-hub-overdue')}: {len(overdue_tasks)}\n"
        f"📌 {i18n.get('tasks-status-todo')}: {len(active_tasks)}\n"
        f"{i18n.get('tasks-hub-completed')} {i18n.get('common-today')}: {len(completed_today)}"
    )

    from bot.utils.keyboards import get_tasks_hub_keyboard

    if isinstance(event, types.Message):
        await event.answer(
            text, reply_markup=get_tasks_hub_keyboard(i18n), parse_mode="HTML"
        )
    else:
        await safe_edit_or_answer(event, text, reply_markup=get_tasks_hub_keyboard(i18n))


@router.callback_query(TasksHubCb.filter(F.section != None))
async def tasks_hub_sections(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TasksHubCb,
):
    section = callback_data.section
    user_id = callback.from_user.id
    params = {}
    title_key = f"tasks-hub-{section}"

    if section == "my":
        pass
    elif section == "no-project":
        params["project"] = "null"
    elif section == "today":
        params["deadline_date"] = datetime.datetime.now().date().isoformat()
    elif section == "tomorrow":
        params["deadline_date"] = (
            (datetime.datetime.now() + datetime.timedelta(days=1)).date().isoformat()
        )
    elif section == "week":
        params["deadline_after"] = datetime.datetime.now().date().isoformat()
        params["deadline_before"] = (
            (datetime.datetime.now() + datetime.timedelta(days=7)).date().isoformat()
        )
    elif section == "overdue":
        params["overdue"] = "true"
    elif section == "completed":
        params["status"] = "done"
    elif section == "by-projects":
        from bot.handlers.projects import list_projects

        return await list_projects(callback, api_client, i18n)

    tasks = await api_client.get_tasks(user_id, **params)
    text = render_tasks_grouped(tasks, i18n, title=i18n.get(title_key))

    from bot.utils.keyboards import get_tasks_list_keyboard

    await safe_edit_or_answer(
        callback,
        text,
        reply_markup=get_tasks_list_keyboard(
            None,
            i18n,
            tasks,
            back_callback="tasks_hub",
            show_create=(section != "completed"),
        ),
    )


@router.callback_query(ProjectTasksCb.filter())
async def list_project_tasks(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: ProjectTasksCb,
):
    project_id = callback_data.project_id
    page = callback_data.page
    if project_id == "null":
        project_id = None

    tasks = await api_client.get_tasks(callback.from_user.id, project=project_id)
    text = render_tasks_grouped(tasks, i18n)
    await safe_edit_or_answer(
        callback,
        text,
        reply_markup=get_tasks_list_keyboard(
            project_id, i18n, tasks, page=page
        ),
    )


@router.callback_query(TaskViewCb.filter())
async def view_task(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskViewCb,
):
    task_id = callback_data.id
    task = await api_client.get_task(callback.from_user.id, task_id)

    if "project" in task and task["project"]:
        project = await api_client.get_project(callback.from_user.id, task["project"])
        task["project_name"] = project["name"]

    text = render_task_detail(task, i18n)

    back_callback = (
        ProjectTasksCb(project_id=task["project"]).pack()
        if task.get("project")
        else TasksHubCb().pack()
    )

    await safe_edit_or_answer(
        callback,
        text,
        reply_markup=get_task_detail_keyboard(
            task_id, task["project"], i18n, back_callback=back_callback
        ),
    )


# --- CREATE TASK FLOW ---


@router.callback_query(TaskCreateCb.filter())
async def start_task_creation(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskCreateCb,
):
    project_id = callback_data.project_id
    if project_id == "none":
        projects = await api_client.get_projects(callback.from_user.id)
        builder = InlineKeyboardBuilder()

        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("tasks-hub-no-project"),
                callback_data=TaskCreateCb(project_id="null").pack(),
            )
        )

        for p in projects:
            builder.row(
                types.InlineKeyboardButton(
                    text=p["name"], callback_data=TaskCreateCb(project_id=p["id"]).pack()
                )
            )
        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("common-back"), callback_data=TasksHubCb().pack()
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
            text=i18n.get("common-skip"),
            callback_data=TaskActionCb(action="sd", id="new").pack()
        )
    )
    await message.answer(
        i18n.get("tasks-enter-description"), reply_markup=builder.as_markup()
    )
    await state.set_state(TaskStates.waiting_for_description)


@router.callback_query(TaskStates.waiting_for_description, TaskActionCb.filter(F.action == "sd"))
async def skip_task_description(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    await state.update_data(description=None)
    await callback.message.answer(
        i18n.get("tasks-enter-priority"), reply_markup=get_priority_keyboard(i18n)
    )
    await state.set_state(TaskStates.waiting_for_priority)
    await callback.answer()


@router.message(TaskStates.waiting_for_description)
async def process_task_description(
    message: types.Message, state: FSMContext, i18n: I18nContext
):
    await state.update_data(description=message.text)
    await message.answer(
        i18n.get("tasks-enter-priority"), reply_markup=get_priority_keyboard(i18n)
    )
    await state.set_state(TaskStates.waiting_for_priority)


@router.callback_query(TaskPriorityCb.filter(F.is_edit == False))
async def process_task_priority(
    callback: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    callback_data: TaskPriorityCb,
):
    priority = callback_data.priority
    await state.update_data(priority=priority)
    await callback.message.answer(
        i18n.get("tasks-enter-deadline-date"),
        reply_markup=get_deadline_date_keyboard(i18n),
    )
    await state.set_state(TaskStates.waiting_for_deadline_date)
    await callback.answer()


@router.callback_query(TaskDeadlineDateCb.filter(F.is_edit == False))
async def process_task_deadline_date(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskDeadlineDateCb,
):
    choice = callback_data.choice
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


@router.callback_query(TaskDeadlineTimeCb.filter(F.is_edit == False))
async def process_task_deadline_time(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskDeadlineTimeCb,
):
    choice = callback_data.choice
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


@router.callback_query(TaskAssigneeCb.filter(F.is_edit == False))
async def process_task_assignee(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskAssigneeCb,
):
    choice = callback_data.id
    data = await state.get_data()
    project_id = data.get("project_id")

    if choice == "skip":
        await state.update_data(
            assignee_id=None, assignee_name=i18n.get("common-unassigned")
        )
    else:
        await state.update_data(assignee_id=choice)
        assignee_name = i18n.get("common-unassigned")
        if project_id and project_id != "null":
            project = await api_client.get_project(callback.from_user.id, project_id)
            for m in project.get("members", []):
                if str(m["user_detail"]["id"]) == choice:
                    assignee_name = m["user_detail"]["first_name"]
                    break
        else:
            assignee_name = f"User {choice}"

        await state.update_data(assignee_name=assignee_name)

    data = await state.get_data()
    project_name = i18n.get("common-none")
    if project_id and project_id != "null":
        project = await api_client.get_project(callback.from_user.id, project_id)
        project_name = project["name"]
    else:
        project_name = i18n.get("tasks-hub-no-project")

    deadline_str = i18n.get("common-none")
    if data.get("deadline_date"):
        deadline_str = f"{data['deadline_date']} {data.get('deadline_time', '')}"

    text = i18n.get(
        "tasks-confirm-create",
        title=data["title"],
        project=project_name,
        priority=i18n.get(f"priority-{data['priority']}"),
        deadline=deadline_str,
        assignee=data.get("assignee_name", i18n.get("common-unassigned")),
    )

    await safe_edit_or_answer(
        callback,
        text,
        reply_markup=get_confirmation_keyboard(
            CommonConfirmCb(action="task_create_yes").pack(),
            CommonConfirmCb(action="task_create_no").pack(),
            i18n,
        ),
    )
    await state.set_state(TaskStates.waiting_for_confirmation)
    await callback.answer()


@router.callback_query(
    TaskStates.waiting_for_confirmation,
    CommonConfirmCb.filter(F.action == "task_create_yes"),
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
        project_id = data["project_id"]
        if project_id == "null":
            project_id = None

        task = await api_client.create_task(
            callback.from_user.id,
            title=data["title"],
            project_id=project_id,
            description=data.get("description"),
            priority=data["priority"],
            deadline=deadline,
            assignee=data.get("assignee_id"),
        )
        await callback.message.answer(i18n.get("tasks-created"))

        await state.update_data(task_id=task["id"])
        await state.set_state(TaskStates.waiting_for_attachment)

        builder = InlineKeyboardBuilder()
        builder.row(
            types.InlineKeyboardButton(
                text=i18n.get("common-skip"),
                callback_data=TaskViewCb(id=task["id"]).pack(),
            )
        )
        await callback.message.answer(
            i18n.get("tasks-upload-instruction"), reply_markup=builder.as_markup()
        )
    except Exception:
        await callback.message.answer(i18n.get("tasks-create-failed"))
        await state.clear()
    await callback.answer()


@router.callback_query(
    TaskStates.waiting_for_confirmation, CommonConfirmCb.filter(F.action == "task_create_no")
)
async def task_confirm_no(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    await state.clear()
    await callback.answer(i18n.get("common-cancel"))
    await callback.message.edit_text(i18n.get("tasks-creation-cancelled"))


# --- ATTACHMENTS ---


@router.callback_query(TaskAttachmentCb.filter(F.action == "l"))
async def list_attachments(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskAttachmentCb,
    state: FSMContext,
):
    task_id = callback_data.id
    await state.update_data(task_id=task_id)
    attachments = await api_client.get_attachments(callback.from_user.id, task_id)
    lines = [f"📎 <b>{i18n.get('tasks-attachments')}</b>\n"]
    builder = InlineKeyboardBuilder()
    for a in attachments:
        lines.append(f"• {a['file_name']} ({a['file_size']} bytes)")
        builder.row(
            types.InlineKeyboardButton(
                text=f"❌ {a['file_name']}",
                callback_data=TaskAttachmentCb(
                    action="d", id=a["id"]
                ).pack(),
            )
        )
    text = "\n".join(lines)
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("tasks-add-attachment"),
            callback_data=TaskAttachmentCb(action="s", id=task_id).pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=TaskViewCb(id=task_id).pack()
        )
    )
    await safe_edit_or_answer(callback, text, reply_markup=builder.as_markup())


@router.callback_query(TaskAttachmentCb.filter(F.action == "d"))
async def delete_attachment(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskAttachmentCb,
    state: FSMContext,
):
    attach_id = callback_data.id
    try:
        await api_client._request(
            "DELETE", f"/api/attachments/{attach_id}/", user_id=callback.from_user.id
        )
        await callback.answer(i18n.get("tasks-attachment-deleted"))

        data = await state.get_data()
        task_id = data.get("task_id")
        if task_id:
            await list_attachments(callback, api_client, i18n, TaskAttachmentCb(action="l", id=task_id), state)
        else:
            await callback.message.edit_text(i18n.get("tasks-attachment-deleted"))
    except Exception:
        await callback.answer(i18n.get("tasks-attachment-delete-failed"))


@router.callback_query(TaskAttachmentCb.filter(F.action == "s"))
async def start_attachment_upload(
    callback: types.CallbackQuery,
    state: FSMContext,
    i18n: I18nContext,
    callback_data: TaskAttachmentCb,
):
    task_id = callback_data.id
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
            text=i18n.get("common-finish"),
            callback_data=TaskViewCb(id=task_id).pack(),
        )
    )
    await message.answer(
        i18n.get("tasks-attachment-added"), reply_markup=builder.as_markup()
    )


# --- ACTIONS ---


@router.callback_query(TaskActionCb.filter(F.action == "dc"))
async def confirm_delete_task(
    callback: types.CallbackQuery, i18n: I18nContext, callback_data: TaskActionCb
):
    task_id = callback_data.id
    await safe_edit_or_answer(
        callback,
        i18n.get("tasks-delete-confirm"),
        reply_markup=get_confirmation_keyboard(
            TaskActionCb(action="df", id=task_id).pack(),
            TaskViewCb(id=task_id).pack(),
            i18n,
        ),
    )


@router.callback_query(TaskActionCb.filter(F.action == "df"))
async def delete_task_final(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskActionCb,
):
    task_id = callback_data.id
    user_id = callback.from_user.id
    try:
        task = await api_client.get_task(user_id, task_id)
        project_id = task["project"]
        await api_client.delete_task(user_id, task_id)
        await callback.answer(i18n.get("tasks-deleted"))
        tasks = await api_client.get_tasks(user_id, project=project_id)
        text = render_tasks_grouped(tasks, i18n)
        await safe_edit_or_answer(
            callback,
            text,
            reply_markup=get_tasks_list_keyboard(project_id, i18n, tasks),
        )
    except Exception:
        await callback.answer(i18n.get("tasks-delete-failed"))


@router.callback_query(TaskActionCb.filter(F.action == "c"))
async def complete_task_callback(
    callback: types.CallbackQuery,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskActionCb,
):
    task_id = callback_data.id
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


@router.callback_query(TaskActionCb.filter(F.action == "e"))
async def show_edit_options(
    callback: types.CallbackQuery, i18n: I18nContext, callback_data: TaskActionCb
):
    task_id = callback_data.id
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Title", callback_data=TaskEditCb(field="t", id=task_id).pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Description",
            callback_data=TaskEditCb(field="d", id=task_id).pack(),
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Priority", callback_data=TaskEditCb(field="p", id=task_id).pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Deadline", callback_data=TaskEditCb(field="dl", id=task_id).pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text="Assignee", callback_data=TaskEditCb(field="a", id=task_id).pack()
        )
    )
    builder.row(
        types.InlineKeyboardButton(
            text=i18n.get("common-back"), callback_data=TaskViewCb(id=task_id).pack()
        )
    )
    await safe_edit_or_answer(
        callback, i18n.get("tasks-edit-select-field"), reply_markup=builder.as_markup()
    )


@router.callback_query(TaskEditCb.filter())
async def start_edit_field(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskEditCb,
):
    field, task_id = callback_data.field, callback_data.id
    await state.update_data(edit_task_id=task_id)
    if field == "t":
        await callback.message.answer(i18n.get("tasks-enter-new-title"))
        await state.set_state(TaskStates.editing_title)
    elif field == "d":
        await callback.message.answer(i18n.get("tasks-enter-new-description"))
        await state.set_state(TaskStates.editing_description)
    elif field == "p":
        await callback.message.answer(
            i18n.get("tasks-select-new-priority"),
            reply_markup=get_priority_keyboard(i18n, prefix="editprio"),
        )
        await state.set_state(TaskStates.editing_priority)
    elif field == "dl":
        await callback.message.answer(
            i18n.get("tasks-select-new-deadline-date"),
            reply_markup=get_deadline_date_keyboard(i18n, is_edit=True),
        )
        await state.set_state(TaskStates.editing_deadline_date)
    elif field == "a":
        task = await api_client.get_task(callback.from_user.id, task_id)
        if task.get("project"):
            project = await api_client.get_project(
                callback.from_user.id, task["project"]
            )
            members = project["members"]
        else:
            members = []
        await callback.message.answer(
            i18n.get("tasks-select-new-assignee"),
            reply_markup=get_assignee_keyboard(members, i18n, is_edit=True),
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


@router.callback_query(TaskPriorityCb.filter(F.is_edit == True))
async def process_edit_priority(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskPriorityCb,
):
    priority = callback_data.priority
    data = await state.get_data()
    await api_client.update_task(
        callback.from_user.id, data["edit_task_id"], priority=priority
    )
    await callback.message.answer(i18n.get("tasks-priority-updated"))
    await state.clear()
    await view_task_internal(callback.message, data["edit_task_id"], api_client, i18n)
    await callback.answer()


@router.callback_query(TaskDeadlineDateCb.filter(F.is_edit == True))
async def process_edit_deadline_date(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskDeadlineDateCb,
):
    choice = callback_data.choice
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
        reply_markup=get_deadline_time_keyboard(i18n, is_edit=True),
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
            reply_markup=get_deadline_time_keyboard(i18n, is_edit=True),
        )
        await state.set_state(TaskStates.editing_deadline_time)
    except ValueError:
        await message.answer(i18n.get("tasks-invalid-date-format"))


@router.callback_query(TaskDeadlineTimeCb.filter(F.is_edit == True))
async def process_edit_deadline_time(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskDeadlineTimeCb,
):
    choice = callback_data.choice
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


@router.callback_query(TaskAssigneeCb.filter(F.is_edit == True))
async def process_edit_assignee(
    callback: types.CallbackQuery,
    state: FSMContext,
    api_client: APIClient,
    i18n: I18nContext,
    callback_data: TaskAssigneeCb,
):
    choice = callback_data.id
    assignee_id = None if choice == "skip" else choice
    data = await state.get_data()
    await api_client.update_task(
        callback.from_user.id, data["edit_task_id"], assignee=assignee_id
    )
    await callback.message.answer(i18n.get("tasks-assignee-updated"))
    await state.clear()
    await view_task_internal(callback.message, data["edit_task_id"], api_client, i18n)
    await callback.answer()


# --- HELPERS ---


async def go_to_assignee_selection(
    message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext
):
    data = await state.get_data()
    project_id = data.get("project_id")
    if project_id and project_id != "null":
        project = await api_client.get_project(message.chat.id, project_id)
        members = project.get("members", [])
    else:
        members = []

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
