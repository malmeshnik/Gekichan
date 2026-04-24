from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from bot.services.api_client import APIClient
from bot.keyboards.projects import get_projects_keyboard, get_project_detail_keyboard
from bot.states.project_states import ProjectStates

router = Router()

@router.message(F.text == "Projects")
@router.callback_query(F.data == "projects_list")
async def list_projects(event: types.Message | types.CallbackQuery, api_client: APIClient):
    user_id = event.from_user.id
    projects = await api_client.get_projects(user_id)

    text = "Your Projects:"
    keyboard = get_projects_keyboard(projects)

    if isinstance(event, types.Message):
        await event.answer(text, reply_markup=keyboard)
    else:
        await event.message.edit_text(text, reply_markup=keyboard)

@router.callback_query(F.data.startswith("project_view_"))
async def view_project(callback: types.CallbackQuery, api_client: APIClient):
    project_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    # In a real app we'd fetch detail, but list already has most info for MVP
    projects = await api_client.get_projects(user_id)
    project = next((p for p in projects if str(p['id']) == project_id), None)

    if not project:
        await callback.answer("Project not found.")
        return

    text = f"Project: {project['name']}\nDescription: {project.get('description') or 'No description'}"
    await callback.message.edit_text(text, reply_markup=get_project_detail_keyboard(project_id))

@router.callback_query(F.data == "project_create")
async def start_project_creation(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Enter project name:")
    await state.set_state(ProjectStates.waiting_for_name)
    await callback.answer()

@router.message(ProjectStates.waiting_for_name)
async def process_project_name(message: types.Message, state: FSMContext, api_client: APIClient):
    name = message.text
    user_id = message.from_user.id

    try:
        await api_client.create_project(user_id, name)
        await message.answer(f"Project '{name}' created!")
        await state.clear()
        # Refresh list
        projects = await api_client.get_projects(user_id)
        await message.answer("Your Projects:", reply_markup=get_projects_keyboard(projects))
    except Exception:
        await message.answer("Failed to create project. Please try again.")

@router.callback_query(F.data.startswith("project_delete_"))
async def delete_project(callback: types.CallbackQuery, api_client: APIClient):
    project_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.delete_project(user_id, project_id)
        await callback.answer("Project deleted.")
        # Refresh list
        projects = await api_client.get_projects(user_id)
        await callback.message.edit_text("Your Projects:", reply_markup=get_projects_keyboard(projects))
    except Exception:
        await callback.answer("Failed to delete project.")
