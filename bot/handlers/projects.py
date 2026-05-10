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
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(I18nTextFilter("menu-projects"))
@router.callback_query(F.data == "projects_list")
@router.callback_query(F.data.startswith("projects_list_page_"))
async def list_projects(event: types.Message | types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    user_id = event.from_user.id
    page = 1
    if isinstance(event, types.CallbackQuery) and event.data.startswith("projects_list_page_"):
        page = int(event.data.split("_")[-1])

    projects = await api_client.get_projects(user_id)
    text = render_project_list(projects, i18n)
    keyboard = get_projects_list_keyboard(projects, i18n, page=page)

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=keyboard, parse_mode="HTML")
    else:
        await event.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

@router.callback_query(F.data.startswith("project_view_"))
async def view_project(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        project = await api_client.get_project(user_id, project_id)
        text = render_project_dashboard(project, i18n)
        await callback.message.edit_text(text, reply_markup=get_project_dashboard_keyboard(project_id, i18n), parse_mode="HTML")
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
    user_id = message.from_user.id

    try:
        await api_client.create_project(user_id, name)
        await message.answer(i18n.get("projects-created", name=name))
        await state.clear()
        # Redirect to projects list
        projects = await api_client.get_projects(user_id)
        text = render_project_list(projects, i18n)
        await message.answer(text, reply_markup=get_projects_list_keyboard(projects, i18n), parse_mode="HTML")
    except Exception:
        await message.answer(i18n.get("projects-create-failed"))

@router.callback_query(F.data.startswith("project_members_"))
async def list_project_members(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    project = await api_client.get_project(callback.from_user.id, project_id)
    members = project.get('members', [])
    text = render_members_list(members, i18n)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=i18n.get("members-add"), callback_data=f"project_member_add_{project_id}"))
    builder.row(types.InlineKeyboardButton(text=i18n.get("common-back"), callback_data=f"project_view_{project_id}"))

    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("project_delete_confirm_"))
async def confirm_delete_project(callback: types.CallbackQuery, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await callback.message.edit_text(
        i18n.get("projects-delete-confirm"),
        reply_markup=get_confirmation_keyboard(f"project_delete_final_{project_id}", f"project_view_{project_id}", i18n)
    )

@router.callback_query(F.data.startswith("project_delete_final_"))
async def delete_project_final(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.delete_project(user_id, project_id)
        await callback.answer(i18n.get("projects-deleted"))
        # Back to list
        projects = await api_client.get_projects(user_id)
        text = render_project_list(projects, i18n)
        await callback.message.edit_text(text, reply_markup=get_projects_list_keyboard(projects, i18n), parse_mode="HTML")
    except Exception:
        await callback.answer(i18n.get("projects-delete-failed"))

@router.callback_query(F.data == "project_search")
async def start_project_search(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.answer(i18n.get("projects-enter-search"))
    await state.set_state(ProjectStates.waiting_for_name) # Reuse for simplicity or create new
    await callback.answer()

@router.callback_query(F.data == "projects_archive")
async def view_archived_projects(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.answer(i18n.get("common-not-implemented"), show_alert=True)
