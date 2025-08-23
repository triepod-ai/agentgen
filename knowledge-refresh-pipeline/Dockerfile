# Knowledge Refresh Pipeline - Production Dockerfile
# Multi-stage build for optimized deployment

FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create application user
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Development stage
FROM base as development

# Install development dependencies
RUN pip install pytest pytest-asyncio pytest-mock black flake8 mypy

# Copy source code
COPY --chown=appuser:appuser . .

# Switch to application user
USER appuser

# Default command for development
CMD ["python", "knowledge_refresh_orchestrator.py", "--daemon"]

# Production stage
FROM base as production

# Copy only necessary files
COPY --chown=appuser:appuser orchestration/ ./orchestration/
COPY --chown=appuser:appuser pipelines/ ./pipelines/
COPY --chown=appuser:appuser monitoring/ ./monitoring/
COPY --chown=appuser:appuser config/ ./config/
COPY --chown=appuser:appuser knowledge_refresh_orchestrator.py .
COPY --chown=appuser:appuser requirements.txt .

# Create necessary directories
RUN mkdir -p logs data && \
    chown -R appuser:appuser logs data

# Switch to application user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import asyncio; import sys; sys.path.append('/app'); \
    from knowledge_refresh_orchestrator import KnowledgeRefreshOrchestrator; \
    orchestrator = KnowledgeRefreshOrchestrator(); \
    result = asyncio.run(orchestrator.get_system_status()); \
    exit(0 if result['system_health']['overall_status'] == 'healthy' else 1)"

# Default command for production
CMD ["python", "knowledge_refresh_orchestrator.py", "--daemon"]

# Final stage selection
FROM ${BUILD_STAGE:-production} as final