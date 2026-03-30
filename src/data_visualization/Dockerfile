FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip

COPY src/data_visualization/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/config.py ./src/
COPY src/utils.py ./src/

COPY src/data_visualization/ ./src/data_visualization/

CMD ["python", "-m", "src.data_visualization.data_visualization"]