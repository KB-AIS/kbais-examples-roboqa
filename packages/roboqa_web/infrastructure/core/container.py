import tomllib
from typing import AsyncIterator, Iterator

import redis as r_s
import redis.asyncio as r_a
from dependency_injector import containers, providers
from dramatiq.brokers.redis import RedisBroker
from dramatiq.rate_limits.backends import RedisBackend


def _load_config() -> dict:
    with open("config.toml", "rb") as f:
        app_config = tomllib.load(f)

        return app_config


async def _setup_redis_async_client(url: str) -> AsyncIterator[r_a.Redis]:
    session = r_a.from_url(url, encoding="utf-8", decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()


def _setup_redis_sync_client(url: str) -> Iterator[r_s.Redis]:
    """
    Синхронный клиент Redis для dramatiq
    :param url:
    :return:
    """
    session: r_s.Redis = r_s.from_url(url)
    yield session
    session.close()


def _setup_dq_broker(
    url: str
):
    dq_broker = RedisBroker(url=url)

    return dq_broker


class ContainerCore(containers.DeclarativeContainer):
    config = providers.Configuration()

    config.from_dict(_load_config())

    # Infrastructure

    redis_async = providers.Resource(
        _setup_redis_async_client,
        url=config.infrastructure.data.redis_url
    )

    redis_client_sync = providers.Resource(
        _setup_redis_sync_client,
        url=config.infrastructure.data.redis_url,
    )

    dq_rate_limit_backend = providers.Singleton(
        RedisBackend,
        client=redis_client_sync
    )

    dq_broker = providers.Singleton(
        _setup_dq_broker,
        url=config.infrastructure.data.redis_url
    )
