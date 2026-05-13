from typing import Any, Union, Dict
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram_i18n import I18nContext

class I18nTextFilter(Filter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: Message, i18n: I18nContext) -> Union[bool, Dict[str, Any]]:
        # This is a bit expensive but robust
        localized_text = i18n.get(self.key)
        return message.text == localized_text
