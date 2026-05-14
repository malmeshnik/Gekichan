import logging
import time
import uuid
from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
from apps.core.logging.correlation import set_correlation_id

logger_handlers = logging.getLogger('handlers')
logger_callbacks = logging.getLogger('callbacks')
logger_bot = logging.getLogger('bot')

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        correlation_id = str(uuid.uuid4())
        set_correlation_id(correlation_id)

        start_time = time.time()

        user = data.get('event_from_user')
        user_info = f"User: {user.id} (@{user.username})" if user else "Unknown User"

        event_type = "unknown"
        logger = logger_bot

        if event.message:
            event_type = "Message"
            logger = logger_handlers
            text = event.message.text or "[non-text]"
            msg = f"{event_type} from {user_info}: {text}"
        elif event.callback_query:
            event_type = "Callback"
            logger = logger_callbacks
            data_str = event.callback_query.data
            msg = f"{event_type} from {user_info}: {data_str}"
        else:
            msg = f"Update type {type(event)} from {user_info}"

        try:
            result = await handler(event, data)
            duration = time.time() - start_time
            logger.info(f"{msg} | Processed in {duration:.3f}s")
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.exception(f"Error processing {msg} | Failed in {duration:.3f}s: {e}")
            raise
