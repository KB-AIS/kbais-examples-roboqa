import logging

from redis.asyncio import Redis

from roboqa_web.application.core.usecase import UseCase


class IssuePublishToGithubUseCase(UseCase[str, None]):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def execute(self, cmd: str) -> None:
        await self._redis.mset({"Croatia": "Zagreb", "Bahamas": cmd})

        logging.info(await self._redis.get("Bahamas"))

        return None
