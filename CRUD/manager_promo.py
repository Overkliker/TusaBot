from sqlalchemy import insert
from sqlalchemy.orm import Session

from db_models.classes import ManagerPromo


def get_manager_by_promo(engine, promo):
    with Session(engine) as session:
        query = session.query(ManagerPromo).filter(ManagerPromo.promo_id == promo).first()
        return query
