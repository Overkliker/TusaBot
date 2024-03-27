import concurrent.futures
from CRUD.users import *
from CRUD.promocodes import *
from CRUD.tutor_promo import *
from CRUD.tutor_promouter import *
from CRUD.sold_tickets import *
from CRUD.manager_promo import *


class UserTutor:
    def __init__(self, tg_id, engine):
        self.tg_id = tg_id

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(get_user_by_telegram_id, engine, tg_id)
            self.user = future.result()[0]

            future = executor.submit(get_promo_by_tutor_id, engine, self.user.id)
            self.promo_code_id = future.result().id

            future = executor.submit(promocode_by_id, self.promo_code_id, engine)
            self.promo_text = future.result().text_promo

            future = executor.submit(get_count_of_sold_for_promo, engine, self.promo_text)
            self.sold_tickets = future.result()
