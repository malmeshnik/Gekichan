from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.services.ui_renderer import UIRenderer
from bot.keyboards.builders import KeyboardBuilder, ProjectCallback
from bot.states.project_states import ProjectStates

router = Router()

@router.message(F.text.in_(["📁 Projects", "📁 Проєкти", "📁 Проекты"]))
@router.callback_query(ProjectCallback.filter(F.action == "list"))
async def list_projects(event: types.Message | types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: ProjectCallback = None):
    user_id = event.from_user.id
    page = callback_data.page if callback_data else 0

    projects_data = await api_client.get_projects(user_id)
    # Basic pagination logic (frontend-side for now as we don't want to change backend too much)
    PAGE_SIZE = 5
    total_pages = (len(projects_data) + PAGE_SIZE - 1) // PAGE_SIZE
    start_idx = page * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    current_page_projects = projects_data[start_idx:end_idx]

    text = f"<b>{i18n.get('projects-title')}</b>\n\n"
    if not projects_data:
        text += i18n.get("projects-empty")
    else:
        for i, p in enumerate(current_page_projects, start=start_idx + 1):
            text += UIRenderer.render_project_list_item(p, i, i18n)

    keyboard = KeyboardBuilder.project_list(current_page_projects, page, total_pages, i18n)

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await event.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(ProjectCallback.filter(F.action == "view"))
async def view_project(callback: types.CallbackQuery, callback_data: ProjectCallback, api_client: APIClient, i18n: I18nContext):
    project_id = callback_data.id
    user_id = callback.from_user.id

    # Fetch project details
    projects = await api_client.get_projects(user_id)
    project = next((p for p in projects if str(p['id']) == project_id), None)

    if not project:
        await callback.answer(i18n.get("project-not-found"))
        return

    # Use real stats from project object
    stats = {
        "members_total": project.get('members_count', 0),
        "members_active": project.get('active_members_count', 0),
        "tasks_total": project.get('tasks_count', 0),
        "tasks_in_progress": project.get('tasks_in_progress_count', 0),
        "tasks_overdue": project.get('overdue_tasks_count', 0),
        "tasks_done": project.get('tasks_done_count', 0),
        "focus_time": "0h", # Focus time still needs backend service integration
        "last_activity": "5m" # Placeholder for activity timing
    }

    text = UIRenderer.render_project_dashboard(project, stats, i18n)
    await callback.message.edit_text(text, reply_markup=KeyboardBuilder.project_dashboard(project_id, i18n), parse_mode="HTML")

@router.callback_query(ProjectCallback.filter(F.action == "delete_confirm"))
async def confirm_delete_project(callback: types.CallbackQuery, callback_data: ProjectCallback, i18n: I18nContext):
    project_id = callback_data.id
    text = f"<b>{i18n.get('confirm-delete-project')}</b>\n\n{i18n.get('confirm-delete-project-note', count=0)}"

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(text=i18n.get("common-delete"), callback_data=ProjectCallback(action="delete_final", id=project_id))
    builder.button(text=i18n.get("common-cancel"), callback_data=ProjectCallback(action="view", id=project_id))
    builder.adjust(1)

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(ProjectCallback.filter(F.action == "delete_final"))
async def delete_project_final(callback: types.CallbackQuery, callback_data: ProjectCallback, api_client: APIClient, i18n: I18nContext):
    project_id = callback_data.id
    user_id = callback.from_user.id

    try:
        await api_client.delete_project(user_id, project_id)
        await callback.answer(i18n.get("project-deleted"))
        await list_projects(callback, api_client, i18n)
    except Exception:
        await callback.answer(i18n.get("project-delete-failed"))

@router.callback_query(ProjectCallback.filter(F.action == "search"))
async def start_project_search(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.answer(i18n.get("search-prompt"))
    await state.set_state(ProjectStates.waiting_for_search)
    await callback.answer()

@router.message(ProjectStates.waiting_for_search)
async def process_project_search(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    query = message.text
    user_id = message.from_user.id

    # Simple search implementation on top of projects list
    projects = await api_client.get_projects(user_id)
    results = [p for p in projects if query.lower() in p['name'].lower() or (p.get('description') and query.lower() in p['description'].lower())]

    text = f"<b>{i18n.get('common-search')}</b>: {query}\n\n"
    if not results:
        text += i18n.get("search-no-results", query=query)
    else:
        for i, p in enumerate(results, 1):
            text += UIRenderer.render_project_list_item(p, i, i18n)

    await state.clear()
    await message.answer(text, reply_markup=KeyboardBuilder.project_list(results, 0, 1, i18n), parse_mode="HTML")

@router.callback_query(ProjectCallback.filter(F.action == "members"))
async def list_project_members(callback: types.CallbackQuery, callback_data: ProjectCallback, api_client: APIClient, i18n: I18nContext):
    project_id = callback_data.id
    user_id = callback.from_user.id

    members = await api_client.get_project_members(user_id, project_id)

    text = f"<b>{i18n.get('members-title')}</b>\n\n"
    for m in members:
        user = m['user']
        role = i18n.get(f"members-role-{m['role']}")
        # random emoji avatar mock
        avatar = "🦊" if m['role'] == "owner" else "🐼"

        if user.get('is_active_now'):
            status = i18n.get("common-active-now")
        elif user.get('last_activity_at'):
            status = i18n.get("common-last-active", time="some time") # Simplified
        else:
            status = ""

        text += f"{avatar} <b>{user['first_name']}</b> — {role}\n{status}\n\n"

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardBuilder().button(text=i18n.get("members-btn-add"), callback_data=ProjectCallback(action="member_add", id=project_id)).export()[0],
        InlineKeyboardBuilder().button(text=i18n.get("members-btn-manage-roles"), callback_data=ProjectCallback(action="member_roles", id=project_id)).export()[0]
    )
    builder.row(InlineKeyboardBuilder().button(text=i18n.get("common-back"), callback_data=ProjectCallback(action="view", id=project_id)).export()[0])

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")
