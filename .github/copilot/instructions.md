# Global Instructions for GitHub Copilot

## Environment Information
- Python version: 3.11
- Framework: Dash with Gunicorn
- Deployment: Docker containers with Apache reverse proxy
- Authentication: PingID integration planned
- Containerization: Docker with docker-compose
- OS: Windows development environment, Linux deployment
- Date: April 2025

## Project Structure
- `app.py`: Main application (original portal version)
- `app_bytab.py`: Tabbed version of the portal
- `app-bysection.py`: Section-based collapsible version of the portal
- `apache/portal.conf`: Apache reverse proxy configuration with WebSocket support
- `nginx/nginx.conf`: Alternative Nginx configuration (not currently used)
- `Dockerfile`: Containerization configuration with Gunicorn multi-worker setup
- `docker-compose.yml`: Multi-container Docker configuration with resource constraints
- `run.sh`/`run.bat`: Deployment and management scripts with monitoring capabilities
- `config.yaml`: Central configuration for all portal versions

## Coding Standards
- Use PEP 8 for Python code style
- Follow Dash best practices for component structure
- DocStrings: Use Google style docstrings
- Logging: Use the logging module with appropriate levels
- Error handling: Always use try/except with specific exceptions

## Preferred Patterns
- Callbacks should be organized with related functionality grouped together
- Use f-strings instead of format() or % formatting
- Prefer dataclasses for structured data
- Implement proper type hints for functions and methods
- Resource constraints on Docker containers for better scalability

## Performance Considerations
- The application must support multiple concurrent users
- WebSocket connections through Apache are handled by Gunicorn workers
- Use efficient data loading patterns to avoid blocking operations
- Cache expensive operations where possible
- Using the formula of (CPU cores × 2 + 1) for Gunicorn worker count

## Technology Stack
- Dash: For building web applications
- Dash Bootstrap Components: For responsive UI
- PyYAML: For configuration parsing
- Gunicorn: For production-grade WSGI server
- Apache: For reverse proxy and WebSocket routing
- Docker: For containerization and deployment