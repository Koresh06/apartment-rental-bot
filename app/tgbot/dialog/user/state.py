from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()
    phone = State()


class MainSG(StatesGroup):
    main = State()

