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

# Expose the port the app runs on
EXPOSE 8050

# Command to run the application
CMD ["python", "app.py"]