from datetime import date

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Сотрудник АО "Узметкомбинат"'),
        ],
        [
            KeyboardButton('Не работает АО "Узметкомбинат"'),
        ],

    ],
    resize_keyboard=True
)

month = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'Январь'),
            KeyboardButton(text=f'Февраль')
        ],
        [
            KeyboardButton(text=f'Март'),
            KeyboardButton(text=f'Апрель')
        ],
        [
            KeyboardButton(text=f'Май'),
            KeyboardButton(text=f'Июнь')
        ],
        [
            KeyboardButton(text=f'Июль'),
            KeyboardButton(text=f'Август')
        ],
        [
            KeyboardButton(text=f'Сентябрь'),
            KeyboardButton(text=f'Октябрь')
        ],
        [
            KeyboardButton(text=f'Ноябрь'),
            KeyboardButton(text=f'Декабрь')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
)

year_now = date.today()
year = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'{year_now.year}'),
            KeyboardButton(text=f'{int(year_now.year) + 1}'),
        ],
        [
            KeyboardButton(text=f'{int(year_now.year) + 2}'),
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Нохор ош')
        ],
        [
            KeyboardButton(text='Дневное мероприятие')
        ],
        [
            KeyboardButton(text='Вечернее мероприятие')
        ],
        [
            KeyboardButton(text='Нохор оши и дневное мероприятие')
        ],
        [
            KeyboardButton(text='Нохор оши и вечернее мероприятие')
        ],
        [
            KeyboardButton(text='Дневное и вечернее мероприятие')
        ],
        [
            KeyboardButton(text='Нохор оши, дневное и вечернее мероприятия')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
pays = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Click 💳')
        # ],
        # [
        #     KeyboardButton(text='Payme 💳')
        # ],
        [
            KeyboardButton(text='Наличными 💵')
        ],
        [
            KeyboardButton(text='Отменить заказ ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

cancel = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Отменить заказ ❌')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )