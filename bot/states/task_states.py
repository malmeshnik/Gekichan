from aiogram.fsm.state import State, StatesGroup

class TaskStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_project = State()
    waiting_for_deadline = State()
