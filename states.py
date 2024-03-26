from aiogram.fsm.state import State, StatesGroup


class StepsRegisterForm(StatesGroup):
    GET_NAME = State()
    GET_INFO = State()
    GET_PROMO = State()
    GET_VK = State()


class PassTicketForm(StatesGroup):
    GET_TYPE = State()
    GET_PHOTO = State()