import asyncio
from datetime import date

# from data import config
from utils.db_api import quick_commands as commands
from utils.db_api.db_gino import db


async def db_test():
    # await db.set_bind(config.POSTGRES_URI)
    await db.set_bind('postgresql://postgres:12369@localhost/postgres')
    # await db.gino.drop_all()
    await db.gino.create_all()

    dates = date(2023, 11, 2)
    # await commands.add_orders(14, 'Djuraev Shaxboz A\'zamdjonovich', dates, '57394', "Click", True, True, False, False, 1000000, '998901282852')

    # orders = await commands.select_all_orders()
    # print(orders)
    # order = []
    # order = await commands.select_order_by_date(2023, 11)
    # for ord in orders:
    #     if ord.noxor == False:
    #         order.append(ord.dates.day)
    order_id = []
    await commands.change_day(5, dates)




    # try:
    #     for i in range(1, 32):
    #         year_now = date(2023, 5, i)
    #         if i in order:
    #             continue
    #         print(year_now)
    # except ValueError:
    #     pass
    #
    # work_update = await commands.update_work(14)
    # print(order)
    # order = await commands.select_order(14)
    # await order.update(noxor=True).apply()


loop = asyncio.get_event_loop()
loop.run_until_complete(db_test())
