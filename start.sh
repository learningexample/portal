#!/bin/bash

# Use environment variable or calculate workers
if [ -n "$WORKERS_PER_CORE" ]; then
  CORES=$(nproc)
  WORKERS=$(($CORES * $WORKERS_PER_CORE))
  # Ensure at least one worker
  if [ "$WORKERS" -lt 1 ]; then
    WORKERS=1
  fi
else
  CORES=$(nproc)
  WORKERS=$(($CORES + 1))
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

echo "Starting Gunicorn with $WORKERS workers for $APP_MODULE"
exec gunicorn --workers=$WORKERS --threads=2 \
    --bind=0.0.0.0:$PORT \
    --forwarded-allow-ips="*" \
    --log-level=warning \
    --timeout=60 \
    --access-logfile=- \
    --error-logfile=- \
    --worker-tmp-dir=/dev/shm \
    --worker-class=gthread \
    --max-requests=1000 \
    --max-requests-jitter=50 \
    $APP_MODULE