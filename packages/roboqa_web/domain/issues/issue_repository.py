from abc import ABC, abstractmethod
from typing import Optional

from roboqa_web.domain.issues.issue import Issue


class IssueRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Issue]:
        raise NotImplementedError

    @abstractmethod
    async def upsert(self, issue: Issue) -> Issue:
        raise NotImplementedError


