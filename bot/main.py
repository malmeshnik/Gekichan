import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from bot.handlers import start, projects, tasks, focus, stats, settings
from bot.handlers.project.productivity import router as analytics_router
from bot.services.api_client import APIClient
from bot.services.i18n_manager import I18nManager
from bot.middlewares.logging import LoggingMiddleware as BotLoggingMiddleware
from apps.core.logging.config import get_logging_config
from apps.core.logging.hooks import setup_exception_hooks
import logging.config

async def main():
    # Initialize logging
    logging_config = get_logging_config(is_bot=True)
    logging.config.dictConfig(logging_config)

    # Setup exception hooks
    asyncio_handler = setup_exception_hooks()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(asyncio_handler)

    logger = logging.getLogger("bot")
    logger.info("Starting bot...")

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    api_url = os.getenv("API_BASE_URL", "http://backend:8000")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    api_client = APIClient(base_url=api_url)

    i18n_middleware = I18nMiddleware(
        core=FluentRuntimeCore(
            path="bot/locales",
            default_locale="en",
        ),
        manager=I18nManager(api_client=api_client)
    )

    i18n_middleware.setup(dp)

    # Register logging middleware
    dp.update.outer_middleware(BotLoggingMiddleware())

    # Register handlers and inject api_client
    dp.include_router(start.router)
    dp.include_router(projects.router)
    dp.include_router(tasks.router)
    dp.include_router(focus.router)
    dp.include_router(stats.router)
    dp.include_router(settings.router)
    dp.include_router(analytics_router)

    # Inject api_client into all handlers
    await dp.start_polling(bot, api_client=api_client)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
