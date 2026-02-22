FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --extras "web" --no-root --no-interaction --no-ansi

COPY . .
