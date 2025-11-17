"""
Consolidated Proxy Implementations

This module provides all remaining proxy agents for Phase 0 bootstrap:
- Architect Proxy
- Developer Proxy  
- QA Proxy
- UX Proxy
- Platform Proxy

Each follows the established BaseProxyAgent pattern.
"""

from pathlib import Path
from typing import Any, Dict

from santiago_core.agents._proxy.base_proxy import (
    BaseProxyAgent,
    MCPTool,
    MCPManifest,
    ProxyConfig,
)


class ArchitectProxyAgent(BaseProxyAgent):
    """Architect proxy for system design and technical decisions"""

    def __init__(self, workspace_path: Path):
        manifest = MCPManifest(
            role="architect",
            capabilities=["system_design", "architecture_decisions", "technology_evaluation"],
            input_tools=[
                MCPTool(name="read_requirements", description="Read feature requirements", parameters={"feature_id": "string"}),
                MCPTool(name="query_patterns", description="Query architecture patterns", parameters={"pattern": "string"}),
            ],
            output_tools=[
                MCPTool(name="create_design", description="Create system design", parameters={"feature": "string"}),
                MCPTool(name="create_adr", description="Create architecture decision record", parameters={"decision": "string"}),
                MCPTool(name="evaluate_technology", description="Evaluate technology options", parameters={"options": "array"}),
            ],
            communication_tools=[
                MCPTool(name="message_team", description="Broadcast design", parameters={"content": "string"}),
                MCPTool(name="message_role", description="Consult with role", parameters={"role": "string", "content": "string"}),
            ],
        )
        
        config = ProxyConfig(
            role_name="architect_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",
            budget_per_day=30.0,  # Higher budget for complex design work
            session_ttl_hours=2,
            log_dir="ships-logs/architect/",
        )
        
        super().__init__(name="architect-proxy", workspace_path=workspace_path, config=config, manifest=manifest)
        self._load_role_instructions()

    def _load_role_instructions(self):
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "architect.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "create_design":
            return {"design": {"components": [], "patterns": [], "rationale": "Design rationale"}}
        elif tool_name == "create_adr":
            return {"adr": {"decision": params.get("decision"), "status": "proposed", "consequences": []}}
        elif tool_name == "evaluate_technology":
            return {"evaluation": {"options": params.get("options", []), "recommendation": "Option 1"}}
        else:
            return {"status": "not_implemented"}

    async def handle_custom_message(self, message):
        pass

    async def start_working_on_task(self, task):
        self.logger.info(f"Architect starting: {task.title}")


class DeveloperProxyAgent(BaseProxyAgent):
    """Developer proxy for TDD/BDD implementation"""

    def __init__(self, workspace_path: Path):
        manifest = MCPManifest(
            role="developer",
            capabilities=["tdd_implementation", "code_generation", "test_execution"],
            input_tools=[
                MCPTool(name="read_feature", description="Read BDD feature", parameters={"feature_file": "string"}),
                MCPTool(name="read_design", description="Read architecture design", parameters={"design_id": "string"}),
            ],
            output_tools=[
                MCPTool(name="write_test", description="Write test code", parameters={"test_file": "string", "code": "string"}),
                MCPTool(name="write_code", description="Write implementation", parameters={"file": "string", "code": "string"}),
                MCPTool(name="run_tests", description="Execute test suite", parameters={}),
            ],
            communication_tools=[
                MCPTool(name="message_team", description="Update team", parameters={"content": "string"}),
                MCPTool(name="message_role", description="Ask question", parameters={"role": "string", "content": "string"}),
            ],
        )
        
        config = ProxyConfig(
            role_name="developer_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",
            budget_per_day=35.0,
            session_ttl_hours=4,  # Longer sessions for implementation
            log_dir="ships-logs/developer/",
        )
        
        super().__init__(name="developer-proxy", workspace_path=workspace_path, config=config, manifest=manifest)
        self._load_role_instructions()

    def _load_role_instructions(self):
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "developer.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "write_test":
            return {"test_written": True, "file": params.get("test_file")}
        elif tool_name == "write_code":
            return {"code_written": True, "file": params.get("file")}
        elif tool_name == "run_tests":
            return {"tests_passed": True, "failures": 0}
        else:
            return {"status": "not_implemented"}

    async def handle_custom_message(self, message):
        pass

    async def start_working_on_task(self, task):
        self.logger.info(f"Developer starting: {task.title}")


class QAProxyAgent(BaseProxyAgent):
    """QA proxy for testing validation"""

    def __init__(self, workspace_path: Path):
        manifest = MCPManifest(
            role="qa",
            capabilities=["test_execution", "bug_tracking", "contract_validation"],
            input_tools=[
                MCPTool(name="read_feature", description="Get BDD scenarios", parameters={"feature_file": "string"}),
                MCPTool(name="query_bugs", description="Access bug database", parameters={}),
            ],
            output_tools=[
                MCPTool(name="run_tests", description="Execute test suite", parameters={"test_files": "array"}),
                MCPTool(name="file_bug", description="Document defect", parameters={"title": "string", "description": "string"}),
                MCPTool(name="report_coverage", description="Report coverage", parameters={"coverage": "number"}),
            ],
            communication_tools=[
                MCPTool(name="message_team", description="Broadcast status", parameters={"content": "string"}),
                MCPTool(name="message_role", description="Report bug", parameters={"role": "string", "content": "string"}),
            ],
        )
        
        config = ProxyConfig(
            role_name="qa_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",
            budget_per_day=25.0,
            session_ttl_hours=2,
            log_dir="ships-logs/qa/",
        )
        
        super().__init__(name="qa-proxy", workspace_path=workspace_path, config=config, manifest=manifest)
        self._load_role_instructions()

    def _load_role_instructions(self):
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "qa.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "run_tests":
            return {"passed": True, "total": 10, "failures": 0}
        elif tool_name == "file_bug":
            return {"bug_id": "BUG001", "status": "filed"}
        elif tool_name == "report_coverage":
            return {"coverage": params.get("coverage", 90)}
        else:
            return {"status": "not_implemented"}

    async def handle_custom_message(self, message):
        pass

    async def start_working_on_task(self, task):
        self.logger.info(f"QA starting: {task.title}")


class UXProxyAgent(BaseProxyAgent):
    """UX proxy for user research and design"""

    def __init__(self, workspace_path: Path):
        manifest = MCPManifest(
            role="ux",
            capabilities=["user_research", "journey_mapping", "usability_testing"],
            input_tools=[
                MCPTool(name="read_hypothesis", description="Get hypothesis", parameters={"hypothesis_id": "string"}),
                MCPTool(name="query_personas", description="Access personas", parameters={}),
            ],
            output_tools=[
                MCPTool(name="create_persona", description="Document user archetype", parameters={"persona": "object"}),
                MCPTool(name="map_journey", description="Create journey map", parameters={"journey": "object"}),
                MCPTool(name="report_findings", description="Document research", parameters={"findings": "string"}),
            ],
            communication_tools=[
                MCPTool(name="message_team", description="Share insights", parameters={"content": "string"}),
                MCPTool(name="message_role", description="Coordinate", parameters={"role": "string", "content": "string"}),
            ],
        )
        
        config = ProxyConfig(
            role_name="ux_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",
            budget_per_day=25.0,
            session_ttl_hours=2,
            log_dir="ships-logs/ux/",
        )
        
        super().__init__(name="ux-proxy", workspace_path=workspace_path, config=config, manifest=manifest)
        self._load_role_instructions()

    def _load_role_instructions(self):
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "ux.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "create_persona":
            return {"persona": params.get("persona", {}), "status": "created"}
        elif tool_name == "map_journey":
            return {"journey": params.get("journey", {}), "status": "mapped"}
        elif tool_name == "report_findings":
            return {"findings": params.get("findings", ""), "status": "reported"}
        else:
            return {"status": "not_implemented"}

    async def handle_custom_message(self, message):
        pass

    async def start_working_on_task(self, task):
        self.logger.info(f"UX starting: {task.title}")


class PlatformProxyAgent(BaseProxyAgent):
    """Platform proxy for infrastructure and deployment"""

    def __init__(self, workspace_path: Path):
        manifest = MCPManifest(
            role="platform",
            capabilities=["infrastructure_management", "deployment", "observability"],
            input_tools=[
                MCPTool(name="read_architecture", description="Get infra requirements", parameters={}),
                MCPTool(name="query_metrics", description="Access metrics", parameters={}),
            ],
            output_tools=[
                MCPTool(name="provision_resource", description="Create infrastructure", parameters={"resource": "object"}),
                MCPTool(name="deploy_service", description="Execute deployment", parameters={"service": "string"}),
                MCPTool(name="configure_monitoring", description="Set up observability", parameters={"config": "object"}),
            ],
            communication_tools=[
                MCPTool(name="message_team", description="Broadcast deployment", parameters={"content": "string"}),
                MCPTool(name="message_role", description="Notify issues", parameters={"role": "string", "content": "string"}),
            ],
        )
        
        config = ProxyConfig(
            role_name="platform_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",
            budget_per_day=30.0,
            session_ttl_hours=2,
            log_dir="ships-logs/platform/",
        )
        
        super().__init__(name="platform-proxy", workspace_path=workspace_path, config=config, manifest=manifest)
        self._load_role_instructions()

    def _load_role_instructions(self):
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "platform.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "provision_resource":
            return {"resource_id": "RES001", "status": "provisioned"}
        elif tool_name == "deploy_service":
            return {"deployment_id": "DEP001", "status": "deployed"}
        elif tool_name == "configure_monitoring":
            return {"monitoring": "configured", "status": "active"}
        else:
            return {"status": "not_implemented"}

    async def handle_custom_message(self, message):
        pass

    async def start_working_on_task(self, task):
        self.logger.info(f"Platform starting: {task.title}")
