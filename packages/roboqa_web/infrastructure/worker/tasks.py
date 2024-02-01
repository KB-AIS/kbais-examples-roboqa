import dramatiq
from dependency_injector.wiring import inject, Provide

from roboqa_web.application.core.usecase import UseCase
from roboqa_web.infrastructure.worker.container import ContainerWorker


@dramatiq.actor(max_retries=None, min_backoff=500, max_backoff=1000)
@inject
async def issue_publish_gh_task(
    issue_id: str,
    use_case: UseCase[str, None] = Provide[ContainerWorker.publishToGithubUseCase]
):
    await use_case.execute(issue_id)

    issue_publish_tg_task.send(issue_id)


@dramatiq.actor(max_retries=None, min_backoff=500, max_backoff=1000)
@inject
async def issue_publish_tg_task(
    issue_id: str,
    use_case: UseCase[str, None] = Provide[ContainerWorker.publishToTelegramUseCase]
):
    await use_case.execute(issue_id)

