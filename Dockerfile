FROM python:3.14-slim

# --------------------------------------------------
# Python environment
# --------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# --------------------------------------------------
# Application directory
# --------------------------------------------------

WORKDIR /app

# --------------------------------------------------
# System dependencies
# --------------------------------------------------

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------
# Create non-root application user
# --------------------------------------------------

RUN groupadd \
        --system \
        --gid 10001 \
        curamind \
    && useradd \
        --system \
        --uid 10001 \
        --gid 10001 \
        --home-dir /app \
        --shell /usr/sbin/nologin \
        curamind

# --------------------------------------------------
# Install Python dependencies
# --------------------------------------------------

COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip \
    && pip install -r /app/requirements.txt

# --------------------------------------------------
# Copy application
# --------------------------------------------------

COPY . /app/

# --------------------------------------------------
# Create required directories
# --------------------------------------------------

RUN mkdir -p \
        /app/staticfiles \
        /app/media \
        /app/media/uploads \
        /app/logs \
    && chown -R curamind:curamind /app \
    && chmod +x /app/docker/entrypoint.sh

# --------------------------------------------------
# Run as non-root user
# --------------------------------------------------

USER curamind

# --------------------------------------------------
# Django application port
# --------------------------------------------------

EXPOSE 8000

# --------------------------------------------------
# Container health check
# --------------------------------------------------

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=3 \
    CMD python manage.py check \
        || exit 1

# --------------------------------------------------
# Container startup
# --------------------------------------------------

ENTRYPOINT ["/app/docker/entrypoint.sh"]