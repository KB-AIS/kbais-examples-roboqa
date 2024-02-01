from typing import TypedDict

from gql import gql
from gql.client import AsyncClientSession

from roboqa_web.domain.issues.issue import Issue


class GithubProjectOptions(TypedDict):
    owner: str
    project_id: int
    project_api_id: str


class GithubIssuePublisher:
    def __init__(self, options: GithubProjectOptions, client: AsyncClientSession):
        self._options = options
        self._client = client

    async def publish(self, issue: Issue) -> int:
        """
        Опубликовать проблему на github
        :issue Проблема для публикации на github
        :return: Идентификатор новой проблемы на github
        """

        create_issue_mutation = gql(
            """
            mutation ($project_id: ID!, $title: String!, $body: String!) {
                addProjectV2DraftIssue(
                    input: { projectId: $project_id, title: $title, body: $body }
                ) {
                    projectItem { id databaseId }
                }
            }
            """
        )

        result = await self._client.execute(
            create_issue_mutation,
            variable_values=dict(
                project_id=self._options["project_api_id"],
                title=issue.title,
                body=issue.content
            )
        )

        return result["addProjectV2DraftIssue"]["projectItem"]["databaseId"]
