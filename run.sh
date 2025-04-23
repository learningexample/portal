#!/bin/bash

# Enterprise AI Portal management script
# Usage: ./run.sh [stop|build|run|restart|test|test-tabbed]

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

# Function to test the standard app locally
test_app() {
  echo "=== Testing standard app locally ==="
  echo "Starting Python app.py..."
  python app.py
}

# Function to test the tabbed app locally
test_tabbed_app() {
  echo "=== Testing tabbed version locally ==="
  echo "Starting Python app_tabbed.py..."
  python app_tabbed.py
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
  test)
    test_app
    ;;
  test-tabbed)
    test_tabbed_app
    ;;
  "")
    restart_app
    ;;
  *)
    echo "Usage: $0 {stop|build|run|restart|test|test-tabbed}"
    echo ""
    echo "Commands:"
    echo "  stop        - Stop all running containers"
    echo "  build       - Build the Docker image"
    echo "  run         - Stop any running containers, build, and then run the application (full deployment)"
    echo "  restart     - Restart the application without rebuilding (default if no command is specified)"
    echo "  test        - Run the standard app locally without Docker (python app.py)"
    echo "  test-tabbed - Run the tabbed app locally without Docker (python app_tabbed.py)"
    echo ""
    exit 1
esac

exit 0