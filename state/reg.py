from aiogram.dispatcher.filters.state import StatesGroup, State


class regis(StatesGroup):
    work = State()
    fio = State()
    dates = State()
    orders = State()
    year = State()
    months = State()
    dayru = State()
    paytype= State()
    tel = State()


class uz_regis(StatesGroup):
    work_uz = State()
    fio_uz = State()
    dates_uz = State()
    orders_uz = State()
    year_uz = State()
    months_uz = State()
    dayru_uz = State()
    paytype_uz = State()
    tel_uz = State()


