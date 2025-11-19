# Santiago Multi-Agent AI Factory
# Production-ready container for autonomous development workflows

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    NUSY_ENV=production \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash santiago
USER santiago

# Set work directory
WORKDIR /app

# Copy dependency files first for better caching
COPY --chown=santiago:santiago requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --user --upgrade pip && \
    pip install --user -r requirements.txt && \
    pip install --user -e .

# Copy application code
COPY --chown=santiago:santiago . .

# Create necessary directories
RUN mkdir -p /app/workspace /app/logs /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import santiago_core; print('Santiago is healthy')" || exit 1

# Expose ports (adjust based on your services)
EXPOSE 8000 8001 8002

# Default command - can be overridden
CMD ["python", "-m", "santiago_core.agents.factory"]