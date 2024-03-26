from sqlalchemy import insert
from sqlalchemy.orm import Session

from db_models.classes import TutorPromouter


def insert_new_promouter(tutor_id, promouter_id, engine):
    tutor_promo = TutorPromouter(
        tutor_id=tutor_id,
        promouter_id=promouter_id
    )

    with Session(engine) as session:
        session.add(tutor_promo)
        session.commit()


def get_tutor_by_promouter_id(engine, promouter_id):
    with Session(engine) as session:
        data = session.query(TutorPromouter).where(TutorPromouter.promouter_id == promouter_id).first()
        return data

