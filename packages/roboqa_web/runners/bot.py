import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

dp = Dispatcher()


@dp.update()
async def handle(message: Message):
    ...


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.chat.id)}!")


async def run_async():
    tg_bot = Bot('')

    await dp.start_polling(tg_bot)


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(run_async())


if __name__ == "__main__":
    run()
