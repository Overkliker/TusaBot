from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def create_orders_kb(telegram_id: int) -> InlineKeyboardBuilder:
    approve = 'approve_request' + str(telegram_id)
    reject = 'reject_request' + str(telegram_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Одобрить",
        callback_data=approve)
    )

    builder.add(InlineKeyboardButton(
        text="Отклонить",
        callback_data=reject)
    )

    return builder


def create_sold_orders_kb(telegram_id: int, order_id: int) -> InlineKeyboardBuilder:
    approve = 'approve_request_sold' + str(telegram_id) + '_' + str(order_id)
    reject = 'reject_request_sold' + str(telegram_id) + '_' + str(order_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Одобрить",
        callback_data=approve)
    )

    builder.add(InlineKeyboardButton(
        text="Отклонить",
        callback_data=reject)
    )

    return builder


def create_kb_promouter_profile(telegram_id: int) -> InlineKeyboardBuilder:
    profile = 'profile_promouter' + str(telegram_id)
    materials = 'materials' + str(telegram_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="\U0001F935 Профиль",
        callback_data=profile)
    )

    builder.row(InlineKeyboardButton(
        text="\U0001F4DA Материалы",
        callback_data=materials)
    )

    return builder


def create_kb_tutor_profile(telegram_id: int) -> InlineKeyboardBuilder:
    profile = 'profile_tutor' + str(telegram_id)
    materials = 'materials' + str(telegram_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="\U0001F935 Профиль",
        callback_data=profile)
    )

    builder.row(InlineKeyboardButton(
        text="\U0001F4DA Материалы",
        callback_data=materials)
    )

    return builder


def create_kb_admin_profile(telegram_id: int) -> InlineKeyboardBuilder:
    profile = 'profile_admin' + str(telegram_id)
    materials = 'materials' + str(telegram_id)
    solt = 'solt' + str(telegram_id)
    promo_state = 'promo_state' + str(telegram_id)
    crud_promo = 'crud_promo' + str(telegram_id)
    crud_crews = 'crud_crews' + str(telegram_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="\U0001F935 Профиль",
        callback_data=profile)
    )

    builder.add(InlineKeyboardButton(
        text="\U0001F4DA Материалы",
        callback_data=materials)
    )

    builder.row(InlineKeyboardButton(
        text="Продажи",
        callback_data=solt)
    )

    builder.row(InlineKeyboardButton(
        text="Статистика по промокодам",
        callback_data=promo_state)
    )

    builder.row(InlineKeyboardButton(
        text="Промокоды",
        callback_data=crud_promo)
    )

    builder.row(InlineKeyboardButton(
        text="Составы",
        callback_data=crud_crews)
    )

    return builder


def create_back() -> InlineKeyboardBuilder:
    delete = 'delete'

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="\U00002B05 Назад",
        callback_data=delete)
    )

    return builder


def kb_types() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(KeyboardButton(text='VIP'))
    keyboard.add(KeyboardButton(text='Standard'))
    return keyboard.as_markup()


def new_sold() -> ReplyKeyboardMarkup:
    kb = [[
        KeyboardButton(text='Сдать билет')
    ]]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=kb)
    return keyboard

