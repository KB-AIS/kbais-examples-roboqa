from typing import Optional

from pydantic import BaseModel

from roboqa_web.application.services.issue_publisher import IssuePublisher
from roboqa_web.domain import IssueRepository, Issue


class IssueRegisterCommand(BaseModel):
    title: str
    author_name: Optional[str]
    is_issue: Optional[bool]
    content: Optional[str]


class IssueRegisterUseCase:
    def __init__(
        self,
        issue_repository: IssueRepository,
        issue_publisher: IssuePublisher
    ):
        self._issue_repository = issue_repository
        self._issue_publisher = issue_publisher

    async def execute(self, cmd: IssueRegisterCommand) -> str:
        issue = await self._issue_repository.upsert(Issue(
            title=cmd.title,
            author=cmd.author_name,
            content=cmd.content,
        ))

        self._issue_publisher.issue_registered(issue.id)

        return issue.id
