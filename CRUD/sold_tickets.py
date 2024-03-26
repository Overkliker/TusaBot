from sqlalchemy import insert, update
from sqlalchemy.orm import Session

from db_models.classes import SoldTickets
from CRUD.typing import *


def insert_new_sold_ticket(engine, ticket):
    with Session(engine) as session:
        session.add(ticket)
        session.commit()


def get_last_ticket_for_user(engine, tg_id):
    with Session(engine) as session:
        query = session.query(SoldTickets).filter(SoldTickets.solder_tg_id == tg_id).all()
        return query[-1]

def change_status_for_order(engine, id, status):
    with Session(engine) as session:
        query = update(SoldTickets).where(SoldTickets.id
                                               == id).values(status=status)
        session.execute(query)
        session.commit()