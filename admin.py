from datetime import date

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from keyboards import kb_admin, years_adm, month_adm, res, pay_change, lang_btn, summa
from state import admin
from loader import dp
from filters import IsAdm
from utils.db_api import quick_commands as commands


@dp.message_handler(IsAdm(), text='Тўйхона бандлигини кўриш.')
async def admins(message: Message):
    txt = 'Йилни танланг:'
    await message.answer(txt, reply_markup=years_adm)
    await admin.year_admin.set()


@dp.message_handler(IsAdm(), state=admin.year_admin)
async def year_adm(message: Message, state: FSMContext):
    await state.update_data(year_admin=message.text)
    txt = 'Ойни танланг:'
    await message.answer(txt, reply_markup=month_adm)
    await admin.months_admin.set()


@dp.message_handler(IsAdm(), state=admin.months_admin)
async def year_adm(message: Message, state: FSMContext):
    if message.text == 'Январ':
        await state.update_data(mont_admin=1)
        await state.update_data(months_txt_adm='Январ')
    elif message.text == 'Феврал':
        await state.update_data(mont_admin=2)
        await state.update_data(months_txt_adm='Феврал')
    elif message.text == 'Март':
        await state.update_data(mont_admin=3)
        await state.update_data(months_txt_adm='Март')
    elif message.text == 'Апрел':
        await state.update_data(mont_admin=4)
        await state.update_data(months_txt_adm='Апрел')
    elif message.text == 'Май':
        await state.update_data(mont_admin=5)
        await state.update_data(months_txt_adm='Май')
    elif message.text == 'Июн':
        await state.update_data(mont_admin=6)
        await state.update_data(months_txt_adm='Июн')
    elif message.text == 'Июл':
        await state.update_data(mont_admin=7)
        await state.update_data(months_txt_adm='Июл')
    elif message.text == 'Август':
        await state.update_data(mont_admin=8)
        await state.update_data(months_txt_adm='Август')
    elif message.text == 'Сентябр':
        await state.update_data(mont_admin=9)
        await state.update_data(months_txt_adm='Сентябр')
    elif message.text == 'Октябр':
        await state.update_data(mont_admin=10)
        await state.update_data(months_txt_adm='Октябр')
    elif message.text == 'Ноябр':
        await state.update_data(mont_admin=11)
        await state.update_data(months_txt_adm='Ноябр')
    elif message.text == 'Декабр':
        await state.update_data(mont_admin=12)
        await state.update_data(months_txt_adm='Декабр')

    data = await state.get_data()
    try:
        year = int(data.get('year_admin'))
        mont_admin = int(data.get('mont_admin'))
        order = await commands.select_order_by_date(year, mont_admin)
        if not order:
            await message.answer('Бу ойда буюртма қилинмаган', reply_markup=kb_admin)
        else:
            for i in order:
                txtx = ''
                orders = await commands.select_order(i)
                txtx += f'| Куни: {orders.dates} | Заказ № <code>{i}</code> | ФИО: {orders.fio} | Тел: <code>{orders.tel}</code> | Тўлов тури: {orders.paytype} | Тўлов суммаси: {orders.summa} | Заказ тури:'
                if orders.noxor:
                    txtx += " Наҳор "
                if orders.kunduz:
                    txtx += ' Кундузги базм '
                if orders.kech:
                    txtx += ' Кечги базм |'
                await message.answer(txtx)
            await message.answer('Буюртмалар тугади', reply_markup=kb_admin)
    except Exception:
        await state.finish()
        await message.answer('Хатолик', reply_markup=kb_admin)

    await state.finish()


@dp.message_handler(IsAdm(), text='Буюртмани рақами бўйича текшириш.')
async def admins(message: Message):
    txt = 'Буюртмани рақамини ёзинг'
    await message.answer(txt)
    await admin.order_number.set()


@dp.message_handler(IsAdm(), state=admin.order_number)
async def order_adm(message: Message, state: FSMContext):
    await state.update_data(order_id=message.text)
    data = await state.get_data()
    try:
        order_id = int(data.get('order_id'))
        orders = await commands.select_order(order_id)
        txt_or = ''
        if orders.pay_status:
            pay = " Тўлов қилинган ✅ "
        else:
            pay = " Тўлов қилинмаган ❌"
        txt_or += f'| Куни: {orders.dates} | Буюртма № <code>{order_id}</code> | ФИО: {orders.fio} | Тел: <code>{orders.tel}</code> | Тўлов холати {pay}| Тўлов тури: {orders.paytype} | Тўлов суммаси: {orders.summa} | Буюртма тури:'
        if orders.noxor:
            txt_or += " Наҳор, "
        if orders.kunduz:
            txt_or += ' Кундузги базм, '
        if orders.kech:
            txt_or += ' Кечги базм. |'

        await message.answer(txt_or, reply_markup=kb_admin)

    except Exception:
        await message.answer('Хатолик', reply_markup=kb_admin)
        await state.finish()
    await state.finish()


@dp.message_handler(IsAdm(), text='Буюртмани рақами бўйича ўзгартириш.')
async def admins(message: Message):
    txt = 'Буюртмани рақамини ёзинг'
    await message.answer(txt)
    await admin.order_change.set()


@dp.message_handler(IsAdm(), state=admin.order_change)
async def year_adm(message: Message, state: FSMContext):
    await state.update_data(order_change_id=message.text)
    data = await state.get_data()
    global order_change_id
    order_change_id = data.get('order_change_id')
    txt = 'Ўзгартириш турини танланг:'
    await message.answer(txt, reply_markup=res)
    await state.finish()


@dp.message_handler(IsAdm(), text='Тўлов холатини ўзгартириш.')
async def year_adm(message: Message, state: FSMContext):
    txt = 'Ўзгартиришни танланг:'
    await message.answer(txt, reply_markup=pay_change)


@dp.message_handler(IsAdm(), text='Тўлов қилиш.')
async def year_adm(message: Message, state: FSMContext):
    txt = 'Суммани киритинг:'
    await message.answer(txt, reply_markup=summa)
    await admin.pay.set()


@dp.message_handler(IsAdm(), state=admin.pay)
async def year_adm(message: Message, state: FSMContext):
    try:
        pay_int = int(message.text)
        order_id = int(order_change_id)
        orders = await commands.select_order(order_id)
        pays = orders.summa + pay_int
        await commands.change_pay(order_id, pays)
        await commands.paid(order_id)
        txt = 'Тўлов қилинди.'
        await message.answer(txt, reply_markup=kb_admin)
        txt_or = ''
        pay = "Тўлов қилинди ✅ "
        txt_or += f'| Куни: {orders.dates} | Буюртма № <code>{order_id}</code> | ФИО: {orders.fio} | Тел: <code>{orders.tel}</code> | Тўлов холати {pay}| Тўлов тури: {orders.paytype} | Тўлов суммаси: {pays} | Буюртма тури:'
        if orders.noxor:
            txt_or += " Наҳор, "
        if orders.kunduz:
            txt_or += ' Кундузги базм, '
        if orders.kech:
            txt_or += ' Кечги базм. |'
        await message.answer(txt_or, reply_markup=kb_admin)
    except Exception:
        await message.answer('Хатолик', reply_markup=kb_admin)
        await state.finish()

    await state.finish()


@dp.message_handler(IsAdm(), text='Тўловни бекор қилиш.')
async def year_adm(message: Message, state: FSMContext):
    try:
        order_id = int(order_change_id)
        orders = await commands.select_order(order_id)
        await commands.change_pay(order_id, 0)
        await commands.unpaid(order_id)
        txt = 'Тўловни бекор қилинди.'
        await message.answer(txt, reply_markup=kb_admin)
        txt_or = ''
        pay = "Тўловни бекор қилинди ❌"
        txt_or += f'| Куни: {orders.dates} | Буюртма № <code>{order_id}</code> | ФИО: {orders.fio} | Тел: <code>{orders.tel}</code> | Тўлов холати {pay}| Тўлов тури: {orders.paytype} | Буюртма тури:'
        if orders.noxor:
            txt_or += " Наҳор, "
        if orders.kunduz:
            txt_or += ' Кундузги базм, '
        if orders.kech:
            txt_or += ' Кечги базм. |'

        await message.answer(txt_or, reply_markup=kb_admin)
    except Exception:
        await message.answer('Хатолик', reply_markup=kb_admin)
        await state.finish()


@dp.message_handler(IsAdm(), text='Буюртма кунини ўзгартириш')
async def year_adm(message: Message, state: FSMContext):
    txt = 'Йилни танланг:'
    await message.answer(txt, reply_markup=years_adm)
    await admin.year_admin_change.set()


@dp.message_handler(IsAdm(), state=admin.year_admin_change)
async def year_adm(message: Message, state: FSMContext):
    await state.update_data(change_year=message.text)
    txt = 'Ой танланг:'
    await message.answer(txt, reply_markup=month_adm)
    await admin.months_admin_change.set()


@dp.message_handler(IsAdm(), state=admin.months_admin_change)
async def year_adm(message: Message, state: FSMContext):
    if message.text == 'Январ':
        await state.update_data(change_month=1)
        await state.update_data(months_txt='Январ')
    elif message.text == 'Феврал':
        await state.update_data(change_month=2)
        await state.update_data(months_txt='Феврал')
    elif message.text == 'Март':
        await state.update_data(change_month=3)
        await state.update_data(months_txt='Март')
    elif message.text == 'Апрел':
        await state.update_data(change_month=4)
        await state.update_data(months_txt='Апрел')
    elif message.text == 'Май':
        await state.update_data(change_month=5)
        await state.update_data(months_txt='Май')
    elif message.text == 'Июн':
        await state.update_data(change_month=6)
        await state.update_data(months_txt='Июн')
    elif message.text == 'Июл':
        await state.update_data(change_month=7)
        await state.update_data(months_txt='Июл')
    elif message.text == 'Август':
        await state.update_data(change_month=8)
        await state.update_data(months_txt='Август')
    elif message.text == 'Сентябр':
        await state.update_data(change_month=9)
        await state.update_data(months_txt='Сентябр')
    elif message.text == 'Октябр':
        await state.update_data(change_month=10)
        await state.update_data(months_txt='Октябр')
    elif message.text == 'Ноябр':
        await state.update_data(change_month=11)
        await state.update_data(months_txt='Ноябр')
    elif message.text == 'Декабр':
        await state.update_data(change_month=12)
        await state.update_data(months_txt='Декабр')
    else:
        await message.answer('Бундай ой йўқ.\nТўғри ойни танланг:', reply_markup=month_adm)
        await admin.months_admin_change.set()

    data = await state.get_data()
    year = data.get('change_year')
    month = data.get('change_month')
    list3 = []
    try:
        for i in range(1, 32):
            year_now = date(int(year), int(month), i)
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
    if list3 != []:
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

        cancel = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer('Кунни танланг:', reply_markup=cancel)
        await admin.day_change.set()
    else:
        await message.answer("Хатолик", reply_markup=kb_admin)
        await state.finish()


@dp.message_handler(IsAdm(), state=admin.day_change)
async def year_adm(message: Message, state: FSMContext):
    await state.update_data(change_day=message.text)
    data = await state.get_data()
    try:
        year = int(data.get('change_year'))
        month = int(data.get('change_month'))
        month_txt = data.get('months_txt')
        day = int(data.get('change_day'))
        dates = date(year, month, day)
        print(dates, order_change_id)
        await commands.change_day(int(order_change_id), dates)
        await message.answer(f'Буюртма куни {day} {month_txt} {year}й. кунига ўзгартирилди!', reply_markup=kb_admin)

    except Exception:
        await message.answer("Хатолик", reply_markup=kb_admin)
        await state.finish()

    await state.finish()


@dp.message_handler(IsAdm(), text='Янги буюртма қилиш.')
async def langu(message: Message):
    await message.answer("Тилни танланг!", reply_markup=lang_btn)


@dp.message_handler(IsAdm(), text='ok')
async def ok(message: Message):
    await message.answer('ok', reply_markup=kb_admin)
