from aiogram import Router, types, F

from bot.utils.navigation import safe_edit_or_answer
from bot.services.api_client import APIClient
from bot.utils.filters import I18nTextFilter
from bot.utils.callbacks import AnalyticsPeriodCb, ProjectViewCb

router = Router()

from aiogram_i18n import I18nContext

@router.message(I18nTextFilter("menu-stats"))
async def show_dashboard(message: types.Message, api_client: APIClient, i18n: I18nContext):
    await show_productivity_analytics(message, api_client, i18n)


async def show_productivity_analytics(
    union: [types.Message, types.CallbackQuery],
    api_client: APIClient,
    i18n: I18nContext,
    project_id: str = None,
    period: str = "day"
):
    user_id = union.from_user.id
    try:
        if project_id:
            stats = await api_client._request(
                "GET", f"/api/projects/{project_id}/productivity/", user_id=user_id, params={"period": period}
            )
        else:
            stats = await api_client._request(
                "GET", "/api/productivity/", user_id=user_id, params={"period": period}
            )

        from bot.utils.renderers import format_duration

        # Format stats for rendering
        formatted_stats = {
            "tasks_delta_percent": stats.get("tasks_delta_percent", 0),
            "tasks_created_today": stats.get("tasks_created_today", 0),
            "tasks_completed_today": stats.get("tasks_completed_today", 0),
            "overdue_tasks": stats.get("overdue_tasks", 0),
            "completion_rate": stats.get("completion_rate", 0),
            "focus_today_seconds": stats.get("focus_today_seconds", 0),
            "focus_yesterday_seconds": stats.get("focus_yesterday_seconds", 0),
            "best_focus_duration_seconds": stats.get("best_focus_duration_seconds", 0),
            "average_focus_session_seconds": stats.get("average_focus_session_seconds", 0),
            "top_member_username": stats.get("top_member_username"),
            "top_member_tasks": stats.get("top_member_tasks", 0),
            "leaderboard": stats.get("leaderboard", []),
            "active_members_count": stats.get("active_members_count", 0),
            "ai_insight": stats.get("ai_insight"),
        }

        from bot.utils.renderers import ProductivityAnalyticsRenderer
        text = ProductivityAnalyticsRenderer.render(formatted_stats, i18n)

        from bot.utils.keyboards import get_analytics_period_keyboard
        reply_markup = get_analytics_period_keyboard(i18n, project_id)

        await safe_edit_or_answer(union, text, reply_markup=reply_markup)

    except Exception as e:
        import logging
        logging.error(f"Error fetching analytics: {e}")
        await safe_edit_or_answer(union, i18n.stats.fetch.failed())


@router.callback_query(AnalyticsPeriodCb.filter())
async def analytics_period_callback(callback: types.CallbackQuery, api_client: APIClient, i18n: I18nContext, callback_data: AnalyticsPeriodCb):
    period = callback_data.period
    project_id = callback_data.project_id
    await show_productivity_analytics(callback, api_client, i18n, project_id=project_id, period=period)
    await callback.answer()
