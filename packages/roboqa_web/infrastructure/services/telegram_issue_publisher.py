from roboqa_web.domain import Issue


class TelegramIssuePublisher:

    async def publish(self, issue: Issue) -> None:
        raise NotImplementedError
