from datetime import date

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\"Узметкомбинат\"АЖ ходими!"),
        ],
        [
            KeyboardButton("\"Узметкомбинат\"АЖ ходими эмасман"),
        ],

    ],
    resize_keyboard=True
)


month_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'Январ'),
            KeyboardButton(text=f'Феврал')
        ],
        [
            KeyboardButton(text=f'Март'),
            KeyboardButton(text=f'Апрел')
        ],
        [
            KeyboardButton(text=f'Май'),
            KeyboardButton(text=f'Июн')
        ],
        [
            KeyboardButton(text=f'Июл'),
            KeyboardButton(text=f'Август')
        ],
        [
            KeyboardButton(text=f'Сентябр'),
            KeyboardButton(text=f'Октябр')
        ],
        [
            KeyboardButton(text=f'Ноябр'),
            KeyboardButton(text=f'Декабр')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
)

year_now = date.today()
years_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=f'{year_now.year}'),
            KeyboardButton(text=f'{int(year_now.year) + 1}'),
        ],
        [
            KeyboardButton(text=f'{int(year_now.year) + 2}'),
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

order_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Наҳор оши')
        ],
        [
            KeyboardButton(text='Кундузги базм')
        ],
        [
            KeyboardButton(text='Кечки базм')
        ],
        [
            KeyboardButton(text='Наҳор оши ва кундузги базм')
        ],
        [
            KeyboardButton(text='Наҳор оши ва кечки базм')
        ],
        [
            KeyboardButton(text='Кундузги базм ва кечки базм')
        ],
        [
            KeyboardButton(text='Наҳор оши, кундузги базм ва кечки базм')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
pays_uz = ReplyKeyboardMarkup(
    keyboard=[
        # [
        #     KeyboardButton(text='Click 💳')
        # ],
        # [
        #     KeyboardButton(text='Payme 💳')
        # ],
        [
            KeyboardButton(text='Нақт пулга 💵')
        ],
        [
            KeyboardButton(text='Буюртмани бекор қилиш ❌')
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

cancel_uz = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Буюртмани бекор қилиш ❌')
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )