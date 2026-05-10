from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.keyboards.projects import (
    get_projects_keyboard, get_project_detail_keyboard,
    get_member_add_options_keyboard
)
from bot.states.project_states import ProjectStates
from bot.utils.filters import I18nTextFilter

router = Router()

@router.message(I18nTextFilter("menu-projects"))
@router.callback_query(F.data == "projects_list")
async def list_projects(event: types.Message | types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    user_id = event.from_user.id
    projects = await api_client.get_projects(user_id)

    text = i18n.projects.list()
    keyboard = get_projects_keyboard(projects, i18n)

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=keyboard)
    else:
        await event.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("project_view_"))
async def view_project(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    # In a real app we'd fetch detail, but list already has most info for MVP
    projects = await api_client.get_projects(user_id)
    project = next((p for p in projects if str(p['id']) == project_id), None)

    if not project:
        await callback.answer(i18n.projects.not_found())
        return

    text = (
        f"<b>{i18n.projects.label()}</b> {project['name']}\n"
        f"<b>{i18n.projects.desc_label()}</b> {project.get('description') or i18n.projects.no_desc()}"
    )
    await callback.message.edit_text(text, reply_markup=get_project_detail_keyboard(project_id, i18n), parse_mode="HTML")

@router.callback_query(F.data == "project_create")
async def start_project_creation(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    await callback.message.answer(i18n.projects.enter_name())
    await state.set_state(ProjectStates.waiting_for_name)
    await callback.answer()

@router.message(ProjectStates.waiting_for_name)
async def process_project_name(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    name = message.text
    user_id = message.from_user.id

    try:
        await api_client.create_project(user_id, name)
        await message.answer(i18n.projects.created(name=name))
        await state.clear()
        # Refresh list
        projects = await api_client.get_projects(user_id)
        await message.answer(i18n.projects.list(), reply_markup=get_projects_keyboard(projects, i18n))
    except Exception:
        await message.answer(i18n.projects.create_failed())

@router.callback_query(F.data.startswith("project_member_add_"))
async def select_member_add_method(callback: types.CallbackQuery, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await callback.message.edit_text(
        i18n.projects.add_member(),
        reply_markup=get_member_add_options_keyboard(project_id, i18n)
    )

@router.callback_query(F.data.startswith("project_add_username_"))
async def start_add_member_username(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await state.update_data(project_id=project_id)
    await state.set_state(ProjectStates.waiting_for_member_username)
    await callback.message.answer(i18n.projects.enter_username())
    await callback.answer()

@router.message(ProjectStates.waiting_for_member_username)
async def process_member_username(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    data = await state.get_data()
    username = message.text.lstrip('@')

    try:
        await api_client.add_project_member(message.from_user.id, data['project_id'], member_username=username)
        await message.answer(i18n.projects.member_added())
        await state.clear()
    except Exception:
        await message.answer(i18n.projects.member_add_failed())

@router.callback_query(F.data.startswith("project_add_contact_"))
async def start_add_member_contact(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    await state.update_data(project_id=project_id)
    await state.set_state(ProjectStates.waiting_for_member_contact)
    await callback.message.answer(i18n.projects.share_contact())
    await callback.answer()

@router.message(ProjectStates.waiting_for_member_contact, F.contact)
async def process_member_contact(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    data = await state.get_data()
    user_id = message.contact.user_id

    if not user_id:
        await message.answer(i18n.projects.member_add_failed())
        return

    try:
        await api_client.add_project_member(message.from_user.id, data['project_id'], member_id=user_id)
        await message.answer(i18n.projects.member_added())
        await state.clear()
    except Exception:
        await message.answer(i18n.projects.member_add_failed())

@router.callback_query(F.data.startswith("project_delete_"))
async def delete_project(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    project_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.delete_project(user_id, project_id)
        await callback.answer(i18n.projects.deleted())
        # Refresh list
        projects = await api_client.get_projects(user_id)
        await callback.message.edit_text(i18n.projects.list(), reply_markup=get_projects_keyboard(projects, i18n))
    except Exception:
        await callback.answer(i18n.projects.delete_failed())
