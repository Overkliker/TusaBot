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
    promo_codes = 'promo_codes' + str(telegram_id)
    materials = 'materials' + str(telegram_id)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="\U0001F935 Профиль",
        callback_data=profile)
    )

    builder.row(InlineKeyboardButton(
        text="\U0001F3F7 Промокоды",
        callback_data=promo_codes)
    )

    builder.row(InlineKeyboardButton(
        text="\U0001F4DA Материалы",
        callback_data=materials)
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

