from dataclasses import dataclass


@dataclass
class LeaderboardMemberData:
    username: str
    completed_tasks: int


@dataclass
class ProductivityAnalyticsData:

    tasks_created_today: int

    tasks_completed_today: int

    tasks_completed_yesterday: int

    tasks_delta_percent: int

    overdue_tasks: int

    completion_rate: int

    focus_today_seconds: int

    focus_yesterday_seconds: int

    focus_delta_percent: int

    average_focus_session_seconds: int

    best_focus_duration_seconds: int

    active_members_count: int

    top_member_username: str | None

    top_member_tasks: int

    leaderboard: list[LeaderboardMemberData]

    focus_streak: int = 0
    task_streak: int = 0
    best_day: str | None = None
    chart_data: list[dict] | None = None

    ai_insight: str | None = None
