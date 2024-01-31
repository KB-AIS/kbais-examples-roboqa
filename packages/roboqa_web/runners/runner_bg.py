import asyncio
import logging
from uuid import UUID

from celery import Celery

runner = Celery('tasks', broker='redis://localhost:6379')


@runner.task
async def handle_publish_issue(issue_uuid: str):
    await asyncio.sleep(2)
    logging.info('start')
    logging.info(issue_uuid)
    logging.info('finish')
