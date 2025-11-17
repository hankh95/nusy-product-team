"""
Developer Proxy Agent

Implements features following TDD/BDD practices.
Transforms designs and scenarios into working, tested code.
"""

from pathlib import Path
from typing import Any, Dict

from santiago_core.agents._proxy.base_proxy import (
    BaseProxyAgent,
    MCPTool,
    MCPManifest,
    ProxyConfig,
)


class DeveloperProxyAgent(BaseProxyAgent):
    """Developer proxy for Phase 0 bootstrap"""

    def __init__(self, workspace_path: Path):
        # Define Developer-specific manifest
        manifest = MCPManifest(
            role="developer",
            capabilities=[
                "feature_implementation",
                "test_driven_development",
                "code_quality",
                "integration",
            ],
            input_tools=[
                MCPTool(
                    name="read_feature",
                    description="Get BDD feature file and acceptance criteria",
                    parameters={"feature_id": "string"},
                ),
                MCPTool(
                    name="read_design",
                    description="Access architecture design and contracts",
                    parameters={"design_id": "string"},
                ),
                MCPTool(
                    name="query_codebase",
                    description="Search existing code patterns",
                    parameters={"query": "string"},
                ),
            ],
            output_tools=[
                MCPTool(
                    name="write_code",
                    description="Implement feature with tests",
                    parameters={"feature": "string", "code": "string", "tests": "string"},
                ),
                MCPTool(
                    name="run_tests",
                    description="Execute test suite and report results",
                    parameters={"test_path": "string"},
                ),
                MCPTool(
                    name="update_docs",
                    description="Maintain code documentation",
                    parameters={"path": "string", "content": "string"},
                ),
                MCPTool(
                    name="refactor_code",
                    description="Improve code structure while preserving behavior",
                    parameters={"target": "string", "approach": "string"},
                ),
            ],
            communication_tools=[
                MCPTool(
                    name="message_team",
                    description="Report implementation status",
                    parameters={"content": "string"},
                ),
                MCPTool(
                    name="message_role",
                    description="Technical discussions",
                    parameters={"role": "string", "content": "string"},
                ),
            ],
        )

        # Define Developer-specific configuration
        import os
        config = ProxyConfig(
            role_name="developer_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",  # To be loaded from env
            session_ttl_hours=1,
            log_dir="ships-logs/developer/",
            budget_tracking=os.getenv("PROXY_BUDGET_TRACKING", "false").lower() == "true",
        )

        # Load role instructions
        role_card_path = workspace_path / "knowledge" / "proxy-instructions" / "developer.md"
        role_instructions = None
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                role_instructions = f.read()

        super().__init__(
            name="developer-proxy",
            workspace_path=workspace_path,
            config=config,
            manifest=manifest,
            role_instructions=role_instructions,
        )

    def _load_role_instructions(self) -> None:
        """Load Developer role card instructions"""
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "developer.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()
        else:
            self.logger.warning(f"Role card not found: {role_card_path}")
            self.role_instructions = ""

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call external API with code context.
        
        TODO: Implement actual OpenAI API integration.
        """
        # Mock responses for now
        if tool_name == "write_code":
            return {
                "implementation": {
                    "code": "# Generated code",
                    "tests": "# Generated tests",
                    "coverage": 95,
                    "files_modified": [],
                }
            }
        
        elif tool_name == "run_tests":
            return {
                "test_results": {
                    "passed": 10,
                    "failed": 0,
                    "skipped": 0,
                    "coverage": 92,
                    "duration": "1.2s",
                }
            }
        
        elif tool_name == "update_docs":
            return {
                "documentation": {
                    "path": params.get("path", ""),
                    "updated": True,
                }
            }
        
        elif tool_name == "refactor_code":
            return {
                "refactoring": {
                    "target": params.get("target", ""),
                    "changes": [],
                    "tests_passing": True,
                }
            }
        
        else:
            return {"status": "not_implemented", "tool": tool_name}

    async def handle_custom_message(self, message) -> None:
        """Handle Developer-specific messages"""
        self.logger.info(f"Developer proxy received message: {message}")

    async def start_working_on_task(self, task) -> None:
        """Start Developer task"""
        self.logger.info(f"Developer proxy starting task: {task.title}")
