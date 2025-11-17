"""
Architect Proxy Agent

Designs and maintains technical architecture for Santiago Factory.
Ensures scalability, maintainability, and alignment with system patterns.
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
    """Architect proxy for Phase 0 bootstrap"""

    def __init__(self, workspace_path: Path):
        # Define Architect-specific manifest
        manifest = MCPManifest(
            role="architect",
            capabilities=[
                "system_design",
                "architecture_decision_records",
                "contract_definition",
                "technical_feasibility",
            ],
            input_tools=[
                MCPTool(
                    name="read_requirements",
                    description="Get feature requirements from PM",
                    parameters={"feature_id": "string"},
                ),
                MCPTool(
                    name="query_architecture",
                    description="Access existing architecture docs",
                    parameters={"topic": "string"},
                ),
                MCPTool(
                    name="check_constraints",
                    description="Review technical and budget limits",
                    parameters={},
                ),
            ],
            output_tools=[
                MCPTool(
                    name="create_design",
                    description="Produce architecture design with diagrams",
                    parameters={"feature": "string", "context": "string"},
                ),
                MCPTool(
                    name="define_contract",
                    description="Specify service interface contract",
                    parameters={"service": "string", "operations": "array"},
                ),
                MCPTool(
                    name="update_adr",
                    description="Record architecture decision with rationale",
                    parameters={"decision": "string", "rationale": "string"},
                ),
                MCPTool(
                    name="assess_feasibility",
                    description="Evaluate technical viability and effort",
                    parameters={"proposal": "string"},
                ),
            ],
            communication_tools=[
                MCPTool(
                    name="message_team",
                    description="Broadcast technical updates",
                    parameters={"content": "string"},
                ),
                MCPTool(
                    name="message_role",
                    description="Direct technical discussions",
                    parameters={"role": "string", "content": "string"},
                ),
            ],
        )

        # Define Architect-specific configuration
        import os
        config = ProxyConfig(
            role_name="architect_proxy",
            api_endpoint="https://api.x.ai/v1",
            api_key="",  # To be loaded from env
            session_ttl_hours=2,  # Longer sessions for complex design
            log_dir="ships-logs/architect/",
            budget_tracking=os.getenv("PROXY_BUDGET_TRACKING", "false").lower() == "true",
        )

        # Load role instructions
        role_card_path = workspace_path / "knowledge" / "proxy-instructions" / "architect.md"
        role_instructions = None
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                role_instructions = f.read()

        super().__init__(
            name="architect-proxy",
            workspace_path=workspace_path,
            config=config,
            manifest=manifest,
            role_instructions=role_instructions,
        )

    def _load_role_instructions(self) -> None:
        """Load Architect role card instructions"""
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "architect.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()
        else:
            self.logger.warning(f"Role card not found: {role_card_path}")
            self.role_instructions = ""

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call external API with architecture context.
        
        TODO: Implement actual xAI API integration.
        """
        # Mock responses for now
        if tool_name == "create_design":
            return {
                "design": {
                    "components": ["Navigator", "Catchfish", "Fishnet"],
                    "contracts": ["MCP interface", "KG schema"],
                    "diagram": "mermaid code here",
                    "rationale": "Design rationale",
                }
            }
        
        elif tool_name == "define_contract":
            return {
                "contract": {
                    "service": params.get("service", ""),
                    "operations": params.get("operations", []),
                    "schema": {"input": {}, "output": {}},
                }
            }
        
        elif tool_name == "update_adr":
            return {
                "adr": {
                    "id": "ADR-001",
                    "title": "Architecture Decision",
                    "status": "accepted",
                    "decision": params.get("decision", ""),
                    "rationale": params.get("rationale", ""),
                }
            }
        
        elif tool_name == "assess_feasibility":
            return {
                "feasibility": {
                    "viable": True,
                    "effort": "medium",
                    "risks": [],
                    "recommendations": [],
                }
            }
        
        else:
            return {"status": "not_implemented", "tool": tool_name}

    async def handle_custom_message(self, message) -> None:
        """Handle Architect-specific messages"""
        self.logger.info(f"Architect proxy received message: {message}")

    async def start_working_on_task(self, task) -> None:
        """Start Architect task"""
        self.logger.info(f"Architect proxy starting task: {task.title}")
