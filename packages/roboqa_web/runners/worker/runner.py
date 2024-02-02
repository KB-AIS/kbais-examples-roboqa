import logging
import sys

import dramatiq
from dependency_injector.wiring import inject, Provide
from dramatiq.middleware import AsyncIO
from dramatiq.rate_limits import RateLimiter

from roboqa_web.application.core.usecase import UseCase
from roboqa_web.infrastructure.worker.container import ContainerWorker

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

runner_container = ContainerWorker()

dq_broker = runner_container.core.dq_broker()
dq_broker.add_middleware(AsyncIO())

dramatiq.set_broker(dq_broker)


@dramatiq.actor(max_retries=None, min_backoff=1000, max_backoff=5000)
@inject
async def issue_publish_gh_task(
    issue_id: str,
    mutex: RateLimiter = Provide[ContainerWorker.dq_issue_publish_rl],
    use_case: UseCase[str, None] = Provide[ContainerWorker.publishToGithubUseCase]
):
    with mutex.acquire():
        await use_case.execute(issue_id)

        issue_publish_tg_task.send(issue_id)


@dramatiq.actor(max_retries=None, min_backoff=1000, max_backoff=5000)
@inject
async def issue_publish_tg_task(
    issue_id: str,
    mutex: RateLimiter = Provide[ContainerWorker.dq_issue_publish_rl],
    use_case: UseCase[str, None] = Provide[ContainerWorker.publishToTelegramUseCase]
):
    with mutex.acquire():
        await use_case.execute(issue_id)

# TODO: FIX
runner_container.wire(modules=["roboqa_web.runners.worker.runner"])
