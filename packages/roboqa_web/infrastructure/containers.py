from dependency_injector import containers, providers

from roboqa_web.application import usecases
from roboqa_web.infrastructure.data.setup import setup_redis_pool

import tomllib


def get_config() -> dict:
    with open("config.toml", "rb") as f:
        app_config = tomllib.load(f)

        return app_config


class Core(containers.DeclarativeContainer):

    # TODO: Provide configuration
    redis_pool = providers.Resource(
        setup_redis_pool,
        host="localhost:6379"
    )


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    config.from_dict(get_config())

    core = providers.Container(Core)

    # UseCases

    publishToGithubUseCase = providers.Factory(
        usecases.PublishToGithubUseCase,
        redis=core.redis_pool,
    )

    publishToTelegramUseCase = providers.Factory(
        usecases.PublishToTelegramUseCase
    )
