from typing import Any, Dict, Optional
from aiogram_i18n.managers import BaseManager
from bot.services.api_client import APIClient

class I18nManager(BaseManager):
    def __init__(self, api_client: APIClient, default_locale: str = "en"):
        self.api_client = api_client
        self.cache = {} # Simple in-memory cache {user_id: locale}
        super().__init__(default_locale=default_locale)

    async def get_locale(self, event_from_user: Any, api_client: APIClient) -> str:
        if not event_from_user:
            return self.default_locale

        user_id = event_from_user.id
        if user_id in self.cache:
            return self.cache[user_id]

        try:
            user_data = await api_client.authenticate(
                telegram_id=user_id,
                username=event_from_user.username,
                first_name=event_from_user.first_name,
                last_name=event_from_user.last_name,
                language_code=event_from_user.language_code
            )
            locale = user_data.get("language", event_from_user.language_code or self.default_locale)
            self.cache[user_id] = locale
            return locale
        except Exception:
            return event_from_user.language_code or self.default_locale

    async def set_locale(self, locale: str, event_from_user: Any, api_client: APIClient) -> None:
        if not event_from_user:
            return

        user_id = event_from_user.id
        await api_client.update_user(user_id, language=locale)
        self.cache[user_id] = locale
