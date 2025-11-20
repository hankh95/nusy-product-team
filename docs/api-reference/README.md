# 🔌 API Reference

This section provides comprehensive documentation for all Santiago APIs, including REST endpoints, MCP contracts, Python SDK, and integration patterns.

---

## 📋 API Overview

Santiago provides multiple integration points for different use cases:

| API Type | Use Case | Protocol | Authentication |
|----------|----------|----------|----------------|
| **REST API** | Web applications, external integrations | HTTP/JSON | API Key, OAuth2 |
| **MCP** | AI agent integration | JSON-RPC 2.0 over WebSocket | Agent tokens |
| **Python SDK** | Python applications, custom agents | Direct imports | Service account |
| **GraphQL** | Complex queries, real-time updates | GraphQL over HTTP | API Key, OAuth2 |

---

## 🚀 Quick Start

### REST API Example
```bash
# Get available agents
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:8000/api/v1/agents

# Create a new task
curl -X POST \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"type": "code-review", "context": {"repo": "my-repo", "pr": 123}}' \
     http://localhost:8000/api/v1/tasks
```

### Python SDK Example
```python
from santiago_core import SantiagoFactory

# Initialize factory
factory = SantiagoFactory(api_key="your-api-key")

# Create specialized agent
agent = factory.create_agent("code-review", domain="python")

# Execute task
result = await agent.execute({
    "action": "review",
    "code": "def hello(): return 'world'",
    "standards": ["PEP8", "security"]
})
```

### MCP Integration Example
```javascript
// Connect to Santiago MCP server
const client = new MCPClient({
    endpoint: "ws://localhost:8000/mcp",
    token: "agent-token"
});

// List available tools
const tools = await client.listTools();

// Execute tool
const result = await client.callTool("santiago.code-review", {
    code: "function hello() { return 'world'; }",
    language: "javascript"
});
```

---

## 📚 API Documentation

### [REST API Reference](rest-api.md)
Complete reference for HTTP endpoints, request/response formats, and authentication.

### [MCP Integration Guide](mcp-integration.md)
Model Context Protocol contracts, tool definitions, and agent integration patterns.

### [Python SDK Reference](python-sdk.md)
Python client library documentation, classes, methods, and examples.

### [GraphQL Schema](graphql-schema.md)
GraphQL API for complex queries and real-time subscriptions.

### [Authentication Guide](authentication.md)
API keys, OAuth2 flows, agent tokens, and security best practices.

### [Rate Limiting](rate-limiting.md)
Rate limit policies, quota management, and usage optimization.

---

## 🔧 Core Concepts

### Agent Factory Pattern

Santiago uses a **factory pattern** for agent creation:

```python
# Factory creates specialized agents
factory = SantiagoFactory()

# Each agent has specific capabilities
code_agent = factory.create_agent("developer", domain="python")
pm_agent = factory.create_agent("product-manager", domain="saas")
qa_agent = factory.create_agent("quality-assurance", domain="testing")
```

### Task Execution Model

Tasks are executed asynchronously with provenance tracking:

```python
# Submit task
task_id = await factory.submit_task({
    "type": "feature-development",
    "requirements": {...},
    "constraints": {...}
})

# Monitor progress
status = await factory.get_task_status(task_id)

# Get results
result = await factory.get_task_result(task_id)
```

### Knowledge Graph Integration

All agents have access to a shared knowledge graph:

```python
# Query domain knowledge
knowledge = await agent.query_knowledge(
    "SELECT ?feature WHERE { ?feature rdf:type santiago:Feature }"
)

# Add new knowledge
await agent.add_knowledge({
    "subject": "new-feature",
    "predicate": "implements",
    "object": "requirement-123"
})
```

---

## 📊 Response Formats

### Standard Response Structure

All APIs return consistent response formats:

```json
{
  "success": true,
  "data": {
    "id": "task-123",
    "status": "completed",
    "result": {...}
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req-456",
    "version": "1.0.0"
  }
}
```

### Error Response Structure

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid task parameters",
    "details": {
      "field": "requirements",
      "issue": "missing required field 'description'"
    }
  },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req-456"
  }
}
```

---

## 🔄 Webhook Integration

Santiago supports webhooks for real-time notifications:

```python
# Register webhook
await factory.register_webhook({
    "url": "https://my-app.com/webhooks/santiago",
    "events": ["task.completed", "agent.created"],
    "secret": "webhook-secret"
})
```

### Webhook Payload

```json
{
  "event": "task.completed",
  "data": {
    "task_id": "task-123",
    "agent_id": "agent-456",
    "result": {...},
    "metadata": {...}
  },
  "signature": "sha256=..."
}
```

---

## 📈 Monitoring & Metrics

### Health Check Endpoint

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "2d 4h 30m",
  "services": {
    "database": "healthy",
    "knowledge_graph": "healthy",
    "agent_factory": "healthy"
  }
}
```

### Metrics Endpoint

```bash
curl http://localhost:8000/metrics
```

Returns Prometheus-compatible metrics for monitoring.

---

## 🔒 Security Considerations

### API Key Management

- Rotate API keys regularly
- Use different keys for different environments
- Store keys securely (never in code)

### Request Signing

For enhanced security, sign requests:

```python
import hmac
import hashlib

def sign_request(payload, secret):
    signature = hmac.new(
        secret.encode(),
        json.dumps(payload).encode(),
        hashlib.sha256
    ).hexdigest()
    return signature
```

### Rate Limiting

All endpoints are rate-limited. Check headers for limits:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

---

## 🚀 Best Practices

### Error Handling

```python
try:
    result = await santiago.execute_task(task)
except SantiagoError as e:
    if e.code == "RATE_LIMITED":
        await asyncio.sleep(e.retry_after)
        result = await santiago.execute_task(task)
    elif e.code == "VALIDATION_ERROR":
        # Fix validation issues
        task = fix_validation_errors(task)
        result = await santiago.execute_task(task)
    else:
        logger.error(f"Unexpected error: {e}")
        raise
```

### Connection Pooling

```python
from santiago_core import SantiagoClient

# Reuse client for multiple requests
client = SantiagoClient(api_key="key", pool_size=10)

# Client automatically manages connections
results = await asyncio.gather(*[
    client.execute_task(task) for task in tasks
])
```

### Caching Strategy

```python
from santiago_core.cache import ResultCache

cache = ResultCache(ttl=3600)  # 1 hour TTL

async def execute_with_cache(task):
    cache_key = hashlib.md5(json.dumps(task).encode()).hexdigest()
    return await cache.get_or_compute(cache_key, lambda: santiago.execute_task(task))
```

---

## 📞 Support

- **Documentation**: [docs.santiago.ai](https://docs.santiago.ai)
- **API Playground**: [playground.santiago.ai](https://playground.santiago.ai)
- **Community Forum**: [community.santiago.ai](https://community.santiago.ai)
- **GitHub Issues**: [github.com/santiago/issues](https://github.com/santiago/issues)

---

*For detailed API specifications, see the individual reference documents linked above.*