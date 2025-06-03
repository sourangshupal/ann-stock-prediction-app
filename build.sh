#!/bin/bash

# ANN Stock Prediction App - Docker Build Script
# Usage: ./build.sh [option]
# Options: build, run, dev, stop, clean, logs

set -e

APP_NAME="ann-stock-app"
CONTAINER_NAME="ann-stock-prediction"
PORT="8501"
DEV_PORT="8502"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Build the application
build_app() {
    print_status "Building ANN Stock Prediction App..."
    docker-compose build --no-cache
    print_success "Build completed successfully!"
}

# Run the application
run_app() {
    print_status "Starting ANN Stock Prediction App..."
    docker-compose up -d
    print_success "App is running at http://localhost:$PORT"
    print_status "Use 'docker-compose logs -f' to view logs"
}

# Run in development mode
run_dev() {
    print_status "Starting ANN Stock Prediction App in development mode..."
    docker-compose --profile dev up -d ann-stock-app-dev
    print_success "Development app is running at http://localhost:$DEV_PORT"
    print_status "Files are mounted for hot reload"
}

# Stop the application
stop_app() {
    print_status "Stopping ANN Stock Prediction App..."
    docker-compose down
    print_success "App stopped successfully!"
}

# Clean up Docker resources
clean_app() {
    print_warning "This will remove all containers, images, and volumes for this app."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Cleaning up Docker resources..."
        docker-compose down -v --rmi all --remove-orphans
        print_success "Cleanup completed!"
    else
        print_status "Cleanup cancelled."
    fi
}

# Show logs
show_logs() {
    print_status "Showing application logs (Ctrl+C to exit)..."
    docker-compose logs -f
}

# Show help
show_help() {
    echo "ANN Stock Prediction App - Docker Build Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  build     Build the Docker image"
    echo "  run       Build and run the application"
    echo "  dev       Run in development mode with hot reload"
    echo "  stop      Stop the running application"
    echo "  clean     Remove all Docker resources for this app"
    echo "  logs      Show application logs"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 run      # Build and start the app"
    echo "  $0 dev      # Start in development mode"
    echo "  $0 logs     # View logs"
    echo "  $0 stop     # Stop the app"
}

# Main script logic
main() {
    check_docker
    
    case "${1:-help}" in
        build)
            build_app
            ;;
        run)
            build_app
            run_app
            ;;
        dev)
            build_app
            run_dev
            ;;
        stop)
            stop_app
            ;;
        clean)
            clean_app
            ;;
        logs)
            show_logs
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
