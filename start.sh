#!/bin/bash

# Use environment variable or default to 1 worker
if [ -n "$WORKERS" ]; then
  WORKERS=$WORKERS
else
  WORKERS=1
fi

# Set thread count from environment variable or default
if [ -n "$WORKER_THREADS" ]; then
  THREADS=$WORKER_THREADS
else
  THREADS=1
fi

# Set worker connections from environment variable or default
if [ -n "$WORKER_CONNECTIONS" ]; then
  CONNECTIONS=$WORKER_CONNECTIONS
else
  CONNECTIONS=100
fi

if [ "$PORTAL_VERSION" = "tabbed" ]; then
  APP_MODULE="app_bytab:server"
elif [ "$PORTAL_VERSION" = "bysection" ]; then
  APP_MODULE="app-bysection:server"
elif [ "$PORTAL_VERSION" = "bysection-fixed" ]; then
  APP_MODULE="app-bysection-fixed:server"
elif [ "$PORTAL_VERSION" = "bysection-minimal" ]; then
  APP_MODULE="app-bysection-minimal:server"
elif [ "$PORTAL_VERSION" = "appstore" ]; then
  APP_MODULE="app_store:server"
else
  APP_MODULE="app:server"
fi

echo "Starting Gunicorn with $WORKERS worker, $THREADS threads and $CONNECTIONS connections for $APP_MODULE"
exec gunicorn --workers=$WORKERS --threads=$THREADS \
    --bind=0.0.0.0:$PORT \
    --forwarded-allow-ips="*" \
    --log-level=info \
    --timeout=60 \
    --access-logfile=- \
    --error-logfile=- \
    --worker-tmp-dir=/dev/shm \
    --worker-class=gthread \
    --worker-connections=$CONNECTIONS \
    --max-requests=1000 \
    --max-requests-jitter=50 \
    $APP_MODULE