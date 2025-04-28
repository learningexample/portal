#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}AI Portal Test Runner${NC}"
echo -e "${BLUE}====================${NC}"

if [ $# -eq 0 ]; then
    echo "Usage: ./test.sh [command]"
    echo ""
    echo "Available commands:"
    echo "  build    - Build test Docker images"
    echo "  up       - Start test environment"
    echo "  down     - Stop test environment"
    echo "  run      - Build and start test environment"
    echo "  test     - Run all automated tests"
    echo "  e2e      - Run end-to-end tests"
    echo "  unit     - Run unit tests"
    echo "  stop     - Stop and remove all containers"
    echo "  logs     - View container logs"
    echo "  shell    - Open shell in portal container"
    exit 0
fi

command=$1

case $command in
    build)
        echo -e "${GREEN}Building test Docker images...${NC}"
        docker-compose -f docker-compose.test.yml build
        echo -e "${GREEN}Build complete.${NC}"
        ;;
    up)
        echo -e "${GREEN}Starting test environment...${NC}"
        docker-compose -f docker-compose.test.yml up -d
        echo ""
        echo -e "${GREEN}Test environment is running at http://localhost:8051${NC}"
        echo ""
        echo -e "${GREEN}Test dashboard available at:${NC}"
        echo -e "${GREEN}- Standard version: http://localhost:8051/portal-1/${NC}"
        ;;
    down)
        echo -e "${GREEN}Stopping test environment...${NC}"
        docker-compose -f docker-compose.test.yml down
        ;;
    run)
        echo -e "${GREEN}Building and starting test environment...${NC}"
        docker-compose -f docker-compose.test.yml up --build -d
        echo ""
        echo -e "${GREEN}Test environment is running at http://localhost:8051${NC}"
        echo ""
        echo -e "${GREEN}Test dashboard available at:${NC}"
        echo -e "${GREEN}- Standard version: http://localhost:8051/portal-1/${NC}"
        ;;
    test)
        echo -e "${GREEN}Running all tests...${NC}"
        docker exec -it ai-portal-test python -m pytest -xvs
        ;;
    e2e)
        echo -e "${GREEN}Running end-to-end tests...${NC}"
        docker exec -it ai-portal-test python -m pytest test_portal_e2e.py -xvs
        ;;
    unit)
        echo -e "${GREEN}Running unit tests...${NC}"
        docker exec -it ai-portal-test python -m pytest test_portal.py -xvs
        ;;
    stop)
        echo -e "${GREEN}Stopping all test containers...${NC}"
        docker-compose -f docker-compose.test.yml down
        ;;
    logs)
        echo -e "${GREEN}Viewing test container logs...${NC}"
        docker-compose -f docker-compose.test.yml logs -f
        ;;
    shell)
        echo -e "${GREEN}Opening shell in portal test container...${NC}"
        docker exec -it ai-portal-test /bin/bash
        ;;
    *)
        echo "Unknown command: $command"
        echo "Run './test.sh' without arguments to see available commands."
        exit 1
        ;;
esac

exit 0