from sqlalchemy import Column, BigInteger, String, sql, Date, Boolean, Integer

from utils.db_api.db_gino import TimedBaseModel


class Orders(TimedBaseModel):
    __tablename__ = 'orders'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(BigInteger())
    fio = Column(String(255))
    work = Column(Boolean(), default=False)
    dates = Column(Date(), nullable=False)
    tabel = Column(String(15))
    tel = Column(String(25))
    noxor = Column(Boolean(), default=False)
    kunduz = Column(Boolean(), default=False)
    kech = Column(Boolean(), default=False)
    paytype = Column(String(150))
    pay_status = Column(Boolean(), default=False)
    summa = Column(Integer())

    query: sql.select
