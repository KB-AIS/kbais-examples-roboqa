import logging

from roboqa_web.application.core.usecase import UseCase
from roboqa_web.application.issues.services.github_issue_publisher import GithubIssuePublisher
from roboqa_web.domain import IssueRepository


class IssuePublishToGithubUseCase(UseCase[str, None]):
    def __init__(
        self,
        issue_repository: IssueRepository,
        issue_publisher: GithubIssuePublisher
    ):
        self._repo = issue_repository
        self._publisher = issue_publisher

    async def execute(self, issue_id: str) -> None:
        issue = await self._repo.get_by_id(issue_id)

        if issue is None:
            logging.warning("Issue has not been found by provided id: %s", issue_id)

            return None

        issue.url = await self._publisher.publish(issue)

        await self._repo.upsert(issue)

        logging.info("Issue has been published to GitHub with URL: %s", issue.url)

        return None
