FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/worker_service

WORKDIR /app

COPY worker_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY worker_service ./worker_service

RUN mkdir -p /app/logs

EXPOSE 8001

CMD ["python", "-m", "src.main"]
