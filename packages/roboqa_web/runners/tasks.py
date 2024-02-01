import logging
import sys

import dramatiq
from dependency_injector.wiring import inject, Provide
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from roboqa_web.application.usecases import UseCase
from roboqa_web.infrastructure.containers import ApplicationContainer


@dramatiq.actor(max_retries=None, min_backoff=500, max_backoff=1000)
@inject
async def handle_publish_issue_to_github(
        issue_uuid: str,
        use_case: UseCase[str, None] = Provide[ApplicationContainer.publishToGithubUseCase]
):
    await use_case.execute(issue_uuid)

    handle_publish_issue_to_telegram.send(issue_uuid)


@dramatiq.actor(max_retries=None, min_backoff=500, max_backoff=1000)
@inject
async def handle_publish_issue_to_telegram(
        issue_uuid: str,
        use_case: UseCase[str, None] = Provide[ApplicationContainer.publishToTelegramUseCase]
):
    await use_case.execute(issue_uuid)


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    container = ApplicationContainer()
    container.wire(modules=[__name__])
    # "redis://localhost:6379"

    redis_connection_string = container.config.get("infrastructure.data.redis.connection_string")

    broker = RedisBroker(url=redis_connection_string)

    dramatiq.set_broker(broker)
    dramatiq.get_broker().add_middleware(AsyncIO())

    dramatiq.get_broker().declare_actor(handle_publish_issue_to_github)
    dramatiq.get_broker().declare_actor(handle_publish_issue_to_telegram)

