from aiogram import Router, types, F
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.keyboards.focus import (
    get_focus_keyboard, get_focus_resume_keyboard,
    get_timer_options_keyboard
)
from bot.utils.filters import I18nTextFilter

router = Router()

@router.message(F.command("focus"))
@router.message(I18nTextFilter("menu-focus"))
async def start_focus_general(message: types.Message, api_client: APIClient, i18n: I18nContext):
    user_id = message.from_user.id
    active_session = await api_client.get_active_session(user_id)

    if active_session:
        await message.answer(
            i18n.timer.active_error(),
            reply_markup=get_focus_keyboard(active_session['id'], i18n)
        )
        return

    await message.answer(
        i18n.timer.mode_select(),
        reply_markup=get_timer_options_keyboard(None, i18n)
    )

@router.callback_query(F.data.startswith("timer_start_"))
async def start_timer_callback(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    parts = callback.data.split("_")
    task_id = parts[2] if parts[2] != "None" else None
    duration = int(parts[3])
    user_id = callback.from_user.id

    try:
        session = await api_client.start_session(user_id, task_id=task_id, target_duration=duration if duration > 0 else None)
        await callback.message.edit_text(
            i18n.timer.started_msg(),
            reply_markup=get_focus_keyboard(session['id'], i18n)
        )
    except Exception:
        await callback.answer(i18n.timer.start_failed())

@router.callback_query(F.data.startswith("focus_pause_"))
async def pause_focus(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    session_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.pause_session(user_id, session_id)
        await callback.answer(i18n.timer.paused_confirm())
        await callback.message.edit_text(
            i18n.timer.paused_msg(),
            reply_markup=get_focus_resume_keyboard(session_id, i18n)
        )
    except Exception:
        await callback.answer(i18n.timer.pause_failed())

@router.callback_query(F.data.startswith("focus_resume_"))
async def resume_focus(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    session_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.resume_session(user_id, session_id)
        await callback.answer(i18n.timer.resumed_confirm())
        await callback.message.edit_text(
            i18n.timer.active_msg(),
            reply_markup=get_focus_keyboard(session_id, i18n)
        )
    except Exception:
        await callback.answer(i18n.timer.resume_failed())

@router.callback_query(F.data.startswith("focus_stop_"))
async def stop_focus(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    session_id = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    try:
        await api_client.stop_session(user_id, session_id)
        await callback.answer(i18n.timer.stopped_confirm())
        await callback.message.edit_text(i18n.timer.stopped_msg())
    except Exception:
        await callback.answer(i18n.timer.stop_failed())

@router.callback_query(F.data.startswith("task_done_"))
async def timer_task_done(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    parts = callback.data.split("_")
    task_id = parts[2]
    session_id = parts[3]
    user_id = callback.from_user.id

    try:
        # 1. Stop session if active
        await api_client.stop_session(user_id, session_id)
        # 2. Mark task as done
        if task_id != "None":
            await api_client.update_task(user_id, task_id, status="done")

        await callback.answer(i18n.timer.task_done())
        await callback.message.edit_text(i18n.timer.stopped_msg() + " ✅")
    except Exception:
        await callback.answer(i18n.get("tasks-status-update-failed"))

@router.callback_query(F.data.startswith("timer_resume_"))
async def timer_resume_action(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    parts = callback.data.split("_")
    task_id = parts[2]
    session_id = parts[3]
    user_id = callback.from_user.id

    try:
        # For "Continue", we just start a new stopwatch session linked to the same task
        session = await api_client.start_session(user_id, task_id=None if task_id == "None" else task_id)
        await callback.answer(i18n.timer.resumed_confirm())
        await callback.message.edit_text(
            i18n.timer.active_msg(),
            reply_markup=get_focus_keyboard(session['id'], i18n)
        )
    except Exception:
        await callback.answer(i18n.timer.start_failed())

@router.callback_query(F.data.startswith("timer_more_"))
async def timer_more_action(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext):
    parts = callback.data.split("_")
    task_id = parts[2]
    user_id = callback.from_user.id

    # Show duration options again
    await callback.message.edit_text(
        i18n.timer.mode_select(),
        reply_markup=get_timer_options_keyboard(task_id, i18n)
    )
    await callback.answer()
