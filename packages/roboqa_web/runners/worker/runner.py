import logging
import sys

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from roboqa_web.infrastructure.worker.container import ContainerWorker
from roboqa_web.infrastructure.worker.tasks import issue_publish_tg_task, issue_publish_gh_task


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    container = ContainerWorker()

    broker = RedisBroker(url=container.config.get("infrastructure.data.redis_url"))

    broker.add_middleware(AsyncIO())

    broker.declare_actor(issue_publish_tg_task)
    broker.declare_actor(issue_publish_gh_task)

    dramatiq.set_broker(broker)
