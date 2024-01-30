import asyncio
import logging
import sys

from aiogram import Bot
from apscheduler import AsyncScheduler
from apscheduler.triggers.cron import CronTrigger

tg_bot = Bot('')


async def handle_daily_duty():
    pass


async def main_async():
    async with AsyncScheduler() as scheduler:
        await scheduler.add_schedule(handle_daily_duty, CronTrigger(minute='*/5', timezone='Asia/Krasnoyarsk'))
        await scheduler.run_until_stopped()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    asyncio.run(main_async())
