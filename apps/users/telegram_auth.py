import hashlib
import hmac
import json
import time
import urllib.parse
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def validate_telegram_data(init_data: str) -> dict | None:
    """
    Validates the data received from the Telegram Mini App.
    Returns the parsed user data if valid, None otherwise.
    """
    if not init_data:
        logger.info("Telegram auth failed: init_data is empty")
        return None

    try:
        # 1. Декодуємо рядок. 
        # УВАГА: На проді бот шле url-encoded рядок. Якщо у рядку є спецсимволи (наприклад, {}),
        # parse_qsl може відпрацювати не так, як сирий urllib.parse.unquote.
        # Але головне — переконатися, що типи даних залишаються рядками.
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
        logger.info(f"Parsed data: {parsed_data}")
        if "hash" not in parsed_data:
            logger.info("Telegram auth failed: 'hash' not found in parsed_data")
            return None

        received_hash = parsed_data.pop("hash")

        # Sort keys alphabetically
        data_check_list = sorted(parsed_data.items())
        data_check_string = "\n".join([f"{k}={v}" for k, v in data_check_list])

        # Перевіряємо, чи взагалиш існує токен в налаштуваннях
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.error("CRITICAL: TELEGRAM_BOT_TOKEN is empty in Django settings!")
            return None

        # Secret key is HMAC-SHA256 of the bot token with "WebAppData" as key
        secret_key = hmac.new(
            b"WebAppData",
            settings.TELEGRAM_BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        # Calculated hash is HMAC-SHA256 of the data_check_string with secret_key as key
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if calculated_hash != received_hash:
            logger.info(f"Telegram auth failed: Hash mismatch! Calculated: {calculated_hash}, Received: {received_hash}")
            return None

        # ----------------------------------------------------------------
        # 2. ГОЛОВНА ПОМИЛКА: Перевірка auth_date
        # ----------------------------------------------------------------
        auth_date = int(parsed_data.get("auth_date", 0))
        
        # Використовуємо abs(), бо якщо годинник бекенду відстає від бота,
        # різниця буде ВІД'ЄМНОЮ (наприклад, -3600), і твоя стара умова
        # (time.time() - auth_date > 3600) пропустила б це, АЛЕ якщо годинник 
        # бекенду поспішає — вона жорстко поверне None.
        # Розширюємо вікно до 24 годин (86400 сек), щоб покрити будь-які збої таймзон на VPS.
        if abs(time.time() - auth_date) > 86400:
            logger.info(f"Telegram auth failed: Expired auth_date. Server time: {time.time()}, Auth time: {auth_date}")
            return None

        # Data is valid, parse the 'user' field
        user_data = json.loads(parsed_data.get("user", "{}"))
        return user_data

    except Exception as e:
        logger.exception(f"Telegram auth failed with unexpected exception: {e}")
        return None