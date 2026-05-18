FROM ghcr.io/astral-sh/uv:latest AS uv_setup

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

COPY --from=uv_setup /uv /uvx /bin/

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev --group download

COPY src/ ./src/

CMD ["uv", "run", "-m", "src.data_load.data_load"]