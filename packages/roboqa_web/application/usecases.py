import abc
import asyncio
import logging

from redis.asyncio import Redis


class UseCase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def execute(self, cmd):
        ...


class Issue:
    ...


class IssueRepository:
    def get_by_uuid(self):
        ...


class PublishToGithubUseCase(UseCase):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def execute(self, cmd: str):
        await self._redis.mset({"Croatia": "Zagreb", "Bahamas": cmd})

        logging.info(await self._redis.get("Bahamas"))

        return None


class PublishToTelegramUseCase(UseCase):
    def __init__(self):
        ...

    async def execute(self, cmd) -> asyncio.Task[None]:
        ...
