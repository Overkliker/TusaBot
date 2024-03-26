import concurrent.futures

from CRUD.users import *
from CRUD.tutor_promo import *
from CRUD.promocodes import *
from CRUD.tutor_promouter import *
from CRUD.orders_on_register import *
from CRUD.manager_tutor import *
from CRUD.manager_promo import *


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


def generate_promouter_text(user):
    text = f"Профиль \n Ваш ID: {user.telegram_id} \n Проданные билеты: {user.ticket_count} \n"
    return text


async def new_tutor_for_manager(user_id, promocode_id, engine):
    try:
        tutor_id = get_user_by_telegram_id(engine, user_id).id
        manager_id = get_manager_by_promo(engine, promocode_id).tutor_id

        insert_new_tutor(tutor_id, manager_id, engine)

    except Exception as ex:
        print(ex)