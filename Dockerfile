FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PORT=8050
ENV PYTHONUNBUFFERED=1

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
else\n\
  APP_MODULE="app:server"\n\
fi\n\
\n\
echo "Starting Gunicorn with $WORKERS workers for $APP_MODULE"\n\
exec gunicorn --workers=$WORKERS --threads=2 \\\n\
    --bind=0.0.0.0:$PORT \\\n\
    --forwarded-allow-ips="*" \\\n\
    --log-level=info \\\n\
    --access-logfile=- \\\n\
    --error-logfile=- \\\n\
    $APP_MODULE\n' > /app/start.sh \
    && chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["/app/start.sh"]