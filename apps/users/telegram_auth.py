import hashlib
import hmac
import json
import time
import urllib.parse
from django.conf import settings

def validate_telegram_data(init_data: str) -> dict | None:
    """
    Validates the data received from the Telegram Mini App.
    Returns the parsed user data if valid, None otherwise.
    """
    if not init_data:
        return None

    try:
        parsed_data = dict(urllib.parse.parse_qsl(init_data))
        if "hash" not in parsed_data:
            return None

        received_hash = parsed_data.pop("hash")

        # Sort keys alphabetically
        data_check_list = sorted(parsed_data.items())
        data_check_string = "\n".join([f"{k}={v}" for k, v in data_check_list])

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

        if calculated_hash == received_hash:
            # Check auth_date (max 24 hours old)
            auth_date = int(parsed_data.get("auth_date", 0))
            if time.time() - auth_date > 86400:
                return None

            # Data is valid, parse the 'user' field
            user_data = json.loads(parsed_data.get("user", "{}"))
            return user_data

    except Exception:
        return None

    return None
