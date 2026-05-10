from aiogram.fsm.state import State, StatesGroup

class TaskStates(StatesGroup):
    waiting_for_project = State()
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_priority = State()
    waiting_for_deadline_date = State()
    waiting_for_deadline_time = State()
    waiting_for_assignee = State()
    waiting_for_attachment = State()
    waiting_for_confirmation = State()
    waiting_for_search_query = State()
    waiting_for_add_time_custom = State()

    # Editing states
    editing_title = State()
    editing_description = State()
    editing_priority = State()
    editing_deadline_date = State()
    editing_deadline_time = State()
    editing_assignee = State()
