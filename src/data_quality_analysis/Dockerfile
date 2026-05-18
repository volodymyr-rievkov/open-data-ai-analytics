FROM ghcr.io/astral-sh/uv:latest AS uv_setup

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

COPY --from=uv_setup /uv /uvx /bin/

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev --group analysis

COPY src/ ./src/

CMD ["uv", "run", "-m", "src.data_quality_analysis.data_quality_analysis"]