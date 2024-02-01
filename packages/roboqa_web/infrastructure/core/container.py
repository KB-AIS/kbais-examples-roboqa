import tomllib
from typing import TypedDict, AsyncIterator

import redis.asyncio as r
from dependency_injector import containers, providers


def _load_config() -> dict:
    with open("config.toml", "rb") as f:
        app_config = tomllib.load(f)

        return app_config


async def get_redis_pool(url: str) -> AsyncIterator[r.Redis]:
    session = r.from_url(url, encoding="utf-8", decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()


class ContainerCore(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(_load_config())

    redis_pool = providers.Resource(
        get_redis_pool,
        url=config.infrastructure.data.redis_url
    )


class Config(containers.DeclarativeContainer):
    config = providers.Configuration()


class GithubClientOptions(TypedDict):
    api_key: str


class TelegramClientOptions(TypedDict):
    api_key: str
    group_id: int
