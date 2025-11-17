"""
Ethicist Proxy Agent

Provides ethical oversight rooted in Baha'i principles of service and consultation.
Guides technical decisions to honor human dignity and collective flourishing.
"""

from pathlib import Path
from typing import Any, Dict, List

from santiago_core.agents._proxy.base_proxy import (
    BaseProxyAgent,
    MCPTool,
    MCPManifest,
    ProxyConfig,
)


class EthicistProxyAgent(BaseProxyAgent):
    """Ethicist proxy for Phase 0 bootstrap with Baha'i principles"""

    # 12 Baha'i Principles (from EthicalOversight in agent_framework.py)
    BAHAI_PRINCIPLES = [
        "Unity of God",
        "Unity of Religion",
        "Unity of Humanity",
        "Equality of Men and Women",
        "Elimination of Prejudice",
        "Universal Education",
        "Harmony of Science and Religion",
        "Independent Investigation of Truth",
        "World Peace",
        "Universal Auxiliary Language",
        "World Federation",
        "Equality of Opportunity"
    ]

    def __init__(self, workspace_path: Path):
        # Define Ethicist-specific manifest
        manifest = MCPManifest(
            role="ethicist",
            capabilities=[
                "ethical_review",
                "consultation_facilitation",
                "service_alignment",
                "principle_application",
            ],
            input_tools=[
                MCPTool(
                    name="read_feature",
                    description="Read feature for ethical review",
                    parameters={"feature_id": "string"},
                ),
                MCPTool(
                    name="read_decision",
                    description="Read technical decision for ethical assessment",
                    parameters={"decision_id": "string"},
                ),
                MCPTool(
                    name="query_principles",
                    description="Query Baha'i principle definitions and applications",
                    parameters={"principle": "string"},
                ),
            ],
            output_tools=[
                MCPTool(
                    name="ethical_review",
                    description="Provide structured ethical assessment",
                    parameters={"subject": "string", "description": "string"},
                ),
                MCPTool(
                    name="consultation_report",
                    description="Document consultation outcomes",
                    parameters={"consultation_id": "string"},
                ),
                MCPTool(
                    name="principle_guidance",
                    description="Offer principle-based recommendations",
                    parameters={"principle": "string", "context": "string"},
                ),
                MCPTool(
                    name="flag_concern",
                    description="Raise ethical red flag for team attention",
                    parameters={"concern": "string", "severity": "string"},
                ),
                MCPTool(
                    name="check_service_alignment",
                    description="Evaluate service to humanity alignment",
                    parameters={"description": "string"},
                ),
                MCPTool(
                    name="apply_decision_framework",
                    description="Apply full ethical decision framework",
                    parameters={"decision": "string", "options": "array"},
                ),
            ],
            communication_tools=[
                MCPTool(
                    name="message_team",
                    description="Share ethical reflection with all",
                    parameters={"content": "string"},
                ),
                MCPTool(
                    name="message_role",
                    description="Consult with specific role on ethics",
                    parameters={"role": "string", "content": "string"},
                ),
                MCPTool(
                    name="convene_consultation",
                    description="Request ethical consultation session",
                    parameters={"topic": "string", "participants": "array"},
                ),
            ],
        )

        # Define Ethicist-specific configuration
        config = ProxyConfig(
            role_name="ethicist_proxy",
            api_endpoint="https://api.openai.com/v1/chat/completions",
            api_key="",  # To be loaded from env
            budget_per_day=20.0,  # Lower than other roles (reflection-focused)
            session_ttl_hours=2,  # Longer sessions for deep reflection
            log_dir="ships-logs/ethics/",
        )

        super().__init__(
            name="ethicist-proxy",
            workspace_path=workspace_path,
            config=config,
            manifest=manifest,
        )

        # Store Baha'i principles for access
        self.bahai_principles = self.BAHAI_PRINCIPLES

        # Load role instructions
        self._load_role_instructions()

    def _load_role_instructions(self) -> None:
        """Load Ethicist role card instructions"""
        role_card_path = self.workspace_path / "knowledge" / "proxy-instructions" / "ethicist.md"
        if role_card_path.exists():
            with open(role_card_path, 'r') as f:
                self.role_instructions = f.read()
        else:
            self.logger.warning(f"Role card not found: {role_card_path}")
            self.role_instructions = ""

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route tool call to external API with Baha'i principles context.
        """
        return await self._call_external_api(tool_name, params)

    async def _call_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call external API with ethical reasoning context.
        
        In production, this would include full Baha'i principles context
        and consultation method guidance.
        """
        # TODO: Implement actual API call with ethical framework
        
        if tool_name == "ethical_review":
            return await self._mock_ethical_review(params)
        
        elif tool_name == "consultation_report":
            return {
                "report": {
                    "topic": "Consultation topic",
                    "participants": [],
                    "synthesis": "Consensus reached",
                    "decisions": [],
                    "dissent": None,
                }
            }
        
        elif tool_name == "principle_guidance":
            return {
                "guidance": {
                    "principle": params.get("principle", ""),
                    "application": "Application guidance",
                    "concrete_actions": [],
                }
            }
        
        elif tool_name == "flag_concern":
            return {
                "flag": {
                    "severity": params.get("severity", "medium"),
                    "concern": params.get("concern", ""),
                    "principle_violated": "Principle name",
                    "action_required": "Review required",
                }
            }
        
        elif tool_name == "check_service_alignment":
            return {
                "service_alignment": {
                    "serves_genuine_need": True,
                    "benefits": "Service benefits",
                    "potential_harms": "Potential harms",
                    "recommendation": "Recommendation",
                }
            }
        
        elif tool_name == "apply_decision_framework":
            return {
                "decision": {
                    "stakes": "Stakes analysis",
                    "principles_applied": [],
                    "consultation_needed": False,
                    "options_evaluated": len(params.get("options", [])),
                    "recommendation": "Recommendation",
                    "reasoning": "Ethical reasoning",
                }
            }
        
        elif tool_name == "convene_consultation":
            return {
                "consultation": {
                    "topic": params.get("topic", ""),
                    "participants": params.get("participants", []),
                    "status": "scheduled",
                }
            }
        
        else:
            return {"status": "not_implemented", "tool": tool_name}

    async def _mock_ethical_review(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Mock ethical review (placeholder for actual implementation)"""
        description = params.get("description", "").lower()
        
        # Simple heuristic for demonstration
        approved = True
        concerns = []
        principles_applied = ["Unity of Humanity", "Universal Education"]
        
        # Check for potential issues
        if any(word in description for word in ["exclude", "restrict", "deny"]):
            approved = False
            concerns.append("Potential exclusion of user groups")
            principles_applied.append("Equality of Opportunity")
        
        if any(word in description for word in ["bias", "discriminate", "gender"]):
            concerns.append("Potential bias or discrimination")
            principles_applied.append("Equality of Men and Women")
            principles_applied.append("Elimination of Prejudice")
        
        if any(word in description for word in ["manipulate", "deceive", "trick"]):
            approved = False
            concerns.append("Potential manipulation of users")
            principles_applied.append("Independent Investigation of Truth")
        
        return {
            "review": {
                "approved": approved,
                "principles_applied": list(set(principles_applied)),
                "concerns": concerns,
                "recommendations": "Proceed with caution" if concerns else "Approved for implementation",
            }
        }

    async def check_principle_alignment(
        self,
        principle: str,
        description: str,
    ) -> Dict[str, Any]:
        """
        Check if a description aligns with a specific Baha'i principle.
        
        This is a helper method for testing principle application.
        """
        description_lower = description.lower()
        aligned = True
        guidance = ""
        
        if principle == "Unity of Humanity":
            if any(word in description_lower for word in ["exclude", "certain countries", "restrict access"]):
                aligned = False
                guidance = "Ensure global accessibility and inclusive design"
        
        elif principle == "Equality of Men and Women":
            if "equal access" in description_lower or "all users" in description_lower:
                aligned = True
                guidance = "Feature promotes equality"
            else:
                # Neutral - need more context
                aligned = True
                guidance = "Verify gender equity in implementation"
        
        elif principle == "Universal Compulsory Education":
            if any(word in description_lower for word in ["no documentation", "high learning curve", "complex"]):
                aligned = False
                guidance = "Add educational resources and lower barriers to learning"
            else:
                aligned = True
                guidance = "Ensure learnability and documentation"
        
        elif principle == "Elimination of Prejudice":
            if "bias" in description_lower:
                aligned = False
                guidance = "Implement bias testing and diverse validation"
        
        elif principle == "Independent Investigation of Truth":
            if any(word in description_lower for word in ["manipulate", "hide", "obscure"]):
                aligned = False
                guidance = "Provide transparency and user autonomy"
        
        return {
            "aligned": aligned,
            "principle": principle,
            "guidance": guidance,
        }

    async def handle_custom_message(self, message) -> None:
        """Handle Ethicist-specific messages"""
        if message.message_type == "ethical_review_request":
            await self._handle_review_request(message)
        elif message.message_type == "consultation_request":
            await self._handle_consultation_request(message)

    async def start_working_on_task(self, task) -> None:
        """Start Ethicist task"""
        self.logger.info(f"Ethicist proxy starting task: {task.title}")
        
        # Ethicist tasks typically involve review
        if "review" in task.title.lower():
            await self.invoke_tool("ethical_review", {
                "subject": "task",
                "description": task.description
            })
        elif "consultation" in task.title.lower():
            await self.invoke_tool("convene_consultation", {
                "topic": task.title,
                "participants": ["pm", "architect", "developer"]
            })

    async def _handle_review_request(self, message) -> None:
        """Handle ethical review request"""
        self.logger.info("Processing ethical review request")
        content = message.content
        await self.invoke_tool("ethical_review", {
            "subject": "request",
            "description": content
        })

    async def _handle_consultation_request(self, message) -> None:
        """Handle consultation request"""
        self.logger.info("Processing consultation request")
        await self.invoke_tool("convene_consultation", {
            "topic": message.content,
            "participants": []
        })
