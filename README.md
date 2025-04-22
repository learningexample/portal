# Enterprise AI Portal

A central portal for accessing AI applications across departments and shared AI tools.

## Features

- Clean, modern UI built with Dash and Bootstrap
- Department-based organization of AI applications
- Responsive design for desktop and mobile devices
- Interactive navigation with smooth transitions
- Shared AI tools accessible to all departments
- **Configurable via YAML configuration file**
- **Docker containerization for easy deployment**

## Configuration

All portal content is configurable through the `config.yaml` file, including:
- Portal title and description
- Department list
- Applications for each department
- Shared applications

## Running with Docker

### Using Docker Compose (Recommended)

1. Make sure Docker and Docker Compose are installed on your system
2. Clone this repository
3. Run the application:
   ```
   docker-compose up -d
   ```
4. Access the portal at http://localhost:8050

### Using Docker Directly

1. Make sure Docker is installed on your system
2. Clone this repository
3. Build the Docker image:
   ```
   docker build -t ai-portal .
   ```
4. Run the container:
   ```
   docker run -p 8050:8050 -v $(pwd)/config.yaml:/app/config.yaml ai-portal
   ```
5. Access the portal at http://localhost:8050

### Configuration with Docker

The `config.yaml` file is mounted as a volume in the Docker container, allowing you to update the configuration without rebuilding the image. After modifying the configuration file, simply restart the container:

```
docker-compose restart
```

## Local Setup (Non-Docker)

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python app.py
   ```
4. Access the portal at http://localhost:8050

## Structure

- `app.py` - Main Dash application
- `config.yaml` - Configuration file for portal content
- `Dockerfile` - Instructions for Docker to build the application container
- `docker-compose.yml` - Docker Compose configuration for easy deployment
- `assets/` - Static assets (CSS, images, etc.)
  - `custom.css` - Custom styling
  - `index.html` - HTML template

## Customizing

To add new AI applications or departments:
1. Edit the `config.yaml` file
2. For departments, add a new entry under the `departments` list
3. For applications, add new entries under the appropriate department's `apps` list or under `shared.apps`

## Requirements

- Python 3.8+
- Dash 2.15.0+
- Dash Bootstrap Components 1.5.0+
- PyYAML 6.0+
- Docker (for containerized deployment)