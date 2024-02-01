FROM python:3.11.7-alpine3.19 as builder
WORKDIR /app

ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==1.7.1

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR \
    poetry config virtualenvs.in-project true \
    && poetry install --no-root

FROM python:3.11.7-alpine3.19 as runtime
WORKDIR  /app

COPY --from=builder /app .

ENV PATH="/app/.venv/bin:$PATH"

COPY ./packages/roboqa_web ./roboqa_web
