FROM python:3.12

# Set working directory
WORKDIR /app

# System packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    librdkafka-dev \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_HOME="/opt/poetry"
ENV PATH="${POETRY_HOME}/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run migration and app
CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn src.server:app --host 0.0.0.0 --port 8000"]
