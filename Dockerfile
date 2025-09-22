FROM python:3.13-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install --no-cache-dir poetry

# Configure Poetry to not use virtualenvs
RUN poetry config virtualenvs.create false

# Install dependencies from pyproject.toml (skip project install)
RUN poetry install --no-root --no-interaction --no-ansi

# Install dependencies only (skip project install)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy project code
COPY app/ app/
COPY data/ data/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
