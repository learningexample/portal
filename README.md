# Enterprise AI Portal

A central portal for accessing AI applications across departments and shared AI tools.

## Features

- Clean, modern UI built with Dash and Bootstrap
- Department-based organization of AI applications
- Multiple interface versions (scrolling, tabbed, collapsible sections, app store)
- Responsive design for desktop and mobile devices
- Interactive navigation with smooth transitions
- Shared AI tools accessible to all departments
- **Gunicorn integration for high concurrency support**
- **WebSocket support via Apache for real-time updates**
- **Configurable via YAML configuration file**
- **Docker containerization for easy deployment**
- **Container health checks for improved reliability**
- **Optimized for scalability with resource constraints**

## Portal Versions

The application comes in four interface variations:

1. **Standard Version** (`app.py`) - Scrolling sections layout
2. **Tabbed Version** (`app_bytab.py`) - Tab-based navigation
3. **Collapsible Version** (`app-bysection.py`) - Sections that can be expanded/collapsed
4. **App Store Version** (`app_store.py`) - App store style interface

Each version can be accessed through different paths:
- Standard: `/portal-1/`
- Tabbed: `/portal-2/`
- Collapsible: `/portal-3/`
- App Store: `/portal-4/`

## Configuration

All portal content is configurable through the `config.yaml` file, including:
- Portal title and description
- Department list
- Applications for each department
- Shared applications
- App Store entries

## Running with Docker

### Using Docker Compose (Recommended)

1. Make sure Docker and Docker Compose are installed on your system
2. Clone this repository
3. Run the application:
   ```
   docker-compose up -d
   ```
4. Access the portal at http://localhost:8050

### Using the Management Scripts

The project includes management scripts for both Windows and Linux/macOS:

```
# Windows
run.bat [stop|build|run|restart|status|scale|test|test-tabbed|test-bysection|test-appstore]

# Linux/macOS
./run.sh [stop|build|run|restart|status|scale|test|test-tabbed|test-bysection|test-appstore]
```

Key commands:
- `run` - Performs full deployment (stop, build, run)
- `status` - Shows running containers and connection status
- `scale` - Displays scaling capabilities based on your hardware
- `test-*` - Test different portal versions locally with Gunicorn

### Configuration with Docker

The `config.yaml` file is mounted as a volume in the Docker container, allowing you to update the configuration without rebuilding the image. After modifying the configuration file, simply restart the container:

```
docker-compose restart
```

## Performance Optimization

The portal is optimized for high concurrent user support:

- **Gunicorn Workers**: Uses the formula `(CPU cores × 2 + 1)` for optimal worker count
- **WebSocket Support**: Configured in Apache for real-time UI updates
- **Resource Constraints**: Container resource limits for balanced performance
- **Multiple Instances**: Four independent application instances for load distribution
- **Worker Temp Directory**: Uses shared memory for improved performance
- **Health Checks**: Container health monitoring for increased reliability

To check the estimated concurrent user capacity of your system:
```
run.bat scale   # Windows
./run.sh scale  # Linux/macOS
```

## Local Setup (Non-Docker)

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run any application version with Gunicorn:
   ```
   # Standard version
   gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app:server
   
   # Tabbed version
   gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app_bytab:server
   
   # Collapsible version
   gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app-bysection:server
   
   # App store version
   gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app_store:server
   ```
4. Access the portal at http://localhost:8050

## Project Structure

- `app.py` - Standard scrolling version
- `app_bytab.py` - Tabbed interface version
- `app-bysection.py` - Collapsible sections version
- `app_store.py` - App store style interface
- `config.yaml` - Configuration file for portal content
- `Dockerfile` - Container configuration with Gunicorn multi-worker setup
- `docker-compose.yml` - Docker Compose with resource constraints and health checks
- `run.bat`/`run.sh` - Management scripts with monitoring capabilities
- `portal_manager.py` - GUI tool for managing the portal
- `utils/portal_utils.py` - Shared utility functions
- `apache/portal.conf` - Apache configuration with WebSocket support
- `assets/` - Static assets (CSS, images, etc.)
  - `custom.css` - Custom styling
  - `draggable-tabs.js` - JavaScript for tab interface
  - `index.html` - HTML template

## Technical Improvements

### Apache Configuration
- Properly configured for WebSocket proxying
- Optimized for each portal version
- Health check monitoring included
- Configured for high concurrency

### Docker Configuration
- Python 3.12 base image for better performance
- Container health checks for improved reliability
- Optimized Gunicorn configuration with timeouts
- Shared memory temp directory for better performance

## Customizing

To add new AI applications or departments:
1. Edit the `config.yaml` file
2. For departments, add a new entry under the `departments` list
3. For applications, add new entries under the appropriate department's `apps` list or under `shared.apps`

## Security

The application is designed to run behind a reverse proxy with WebSocket support. For production environments, consider implementing authentication (e.g., PingID) at the Apache level.

## Requirements

- Python 3.12+
- Dash 2.15.0+
- Dash Bootstrap Components 1.5.0+
- PyYAML 6.0+
- Gunicorn 21.2.0+
- Docker and Docker Compose (for containerized deployment)