from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command('start'))
async def start_handler(message: Message):
    await message.answer('Hi, that your id')


@router.message()
async def message_handler(message: Message):
    await message.answer(str(message.from_user.id))