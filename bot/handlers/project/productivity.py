from aiogram import Router, F
from aiogram.types import CallbackQuery

from bot.services.api_client import APIClient
from bot.utils.navigation import safe_edit_or_answer
from bot.utils.renderers import ProductivityAnalyticsRenderer

from bot.keyboards.projects import project_analytics_keyboard
from bot.utils.callbacks import AnalyticsPeriodCb

router = Router()


@router.callback_query(AnalyticsPeriodCb.filter())
async def productivity_handler(callback: CallbackQuery, api_client: APIClient, i18n, callback_data: AnalyticsPeriodCb):

    await callback.answer(i18n.analytics.loading())

    project_id = callback_data.project_id
    period = callback_data.period
    user_id = callback.message.chat.id

    stats = await api_client.get_project_productivity(user_id, project_id)

    text = ProductivityAnalyticsRenderer.render(stats, i18n)

    await safe_edit_or_answer(
        event=callback,
        text=text,
        reply_markup=project_analytics_keyboard(project_id, i18n),
    )
