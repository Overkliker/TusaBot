from sqlalchemy import Column, BIGINT, String, Integer


from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass


class OrdersOnRegister(Base):
    __tablename__ = 'orders_on_register'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    telegram_id = Column(BIGINT, nullable=False)
    fio = Column(String(128), nullable=False)
    description = Column(String(350), nullable=False)
    promocode = Column(String(12), nullable=False)
    vk_link = Column(String(100), nullable=False)
    status = Column(Integer, nullable=False)


class Promocodes(Base):
    __tablename__ = 'promocodes'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    text_promo = Column(String(64), nullable=False)
    type_promo = Column(Integer, nullable=False)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    telegram_id = Column(BIGINT, nullable=False)
    user_role = Column(Integer, nullable=False)
    fio = Column(String(128), nullable=False)
    ticket_count = Column(Integer, nullable=False)


class TutorPromo(Base):
    __tablename__ = 'tutor_promo'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tutor_id = Column(Integer, nullable=False)
    promo_id = Column(Integer, nullable=False)


class TutorPromouter(Base):
    __tablename__ = 'tutor_promouter'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    tutor_id = Column(Integer, nullable=False)
    promouter_id = Column(Integer, nullable=False)


class ManagerPromo(Base):
    __tablename__ = 'manager_promo'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    manager_id = Column(Integer, nullable=False)
    promo_id = Column(Integer, nullable=False)


class ManagerTutor(Base):
    __tablename__ = 'manager_tutor'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    manager_id = Column(Integer, nullable=False)
    tutor_id = Column(Integer, nullable=False)


class SoldTickets(Base):
    __tablename__ = 'sold_tickets'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    solder_tg_id = Column(BIGINT, nullable=False)
    ticket_photo_path = Column(String(256), nullable=False)
    ticket_type = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    promo_code_name = Column(String(64), nullable=False)

