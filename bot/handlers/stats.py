from aiogram import Router, types, F
from bot.services.api_client import APIClient

router = Router()

@router.message(F.text == "Dashboard")
async def show_dashboard(message: types.Message, api_client: APIClient):
    user_id = message.from_user.id
    try:
        stats = await api_client.get_today_stats(user_id)
        # focus_time is in seconds (DurationField in Django usually returns string or seconds depending on serializer)
        # Let's assume it's formatted by serializer or we handle it.
        # Looking at backend analytics/views.py, it aggregates Sum('duration')

        text = (
            "📊 **Today's Dashboard**\n\n"
            f"⏱ Focus Time: {stats.get('total_focus_time')}\n"
            f"✅ Tasks Completed: {stats.get('completed_tasks_count')}\n"
            f"⚠️ Interruptions: {stats.get('interruptions_count')}"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception:
        await message.answer("Failed to fetch dashboard stats.")

@router.message(F.text == "Stats")
async def show_stats(message: types.Message, api_client: APIClient):
    user_id = message.from_user.id
    try:
        data = await api_client.get_dashboard_stats(user_id)
        last_7 = data.get('last_7_days', [])

        text = "📈 **Historical Stats (Last 7 Days)**\n\n"
        for day in last_7:
            text += f"📅 {day['date']}: {day['focus_time']} focus, {day['tasks_done']} tasks\n"

        await message.answer(text, parse_mode="Markdown")
    except Exception:
        await message.answer("Failed to fetch historical stats.")
