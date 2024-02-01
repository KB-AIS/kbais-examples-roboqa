import asyncio
import logging
import sys

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from roboqa_web.infrastructure.web.container import ContainerApi
from roboqa_web.infrastructure.web.endpoints import issues_router


def make_runner_composer() -> FastAPI:
    runner_composer = FastAPI()
    runner_composer.include_router(issues_router)
    runner_composer.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )

    return runner_composer


async def run_async():
    runner_container = ContainerApi()

    runner = uvicorn.Server(uvicorn.Config(
        "roboqa_web.runners.web.runner:make_runner_composer",
        host='0.0.0.0', port=5000,
        log_level="debug"
    ))

    await runner.serve()


def run():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(run_async())


if __name__ == "__main__":
    run()
