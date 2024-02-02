import dramatiq
from dependency_injector.wiring import inject, Provide
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import RedisBackend

from roboqa_web.application.core.usecase import UseCase
from roboqa_web.infrastructure.worker.container import ContainerWorker

backend = RedisBackend()

PUBLISH_TG_TASK_MUTEX = ConcurrentRateLimiter(backend, "publish-tg-mutex", limit=1, ttl=1_000)


@dramatiq.actor(max_retries=None, min_backoff=1000, max_backoff=5000)
@inject
async def issue_publish_gh_task(
    issue_id: str,
    use_case: UseCase[str, None] = Provide[ContainerWorker.publishToGithubUseCase]
):
    with PUBLISH_TG_TASK_MUTEX.acquire():
        await use_case.execute(issue_id)

        issue_publish_tg_task.send(issue_id)



@dramatiq.actor(max_retries=None, min_backoff=1000, max_backoff=5000)
@inject
async def issue_publish_tg_task(
    issue_id: str,
    use_case: UseCase[str, None] = Provide[ContainerWorker.publishToTelegramUseCase]
):
    with PUBLISH_TG_TASK_MUTEX.acquire():
        # (await container.publishToTelegramUseCase())
        await use_case.execute(issue_id)
