from aiogram.fsm.state import State, StatesGroup

class ProjectStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_member_username = State()
    waiting_for_member_contact = State()
    waiting_for_description = State()
