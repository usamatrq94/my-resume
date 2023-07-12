# Use the official Python base image
FROM python:3.11.4-bullseye as base

# Setup shared environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    BOKEH_ALLOW_WS_ORIGIN="*"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/app"
WORKDIR $PYSETUP_PATH

FROM base as builder
# Install system dependencies
RUN apt-get update \
    && apt-get install -y curl

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Install Python dependencies
COPY poetry.lock pyproject.toml ./
RUN --mount=type=ssh poetry install --no-root --without dev --all-extras

# Install NLTK data
RUN python -m nltk.downloader punkt averaged_perceptron_tagger

FROM builder as application
# Set working directory
WORKDIR /app

# Copy the source code into the container
COPY src ./src
COPY resume ./resume

# Expose port 5050
EXPOSE 5050

# Set the entrypoint to run the dashboard file with desired options
CMD ["panel", "serve", "src/dashboard.py","--port", "5050", "--allow-websocket-origin=*"]

