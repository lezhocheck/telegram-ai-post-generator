FROM python:3.12.2-slim as builder

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && \
    apt-get install -y python3 gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /bot

COPY ./pyproject.toml ./poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-root

FROM python:3.12.2-slim as runtime

ENV VIRTUAL_ENV=bot/.venv \
    PATH="/bot/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src

EXPOSE 8000

ENTRYPOINT ["uvicorn", "src:create_app", "--host", "0.0.0.0", "--port", "8000"]