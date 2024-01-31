import abc
import asyncio
import logging
from typing import TypeVar, Generic

from redis.asyncio import Redis

TCmd = TypeVar('TCmd')
TRes = TypeVar('TRes')


class UseCase(abc.ABC, Generic[TCmd, TRes]):

    @abc.abstractmethod
    async def execute(self, cmd: TCmd) -> TRes:
        ...


class Issue:
    ...


class IssueRepository:
    def get_by_uuid(self):
        ...


class PublishToGithubUseCase(UseCase[str, None]):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def execute(self, cmd: str) -> None:
        await self._redis.mset({"Croatia": "Zagreb", "Bahamas": cmd})

        logging.info(await self._redis.get("Bahamas"))

        return None


class PublishToTelegramUseCase(UseCase):
    def __init__(self):
        ...

    async def execute(self, cmd) -> asyncio.Task[None]:
        ...
