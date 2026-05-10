from typing import List, Dict, Any
from aiogram_i18n import I18nContext

class UIRenderer:
    @staticmethod
    def render_breadcrumbs(path: List[str]) -> str:
        return " > ".join(path)

    @staticmethod
    def render_project_list_item(project: Dict[str, Any], index: int, i18n: I18nContext) -> str:
        name = project.get('name', 'Unnamed')
        members = project.get('members_count', 0)
        tasks = project.get('tasks_count', 0)
        overdue = project.get('overdue_tasks_count', 0)

        number_emoji = f"{index}️⃣" if index <= 10 else f"{index}."

        summary = i18n.get("projects-summary", members=members, tasks=tasks, overdue=overdue)
        return f"{number_emoji} {name}\n{summary}\n"

    @staticmethod
    def render_project_dashboard(project: Dict[str, Any], stats: Dict[str, Any], i18n: I18nContext) -> str:
        name = project.get('name', 'Unnamed')
        desc = project.get('description') or ""

        # We need to fetch more detailed stats for the dashboard
        # Assuming stats contains: members_total, members_active, tasks_total,
        # tasks_in_progress, tasks_overdue, tasks_done, focus_time, last_activity

        lines = [
            f"📁 <b>{name}</b>",
            f"\n{desc}" if desc else "",
            f"\n{i18n.get('project-dashboard-members', total=stats.get('members_total', 0))}",
            f"{i18n.get('project-dashboard-active', active=stats.get('members_active', 0))}",
            f"\n{i18n.get('project-dashboard-tasks', total=stats.get('tasks_total', 0))}",
            f"{i18n.get('project-dashboard-in-progress', count=stats.get('tasks_in_progress', 0))}",
            f"{i18n.get('project-dashboard-overdue', count=stats.get('tasks_overdue', 0))}",
            f"{i18n.get('project-dashboard-done', count=stats.get('tasks_done', 0))}",
            f"\n{i18n.get('project-dashboard-focus', time=stats.get('focus_time', '0h'))}",
            f"\n{i18n.get('project-dashboard-activity', time=stats.get('last_activity', 'unknown'))}"
        ]
        return "\n".join(filter(None, lines))

    @staticmethod
    def render_task_card(task: Dict[str, Any], i18n: I18nContext) -> str:
        title = task.get('title', 'No title')
        assignee = task.get('assignee_name') or "Unassigned"
        deadline = task.get('deadline') or "No deadline"
        priority = task.get('priority', 'medium')
        attachments = task.get('attachment_count', 0)
        focus_time = task.get('focus_time_total', 0)

        # Format focus time (seconds to Hh Mm)
        hours = int(focus_time // 3600)
        minutes = int((focus_time % 3600) // 60)
        focus_str = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

        lines = [
            f"📝 <b>{title}</b>",
            i18n.get("task-card-assignee", name=assignee),
            i18n.get("task-card-deadline", date=deadline) if task.get('deadline') else "",
            i18n.get("task-card-priority", priority=priority),
            i18n.get("task-card-attachments", count=attachments) if attachments > 0 else "",
            i18n.get("task-card-focus", time=focus_str) if focus_time > 0 else ""
        ]
        return "\n".join(filter(None, lines))
