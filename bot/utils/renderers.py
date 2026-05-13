import math
from typing import List, Dict, Any
from aiogram_i18n import I18nContext


def get_priority_emoji(priority: str) -> str:
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪️")


def get_status_emoji(status: str) -> str:
    return {"todo": "📌", "in_progress": "🔥", "done": "✅"}.get(status, "📝")


def get_random_emoji(user_id: int) -> str:
    emojis = ["🦊", "🐼", "🦉", "🦁", "🐯", "🐱", "🐨", "🐰", "🐻", "🐶"]
    return emojis[user_id % len(emojis)]


def render_project_list(
    projects: List[Dict[str, Any]], i18n: I18nContext, page: int = 1, page_size: int = 5
) -> str:
    if not projects:
        return i18n.get("projects-empty")

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    current_projects = projects[start_idx:end_idx]

    lines = [f"📁 <b>{i18n.get('projects-list-title')}</b>\n"]
    for i, p in enumerate(current_projects, start_idx + 1):
        overdue = p.get("overdue_tasks_count", 0)
        overdue_str = (
            f" ⚠️ {overdue} {i18n.get('projects-overdue')}" if overdue > 0 else ""
        )
        line = (
            f"{i}️⃣ <b>{p['name']}</b> 👥 {p.get('members_count', 0)} "
            f"📝 {p.get('tasks_count', 0)}{overdue_str}"
        )
        lines.append(line)

    return "\n".join(lines)


def format_timeago(timestamp: str, i18n: I18nContext) -> str:
    if not timestamp:
        return i18n.get("common-never")

    import datetime

    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return timestamp

    diff = now - dt
    seconds = int(diff.total_seconds())

    if seconds < 60:
        return i18n.get("common-timeago-s", seconds=seconds)
    if seconds < 3600:
        return i18n.get("common-timeago-m", minutes=seconds // 60)
    if seconds < 86400:
        return i18n.get("common-timeago-h", hours=seconds // 3600)
    return i18n.get("common-timeago-d", days=seconds // 86400)


def render_project_dashboard(project: Dict[str, Any], i18n: I18nContext) -> str:
    last_activity = project.get("last_activity")
    last_activity_str = format_timeago(last_activity, i18n)

    text = (
        f"📁 <b>{project['name']}</b>\n"
        f"{project.get('description') or ''}\n\n"
        f"👥 {i18n.get('projects-members-label')}: {project.get('members_count', 0)} \n"
        f"🟢 {i18n.get('projects-active-now')}: {project.get('active_members_count', 0)}\n"
        f"📝 {i18n.get('projects-tasks-label')}: {project.get('tasks_count', 0)} \n "
        f"🔥 {i18n.get('projects-in-progress')}: {project.get('in_progress_tasks_count', 0)} \n"
        f"⚠️ {i18n.get('projects-overdue')}: {project.get('overdue_tasks_count', 0)} \n\n"
        f"✅ {i18n.get('projects-done')}: {project.get('done_tasks_count', 0)}\n"
        f"⏱ {i18n.get('projects-focus-tracked')}: {format_duration(project.get('total_focus_time', 0))}\n"
        f"{i18n.get('common-last-activity')}: {last_activity_str}"
    )
    return text


def render_tasks_grouped(tasks: List[Dict[str, Any]], i18n: I18nContext, title: str = None) -> str:
    if not tasks:
        return i18n.get("tasks-empty")

    groups = {"overdue": [], "in_progress": [], "todo": [], "done": []}

    import datetime

    now = datetime.datetime.now(datetime.timezone.utc)

    for t in tasks:
        status = t["status"]
        deadline = t.get("deadline")
        if deadline:
            dt = datetime.datetime.fromisoformat(deadline.replace("Z", "+00:00"))
            if dt < now and status != "done":
                groups["overdue"].append(t)
                continue

        if status in groups:
            groups[status].append(t)
        else:
            groups["todo"].append(t)

    sections = []
    if title:
        sections.append(f"<b>{title}</b>")

    titles = {
        "overdue": f"⚠️ {i18n.get('tasks-group-overdue')}",
        "in_progress": f"🔥 {i18n.get('tasks-group-in-progress')}",
        "todo": f"📌 {i18n.get('tasks-group-todo')}",
        "done": f"✅ {i18n.get('tasks-group-done')}",
    }

    priority_map = {"high": 3, "medium": 2, "low": 1}

    for key, group_tasks in groups.items():
        if not group_tasks:
            continue

        # Sort by priority within group
        group_tasks.sort(
            key=lambda x: priority_map.get(x.get("priority", "medium"), 2), reverse=True
        )

        section = [f"<b>{titles[key]}</b>"]
        for t in group_tasks:
            priority_emoji = get_priority_emoji(t.get("priority"))
            attachments = (
                f" 📎 {t['attachments_count']}"
                if t.get("attachments_count", 0) > 0
                else ""
            )
            focus = f" ⏱ {format_duration(t.get('focus_time', 0))}"
            section.append(f"• {priority_emoji} {t['title']}{attachments}{focus}")
        sections.append("\n".join(section))

    return "\n\n".join(sections)


def render_task_detail(task: Dict[str, Any], i18n: I18nContext) -> str:
    priority_emoji = get_priority_emoji(task.get("priority"))
    status_emoji = get_status_emoji(task["status"])
    task_status = task["status"]

    deadline = task.get("deadline")
    if deadline:
        # Simplified formatting
        deadline = deadline.replace("T", " ").replace("Z", "")[:16]

    priority = task.get("priority", "medium")
    task_status = task.get("status", "todo")

    text = (
        f"{priority_emoji} <b>{task['title']}</b>\n"
        f"{task.get('description') or i18n.get('tasks-no-desc')}\n\n"
        f"📁 {i18n.get('projects-label')}: "
        f"{task.get('project_name') or i18n.get('common-none')}\n"
        f"👤 {i18n.get('tasks-assignee')}: "
        f"{task.get('assignee_name') or i18n.get('common-unassigned')}\n"
        f"{priority_emoji} {i18n.get('tasks-priority')}: "
        f"{i18n.get(f'priority-{priority}')}\n"
        f"📅 {i18n.get('tasks-deadline')}: "
        f"{deadline or i18n.get('common-none')}\n"
        f"📊 {i18n.get('tasks-status')}: "
        f"{status_emoji} {i18n.get(f'tasks-status-{task_status}')}\n"
        f"📎 {i18n.get('tasks-attachments')}: "
        f"{task.get('attachments_count', 0)}\n"
        f"⏱ {i18n.get('tasks-focus-tracked')}: "
        f"{format_duration(task.get('focus_time', 0))}\n"
    )
    return text


def render_members_list(members: List[Dict[str, Any]], i18n: I18nContext) -> str:
    lines = [f"👥 <b>{i18n.get('members-title')}</b>\n"]

    import datetime

    now = datetime.datetime.now(datetime.timezone.utc)

    for m in members:
        user = m["user_detail"]
        emoji = get_random_emoji(user["id"])
        role = i18n.get(f"members-role-{m['role']}")

        last_activity = user.get("last_activity_at")
        if last_activity:
            la_dt = datetime.datetime.fromisoformat(
                last_activity.replace("Z", "+00:00")
            )
            if (now - la_dt).total_seconds() < 300:
                activity_str = f"🟢 {i18n.get('members-active-now')}"
            else:
                activity_str = f"{i18n.get('members-last-active')}: {format_timeago(last_activity, i18n)}"
        else:
            activity_str = i18n.get("members-never-active")

        lines.append(f"{emoji} <b>{user['first_name']}</b> — {role} {activity_str}")

    return "\n".join(lines)


def format_duration(seconds: int) -> str:
    if not seconds:
        return f"0h 0m"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    return f"{hours}h {minutes}m"


def build_progress_bar(percent: int) -> str:
    filled = percent // 10
    empty = 10 - filled

    return "🟩" * filled + "⬜" * empty


class ProductivityAnalyticsRenderer:

    @staticmethod
    def render(stats, i18n):

        focus_today = format_duration(stats["focus_today_seconds"])

        best_focus = format_duration(stats["best_focus_duration_seconds"])

        average_focus = format_duration(stats["average_focus_session_seconds"])

        top_member = (
            f'@{stats["top_member_username"]}'
            if stats["top_member_username"]
            else i18n.analytics.no.top.member()
        )

        leaderboard_lines = []

        medals = ["🥇", "🥈", "🥉"]

        for index, member in enumerate(stats["leaderboard"]):

            medal = medals[index] if index < len(medals) else "🏅"

            leaderboard_lines.append(
                i18n.analytics.leaderboard.item(
                    medal=medal,
                    username=f'@{member["username"]}',
                    tasks=member["completed_tasks"],
                )
            )

        leaderboard_text = "\n".join(leaderboard_lines)

        return i18n.analytics.productivity.dashboard(
            tasks_delta=stats["tasks_delta_percent"],
            tasks_created_today=stats["tasks_created_today"],
            tasks_completed_today=stats["tasks_completed_today"],
            overdue_tasks=stats["overdue_tasks"],
            completion_rate=stats["completion_rate"],
            focus_today=focus_today,
            focus_delta_minutes=round(
                (stats["focus_today_seconds"] - stats["focus_yesterday_seconds"]) / 60
            ),
            best_focus=best_focus,
            average_focus=average_focus,
            top_member=top_member,
            top_member_tasks=stats["top_member_tasks"],
            leaderboard=leaderboard_text,
            active_members=stats["active_members_count"],
            ai_insight=(stats["ai_insight"] or i18n.analytics.default.ai.insight()),
        )
