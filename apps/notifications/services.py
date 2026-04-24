import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def send_telegram_message(user_id, text):
    """
    Sends a message to a Telegram user using the Telegram Bot API.
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN is not set.")
        return False

    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": user_id,
        "text": text,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        logger.error(f"Error sending Telegram message to {user_id}: {e}")
        if hasattr(e, 'response') and e.response is not None:
             logger.error(f"Response: {e.response.text}")
        return False
