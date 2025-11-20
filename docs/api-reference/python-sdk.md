# 🐍 Python SDK Reference

Complete reference for Santiago's Python SDK, including classes, methods, examples, and integration patterns.

---

## 📦 Installation

Install the Santiago Python SDK:

```bash
pip install santiago-sdk
```

Or install with optional dependencies:

```bash
pip install santiago-sdk[dev,docs,examples]
```

---

## 🔧 Initialization

### Basic Setup

```python
from santiago import SantiagoClient

# Initialize with API key
client = SantiagoClient(api_key="your-api-key")

# Or use environment variable
import os
os.environ["SANTIAGO_API_KEY"] = "your-api-key"
client = SantiagoClient()  # Reads from env
```

### Advanced Configuration

```python
from santiago import SantiagoClient
from santiago.config import ClientConfig

config = ClientConfig(
    api_key="your-api-key",
    base_url="https://api.santiago.ai/v1",  # Custom endpoint
    timeout=30.0,  # Request timeout
    max_retries=3,  # Retry failed requests
    retry_delay=1.0,  # Delay between retries
    enable_compression=True,  # Compress requests
    debug=True  # Enable debug logging
)

client = SantiagoClient(config=config)
```

### Async Client

```python
import asyncio
from santiago import AsyncSantiagoClient

async def main():
    client = AsyncSantiagoClient(api_key="your-api-key")

    # Use async methods
    agents = await client.agents.list()
    print(agents)

asyncio.run(main())
```

---

## 🤖 Agents API

### List Agents

```python
# List all agents
agents = client.agents.list()
print(f"Found {len(agents)} agents")

# Filter by type
developers = client.agents.list(type="developer")
print(f"Found {len(developers)} developer agents")

# Filter by domain and status
python_devs = client.agents.list(
    type="developer",
    domain="python",
    status="available"
)
```

**Parameters:**
- `type` (str, optional): Agent type filter
- `domain` (str, optional): Domain filter
- `status` (str, optional): Status filter (`available`, `busy`, `offline`)
- `limit` (int, optional): Max results (default: 50)
- `offset` (int, optional): Pagination offset

**Returns:** List of `Agent` objects

### Get Agent Details

```python
agent = client.agents.get("agent-dev-py-001")
print(f"Agent: {agent.name}")
print(f"Capabilities: {agent.capabilities}")
print(f"Performance Score: {agent.performance_score}")
```

**Parameters:**
- `agent_id` (str): Agent identifier

**Returns:** `Agent` object

### Create Custom Agent

```python
from santiago.models import AgentConfig

config = AgentConfig(
    type="custom",
    domain="medical",
    capabilities=["diagnosis", "treatment-planning"],
    model="gpt-4",
    temperature=0.3,
    training_data={
        "examples": [
            {"input": "Patient symptoms", "output": "Diagnosis"},
            # ... more examples
        ]
    }
)

agent = client.agents.create(config)
print(f"Created agent: {agent.id}")
```

### Agent Object

```python
class Agent:
    id: str
    type: str
    domain: str
    capabilities: List[str]
    status: str
    performance_score: float
    quality_metrics: Dict[str, Any]
    created_at: datetime
    last_active: datetime

    def is_available(self) -> bool:
        """Check if agent is available for tasks"""
        return self.status == "available"

    def supports_capability(self, capability: str) -> bool:
        """Check if agent supports a capability"""
        return capability in self.capabilities
```

---

## 🎯 Tasks API

### Submit Task

```python
from santiago.models import TaskRequest

# Simple task submission
task = client.tasks.submit({
    "type": "code-review",
    "context": {
        "repository": "myorg/myrepo",
        "pull_request": 123,
        "files": ["api/auth.py"]
    }
})
print(f"Task submitted: {task.id}")

# Advanced task with constraints
task_request = TaskRequest(
    type="feature-development",
    requirements="Implement OAuth2 authentication",
    context={
        "repository": "myorg/myrepo",
        "branch": "feature/oauth",
        "framework": "FastAPI"
    },
    constraints={
        "deadline": "2024-02-01T00:00:00Z",
        "quality_threshold": 0.9,
        "max_cost": 1000
    },
    priority="high"
)

task = client.tasks.submit(task_request)
```

**Parameters:**
- `task_request`: Task specification (dict or TaskRequest object)

**Returns:** `Task` object

### Get Task Status

```python
task = client.tasks.get("task-456")
print(f"Status: {task.status}")
print(f"Progress: {task.progress.percentage}%")

if task.status == "completed":
    result = client.tasks.get_result(task.id)
    print(f"Result: {result}")
elif task.status == "failed":
    print(f"Error: {task.error}")
```

### Get Task Result

```python
result = client.tasks.get_result("task-456")

# Access result data
if result.success:
    print("Task completed successfully")
    print(f"Quality score: {result.quality_score}")
    print(f"Output: {result.data}")
else:
    print(f"Task failed: {result.error}")
```

### Cancel Task

```python
success = client.tasks.cancel("task-456")
if success:
    print("Task cancelled successfully")
```

### List Tasks

```python
# Get recent tasks
recent_tasks = client.tasks.list(limit=10)

# Filter by status and type
completed_reviews = client.tasks.list(
    status="completed",
    type="code-review",
    limit=50
)

# Filter by date range
from datetime import datetime, timedelta

week_ago = datetime.now() - timedelta(days=7)
recent_tasks = client.tasks.list(
    created_after=week_ago,
    status="completed"
)
```

### Task Object

```python
class Task:
    id: str
    type: str
    status: str  # queued, in_progress, completed, failed, cancelled
    agent_id: Optional[str]
    priority: str
    progress: TaskProgress
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    estimated_completion: Optional[datetime]

class TaskProgress:
    percentage: int
    current_step: str
    steps_completed: List[str]
    steps_remaining: List[str]
    estimated_time_remaining: Optional[int]  # seconds
```

### Task Result Object

```python
class TaskResult:
    task_id: str
    success: bool
    data: Any  # Task-specific result data
    quality_score: Optional[float]
    execution_time: int  # seconds
    cost: Optional[float]
    error: Optional[str]
    metadata: Dict[str, Any]
```

---

## 🧠 Knowledge API

### Query Knowledge

```python
# Simple SPARQL query
results = client.knowledge.query("""
    SELECT ?feature ?status WHERE {
        ?feature rdf:type santiago:Feature ;
                 santiago:status ?status
    }
""")

for result in results:
    print(f"{result['feature']}: {result['status']}")

# Query with parameters
query = """
    SELECT ?item ?value WHERE {
        ?item santiago:priority ?value .
        FILTER(?value > $min_priority)
    }
"""

results = client.knowledge.query(query, parameters={"min_priority": 7})
```

**Parameters:**
- `query` (str): SPARQL query string
- `parameters` (dict, optional): Query parameters
- `domain` (str, optional): Knowledge domain filter
- `limit` (int, optional): Result limit

**Returns:** List of result dictionaries

### Add Knowledge

```python
# Add single fact
client.knowledge.add_fact(
    subject="feature-123",
    predicate="hasStatus",
    object="completed",
    domain="product-management"
)

# Add multiple facts
facts = [
    {
        "subject": "feature-123",
        "predicate": "completedAt",
        "object": "2024-01-15T10:00:00Z"
    },
    {
        "subject": "feature-123",
        "predicate": "qualityScore",
        "object": 0.95
    }
]

client.knowledge.add_facts(facts, domain="product-management")
```

### Search Knowledge

```python
# Semantic search
results = client.knowledge.search(
    query="user authentication best practices",
    domain="security",
    limit=10,
    threshold=0.7
)

for result in results:
    print(f"Match: {result['text']} (score: {result['score']})")
```

### Knowledge Stats

```python
stats = client.knowledge.get_stats()
print(f"Total facts: {stats['total_facts']}")
print(f"Domains: {stats['domains']}")

# Domain-specific stats
pm_stats = client.knowledge.get_stats(domain="product-management")
print(f"PM facts: {pm_stats['total_facts']}")
```

---

## 📊 Analytics API

### Agent Performance

```python
# Get agent performance metrics
performance = client.analytics.get_agent_performance(
    agent_id="agent-dev-py-001",
    period="30d"  # 1d, 7d, 30d, 90d
)

print(f"Tasks completed: {performance.tasks_completed}")
print(f"Success rate: {performance.success_rate}")
print(f"Avg response time: {performance.avg_response_time}s")
```

### System Health

```python
health = client.analytics.get_system_health()
print(f"Status: {health.status}")
print(f"Uptime: {health.uptime}")
print(f"Services: {health.services}")

# Check specific service
if health.services['database'] == 'healthy':
    print("Database is healthy")
```

### Usage Metrics

```python
usage = client.analytics.get_usage(
    start_date="2024-01-01",
    end_date="2024-01-31",
    group_by="day"
)

for period in usage.periods:
    print(f"{period.date}: {period.requests} requests, ${period.cost}")
```

---

## ⚙️ Webhooks API

### Register Webhook

```python
webhook = client.webhooks.register(
    url="https://my-app.com/webhooks/santiago",
    events=["task.completed", "task.failed", "agent.created"],
    secret="webhook-secret-123",
    active=True
)
print(f"Webhook registered: {webhook.id}")
```

### List Webhooks

```python
webhooks = client.webhooks.list()
for webhook in webhooks:
    print(f"{webhook.id}: {webhook.url} ({webhook.status})")
```

### Update Webhook

```python
client.webhooks.update(
    webhook_id="webhook-123",
    events=["task.completed", "agent.updated"],  # Add new event
    active=True
)
```

### Delete Webhook

```python
client.webhooks.delete("webhook-123")
```

### Webhook Object

```python
class Webhook:
    id: str
    url: str
    events: List[str]
    secret: str
    active: bool
    created_at: datetime
    last_triggered: Optional[datetime]
    failure_count: int
```

---

## 🔄 Async Operations

### Async Client Usage

```python
import asyncio
from santiago import AsyncSantiagoClient

async def process_tasks():
    client = AsyncSantiagoClient(api_key="your-api-key")

    # Submit multiple tasks concurrently
    tasks = []
    for i in range(10):
        task = await client.tasks.submit({
            "type": "code-review",
            "context": {"file": f"code_{i}.py"}
        })
        tasks.append(task)

    # Wait for all to complete
    completed_tasks = []
    for task in tasks:
        while True:
            status = await client.tasks.get(task.id)
            if status.status == "completed":
                result = await client.tasks.get_result(task.id)
                completed_tasks.append(result)
                break
            elif status.status == "failed":
                print(f"Task {task.id} failed")
                break
            await asyncio.sleep(5)  # Wait 5 seconds

    return completed_tasks

results = asyncio.run(process_tasks())
```

### Streaming Results

```python
async def stream_task_progress(task_id):
    client = AsyncSantiagoClient(api_key="your-api-key")

    async for progress in client.tasks.stream_progress(task_id):
        print(f"Progress: {progress.percentage}% - {progress.current_step}")
        if progress.percentage == 100:
            break
```

---

## 🛠️ Advanced Features

### Custom Agent Classes

```python
from santiago.agents import BaseAgent

class CustomCodeReviewer(BaseAgent):
    def __init__(self, client, **kwargs):
        super().__init__(client, **kwargs)
        self.capabilities = ["code-review", "security-audit"]

    async def review_code(self, code, language, standards=None):
        """Custom code review method"""
        if standards is None:
            standards = ["PEP8", "security", "performance"]

        task = await self.client.tasks.submit({
            "type": "code-review",
            "context": {
                "code": code,
                "language": language,
                "standards": standards
            }
        })

        # Wait for completion
        result = await self.wait_for_task(task.id)
        return self.parse_review_result(result)

    def parse_review_result(self, result):
        """Parse and structure review results"""
        return {
            "issues": result.data.get("issues", []),
            "suggestions": result.data.get("recommendations", []),
            "score": result.quality_score
        }

# Usage
reviewer = CustomCodeReviewer(client)
result = await reviewer.review_code(
    code="def hello(): return 'world'",
    language="python"
)
```

### Batch Operations

```python
from santiago.batch import BatchProcessor

processor = BatchProcessor(client)

# Batch task submission
task_requests = [
    {"type": "code-review", "context": {"file": "auth.py"}},
    {"type": "testing", "context": {"file": "test_auth.py"}},
    {"type": "documentation", "context": {"file": "auth.py"}}
]

batch_results = await processor.submit_batch(task_requests)

# Process results
for result in batch_results:
    if result.success:
        print(f"Task {result.task_id} completed with score {result.quality_score}")
    else:
        print(f"Task {result.task_id} failed: {result.error}")
```

### Caching Layer

```python
from santiago.cache import ResultCache
from santiago import SantiagoClient

# Add caching to client
cache = ResultCache(ttl=3600)  # 1 hour TTL
client = SantiagoClient(api_key="your-api-key", cache=cache)

# Cached knowledge queries
results1 = client.knowledge.query("SELECT * WHERE { ?s ?p ?o } LIMIT 100")
results2 = client.knowledge.query("SELECT * WHERE { ?s ?p ?o } LIMIT 100")
# results2 comes from cache

# Cached task results
result1 = client.tasks.get_result("task-123")
result2 = client.tasks.get_result("task-123")
# result2 comes from cache
```

### Error Handling

```python
from santiago.exceptions import (
    SantiagoError, AuthenticationError, ValidationError,
    RateLimitError, NotFoundError, ServerError
)

try:
    result = client.tasks.submit(task_request)
except AuthenticationError:
    print("Invalid API key")
    # Re-authenticate
except ValidationError as e:
    print(f"Invalid request: {e.details}")
    # Fix validation issues
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after} seconds")
    time.sleep(e.retry_after)
    result = client.tasks.submit(task_request)
except ServerError:
    print("Server error, retrying...")
    result = client.tasks.submit(task_request)
except SantiagoError as e:
    print(f"Santiago error: {e.code} - {e.message}")
```

### Logging and Monitoring

```python
import logging
from santiago.logging import SantiagoLogger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = SantiagoLogger(client)

# Log all API calls
logger.enable_request_logging()

# Custom metrics
with logger.measure_operation("complex_task"):
    # Your complex operation
    result = await client.tasks.submit(complex_task)
    await client.tasks.wait_for_completion(result.id)

# Export metrics
metrics = logger.get_metrics()
print(f"Total requests: {metrics['total_requests']}")
print(f"Success rate: {metrics['success_rate']}")
print(f"Average latency: {metrics['avg_latency']}ms")
```

---

## 🔧 Configuration

### Environment Variables

```bash
export SANTIAGO_API_KEY="your-api-key"
export SANTIAGO_BASE_URL="https://api.santiago.ai/v1"
export SANTIAGO_TIMEOUT="30.0"
export SANTIAGO_MAX_RETRIES="3"
export SANTIAGO_DEBUG="true"
```

### Configuration File

```python
# santiago_config.py
from santiago.config import ClientConfig

config = ClientConfig(
    api_key="your-api-key",
    base_url="https://api.santiago.ai/v1",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0,
    enable_compression=True,
    debug=False,
    proxies={
        "http": "http://proxy.company.com:8080",
        "https": "https://proxy.company.com:8080"
    },
    headers={
        "User-Agent": "MyApp/1.0",
        "X-Custom-Header": "value"
    }
)
```

### SSL Configuration

```python
from santiago.config import ClientConfig
import ssl

# Custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

config = ClientConfig(
    api_key="your-api-key",
    ssl_context=ssl_context
)
```

---

## 📚 Examples

### Code Review Workflow

```python
import asyncio
from santiago import AsyncSantiagoClient

async def review_pull_request(repo, pr_number):
    client = AsyncSantiagoClient(api_key="your-api-key")

    # Get PR details (assuming you have GitHub integration)
    pr_files = get_pr_files(repo, pr_number)

    # Submit review tasks for each file
    review_tasks = []
    for file_path in pr_files:
        if is_code_file(file_path):
            code = get_file_content(repo, pr_number, file_path)
            task = await client.tasks.submit({
                "type": "code-review",
                "context": {
                    "repository": repo,
                    "pull_request": pr_number,
                    "file": file_path,
                    "code": code,
                    "language": detect_language(file_path)
                }
            })
            review_tasks.append(task)

    # Wait for all reviews to complete
    results = []
    for task in review_tasks:
        result = await client.tasks.wait_for_completion(task.id)
        results.append(result)

    # Generate summary report
    summary = generate_review_summary(results)
    return summary
```

### Knowledge Base Integration

```python
from santiago import SantiagoClient

def update_knowledge_base(project_data):
    client = SantiagoClient(api_key="your-api-key")

    # Add project facts
    facts = []
    for feature in project_data['features']:
        facts.extend([
            {
                "subject": f"feature:{feature['id']}",
                "predicate": "rdf:type",
                "object": "santiago:Feature"
            },
            {
                "subject": f"feature:{feature['id']}",
                "predicate": "santiago:title",
                "object": feature['title']
            },
            {
                "subject": f"feature:{feature['id']}",
                "predicate": "santiago:status",
                "object": feature['status']
            }
        ])

    client.knowledge.add_facts(facts, domain="product-management")

    # Query for insights
    insights = client.knowledge.query("""
        SELECT ?status (COUNT(?feature) as ?count) WHERE {
            ?feature rdf:type santiago:Feature ;
                     santiago:status ?status
        } GROUP BY ?status
    """)

    return insights
```

### Multi-Agent Coordination

```python
import asyncio
from santiago import AsyncSantiagoClient

class DevelopmentTeam:
    def __init__(self, api_key):
        self.client = AsyncSantiagoClient(api_key=api_key)
        self.agents = {}

    async def initialize_team(self):
        # Get available agents
        agents = await self.client.agents.list()

        # Organize by role
        self.agents = {
            'developer': [a for a in agents if a.type == 'developer'],
            'tester': [a for a in agents if a.type == 'quality-assurance'],
            'architect': [a for a in agents if a.type == 'architect']
        }

    async def develop_feature(self, feature_spec):
        # Step 1: Architecture review
        architect = self.agents['architect'][0]
        arch_task = await self.client.tasks.submit({
            "type": "architecture-review",
            "agent_id": architect.id,
            "context": feature_spec
        })
        arch_result = await self.client.tasks.wait_for_completion(arch_task.id)

        # Step 2: Implementation
        dev_tasks = []
        for component in arch_result.data['components']:
            dev_agent = self.select_best_developer(component)
            dev_task = await self.client.tasks.submit({
                "type": "feature-development",
                "agent_id": dev_agent.id,
                "context": {
                    "component": component,
                    "architecture": arch_result.data
                }
            })
            dev_tasks.append(dev_task)

        # Wait for development completion
        dev_results = await asyncio.gather(*[
            self.client.tasks.wait_for_completion(task.id)
            for task in dev_tasks
        ])

        # Step 3: Testing
        test_task = await self.client.tasks.submit({
            "type": "integration-testing",
            "agent_id": self.agents['tester'][0].id,
            "context": {
                "components": dev_results,
                "feature_spec": feature_spec
            }
        })
        test_result = await self.client.tasks.wait_for_completion(test_task.id)

        return {
            "architecture": arch_result,
            "development": dev_results,
            "testing": test_result
        }

    def select_best_developer(self, component):
        # Select developer based on component requirements
        # Implementation depends on your selection criteria
        return self.agents['developer'][0]
```

---

*For more examples and detailed API documentation, see the [REST API Reference](rest-api.md) and [MCP Integration Guide](mcp-integration.md).* 