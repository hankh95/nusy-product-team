# Santiago REST API Documentation

## Overview

Santiago provides a REST API for external integration, allowing external systems to interact with the multi-agent factory. The API is built with FastAPI and provides endpoints for health monitoring, task management, and agent orchestration.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. Authentication will be added in future versions.

## Response Format

All responses are in JSON format. Successful responses include a `result` field, while errors include an `error` field.

### Success Response
```json
{
  "result": {
    "key": "value"
  }
}
```

### Error Response
```json
{
  "error": "Error message",
  "detail": "Additional error information"
}
```

## Endpoints

### Health Check

Get the health status of the Santiago service.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development",
  "services": {
    "llm_router": true,
    "factory": true,
    "llm_openai": true,
    "llm_xai": true
  }
}
```

**Status Codes:**
- `200` - Service is healthy
- `503` - Service is unhealthy

### Task Management

#### Create Task

Create a new development task for Santiago agents to work on.

**Endpoint:** `POST /tasks`

**Request Body:**
```json
{
  "task_description": "Implement user authentication system",
  "priority": "high",
  "assignee": "santiago-developer"
}
```

**Parameters:**
- `task_description` (string, required): Description of the task
- `priority` (string, optional): Priority level ("low", "medium", "high")
- `assignee` (string, optional): Agent to assign the task to

**Response:**
```json
{
  "task_id": "task_123456789",
  "status": "created",
  "description": "Implement user authentication system",
  "priority": "high",
  "assignee": "santiago-developer",
  "message": "Task created successfully. Santiago agents will begin work shortly."
}
```

**Status Codes:**
- `200` - Task created successfully
- `500` - Internal server error

#### List Tasks

Get a list of active tasks.

**Endpoint:** `GET /tasks`

**Response:**
```json
{
  "tasks": [],
  "total": 0,
  "message": "Task listing not yet implemented - use kanban service directly"
}
```

**Note:** Task listing is currently not implemented and will be added in future versions.

### Agent Management

#### List Agents

Get a list of available Santiago agents.

**Endpoint:** `GET /agents`

**Response:**
```json
{
  "agents": [
    {
      "name": "santiago-developer",
      "role": "developer",
      "capabilities": ["coding", "testing", "deployment"],
      "status": "available"
    },
    {
      "name": "santiago-architect",
      "role": "architect",
      "capabilities": ["design", "planning", "review"],
      "status": "available"
    }
  ],
  "total": 2
}
```

#### Execute Agent Task

Execute a task with a specific agent.

**Endpoint:** `POST /agents/{agent_name}/execute`

**Path Parameters:**
- `agent_name` (string): Name of the agent to execute the task

**Request Body:**
```json
{
  "task_description": "Refactor authentication module",
  "priority": "medium",
  "assignee": "santiago-developer"
}
```

**Response:**
```json
{
  "execution_id": "exec_123456789",
  "agent": "santiago-developer",
  "task": "Refactor authentication module",
  "status": "started",
  "estimated_completion": "2025-11-18T15:30:00Z"
}
```

**Status Codes:**
- `200` - Task execution started
- `404` - Agent not found
- `500` - Execution failed

## Error Handling

The API uses standard HTTP status codes and provides detailed error messages:

- `400` - Bad Request (invalid parameters)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error (server-side issues)

Error responses include:
```json
{
  "error": "Brief error description",
  "detail": "Detailed error information",
  "timestamp": "2025-11-18T14:30:00Z"
}
```

## Rate Limiting

Currently, there is no rate limiting implemented. This will be added in future versions.

## CORS

The API supports Cross-Origin Resource Sharing (CORS) for web client integration. By default, all origins are allowed in development. This should be restricted in production.

## Examples

### Python Client

```python
import requests

# Check health
response = requests.get("http://localhost:8000/health")
print(response.json())

# Create a task
task_data = {
    "task_description": "Add logging to authentication module",
    "priority": "medium"
}
response = requests.post("http://localhost:8000/tasks", json=task_data)
print(response.json())

# List agents
response = requests.get("http://localhost:8000/agents")
agents = response.json()
print(f"Available agents: {len(agents['agents'])}")
```

### JavaScript Client

```javascript
// Check health
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log('Health:', data));

// Create a task
const taskData = {
  task_description: "Implement password reset feature",
  priority: "high"
};

fetch('http://localhost:8000/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(taskData)
})
.then(response => response.json())
.then(data => console.log('Task created:', data));
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_description": "Add unit tests for auth module", "priority": "medium"}'

# List agents
curl http://localhost:8000/agents

# Execute with specific agent
curl -X POST http://localhost:8000/agents/santiago-developer/execute \
  -H "Content-Type: application/json" \
  -d '{"task_description": "Fix login bug", "priority": "high"}'
```

## WebSocket Support (Future)

Real-time communication via WebSockets will be added for:
- Task progress updates
- Agent status changes
- Live logging
- Interactive debugging

## API Versioning

The API uses URL versioning. Current version is v1:
```
/api/v1/health
/api/v1/tasks
/api/v1/agents
```

## Monitoring

API usage can be monitored through:
- Application logs
- Health endpoint metrics
- Future: Prometheus metrics and Grafana dashboards

## Security Considerations

- **Input Validation**: All inputs are validated using Pydantic models
- **Error Handling**: Sensitive information is not exposed in error messages
- **HTTPS**: Use HTTPS in production environments
- **Rate Limiting**: Will be implemented in future versions
- **Authentication**: Will be added for production use

## Changelog

### v1.0.0 (Current)
- Initial API release
- Health check endpoint
- Task creation and agent listing
- Basic error handling and CORS support