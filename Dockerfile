FROM python:3.11-slim

WORKDIR /app

# Install system dependencies - only essential ones with explicit timeout
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for better security
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/bash -m appuser

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --timeout 100

# Copy script files first
COPY start.sh healthcheck.sh ./
RUN chmod +x /app/start.sh /app/healthcheck.sh

# Copy only necessary files (exclude large or unnecessary files)
COPY *.py *.yaml *.bat ./
COPY apache/ ./apache/
COPY assets/ ./assets/
COPY utils/ ./utils/
COPY tests/ ./tests/

# Set environment variables
ENV PORT=8050
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DASH_DEBUG_MODE=False
ENV PIP_DEFAULT_TIMEOUT=100

# Set ownership of application files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user for better security
USER appuser

# Set up healthcheck with reduced frequency
HEALTHCHECK --interval=60s --timeout=3s --start-period=20s --retries=2 CMD [ "/app/healthcheck.sh" ]

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["/app/start.sh"]