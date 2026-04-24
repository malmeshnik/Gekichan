from aiogram.fsm.state import State, StatesGroup

class ProjectStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
