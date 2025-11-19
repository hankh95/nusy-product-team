# Santiago CI/CD and Deployment Guide

## Overview

Santiago implements a comprehensive CI/CD pipeline that ensures code quality, automated testing, and reliable deployment across multiple environments. This guide covers the complete development and deployment workflow.

## CI/CD Pipeline

### Pipeline Stages

1. **Lint & Test** - Code quality checks and automated testing
2. **Quality Gate** - Security scanning and coverage validation
3. **Staging Deploy** - Automated deployment to staging environment
4. **Production Deploy** - Manual promotion to production (optional)

### GitHub Actions Workflow

The main CI/CD workflow is defined in `.github/workflows/ci-cd.yml` and includes:

- **Multi-environment testing** (Python 3.11, 3.12)
- **Coverage enforcement** (80% minimum)
- **Security scanning** (dependencies and code)
- **Progressive deployment** (dev → staging → production)

### Local Development

Use the Makefile for local development:

```bash
# Run full CI pipeline locally
make ci

# Run tests with coverage
make test-cov

# Start development server
make serve-reload

# Deploy to local development
make deploy-dev
```

## Testing Strategy

### Test Types

- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction validation
- **BDD Tests**: Business logic validation using Gherkin scenarios
- **Smoke Tests**: API connectivity and basic functionality
- **End-to-End Tests**: Full workflow validation

### Coverage Requirements

- **Minimum Coverage**: 80% across all modules
- **Coverage Areas**:
  - `santiago_core/` - Core agent framework
  - `nusy_pm_core/` - PM domain logic
  - `nusy_orchestrator/` - Multi-agent coordination

### Running Tests

```bash
# All tests
make test

# Tests with coverage
make test-cov

# Smoke tests (API connectivity)
make test-smoke

# Full CI pipeline
make ci
```

## Deployment Environments

### Development Environment

**Purpose**: Local development and testing
**Deployment**: Direct Python execution or Docker
**Features**:

- Hot reload enabled
- Debug logging
- Local database/storage

```bash
# Start development server
make serve-reload

# Or with Docker
make docker-run
```

### Staging Environment

**Purpose**: Integration testing and validation
**Deployment**: Docker Compose with full service stack
**Features**:

- Production-like configuration
- Full service dependencies (Redis, monitoring)
- Automated deployment from CI/CD

```bash
# Deploy to staging
make deploy-staging
```

### Production Environment

**Purpose**: Live Santiago operation
**Deployment**: Container orchestration (Docker/Kubernetes)
**Features**:

- High availability
- Monitoring and alerting
- Security hardening
- Manual deployment approval

```bash
# Deploy to production
make deploy-prod
```

## Docker Deployment

### Container Architecture

Santiago uses a multi-container architecture:

- **santiago-core**: Main application container
- **redis**: Caching and coordination
- **nginx**: Reverse proxy and load balancing
- **prometheus/grafana**: Monitoring stack (optional)

### Docker Commands

```bash
# Build container
make docker-build

# Run full stack
make docker-run

# View logs
make docker-logs

# Stop containers
make docker-stop
```

### Docker Compose Configuration

The `docker-compose.yml` defines the complete service stack with:

- **Health checks** for service dependencies
- **Volume mounts** for data persistence
- **Environment variables** for configuration
- **Network isolation** for security

## API Endpoints

Santiago provides a REST API for external integration:

### Health Check

```http
GET /health
```

Returns service health status and version information.

### Task Management

```http
POST /tasks
```

Create new development tasks for Santiago agents.

```http
GET /tasks
```

List active tasks and their status.

### Agent Operations

```http
GET /agents
```

List available Santiago agents.

```http
POST /agents/{agent_name}/execute
```

Execute tasks with specific agents.

### Example Usage

```bash
# Check service health
curl http://localhost:8000/health

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_description": "Implement user authentication", "priority": "high"}'

# List agents
curl http://localhost:8000/agents
```

## Deployment Script

The `scripts/deploy.sh` provides advanced deployment options:

```bash
# Deploy to specific environment
./scripts/deploy.sh development
./scripts/deploy.sh staging
./scripts/deploy.sh production

# Deploy specific version
./scripts/deploy.sh production v1.2.3
```

### Deployment Features

- **Environment validation**
- **Pre-deployment checks** (git status, dependencies)
- **Automated testing** before deployment
- **Rollback support**
- **Comprehensive logging**

## Configuration Management

### Environment Variables

Santiago uses environment variables for configuration:

```bash
# Core settings
NUSY_ENV=production
PYTHONPATH=/app

# API Keys (secure storage recommended)
OPENAI_API_KEY=your_key_here
XAI_API_KEY=your_key_here

# Service configuration
REDIS_URL=redis://redis:6379/0
HOST=0.0.0.0
PORT=8000
WORKERS=4
```

### Environment Files

- `.env.development` - Development configuration
- `.env.staging` - Staging configuration
- `.env.production` - Production configuration
- `.env.example` - Template for new environments

## Monitoring and Observability

### Health Checks

- **Container health**: Built-in Docker health checks
- **Application health**: `/health` endpoint
- **Dependency checks**: Redis, LLM APIs

### Logging

- **Development**: Debug level logging
- **Staging**: Info level logging
- **Production**: Warning+ level logging

### Metrics (Future)

- **Prometheus integration** for system metrics
- **Custom metrics** for agent performance
- **Grafana dashboards** for visualization

## Security Considerations

### Container Security

- **Non-root user** execution
- **Minimal base images** (Python slim)
- **No privileged containers**
- **Read-only filesystems** where possible

### API Security

- **CORS configuration** for web clients
- **Input validation** with Pydantic models
- **Rate limiting** (future implementation)
- **Authentication** (future implementation)

### Secret Management

- **Environment variables** for API keys
- **GitHub Secrets** for CI/CD
- **AWS Secrets Manager** for production (future)

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure package is installed with `pip install -e .`
2. **Test Failures**: Check API keys in `.env` file
3. **Docker Issues**: Verify Docker daemon is running
4. **Port Conflicts**: Check if ports 8000, 6379 are available

### Debug Commands

```bash
# Check service status
curl http://localhost:8000/health

# View application logs
make docker-logs

# Run tests with verbose output
pytest -v -s

# Check environment variables
env | grep NUSY
```

## Future Enhancements

- **Kubernetes deployment** for production scaling
- **Blue-green deployments** for zero-downtime updates
- **Canary releases** for gradual rollouts
- **Advanced monitoring** with distributed tracing
- **API authentication** and authorization
- **Multi-region deployment** for high availability
