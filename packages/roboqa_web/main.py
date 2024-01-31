import asyncio
import logging
import sys
import uuid
from typing import Annotated, AsyncIterator, TypedDict, Optional

import uvicorn
from aiogram import Bot
from aiogram.enums import ParseMode
from fastapi import FastAPI, APIRouter, Depends
from gql import Client, gql
from gql.client import AsyncClientSession
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import BaseModel, TypeAdapter, Field
from starlette.middleware.cors import CORSMiddleware

from roboqa_web.config import AppConfig, TomlAppConfig
from roboqa_web.runners.runner_bg import handle_publish_issue

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


def get_app_config() -> AppConfig:
    return TomlAppConfig()


class GithubProjectInfo(TypedDict):
    owner: str
    project_id: int
    project_node: str


def get_github_project_info(
        app_config: Annotated[AppConfig, Depends(get_app_config)]
) -> GithubProjectInfo:
    return TypeAdapter(GithubProjectInfo) \
        .validate_python(app_config.get_value(['integrations', 'github', 'project']))


class GithubClientConfig(TypedDict):
    api_key: str


def get_github_client_config(
        app_config: Annotated[AppConfig, Depends(get_app_config)]
) -> GithubClientConfig:
    return TypeAdapter(GithubClientConfig) \
        .validate_python(app_config.get_value(['integrations', 'github']))


class GithubProjectsService:
    def __init__(self, gh_project: GithubProjectInfo, gh_client: AsyncClientSession):
        self.project_info = gh_project
        self._gh_client = gh_client

    async def create_issue(self, title: str, content: str) -> int:
        """
        Создать черновик проблемы в проекте
        :param title: Заголовок проболемы
        :param content: Текстовое описание проблемы
        :return: Идентификатор новой проблемы
        """

        create_issue_mutation = gql(
            '''
            mutation ($project_id: ID!, $title: String!, $body: String!) {
                addProjectV2DraftIssue(
                    input: { projectId: $project_id, title: $title, body: $body }
                ) {
                    projectItem {
                        id
                        databaseId
                    }
                }
            }
            '''
        )

        result = await self._gh_client.execute(
            create_issue_mutation,
            variable_values={
                'project_id': self.project_info['project_node'],
                'title': title,
                'body': content
            }
        )

        return result['addProjectV2DraftIssue']['projectItem']['databaseId']


async def get_github_project_service(
        gh_client_config: Annotated[GithubClientConfig, Depends(get_github_client_config)],
        gh_project_info: Annotated[GithubProjectInfo, Depends(get_github_project_info)]
) -> AsyncIterator[GithubProjectsService]:
    github_client_transport = AIOHTTPTransport(
        url='https://api.github.com/graphql',
        headers={
            f'Authorization': f'Bearer {gh_client_config['api_key']}'
        }
    )

    async with Client(transport=github_client_transport) as client:
        yield GithubProjectsService(gh_project_info, client)


class TelegramClientConfig(TypedDict):
    api_key: str
    group_id: int


def get_telegram_client_config(
        app_config: Annotated[AppConfig, Depends(get_app_config)]
) -> TelegramClientConfig:
    return TypeAdapter(TelegramClientConfig) \
        .validate_python(app_config.get_value(['integrations', 'telegram']))


def get_telegram_client(
        tg_client_config: Annotated[TelegramClientConfig, Depends(get_telegram_client_config)]
) -> Bot:
    return Bot(tg_client_config['api_key'], parse_mode=ParseMode.HTML)


class IssueInfo:
    ...


class TelegramNotificator:
    def __init__(self, tg_client: Bot):
        self._tg_client = tg_client

    def notify_new_issue_created(self, issue: IssueInfo):
        # await tg_bot.send_message(
        #     app_config['integrations']['telegram']['chat_id'],
        #     text=
        #     f"""<b>Проблема от {req.author_name}</b>\n{req.content}\n<a href="{issue_url}">Задача на GH</a>""",
        #     link_preview_options=LinkPreviewOptions(is_disabled=True)
        # )
        ...


issues_router = APIRouter(prefix="/api/v1/issues")


class FeedbackRequestDto(BaseModel):
    title:      str
    authorName: Optional[str]  = Field(default=None)
    isIssue:    Optional[bool] = Field(default=None)
    content:    Optional[str]  = Field(default=None)


@issues_router.get("/bg")
async def handle_bg():
    handle_publish_issue.delay(str(uuid.uuid4()))


@issues_router.post('/')
async def handle_issue_register(
        req: FeedbackRequestDto,
        project_service: Annotated[GithubProjectsService, Depends(get_github_project_service)]
):
    issue_id = await project_service.create_issue(req.title, req.content)

    issue_url = (f"https://github.com/{project_service.project_info["owner"]}/projects/"
                 f"{project_service.project_info['project_id']}"
                 f"?pane=issue"
                 f"&itemId={issue_id}")

    return issue_url


def setup_app_composer() -> FastAPI:
    app_composer = FastAPI()
    app_composer.include_router(issues_router)

    app_composer.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_composer


async def run_async():
    app_config = uvicorn.Config("roboqa_web.main:setup_app_composer", host='0.0.0.0', port=5000, log_level="debug")
    app_runner = uvicorn.Server(app_config)


    await app_runner.serve()


def run():
    asyncio.run(run_async())


if __name__ == "__main__":
    run()
