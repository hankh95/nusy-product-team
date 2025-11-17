"""
UX Researcher/Designer Proxy Agent

Keeps Santiago Factory human-centered through user research and journey mapping.
Validates feature hypotheses with real user needs.
"""

from pathlib import Path
from typing import Any, Dict

from santiago_core.agents._proxy.base_proxy import (
    BaseProxyAgent,
    MCPTool,
    MCPManifest,
    ProxyConfig,
)


class UXProxyAgent(BaseProxyAgent):
    """UX proxy for Phase 0 bootstrap"""

    def __init__(self, workspace_path: Path):
        # Define UX-specific manifest
        manifest = MCPManifest(
            role="ux",
            capabilities=[
                "user_research",
                "journey_mapping",
                "usability_testing",
                "design_guidance",
            ],
            input_tools=[
                MCPTool(
                    name="read_hypothesis",
                    description="Get product hypothesis to validate",
                    parameters={"hypothesis_id": "string"},
                ),
                MCPTool(
                    name="query_personas",
                    description="Access existing persona library",
                    parameters={"criteria": "string"},
                ),
                MCPTool(
                    name="read_feature",
                    description="Understand feature context",
                    parameters={"feature_id": "string"},
                ),
            ],
            output_tools=[
                MCPTool(
                    name="create_persona",
                    description="Document user archetype",
                    parameters={"name": "string", "goals": "array", "pains": "array"},
                ),
                MCPTool(
                    name="map_journey",
                    description="Create user journey visualization",
                    parameters={"persona": "string", "scenario": "string"},
                ),
                MCPTool(
                    name="report_findings",
                    description="Document research results",
                    parameters={"study": "string", "insights": "array"},
                ),
                MCPTool(
                    name="create_wireframe",
                    description="Design interface mockup",
                    parameters={"feature": "string", "fidelity": "string"},
                ),
                MCPTool(
                    name="test_usability",
                    description="Conduct usability testing",
                    parameters={"prototype": "string", "participants": "number"},
                ),
            ],
            communication_tools=[
                MCPTool(
                    name="message_team",
                    description="Share research insights",
                    parameters={"content": "string"},
                ),
                MCPTool(
                    name="message_role",
                    description="Coordinate with PM on validation",
                    parameters={"role": "string", "content": "string"},
                ),
            ],
        )

        # Define UX-specific configuration
        import os
        config = ProxyConfig(
            role_name="ux_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",  # To be loaded from env
            session_ttl_hours=2,  # Longer for research work
            log_dir="ships-logs/ux/",
            budget_tracking=os.getenv("PROXY_BUDGET_TRACKING", "false").lower() == "true",
        )

        super().__init__(
            name="ux-proxy",
            workspace_path=workspace_path,
            config=config,
            manifest=manifest,
        )

        # Load role instructions
        self._load_role_instructions()

    def _load_role_instructions(self) -> None:
        """Load UX role card instructions"""
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "ux.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()
        else:
            self.logger.warning(f"Role card not found: {role_card_path}")
            self.role_instructions = ""

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call external API with UX research context.
        
        TODO: Implement actual OpenAI API integration.
        """
        # Mock responses for now
        if tool_name == "create_persona":
            return {
                "persona": {
                    "name": params.get("name", ""),
                    "goals": params.get("goals", []),
                    "pains": params.get("pains", []),
                    "context": "User context",
                    "behaviors": [],
                }
            }
        
        elif tool_name == "map_journey":
            return {
                "journey": {
                    "persona": params.get("persona", ""),
                    "scenario": params.get("scenario", ""),
                    "stages": ["Awareness", "Consideration", "Decision", "Use"],
                    "touchpoints": [],
                    "pain_points": [],
                }
            }
        
        elif tool_name == "report_findings":
            return {
                "research": {
                    "study": params.get("study", ""),
                    "insights": params.get("insights", []),
                    "recommendations": [],
                    "confidence": "high",
                }
            }
        
        elif tool_name == "create_wireframe":
            return {
                "wireframe": {
                    "feature": params.get("feature", ""),
                    "fidelity": params.get("fidelity", "low"),
                    "screens": [],
                    "interactions": [],
                }
            }
        
        elif tool_name == "test_usability":
            return {
                "usability": {
                    "prototype": params.get("prototype", ""),
                    "participants": params.get("participants", 5),
                    "success_rate": 0.8,
                    "issues": [],
                    "recommendations": [],
                }
            }
        
        else:
            return {"status": "not_implemented", "tool": tool_name}

    async def handle_custom_message(self, message) -> None:
        """Handle UX-specific messages"""
        self.logger.info(f"UX proxy received message: {message}")

    async def start_working_on_task(self, task) -> None:
        """Start UX task"""
        self.logger.info(f"UX proxy starting task: {task.title}")
