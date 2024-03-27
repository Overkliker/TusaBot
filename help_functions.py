import concurrent.futures

from CRUD.users import *
from CRUD.tutor_promo import *
from CRUD.promocodes import *
from CRUD.tutor_promouter import *
from CRUD.orders_on_register import *
from CRUD.manager_tutor import *
from CRUD.manager_promo import *
from CRUD.sold_tickets import *
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table


async def change_status_to_sold(engine, sold_ticket_id, status):
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(change_status_to_sold, engine, sold_ticket_id, status)
            if future.done():
                return True

    except Exception as e:
        return False

async def connect_new_user(user_id, engine):
    order = get_order_by_telegram_id(engine, user_id)

    if order.status != 1:
        promocode = promocode_by_name(order.promocode, engine)
        set_status_by_telegram_id(engine, user_id, 1)

        if promocode.type_promo == manager_promo:
            insert_users(
                data=order,
                engine=engine,
                role=tutor
            )
            await new_tutor_for_manager(user_id, promocode.id, engine)

        elif promocode.type_promo == tutor_promo:
            insert_users(
                data=order,
                engine=engine,
                role=promouter
            )
            await new_promouter_for_tutor(user_id, promocode.id, engine)
            return True

    else:
        return False


async def new_promouter_for_tutor(user_id, promocode_id, engine):
    try:
        promouter_id = get_user_by_telegram_id(engine, user_id).id
        tutor_id = get_tutor_by_promo(engine, promocode_id).tutor_id

        insert_new_promouter(tutor_id, promouter_id)

    except Exception as ex:
        print(ex)


def generate_promouter_text(user, promo_text):
    text = (f"Профиль \n Ваш ID: {user.telegram_id} \nВаш промокод: {promo_text}"
            f" \n Проданные билеты: {user.ticket_count} \n")
    return text


def generate_tutor_text(user, count_for_promo, promo_text):
    text = (f"Профиль \n\nВаш ID: {user.telegram_id} \nВаш промокод: {promo_text}"
            f" \nПроданные билеты: {user.ticket_count}"
            f" \nПродаж по промокоду: {count_for_promo}")
    return text


def generate_admin_text(user, promo_text):
    text = f"Профиль \n\nВаш ID: {user.telegram_id} \nВаш промокод: {promo_text}"
    return text


async def new_tutor_for_manager(user_id, promocode_id, engine):
    try:
        tutor_id = get_user_by_telegram_id(engine, user_id).id
        manager_id = get_manager_by_promo(engine, promocode_id).tutor_id

        insert_new_tutor(tutor_id, manager_id, engine)

    except Exception as ex:
        print(ex)


async def create_text_promo_state(engine):
    try:
        state_text = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(get_tutors_promocodes, engine)
            promo_codes = future.result()

        for promo_code in promo_codes:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(get_count_of_sold_for_promo, engine, promo_code.text_promo)
                count = future.result()

                state_text += f"{promo_code.text_promo} --- {count}"

        return state_text

    except Exception as ex:
        return "Пока что статистики нету"


async def create_text_users_state(engine):
    try:
        state_text = ''
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(get_tutors_and_promouters, engine)
            users = future.result()

        for user in users:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(get_count_of_sold_for_user, engine, user.telegram_id)
                count = future.result()

                state_text += f"{user.fio} --- {user.telegram_id} --- {count}"

        return state_text

    except Exception as ex:
        return "Пока что статистики нету"