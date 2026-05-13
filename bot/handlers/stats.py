from aiogram import Router, types, F
from bot.services.api_client import APIClient
from bot.utils.filters import I18nTextFilter

router = Router()

from aiogram_i18n import I18nContext

@router.message(I18nTextFilter("menu-stats"))
async def show_dashboard(message: types.Message, api_client: APIClient, i18n: I18nContext):
    user_id = message.from_user.id
    try:
        stats = await api_client.get_today_stats(user_id)

        title = i18n.stats.daily.title()
        focus_label = i18n.stats.focus.label()
        tasks_label = i18n.stats.tasks.label()
        interr_label = i18n.stats.interruptions.label()

        text = (
            f"📊 <b>{title}:</b>\n"
            f"- {focus_label}: {stats.get('total_focus_time', 0) // 60}m\n"
            f"- {tasks_label}: {stats.get('completed_tasks_count', 0)}\n"
            f"- {interr_label}: {stats.get('interruptions_count', 0)}\n"
            f"- Score: {stats.get('productivity_score', 0)}"
        )
        await message.answer(text, parse_mode="HTML")
    except Exception:
        await message.answer(i18n.stats.fetch.failed())
