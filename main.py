import config
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import *


async def main():
    bot = Bot(token=config.TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    # dp.message.register(get_name, StepsRegisterForm.GET_NAME)
    # dp.message.register(get_info, StepsRegisterForm.GET_INFO)
    # dp.message.register(get_promo, StepsRegisterForm.GET_PROMO)
    # dp.message.register(vk_getter, StepsRegisterForm.GET_VK)
    # dp.callback_query.register(get_approval1, StepsRegisterForm.GET_APPROVAL,
    #                            lambda query: query.data == 'approve_request')
    #
    # dp.callback_query.register(get_approval2, StepsRegisterForm.GET_APPROVAL,
    #                            lambda query: query.data == 'reject_request')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

