from sqlalchemy import insert
from sqlalchemy.orm import Session

from db_models.classes import Promocodes


def promocodes_by_name(name, engine):
    with (Session(engine) as session):
        promocode_from_db = session.query(Promocodes).filter(Promocodes.text_promo == name).all()
        return promocode_from_db


def promocode_by_name(name, engine):
    with (Session(engine) as session):
        promocode_from_db = session.query(Promocodes).filter(Promocodes.text_promo == name).first()
        return promocode_from_db


def promocode_by_id(id, engine):
    with Session(engine) as session:
        query = session.query(Promocodes).filter(Promocodes.id == id).first()
        return query
