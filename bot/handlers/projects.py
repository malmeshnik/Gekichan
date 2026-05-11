from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.utils.renderers import render_project_list, render_project_dashboard, render_members_list
from bot.utils.keyboards import (
    get_projects_list_keyboard, get_project_dashboard_keyboard,
    get_confirmation_keyboard
)
from bot.states.project_states import ProjectStates
from bot.utils.filters import I18nTextFilter
from bot.utils.navigation import safe_edit_or_answer
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(I18nTextFilter("menu-projects"))
@router.callback_query(F.data == "projects_list")
@router.callback_query(F.data.startswith("projects_list_page_"))
async def list_projects(event: types.Message | types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    user_id = event.chat.id
    page = 1
    if isinstance(event, types.CallbackQuery) and event.data.startswith("projects_list_page_"):
        page = int(event.data.split("_")[-1])

    projects = await api_client.get_projects(user_id)
    text = render_project_list(projects, i18n, page=page)
    keyboard = get_projects_list_keyboard(projects, i18n, page=page)

    await safe_edit_or_answer(event, text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("project_view_"))
async def view_project(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    user_id = callback.message.chat.id

    try:
        project = await api_client.get_project(user_id, project_id)
        text = render_project_dashboard(project, i18n)
        await safe_edit_or_answer(callback, text, reply_markup=get_project_dashboard_keyboard(project_id, i18n))
    except Exception:
        await callback.answer(i18n.get("projects-not-found"))

@router.callback_query(F.data == "project_create")
async def start_project_creation(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.answer(i18n.get("projects-enter-name"))
    await state.set_state(ProjectStates.waiting_for_name)
    await callback.answer()

@router.message(ProjectStates.waiting_for_name)
async def process_project_name(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    name = message.text
    user_id = message.chat.id

    try:
        await api_client.create_project(user_id, name)
        await message.answer(i18n.get("projects-created", name=name))
        await state.clear()
        # Redirect to projects list
        projects = await api_client.get_projects(user_id)
        text = render_project_list(projects, i18n, page=1)
        await message.answer(text, reply_markup=get_projects_list_keyboard(projects, i18n), parse_mode="HTML")
    except Exception:
        await message.answer(i18n.get("projects-create-failed"))

@router.callback_query(F.data.startswith("project_members_"))
async def list_project_members(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    project = await api_client.get_project(callback.message.chat.id, project_id)
    members = project.get('members', [])
    text = render_members_list(members, i18n)

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("members-add"), callback_data=f"project_member_add_{project_id}"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"project_view_{project_id}"))

    await safe_edit_or_answer(callback, text, reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("project_member_add_"))
async def select_member_add_method(callback: types.CallbackQuery, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("projects-add-by-username"), callback_data=f"project_add_username_{project_id}"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("projects-add-by-contact"), callback_data=f"project_add_contact_{project_id}"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"project_members_{project_id}"))

    await safe_edit_or_answer(callback, i18n.get("projects-add-member"), reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("project_add_username_"))
async def start_add_member_username(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await state.update_data(project_id=project_id)
    await state.set_state(ProjectStates.waiting_for_member_username)
    await callback.message.answer(i18n.get("projects-enter-username"))
    await callback.answer()

@router.message(ProjectStates.waiting_for_member_username)
async def process_member_username(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    data = await state.get_data()
    username = message.text.lstrip('@')

    try:
        await api_client.add_project_member(message.from_user.id, data['project_id'], member_username=username)
        await message.answer(i18n.get("projects-member-added"))
        await state.clear()
        # Refresh members dashboard
        await list_project_members_as_message(message, data['project_id'], api_client, i18n)
    except Exception:
        await message.answer(i18n.get("projects-member-add-failed"))

async def list_project_members_as_message(message: types.Message, project_id: str, api_client: APIClient, i18n: I18nContext):
    project = await api_client.get_project(message.chat.id, project_id)
    members = project.get('members', [])
    text = render_members_list(members, i18n)
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("members-add"), callback_data=f"project_member_add_{project_id}"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"project_view_{project_id}"))
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("project_add_contact_"))
async def start_add_member_contact(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await state.update_data(project_id=project_id)
    await state.set_state(ProjectStates.waiting_for_member_contact)
    await callback.message.answer(i18n.get("projects-share-contact"))
    await callback.answer()

@router.message(ProjectStates.waiting_for_member_contact, F.contact)
async def process_member_contact(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    data = await state.get_data()
    user_id = message.contact.user_id

    if not user_id:
        await message.answer(i18n.get("projects-member-add-failed"))
        return

    try:
        await api_client.add_project_member(message.from_user.id, data['project_id'], member_id=user_id)
        await message.answer(i18n.get("projects-member-added"))
        await state.clear()
        await list_project_members_as_message(message, data['project_id'], api_client, i18n)
    except Exception:
        await message.answer(i18n.get("projects-member-add-failed"))

@router.callback_query(F.data.startswith("project_delete_confirm_"))
async def confirm_delete_project(callback: types.CallbackQuery, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await safe_edit_or_answer(callback, i18n.get("projects-delete-confirm"), reply_markup=get_confirmation_keyboard(f"project_delete_final_{project_id}", f"project_view_{project_id}", i18n))

@router.callback_query(F.data.startswith("project_delete_final_"))
async def delete_project_final(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    user_id = callback.message.chat.id

    try:
        await api_client.delete_project(user_id, project_id)
        await callback.answer(i18n.get("projects-deleted"))
        # Back to list
        projects = await api_client.get_projects(user_id)
        text = render_project_list(projects, i18n, page=1)
        await safe_edit_or_answer(callback, text, reply_markup=get_projects_list_keyboard(projects, i18n))
    except Exception:
        await callback.answer(i18n.get("projects-delete-failed"))

@router.callback_query(F.data == "project_search")
async def start_project_search(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.answer(i18n.get("projects-enter-search"))
    await state.set_state(ProjectStates.waiting_for_search_query)
    await callback.answer()

@router.message(ProjectStates.waiting_for_search_query)
async def process_project_search(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    query = message.text
    user_id = message.chat.id

    # In a real app we'd pass the query to the API
    projects = await api_client.get_projects(user_id)
    filtered = [p for p in projects if query.lower() in p['name'].lower()]

    text = render_project_list(filtered, i18n, page=1)
    keyboard = get_projects_list_keyboard(filtered, i18n) # Use filtered list for keyboard

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")
    await state.clear()

@router.callback_query(F.data == "projects_archive")
async def view_archived_projects(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)

@router.callback_query(F.data.startswith("project_analytics_"))
async def view_project_analytics(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)

@router.callback_query(F.data.startswith("project_focus_"))
async def view_project_focus(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)

@router.callback_query(F.data.startswith("project_settings_"))
async def view_project_settings(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)
