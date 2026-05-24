import json
import hmac
import hashlib
from datetime import datetime
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User

class TelegramAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.bot_token = "12345678:ABCDEF-GHIJKL"
        self.url = reverse('telegram_auth')

    def generate_init_data(self, user_id, first_name):
        user = {
            "id": user_id,
            "first_name": first_name,
            "username": f"user_{user_id}",
            "language_code": "uk"
        }
        auth_date = int(datetime.now().timestamp())
        parsed_data = {
            "auth_date": str(auth_date),
            "user": json.dumps(user, separators=(',', ':'))
        }

        data_check_list = sorted(parsed_data.items())
        data_check_string = "\n".join([f"{k}={v}" for k, v in data_check_list])

        secret_key = hmac.new(b"WebAppData", self.bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        return f"{data_check_string}&hash={calculated_hash}".replace("\n", "&")

    @override_settings(TELEGRAM_BOT_TOKEN="12345678:ABCDEF-GHIJKL", DEBUG=False)
    def test_valid_init_data(self):
        init_data = self.generate_init_data(12345, "Ivan")
        response = self.client.post(self.url, {"init_data": init_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['id'], 12345)
        self.assertEqual(response.data['user']['first_name'], "Ivan")
        self.assertTrue(User.objects.filter(id=12345).exists())

    @override_settings(TELEGRAM_BOT_TOKEN="12345678:ABCDEF-GHIJKL", DEBUG=False)
    def test_invalid_init_data(self):
        response = self.client.post(self.url, {"init_data": "invalid"})
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)
    def test_debug_fallback(self):
        response = self.client.post(self.url, {"telegram_id": 999, "first_name": "Dev"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['id'], 999)

    @override_settings(TELEGRAM_BOT_TOKEN="12345678:ABCDEF-GHIJKL", DEBUG=False)
    def test_user_update(self):
        User.objects.create(id=555, first_name="OldName")
        init_data = self.generate_init_data(555, "NewName")
        response = self.client.post(self.url, {"init_data": init_data})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['first_name'], "NewName")
        self.assertEqual(User.objects.get(id=555).first_name, "NewName")
