from sqlalchemy import insert, update
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, cast

from db_models.classes import OrdersOnRegister


def get_order_by_telegram_id(engine, id):
    with (Session(engine) as session):
        order = session.query(OrdersOnRegister).filter(OrdersOnRegister.telegram_id == id).first()
        return order


def order_insert(data, engine):
    with Session(engine) as session:
        order = OrdersOnRegister(
            telegram_id=data['telegram_id'],
            fio=data['fio'],
            description=data['description'],
            promocode=data['promocode'],
            vk_link=data['vk'],
            status=0)

        session.add(order)
        session.commit()


def set_status_by_telegram_id(engine, telegram_id, status):
    with (Session(engine) as session):
        query = update(OrdersOnRegister).where(OrdersOnRegister.telegram_id
                                                       == telegram_id).values(status=status)
        session.execute(query)
        session.commit()


