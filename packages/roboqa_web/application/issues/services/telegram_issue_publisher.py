import logging
from typing import Optional

from aiogram import Bot
from aiogram.types import LinkPreviewOptions
from typing_extensions import TypedDict

from roboqa_web.domain import Issue


class TelegramGroupOptions(TypedDict):
    tg_id: int
    topic_id: Optional[int]


class TelegramIssuePublisher:

    def __init__(self, options: TelegramGroupOptions, client: Bot):
        self._opts = options
        self._client = client

    async def publish(self, issue: Issue) -> None:
        message = await self._client.send_message(
            self._opts['tg_id'],
            text=f"<b>Проблема от {issue.author}: {issue.title}</b>\n\n"
                 f"{issue.content}\n\n"
                 f"<a href='{issue.url}'>Ссылка на GH</a>",
            message_thread_id=self._opts['topic_id'],
            link_preview_options=LinkPreviewOptions(is_disabled=True)
        )

        logging.info("Issue has been published to Telegram, message id: %s", message.message_id)
