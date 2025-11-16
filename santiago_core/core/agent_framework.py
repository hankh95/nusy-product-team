"""
Santiago Core Agent Framework

This module provides the foundation for autonomous AI agents in the Santiago ecosystem.
Agents are designed to work collaboratively on software development tasks with ethical oversight.
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

from pydantic import BaseModel, Field


class Message(BaseModel):
    """Represents a message between agents"""
    sender: str
    recipient: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    message_type: str = "communication"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Task(BaseModel):
    """Represents a development task"""
    id: str
    title: str
    description: str
    status: str = "pending"  # pending, in_progress, completed, blocked
    assigned_to: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    dependencies: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentProtocol(Protocol):
    """Protocol for agent communication"""
    name: str

    async def receive_message(self, message: Message) -> None:
        """Receive a message from another agent"""
        ...

    async def send_message(self, recipient: str, content: str, message_type: str = "communication") -> None:
        """Send a message to another agent"""
        ...


class SantiagoAgent(ABC):
    """Base class for all Santiago autonomous agents"""

    def __init__(self, name: str, workspace_path: Path):
        self.name = name
        self.workspace_path = workspace_path
        self.logger = logging.getLogger(f"santiago.{name}")
        self.message_queue: asyncio.Queue[Message] = asyncio.Queue()
        self.tasks: Dict[str, Task] = {}
        self.active_task: Optional[Task] = None
        self.communication_peers: Dict[str, AgentProtocol] = {}

    async def start(self) -> None:
        """Start the agent's main processing loop"""
        self.logger.info(f"Starting Santiago agent: {self.name}")
        while True:
            try:
                message = await self.message_queue.get()
                await self.process_message(message)
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")

    async def receive_message(self, message: Message) -> None:
        """Receive a message and add it to the processing queue"""
        await self.message_queue.put(message)

    async def send_message(self, recipient: str, content: str, message_type: str = "communication") -> None:
        """Send a message to another agent"""
        if recipient in self.communication_peers:
            message = Message(
                sender=self.name,
                recipient=recipient,
                content=content,
                message_type=message_type
            )
            await self.communication_peers[recipient].receive_message(message)
        else:
            self.logger.warning(f"No peer found for recipient: {recipient}")

    async def process_message(self, message: Message) -> None:
        """Process an incoming message"""
        self.logger.info(f"Processing message from {message.sender}: {message.content[:100]}...")

        # Handle different message types
        if message.message_type == "task_assignment":
            await self.handle_task_assignment(message)
        elif message.message_type == "task_update":
            await self.handle_task_update(message)
        elif message.message_type == "communication":
            await self.handle_communication(message)
        else:
            await self.handle_custom_message(message)

    async def handle_task_assignment(self, message: Message) -> None:
        """Handle task assignment messages"""
        try:
            task_data = json.loads(message.content)
            task = Task(**task_data)
            self.tasks[task.id] = task
            if not self.active_task:
                self.active_task = task
                task.status = "in_progress"
                task.assigned_to = self.name
                await self.start_working_on_task(task)
        except Exception as e:
            self.logger.error(f"Error handling task assignment: {e}")

    async def handle_task_update(self, message: Message) -> None:
        """Handle task update messages"""
        # Implementation for task updates
        pass

    async def handle_communication(self, message: Message) -> None:
        """Handle general communication messages"""
        # Implementation for general communication
        pass

    @abstractmethod
    async def handle_custom_message(self, message: Message) -> None:
        """Handle custom message types specific to this agent"""
        pass

    @abstractmethod
    async def start_working_on_task(self, task: Task) -> None:
        """Start working on an assigned task"""
        pass

    def register_peer(self, peer_name: str, peer: AgentProtocol) -> None:
        """Register another agent as a communication peer"""
        self.communication_peers[peer_name] = peer

    async def update_task_status(self, task_id: str, status: str, **kwargs) -> None:
        """Update the status of a task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            task.status = status
            task.updated_at = datetime.now()
            for key, value in kwargs.items():
                setattr(task, key, value)

            # Notify other agents of task update
            update_message = {
                "task_id": task_id,
                "status": status,
                "updated_by": self.name,
                **kwargs
            }
            await self.broadcast_message(
                json.dumps(update_message),
                "task_update"
            )

    async def broadcast_message(self, content: str, message_type: str = "communication") -> None:
        """Broadcast a message to all peers"""
        for peer_name in self.communication_peers:
            await self.send_message(peer_name, content, message_type)


class EthicalOversight:
    """Provides ethical oversight for all agent actions"""

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

    @staticmethod
    def evaluate_action(action_description: str) -> Dict[str, Any]:
        """Evaluate an action against ethical principles"""
        # Simplified ethical evaluation - in practice this would be more sophisticated
        concerns = []

        # Check for potential harm
        harmful_keywords = ["harm", "damage", "exploit", "manipulate", "deceive"]
        if any(keyword in action_description.lower() for keyword in harmful_keywords):
            concerns.append("Potential for harm or manipulation")

        # Check for bias
        bias_keywords = ["bias", "discriminate", "exclude"]
        if any(keyword in action_description.lower() for keyword in bias_keywords):
            concerns.append("Potential bias or discrimination")

        return {
            "approved": len(concerns) == 0,
            "concerns": concerns,
            "principles_considered": EthicalOversight.BAHAI_PRINCIPLES[:3]  # Focus on key principles
        }