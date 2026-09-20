FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.12.15 /uv /uvx /bin/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/service/.venv/bin:$PATH"

WORKDIR /service

COPY pyproject.toml uv.lock ./

RUN uv sync \
    --frozen \
    --no-dev \
    --no-install-project

COPY alembic.ini ./
COPY migrations ./migrations
COPY app ./app

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]