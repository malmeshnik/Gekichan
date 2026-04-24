from aiogram import Router, types, F
from bot.services.api_client import APIClient
from bot.keyboards.focus import get_focus_keyboard, get_focus_resume_keyboard

router = Router()

@router.message(F.text == "Start Focus")
async def start_focus_general(message: types.Message, api_client: APIClient):
    user_id = message.from_user.id
    active_session = await api_client.get_active_session(user_id)

    if active_session:
        await message.answer(
            "You already have an active session",
            reply_markup=get_focus_keyboard(active_session['id'])
        )
        return

    try:
        session = await api_client.start_session(user_id)
        await message.answer(
            "Focus session started! Deep work mode ON. 🚀",
            reply_markup=get_focus_keyboard(session['id'])
        )
    except Exception:
        await message.answer("Failed to start focus session.")

@router.callback_query(F.data.startswith("focus_start_"))
async def start_focus_task(callback: types.CallbackQuery, api_client: APIClient):
    task_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    active_session = await api_client.get_active_session(user_id)
    if active_session:
        await callback.answer("You already have an active session", show_alert=True)
        return

    try:
        session = await api_client.start_session(user_id, task_id=task_id)
        await callback.message.answer(
            "Focus session started for task! 🚀",
            reply_markup=get_focus_keyboard(session['id'])
        )
        await callback.answer()
    except Exception:
        await callback.answer("Failed to start focus session.")

@router.callback_query(F.data.startswith("focus_pause_"))
async def pause_focus(callback: types.CallbackQuery, api_client: APIClient):
    session_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.pause_session(user_id, session_id)
        await callback.answer("Interruption logged!")
        await callback.message.edit_text(
            "Session paused (interruption logged). Tap Resume to continue.",
            reply_markup=get_focus_resume_keyboard(session_id)
        )
    except Exception:
        await callback.answer("Failed to pause session.")

@router.callback_query(F.data.startswith("focus_stop_"))
async def stop_focus(callback: types.CallbackQuery, api_client: APIClient):
    session_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.stop_session(user_id, session_id)
        await callback.answer("Focus session stopped!")
        await callback.message.edit_text("Great job! Focus session completed. 🏁")
    except Exception:
        await callback.answer("Failed to stop session.")
