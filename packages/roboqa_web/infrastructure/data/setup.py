from typing import AsyncIterator

from redis.asyncio import Redis, from_url


async def setup_redis_pool(host: str) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{host}", encoding="utf-8", decode_responses=True)

    yield session

    session.close()

    await session.wait_closed()
