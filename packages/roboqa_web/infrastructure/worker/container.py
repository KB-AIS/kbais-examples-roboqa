from typing import AsyncIterator

from aiogram import Bot
from aiogram.enums import ParseMode
from dependency_injector import containers, providers
from dramatiq.rate_limits import ConcurrentRateLimiter
from gql.client import Client, AsyncClientSession
from gql.transport.aiohttp import AIOHTTPTransport
from pydantic import TypeAdapter
from typing_extensions import TypedDict

from roboqa_web.application.issues.services.github_issue_publisher import GithubIssuePublisher, GithubProjectOptions
from roboqa_web.application.issues.services.telegram_issue_publisher import TelegramIssuePublisher, TelegramGroupOptions
from roboqa_web.application.issues.usecases.issue_publish_to_gh import IssuePublishToGithubUseCase
from roboqa_web.application.issues.usecases.issue_publish_to_tg import IssuePublishToTelegramUseCase
from roboqa_web.infrastructure.core.container import ContainerCore
from roboqa_web.infrastructure.services import RedisIssueRepository


class GithubClientOptions(TypedDict):
    api_key: str


async def _setup_github_client_session(
        opts: GithubClientOptions
) -> AsyncIterator[AsyncClientSession]:
    github_client_transport = AIOHTTPTransport(
        url='https://api.github.com/graphql',
        headers={
            f"Authorization": f"Bearer {opts['api_key']}"
        }
    )

    async with Client(transport=github_client_transport) as session:
        yield session


def _setup_tg_client(api_key: str) -> Bot:
    return Bot(api_key, parse_mode=ParseMode.MARKDOWN_V2)


class ContainerWorker(containers.DeclarativeContainer):
    core = providers.Container(ContainerCore)

    # wiring_config = containers.WiringConfiguration(packages=["roboqa_web.infrastructure.worker"])

    # Domain

    issue_repository = providers.Factory(RedisIssueRepository, redis=core.redis_async)

    dq_issue_publish_rl = providers.Singleton(
        ConcurrentRateLimiter,
        backend=core.dq_rate_limit_backend,
        key="issue-publish-mux", limit=2, ttl=1_000
    )

    # Application

    gh_project_opts = providers.Singleton(
        TypeAdapter(GithubProjectOptions).validate_python,
        core.config.integrations.github.project
    )

    gh_client_opts = providers.Singleton(
        TypeAdapter(GithubClientOptions).validate_python,
        core.config.integrations.github
    )

    gh_client = providers.Resource(
        _setup_github_client_session,
        opts=gh_client_opts
    )

    gh_issue_publisher = providers.Singleton(
        GithubIssuePublisher,
        options=gh_project_opts,
        client=gh_client
    )

    tg_client = providers.Singleton(
        _setup_tg_client,
        api_key=core.config.integrations.telegram.api_key
    )

    tg_issue_publisher = providers.Singleton(
        TelegramIssuePublisher,
        options=providers.Singleton(
            TypeAdapter(TelegramGroupOptions).validate_python,
            core.config.integrations.telegram.group
        ),
        client=tg_client
    )

    publishToGithubUseCase = providers.Factory(
        IssuePublishToGithubUseCase,
        issue_repository=issue_repository,
        issue_publisher=gh_issue_publisher
    )

    publishToTelegramUseCase = providers.Factory(
        IssuePublishToTelegramUseCase,
        issue_repository=issue_repository,
        issue_publisher=tg_issue_publisher
    )
