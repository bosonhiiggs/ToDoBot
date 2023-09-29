import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import welcome, todo, notes
from config_reader import config


async def main():
    """
    Main func с параметрами логирования
    :return: start polling
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(
        welcome.router,
        todo.router,
        notes.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

