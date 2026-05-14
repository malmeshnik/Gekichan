from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from bot.services.api_client import APIClient
from bot.keyboards.focus import (
    get_focus_keyboard, get_focus_resume_keyboard,
    get_timer_options_keyboard, get_post_timer_keyboard,
    get_add_time_keyboard
)
from bot.utils.filters import I18nTextFilter
from bot.utils.navigation import safe_edit_or_answer
from bot.states.task_states import TaskStates
from bot.utils.callbacks import (
    FocusActionCb,
    FocusStartCb,
    TimerStartCb,
    FocusPostTimerCb,
    TimerAddCb,
    TaskViewCb,
)

router = Router()

@router.message(F.command("focus"))
@router.message(I18nTextFilter("menu-focus"))
async def start_focus_general(message: types.Message, api_client: APIClient, i18n: I18nContext):
    user_id = message.from_user.id
    active_session = await api_client.get_active_session(user_id)
    if active_session:
        await message.answer(i18n.get("timer-active-error"), reply_markup=get_focus_keyboard(active_session['id'], i18n))
        return
    await message.answer(i18n.get("timer-mode-select"), reply_markup=get_timer_options_keyboard(None, i18n))

@router.callback_query(FocusStartCb.filter())
async def start_focus_from_task(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: FocusStartCb):
    task_id = callback_data.task_id
    await start_timer_callback_logic(callback, api_client, i18n, task_id, 1500)

@router.callback_query(TimerStartCb.filter())
async def start_timer_callback(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: TimerStartCb):
    task_id = callback_data.task_id
    duration = callback_data.duration
    await start_timer_callback_logic(callback, api_client, i18n, task_id, duration)

async def start_timer_callback_logic(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, task_id: str = None, duration: int = 0):
    user_id = callback.from_user.id
    try:
        session = await api_client.start_session(user_id, task_id=task_id, target_duration=duration if duration > 0 else None)
        await safe_edit_or_answer(callback, i18n.get("timer-started-msg"), reply_markup=get_focus_keyboard(session['id'], i18n))
    except Exception:
        await callback.answer(i18n.get("timer-start-failed"))

@router.callback_query(FocusActionCb.filter(F.action == "p"))
async def pause_focus(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: FocusActionCb):
    session_id = callback_data.id
    user_id = callback.from_user.id
    try:
        await api_client.pause_session(user_id, session_id)
        await callback.answer(i18n.get("timer-paused-confirm"))
        await safe_edit_or_answer(callback, i18n.get("timer-paused-msg"), reply_markup=get_focus_resume_keyboard(session_id, i18n))
    except Exception:
        await callback.answer(i18n.get("timer-pause-failed"))

@router.callback_query(FocusActionCb.filter(F.action == "r"))
async def resume_focus(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: FocusActionCb):
    session_id = callback_data.id
    user_id = callback.from_user.id
    try:
        await api_client.resume_session(user_id, session_id)
        await callback.answer(i18n.get("timer-resumed-confirm"))
        await safe_edit_or_answer(callback, i18n.get("timer-active-msg"), reply_markup=get_focus_keyboard(session_id, i18n))
    except Exception:
        await callback.answer(i18n.get("timer-resume-failed"))

@router.callback_query(FocusActionCb.filter(F.action == "ref"))
async def refresh_focus(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: FocusActionCb):
    session_id = callback_data.id
    user_id = callback.from_user.id
    try:
        session = await api_client._request("GET", f"/api/sessions/{session_id}/", user_id=user_id)
        # Calculate elapsed time
        import datetime
        start_time = datetime.datetime.fromisoformat(session['start_time'].replace("Z", "+00:00"))
        now = datetime.datetime.now(datetime.timezone.utc)
        elapsed = int((now - start_time).total_seconds()) - session.get('total_paused_duration', 0)

        from bot.utils.renderers import format_duration
        elapsed_str = format_duration(elapsed)

        text = f"{i18n.get('timer-active-msg')}\n\n⏱ {i18n.get('timer-duration', duration=elapsed_str)}"

        await safe_edit_or_answer(callback, text, reply_markup=get_focus_keyboard(session_id, i18n))
        await callback.answer(i18n.get("timer-resumed-confirm")) # Generic success
    except Exception:
        await callback.answer(i18n.get("timer-fetch-failed"))


@router.callback_query(FocusActionCb.filter(F.action == "s"))
async def stop_focus(callback: types.CallbackQuery, state: FSMContext, api_client: APIClient, i18n: I18nContext, callback_data: FocusActionCb):
    session_id = callback_data.id
    user_id = callback.from_user.id
    try:
        # Reset FSM state
        await state.clear()

        session = await api_client.stop_session(user_id, session_id)
        task_id = session.get('task')

        from bot.utils.renderers import format_duration
        duration_str = format_duration(session.get('duration', 0))

        # Fetch today's stats for more detail
        stats = await api_client._request("GET", "/api/productivity/", user_id=user_id, params={"period": "day"})

        project_str = i18n.get("tasks-hub-no-project")
        if session.get('task'):
            task = await api_client.get_task(user_id, session['task'])
            if task.get('project_name'):
                project_str = task['project_name']

        text = (
            f"<b>{i18n.get('timer-finished-title')}</b>\n\n"
            f"{i18n.get('timer-duration', duration=duration_str)}\n"
            f"{i18n.get('projects-label')}: {project_str}\n"
            f"{i18n.get('analytics-focus-today')}: {format_duration(stats.get('focus_today_seconds', 0))}\n"
            f"{i18n.get('timer-productivity-updated')}: {session.get('productivity_score', 0)}"
        )

        await callback.answer(i18n.get("timer-stopped-confirm"))
        await callback.message.edit_text(text, reply_markup=get_post_timer_keyboard(task_id, i18n, session_id), parse_mode="HTML")
    except Exception:
        await callback.answer(i18n.get("timer-stop-failed"))

@router.callback_query(FocusPostTimerCb.filter(F.action == "d"))
async def timer_task_done(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: FocusPostTimerCb):
    task_id = callback_data.id
    user_id = callback.from_user.id
    try:
        if task_id:
            await api_client.update_task(user_id, task_id, status="done")
        await callback.answer(i18n.get("timer-task-done"))
        await callback.message.edit_text(i18n.get("timer-stopped-msg") + " ✅")
    except Exception:
        await callback.answer(i18n.get("tasks-status-update-failed"))

@router.callback_query(FocusPostTimerCb.filter(F.action == "c"))
async def timer_resume_action(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: FocusPostTimerCb):
    task_id = callback_data.id
    user_id = callback.from_user.id
    try:
        session = await api_client.start_session(user_id, task_id=task_id)
        await callback.answer(i18n.get("timer-resumed-confirm"))
        await callback.message.edit_text(i18n.get("timer-active-msg"), reply_markup=get_focus_keyboard(session['id'], i18n))
    except Exception:
        await callback.answer(i18n.get("timer-start-failed"))

@router.callback_query(FocusPostTimerCb.filter(F.action == "m"))
async def timer_more_action(callback: types.CallbackQuery, i18n: I18nContext, callback_data: FocusPostTimerCb):
    task_id = callback_data.id
    await callback.message.edit_text(i18n.get("timer-need-more"), reply_markup=get_add_time_keyboard(task_id, i18n))
    await callback.answer()

@router.callback_query(TimerAddCb.filter())
async def add_time_action(callback: types.CallbackQuery, state: FSMContext, api_client: APIClient, i18n: I18nContext, callback_data: TimerAddCb):
    task_id = callback_data.task_id
    seconds = callback_data.seconds
    if seconds == "custom":
        await state.update_data(add_time_task_id=task_id)
        await state.set_state(TaskStates.waiting_for_add_time_custom)
        await callback.message.answer(i18n.get("timer-enter-custom-minutes"))
        await callback.answer()
        return
    await start_timer_callback_logic(callback, api_client, i18n, task_id=task_id, duration=int(seconds))
    await callback.answer()

@router.message(TaskStates.waiting_for_add_time_custom)
async def process_add_time_custom(message: types.Message, state: FSMContext, api_client: APIClient, i18n: I18nContext):
    try:
        minutes = int(message.text)
        data = await state.get_data()
        task_id = data.get('add_time_task_id')
        await state.clear()
        session = await api_client.start_session(message.from_user.id, task_id=task_id, target_duration=minutes * 60)
        await message.answer(i18n.get("timer-started-msg"), reply_markup=get_focus_keyboard(session['id'], i18n))
    except ValueError:
        await message.answer(i18n.get("timer-invalid-minutes"))

@router.callback_query(FocusActionCb.filter(F.action == "b"))
async def take_break(callback: types.CallbackQuery, i18n: I18nContext):
    await callback.message.edit_text(i18n.get("timer-break-msg"))
    await callback.answer()
