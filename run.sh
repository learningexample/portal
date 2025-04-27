#!/bin/bash

# Enterprise AI Portal management script
# Usage: ./run.sh [stop|build|run|restart|test|test-tabbed|test-bysection|status|scale]

# Function to stop any running instances
stop_app() {
  echo "Stopping any running AI Portal containers..."
  docker-compose down
  echo "All containers stopped."
}

# Function to build the application
build_app() {
  echo "Building AI Portal Docker image..."
  docker-compose build
  echo "Build completed."
}

# Function to run the application
run_app() {
  echo "Starting AI Portal..."
  docker-compose up -d
  echo "AI Portal is running at http://localhost:8050"
}

# Function to restart the application
restart_app() {
  echo "Restarting AI Portal..."
  docker-compose restart
  echo "AI Portal has been restarted and is available at http://localhost:8050"
}

# Function for the full process: stop, build, and run
run_full() {
  echo "=== Performing full deployment process ==="
  stop_app
  build_app
  run_app
  echo "=== Full deployment completed ==="
}

# Function to check status and connections
status_app() {
  echo "=== AI Portal Status ==="
  echo "Running containers:"
  docker-compose ps
  echo ""
  echo "Current connections to Apache:"
  docker exec portal-apache bash -c "apachectl status | grep 'requests currently'"
  echo ""
  echo "Container resource usage:"
  docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
}

# Function to show scaling capabilities
scale_info() {
  echo "=== AI Portal Scaling Information ==="
  echo "CPU Cores available: $(nproc)"
  echo "Estimated Gunicorn workers per container: $(($(nproc) * 2 + 1))"
  echo "Total estimated workers across all portals: $(($(nproc) * 2 + 1)) x 3"
  echo ""
  echo "Estimated concurrent user capacity:"
  echo "- Basic capacity: ~$((($(nproc) * 2 + 1) * 3 * 10)) users"
  echo "- Maximum capacity: ~$((($(nproc) * 2 + 1) * 3 * 20)) users"
  echo ""
  echo "Current container limits (from docker-compose.yml):"
  grep -A4 "resources:" docker-compose.yml | grep -v "resources:" | sed 's/^/  /'
}

# Function to test the standard app locally with Gunicorn
test_app() {
  echo "=== Testing standard app locally with Gunicorn ==="
  echo "Starting Gunicorn with app.py..."
  gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app:server
}

# Function to test the tabbed app locally with Gunicorn
test_tabbed_app() {
  echo "=== Testing tabbed version locally with Gunicorn ==="
  echo "Starting Gunicorn with app_bytab.py..."
  gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 app_bytab:server
}

# Function to test the collapsible sections app locally with Gunicorn
test_bysection_app() {
  echo "=== Testing collapsible sections version locally with Gunicorn ==="
  echo "Starting Gunicorn with app-bysection.py..."
  gunicorn --workers=4 --threads=2 --bind=0.0.0.0:8050 "app-bysection:server"
}

# Process command line arguments
case "$1" in
  stop)
    stop_app
    ;;
  build)
    build_app
    ;;
  run)
    run_full
    ;;
  restart)
    restart_app
    ;;
  status)
    status_app
    ;;
  scale)
    scale_info
    ;;
  test)
    test_app
    ;;
  test-tabbed)
    test_tabbed_app
    ;;
  test-bysection)
    test_bysection_app
    ;;
  "")
    restart_app
    ;;
  *)
    echo "Usage: $0 {stop|build|run|restart|status|scale|test|test-tabbed|test-bysection}"
    echo ""
    echo "Commands:"
    echo "  stop          - Stop all running containers"
    echo "  build         - Build the Docker image"
    echo "  run           - Stop any running containers, build, and then run the application (full deployment)"
    echo "  restart       - Restart the application without rebuilding (default if no command is specified)"
    echo "  status        - Show current status, connections, and resource usage"
    echo "  scale         - Show information about scaling capabilities"
    echo "  test          - Run the standard app locally with Gunicorn"
    echo "  test-tabbed   - Run the tabbed app locally with Gunicorn"
    echo "  test-bysection - Run the collapsible sections app locally with Gunicorn"
    echo ""
    exit 1
esac

exit 0