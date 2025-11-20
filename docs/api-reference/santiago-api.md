# API Documentation

**Generated:** 2025-11-20 16:00:17

## API Endpoints

- `GET /health` - health_check (santiago_core/api.py)
- `GET /tasks` - create_task (santiago_core/api.py)
- `GET /tasks` - list_tasks (santiago_core/api.py)
- `GET /agents` - list_agents (santiago_core/api.py)
- `GET /agents/{agent_name}/execute` - execute_agent_task (santiago_core/api.py)

## Classes

## Class: `HealthResponse`

**Location:** `santiago_core/api.py:21`

**Description:** No description

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.api import HealthResponse

instance = HealthResponse()
```


## Class: `TaskRequest`

**Location:** `santiago_core/api.py:28`

**Description:** No description

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.api import TaskRequest

instance = TaskRequest()
```


## Class: `MCPTool`

**Location:** `santiago_core/core/mcp_service.py:15`

**Description:** MCP Tool definition

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.core.mcp_service import MCPTool

instance = MCPTool()
```


## Class: `MCPToolResult`

**Location:** `santiago_core/core/mcp_service.py:23`

**Description:** MCP Tool execution result

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.core.mcp_service import MCPToolResult

instance = MCPToolResult()
```


## Class: `MCPServer`

**Location:** `santiago_core/core/mcp_service.py:29`

**Description:** Base MCP Server class

**Inheritance:** None

**Public Methods:**
- `__init__` - No description
- `register_tool` - Register an MCP tool
- `register_tool_handler` - Register a tool handler

**Usage Example:**
```python
from santiago_core.core.mcp_service import MCPServer

instance = MCPServer()
```


## Class: `Message`

**Location:** `santiago_core/core/agent_framework.py:19`

**Description:** Represents a message between agents

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.core.agent_framework import Message

instance = Message()
```


## Class: `Task`

**Location:** `santiago_core/core/agent_framework.py:29`

**Description:** Represents a development task

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.core.agent_framework import Task

instance = Task()
```


## Class: `AgentProtocol`

**Location:** `santiago_core/core/agent_framework.py:42`

**Description:** Protocol for agent communication

**Inheritance:** Protocol

**Public Methods:**


**Usage Example:**
```python
from santiago_core.core.agent_framework import AgentProtocol

instance = AgentProtocol()
```


## Class: `SantiagoAgent`

**Location:** `santiago_core/core/agent_framework.py:55`

**Description:** Base class for all Santiago autonomous agents

**Inheritance:** ABC

**Public Methods:**
- `__init__` - No description
- `register_peer` - Register another agent as a communication peer

**Usage Example:**
```python
from santiago_core.core.agent_framework import SantiagoAgent

instance = SantiagoAgent()
```


## Class: `EthicalOversight`

**Location:** `santiago_core/core/agent_framework.py:173`

**Description:** Provides ethical oversight for all agent actions

**Inheritance:** None

**Public Methods:**
- `evaluate_action` - Evaluate an action against ethical principles

**Usage Example:**
```python
from santiago_core.core.agent_framework import EthicalOversight

instance = EthicalOversight()
```


## Class: `SantiagoTeamCoordinator`

**Location:** `santiago_core/core/team_coordinator.py:20`

**Description:** Coordinates the autonomous development team

**Inheritance:** None

**Public Methods:**
- `__init__` - No description
- `_register_agent_peers` - Register agents as communication peers with each other
- `_determine_task_agent` - Determine which agent should handle a task

**Usage Example:**
```python
from santiago_core.core.team_coordinator import SantiagoTeamCoordinator

instance = SantiagoTeamCoordinator()
```


## Class: `TestProxyMessageBus`

**Location:** `santiago_core/tests/test_proxy_message_bus.py:16`

**Description:** Test proxy integration with message bus

**Inheritance:** None

**Public Methods:**
- `workspace` - Create test workspace
- `redis_available` - Check if Redis is available

**Usage Example:**
```python
from santiago_core.tests.test_proxy_message_bus import TestProxyMessageBus

instance = TestProxyMessageBus()
```


## Class: `TestEthicistProxyInitialization`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:31`

**Description:** Test Ethicist proxy initialization

**Inheritance:** None

**Public Methods:**
- `test_ethicist_proxy_creation` - Should initialize with Ethicist-specific manifest
- `test_bahai_principles_loaded` - Should load all 12 Baha'i principles
- `test_ethicist_tools_available` - Should have ethical review tools

**Usage Example:**
```python
from santiago_core.tests.test_ethicist_proxy import TestEthicistProxyInitialization

instance = TestEthicistProxyInitialization()
```


## Class: `TestEthicalReview`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:55`

**Description:** Test ethical review functionality

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_ethicist_proxy import TestEthicalReview

instance = TestEthicalReview()
```


## Class: `TestConsultationFacilitation`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:132`

**Description:** Test consultation facilitation

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_ethicist_proxy import TestConsultationFacilitation

instance = TestConsultationFacilitation()
```


## Class: `TestServiceAlignment`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:176`

**Description:** Test service to humanity alignment

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_ethicist_proxy import TestServiceAlignment

instance = TestServiceAlignment()
```


## Class: `TestPrincipleApplication`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:220`

**Description:** Test application of specific Baha'i principles

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_ethicist_proxy import TestPrincipleApplication

instance = TestPrincipleApplication()
```


## Class: `TestEthicalDecisionFramework`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:258`

**Description:** Test ethical decision framework

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_ethicist_proxy import TestEthicalDecisionFramework

instance = TestEthicalDecisionFramework()
```


## Class: `TestProxyTeamInitialization`

**Location:** `santiago_core/tests/test_proxy_integration.py:58`

**Description:** Test that all proxies initialize correctly

**Inheritance:** None

**Public Methods:**
- `test_all_proxies_created` - Should create all 7 proxy agents
- `test_unique_proxy_names` - Should have unique names for each proxy
- `test_budgets_configured` - Should have configured budgets

**Usage Example:**
```python
from santiago_core.tests.test_proxy_integration import TestProxyTeamInitialization

instance = TestProxyTeamInitialization()
```


## Class: `TestBacklogGroomingSession`

**Location:** `santiago_core/tests/test_proxy_integration.py:78`

**Description:** Test coordinated backlog grooming workflow

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_integration import TestBacklogGroomingSession

instance = TestBacklogGroomingSession()
```


## Class: `TestEthicalOversightIntegration`

**Location:** `santiago_core/tests/test_proxy_integration.py:139`

**Description:** Test ethical oversight is integrated throughout workflow

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_integration import TestEthicalOversightIntegration

instance = TestEthicalOversightIntegration()
```


## Class: `TestMultiProxyCollaboration`

**Location:** `santiago_core/tests/test_proxy_integration.py:187`

**Description:** Test multi-proxy coordination patterns

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_integration import TestMultiProxyCollaboration

instance = TestMultiProxyCollaboration()
```


## Class: `TestProvenanceLogging`

**Location:** `santiago_core/tests/test_proxy_integration.py:220`

**Description:** Test provenance logging across proxies

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_integration import TestProvenanceLogging

instance = TestProvenanceLogging()
```


## Class: `TestCompoundTask`

**Location:** `santiago_core/tests/test_proxy_integration.py:246`

**Description:** Test complete compound task: Backlog grooming + Design session

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_integration import TestCompoundTask

instance = TestCompoundTask()
```


## Class: `TestAllProxies`

**Location:** `santiago_core/tests/test_all_proxies.py:23`

**Description:** Test all 7 proxy agents

**Inheritance:** None

**Public Methods:**
- `workspace` - Create test workspace with role cards
- `test_pm_proxy_instantiation` - Test PM proxy can be created
- `test_architect_proxy_instantiation` - Test Architect proxy can be created
- `test_developer_proxy_instantiation` - Test Developer proxy can be created
- `test_qa_proxy_instantiation` - Test QA proxy can be created
- `test_ux_proxy_instantiation` - Test UX proxy can be created
- `test_platform_proxy_instantiation` - Test Platform proxy can be created
- `test_ethicist_proxy_instantiation` - Test Ethicist proxy can be created
- `test_all_proxies_have_llm_routing` - Test all proxies have LLM router configured
- `test_xai_proxies_route_to_xai` - Test that architect and ethicist route to xAI
- `test_openai_proxies_route_to_openai` - Test that dev/qa/platform proxies route to OpenAI
- `test_all_proxies_have_manifests` - Test all proxies have complete manifests
- `test_all_proxies_disable_budget_by_default` - Test budget tracking is disabled by default

**Usage Example:**
```python
from santiago_core.tests.test_all_proxies import TestAllProxies

instance = TestAllProxies()
```


## Class: `MockProxyAgent`

**Location:** `santiago_core/tests/test_proxy_base.py:28`

**Description:** Mock proxy for testing

**Inheritance:** BaseProxyAgent

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_base import MockProxyAgent

instance = MockProxyAgent()
```


## Class: `TestMCPModels`

**Location:** `santiago_core/tests/test_proxy_base.py:94`

**Description:** Test MCP data models

**Inheritance:** None

**Public Methods:**
- `test_mcp_tool_creation` - Should create MCP tool with name and description
- `test_mcp_manifest_creation` - Should create MCP manifest with tools

**Usage Example:**
```python
from santiago_core.tests.test_proxy_base import TestMCPModels

instance = TestMCPModels()
```


## Class: `TestProxyConfig`

**Location:** `santiago_core/tests/test_proxy_base.py:116`

**Description:** Test proxy configuration

**Inheritance:** None

**Public Methods:**
- `test_config_creation` - Should create proxy config with defaults
- `test_config_validation` - Should validate budget is positive

**Usage Example:**
```python
from santiago_core.tests.test_proxy_base import TestProxyConfig

instance = TestProxyConfig()
```


## Class: `TestBaseProxyAgent`

**Location:** `santiago_core/tests/test_proxy_base.py:136`

**Description:** Test base proxy agent

**Inheritance:** None

**Public Methods:**
- `test_proxy_initialization` - Should initialize proxy with config and manifest
- `test_get_manifest_dict` - Should return manifest as dictionary

**Usage Example:**
```python
from santiago_core.tests.test_proxy_base import TestBaseProxyAgent

instance = TestBaseProxyAgent()
```


## Class: `TestProxyIntegration`

**Location:** `santiago_core/tests/test_proxy_base.py:224`

**Description:** Test proxy integration with Santiago framework

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_proxy_base import TestProxyIntegration

instance = TestProxyIntegration()
```


## Class: `TestProxyObservability`

**Location:** `santiago_core/tests/test_proxy_base.py:263`

**Description:** Test proxy observability and metrics

**Inheritance:** None

**Public Methods:**
- `test_cost_estimation` - Should estimate cost per tool call

**Usage Example:**
```python
from santiago_core.tests.test_proxy_base import TestProxyObservability

instance = TestProxyObservability()
```


## Class: `TestPMProxyInitialization`

**Location:** `santiago_core/tests/test_pm_proxy.py:32`

**Description:** Test PM proxy initialization

**Inheritance:** None

**Public Methods:**
- `test_pm_proxy_creation` - Should initialize with PM-specific manifest
- `test_pm_tools_available` - Should have PM-specific tools
- `test_pm_output_tools` - Should have PM output tools

**Usage Example:**
```python
from santiago_core.tests.test_pm_proxy import TestPMProxyInitialization

instance = TestPMProxyInitialization()
```


## Class: `TestPMHypothesisGeneration`

**Location:** `santiago_core/tests/test_pm_proxy.py:55`

**Description:** Test PM hypothesis generation

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_pm_proxy import TestPMHypothesisGeneration

instance = TestPMHypothesisGeneration()
```


## Class: `TestPMBacklogManagement`

**Location:** `santiago_core/tests/test_pm_proxy.py:103`

**Description:** Test PM backlog operations

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_pm_proxy import TestPMBacklogManagement

instance = TestPMBacklogManagement()
```


## Class: `TestPMTeamCoordination`

**Location:** `santiago_core/tests/test_pm_proxy.py:138`

**Description:** Test PM team coordination

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_pm_proxy import TestPMTeamCoordination

instance = TestPMTeamCoordination()
```


## Class: `TestPMLeanPractices`

**Location:** `santiago_core/tests/test_pm_proxy.py:173`

**Description:** Test PM Lean UX practices

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_pm_proxy import TestPMLeanPractices

instance = TestPMLeanPractices()
```


## Class: `TestLLMRouting`

**Location:** `santiago_core/tests/test_integration_phase0.py:16`

**Description:** Test LLM routing to appropriate providers

**Inheritance:** None

**Public Methods:**
- `test_architect_routes_to_xai` - Architect role should route to xAI (Grok)
- `test_developer_routes_to_openai` - Developer role should route to OpenAI
- `test_ethicist_routes_to_xai` - Ethicist role should route to xAI (Grok)
- `test_complexity_affects_model_selection_openai` - OpenAI model selection should vary by complexity
- `test_task_complexity_detection` - Test automatic complexity detection from tool names
- `test_all_roles_have_routing` - All proxy roles should have routing configured

**Usage Example:**
```python
from santiago_core.tests.test_integration_phase0 import TestLLMRouting

instance = TestLLMRouting()
```


## Class: `TestMessageBus`

**Location:** `santiago_core/tests/test_integration_phase0.py:103`

**Description:** Test Redis message bus for agent communication

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_integration_phase0 import TestMessageBus

instance = TestMessageBus()
```


## Class: `TestProxyIntegration`

**Location:** `santiago_core/tests/test_integration_phase0.py:255`

**Description:** Test integration of proxies with LLM routing and message bus

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_integration_phase0 import TestProxyIntegration

instance = TestProxyIntegration()
```


## Class: `TestKanbanCloseIssue`

**Location:** `santiago_core/tests/test_kanban_service.py:29`

**Description:** Test kanban_close_issue tool functionality

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.tests.test_kanban_service import TestKanbanCloseIssue

instance = TestKanbanCloseIssue()
```


## Class: `TestAPIClients`

**Location:** `santiago_core/tests/test_api_clients.py:18`

**Description:** Test API client implementations

**Inheritance:** None

**Public Methods:**
- `test_api_client_methods_exist` - Verify API client methods exist and are no longer stubs
- `test_build_prompt_method` - Test prompt building from tool definitions

**Usage Example:**
```python
from santiago_core.tests.test_api_clients import TestAPIClients

instance = TestAPIClients()
```


## Class: `SantiagoProductManager`

**Location:** `santiago_core/agents/santiago_pm.py:17`

**Description:** Product Manager agent for the Santiago autonomous development team

**Inheritance:** SantiagoAgent

**Public Methods:**
- `__init__` - No description
- `_analyze_requirements` - Analyze requirements and generate hypotheses
- `_create_bdd_feature` - Create a BDD feature specification

**Usage Example:**
```python
from santiago_core.agents.santiago_pm import SantiagoProductManager

instance = SantiagoProductManager()
```


## Class: `SantiagoDeveloper`

**Location:** `santiago_core/agents/santiago_developer.py:20`

**Description:** Developer agent for implementing features and writing code

**Inheritance:** SantiagoAgent

**Public Methods:**
- `__init__` - No description
- `_parse_bdd_scenarios` - Parse BDD scenarios from feature specification
- `_generate_code_from_scenarios` - Generate Python code from BDD scenarios
- `_step_to_method_name` - Convert a BDD step to a method name
- `_save_implementation` - Save the implementation to a file
- `_analyze_architecture_for_implementation` - Analyze architecture document for implementation concerns
- `_parse_coverage` - Parse coverage percentage from pytest output
- `_generate_failing_test_content` - Generate failing test content for TDD Red phase
- `_generate_minimal_implementation` - Generate minimal implementation to make tests pass
- `_apply_code_quality_improvements` - Apply code quality improvements

**Usage Example:**
```python
from santiago_core.agents.santiago_developer import SantiagoDeveloper

instance = SantiagoDeveloper()
```


## Class: `SantiagoArchitect`

**Location:** `santiago_core/agents/santiago_architect.py:17`

**Description:** Architect agent for defining system architecture and technical approaches

**Inheritance:** SantiagoAgent

**Public Methods:**
- `__init__` - No description
- `_evaluate_technical_feasibility` - Evaluate technical feasibility of a hypothesis
- `_generate_architecture_design` - Generate an architecture design document
- `_review_feature_spec` - Review a feature specification for architectural concerns

**Usage Example:**
```python
from santiago_core.agents.santiago_architect import SantiagoArchitect

instance = SantiagoArchitect()
```


## Class: `SantiagoFactory`

**Location:** `santiago_core/agents/factory.py:12`

**Description:** Factory for creating and managing Santiago agents

**Inheritance:** None

**Public Methods:**
- `__init__` - No description
- `list_available_agents` - List all available agents

**Usage Example:**
```python
from santiago_core.agents.factory import SantiagoFactory

instance = SantiagoFactory()
```


## Class: `MessageBus`

**Location:** `santiago_core/services/message_bus.py:20`

**Description:** Redis-based message bus for Santiago agent communication.

**Inheritance:** None

**Public Methods:**
- `__init__` - Initialize message bus.

**Usage Example:**
```python
from santiago_core.services.message_bus import MessageBus

instance = MessageBus()
```


## Class: `SantiagoKanbanService`

**Location:** `santiago_core/services/kanban_service.py:23`

**Description:** MCP service for Kanban board management in Santiago Factory

**Inheritance:** MCPServer

**Public Methods:**
- `__init__` - No description
- `register_tools` - Register all Kanban-related MCP tools
- `_infer_skills_from_title` - Infer required skills from item title
- `_calculate_dgx_customer_value` - Calculate customer value with DGX readiness bias
- `_assess_dgx_readiness` - Assess how this item contributes to DGX readiness

**Usage Example:**
```python
from santiago_core.services.kanban_service import SantiagoKanbanService

instance = SantiagoKanbanService()
```


## Class: `TaskComplexity`

**Location:** `santiago_core/services/llm_router.py:14`

**Description:** Task complexity levels for model selection

**Inheritance:** Enum

**Public Methods:**


**Usage Example:**
```python
from santiago_core.services.llm_router import TaskComplexity

instance = TaskComplexity()
```


## Class: `LLMProvider`

**Location:** `santiago_core/services/llm_router.py:22`

**Description:** Available LLM providers

**Inheritance:** Enum

**Public Methods:**


**Usage Example:**
```python
from santiago_core.services.llm_router import LLMProvider

instance = LLMProvider()
```


## Class: `LLMConfig`

**Location:** `santiago_core/services/llm_router.py:29`

**Description:** Configuration for LLM API calls

**Inheritance:** None

**Public Methods:**


**Usage Example:**
```python
from santiago_core.services.llm_router import LLMConfig

instance = LLMConfig()
```


## Class: `LLMRouter`

**Location:** `santiago_core/services/llm_router.py:39`

**Description:** Routes LLM requests to appropriate provider and model

**Inheritance:** None

**Public Methods:**
- `__init__` - No description
- `get_config` - Get LLM configuration for a specific role and task.
- `get_task_complexity` - Determine task complexity based on tool name.

**Usage Example:**
```python
from santiago_core.services.llm_router import LLMRouter

instance = LLMRouter()
```


## Class: `SantiagoKnowledgeGraph`

**Location:** `santiago_core/services/knowledge_graph.py:18`

**Description:** RDF-based knowledge graph for Santiago agents

**Inheritance:** None

**Public Methods:**
- `__init__` - No description
- `_bind_namespaces` - Bind RDF namespaces
- `_load_knowledge` - Load existing knowledge from file
- `save_knowledge` - Save knowledge graph to file
- `register_agent` - Register an agent in the knowledge graph
- `get_agent_capabilities` - Get capabilities for an agent
- `record_task` - Record a task in the knowledge graph
- `update_task_status` - Update task status in knowledge graph
- `get_task_history` - Get task history, optionally filtered by agent
- `record_learning` - Record a learning experience
- `get_similar_experiences` - Get similar learning experiences for a concept
- `add_concept_relationship` - Add relationship between concepts
- `get_related_concepts` - Get concepts related to the given concept
- `sparql_query` - Execute a SPARQL query
- `get_statistics` - Get knowledge graph statistics

**Usage Example:**
```python
from santiago_core.services.knowledge_graph import SantiagoKnowledgeGraph

instance = SantiagoKnowledgeGraph()
```


## Class: `DocumentationAutomationService`

**Location:** `santiago_core/services/documentation_service.py:33`

**Description:** Automated documentation service for Santiago Factory

**Inheritance:** MCPServer

**Public Methods:**
- `__init__` - No description
- `_load_templates` - Load documentation templates
- `_load_doc_patterns` - Load regex patterns for documentation extraction
- `register_tools` - Register all documentation automation MCP tools
- `_extract_class_info` - Extract information about a class
- `_extract_function_info` - Extract information about a function
- `_extract_endpoint_info` - Extract information about an API endpoint
- `_generate_api_docs_content` - Generate markdown content for API documentation
- `_generate_audit_report` - Generate documentation audit report
- `_generate_feature_docs_content` - Generate feature documentation content

**Usage Example:**
```python
from santiago_core.services.documentation_service import DocumentationAutomationService

instance = DocumentationAutomationService()
```


## Class: `PlatformProxyAgent`

**Location:** `santiago_core/agents/_proxy/platform_proxy.py:19`

**Description:** Platform proxy for Phase 0 bootstrap

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load Platform role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.platform_proxy import PlatformProxyAgent

instance = PlatformProxyAgent()
```


## Class: `UXProxyAgent`

**Location:** `santiago_core/agents/_proxy/ux_proxy.py:19`

**Description:** UX proxy for Phase 0 bootstrap

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load UX role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.ux_proxy import UXProxyAgent

instance = UXProxyAgent()
```


## Class: `DeveloperProxyAgent`

**Location:** `santiago_core/agents/_proxy/developer_proxy.py:19`

**Description:** Developer proxy for Phase 0 bootstrap

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load Developer role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.developer_proxy import DeveloperProxyAgent

instance = DeveloperProxyAgent()
```


## Class: `ArchitectProxyAgent`

**Location:** `santiago_core/agents/_proxy/architect_proxy.py:19`

**Description:** Architect proxy for Phase 0 bootstrap

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load Architect role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.architect_proxy import ArchitectProxyAgent

instance = ArchitectProxyAgent()
```


## Class: `PMProxyAgent`

**Location:** `santiago_core/agents/_proxy/pm_proxy.py:22`

**Description:** Product Manager proxy for Phase 0 bootstrap

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load PM role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.pm_proxy import PMProxyAgent

instance = PMProxyAgent()
```


## Class: `ArchitectProxyAgent`

**Location:** `santiago_core/agents/_proxy/consolidated_proxies.py:25`

**Description:** Architect proxy for system design and technical decisions

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - No description

**Usage Example:**
```python
from santiago_core.agents._proxy.consolidated_proxies import ArchitectProxyAgent

instance = ArchitectProxyAgent()
```


## Class: `DeveloperProxyAgent`

**Location:** `santiago_core/agents/_proxy/consolidated_proxies.py:85`

**Description:** Developer proxy for TDD/BDD implementation

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - No description

**Usage Example:**
```python
from santiago_core.agents._proxy.consolidated_proxies import DeveloperProxyAgent

instance = DeveloperProxyAgent()
```


## Class: `QAProxyAgent`

**Location:** `santiago_core/agents/_proxy/consolidated_proxies.py:145`

**Description:** QA proxy for testing validation

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - No description

**Usage Example:**
```python
from santiago_core.agents._proxy.consolidated_proxies import QAProxyAgent

instance = QAProxyAgent()
```


## Class: `UXProxyAgent`

**Location:** `santiago_core/agents/_proxy/consolidated_proxies.py:205`

**Description:** UX proxy for user research and design

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - No description

**Usage Example:**
```python
from santiago_core.agents._proxy.consolidated_proxies import UXProxyAgent

instance = UXProxyAgent()
```


## Class: `PlatformProxyAgent`

**Location:** `santiago_core/agents/_proxy/consolidated_proxies.py:265`

**Description:** Platform proxy for infrastructure and deployment

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - No description

**Usage Example:**
```python
from santiago_core.agents._proxy.consolidated_proxies import PlatformProxyAgent

instance = PlatformProxyAgent()
```


## Class: `EthicistProxyAgent`

**Location:** `santiago_core/agents/_proxy/ethicist_proxy.py:19`

**Description:** Ethicist proxy for Phase 0 bootstrap with Baha'i principles

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load Ethicist role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.ethicist_proxy import EthicistProxyAgent

instance = EthicistProxyAgent()
```


## Class: `MCPTool`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:22`

**Description:** MCP tool definition

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.agents._proxy.base_proxy import MCPTool

instance = MCPTool()
```


## Class: `MCPManifest`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:29`

**Description:** MCP service manifest defining proxy capabilities

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.agents._proxy.base_proxy import MCPManifest

instance = MCPManifest()
```


## Class: `ProxyConfig`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:39`

**Description:** Configuration for proxy agent

**Inheritance:** BaseModel

**Public Methods:**


**Usage Example:**
```python
from santiago_core.agents._proxy.base_proxy import ProxyConfig

instance = ProxyConfig()
```


## Class: `ProxyBudgetExceeded`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:51`

**Description:** Raised when proxy budget is exceeded

**Inheritance:** Exception

**Public Methods:**


**Usage Example:**
```python
from santiago_core.agents._proxy.base_proxy import ProxyBudgetExceeded

instance = ProxyBudgetExceeded()
```


## Class: `ProxySessionExpired`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:56`

**Description:** Raised when proxy session has expired

**Inheritance:** Exception

**Public Methods:**


**Usage Example:**
```python
from santiago_core.agents._proxy.base_proxy import ProxySessionExpired

instance = ProxySessionExpired()
```


## Class: `BaseProxyAgent`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:61`

**Description:** Base class for all proxy agents in Phase 0.

**Inheritance:** SantiagoAgent

**Public Methods:**
- `__init__` - No description
- `_build_prompt` - Build prompt for LLM from tool name and parameters.
- `_tool_exists` - Check if tool exists in manifest
- `_is_session_valid` - Check if session is still valid
- `estimate_tool_cost` - Estimate cost for a tool call
- `get_metrics` - Get proxy metrics
- `get_manifest_dict` - Get manifest as dictionary

**Usage Example:**
```python
from santiago_core.agents._proxy.base_proxy import BaseProxyAgent

instance = BaseProxyAgent()
```


## Class: `QAProxyAgent`

**Location:** `santiago_core/agents/_proxy/qa_proxy.py:19`

**Description:** QA proxy for Phase 0 bootstrap

**Inheritance:** BaseProxyAgent

**Public Methods:**
- `__init__` - No description
- `_load_role_instructions` - Load QA role card instructions

**Usage Example:**
```python
from santiago_core.agents._proxy.qa_proxy import QAProxyAgent

instance = QAProxyAgent()
```


## Functions

### Function: `register_tool`

**Location:** `santiago_core/core/mcp_service.py:39`

**Signature:** `register_tool(self, tool)`

**Description:** Register an MCP tool

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `register_tool_handler`

**Location:** `santiago_core/core/mcp_service.py:50`

**Signature:** `register_tool_handler(self, tool_name, handler)`

**Description:** Register a tool handler

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `register_peer`

**Location:** `santiago_core/core/agent_framework.py:142`

**Signature:** `register_peer(self, peer_name, peer)`

**Description:** Register another agent as a communication peer

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `evaluate_action`

**Location:** `santiago_core/core/agent_framework.py:192`

**Signature:** `evaluate_action(action_description)`

**Description:** Evaluate an action against ethical principles

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace`

**Location:** `santiago_core/tests/test_proxy_message_bus.py:20`

**Signature:** `workspace(self, tmp_path)`

**Description:** Create test workspace

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `redis_available`

**Location:** `santiago_core/tests/test_proxy_message_bus.py:36`

**Signature:** `redis_available(self)`

**Description:** Check if Redis is available

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace_path`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:18`

**Signature:** `workspace_path(tmp_path)`

**Description:** Create temporary workspace

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `ethicist_proxy`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:26`

**Signature:** `ethicist_proxy(workspace_path)`

**Description:** Create Ethicist proxy instance

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_ethicist_proxy_creation`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:34`

**Signature:** `test_ethicist_proxy_creation(self, ethicist_proxy)`

**Description:** Should initialize with Ethicist-specific manifest

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_bahai_principles_loaded`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:40`

**Signature:** `test_bahai_principles_loaded(self, ethicist_proxy)`

**Description:** Should load all 12 Baha'i principles

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_ethicist_tools_available`

**Location:** `santiago_core/tests/test_ethicist_proxy.py:47`

**Signature:** `test_ethicist_tools_available(self, ethicist_proxy)`

**Description:** Should have ethical review tools

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace_path`

**Location:** `santiago_core/tests/test_proxy_integration.py:28`

**Signature:** `workspace_path(tmp_path)`

**Description:** Create test workspace with role cards

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `proxy_team`

**Location:** `santiago_core/tests/test_proxy_integration.py:45`

**Signature:** `proxy_team(workspace_path)`

**Description:** Create full proxy team

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_all_proxies_created`

**Location:** `santiago_core/tests/test_proxy_integration.py:61`

**Signature:** `test_all_proxies_created(self, proxy_team)`

**Description:** Should create all 7 proxy agents

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_unique_proxy_names`

**Location:** `santiago_core/tests/test_proxy_integration.py:66`

**Signature:** `test_unique_proxy_names(self, proxy_team)`

**Description:** Should have unique names for each proxy

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_budgets_configured`

**Location:** `santiago_core/tests/test_proxy_integration.py:71`

**Signature:** `test_budgets_configured(self, proxy_team)`

**Description:** Should have configured budgets

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace`

**Location:** `santiago_core/tests/test_all_proxies.py:27`

**Signature:** `workspace(self, tmp_path)`

**Description:** Create test workspace with role cards

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_pm_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:52`

**Signature:** `test_pm_proxy_instantiation(self, workspace)`

**Description:** Test PM proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_architect_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:62`

**Signature:** `test_architect_proxy_instantiation(self, workspace)`

**Description:** Test Architect proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_developer_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:72`

**Signature:** `test_developer_proxy_instantiation(self, workspace)`

**Description:** Test Developer proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_qa_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:82`

**Signature:** `test_qa_proxy_instantiation(self, workspace)`

**Description:** Test QA proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_ux_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:92`

**Signature:** `test_ux_proxy_instantiation(self, workspace)`

**Description:** Test UX proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_platform_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:102`

**Signature:** `test_platform_proxy_instantiation(self, workspace)`

**Description:** Test Platform proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_ethicist_proxy_instantiation`

**Location:** `santiago_core/tests/test_all_proxies.py:112`

**Signature:** `test_ethicist_proxy_instantiation(self, workspace)`

**Description:** Test Ethicist proxy can be created

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_all_proxies_have_llm_routing`

**Location:** `santiago_core/tests/test_all_proxies.py:122`

**Signature:** `test_all_proxies_have_llm_routing(self, workspace)`

**Description:** Test all proxies have LLM router configured

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_xai_proxies_route_to_xai`

**Location:** `santiago_core/tests/test_all_proxies.py:138`

**Signature:** `test_xai_proxies_route_to_xai(self, workspace)`

**Description:** Test that architect and ethicist route to xAI

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_openai_proxies_route_to_openai`

**Location:** `santiago_core/tests/test_all_proxies.py:154`

**Signature:** `test_openai_proxies_route_to_openai(self, workspace)`

**Description:** Test that dev/qa/platform proxies route to OpenAI

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_all_proxies_have_manifests`

**Location:** `santiago_core/tests/test_all_proxies.py:173`

**Signature:** `test_all_proxies_have_manifests(self, workspace)`

**Description:** Test all proxies have complete manifests

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_all_proxies_disable_budget_by_default`

**Location:** `santiago_core/tests/test_all_proxies.py:193`

**Signature:** `test_all_proxies_disable_budget_by_default(self, workspace)`

**Description:** Test budget tracking is disabled by default

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace_path`

**Location:** `santiago_core/tests/test_proxy_base.py:45`

**Signature:** `workspace_path(tmp_path)`

**Description:** Create temporary workspace

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `proxy_config`

**Location:** `santiago_core/tests/test_proxy_base.py:53`

**Signature:** `proxy_config()`

**Description:** Create test proxy configuration

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `mcp_manifest`

**Location:** `santiago_core/tests/test_proxy_base.py:66`

**Signature:** `mcp_manifest()`

**Description:** Create test MCP manifest

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `mock_proxy`

**Location:** `santiago_core/tests/test_proxy_base.py:84`

**Signature:** `mock_proxy(workspace_path, proxy_config, mcp_manifest)`

**Description:** Create mock proxy agent

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_mcp_tool_creation`

**Location:** `santiago_core/tests/test_proxy_base.py:97`

**Signature:** `test_mcp_tool_creation(self)`

**Description:** Should create MCP tool with name and description

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_mcp_manifest_creation`

**Location:** `santiago_core/tests/test_proxy_base.py:108`

**Signature:** `test_mcp_manifest_creation(self, mcp_manifest)`

**Description:** Should create MCP manifest with tools

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_config_creation`

**Location:** `santiago_core/tests/test_proxy_base.py:119`

**Signature:** `test_config_creation(self, proxy_config)`

**Description:** Should create proxy config with defaults

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_config_validation`

**Location:** `santiago_core/tests/test_proxy_base.py:125`

**Signature:** `test_config_validation(self)`

**Description:** Should validate budget is positive

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_proxy_initialization`

**Location:** `santiago_core/tests/test_proxy_base.py:139`

**Signature:** `test_proxy_initialization(self, mock_proxy, proxy_config, mcp_manifest)`

**Description:** Should initialize proxy with config and manifest

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_get_manifest_dict`

**Location:** `santiago_core/tests/test_proxy_base.py:215`

**Signature:** `test_get_manifest_dict(self, mock_proxy)`

**Description:** Should return manifest as dictionary

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_cost_estimation`

**Location:** `santiago_core/tests/test_proxy_base.py:279`

**Signature:** `test_cost_estimation(self, mock_proxy)`

**Description:** Should estimate cost per tool call

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace_path`

**Location:** `santiago_core/tests/test_pm_proxy.py:19`

**Signature:** `workspace_path(tmp_path)`

**Description:** Create temporary workspace

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `pm_proxy`

**Location:** `santiago_core/tests/test_pm_proxy.py:27`

**Signature:** `pm_proxy(workspace_path)`

**Description:** Create PM proxy instance

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_pm_proxy_creation`

**Location:** `santiago_core/tests/test_pm_proxy.py:35`

**Signature:** `test_pm_proxy_creation(self, pm_proxy)`

**Description:** Should initialize with PM-specific manifest

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_pm_tools_available`

**Location:** `santiago_core/tests/test_pm_proxy.py:41`

**Signature:** `test_pm_tools_available(self, pm_proxy)`

**Description:** Should have PM-specific tools

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_pm_output_tools`

**Location:** `santiago_core/tests/test_pm_proxy.py:47`

**Signature:** `test_pm_output_tools(self, pm_proxy)`

**Description:** Should have PM output tools

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_architect_routes_to_xai`

**Location:** `santiago_core/tests/test_integration_phase0.py:19`

**Signature:** `test_architect_routes_to_xai(self)`

**Description:** Architect role should route to xAI (Grok)

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_developer_routes_to_openai`

**Location:** `santiago_core/tests/test_integration_phase0.py:31`

**Signature:** `test_developer_routes_to_openai(self)`

**Description:** Developer role should route to OpenAI

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_ethicist_routes_to_xai`

**Location:** `santiago_core/tests/test_integration_phase0.py:43`

**Signature:** `test_ethicist_routes_to_xai(self)`

**Description:** Ethicist role should route to xAI (Grok)

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_complexity_affects_model_selection_openai`

**Location:** `santiago_core/tests/test_integration_phase0.py:55`

**Signature:** `test_complexity_affects_model_selection_openai(self)`

**Description:** OpenAI model selection should vary by complexity

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_task_complexity_detection`

**Location:** `santiago_core/tests/test_integration_phase0.py:72`

**Signature:** `test_task_complexity_detection(self)`

**Description:** Test automatic complexity detection from tool names

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_all_roles_have_routing`

**Location:** `santiago_core/tests/test_integration_phase0.py:82`

**Signature:** `test_all_roles_have_routing(self)`

**Description:** All proxy roles should have routing configured

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `workspace_path`

**Location:** `santiago_core/tests/test_kanban_service.py:16`

**Signature:** `workspace_path(tmp_path)`

**Description:** Create temporary workspace

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `kanban_service`

**Location:** `santiago_core/tests/test_kanban_service.py:24`

**Signature:** `kanban_service(workspace_path)`

**Description:** Create kanban service instance

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_api_client_methods_exist`

**Location:** `santiago_core/tests/test_api_clients.py:21`

**Signature:** `test_api_client_methods_exist(self)`

**Description:** Verify API client methods exist and are no longer stubs

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `test_build_prompt_method`

**Location:** `santiago_core/tests/test_api_clients.py:201`

**Signature:** `test_build_prompt_method(self)`

**Description:** Test prompt building from tool definitions

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `list_available_agents`

**Location:** `santiago_core/agents/factory.py:37`

**Signature:** `list_available_agents(self)`

**Description:** List all available agents

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_message_bus`

**Location:** `santiago_core/services/message_bus.py:197`

**Signature:** `get_message_bus(redis_url)`

**Description:** Get or create message bus singleton.

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `register_tools`

**Location:** `santiago_core/services/kanban_service.py:40`

**Signature:** `register_tools(self)`

**Description:** Register all Kanban-related MCP tools

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_config`

**Location:** `santiago_core/services/llm_router.py:82`

**Signature:** `get_config(self, role, task_complexity, temperature, max_tokens)`

**Description:** Get LLM configuration for a specific role and task.

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_task_complexity`

**Location:** `santiago_core/services/llm_router.py:130`

**Signature:** `get_task_complexity(self, tool_name)`

**Description:** Determine task complexity based on tool name.

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `save_knowledge`

**Location:** `santiago_core/services/knowledge_graph.py:65`

**Signature:** `save_knowledge(self)`

**Description:** Save knowledge graph to file

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `register_agent`

**Location:** `santiago_core/services/knowledge_graph.py:74`

**Signature:** `register_agent(self, agent_name, agent_type, capabilities)`

**Description:** Register an agent in the knowledge graph

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_agent_capabilities`

**Location:** `santiago_core/services/knowledge_graph.py:89`

**Signature:** `get_agent_capabilities(self, agent_name)`

**Description:** Get capabilities for an agent

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `record_task`

**Location:** `santiago_core/services/knowledge_graph.py:100`

**Signature:** `record_task(self, task_id, title, description, assigned_to)`

**Description:** Record a task in the knowledge graph

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `update_task_status`

**Location:** `santiago_core/services/knowledge_graph.py:117`

**Signature:** `update_task_status(self, task_id, status, completed_by)`

**Description:** Update task status in knowledge graph

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_task_history`

**Location:** `santiago_core/services/knowledge_graph.py:134`

**Signature:** `get_task_history(self, agent_name)`

**Description:** Get task history, optionally filtered by agent

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `record_learning`

**Location:** `santiago_core/services/knowledge_graph.py:177`

**Signature:** `record_learning(self, agent_name, concept, experience, outcome)`

**Description:** Record a learning experience

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_similar_experiences`

**Location:** `santiago_core/services/knowledge_graph.py:193`

**Signature:** `get_similar_experiences(self, concept, limit)`

**Description:** Get similar learning experiences for a concept

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `add_concept_relationship`

**Location:** `santiago_core/services/knowledge_graph.py:222`

**Signature:** `add_concept_relationship(self, concept1, relationship, concept2)`

**Description:** Add relationship between concepts

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_related_concepts`

**Location:** `santiago_core/services/knowledge_graph.py:233`

**Signature:** `get_related_concepts(self, concept, relationship)`

**Description:** Get concepts related to the given concept

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `sparql_query`

**Location:** `santiago_core/services/knowledge_graph.py:258`

**Signature:** `sparql_query(self, query)`

**Description:** Execute a SPARQL query

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_statistics`

**Location:** `santiago_core/services/knowledge_graph.py:267`

**Signature:** `get_statistics(self)`

**Description:** Get knowledge graph statistics

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `register_tools`

**Location:** `santiago_core/services/documentation_service.py:151`

**Signature:** `register_tools(self)`

**Description:** Register all documentation automation MCP tools

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `estimate_tool_cost`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:390`

**Signature:** `estimate_tool_cost(self, tool_name)`

**Description:** Estimate cost for a tool call

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_metrics`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:438`

**Signature:** `get_metrics(self)`

**Description:** Get proxy metrics

**Parameters:**
None

**Returns:** None

**Raises:** None


### Function: `get_manifest_dict`

**Location:** `santiago_core/agents/_proxy/base_proxy.py:456`

**Signature:** `get_manifest_dict(self)`

**Description:** Get manifest as dictionary

**Parameters:**
None

**Returns:** None

**Raises:** None

