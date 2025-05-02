FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    procps \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for better security
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -s /bin/bash -m appuser

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8050
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DASH_DEBUG_MODE=False

# Create start script that uses Gunicorn for better performance
RUN echo '#!/bin/bash\n\
# Calculate optimal number of workers based on CPU cores\n\
CORES=$(nproc)\n\
WORKERS=$(($CORES * 2 + 1))\n\
\n\
if [ "$PORTAL_VERSION" = "tabbed" ]; then\n\
  APP_MODULE="app_bytab:server"\n\
elif [ "$PORTAL_VERSION" = "bysection" ]; then\n\
  APP_MODULE="app-bysection:server"\n\
elif [ "$PORTAL_VERSION" = "bysection-fixed" ]; then\n\
  APP_MODULE="app-bysection-fixed:server"\n\
elif [ "$PORTAL_VERSION" = "bysection-minimal" ]; then\n\
  APP_MODULE="app-bysection-minimal:server"\n\
elif [ "$PORTAL_VERSION" = "appstore" ]; then\n\
  APP_MODULE="app_store:server"\n\
else\n\
  APP_MODULE="app:server"\n\
fi\n\
\n\
echo "Starting Gunicorn with $WORKERS workers for $APP_MODULE"\n\
exec gunicorn --workers=$WORKERS --threads=2 \\\n\
    --bind=0.0.0.0:$PORT \\\n\
    --forwarded-allow-ips="*" \\\n\
    --log-level=info \\\n\
    --timeout=120 \\\n\
    --access-logfile=- \\\n\
    --error-logfile=- \\\n\
    --worker-tmp-dir=/dev/shm \\\n\
    --worker-class=gthread \\\n\
    $APP_MODULE\n' > /app/start.sh \
    && chmod +x /app/start.sh

# Create healthcheck script
RUN echo '#!/bin/bash\n\
curl --silent --fail http://localhost:$PORT/_dash-layout || exit 1\n' > /app/healthcheck.sh \
    && chmod +x /app/healthcheck.sh

# Set ownership of application files to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user for better security
USER appuser

# Set up healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 CMD [ "/app/healthcheck.sh" ]

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["/app/start.sh"]