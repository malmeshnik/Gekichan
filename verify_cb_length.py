from bot.utils.callbacks import *
import uuid

def check(name, cb):
    try:
        packed = cb.pack()
        length = len(packed.encode('utf-8'))
        print(f"{name:.<40} {length} bytes: {packed}")
        if length > 64:
            print(f"!!! ALERT: {name} exceeds 64 bytes!")
    except ValueError as e:
        print(f"{name:.<40} FAILED: {e}")

u = str(uuid.uuid4())

check("ProjectViewCb", ProjectViewCb(id=u))
check("ProjectActionCb (delete)", ProjectActionCb(action="df", id=u))
check("ProjectMembersCb", ProjectMembersCb(project_id=u))
check("ProjectMemberAddCb", ProjectMemberAddCb(project_id=u, method="u"))
check("ProjectTasksCb", ProjectTasksCb(project_id=u, page=999))
check("TaskViewCb", TaskViewCb(id=u))
check("TaskActionCb (complete)", TaskActionCb(action="c", id=u))
check("TaskEditCb", TaskEditCb(field="dl", id=u))
check("TaskAttachmentCb (delete)", TaskAttachmentCb(action="d", id=u))
check("FocusActionCb (pause)", FocusActionCb(action="p", id=u))
check("TimerStartCb", TimerStartCb(task_id=u, duration=1500))
check("AnalyticsPeriodCb", AnalyticsPeriodCb(period="month", project_id=u))
check("FocusPostTimerCb", FocusPostTimerCb(action="d", id=u))
