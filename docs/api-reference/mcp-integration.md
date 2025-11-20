# 🤖 MCP Integration Guide

Complete guide for integrating AI agents with Santiago using the Model Context Protocol (MCP). This guide covers MCP contracts, tool definitions, and best practices for agent integration.

---

## 📋 What is MCP?

The **Model Context Protocol (MCP)** is a standardized protocol for connecting AI models and agents to external tools and data sources. Santiago implements MCP to provide seamless integration for AI agents.

### Key Benefits

- **Standardized Interface**: Consistent API across different agent platforms
- **Tool Discovery**: Agents can automatically discover available Santiago capabilities
- **Secure Communication**: Built-in authentication and authorization
- **Real-time Updates**: WebSocket-based communication for live interactions

---

## 🔌 Connection Setup

### WebSocket Connection

Connect to Santiago's MCP server using WebSocket:

```javascript
const WebSocket = require('ws');

const ws = new WebSocket('ws://localhost:8000/mcp', {
  headers: {
    'Authorization': 'Bearer YOUR_AGENT_TOKEN'
  }
});

ws.on('open', () => {
  console.log('Connected to Santiago MCP');
});

ws.on('message', (data) => {
  const message = JSON.parse(data.toString());
  handleMessage(message);
});
```

### Authentication

Agents must authenticate using agent tokens:

```javascript
// Request agent token
const tokenResponse = await fetch('/api/v1/auth/agent-token', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    agent_id: 'your-agent-id',
    capabilities: ['code-review', 'testing'],
    permissions: ['read', 'write']
  })
});

const { token } = await tokenResponse.json();
```

---

## 📡 Protocol Messages

### JSON-RPC 2.0 Format

All MCP messages follow JSON-RPC 2.0 specification:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

### Response Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [...]
  }
}
```

### Error Format

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found",
    "data": {
      "details": "Available methods: tools/list, tools/call"
    }
  }
}
```

---

## 🛠️ Tool Discovery

### List Available Tools

Get a list of all available Santiago tools:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "santiago.code-review",
        "description": "Review code for quality, security, and best practices",
        "inputSchema": {
          "type": "object",
          "properties": {
            "code": {
              "type": "string",
              "description": "The code to review"
            },
            "language": {
              "type": "string",
              "enum": ["python", "javascript", "java", "go"],
              "description": "Programming language"
            },
            "standards": {
              "type": "array",
              "items": { "type": "string" },
              "description": "Coding standards to check"
            }
          },
          "required": ["code", "language"]
        }
      },
      {
        "name": "santiago.task-submit",
        "description": "Submit a task to the Santiago factory",
        "inputSchema": {
          "type": "object",
          "properties": {
            "type": {
              "type": "string",
              "enum": ["feature-development", "testing", "documentation"],
              "description": "Type of task"
            },
            "requirements": {
              "type": "string",
              "description": "Task requirements"
            },
            "context": {
              "type": "object",
              "description": "Additional context"
            }
          },
          "required": ["type", "requirements"]
        }
      }
    ]
  }
}
```

### Tool Categories

Santiago provides tools in several categories:

#### Development Tools
- `santiago.code-review`: Code quality analysis
- `santiago.code-generate`: Generate code from specifications
- `santiago.refactor`: Code refactoring suggestions
- `santiago.debug`: Debugging assistance

#### Testing Tools
- `santiago.test-generate`: Generate test cases
- `santiago.test-execute`: Run test suites
- `santiago.coverage-analyze`: Code coverage analysis

#### Project Management Tools
- `santiago.requirements-analyze`: Requirements analysis
- `santiago.task-breakdown`: Task decomposition
- `santiago.progress-track`: Progress tracking

#### Knowledge Tools
- `santiago.knowledge-query`: Query knowledge graph
- `santiago.knowledge-add`: Add new knowledge
- `santiago.learning-update`: Update agent learning

---

## 🔧 Tool Execution

### Calling Tools

Execute a tool using the `tools/call` method:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "santiago.code-review",
    "arguments": {
      "code": "def hello_world():\n    print('Hello, World!')",
      "language": "python",
      "standards": ["PEP8", "security"]
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "## Code Review Results\n\n### Issues Found\n1. **PEP8 Compliance**: Function name should be `hello_world` (current) or `helloWorld` (alternative)\n2. **Documentation**: Missing docstring\n\n### Suggestions\n- Add type hints\n- Include error handling\n- Add unit tests\n\n### Security Analysis\n✅ No security vulnerabilities detected"
      }
    ],
    "isError": false
  }
}
```

### Asynchronous Tool Calls

For long-running tasks, use asynchronous execution:

```javascript
// Submit async task
const submitResponse = await callTool('santiago.task-submit', {
  type: 'feature-development',
  requirements: 'Implement user authentication',
  context: { priority: 'high' }
});

const taskId = submitResponse.task_id;

// Poll for completion
const checkStatus = async () => {
  const status = await callTool('santiago.task-status', { task_id: taskId });
  if (status.status === 'completed') {
    const result = await callTool('santiago.task-result', { task_id: taskId });
    return result;
  } else {
    setTimeout(checkStatus, 5000); // Check again in 5 seconds
  }
};
```

---

## 📊 Resources

### Resource Discovery

List available resources (files, documents, etc.):

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "resources/list",
  "params": {}
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "resources": [
      {
        "uri": "file:///workspace/src/main.py",
        "name": "Main application file",
        "description": "Core application logic",
        "mimeType": "text/x-python"
      },
      {
        "uri": "santiago://knowledge/python-best-practices",
        "name": "Python best practices",
        "description": "Knowledge base for Python development",
        "mimeType": "application/json"
      }
    ]
  }
}
```

### Reading Resources

Read content from a resource:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "resources/read",
  "params": {
    "uri": "file:///workspace/src/main.py"
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "contents": [
      {
        "uri": "file:///workspace/src/main.py",
        "mimeType": "text/x-python",
        "text": "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()"
      }
    ]
  }
}
```

---

## 📢 Notifications

### Subscribing to Notifications

Subscribe to real-time notifications:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "notifications/subscribe",
  "params": {
    "events": ["task.completed", "agent.updated", "knowledge.changed"]
  }
}
```

### Receiving Notifications

Notifications are sent asynchronously:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/event",
  "params": {
    "event": "task.completed",
    "data": {
      "task_id": "task-123",
      "result": { ... },
      "timestamp": "2024-01-15T10:30:00Z"
    }
  }
}
```

---

## 🔄 Sampling

### Creating Samples

Request sampling from Santiago's knowledge:

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "sampling/createMessage",
  "params": {
    "messages": [
      {
        "role": "user",
        "content": {
          "type": "text",
          "text": "How should I implement user authentication?"
        }
      }
    ],
    "maxTokens": 1000,
    "temperature": 0.7,
    "includeContext": true
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "model": "santiago-expert",
    "role": "assistant",
    "content": {
      "type": "text",
      "text": "Based on security best practices and our knowledge base, here's how to implement user authentication..."
    },
    "usage": {
      "inputTokens": 15,
      "outputTokens": 234,
      "totalTokens": 249
    }
  }
}
```

---

## 🏗️ Agent Development

### Santiago Agent Template

```javascript
class SantiagoAgent {
  constructor(ws) {
    this.ws = ws;
    this.requestId = 0;
    this.pendingRequests = new Map();
  }

  async connect() {
    // Initialize connection
    await this.listTools();
    await this.subscribeToNotifications();
  }

  async listTools() {
    const response = await this.sendRequest('tools/list');
    this.tools = response.result.tools;
    return this.tools;
  }

  async callTool(name, args) {
    return await this.sendRequest('tools/call', {
      name: name,
      arguments: args
    });
  }

  async sendRequest(method, params = {}) {
    const id = ++this.requestId;
    const request = {
      jsonrpc: '2.0',
      id: id,
      method: method,
      params: params
    };

    return new Promise((resolve, reject) => {
      this.pendingRequests.set(id, { resolve, reject });
      this.ws.send(JSON.stringify(request));
    });
  }

  handleMessage(message) {
    if (message.id && this.pendingRequests.has(message.id)) {
      const { resolve, reject } = this.pendingRequests.get(message.id);
      this.pendingRequests.delete(message.id);

      if (message.error) {
        reject(message.error);
      } else {
        resolve(message.result);
      }
    } else if (message.method === 'notifications/event') {
      this.handleNotification(message.params);
    }
  }

  handleNotification(event) {
    console.log('Received notification:', event.event, event.data);
    // Handle different event types
    switch (event.event) {
      case 'task.completed':
        this.onTaskCompleted(event.data);
        break;
      case 'agent.updated':
        this.onAgentUpdated(event.data);
        break;
    }
  }

  // Override these methods in subclasses
  onTaskCompleted(data) { }
  onAgentUpdated(data) { }
}
```

### Specialized Agent Example

```javascript
class CodeReviewAgent extends SantiagoAgent {
  async reviewCode(code, language) {
    const result = await this.callTool('santiago.code-review', {
      code: code,
      language: language,
      standards: ['security', 'performance', 'maintainability']
    });

    return this.parseReviewResult(result);
  }

  parseReviewResult(result) {
    // Parse and structure the review results
    const content = result.content[0].text;
    return {
      issues: this.extractIssues(content),
      suggestions: this.extractSuggestions(content),
      score: this.calculateScore(content)
    };
  }

  async onTaskCompleted(data) {
    if (data.type === 'code-review') {
      console.log(`Code review completed for task ${data.task_id}`);
      // Process review results
      await this.processReviewResults(data.result);
    }
  }
}
```

---

## 🔒 Security Best Practices

### Token Management

- Store agent tokens securely (never in code)
- Rotate tokens regularly
- Use different tokens for different environments

### Input Validation

Always validate inputs before sending to Santiago:

```javascript
function validateToolCall(name, args) {
  const tool = tools.find(t => t.name === name);
  if (!tool) {
    throw new Error(`Unknown tool: ${name}`);
  }

  // Validate against schema
  const { error } = validate(args, tool.inputSchema);
  if (error) {
    throw new Error(`Invalid arguments: ${error.message}`);
  }

  return true;
}
```

### Error Handling

Implement robust error handling:

```javascript
async function safeToolCall(name, args) {
  try {
    const result = await callTool(name, args);
    return result;
  } catch (error) {
    if (error.code === -32700) {
      // Parse error - retry with corrected JSON
      console.error('JSON parse error, retrying...');
      return await callTool(name, args);
    } else if (error.code === -32601) {
      // Method not found
      throw new Error(`Tool ${name} not available`);
    } else {
      // Other errors
      console.error('Tool call failed:', error);
      throw error;
    }
  }
}
```

### Rate Limiting

Respect rate limits and implement backoff:

```javascript
class RateLimitedAgent extends SantiagoAgent {
  constructor(ws) {
    super(ws);
    this.requestsPerMinute = 0;
    this.resetTime = Date.now() + 60000;
  }

  async sendRequest(method, params) {
    if (Date.now() > this.resetTime) {
      this.requestsPerMinute = 0;
      this.resetTime = Date.now() + 60000;
    }

    if (this.requestsPerMinute >= 60) {
      const waitTime = this.resetTime - Date.now();
      await new Promise(resolve => setTimeout(resolve, waitTime));
      return this.sendRequest(method, params);
    }

    this.requestsPerMinute++;
    return super.sendRequest(method, params);
  }
}
```

---

## 📊 Monitoring & Debugging

### Connection Health

Monitor connection health:

```javascript
class MonitoredAgent extends SantiagoAgent {
  constructor(ws) {
    super(ws);
    this.lastHeartbeat = Date.now();
    this.heartbeatInterval = setInterval(() => this.sendHeartbeat(), 30000);
  }

  sendHeartbeat() {
    this.sendRequest('ping').catch(() => {
      console.error('Heartbeat failed, reconnecting...');
      this.reconnect();
    });
  }

  handleMessage(message) {
    super.handleMessage(message);
    this.lastHeartbeat = Date.now();
  }
}
```

### Logging

Implement comprehensive logging:

```javascript
class LoggingAgent extends SantiagoAgent {
  log(level, message, data = {}) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level: level,
      message: message,
      agent: this.constructor.name,
      ...data
    };
    console.log(JSON.stringify(logEntry));
  }

  async callTool(name, args) {
    this.log('info', 'Calling tool', { tool: name, args });
    try {
      const result = await super.callTool(name, args);
      this.log('info', 'Tool call successful', { tool: name });
      return result;
    } catch (error) {
      this.log('error', 'Tool call failed', { tool: name, error: error.message });
      throw error;
    }
  }
}
```

---

## 🚀 Advanced Patterns

### Multi-Agent Coordination

Coordinate multiple agents for complex tasks:

```javascript
class CoordinatorAgent extends SantiagoAgent {
  constructor(ws) {
    super(ws);
    this.subAgents = [];
  }

  async addSubAgent(agent) {
    this.subAgents.push(agent);
    await agent.connect();
  }

  async executeComplexTask(task) {
    // Break down complex task
    const subtasks = await this.callTool('santiago.task-breakdown', {
      task: task.description
    });

    // Assign to appropriate agents
    const results = await Promise.all(
      subtasks.map((subtask, index) =>
        this.subAgents[index % this.subAgents.length]
          .executeTask(subtask)
      )
    );

    // Combine results
    return await this.callTool('santiago.results-synthesis', {
      results: results,
      original_task: task
    });
  }
}
```

### Learning and Adaptation

Implement learning from interactions:

```javascript
class LearningAgent extends SantiagoAgent {
  constructor(ws) {
    super(ws);
    this.learningHistory = [];
  }

  async callTool(name, args) {
    const startTime = Date.now();
    const result = await super.callTool(name, args);
    const duration = Date.now() - startTime;

    // Record learning data
    this.learningHistory.push({
      tool: name,
      args: args,
      result: result,
      duration: duration,
      success: !result.isError,
      timestamp: new Date().toISOString()
    });

    // Update knowledge
    if (this.learningHistory.length > 100) {
      await this.updateLearningModel();
    }

    return result;
  }

  async updateLearningModel() {
    const patterns = this.analyzePatterns();
    await this.callTool('santiago.learning-update', {
      patterns: patterns,
      agent_id: this.agentId
    });
  }
}
```

---

## 📚 MCP Extensions

### Custom Tool Development

Create custom tools for your agents:

```javascript
// Register custom tool
await sendRequest('tools/register', {
  name: 'my-custom-tool',
  description: 'My custom functionality',
  inputSchema: {
    type: 'object',
    properties: {
      input: { type: 'string' }
    },
    required: ['input']
  },
  handler: async (args) => {
    // Custom logic here
    return { result: `Processed: ${args.input}` };
  }
});
```

### Resource Provider

Provide custom resources:

```javascript
await sendRequest('resources/register', {
  uri: 'custom://my-resource',
  name: 'My Custom Resource',
  description: 'Provides custom data',
  mimeType: 'application/json',
  provider: async () => {
    return {
      contents: [{
        uri: 'custom://my-resource',
        mimeType: 'application/json',
        text: JSON.stringify({ data: 'custom data' })
      }]
    };
  }
});
```

---

## 🔗 Integration Examples

### VS Code Extension

```typescript
// vscode-santiago extension
import { SantiagoMCPClient } from './mcp-client';

export class SantiagoExtension {
  private client: SantiagoMCPClient;

  async activate() {
    this.client = new SantiagoMCPClient();
    await this.client.connect();

    // Register commands
    vscode.commands.registerCommand('santiago.reviewCode', async () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const code = editor.document.getText();
        const result = await this.client.callTool('santiago.code-review', {
          code: code,
          language: this.getLanguage(editor.document)
        });
        this.displayResults(result);
      }
    });
  }
}
```

### GitHub Actions

```yaml
# .github/workflows/santiago-review.yml
name: Santiago Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Santiago Review
        uses: santiago/github-action@v1
        with:
          api-key: ${{ secrets.SANTIAGO_API_KEY }}
          tool: 'code-review'
          language: 'python'
```

### Slack Bot

```javascript
// slack-santiago-bot
const { WebClient } = require('@slack/web-api');
const { SantiagoMCPClient } = require('santiago-mcp');

class SlackBot {
  constructor() {
    this.slack = new WebClient(process.env.SLACK_TOKEN);
    this.santiago = new SantiagoMCPClient();
  }

  async handleMessage(message) {
    if (message.text.startsWith('/santiago')) {
      const query = message.text.replace('/santiago', '').trim();
      const result = await this.santiago.callTool('santiago.knowledge-query', {
        query: query
      });

      await this.slack.chat.postMessage({
        channel: message.channel,
        text: result.content[0].text
      });
    }
  }
}
```

---

*This guide covers the core MCP integration patterns. For detailed API specifications and additional examples, see the [REST API Reference](rest-api.md) and [Python SDK Reference](python-sdk.md).* 