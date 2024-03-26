from sqlalchemy import insert
from sqlalchemy.orm import Session

from db_models.classes import TutorPromo


def get_tutor_by_promo(engine, promo):
    with Session(engine) as session:
        query = session.query(TutorPromo).filter(TutorPromo.promo_id == promo).first()
        return query


def get_promo_by_tutor_id(engine, tutor_id):
    with Session(engine) as session:
        query = session.query(TutorPromo).filter(TutorPromo.tutor_id == tutor_id).first()
        return query
