"""
Product Manager Proxy Agent

Thin wrapper around external AI that handles:
- Vision translation to hypotheses
- Hypothesis to BDD feature conversion
- Backlog management
- Team coordination
"""

from pathlib import Path
from typing import Any, Dict

from santiago_core.agents._proxy.base_proxy import (
    BaseProxyAgent,
    MCPTool,
    MCPManifest,
    ProxyConfig,
)


class PMProxyAgent(BaseProxyAgent):
    """Product Manager proxy for Phase 0 bootstrap"""

    def __init__(self, workspace_path: Path):
        # Define PM-specific manifest
        manifest = MCPManifest(
            role="product_manager",
            capabilities=[
                "hypothesis_generation",
                "feature_specification",
                "backlog_management",
                "team_coordination",
            ],
            input_tools=[
                MCPTool(
                    name="read_hypothesis",
                    description="Read existing hypothesis from knowledge graph",
                    parameters={"hypothesis_id": "string"},
                ),
                MCPTool(
                    name="query_user_needs",
                    description="Query user research and needs",
                    parameters={"context": "string"},
                ),
                MCPTool(
                    name="query_backlog",
                    description="Query current feature backlog status",
                    parameters={},
                ),
            ],
            output_tools=[
                MCPTool(
                    name="create_hypothesis",
                    description="Create new product hypothesis",
                    parameters={"vision": "string"},
                ),
                MCPTool(
                    name="create_feature",
                    description="Create BDD feature from hypothesis",
                    parameters={"hypothesis": "object"},
                ),
                MCPTool(
                    name="update_backlog",
                    description="Update feature backlog",
                    parameters={"feature_id": "string", "priority": "string"},
                ),
                MCPTool(
                    name="create_story_map",
                    description="Create user story map for feature",
                    parameters={"feature": "string"},
                ),
            ],
            communication_tools=[
                MCPTool(
                    name="message_team",
                    description="Broadcast message to all team members",
                    parameters={"content": "string"},
                ),
                MCPTool(
                    name="message_role",
                    description="Send message to specific role",
                    parameters={"role": "string", "content": "string"},
                ),
            ],
        )

        # Define PM-specific configuration
        import os
        config = ProxyConfig(
            role_name="pm_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",  # To be loaded from env
            session_ttl_hours=1,
            log_dir="ships-logs/pm/",
            budget_tracking=os.getenv("PROXY_BUDGET_TRACKING", "false").lower() == "true",
        )

        super().__init__(
            name="pm-proxy",
            workspace_path=workspace_path,
            config=config,
            manifest=manifest,
        )

        # Load role instructions
        self._load_role_instructions()

    def _load_role_instructions(self) -> None:
        """Load PM role card instructions"""
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "pm.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()
        else:
            self.logger.warning(f"Role card not found: {role_card_path}")
            self.role_instructions = ""

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route tool call to external API.
        
        In production, this would call GPT-4/Claude with role context.
        For now, returns a mock implementation.
        """
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call external API (GPT-4/Claude) with role context.
        
        This is where the actual API integration happens.
        Subclasses can override for testing.
        """
        # TODO: Implement actual API call to GPT-4/Claude/Copilot
        # For now, return structured mock response
        
        if tool_name == "create_hypothesis":
            return {
                "hypothesis": {
                    "title": "Generated Hypothesis",
                    "description": "Hypothesis based on vision",
                    "success_criteria": "Measurable success criteria",
                    "experiments": ["Experiment 1", "Experiment 2"],
                }
            }
        
        elif tool_name == "create_feature":
            return {
                "feature": {
                    "title": "Feature Title",
                    "scenarios": [
                        {
                            "name": "Scenario 1",
                            "given": "Initial context",
                            "when": "Action occurs",
                            "then": "Expected outcome",
                        }
                    ]
                }
            }
        
        elif tool_name == "update_backlog":
            return {
                "status": "success",
                "backlog_updated": True,
            }
        
        elif tool_name == "query_backlog":
            return {
                "backlog": []
            }
        
        elif tool_name == "message_role":
            return {
                "message_sent": True,
                "recipient": f"{params.get('role')}-proxy",
            }
        
        elif tool_name == "message_team":
            return {
                "broadcast": True,
                "recipients": ["architect", "developer", "qa", "ux", "platform", "ethicist"],
            }
        
        elif tool_name == "create_story_map":
            return {
                "story_map": {
                    "backbone": ["Activity 1", "Activity 2"],
                    "stories": [],
                }
            }
        
        else:
            return {"status": "not_implemented", "tool": tool_name}

    async def handle_custom_message(self, message) -> None:
        """Handle PM-specific messages"""
        if message.message_type == "vision_update":
            await self._handle_vision_update(message)
        elif message.message_type == "hypothesis_request":
            await self._handle_hypothesis_request(message)

    async def start_working_on_task(self, task) -> None:
        """Start PM task"""
        self.logger.info(f"PM proxy starting task: {task.title}")
        
        # PM tasks typically involve coordination
        if "hypothesis" in task.title.lower():
            await self.invoke_tool("create_hypothesis", {"vision": task.description})
        elif "feature" in task.title.lower():
            await self.invoke_tool("create_feature", {"hypothesis": {"title": task.title}})

    async def _handle_vision_update(self, message) -> None:
        """Handle vision update message"""
        self.logger.info("Processing vision update")
        # Generate initial hypotheses from vision
        await self.invoke_tool("create_hypothesis", {"vision": message.content})

    async def _handle_hypothesis_request(self, message) -> None:
        """Handle hypothesis request"""
        self.logger.info("Processing hypothesis request")
        await self.invoke_tool("create_hypothesis", {"vision": message.content})
