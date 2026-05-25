import hashlib
import hmac
import json
import logging
import time
import urllib.parse
import httpx

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self, base_url: str, bot_token: str = None):
        self.base_url = base_url.rstrip("/")
        self.bot_token = bot_token
        self.tokens = {}  # {user_id: access_token}
        self.user_infos = {}  # {user_id: {first_name, ...}}

    def _generate_init_data(self, user_id: int, **kwargs) -> str:
        """Generates and signs init_data precisely matching the backend validation rules."""
        if not self.bot_token:
            raise ValueError("bot_token is required to generate init_data")

        # 1. Створюємо чистий словник користувача
        user_data = {
            "id": user_id,
            "first_name": kwargs.get("first_name", f"User_{user_id}"),
            "last_name": kwargs.get("last_name"),
            "username": kwargs.get("username"),
            "language_code": kwargs.get("language_code", "en"),
        }

        # 2. Перетворюємо в JSON-рядок БЕЗ пробілів та з ASCII-безпечним кодуванням.
        # Важливо: ensure_ascii=False може викликати проблеми при кодуванні в query string,
        # тому використовуємо стандартний компактний JSON.
        user_json = json.dumps(user_data, separators=(",", ":"), ensure_ascii=False)

        # 3. Готуємо сирі дані для підпису
        # Твій валідатор очікує ТІЛЬКИ ті поля, які прийшли. Якщо Mini App шле query_id,
        # а твій бот ні — це теж ок, головне, щоб вони були відсортовані.
        data = {
            "auth_date": str(int(time.time())),
            "user": user_json,
        }

        # Якщо бекенду раптом потрібен query_id, розкоментуй рядок нижче:
        # data["query_id"] = kwargs.get("query_id", "STUB_QUERY_ID")

        # 4. Сортуємо та збираємо data_check_string (hash сюди ЩЕ не входить)
        data_check_list = sorted(data.items())
        data_check_string = "\n".join([f"{k}={v}" for k, v in data_check_list])

        # 5. Рахуємо хеш точно так само, як на бекенді
        secret_key = hmac.new(
            b"WebAppData", self.bot_token.encode(), hashlib.sha256
        ).digest()
        calculated_hash = hmac.new(
            secret_key, data_check_string.encode(), hashlib.sha256
        ).hexdigest()

        # 6. Додаємо хеш до фінального словника
        data["hash"] = calculated_hash

        # 7. Кодуємо в URL-формат для відправки
        return urllib.parse.urlencode(data)

    async def _request(self, method: str, path: str, user_id: int = None, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"

        headers = kwargs.get("headers", {}).copy()
        other_kwargs = {k: v for k, v in kwargs.items() if k != "headers"}

        if user_id is not None:
            user_id = int(user_id)

        is_auth_request = path.strip("/").endswith("auth/telegram")
        token = self.tokens.get(user_id)

        if user_id and not token and not is_auth_request:
            logger.warning(f"No token for user {user_id}, re-authenticating...")
            await self.authenticate(user_id)
            token = self.tokens.get(user_id)

        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, **other_kwargs)

                if response.status_code == 401 and user_id and not is_auth_request:
                    logger.warning(f"Token expired for user {user_id}, re-authenticating...")
                    await self.authenticate(user_id)
                    token = self.tokens.get(user_id)
                    if token:
                        headers["Authorization"] = f"Bearer {token}"
                        response = await client.request(method, url, headers=headers, **other_kwargs)

                # Логуємо помилку 400 або будь-яку іншу невдалу відповідь ДО того, як впаде raise_for_status
                if response.is_error:
                    logger.error(
                        f"API Error Response | Method: {method} | URL: {url} | "
                        f"Status: {response.status_code} | Body: {response.text}"
                    )

                response.raise_for_status()

                if response.content:
                    return response.json()
                return None

            except httpx.HTTPStatusError as e:
                # Додатковий бекап-лог, якщо щось пішло не так всередині httpx
                logger.error(f"HTTP Status Error caught: {e.response.text}")
                raise e
            except Exception as e:
                logger.exception(f"Unexpected error during request to {url}: {e}")
                raise e

    async def authenticate(self, telegram_id: int, **kwargs):
        telegram_id = int(telegram_id)

        # Merge new info with existing one to not lose data on re-auth
        if telegram_id not in self.user_infos:
            self.user_infos[telegram_id] = {}

        self.user_infos[telegram_id].update({k: v for k, v in kwargs.items() if v is not None})

        init_data = self._generate_init_data(telegram_id, **self.user_infos[telegram_id])
        logger.info(f"Generated init_data: {init_data!r}")
        data = {"init_data": init_data}

        # Use full path to avoid redirection and 301 errors
        result = await self._request("POST", "/api/auth/telegram/", json=data)

        self.tokens[telegram_id] = result["access"]

        logger.info(f"Saved token for user {telegram_id}")

        return result.get("user", result)

    async def update_user(self, telegram_id: int, **kwargs):
        return await self._request(
            "PATCH", f"/api/users/{telegram_id}/", user_id=telegram_id, json=kwargs
        )

    async def get_projects(self, user_id: int):
        return await self._request("GET", "/api/projects/", user_id=user_id)

    async def get_project(self, user_id: int, project_id: str):
        return await self._request(
            "GET", f"/api/projects/{project_id}/", user_id=user_id
        )

    async def create_project(self, user_id: int, name: str, description: str = ""):
        data = {"name": name, "description": description, "owner": user_id}
        return await self._request("POST", "/api/projects/", user_id=user_id, json=data)

    async def delete_project(self, user_id: int, project_id: str):
        return await self._request(
            "DELETE", f"/api/projects/{project_id}/", user_id=user_id
        )

    async def add_project_member(
        self,
        user_id: int,
        project_id: str,
        member_username: str = None,
        member_id: int = None,
    ):
        data = {}
        if member_username:
            data["username"] = member_username
        if member_id:
            data["user_id"] = member_id
        return await self._request(
            "POST",
            f"/api/projects/{project_id}/add_member/",
            user_id=user_id,
            json=data,
        )

    async def get_project_productivity(self, user_id, project_id: str):

        return await self._request(
            method="GET",
            path=(f"/api/projects/" f"{project_id}/productivity/"),
            user_id=user_id,
        )

    async def get_tasks(self, user_id: int, **params):
        return await self._request("GET", "/api/tasks/", user_id=user_id, params=params)

    async def get_task(self, user_id: int, task_id: str):
        return await self._request("GET", f"/api/tasks/{task_id}/", user_id=user_id)

    async def create_task(
        self,
        user_id: int,
        title: str,
        project_id: str,
        deadline: str = None,
        priority: str = "medium",
        description: str = None,
        assignee: int = None,
    ):
        data = {
            "title": title,
            "project": project_id,
            "status": "todo",
            "priority": priority,
        }
        if description:
            data["description"] = description
        if assignee:
            data["assignee"] = assignee
        if deadline:
            data["deadline"] = deadline
        return await self._request("POST", "/api/tasks/", user_id=user_id, json=data)

    async def update_task(self, user_id: int, task_id: str, **kwargs):
        # Flatten nested fields if necessary
        data = kwargs.copy()
        if "assignee" in data and data["assignee"] is None:
            data["assignee"] = None

        return await self._request(
            "PATCH", f"/api/tasks/{task_id}/", user_id=user_id, json=data
        )

    async def delete_task(self, user_id: int, task_id: str):
        return await self._request("DELETE", f"/api/tasks/{task_id}/", user_id=user_id)

    async def add_attachment(
        self,
        user_id: int,
        task_id: str,
        file_id: str,
        name: str,
        mime_type: str,
        size: int,
    ):
        data = {
            "task": task_id,
            "telegram_file_id": file_id,
            "file_name": name,
            "mime_type": mime_type,
            "file_size": size,
        }
        return await self._request(
            "POST", "/api/attachments/", user_id=user_id, json=data
        )

    async def get_attachments(self, user_id: int, task_id: str):
        return await self._request(
            "GET", "/api/attachments/", user_id=user_id, params={"task": task_id}
        )

    async def get_active_session(self, user_id: int):
        # We can list sessions and find one without end_time,
        # or rely on the backend to fail if we try to start when one exists.
        # For UX, let's try to find an active one.
        sessions = await self._request("GET", "/api/sessions/", user_id=user_id)
        for s in sessions:
            if not s.get("end_time"):
                return s
        return None

    async def start_session(
        self, user_id: int, task_id: str = None, target_duration: int = None
    ):
        data = {}
        if task_id:
            data["task"] = task_id
        if target_duration:
            data["target_duration"] = target_duration
        return await self._request(
            "POST", "/api/sessions/start/", user_id=user_id, json=data
        )

    async def pause_session(self, user_id: int, session_id: str):
        return await self._request(
            "PATCH", f"/api/sessions/{session_id}/pause/", user_id=user_id
        )

    async def resume_session(self, user_id: int, session_id: str):
        return await self._request(
            "PATCH", f"/api/sessions/{session_id}/resume/", user_id=user_id
        )

    async def stop_session(self, user_id: int, session_id: str):
        return await self._request(
            "PATCH", f"/api/sessions/{session_id}/stop/", user_id=user_id
        )

    async def get_today_stats(self, user_id: int):
        return await self._request("GET", "/api/stats/today/", user_id=user_id)

    async def get_dashboard_stats(self, user_id: int):
        return await self._request("GET", "/api/stats/dashboard/", user_id=user_id)
