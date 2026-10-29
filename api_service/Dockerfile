FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY api_service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini ./alembic.ini
COPY migrations ./migrations
COPY api_service ./api_service

ENV PYTHONPATH=/app/api_service

# Create logs directory
RUN mkdir -p /app/logs

# Expose the application port
EXPOSE 8000

# Use a shell script to run migrations then start the app
CMD ["sh", "-c", "alembic -c /app/alembic.ini upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]