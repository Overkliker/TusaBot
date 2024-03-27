import concurrent.futures

from aiogram import Router, F, types
import asyncio
import threading
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove, \
    FSInputFile
from aiogram import Bot
from aiogram.filters import Command, StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.orm import Session

from dto.UserAdmin import UserAdmin
from dto.UserPromouter import UserPromouter
from dto.UserTutor import UserTutor
from states import *
from text import *
from sqlalchemy import create_engine
import psycopg2
from db_models.classes import *
from dbconnect import *

from CRUD.orders_on_register import order_insert, get_order_by_telegram_id, set_status_by_telegram_id
from CRUD.users import *
from CRUD.promocodes import *
from CRUD.tutor_promo import *
from CRUD.tutor_promouter import *
from CRUD.sold_tickets import *
from CRUD.typing import *
from kb import *
from help_functions import *

engine = create_engine(connection_string, echo=True)
# admin = 785760784
router = Router()


@router.message(StateFilter(None), Command('start'))
async def start_handler(message: Message, state: FSMContext):
    """
    Начало общения с ботом
    :param message:
    :param state:
    :return:
    """
    user_id = message.from_user.id
    user_in_db = get_user_by_telegram_id(engine, user_id)

    if len(user_in_db) == 0:
        await message.answer(registrate_text1)
        await message.answer(registrate_text5)
        await state.set_state(StepsRegisterForm.GET_NAME)

    else:
        current_user = user_in_db[0]
        await state.clear()

        match current_user.user_role:
            case 1:
                pass
            case 2:
                builder = create_kb_admin_profile(user_id)
                txt = auth_admin_text1 + current_user.fio
                await message.answer(text="Рады снова видеть тебя")
                await message.answer(text=txt, reply_markup=builder.as_markup())

            case 3:
                builder = create_kb_tutor_profile(user_id)
                sold_kb = new_sold()
                txt = auth_admin_text1 + current_user.fio
                await message.answer(text="Рады снова видеть тебя", reply_markup=sold_kb)
                await message.answer(text=txt, reply_markup=builder.as_markup())

            case 4:
                builder = create_kb_promouter_profile(user_id)
                sold_kb = new_sold()
                txt = auth_admin_text1 + current_user.fio
                await message.answer(text="Рады снова видеть тебя", reply_markup=sold_kb)
                await message.answer(text=txt, reply_markup=builder.as_markup())


# Профили
@router.callback_query(F.data.startswith('profile_admin'))
async def profile_admin(callback: types.CallbackQuery):
    tg_id = int(callback.data.replace('profile_admin', ''))

    user_data = UserAdmin(tg_id, engine)

    text = generate_admin_text(user_data.user, user_data.promo_text)
    back = create_back()
    await callback.bot.send_message(chat_id=callback.message.chat.id,
                                    text=text, reply_markup=back.as_markup())


@router.callback_query(F.data.startswith('profile_promouter'))
async def profile_promouter(callback_query: CallbackQuery):
    """
    Рендер профиля промоутера
    :param callback_query:
    :return:
    """
    tg_id = int(callback_query.data.replace('profile_promouter', ''))

    user_data = UserPromouter(tg_id, engine)

    text = generate_promouter_text(user_data.user, user_data.promo_text)
    back = create_back()
    await callback_query.bot.send_message(chat_id=callback_query.message.chat.id,
                                          text=text, reply_markup=back.as_markup())


@router.callback_query(F.data.startswith('profile_tutor'))
async def profile_tutor(callback_query: CallbackQuery):
    """
    Рендер профиля куратора
    :param callback_query:
    :return:
    """
    tg_id = int(callback_query.data.replace('profile_tutor', ''))

    user_data = UserTutor(tg_id, engine)

    text = generate_tutor_text(user_data.user, user_data.sold_tickets, user_data.promo_text)
    back = create_back()
    await callback_query.bot.send_message(chat_id=callback_query.message.chat.id,
                                          text=text, reply_markup=back.as_markup())


@router.callback_query(F.data.startswith('delete'))
async def clear_message(callback_query: CallbackQuery):
    """
    Удаление сообщения по колбэку
    :param callback_query:
    :return:
    """
    chat_id = callback_query.message.chat.id
    await callback_query.bot.delete_message(chat_id=chat_id, message_id=callback_query.message.message_id)


# Регистрация
@router.message(StepsRegisterForm.GET_NAME)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(fio=name, telegram_id=message.from_user.id)
    await message.answer(registrate_text3)
    await state.set_state(StepsRegisterForm.GET_INFO)


@router.message(StepsRegisterForm.GET_INFO)
async def get_info(message: Message, state: FSMContext):
    description = message.text
    if 2 <= len(description.strip()) <= 300:
        await state.update_data(description=description)
        await message.answer(registrate_text6)

        await state.set_state(StepsRegisterForm.GET_PROMO)
    else:
        await message.answer(error_description_text)


@router.message(StepsRegisterForm.GET_PROMO)
async def get_promo(message: Message, state: FSMContext):
    promocode = message.text
    promocode_from_db = promocodes_by_name(promocode, engine)

    if len(promocode_from_db) > 0:
        await message.answer(registrate_text4)
        await state.update_data(promocode=promocode)
        await state.set_state(StepsRegisterForm.GET_VK)

    else:
        await message.answer(error_promocode_text)


@router.message(StepsRegisterForm.GET_VK)
async def vk_getter(message: Message, state: FSMContext):
    await message.answer(registrate_done_text)

    await state.update_data(vk=message.text)

    data = await state.get_data()
    order_insert(data, engine)

    text_for_admin = f"User: {data['fio']}, promo: {data['promocode']}"

    builder = create_orders_kb(data['telegram_id'])

    with concurrent.futures.ThreadPoolExecutor() as executor:
        tg_id = message.from_user.id
        future = executor.submit(get_user_by_telegram_id, engine, tg_id)
        admin = future.result().telegram_id

    await message.bot.send_message(chat_id=admin,
                                   text=text_for_admin,
                                   reply_markup=builder.as_markup()
                                   )

    await state.clear()


@router.callback_query(F.data.startswith('approve_request'))
async def get_approval1(callback: CallbackQuery):
    user_id = int(callback.data.replace('approve_request', ''))
    new_user = await connect_new_user(user_id, engine)
    if new_user:
        await callback.bot.send_message(user_id, "Ваша заявка одобрена! 🎉")
    else:
        await callback.bot.send_message(callback.from_user.id, "Этот пользователь уже зарегистрирован")


@router.callback_query(F.data.startswith('reject_request'))
async def get_approval2(callback: CallbackQuery):
    user_id = int(callback.data.replace('reject_request', ''))
    await callback.bot.send_message(user_id, "Ваша заявка отклонена. 😔")


# Сдача билета
@router.message(StateFilter(None), F.text == 'Сдать билет')
async def get_new_sold(message: Message, state: FSMContext):
    """
    Выбор типа билета
    :param message:
    :param state:
    :return:
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        tg_id = message.from_user.id
        role = executor.submit(get_user_by_telegram_id, engine, tg_id)
        role_res = role.result()[0].user_role

    if role_res == 4 or role_res == 3:
        get_kb = kb_types()
        await message.bot.send_message(chat_id=message.chat.id, text="Выберите тип билета", reply_markup=get_kb)
        await state.set_state(PassTicketForm.GET_TYPE)

    else:
        await message.answer("Вы не промоутер")
        await state.clear()


@router.message(PassTicketForm.GET_TYPE)
async def get_type_ticket(message: Message, state: FSMContext):
    """
    Получение типа билета
    :param message:
    :param state:
    :return:
    """
    type_ticket = message.text

    if type_ticket == 'VIP':
        await state.update_data(type_ticket=1)
        await message.answer("Отправьте фото билета")
        await state.set_state(PassTicketForm.GET_PHOTO)

    elif type_ticket == 'Standard':
        await state.update_data(type_ticket=2)
        await message.answer("Отправьте фото билета")
        await state.set_state(PassTicketForm.GET_PHOTO)

    else:
        await message.answer("Такого типа нету")


@router.message(PassTicketForm.GET_PHOTO)
async def get_ticket_photo(message: Message, state: FSMContext):
    """
    Принятие фотографии билета от пользователя
    :param message:
    :param state:
    :return:
    """
    if message.photo:
        ticket_type = await state.get_data()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            tg_id = message.from_user.id

            future = executor.submit(get_user_by_telegram_id, engine, tg_id)
            user = future.result()[0]

            if user.user_role == promouter:
                future = executor.submit(get_tutor_by_promouter_id, engine, user.id)
                tutor_id = future.result().tutor_id

                future = executor.submit(get_promo_by_tutor_id, engine, tutor_id)
                promo_code_id = future.result().id

                future = executor.submit(promocode_by_id, promo_code_id, engine)
                promo_code_name = future.result().text_promo

            elif user.user_role == tutor:
                future = executor.submit(get_promo_by_tutor_id, engine, user.id)
                promo_code_id = future.result().id

                future = executor.submit(promocode_by_id, promo_code_id, engine)
                promo_code_name = future.result().text_promo

            photo = message.photo[-1].file_id
            file_name = f"tickets/{photo}.jpg"
            await message.bot.download(photo, destination=file_name)

            ticket = SoldTickets(
                solder_tg_id=tg_id,
                ticket_photo_path=file_name,
                ticket_type=ticket_type["type_ticket"],
                status=in_processing,
                promo_code_name=promo_code_name
            )
            future = executor.submit(insert_new_sold_ticket, engine, ticket)

        last_ticket_for_user = get_last_ticket_for_user(engine, tg_id).id
        if user.user_role == tutor:
            random_tutor = get_random_tutor(engine, tg_id).telegram_id
            in_kb = create_sold_orders_kb(tg_id, last_ticket_for_user)
            await message.bot.send_photo(chat_id=random_tutor,
                                         photo=FSInputFile(file_name),
                                         reply_markup=in_kb.as_markup())

        elif user.user_role == promouter:
            tg_id_tutor = get_user_by_id(engine, tutor_id).telegram_id
            in_kb = create_sold_orders_kb(tg_id, last_ticket_for_user)
            await message.bot.send_photo(chat_id=tg_id_tutor,
                                         photo=FSInputFile(file_name),
                                         reply_markup=in_kb.as_markup())

        sold_kb = new_sold()
        await message.bot.send_message(chat_id=message.chat.id,
                                       text="Заявка отправлена на проверку",
                                       reply_markup=sold_kb)
        await state.clear()


@router.callback_query(F.data.startswith('approve_request_sold'))
async def get_approval_sold_approve(callback: CallbackQuery):
    user_and_ticket = callback.data.replace('approve_request_sold', '').split('_')
    set_status = await change_status_to_sold(engine, user_and_ticket[-1], sold)
    if set_status:
        await callback.bot.delete_message(chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id)
        await callback.bot.send_message(user_and_ticket[0], "Ваша продажа одобрена! 🎉")
    else:
        await callback.bot.delete_message(chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id)
        await callback.bot.send_message(callback.from_user.id, "Что-то пошло не так...")


@router.callback_query(F.data.startswith('reject_request_sold'))
async def get_approval_sold_reject(callback: CallbackQuery):
    user_and_ticket = callback.data.replace('reject_request_sold', '').split('_')
    set_status = await change_status_to_sold(engine, user_and_ticket[-1], cancelled)
    if set_status:
        await callback.bot.delete_message(chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id)
        await callback.bot.send_message(user_and_ticket[0], "Ваша продажа отклонена. 😔")
    else:
        await callback.bot.delete_message(chat_id=callback.message.chat.id,
                                          message_id=callback.message.message_id)
        await callback.bot.send_message(callback.from_user.id, "Что-то пошло не так...")


# Статистика по промокодам

@router.callback_query(F.data.startswith('promo_state'))
async def get_promo_state(callback: CallbackQuery):
    state_promo = await create_text_promo_state(engine)
    kb_back = create_back()
    await callback.bot.send_message(chat_id=callback.message.chat.id,
                                    text=state_promo,
                                    reply_markup=kb_back.as_markup())


# Статистика по пользователям
@router.callback_query(F.data.startswith('solt'))
async def get_promo_state(callback: CallbackQuery):
    state_users = await create_text_users_state(engine)
    kb_back = create_back()
    await callback.bot.send_message(chat_id=callback.message.chat.id,
                                    text=state_users,
                                    reply_markup=kb_back.as_markup())

