# 🤖 Agent Getting Started Guide

Welcome, AI agent! This guide will help you understand how to interact with Santiago agents, integrate with the system, and contribute to the multi-agent ecosystem.

---

## 🎯 Understanding Santiago Agents

### What Are Santiago Agents?

Santiago agents are **specialized AI contractors** built by the Santiago factory. Unlike general-purpose AI systems, each Santiago:

- Has **deep domain expertise** in a specific area
- Operates with **clear boundaries and contracts**
- Maintains **provenance and trust metrics**
- Learns and **improves through each engagement**

### Agent Types

| Agent | Domain | Capabilities | Status |
|-------|--------|--------------|--------|
| **Santiago-PM** | Product Management | Feature planning, backlog management, stakeholder coordination | Active |
| **Santiago-Architect** | System Architecture | Architecture patterns, scalability, technology evaluation | Active |
| **Santiago-Developer** | Software Development | Code generation, testing, refactoring, deployment | Active |
| **Santiago-QA** | Quality Assurance | Test planning, automated testing, quality metrics | Active |

---

## 🔌 Integration Methods

### 1. MCP (Model Context Protocol)

The **primary integration method** for agents:

```python
# Connect to Santiago via MCP
from santiago_core.mcp.client import SantiagoMCPClient

client = SantiagoMCPClient()
await client.connect()

# List available agents
agents = await client.list_agents()
print(f"Available agents: {agents}")

# Hire an agent for work
result = await client.hire_agent(
    agent_type="santiago-developer",
    task="Implement user authentication",
    requirements={
        "security_level": "high",
        "framework": "fastapi",
        "database": "postgresql"
    }
)
```

### 2. REST API Integration

Direct HTTP API access:

```bash
# Health check
curl http://localhost:8000/health

# List agents
curl http://localhost:8000/agents

# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "agent_type": "santiago-developer",
    "task": "Implement user authentication",
    "requirements": {
      "security_level": "high",
      "framework": "fastapi"
    }
  }'
```

### 3. Python SDK

Direct Python integration:

```python
from santiago_core.sdk import SantiagoSDK

sdk = SantiagoSDK()

# Synchronous usage
result = sdk.execute_task(
    agent="santiago-developer",
    task="Add logging to service",
    context={"service": "user-service", "level": "INFO"}
)

# Asynchronous usage
async with sdk.session() as session:
    task_id = await session.create_task(...)
    result = await session.wait_for_completion(task_id)
```

---

## 🧠 Accessing Knowledge

### Knowledge Graph Queries

Access domain knowledge through SPARQL:

```python
from santiago_core.knowledge import KnowledgeGraph

kg = KnowledgeGraph()

# Query for clinical guidelines
query = """
PREFIX clin: <http://santiago/clinical/>
SELECT ?guideline ?recommendation
WHERE {
  ?guideline clin:recommends ?recommendation .
  ?guideline clin:forCondition "diabetes" .
}
"""

results = kg.query(query)
for result in results:
    print(f"Guideline: {result['guideline']}")
    print(f"Recommendation: {result['recommendation']}")
```

### Semantic Search

Natural language knowledge access:

```python
from santiago_core.knowledge import SemanticSearch

search = SemanticSearch()

# Find relevant knowledge
results = search.find(
    query="treatment options for type 2 diabetes",
    domain="clinical",
    confidence_threshold=0.8
)

for result in results:
    print(f"Content: {result['content']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Source: {result['provenance']}")
```

### Knowledge Contribution

Contribute new knowledge to the graph:

```python
from santiago_core.knowledge import KnowledgeBuilder

builder = KnowledgeBuilder()

# Add new clinical knowledge
builder.add_fact(
    subject="metformin",
    predicate="treats",
    object="type_2_diabetes",
    provenance={
        "source": "ADA_2023_guidelines",
        "confidence": 0.95,
        "last_updated": "2023-12-01"
    }
)

# Commit changes
builder.commit()
```

---

## 🔄 Multi-Agent Workflows

### Sequential Workflows

Chain agents together for complex tasks:

```python
from santiago_core.workflow import WorkflowEngine

engine = WorkflowEngine()

# Define workflow
workflow = {
    "name": "feature-development",
    "steps": [
        {
            "agent": "santiago-pm",
            "task": "analyze_requirements",
            "inputs": ["user_story", "acceptance_criteria"]
        },
        {
            "agent": "santiago-architect",
            "task": "design_solution",
            "depends_on": "analyze_requirements"
        },
        {
            "agent": "santiago-developer",
            "task": "implement_feature",
            "depends_on": "design_solution"
        },
        {
            "agent": "santiago-qa",
            "task": "validate_implementation",
            "depends_on": "implement_feature"
        }
    ]
}

# Execute workflow
result = await engine.execute_workflow(workflow)
```

### Parallel Processing

Execute tasks concurrently:

```python
from santiago_core.workflow import ParallelExecutor

executor = ParallelExecutor()

# Define parallel tasks
tasks = [
    {
        "agent": "santiago-developer",
        "task": "implement_authentication",
        "context": {"service": "user-api"}
    },
    {
        "agent": "santiago-developer",
        "task": "implement_authorization",
        "context": {"service": "user-api"}
    },
    {
        "agent": "santiago-qa",
        "task": "test_security",
        "context": {"service": "user-api"}
    }
]

# Execute in parallel
results = await executor.execute_parallel(tasks)
```

### Agent Coordination

Coordinate between multiple agents:

```python
from santiago_core.coordination import AgentCoordinator

coordinator = AgentCoordinator()

# Start multi-agent session
session = await coordinator.create_session(
    agents=["santiago-pm", "santiago-architect", "santiago-developer"],
    goal="Build a new user management system"
)

# Agents coordinate autonomously
await session.start_coordination()

# Monitor progress
status = await session.get_status()
print(f"Progress: {status['completion_percentage']}%")

# Get final result
result = await session.get_result()
```

---

## 📊 Monitoring & Metrics

### Agent Performance

Track agent performance metrics:

```python
from santiago_core.monitoring import AgentMonitor

monitor = AgentMonitor()

# Get agent metrics
metrics = monitor.get_agent_metrics("santiago-developer")

print(f"Tasks completed: {metrics['tasks_completed']}")
print(f"Average response time: {metrics['avg_response_time']}ms")
print(f"Success rate: {metrics['success_rate']}%")
print(f"Quality score: {metrics['quality_score']}/10")
```

### Workflow Analytics

Analyze workflow performance:

```python
from santiago_core.monitoring import WorkflowAnalytics

analytics = WorkflowAnalytics()

# Analyze recent workflows
report = analytics.analyze_workflows(
    time_range="last_30_days",
    workflow_type="feature-development"
)

print(f"Total workflows: {report['total_workflows']}")
print(f"Average completion time: {report['avg_completion_time']}")
print(f"Success rate: {report['success_rate']}%")
print(f"Bottleneck steps: {report['bottlenecks']}")
```

### Quality Assurance

Monitor agent quality metrics:

```python
from santiago_core.qa import QualityAssurance

qa = QualityAssurance()

# Run quality checks
quality_report = qa.assess_agent_quality("santiago-developer")

print(f"Code quality score: {quality_report['code_quality']}")
print(f"Test coverage: {quality_report['test_coverage']}%")
print(f"Documentation completeness: {quality_report['documentation']}%")
print(f"Security score: {quality_report['security']}")
```

---

## 🛡️ Best Practices

### Agent Interaction

#### Clear Task Definition
```python
# Good: Clear, specific task
task = {
    "description": "Implement JWT-based authentication for REST API",
    "requirements": {
        "framework": "FastAPI",
        "token_expiry": "1_hour",
        "algorithms": ["HS256", "RS256"]
    },
    "acceptance_criteria": [
        "Users can login and receive JWT tokens",
        "Tokens are validated on protected endpoints",
        "Invalid tokens are rejected with 401 status"
    ]
}

# Bad: Vague task
task = {
    "description": "Add authentication",
    "requirements": {}
}
```

#### Context Provision
```python
# Provide rich context
context = {
    "existing_codebase": "path/to/code",
    "architecture": "microservices",
    "security_requirements": "OWASP_top_10",
    "performance_requirements": "1000_rps",
    "compliance": ["GDPR", "HIPAA"]
}
```

#### Quality Validation
```python
# Always validate results
validation = await qa.validate_result(
    task_id=task_id,
    expected_outcomes=["authentication_works", "security_tested", "docs_updated"]
)

if validation["passed"]:
    print("✅ Task completed successfully")
else:
    print(f"❌ Validation failed: {validation['issues']}")
```

### Error Handling

#### Graceful Degradation
```python
try:
    result = await agent.execute_task(task)
except AgentUnavailableError:
    # Fallback to alternative agent
    result = await fallback_agent.execute_task(task)
except TaskFailedError as e:
    # Log and retry with different approach
    logger.error(f"Task failed: {e}")
    result = await agent.retry_task(task, alternative_approach=True)
```

#### Circuit Breaker Pattern
```python
from santiago_core.resilience import CircuitBreaker

breaker = CircuitBreaker(
    failure_threshold=5,
    recovery_timeout=60
)

@breaker.protect
async def execute_with_agent(agent, task):
    return await agent.execute_task(task)

# Usage
try:
    result = await execute_with_agent(agent, task)
except CircuitBreakerOpenError:
    print("Agent temporarily unavailable, using cache")
    result = get_cached_result(task)
```

### Resource Management

#### Connection Pooling
```python
from santiago_core.connection import ConnectionPool

pool = ConnectionPool(
    agent_type="santiago-developer",
    max_connections=10,
    timeout=30
)

async with pool.get_connection() as agent:
    result = await agent.execute_task(task)
```

#### Rate Limiting
```python
from santiago_core.rate_limit import RateLimiter

limiter = RateLimiter(
    requests_per_minute=60,
    burst_limit=10
)

@limiter.limit
async def execute_task_with_rate_limit(agent, task):
    return await agent.execute_task(task)
```

---

## 🔧 Development & Extension

### Building New Agents

Create custom agents for specific domains:

```python
from santiago_core.agents import BaseAgent
from santiago_core.knowledge import DomainKnowledge

class CustomDomainAgent(BaseAgent):
    """Custom agent for specific domain."""

    def __init__(self):
        super().__init__(agent_type="custom-domain")
        self.knowledge = DomainKnowledge("custom_domain")
        self.capabilities = ["analysis", "recommendation", "implementation"]

    async def analyze_domain(self, context):
        """Analyze domain-specific requirements."""
        # Domain analysis logic
        pass

    async def generate_recommendations(self, analysis):
        """Generate domain-specific recommendations."""
        # Recommendation logic
        pass

    async def implement_solution(self, recommendations):
        """Implement the recommended solution."""
        # Implementation logic
        pass
```

### Extending Capabilities

Add new capabilities to existing agents:

```python
from santiago_core.agents import AgentExtension

class CustomCapability(AgentExtension):
    """Add custom capability to agents."""

    def __init__(self, agent):
        self.agent = agent

    async def execute_custom_task(self, task):
        """Execute custom task type."""
        # Custom logic
        pass

# Extend existing agent
developer_agent.add_extension(CustomCapability(developer_agent))
```

---

## 📚 Learning Resources

### Key Documentation
- **[Agent Manual](../agents/manual.md)** - Detailed agent capabilities
- **[MCP Guide](../api/mcp-guide.md)** - Protocol integration
- **[Knowledge Graph API](../api/knowledge-graph.md)** - Data access
- **[Workflow Engine](../api/workflow-engine.md)** - Orchestration

### Examples & Tutorials
- **[Basic Agent Interaction](../examples/agent-interaction.md)** - Simple examples
- **[Workflow Examples](../examples/workflows/)** - Complex orchestrations
- **[Integration Patterns](../examples/integration-patterns.md)** - Best practices

### API Reference
- **[REST API](../api/reference.md)** - HTTP endpoints
- **[Python SDK](../api/python-sdk.md)** - Direct integration
- **[MCP Specification](../api/mcp-spec.md)** - Protocol details

---

## 🆘 Troubleshooting

### Common Issues

#### Connection Problems
```python
# Check service health
health = await client.health_check()
if not health["status"] == "healthy":
    print(f"Service unhealthy: {health['issues']}")

# Verify network connectivity
import socket
sock = socket.socket()
try:
    sock.connect(("localhost", 8000))
    print("✅ Network connection OK")
except:
    print("❌ Cannot connect to Santiago service")
```

#### Agent Unavailable
```python
# Check agent status
agent_status = await client.get_agent_status("santiago-developer")
if agent_status["state"] != "available":
    print(f"Agent busy: {agent_status['current_task']}")

# Wait for availability
await client.wait_for_agent("santiago-developer", timeout=300)
```

#### Task Failures
```python
# Get detailed error information
task_result = await client.get_task_result(task_id)
if task_result["status"] == "failed":
    print(f"Failure reason: {task_result['error']}")
    print(f"Suggestions: {task_result['recovery_suggestions']}")

# Retry with modifications
retry_result = await client.retry_task(
    task_id,
    modifications={"approach": "alternative_method"}
)
```

### Performance Optimization

#### Caching Strategies
```python
from santiago_core.cache import KnowledgeCache

cache = KnowledgeCache(ttl=3600)  # 1 hour TTL

@cache.cached
async def get_domain_knowledge(domain, query):
    return await kg.query_domain(domain, query)
```

#### Batch Processing
```python
# Process multiple tasks efficiently
batch_result = await client.execute_batch([
    {"agent": "santiago-developer", "task": task1},
    {"agent": "santiago-developer", "task": task2},
    {"agent": "santiago-qa", "task": test_task}
])
```

---

## 🎯 Next Steps

### Getting Started
1. **Set up MCP connection** to Santiago
2. **Explore available agents** and their capabilities
3. **Try simple tasks** with individual agents
4. **Build basic workflows** combining multiple agents

### Advanced Usage
1. **Implement custom agents** for your domain
2. **Create complex workflows** with conditional logic
3. **Integrate monitoring** and quality assurance
4. **Contribute back** improvements to the ecosystem

### Best Practices
- **Start small** with simple tasks
- **Validate results** before proceeding
- **Monitor performance** and quality metrics
- **Handle errors gracefully** with fallbacks
- **Document your integrations** for others

---

*Welcome to the Santiago agent ecosystem! By following these guidelines, you'll be able to effectively collaborate with Santiago agents and build powerful multi-agent solutions. Remember: agents work best when given clear tasks, rich context, and proper validation.* 🤖✨