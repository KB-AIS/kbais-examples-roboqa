import asyncio

from roboqa_web.application.core.usecase import UseCase


class IssuePublishToTelegramUseCase(UseCase[str, None]):
    def __init__(self):
        ...

    async def execute(self, cmd) -> None:
        ...
