from typing import Optional

from redis.asyncio import Redis
from redis.commands.json.path import Path

from roboqa_web.domain.issues.issue import Issue
from roboqa_web.domain.issues.issue_repository import IssueRepository


def _get_id(id: str) -> str:
    return f"roboqa.issues:{id}"


class RedisIssueRepository(IssueRepository):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def get_by_id(self, id: str) -> Optional[Issue]:
        data = await self._redis.json().get(_get_id(id))

        if data is not None:
            return Issue.model_validate_json(data)

        return None

    async def upsert(self, issue: Issue) -> Issue:
        await self._redis.json().set(_get_id(issue.id), Path.root_path(), issue.model_dump())

        return issue
