from aiogram.filters.callback_data import CallbackData
from typing import Optional


# --- Common ---
class CommonBackCb(CallbackData, prefix="cb"):
    to: str  # projects, tasks, settings, pv (project_view), pm (project_members)
    id: Optional[str] = None


class CommonConfirmCb(CallbackData, prefix="cc"):
    action: str  # ty (task_create_yes), tn (task_create_no)
    id: Optional[str] = None


class CommonIgnoreCb(CallbackData, prefix="ignore"):
    pass


# --- Projects ---
class ProjectListCb(CallbackData, prefix="pl"):
    page: int = 1


class ProjectViewCb(CallbackData, prefix="pv"):
    id: str


class ProjectActionCb(CallbackData, prefix="pa"):
    action: str  # c (create), s (search), a (archive), dc (delete_confirm), df (delete_final)
    id: Optional[str] = None


class ProjectMembersCb(CallbackData, prefix="pm"):
    project_id: str


class ProjectMemberAddCb(CallbackData, prefix="pma"):
    project_id: str
    method: Optional[str] = None  # u (username), c (contact)


# --- Tasks ---
class TasksHubCb(CallbackData, prefix="th"):
    section: Optional[str] = None  # my, today, tomorrow, week, overdue, completed, by-projects


class ProjectTasksCb(CallbackData, prefix="pt"):
    project_id: str
    page: int = 1


class GlobalTasksCb(CallbackData, prefix="gt"):
    section: str
    page: int = 1


class TaskViewCb(CallbackData, prefix="tv"):
    id: str


class TaskCreateCb(CallbackData, prefix="tc"):
    project_id: Optional[str] = None  # "null" if personal


class TaskActionCb(CallbackData, prefix="ta"):
    action: str  # e (edit), c (complete), dc (delete_confirm), df (delete_final), sd (skip desc)
    id: str


class TaskEditCb(CallbackData, prefix="te"):
    field: str  # t (title), d (desc), p (prio), dl (dead), a (assignee)
    id: str


class TaskPriorityCb(CallbackData, prefix="tp"):
    priority: str
    is_edit: bool = False


class TaskDeadlineDateCb(CallbackData, prefix="tdd"):
    choice: str  # today, tomorrow, weekend, nextweek, custom, skip
    is_edit: bool = False


class TaskDeadlineTimeCb(CallbackData, prefix="tdt"):
    choice: str  # plus1, plus2, morning, evening, custom, skip
    is_edit: bool = False


class TaskAssigneeCb(CallbackData, prefix="tas"):
    id: str  # user_id or "skip"
    is_edit: bool = False


class TaskAttachmentCb(CallbackData, prefix="tatt"):
    action: str  # l (list), s (start), d (delete)
    id: str  # task_id OR attach_id


# --- Focus ---
class FocusActionCb(CallbackData, prefix="fa"):
    action: str  # p (pause), r (resume), ref (refresh), s (stop), b (break)
    id: Optional[str] = None  # session_id


class FocusStartCb(CallbackData, prefix="fs"):
    task_id: Optional[str] = None


class TimerStartCb(CallbackData, prefix="ts"):
    task_id: Optional[str] = None
    duration: int


class FocusPostTimerCb(CallbackData, prefix="fpt"):
    action: str  # d (done), c (continue), m (more)
    id: str  # session_id or task_id (depending on action)


class TimerAddCb(CallbackData, prefix="tadd"):
    task_id: Optional[str] = None
    seconds: str  # can be "custom" or integer string


# --- Settings ---
class SettingsCb(CallbackData, prefix="st"):
    action: str  # main, lang, tz


class SetLangCb(CallbackData, prefix="sl"):
    lang: str


# --- Analytics ---
class AnalyticsPeriodCb(CallbackData, prefix="ap"):
    period: str
    project_id: Optional[str] = None
