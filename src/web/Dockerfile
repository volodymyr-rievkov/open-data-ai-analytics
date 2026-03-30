FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip

COPY src/web/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/config.py ./src/

COPY src/web/ ./src/web/

CMD ["python", "-m", "streamlit", "run", "src/web/app.py", "--server.port=8501", "--server.address=0.0.0.0"]