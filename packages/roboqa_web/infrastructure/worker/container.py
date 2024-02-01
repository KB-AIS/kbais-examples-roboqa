from dependency_injector import containers, providers

from roboqa_web.application.issues.usecases.issue_publish_to_gh import IssuePublishToGithubUseCase
from roboqa_web.application.issues.usecases.issue_publish_to_tg import IssuePublishToTelegramUseCase
from roboqa_web.infrastructure.core.container import ContainerCore


class ContainerWorker(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(_load_config())

    core = providers.Container(ContainerCore, config=config)

    wiring_config  = containers.WiringConfiguration(packages=["roboqa_web.infrastructure.worker.tasks"])

    # UseCases

    publishToGithubUseCase = providers.Factory(
        IssuePublishToGithubUseCase,
        redis=core.redis_pool,
    )

    publishToTelegramUseCase = providers.Factory(
        IssuePublishToTelegramUseCase
    )
