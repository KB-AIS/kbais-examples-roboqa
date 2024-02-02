from typing import Optional

from pydantic import BaseModel

from roboqa_web.application.issues.services.issue_publisher import IssueSender
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
        issue_sender: IssueSender
    ):
        self._repo = issue_repository
        self._sender = issue_sender

    async def execute(self, cmd: IssueRegisterCommand) -> str:
        issue = await self._repo \
            .upsert(Issue(title=cmd.title, author=cmd.author_name, content=cmd.content))

        self._sender.registered(issue.id)

        return issue.id
