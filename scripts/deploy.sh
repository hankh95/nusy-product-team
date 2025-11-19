#!/bin/bash
# Santiago Deployment Script
# Handles deployment to different environments with proper configuration

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENVIRONMENT="${1:-staging}"
VERSION="${2:-$(git rev-parse --short HEAD)}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Validate environment
validate_environment() {
    case "$ENVIRONMENT" in
        development|staging|production)
            log_info "Deploying to $ENVIRONMENT environment"
            ;;
        *)
            log_error "Invalid environment: $ENVIRONMENT"
            log_info "Valid environments: development, staging, production"
            exit 1
            ;;
    esac
}

# Setup environment-specific configuration
setup_environment() {
    log_info "Setting up $ENVIRONMENT environment configuration"

    # Create environment-specific .env file
    ENV_FILE="$PROJECT_ROOT/.env.$ENVIRONMENT"
    if [[ ! -f "$ENV_FILE" ]]; then
        log_warning "Environment file $ENV_FILE not found, using .env.example as template"
        cp "$PROJECT_ROOT/.env.example" "$ENV_FILE"
        log_warning "Please configure $ENV_FILE with appropriate values for $ENVIRONMENT"
    fi

    # Set environment variables
    export NUSY_ENV="$ENVIRONMENT"
    export DEPLOYMENT_VERSION="$VERSION"

    # Environment-specific settings
    case "$ENVIRONMENT" in
        development)
            export WORKERS=1
            export LOG_LEVEL=DEBUG
            ;;
        staging)
            export WORKERS=2
            export LOG_LEVEL=INFO
            ;;
        production)
            export WORKERS=4
            export LOG_LEVEL=WARNING
            ;;
    esac
}

# Run pre-deployment checks
pre_deployment_checks() {
    log_info "Running pre-deployment checks"

    # Check if we're in a git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not in a git repository"
        exit 1
    fi

    # Check if working directory is clean (for production)
    if [[ "$ENVIRONMENT" == "production" ]]; then
        if ! git diff --quiet && ! git diff --staged --quiet; then
            log_error "Working directory is not clean. Commit or stash changes before deploying to production."
            exit 1
        fi
    fi

    # Check if required tools are available
    command -v python3 >/dev/null 2>&1 || { log_error "python3 is required but not installed"; exit 1; }
    command -v pip >/dev/null 2>&1 || { log_error "pip is required but not installed"; exit 1; }

    # Check Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ "$PYTHON_VERSION" != "3.11" && "$PYTHON_VERSION" != "3.12" ]]; then
        log_warning "Python $PYTHON_VERSION detected. Recommended: 3.11 or 3.12"
    fi

    log_success "Pre-deployment checks passed"
}

# Install dependencies
install_dependencies() {
    log_info "Installing dependencies"

    cd "$PROJECT_ROOT"

    # Upgrade pip
    pip install --upgrade pip

    # Install dependencies
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
    fi

    # Install the package itself
    pip install -e .

    log_success "Dependencies installed"
}

# Run tests
run_tests() {
    log_info "Running test suite"

    cd "$PROJECT_ROOT"

    # Run tests with coverage
    if command -v pytest >/dev/null 2>&1; then
        pytest --cov=santiago_core --cov=nusy_pm_core --cov=nusy_orchestrator \
               --cov-report=term-missing --cov-fail-under=80 \
               -v tests/
        TEST_EXIT_CODE=$?
    else
        log_warning "pytest not found, running basic import test"
        python3 -c "import santiago_core; print('Import test passed')"
        TEST_EXIT_CODE=$?
    fi

    if [[ $TEST_EXIT_CODE -ne 0 ]]; then
        log_error "Tests failed"
        exit 1
    fi

    log_success "Tests passed"
}

# Build application
build_application() {
    log_info "Building application"

    cd "$PROJECT_ROOT"

    # Create necessary directories
    mkdir -p workspace logs data

    # Any build steps would go here
    # For now, this is mainly a Python application, so no build needed

    log_success "Application built"
}

# Deploy application
deploy_application() {
    log_info "Deploying application to $ENVIRONMENT"

    case "$ENVIRONMENT" in
        development)
            deploy_development
            ;;
        staging)
            deploy_staging
            ;;
        production)
            deploy_production
            ;;
    esac
}

# Development deployment (local)
deploy_development() {
    log_info "Starting development server"

    cd "$PROJECT_ROOT"

    # Set environment file
    export ENV_FILE=".env.development"

    # Start the application
    if command -v uvicorn >/dev/null 2>&1; then
        # If FastAPI/uvicorn is available, start web server
        nohup uvicorn santiago_core.api:app --host 0.0.0.0 --port 8000 --reload &
        SERVER_PID=$!
        echo $SERVER_PID > santiago.pid
        log_success "Development server started (PID: $SERVER_PID)"
    else
        # Fallback to basic Python execution
        nohup python3 -m santiago_core.agents.factory &
        SERVER_PID=$!
        echo $SERVER_PID > santiago.pid
        log_success "Development application started (PID: $SERVER_PID)"
    fi
}

# Staging deployment
deploy_staging() {
    log_info "Deploying to staging environment"

    # For staging, we'll use docker-compose
    if command -v docker-compose >/dev/null 2>&1; then
        cd "$PROJECT_ROOT"

        # Stop existing containers
        docker-compose down || true

        # Start services
        docker-compose up -d

        log_success "Staging deployment completed"
    else
        log_error "docker-compose is required for staging deployment"
        exit 1
    fi
}

# Production deployment
deploy_production() {
    log_info "Deploying to production environment"

    # For production, we could use various strategies:
    # - Kubernetes
    # - AWS ECS/Fargate
    # - Cloud Run
    # - etc.

    # For now, using docker-compose as example
    if command -v docker-compose >/dev/null 2>&1; then
        cd "$PROJECT_ROOT"

        # Use production profile
        COMPOSE_PROFILES=production docker-compose down || true
        COMPOSE_PROFILES=production docker-compose up -d

        log_success "Production deployment completed"
    else
        log_error "docker-compose is required for production deployment"
        exit 1
    fi
}

# Run post-deployment tests
post_deployment_tests() {
    log_info "Running post-deployment tests"

    # Wait for application to be ready
    sleep 10

    # Run smoke tests
    if [[ -f "smoke_test.py" ]]; then
        python3 smoke_test.py
    else
        # Basic health check
        if command -v curl >/dev/null 2>&1; then
            if curl -f http://localhost:8000/health >/dev/null 2>&1; then
                log_success "Health check passed"
            else
                log_warning "Health check failed - application may still be starting"
            fi
        fi
    fi
}

# Main deployment process
main() {
    log_info "Starting Santiago deployment"
    log_info "Environment: $ENVIRONMENT"
    log_info "Version: $VERSION"

    validate_environment
    setup_environment
    pre_deployment_checks
    install_dependencies
    run_tests
    build_application
    deploy_application
    post_deployment_tests

    log_success "Deployment to $ENVIRONMENT completed successfully!"
    log_info "Version: $VERSION"
}

# Handle command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            echo "Usage: $0 [environment] [version]"
            echo ""
            echo "Environments:"
            echo "  development  Local development deployment"
            echo "  staging      Staging environment deployment"
            echo "  production   Production environment deployment"
            echo ""
            echo "Examples:"
            echo "  $0 development"
            echo "  $0 staging v1.2.3"
            echo "  $0 production"
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

# Run main deployment
main "$@"