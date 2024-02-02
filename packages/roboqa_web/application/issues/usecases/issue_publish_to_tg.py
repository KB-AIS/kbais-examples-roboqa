import logging

from roboqa_web.application.core.usecase import UseCase
from roboqa_web.application.issues.services.telegram_issue_publisher import TelegramIssuePublisher
from roboqa_web.domain import IssueRepository


class IssuePublishToTelegramUseCase(UseCase[str, None]):
    def __init__(
        self,
        issue_repository: IssueRepository,
        issue_publisher: TelegramIssuePublisher
    ):
        self._repo = issue_repository
        self._publisher = issue_publisher

    async def execute(self, issue_id) -> None:
        issue = await self._repo.get_by_id(issue_id)

        if issue is None:
            logging.warning("Issue has not been found by provided id: %s", issue_id)

            return None

        await self._publisher.publish(issue)

        return None
