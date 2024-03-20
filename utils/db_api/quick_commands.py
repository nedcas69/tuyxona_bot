from asyncpg import UniqueViolationError
from datetime import date

from utils.db_api.schemas.orders import Orders


async def add_orders(user_id: int, fio: str, dates, tabel, paytype, work, noxor, kunduz, kech, summa, tel):
    try:
        order = Orders(user_id=user_id, fio=fio, work=work, dates=dates, tabel=tabel, noxor=noxor, kunduz=kunduz,
                       kech=kech, paytype=paytype, summa=summa, tel=tel
                       )
        await order.create()
    except UniqueViolationError:
        print("Заказ не создан!")


async def select_all_orders():
    orders = await Orders.query.gino.all()
    return orders


#
# async def select_all_dates():
#     dates = await Orders.query(orders.dates).gino.all()
#     return dates

async def select_order(order_id):
    order = await Orders.query.where(Orders.order_id == order_id).gino.first()
    return order


async def select_order_id(fio):
    order = await Orders.query.where(Orders.fio == fio).gino.all()
    return order.pop()


async def select_order_by_date(year, month):
    orders = []
    try:
        for i in range(1, 32):
            dates = date(year, month, i)
            order = await Orders.query.where(Orders.pay_status == True).gino.all()

            for item in order:
                if item.dates == dates:
                    orders.append(item.order_id)
    except Exception:
        pass

    return orders


async def paid(order_id):
    order = await select_order(order_id)
    await order.update(pay_status=True).apply()


async def unpaid(order_id):
    order = await select_order(order_id)
    await order.update(pay_status=False).apply()


async def change_day(order_id, dates):
    order = await select_order(order_id)
    await order.update(dates=dates).apply()


async def change_pay(order_id, summa):
    order = await select_order(order_id)
    await order.update(summa=summa).apply()


