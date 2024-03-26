import random

from sqlalchemy import insert,update
from sqlalchemy.orm import Session

from db_models.classes import Users
from CRUD.typing import *


def insert_users(engine, data, role):

    with Session(engine) as session:
        query = Users(
            telegram_id=data.telegram_id,
            fio=data.fio,
            user_role=role,
            ticket_count=0)

        session.add(query)
        session.commit()


def get_user_by_telegram_id(engine, telegram_id):
    with Session(engine) as session:
        query = session.query(Users).filter(Users.telegram_id == telegram_id).all()
        return query


def get_user_by_id(engine, id):
    with Session(engine) as session:
        query = session.query(Users).filter(Users.id == id).first()
        return query

def get_superuser(engine):
    with Session(engine) as session:
        query = session.query(Users).filter(Users.user_role == admin).first()
        return query


def get_random_tutor(engine):
    with Session(engine) as session:
        query = session.query(Users).filter(Users.user_role == tutor).all()
        random_tutor = random.choice(query)
        return random_tutor
