import logging
import sys

import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from roboqa_web.infrastructure.worker.container import ContainerWorker
from roboqa_web.infrastructure.worker.tasks import issue_publish_tg_task, issue_publish_gh_task


def run():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    runner_container = ContainerWorker()

    runner_composer = RedisBroker(url=runner_container.core.config.get("infrastructure.data.redis_url"))
    runner_composer.add_middleware(AsyncIO())
    runner_composer.declare_actor(issue_publish_tg_task)
    runner_composer.declare_actor(issue_publish_gh_task)

    dramatiq.set_broker(runner_composer)
