import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import start, projects, tasks, focus, stats
from bot.services.api_client import APIClient

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    api_url = os.getenv("API_BASE_URL", "http://backend:8000")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is not set")

    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())

    api_client = APIClient(base_url=api_url)

    # Register handlers and inject api_client
    dp.include_router(start.router)
    dp.include_router(projects.router)
    dp.include_router(tasks.router)
    dp.include_router(focus.router)
    dp.include_router(stats.router)

    # Inject api_client into all handlers
    await dp.start_polling(bot, api_client=api_client)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
