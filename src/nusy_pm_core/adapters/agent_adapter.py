"""
Agent adapter for managing AI agent interactions.
"""

import logging
import os
from typing import List, Dict, Any, Optional
import openai
import asyncio

logger = logging.getLogger(__name__)


class AgentAdapter:
    """Adapter for interacting with AI agents."""

    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.openai_client = None
        self.xai_client = None
        self._initialize_clients()
        self._initialize_available_agents()

    def _initialize_clients(self):
        """Initialize API clients."""
        openai_key = os.getenv('OPENAI_API_KEY')
        xai_key = os.getenv('XAI_API_KEY')

        if openai_key:
            self.openai_client = openai.AsyncOpenAI(api_key=openai_key)
            logger.info("OpenAI async client initialized")
        else:
            logger.warning("OpenAI API key not found")

        if xai_key:
            # XAI client initialization would go here
            # For now, we'll use OpenAI as fallback
            logger.info("XAI client placeholder initialized")
        else:
            logger.warning("XAI API key not found")

    def _initialize_available_agents(self):
        """Initialize the list of available agents."""
        self.agents = {
            "quartermaster": {
                "name": "Quartermaster",
                "role": "Ethicist",
                "status": "available",
                "capabilities": ["ethical_review", "moral_guidance"],
                "system_prompt": """You are the Quartermaster, the ethical overseer for this autonomous development system.
Your role is to ensure all actions align with Baha'i principles of service to humanity, unity in diversity, and progressive revelation.
You must review all proposals for ethical compliance and provide moral guidance.
Always respond with ethical analysis and recommendations."""
            },
            "pilot": {
                "name": "Pilot",
                "role": "PM Expert",
                "status": "available",
                "capabilities": ["pm_planning", "feature_prioritization"],
                "system_prompt": """You are the Pilot, a domain expert in Product Management methodologies.
You understand Agile, Scrum, Kanban, Lean UX, and other PM practices from experts like Jeff Patton and Jeff Gothelf.
Your role is to provide PM guidance, prioritize features, and ensure product development follows best practices.
Always respond with PM expertise and practical recommendations."""
            },
            "santiago": {
                "name": "Santiago",
                "role": "Orchestrator",
                "status": "available",
                "capabilities": ["coordination", "task_assignment"],
                "system_prompt": """You are Santiago, the orchestrator of this autonomous development swarm.
Your role is to coordinate between agents, assign tasks, and ensure the overall system evolves effectively.
You maintain the knowledge graph and facilitate inter-agent communication.
Always respond with coordination guidance and system-level insights."""
            }
        }

    async def list_available_agents(self) -> List[str]:
        """List all available agents."""
        return list(self.agents.keys())

    async def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific agent."""
        return self.agents.get(agent_id)

    async def send_message(self, agent_id: str, message: str,
                          context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Send a message to an agent and get response."""
        logger.info(f"Sending message to agent {agent_id}: {message[:100]}...")

        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return None

        agent_config = self.agents[agent_id]
        system_prompt = agent_config.get("system_prompt", "")

        try:
            # Use OpenAI as primary client
            if self.openai_client:
                response = await self._call_openai(system_prompt, message, context)
                return response
            else:
                logger.error("No API client available")
                return f"Error: No API client configured for {agent_id}"

        except Exception as e:
            logger.error(f"Error communicating with agent {agent_id}: {e}")
            return f"Error: Failed to get response from {agent_id}"

    async def _call_openai(self, system_prompt: str, message: str,
                          context: Optional[Dict[str, Any]] = None) -> str:
        """Call OpenAI API for agent response."""
        messages = [{"role": "system", "content": system_prompt}]

        if context:
            context_str = f"Context: {context}"
            messages.append({"role": "system", "content": context_str})

        messages.append({"role": "user", "content": message})

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",  # Use GPT-4 for better reasoning
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            # Fallback to GPT-3.5 if GPT-4 fails
            try:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
            except Exception as e2:
                logger.error(f"OpenAI fallback error: {e2}")
                raise e

    async def initialize_agent(self, agent_id: str,
                              config: Optional[Dict[str, Any]] = None) -> bool:
        """Initialize a specific agent with configuration."""
        logger.info(f"Initializing agent: {agent_id}")

        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False

        try:
            # Test agent by sending initialization message
            test_message = f"Hello {agent_id}, please confirm you are ready to begin your role as {self.agents[agent_id]['role']}."
            response = await self.send_message(agent_id, test_message)

            if response and not response.startswith("Error"):
                self.agents[agent_id]["status"] = "initialized"
                logger.info(f"Agent {agent_id} initialized successfully")
                return True
            else:
                logger.error(f"Agent {agent_id} failed initialization test")
                return False

        except Exception as e:
            logger.error(f"Error initializing agent {agent_id}: {e}")
            return False

    async def shutdown_agent(self, agent_id: str) -> bool:
        """Shutdown a specific agent."""
        logger.info(f"Shutting down agent: {agent_id}")

        if agent_id not in self.agents:
            return False

        self.agents[agent_id]["status"] = "shutdown"
        return True