# 🌐 REST API Reference

Complete reference for Santiago's REST API endpoints, including request/response formats, authentication, and examples.

---

## 📋 Base URL

```
https://api.santiago.ai/v1
```

For local development:
```
http://localhost:8000/api/v1
```

---

## 🔐 Authentication

All API requests require authentication via API key in the Authorization header:

```
Authorization: Bearer YOUR_API_KEY
```

### Getting an API Key

1. **Register** at [dashboard.santiago.ai](https://dashboard.santiago.ai)
2. **Create an application** in your account settings
3. **Copy the API key** from the application details

### Example Request

```bash
curl -H "Authorization: Bearer sk-1234567890abcdef" \
     https://api.santiago.ai/v1/agents
```

---

## 📊 Response Format

All responses follow this structure:

```json
{
  "success": true|false,
  "data": { ... } | null,
  "error": { ... } | null,
  "metadata": {
    "request_id": "req-123456",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

### Success Response

```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "id": "agent-123",
        "type": "developer",
        "domain": "python",
        "status": "available"
      }
    ]
  },
  "metadata": {
    "request_id": "req-abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "type",
      "issue": "must be one of: developer, product-manager, quality-assurance"
    }
  },
  "metadata": {
    "request_id": "req-abc123",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0.0"
  }
}
```

---

## 🚀 Agents

### List Agents

Get a list of available agents.

**Endpoint:** `GET /agents`

**Query Parameters:**
- `type` (optional): Filter by agent type (`developer`, `product-manager`, `quality-assurance`)
- `domain` (optional): Filter by domain (`python`, `javascript`, `saas`, etc.)
- `status` (optional): Filter by status (`available`, `busy`, `offline`)
- `limit` (optional): Maximum number of results (default: 50, max: 100)
- `offset` (optional): Pagination offset (default: 0)

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.santiago.ai/v1/agents?type=developer&domain=python&limit=10"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agents": [
      {
        "id": "agent-dev-py-001",
        "type": "developer",
        "domain": "python",
        "capabilities": ["code-generation", "testing", "documentation"],
        "status": "available",
        "performance_score": 0.95,
        "created_at": "2024-01-01T00:00:00Z",
        "last_active": "2024-01-15T09:30:00Z"
      }
    ],
    "total": 1,
    "limit": 10,
    "offset": 0
  }
}
```

### Get Agent Details

Get detailed information about a specific agent.

**Endpoint:** `GET /agents/{agent_id}`

**Path Parameters:**
- `agent_id`: The unique identifier of the agent

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/agents/agent-dev-py-001
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "agent-dev-py-001",
    "type": "developer",
    "domain": "python",
    "capabilities": ["code-generation", "testing", "documentation"],
    "status": "available",
    "performance_score": 0.95,
    "quality_metrics": {
      "success_rate": 0.94,
      "avg_response_time": 45.2,
      "code_quality_score": 8.7
    },
    "specializations": ["web-development", "data-science", "api-design"],
    "created_at": "2024-01-01T00:00:00Z",
    "last_active": "2024-01-15T09:30:00Z"
  }
}
```

### Create Custom Agent

Create a new custom agent with specific capabilities.

**Endpoint:** `POST /agents`

**Request Body:**
```json
{
  "type": "custom",
  "domain": "your-domain",
  "capabilities": ["custom-capability-1", "custom-capability-2"],
  "configuration": {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
  },
  "training_data": {
    "examples": [...],
    "knowledge_base": "kb-123"
  }
}
```

**Example Request:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "type": "custom",
       "domain": "medical",
       "capabilities": ["diagnosis", "treatment-planning"],
       "configuration": {
         "model": "gpt-4",
         "temperature": 0.3
       }
     }' \
     https://api.santiago.ai/v1/agents
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "agent-custom-med-001",
    "type": "custom",
    "domain": "medical",
    "capabilities": ["diagnosis", "treatment-planning"],
    "status": "training",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

## 🎯 Tasks

### Submit Task

Submit a new task for execution by an agent.

**Endpoint:** `POST /tasks`

**Request Body:**
```json
{
  "type": "code-review|feature-development|testing|documentation",
  "agent_id": "agent-123",  // optional, auto-assign if not specified
  "priority": "low|normal|high|urgent",
  "context": {
    "repository": "owner/repo",
    "branch": "main",
    "files": ["src/main.py"],
    "requirements": "Implement user authentication"
  },
  "constraints": {
    "deadline": "2024-01-20T00:00:00Z",
    "budget": 1000,
    "quality_threshold": 0.9
  },
  "webhook_url": "https://your-app.com/webhooks/santiago"  // optional
}
```

**Example Request:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "type": "code-review",
       "priority": "high",
       "context": {
         "repository": "myorg/myrepo",
         "pull_request": 123,
         "files": ["api/auth.py", "tests/test_auth.py"]
       },
       "constraints": {
         "quality_threshold": 0.95
       }
     }' \
     https://api.santiago.ai/v1/tasks
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task-456",
    "type": "code-review",
    "status": "queued",
    "agent_id": "agent-dev-py-001",
    "priority": "high",
    "created_at": "2024-01-15T10:30:00Z",
    "estimated_completion": "2024-01-15T11:00:00Z"
  }
}
```

### Get Task Status

Get the current status of a task.

**Endpoint:** `GET /tasks/{task_id}`

**Path Parameters:**
- `task_id`: The unique identifier of the task

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/tasks/task-456
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task-456",
    "type": "code-review",
    "status": "in_progress",
    "agent_id": "agent-dev-py-001",
    "progress": {
      "percentage": 65,
      "current_step": "analyzing-code-quality",
      "steps_completed": ["parsing-files", "checking-syntax", "running-tests"],
      "steps_remaining": ["generating-report", "suggesting-improvements"]
    },
    "created_at": "2024-01-15T10:30:00Z",
    "started_at": "2024-01-15T10:31:00Z",
    "estimated_completion": "2024-01-15T11:00:00Z"
  }
}
```

### Get Task Result

Get the result of a completed task.

**Endpoint:** `GET /tasks/{task_id}/result`

**Path Parameters:**
- `task_id`: The unique identifier of the task

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/tasks/task-456/result
```

**Response:**
```json
{
  "success": true,
  "data": {
    "task_id": "task-456",
    "status": "completed",
    "result": {
      "overall_score": 8.5,
      "issues": [
        {
          "severity": "medium",
          "category": "security",
          "file": "api/auth.py",
          "line": 45,
          "message": "Potential SQL injection vulnerability",
          "suggestion": "Use parameterized queries"
        }
      ],
      "recommendations": [
        "Add input validation",
        "Implement rate limiting",
        "Add comprehensive test coverage"
      ],
      "metrics": {
        "cyclomatic_complexity": 3.2,
        "maintainability_index": 78,
        "test_coverage": 85
      }
    },
    "quality_score": 0.92,
    "completed_at": "2024-01-15T10:55:00Z",
    "execution_time": 1500
  }
}
```

### Cancel Task

Cancel a running or queued task.

**Endpoint:** `POST /tasks/{task_id}/cancel`

**Path Parameters:**
- `task_id`: The unique identifier of the task

**Example Request:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/tasks/task-456/cancel
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "task-456",
    "status": "cancelled",
    "cancelled_at": "2024-01-15T10:35:00Z",
    "reason": "user_requested"
  }
}
```

### List Tasks

Get a list of tasks with optional filtering.

**Endpoint:** `GET /tasks`

**Query Parameters:**
- `status` (optional): Filter by status (`queued`, `in_progress`, `completed`, `failed`, `cancelled`)
- `agent_id` (optional): Filter by agent
- `type` (optional): Filter by task type
- `priority` (optional): Filter by priority
- `created_after` (optional): Filter tasks created after timestamp (ISO 8601)
- `created_before` (optional): Filter tasks created before timestamp (ISO 8601)
- `limit` (optional): Maximum number of results (default: 50, max: 100)
- `offset` (optional): Pagination offset (default: 0)

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.santiago.ai/v1/tasks?status=completed&limit=20"
```

---

## 🧠 Knowledge Graph

### Query Knowledge

Execute SPARQL queries against the knowledge graph.

**Endpoint:** `POST /knowledge/query`

**Request Body:**
```json
{
  "query": "SELECT ?feature ?status WHERE { ?feature rdf:type santiago:Feature ; santiago:status ?status }",
  "domain": "product-management",  // optional
  "limit": 100  // optional
}
```

**Example Request:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "SELECT ?feature ?status WHERE { ?feature rdf:type santiago:Feature ; santiago:status ?status }",
       "limit": 10
     }' \
     https://api.santiago.ai/v1/knowledge/query
```

**Response:**
```json
{
  "success": true,
  "data": {
    "results": [
      {
        "feature": "user-authentication",
        "status": "completed"
      },
      {
        "feature": "payment-integration",
        "status": "in_progress"
      }
    ],
    "count": 2,
    "execution_time": 45
  }
}
```

### Add Knowledge

Add new facts to the knowledge graph.

**Endpoint:** `POST /knowledge/facts`

**Request Body:**
```json
{
  "facts": [
    {
      "subject": "feature-123",
      "predicate": "hasStatus",
      "object": "completed",
      "domain": "product-management"
    },
    {
      "subject": "feature-123",
      "predicate": "completedAt",
      "object": "2024-01-15T10:00:00Z",
      "domain": "product-management"
    }
  ]
}
```

**Example Request:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "facts": [
         {
           "subject": "new-feature",
           "predicate": "rdf:type",
           "object": "santiago:Feature"
         }
       ]
     }' \
     https://api.santiago.ai/v1/knowledge/facts
```

### Get Knowledge Stats

Get statistics about the knowledge graph.

**Endpoint:** `GET /knowledge/stats`

**Query Parameters:**
- `domain` (optional): Filter by domain

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/knowledge/stats
```

**Response:**
```json
{
  "success": true,
  "data": {
    "total_facts": 15420,
    "domains": {
      "product-management": 3240,
      "software-development": 5670,
      "quality-assurance": 4510
    },
    "last_updated": "2024-01-15T10:00:00Z",
    "provenance_tracking": true
  }
}
```

---

## 📊 Analytics

### Get Agent Performance

Get performance metrics for agents.

**Endpoint:** `GET /analytics/agents/{agent_id}/performance`

**Path Parameters:**
- `agent_id`: The unique identifier of the agent

**Query Parameters:**
- `period` (optional): Time period (`1d`, `7d`, `30d`, `90d`) - default: `30d`

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.santiago.ai/v1/analytics/agents/agent-dev-py-001/performance?period=7d"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "agent_id": "agent-dev-py-001",
    "period": "7d",
    "metrics": {
      "tasks_completed": 45,
      "success_rate": 0.96,
      "avg_response_time": 42.3,
      "avg_quality_score": 8.7,
      "total_execution_time": 1903,
      "cost_efficiency": 0.89
    },
    "trends": {
      "success_rate_trend": "increasing",
      "response_time_trend": "stable",
      "quality_trend": "increasing"
    }
  }
}
```

### Get System Health

Get overall system health and performance metrics.

**Endpoint:** `GET /analytics/health`

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/analytics/health
```

**Response:**
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "uptime": "15d 4h 30m",
    "services": {
      "api": "healthy",
      "database": "healthy",
      "knowledge_graph": "healthy",
      "agent_factory": "healthy"
    },
    "performance": {
      "avg_response_time": 125,
      "error_rate": 0.002,
      "throughput": 450
    },
    "resources": {
      "cpu_usage": 0.65,
      "memory_usage": 0.72,
      "disk_usage": 0.45
    }
  }
}
```

---

## ⚙️ Webhooks

### Register Webhook

Register a webhook for real-time notifications.

**Endpoint:** `POST /webhooks`

**Request Body:**
```json
{
  "url": "https://your-app.com/webhooks/santiago",
  "events": ["task.completed", "task.failed", "agent.created"],
  "secret": "your-webhook-secret",
  "active": true
}
```

**Example Request:**
```bash
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://my-app.com/webhooks/santiago",
       "events": ["task.completed", "task.failed"],
       "secret": "webhook-secret-123"
     }' \
     https://api.santiago.ai/v1/webhooks
```

### List Webhooks

Get a list of registered webhooks.

**Endpoint:** `GET /webhooks`

**Example Request:**
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.santiago.ai/v1/webhooks
```

### Delete Webhook

Remove a webhook registration.

**Endpoint:** `DELETE /webhooks/{webhook_id}`

**Path Parameters:**
- `webhook_id`: The unique identifier of the webhook

---

## 📋 Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `VALIDATION_ERROR` | Invalid request parameters | 400 |
| `AUTHENTICATION_ERROR` | Invalid or missing API key | 401 |
| `AUTHORIZATION_ERROR` | Insufficient permissions | 403 |
| `NOT_FOUND` | Resource not found | 404 |
| `RATE_LIMITED` | Rate limit exceeded | 429 |
| `INTERNAL_ERROR` | Internal server error | 500 |
| `SERVICE_UNAVAILABLE` | Service temporarily unavailable | 503 |

---

## 📊 Rate Limits

| Endpoint Type | Limit | Window |
|---------------|-------|--------|
| Read operations | 1000 requests | 1 minute |
| Write operations | 100 requests | 1 minute |
| Task submissions | 50 requests | 1 minute |
| Knowledge queries | 500 requests | 1 minute |

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## 🔄 SDK Examples

### Python SDK

```python
from santiago_api import SantiagoClient

client = SantiagoClient(api_key="your-api-key")

# List agents
agents = client.agents.list(type="developer")

# Submit task
task = client.tasks.submit({
    "type": "code-review",
    "context": {"repo": "myorg/myrepo", "pr": 123}
})

# Get result
result = client.tasks.get_result(task.id)
```

### JavaScript SDK

```javascript
const { SantiagoClient } = require('santiago-api');

const client = new SantiagoClient({ apiKey: 'your-api-key' });

// Async/await
async function reviewCode() {
  const task = await client.tasks.submit({
    type: 'code-review',
    context: { repo: 'myorg/myrepo', pr: 123 }
  });

  const result = await client.tasks.getResult(task.id);
  return result;
}
```

---

*For more examples and detailed SDK documentation, see the [Python SDK Reference](python-sdk.md) and [MCP Integration Guide](mcp-integration.md).* 