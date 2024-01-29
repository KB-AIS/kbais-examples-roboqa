import asyncio
import logging
import tomllib
from contextlib import asynccontextmanager

import aiogram
import fastapi

logging.basicConfig(level=logging.DEBUG)


def load_app_config() -> dict:
    with open('./config.toml', 'rb') as f:
        app_config = tomllib.load(f)

        return app_config


feedback_router = fastapi.APIRouter()


@feedback_router.get('/')
def read_root():
    return {'Hello': 'World'}


@asynccontextmanager
async def fast_api_lifespan(app: fastapi.FastAPI):
    # Setup aiogram dispatching
    tg_bot_disp = aiogram.Dispatcher()

    # TODO: pass token from config
    tg_bot = aiogram.Bot('')

    tg_bot_polling_task = asyncio.create_task(tg_bot_disp.start_polling(tg_bot))
    yield

    tg_bot_polling_task.cancel()


def setup_app_runner() -> fastapi.FastAPI:
    # web_runner_composer = fastapi.FastAPI(lifespan=fast_api_lifespan)
    app_composer = fastapi.FastAPI()
    app_composer.include_router(feedback_router)

    return app_composer


app = setup_app_runner()
