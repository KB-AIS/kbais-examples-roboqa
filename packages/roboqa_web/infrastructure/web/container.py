from dependency_injector import containers, providers
from dependency_injector.providers import Factory

from roboqa_web.application.issues.usecases.issue_register import IssueRegisterUseCase
from roboqa_web.infrastructure.core.container import ContainerCore
from roboqa_web.infrastructure.services import RedisIssueRepository
from roboqa_web.infrastructure.services.issues.issue_sender import WorkerIssueSender


class ContainerApi(containers.DeclarativeContainer):
    core = providers.Container(ContainerCore)

    wiring_config = containers.WiringConfiguration(packages=["roboqa_web.infrastructure.web"])

    # Domain

    issue_repository = providers.Factory(RedisIssueRepository, redis=core.redis_pool)

    # Application -> Domain

    issue_sender = providers.Singleton(WorkerIssueSender)

    issue_register_uc: Factory[IssueRegisterUseCase] = providers.Factory(
        IssueRegisterUseCase,
        issue_repository=issue_repository,
        issue_sender=issue_sender
    )
