"""
Santiago Autonomous Development Team Coordinator

Manages the coordination and communication between Santiago agents.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from santiago_core.agents.santiago_pm import SantiagoProductManager
from santiago_core.agents.santiago_architect import SantiagoArchitect
from santiago_core.agents.santiago_developer import SantiagoDeveloper
from santiago_core.core.agent_framework import Message, SantiagoAgent, Task


class SantiagoTeamCoordinator:
    """Coordinates the autonomous development team"""

    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.logger = logging.getLogger("santiago-coordinator")

        # Initialize agents
        self.product_manager = SantiagoProductManager(workspace_path)
        self.architect = SantiagoArchitect(workspace_path)
        self.developer = SantiagoDeveloper(workspace_path)

        # Register peers for communication
        self._register_agent_peers()

        # Team state
        self.active_tasks: Dict[str, Task] = {}
        self.team_status = "initialized"
        self.ethical_oversight_enabled = True

    def _register_agent_peers(self) -> None:
        """Register agents as communication peers with each other"""
        # PM communicates with architect and developer
        self.product_manager.register_peer("santiago-architect", self.architect)
        self.product_manager.register_peer("santiago-developer", self.developer)

        # Architect communicates with PM and developer
        self.architect.register_peer("santiago-pm", self.product_manager)
        self.architect.register_peer("santiago-developer", self.developer)

        # Developer communicates with PM and architect
        self.developer.register_peer("santiago-pm", self.product_manager)
        self.developer.register_peer("santiago-architect", self.architect)

    async def initialize_team(self) -> None:
        """Initialize the autonomous development team"""
        self.logger.info("Initializing Santiago autonomous development team")

        # Start agent processing loops
        agent_tasks = [
            asyncio.create_task(self.product_manager.start()),
            asyncio.create_task(self.architect.start()),
            asyncio.create_task(self.developer.start())
        ]

        # Give agents time to initialize
        await asyncio.sleep(1)

        # Set initial vision for the team
        initial_vision = """
        Build an autonomous AI development system called Santiago that can:
        1. Self-organize into specialized development teams
        2. Autonomously develop, test, and deploy software features
        3. Learn from experience and improve development practices
        4. Maintain ethical standards in all autonomous actions
        5. Scale to handle complex multi-agent development workflows
        """

        vision_message = Message(
            sender="system",
            recipient="santiago-pm",
            content=initial_vision,
            message_type="vision_update"
        )

        await self.product_manager.receive_message(vision_message)

        self.team_status = "active"
        self.logger.info("Santiago team initialized and active")

        # Keep the coordinator running
        await asyncio.gather(*agent_tasks, return_exceptions=True)

    async def assign_task(self, task: Task) -> None:
        """Assign a task to the appropriate agent"""
        self.active_tasks[task.id] = task

        # Determine which agent should handle this task
        target_agent = self._determine_task_agent(task)

        if target_agent:
            # Assign task to the agent
            task_message = Message(
                sender="coordinator",
                recipient=target_agent.name,
                content=json.dumps({
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status
                }),
                message_type="task_assignment"
            )

            await target_agent.receive_message(task_message)
            self.logger.info(f"Assigned task '{task.title}' to {target_agent.name}")
        else:
            self.logger.error(f"No suitable agent found for task: {task.title}")

    def _determine_task_agent(self, task: Task) -> Optional[SantiagoAgent]:
        """Determine which agent should handle a task"""
        from ..core.agent_framework import SantiagoAgent
        """Determine which agent should handle a task"""
        title_lower = task.title.lower()
        description_lower = task.description.lower()

        # Route based on keywords
        if any(keyword in title_lower or keyword in description_lower
               for keyword in ['product', 'vision', 'feature', 'hypothesis', 'backlog']):
            return self.product_manager

        elif any(keyword in title_lower or keyword in description_lower
                 for keyword in ['architecture', 'design', 'system', 'technical', 'infrastructure']):
            return self.architect

        elif any(keyword in title_lower or keyword in description_lower
                 for keyword in ['implement', 'code', 'develop', 'test', 'build']):
            return self.developer

        # Default to product manager for coordination tasks
        return self.product_manager

    async def get_team_status(self) -> Dict:
        """Get the current status of the development team"""
        return {
            "team_status": self.team_status,
            "active_tasks": len(self.active_tasks),
            "agents": {
                "product_manager": {
                    "name": self.product_manager.name,
                    "active_tasks": len([t for t in self.product_manager.tasks.values() if t.status == "in_progress"]),
                    "completed_tasks": len([t for t in self.product_manager.tasks.values() if t.status == "completed"])
                },
                "architect": {
                    "name": self.architect.name,
                    "active_tasks": len([t for t in self.architect.tasks.values() if t.status == "in_progress"]),
                    "completed_tasks": len([t for t in self.architect.tasks.values() if t.status == "completed"])
                },
                "developer": {
                    "name": self.developer.name,
                    "active_tasks": len([t for t in self.developer.tasks.values() if t.status == "in_progress"]),
                    "completed_tasks": len([t for t in self.developer.tasks.values() if t.status == "completed"])
                }
            },
            "ethical_oversight": self.ethical_oversight_enabled
        }

    async def create_demo_task(self) -> None:
        """Create a demonstration task to show the team working together"""
        demo_task = Task(
            id="demo-001",
            title="Implement autonomous task coordination",
            description="""
            Create a system where Santiago agents can autonomously coordinate development tasks.
            This includes task assignment, progress tracking, and inter-agent communication.
            The system should demonstrate ethical oversight and autonomous decision making.
            """
        )

        await self.assign_task(demo_task)

    async def shutdown_team(self) -> None:
        """Gracefully shutdown the development team"""
        self.logger.info("Shutting down Santiago autonomous development team")
        self.team_status = "shutdown"

        # Cancel any active tasks
        for task in self.active_tasks.values():
            if task.status == "in_progress":
                task.status = "cancelled"

        # Note: In a real implementation, we'd need to properly cancel the agent tasks