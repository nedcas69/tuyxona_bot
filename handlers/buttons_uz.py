import requests
import json
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from requests.auth import HTTPBasicAuth
from datetime import date

from keyboards import lang_btn  # Импортируем нашу клавиатуру
from keyboards import kb_uz, month_uz, years_uz, order_uz, cancel_uz, pays_uz
from state import uz_regis
from loader import dp
from data.config import C_USER, C_PASS, C_URI
from filters import IsPrivate
from utils.db_api import quick_commands as commands


@dp.message_handler(text='Буюртмани бекор қилиш ❌',
                    state=[uz_regis.work_uz, uz_regis.fio_uz, uz_regis.dates_uz, uz_regis.orders_uz, uz_regis.year_uz,
                           uz_regis.months_uz, uz_regis.dayru_uz, uz_regis.paytype_uz])
async def f_quit(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Буюртмани бекор қилинди.', reply_markup=lang_btn)


@dp.message_handler(text='Буюртмани бекор қилиш ❌')
async def quits(message: Message, state: FSMContext):
    await state.finish()
    await message.answer('Буюртмани бекор қилинди.', reply_markup=lang_btn)


@dp.message_handler(IsPrivate(), content_types=ContentType.DOCUMENT)  # Ловит только фотографии
async def send_photo_file_id(message: Message):
    await message.reply(message.document.file_id)  # Возвращает file_id фотографии с наилучшим разрешением


@dp.message_handler(IsPrivate(), text='Ўзбекча 🇺🇿')
async def rusk(mess: Message):
    hello_text = "Илтимос \"Узметкомбинат\"АЖ ходимимисиз ёки ёки йўқ кўрсатинг!"
    await mess.answer(hello_text, reply_markup=kb_uz)


@dp.message_handler(IsPrivate(), text="\"Узметкомбинат\"АЖ ходими!")
async def worked(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await message.answer("Табел рақамингизни ёзинг:", reply_markup=kb_uz)
    await uz_regis.work_uz.set()


@dp.message_handler(IsPrivate(), text="\"Узметкомбинат\"АЖ ходими эмасман")
async def not_worked(message: Message, state: FSMContext):  # Создаём асинхронную функцию

    await message.answer("Фамилия, исми-шарифингизни ёзинг.", reply_markup=cancel_uz)
    await  uz_regis.fio_uz.set()


@dp.message_handler(IsPrivate(), state=uz_regis.work_uz)
async def reg_fio(message: Message, state: FSMContext):  # Создаём асинхронную функцию
    await state.update_data(tabel_uz=message.text)
    tabel = message.text
    auth = HTTPBasicAuth(C_USER, C_PASS)
    r = requests.get(C_URI + tabel, auth=auth)
    html = r.text.encode('ISO-8859-1').decode('utf-8-sig')
    json_data = json.loads(html)
    name = json_data['ishchi']
    tel = json_data['telefon']
    if name != None:
        await state.update_data(fio_uz=name)
        await state.update_data(work_uz=True)

        if tel != None:
            await state.update_data(tel_uz=tel)
            await message.answer(f"{name} буюртма турини танланг:", reply_markup=order_uz)
            await uz_regis.orders_uz.set()
        else:
            tel_text = 'Телефон рақамингизни ёзинг!'
            await message.answer(tel_text, reply_markup=cancel_uz)
            await uz_regis.tel_uz.set()
    else:
        work_txt = "Бундай табел рақам мавжуд эмас!\nИлтимос \"Узметкомбинат\"АЖ ходимимисиз ёки ёки йўқ кўрсатинг!"
        await message.answer(work_txt, reply_markup=kb_uz)
        await state.finish()


@dp.message_handler(IsPrivate(), state=uz_regis.fio_uz)
async def set_fio(message: Message, state: FSMContext):
    await state.update_data(fio_uz=message.text)
    fio = message.text
    await message.answer(f"{fio} Телефон рақамингизни ёзинг!", reply_markup=cancel_uz)
    await uz_regis.tel_uz.set()


@dp.message_handler(IsPrivate(), state=uz_regis.tel_uz)
async def set_fio(message: Message, state: FSMContext):
    await state.update_data(tel_uz=message.text)
    await message.answer('Буюртма турини танланг:', reply_markup=order_uz)
    await uz_regis.orders_uz.set()


@dp.message_handler(IsPrivate(), state=uz_regis.orders_uz)
async def set_fio(message: Message, state: FSMContext):
    order_x = ['Наҳор оши', 'Кундузги базм', 'Кечки базм', 'Наҳор оши ва кундузги базм', 'Наҳор оши ва кечки базм', 'Кундузги базм ва кечки базм', 'Наҳор оши, кундузги базм ва кечки базм']
    if message.text in order_x:
        await state.update_data(orders_uz=message.text)
        await message.answer('Йилни танланг:', reply_markup=years_uz)
        await uz_regis.year_uz.set()
    else:
        await message.answer('Бундай буюртма мавжуд эмас\nБуюртма турини танланг:', reply_markup=order_uz)
        await uz_regis.orders_uz.set()


@dp.message_handler(IsPrivate(), state=uz_regis.year_uz)
async def set_fio(message: Message, state: FSMContext):
    year_now = date.today()
    if message.text == f'{year_now.year}' or message.text == f'{int(year_now.year) + 1}' or message.text == f'{int(year_now.year) + 2}':
        await state.update_data(year_uz=message.text)
    else:
        await message.answer('Шу ёки келаси йилларни танланг:', reply_markup=years_uz)
        await uz_regis.year_uz.set()

    data = await state.get_data()
    years = data.get("year_uz")
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
                jan = 'Январ'
                i += 1
            if i == 2:
                feb = 'Феврал'
                i += 1
            if i == 3:
                mar = 'Март'
                i += 1
            if i == 4:
                apr = 'Апрел'
                i += 1
            if i == 5:
                may = 'Май'
                i += 1
            if i == 6:
                jun = 'Июн'
                i += 1
            if i == 7:
                jul = 'Июл'
                i += 1
            if i == 8:
                avg = 'Август'
                i += 1
            if i == 9:
                sep = 'Сентябр'
                i += 1
            if i == 10:
                octob = 'Октябр'
                i += 1
            if i == 11:
                nov = 'Ноябр'
                i += 1
            if i == 12:
                dec = 'Декабр'
                i += 1
            break

    else:
        jan = 'Январ'
        feb = 'Феврал'
        mar = 'Март'
        apr = 'Апрел'
        may = 'Май'
        jun = 'Июн'
        jul = 'Июл'
        avg = 'Август'
        sep = 'Сентябр'
        octob = 'Октябр'
        nov = 'Ноябр'
        dec = 'Декабр'

    mont_uz = ReplyKeyboardMarkup(
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
                KeyboardButton(text='Буюртмани бекор қилиш ❌')
            ],
        ],
        resize_keyboard=True,
    )

    await message.answer('Ойни танланг:', reply_markup=mont_uz)
    await uz_regis.months_uz.set()


@dp.message_handler(IsPrivate(), state=uz_regis.months_uz)
async def set_fio(message: Message, state: FSMContext):
    if message.text == 'Январ':
        await state.update_data(months_uz=1)
        await state.update_data(months_txt='Январ')
    elif message.text == 'Феврал':
        await state.update_data(months_uz=2)
        await state.update_data(months_txt='Феврал')
    elif message.text == 'Март':
        await state.update_data(months_uz=3)
        await state.update_data(months_txt='Март')
    elif message.text == 'Апрел':
        await state.update_data(months_uz=4)
        await state.update_data(months_txt='Апрел')
    elif message.text == 'Май':
        await state.update_data(months_uz=5)
        await state.update_data(months_txt='Май')
    elif message.text == 'Июн':
        await state.update_data(months_uz=6)
        await state.update_data(months_txt='Июн')
    elif message.text == 'Июл':
        await state.update_data(months_uz=7)
        await state.update_data(months_txt='Июл')
    elif message.text == 'Август':
        await state.update_data(months_uz=8)
        await state.update_data(months_txt='Август')
    elif message.text == 'Сентябр':
        await state.update_data(months_uz=9)
        await state.update_data(months_txt='Сентябр')
    elif message.text == 'Октябр':
        await state.update_data(months_uz=10)
        await state.update_data(months_txt='Октябр')
    elif message.text == 'Ноябр':
        await state.update_data(months_uz=11)
        await state.update_data(months_txt='Ноябр')
    elif message.text == 'Декабр':
        await state.update_data(months_uz=12)
        await state.update_data(months_txt='Декабр')
    else:
        await message.answer('Бундай ой йўқ.\nТўғри ойни танланг:', reply_markup=month_uz)
        await uz_regis.months_uz.set()

    all_orders = await commands.select_all_orders()
    days = []
    data = await state.get_data()
    client_orders = data.get('orders_uz')
    years = data.get('year_uz')
    monthsx = data.get('months_uz')
    noxor1 = 0
    kunduz1 = 0
    kech1 = 0
    if client_orders == 'Наҳор оши':
        await state.update_data(noxor_uz=True)
        noxor1 = 1
    elif client_orders == 'Кундузги базм':
        await state.update_data(kunduz_uz=True)
        kunduz1 = 1
    elif client_orders == 'Кечки базм':
        await state.update_data(kech_uz=True)
        kech1 = 1
    elif client_orders == 'Наҳор оши ва кундузги базм':
        await state.update_data(noxor_uz=True)
        await state.update_data(kunduz_uz=True)
        noxor1 = 1
        kunduz1 = 1
    elif client_orders == 'Наҳор оши ва кечки базм':
        await state.update_data(noxor_uz=True)
        await state.update_data(kech_uz=True)
        kech1 = 1
        noxor1 = 1
    elif client_orders == 'Кундузги базм ва кечки базм':
        await state.update_data(kech_uz=True)
        await state.update_data(kunduz_uz=True)
        kunduz1 = 1
        kech1 = 1
    elif client_orders == 'Наҳор оши, кундузги базм ва кечки базм':
        await state.update_data(noxor_uz=True)
        await state.update_data(kech_uz=True)
        await state.update_data(kunduz_uz=True)
        noxor1 = 1
        kunduz1 = 1
        kech1 = 1
    else:
        await message.answer("Буюртма турини танланг:", reply_markup=order_uz)
        await uz_regis.orders_uz.set()

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
        await message.answer('Бу ойда барча кунлар банд\nЙилни танланг:', reply_markup=years_uz)
        await uz_regis.year_uz.set()
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

        cancel_kb = [KeyboardButton(text='Буюртмани бекор қилиш ❌')]
        kb.append(cancel_kb)
        cancel = ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await state.update_data(day_x=days)
        await message.answer('Кунни танланг:', reply_markup=cancel)
        await uz_regis.dayru_uz.set()


@dp.message_handler(IsPrivate(), state=uz_regis.dayru_uz)
async def set_day(message: Message, state: FSMContext):
    datta = await state.get_data()
    day_x = datta.get('day_x')
    text = message.text
    days_x = [i for i in range(1, 32)]
    try:
        if int(text) in days_x:
            if int(text) in day_x:
                await state.finish()
                await message.answer('Бу кун банд. Буюртма бекор қилинди!', reply_markup=lang_btn)
            else:
                await state.update_data(days_uz=message.text)
                data = await state.get_data()
                days_uz = data.get('days_uz')
                fio_uz = data.get('fio_uz')
                client_orders_uz = data.get('orders_uz')
                year_uz = data.get('year_uz')
                months_txt_uz = data.get('months_txt')
                mont_uz = data.get('months_uz')
                tel_uz = data.get('tel_uz')
                year_nows = date(int(year_uz), int(mont_uz), int(days_uz))
                year_now = date.today()
                a = year_nows - year_now
                if a.days < 0:
                    await state.finish()
                    await message.answer('Ўтган кунга буюртма бериб бўлмайди!\n\nБуюртма бекор қилинди', reply_markup=lang_btn)
                else:
                    txt = f'{fio_uz} Сиз {client_orders_uz} {days_uz}-{months_txt_uz} {year_uz}й. кунига буюртма бемоқчимисиз?\n\n{tel_uz}-Сизнинг телефон рақамингиз шуми?\nАгар телефон рақамингиз бошқа бўлса, рақамингизни 1С тизимидан ўзгартиринг\n\nБуюртма беришнинг бошланғич тўлови 1 000 000 сўм.\n\nАгар ишончингиз комил бўлса тўлов турини танланг.\n\n*\'Нақт пулга 💵\' тўлов турини танласангиз, тўловни биринчи амалга оширган шахснинг буюртмаси тасдиқланади. \n\nТўлов турини танланг:'
                    await message.answer(txt, reply_markup=pays_uz)
                    await uz_regis.paytype_uz.set()
    except Exception:
        await message.answer('Хатолик. Буюртма бекор килинди!', reply_markup=lang_btn)
        await state.finish()

@dp.message_handler(IsPrivate(), state=uz_regis.paytype_uz)
async def set_fio(message: Message, state: FSMContext):
    pay_x = ['Click 💳', 'Payme 💳', 'Нақт пулга 💵']
    if message.text in pay_x:
        await state.update_data(pay_type_uz=message.text)
        data = await state.get_data()
        fio_uz = data.get('fio_uz')
        work_uz = data.get('work_uz')
        year_uz = data.get('year_uz')
        mont_uz = data.get('months_uz')
        days_uz = data.get('days_uz')
        tabel_uz = data.get('tabel_uz')
        pay_type_uz = data.get('pay_type_uz')
        noxor_uz = data.get('noxor_uz')
        kunduz_uz = data.get('kunduz_uz')
        kech_uz = data.get('kech_uz')
        sums_uz = 0
        tel_uz = data.get('tel_uz')
        year_nows = date(int(year_uz), int(mont_uz), int(days_uz))
        user_id = message.from_user.id
        await state.finish()
        await commands.add_orders(user_id, fio_uz, year_nows, tabel_uz, pay_type_uz, work_uz, noxor_uz, kunduz_uz, kech_uz,
                                  sums_uz, tel_uz)

        if pay_type_uz == 'Нақт пулга 💵':
            order = await commands.select_order_id(fio_uz)
            txt = f'Буюртма рақами: <b>{order.order_id}\n{fio_uz}</b> буюртмангиз ёзилди!, лекин уни кучга кириши учун тўловни амалга оширишингиз керак!'
            await message.answer(txt, reply_markup=lang_btn)
        elif pay_type_uz == 'Click 💳':
            pass
        elif pay_type_uz == 'Payme 💳':
            pass
        else:
            await message.answer('Хатолик. Буюртма бекор килинди!', reply_markup=lang_btn)
    else:
        await message.answer('Тўлов турини танланг:', reply_markup=pays_uz)
        await uz_regis.paytype_uz.set()
