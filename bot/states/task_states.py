from aiogram.fsm.state import State, StatesGroup

class TaskStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_priority = State()
    waiting_for_project = State()
    waiting_for_deadline = State()
    waiting_for_attachment = State()
    waiting_for_search_query = State()
