from celery import result
import httpx
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.tokens = {}  # {user_id: access_token}

    async def _request(self, method: str, path: str, user_id: int = None, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"

        headers = kwargs.pop('headers', {})

        if user_id is not None:
            user_id = int(user_id)

        # НЕ робимо auth recursion
        is_auth_request = path.startswith("/api/auth/telegram/")

        token = self.tokens.get(user_id)

        if user_id and not token and not is_auth_request:
            logger.warning(f"No token for user {user_id}, re-authenticating...")
            await self.authenticate(user_id)
            token = self.tokens.get(user_id)

        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                **kwargs
            )

            response.raise_for_status()

            if response.content:
                return response.json()

            return None

    async def authenticate(self, telegram_id: int, **kwargs):
        telegram_id = int(telegram_id)

        data = {
            "telegram_id": telegram_id,
            **kwargs
        }

        result = await self._request(
            "POST",
            "/api/auth/telegram/",
            json=data
        )

        self.tokens[telegram_id] = result["access"]

        logger.info(f"Saved token for user {telegram_id}")

        return result.get("user", result)

    async def update_user(self, telegram_id: int, **kwargs):
        return await self._request("PATCH", f"/api/users/{telegram_id}/", user_id=telegram_id, json=kwargs)

    async def get_projects(self, user_id: int):
        return await self._request("GET", "/api/projects/", user_id=user_id)

    async def get_project(self, user_id: int, project_id: str):
        return await self._request("GET", f"/api/projects/{project_id}/", user_id=user_id)

    async def create_project(self, user_id: int, name: str, description: str = ""):
        data = {"name": name, "description": description, "owner": user_id}
        return await self._request("POST", "/api/projects/", user_id=user_id, json=data)

    async def delete_project(self, user_id: int, project_id: str):
        return await self._request("DELETE", f"/api/projects/{project_id}/", user_id=user_id)

    async def add_project_member(self, user_id: int, project_id: str, member_username: str = None, member_id: int = None):
        data = {}
        if member_username:
            data['username'] = member_username
        if member_id:
            data['user_id'] = member_id
        return await self._request("POST", f"/api/projects/{project_id}/add_member/", user_id=user_id, json=data)

    async def get_tasks(self, user_id: int, **params):
        return await self._request("GET", "/api/tasks/", user_id=user_id, params=params)

    async def get_task(self, user_id: int, task_id: str):
        return await self._request("GET", f"/api/tasks/{task_id}/", user_id=user_id)

    async def create_task(self, user_id: int, title: str, project_id: str, deadline: str = None, priority: str = "medium", description: str = None, assignee: int = None):
        data = {
            "title": title,
            "project": project_id,
            "status": "todo",
            "priority": priority
        }
        if description:
            data['description'] = description
        if assignee:
            data['assignee'] = assignee
        if deadline:
            data['deadline'] = deadline
        return await self._request("POST", "/api/tasks/", user_id=user_id, json=data)

    async def update_task(self, user_id: int, task_id: str, **kwargs):
        # Flatten nested fields if necessary
        data = kwargs.copy()
        if 'assignee' in data and data['assignee'] is None:
            data['assignee'] = None

        return await self._request("PATCH", f"/api/tasks/{task_id}/", user_id=user_id, json=data)

    async def delete_task(self, user_id: int, task_id: str):
        return await self._request("DELETE", f"/api/tasks/{task_id}/", user_id=user_id)

    async def add_attachment(self, user_id: int, task_id: str, file_id: str, name: str, mime_type: str, size: int):
        data = {
            "task": task_id,
            "telegram_file_id": file_id,
            "file_name": name,
            "mime_type": mime_type,
            "file_size": size
        }
        return await self._request("POST", "/api/attachments/", user_id=user_id, json=data)

    async def get_attachments(self, user_id: int, task_id: str):
        return await self._request("GET", "/api/attachments/", user_id=user_id, params={"task": task_id})

    async def get_active_session(self, user_id: int):
        # We can list sessions and find one without end_time,
        # or rely on the backend to fail if we try to start when one exists.
        # For UX, let's try to find an active one.
        sessions = await self._request("GET", "/api/sessions/", user_id=user_id)
        for s in sessions:
            if not s.get('end_time'):
                return s
        return None

    async def start_session(self, user_id: int, task_id: str = None, target_duration: int = None):
        data = {}
        if task_id:
            data['task'] = task_id
        if target_duration:
            data['target_duration'] = target_duration
        return await self._request("POST", "/api/sessions/start/", user_id=user_id, json=data)

    async def pause_session(self, user_id: int, session_id: str):
        return await self._request("PATCH", f"/api/sessions/{session_id}/pause/", user_id=user_id)

    async def resume_session(self, user_id: int, session_id: str):
        return await self._request("PATCH", f"/api/sessions/{session_id}/resume/", user_id=user_id)

    async def stop_session(self, user_id: int, session_id: str):
        return await self._request("PATCH", f"/api/sessions/{session_id}/stop/", user_id=user_id)

    async def get_today_stats(self, user_id: int):
        return await self._request("GET", "/api/stats/today/", user_id=user_id)

    async def get_dashboard_stats(self, user_id: int):
        return await self._request("GET", "/api/stats/dashboard/", user_id=user_id)
