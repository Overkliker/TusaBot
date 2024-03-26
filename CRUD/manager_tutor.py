from sqlalchemy import insert
from sqlalchemy.orm import Session

from db_models.classes import ManagerTutor


def insert_new_tutor(tutor_id, manager_id, engine):
    manager_tutor = ManagerTutor(
        tutor_id=tutor_id,
        manager_id=manager_id
    )

    with Session(engine) as session:
        session.add(manager_tutor)
        session.commit()