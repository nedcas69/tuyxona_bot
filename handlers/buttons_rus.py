import json
import requests
from requests.auth import HTTPBasicAuth
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from datetime import date

from data.config import C_USER, C_PASS, C_URI
from keyboards import kb_ru, month, year, order, pays, cancel
from loader import dp
from state import regis
from keyboards import lang_btn
from filters import IsPrivate
from utils.db_api import quick_commands as commands


@dp.message_handler(text='Отменить заказ ❌',
                    state=[regis.work, regis.fio, regis.dates, regis.orders, regis.year, regis.months, regis.dayru,
                           regis.paytype])
async def quit(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Заказ отменен.', reply_markup=lang_btn)


@dp.message_handler(text='Отменить заказ ❌')
async def quits(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Заказ отменен', reply_markup=lang_btn)


@dp.message_handler(IsPrivate(), content_types=ContentType.DOCUMENT)  # Ловит только фотографии
async def send_photo_file_id(message: Message):
    await message.reply(message.document.file_id)  # Возвращает file_id фотографии с наилучшим разрешением


@dp.message_handler(IsPrivate(), text='Русский 🇷🇺')
async def rusk(mess: Message):
    hello_text = "Укажите пожалуйста, являетесь ли вы сотрудником АО\"Узметкомбинат\"!"
    await mess.answer(hello_text, reply_markup=kb_ru)


@dp.message_handler(IsPrivate(), text='Сотрудник АО "Узметкомбинат"')
async def worked(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Введите таб№:", reply_markup=kb_ru)
    await regis.work.set()


@dp.message_handler(IsPrivate(), text='Не работает АО "Узметкомбинат"')
async def not_worked(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Напишите фамилию, имя и отчество.", reply_markup=cancel)
    await regis.fio.set()


@dp.message_handler(IsPrivate(), state=regis.work)
async def reg_fio(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await state.update_data(tabel=message.text)
    tabel = message.text
    auth = HTTPBasicAuth(C_USER, C_PASS)
    r = requests.get(C_URI + tabel, auth=auth)
    html = r.text.encode('ISO-8859-1').decode('utf-8-sig')
    json_data = json.loads(html)
    name = json_data['ishchi']
    tel = json_data['telefon']
    if name != None:
        await state.update_data(fio=name)
        await state.update_data(work=True)

        if tel != None:
            await state.update_data(tel=tel)
            await message.answer(f"{name} Выберите категорию заказа:", reply_markup=order)
            await regis.orders.set()
        else:
            tel_text = 'Напишите свой номер!'
            await message.answer(tel_text, reply_markup=cancel)
            await regis.tel.set()
    else:
        work_txt = "Такого табельного номера не существует!\nУкажите пожалуйста, являетесь ли вы сотрудником АО\"Узметкомбинат\"!"
        await message.answer(work_txt, reply_markup=kb_ru)
        await state.finish()


@dp.message_handler(IsPrivate(), state=regis.fio)
async def set_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    fio = message.text
    await message.answer(f"{fio} Напишите свой номер!", reply_markup=cancel)
    await regis.tel.set()


@dp.message_handler(IsPrivate(), state=regis.tel)
async def set_fio(message: Message, state: FSMContext):
    await state.update_data(tel=message.text)
    await message.answer('Выберите категорию заказа:', reply_markup=order)
    await regis.orders.set()


@dp.message_handler(IsPrivate(), state=regis.orders)
async def set_fio(message: Message, state: FSMContext):
    orders_x = ['Нохор ош', 'Дневное мероприятие', 'Вечернее мероприятие', 'Нохор оши и дневное мероприятие',
                'Нохор оши и вечернее мероприятие', 'Дневное и вечернее мероприятие', 'Нохор оши, дневное и вечернее мероприятия']
    if message.text in orders_x:
        await state.update_data(orders=message.text)
        await message.answer('Выберите год:', reply_markup=year)
        await regis.year.set()
    else:
        await message.answer('Такой категории нет\nВыберите категорию заказа:', reply_markup=order)
        await regis.orders.set()


@dp.message_handler(IsPrivate(), state=regis.year)
async def set_fio(message: Message, state: FSMContext):
    year_now = date.today()
    if message.text == f'{year_now.year}' or message.text == f'{int(year_now.year) + 1}' or message.text == f'{int(year_now.year) + 2}':
        await state.update_data(year=message.text)
    else:
        await message.answer('Выберите текущий или следующие года:', reply_markup=year)
        await regis.year.set()

    data = await state.get_data()
    years = data.get("year")
    if years == f'{year_now.year}':
        i = year_now.month
        jan = ''
        feb = ''
        mar = ''
        apr = ''
        may = ''
        jun = ''
        jul = ''
        avg = ''
        sep = ''
        octob = ''
        nov = ''
        dec = ''
        while i < 13:
            if i == 1:
                jan = 'Январь'
                i += 1
            if i == 2:
                feb = 'Февраль'
                i += 1
            if i == 3:
                mar = 'Март'
                i += 1
            if i == 4:
                apr = 'Апрель'
                i += 1
            if i == 5:
                may = 'Май'
                i += 1
            if i == 6:
                jun = 'Июнь'
                i += 1
            if i == 7:
                jul = 'Июль'
                i += 1
            if i == 8:
                avg = 'Август'
                i += 1
            if i == 9:
                sep = 'Сентябрь'
                i += 1
            if i == 10:
                octob = 'Октябрь'
                i += 1
            if i == 11:
                nov = 'Ноябрь'
                i += 1
            if i == 12:
                dec = 'Декабрь'
                i += 1
            break

    else:
        jan = 'Январь'
        feb = 'Февраль'
        mar = 'Март'
        apr = 'Апрель'
        may = 'Май'
        jun = 'Июнь'
        jul = 'Июль'
        avg = 'Август'
        sep = 'Сентябрь'
        octob = 'Октябрь'
        nov = 'Ноябрь'
        dec = 'Декабрь'

    mont = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f'{jan}'),
                KeyboardButton(text=f'{feb}')
            ],
            [
                KeyboardButton(text=f'{mar}'),
                KeyboardButton(text=f'{apr}')
            ],
            [
                KeyboardButton(text=f'{may}'),
                KeyboardButton(text=f'{jun}')
            ],
            [
                KeyboardButton(text=f'{jul}'),
                KeyboardButton(text=f'{avg}')
            ],
            [
                KeyboardButton(text=f'{sep}'),
                KeyboardButton(text=f'{octob}')
            ],
            [
                KeyboardButton(text=f'{nov}'),
                KeyboardButton(text=f'{dec}')
            ],
            [
                KeyboardButton(text='Отменить заказ ❌')
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer('Выберите месяц:', reply_markup=mont)
    await regis.months.set()


@dp.message_handler(IsPrivate(), state=regis.months)
async def set_fio(message: Message, state: FSMContext):
    if message.text == 'Январь':
        await state.update_data(months=1)
        await state.update_data(months_txt='Январь')
    elif message.text == 'Февраль':
        await state.update_data(months=2)
        await state.update_data(months_txt='Февраль')
    elif message.text == 'Март':
        await state.update_data(months=3)
        await state.update_data(months_txt='Март')
    elif message.text == 'Апрель':
        await state.update_data(months=4)
        await state.update_data(months_txt='Апрель')
    elif message.text == 'Май':
        await state.update_data(months=5)
        await state.update_data(months_txt='Май')
    elif message.text == 'Июнь':
        await state.update_data(months=6)
        await state.update_data(months_txt='Июнь')
    elif message.text == 'Июль':
        await state.update_data(months=7)
        await state.update_data(months_txt='Июль')
    elif message.text == 'Август':
        await state.update_data(months=8)
        await state.update_data(months_txt='Август')
    elif message.text == 'Сентябрь':
        await state.update_data(months=9)
        await state.update_data(months_txt='Сентябрь')
    elif message.text == 'Октябрь':
        await state.update_data(months=10)
        await state.update_data(months_txt='Октябрь')
    elif message.text == 'Ноябрь':
        await state.update_data(months=11)
        await state.update_data(months_txt='Ноябрь')
    elif message.text == 'Декабрь':
        await state.update_data(months=12)
        await state.update_data(months_txt='Декабрь')
    else:
        await message.answer('Такого месяца не существует.\nВыберите правильный месяц:', reply_markup=month)
        await regis.months.set()

    all_orders = await commands.select_all_orders()
    days = []
    data = await state.get_data()
    client_orders = data.get('orders')
    years = data.get('year')
    monthsx = data.get('months')
    noxor1 = 0
    kunduz1 = 0
    kech1 = 0
    if client_orders == 'Нохор ош':
        await state.update_data(noxor=True)
        noxor1 = 1
    elif client_orders == 'Дневное мероприятие':
        await state.update_data(kunduz=True)
        kunduz1 = 1
    elif client_orders == 'Вечернее мероприятие':
        await state.update_data(kech=True)
        kech1 = 1
    elif client_orders == 'Нохор оши и дневное мероприятие':
        await state.update_data(noxor=True)
        await state.update_data(kunduz=True)
        noxor1 = 1
        kunduz1 = 1
    elif client_orders == 'Нохор оши и вечернее мероприятие':
        await state.update_data(noxor=True)
        await state.update_data(kech=True)
        kech1 = 1
        noxor1 = 1
    elif client_orders == 'Дневное и вечернее мероприятие':
        await state.update_data(kech=True)
        await state.update_data(kunduz=True)
        kunduz1 = 1
        kech1 = 1
    elif client_orders == 'Нохор оши, дневное и вечернее мероприятия':
        await state.update_data(noxor=True)
        await state.update_data(kech=True)
        await state.update_data(kunduz=True)
        noxor1 = 1
        kunduz1 = 1
        kech1 = 1
    else:
        await message.answer("Выберите категорию заказа:", reply_markup=order)
        await regis.orders.set()

    for items in all_orders:
        if items.pay_status and items.dates.month == int(monthsx):
            if noxor1 == 1 and kunduz1 == 1:
                if items.noxor and items.kunduz:
                    days.append(items.dates.day)
            if noxor1 == 1 and kech1 == 1:
                if items.noxor and items.kech:
                    days.append(items.dates.day)
            if kunduz1 == 1 and kech1 == 1:
                if items.kunduz and items.kech:
                    days.append(items.dates.day)
            if noxor1 == 1:
                if items.noxor:
                    days.append(items.dates.day)
            if kunduz1 == 1:
                if items.kunduz:
                    days.append(items.dates.day)
            if kech1 == 1:
                if items.kech:
                    days.append(items.dates.day)

    list3 = []
    try:
        for i in range(1, 32):
            year_now = date(int(years), int(monthsx), i)
            if i in days:
                continue
            list3.append(i)
            day = year_now.day
    except ValueError:
        pass
    kb_list1 = []
    kb_list2 = []
    kb_list3 = []
    kb_list4 = []
    kb_list5 = []
    kb = [kb_list1, kb_list2, kb_list3, kb_list4, kb_list5]
    if list3 == []:
        await message.answer('Все дни в этом месяце заняты.\nВыберите другой месяц:', reply_markup=month)
        await regis.months.set()
    else:
        for it in list3:
            if it <= 6:
                kb_list1.append(KeyboardButton(text=f'{it}'))
            elif 6 < it <= 12:
                kb_list2.append(KeyboardButton(text=f'{it}'))
            elif 12 < it <= 18:
                kb_list3.append(KeyboardButton(text=f'{it}'))
            elif 18 < it <= 24:
                kb_list4.append(KeyboardButton(text=f'{it}'))
            elif 24 < it <= 31:
                kb_list5.append(KeyboardButton(text=f'{it}'))

        cancel_kb = [KeyboardButton(text='Отменить заказ ❌')]
        kb.append(cancel_kb)
        cancel = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await state.update_data(day_x=days)
        await message.answer('Выберите день:', reply_markup=cancel)
        await regis.dayru.set()


@dp.message_handler(IsPrivate(), state=regis.dayru)
async def set_day(message: Message, state: FSMContext):
    datta = await state.get_data()
    day_x = datta.get('day_x')
    text = message.text
    days_x = [i for i in range(1, 32)]
    try:
        if int(text) in days_x:
            if int(text) in day_x:
                await state.finish()
                await message.answer('Этот день занят. Заказ отменен!', reply_markup=lang_btn)
            else:
                await state.update_data(days=message.text)
                data = await state.get_data()
                days = data.get('days')
                fio = data.get('fio')
                client_orders = data.get('orders')
                years = data.get('year')
                months_txt = data.get('months_txt')
                months = data.get('months')
                tel = data.get('tel')
                year_nows = date(int(years), int(months), int(days))
                year_now = date.today()
                a = year_nows - year_now
                if a.days < 0:
                    await state.finish()
                    await message.answer('Нельзя заказать прошедщим днём!\nЗаказ отменен', reply_markup=lang_btn)
                else:
                    txt = f'{fio} вы хотите заказат {client_orders} на {days}-{months_txt} {years} год?\n{tel}-Ваш номер телефона?\nСумма для забронирования 1 000 000 сумов\nЕсли вы уверены то выберите тип оплаты.\n*При выборе оплаты наличными забронируется день тому кто первый произвел оплату \n\nВыберите тип оплаты:'
                    await message.answer(txt, reply_markup=pays)
                    await regis.paytype.set()
    except Exception:
        await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)
        await state.finish()


@dp.message_handler(IsPrivate(), state=regis.paytype)
async def set_fio(message: Message, state: FSMContext):
    pays_x = ['Click 💳', 'Payme 💳', 'Наличными 💵']
    if message.text in pays_x:
        await state.update_data(pay_type=message.text)
        data = await state.get_data()
        fio = data.get('fio')
        work = data.get('work')
        years = data.get('year')
        months = data.get('months')
        days = data.get('days')
        tabel = data.get('tabel')
        pay_type = data.get('pay_type')
        noxor = data.get('noxor')
        kunduz = data.get('kunduz')
        kech = data.get('kech')
        sums = 0
        tel = data.get('tel')
        year_nows = date(int(years), int(months), int(days))
        user_id = message.from_user.id
        await state.finish()
        await commands.add_orders(user_id, fio, year_nows, tabel, pay_type, work, noxor, kunduz, kech, sums, tel)

        if pay_type == 'Наличными 💵':
            order = await commands.select_order_id(fio)
            txt = f'{fio} ваш заказ оформлен!\nНомер вашего заказа {order.order_id}, но для вступления его в силу нужно произвезти оплату'
            await message.answer(txt, reply_markup=lang_btn)
        elif pay_type == 'Click 💳':
            pass
        elif pay_type == 'Payme 💳':
            pass
        else:
            await message.answer('Заказ отменен. Произошла ошибка!', reply_markup=lang_btn)

    else:
        await message.answer('Выберите тип оплаты:', reply_markup=pays)
        await regis.paytype.set()
