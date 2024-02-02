from typing import TypedDict

from gql import gql
from gql.client import AsyncClientSession

from roboqa_web.domain.issues.issue import Issue

_create_issue_mut = gql(
    """
    mutation ($api_id: ID!, $title: String!, $body: String!) {
        addProjectV2DraftIssue(
            input: { projectId: $api_id, title: $title, body: $body }
        ) {
            projectItem { id databaseId }
        }
    }
    """
)


class GithubProjectOptions(TypedDict):
    owner: str
    gh_id: int
    gh_api_id: str


class GithubIssuePublisher:
    def __init__(self, options: GithubProjectOptions, client: AsyncClientSession):
        self._opts = options
        self._client = client

    async def publish(self, issue: Issue) -> str:
        """
        Опубликовать проблему на github
        :issue Проблема для публикации на github
        :return: URL новой проблемы на github
        """
        # TODO: Handle error result
        result = await self._client.execute(
            _create_issue_mut,
            variable_values=dict(api_id=self._opts["gh_api_id"], title=issue.title, body=issue.content)
        )

        issue_gh_id = result["addProjectV2DraftIssue"]["projectItem"]["databaseId"]

        return self._compose_issue_url(issue_gh_id)

    def _compose_issue_url(self, issue_gh_id) -> str:
        issue_url = (f"https://github.com/{self._opts['owner']}/projects/"
                     f"{self._opts['gh_id']}"
                     f"?pane=issue"
                     f"&itemId={issue_gh_id}")

        return issue_url
