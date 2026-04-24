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
        if user_id and user_id in self.tokens:
            headers['Authorization'] = f"Bearer {self.tokens[user_id]}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                raise

    async def authenticate(self, telegram_id: int):
        data = {"telegram_id": telegram_id}
        result = await self._request("POST", "/api/auth/telegram/", json=data)
        self.tokens[telegram_id] = result['access']
        return result

    async def get_projects(self, user_id: int):
        return await self._request("GET", "/api/projects/", user_id=user_id)

    async def create_project(self, user_id: int, name: str, description: str = ""):
        data = {"name": name, "description": description, "owner": user_id}
        return await self._request("POST", "/api/projects/", user_id=user_id, json=data)

    async def delete_project(self, user_id: int, project_id: str):
        return await self._request("DELETE", f"/api/projects/{project_id}/", user_id=user_id)

    async def get_tasks(self, user_id: int, project_id: str = None):
        params = {}
        if project_id:
            params['project'] = project_id
        return await self._request("GET", "/api/tasks/", user_id=user_id, params=params)

    async def create_task(self, user_id: int, title: str, project_id: str, deadline: str = None):
        data = {
            "title": title,
            "project": project_id,
            "assignee": user_id,
            "status": "todo"
        }
        if deadline:
            data['deadline'] = deadline
        return await self._request("POST", "/api/tasks/", user_id=user_id, json=data)

    async def update_task_status(self, user_id: int, task_id: str, status: str):
        data = {"status": status}
        return await self._request("PATCH", f"/api/tasks/{task_id}/", user_id=user_id, json=data)

    async def get_active_session(self, user_id: int):
        # We can list sessions and find one without end_time,
        # or rely on the backend to fail if we try to start when one exists.
        # For UX, let's try to find an active one.
        sessions = await self._request("GET", "/api/sessions/", user_id=user_id)
        for s in sessions:
            if not s.get('end_time'):
                return s
        return None

    async def start_session(self, user_id: int, task_id: str = None):
        data = {}
        if task_id:
            data['task'] = task_id
        return await self._request("POST", "/api/sessions/start/", user_id=user_id, json=data)

    async def pause_session(self, user_id: int, session_id: str):
        return await self._request("PATCH", f"/api/sessions/{session_id}/pause/", user_id=user_id)

    async def stop_session(self, user_id: int, session_id: str):
        return await self._request("PATCH", f"/api/sessions/{session_id}/stop/", user_id=user_id)

    async def get_today_stats(self, user_id: int):
        return await self._request("GET", "/api/stats/today/", user_id=user_id)

    async def get_dashboard_stats(self, user_id: int):
        return await self._request("GET", "/api/stats/dashboard/", user_id=user_id)
