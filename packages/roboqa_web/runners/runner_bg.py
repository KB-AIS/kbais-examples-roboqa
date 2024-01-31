from typing import AsyncIterator

import dramatiq
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO
from redis.asyncio import Redis, from_url

from roboqa_web.application import usecases
from roboqa_web.application.usecases import UseCase

broker = RedisBroker(url="redis://localhost:6379")

dramatiq.set_broker(broker)
dramatiq.get_broker().add_middleware(AsyncIO())


class Service:
    def __init__(self, payload: str):
        self.payload = payload


async def init_redis_pool(host: str) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{host}", encoding="utf-8", decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()


class Container(containers.DeclarativeContainer):
    service = providers.Factory(Service, "Hello, World")

    redis_pool = providers.Resource(
        init_redis_pool,
        host="localhost:6379"
    )

    publishToGithubUseCase = providers.Factory(
        usecases.PublishToGithubUseCase,
        redis=redis_pool,
    )

    publishToTelegramUseCase = providers.Factory(
        usecases.PublishToTelegramUseCase
    )


@dramatiq.actor(max_retries=None, min_backoff=500, max_backoff=1000)
@inject
async def handle_publish_issue_to_github(
        issue_uuid: str,
        use_case: UseCase[str, None] = Provide[Container.publishToGithubUseCase]
):
    await use_case.execute(issue_uuid)

    handle_publish_issue_to_telegram.send(issue_uuid)


@dramatiq.actor(max_retries=None, min_backoff=500, max_backoff=1000)
@inject
async def handle_publish_issue_to_telegram(
        issue_uuid: str,
        use_case: UseCase = Provide[Container.publishToTelegramUseCase]
):
    raise NotImplementedError()


container = Container()
container.wire(modules=[__name__])
