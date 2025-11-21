"""
Santiago Product Manager Agent

Translates vision into concrete features and coordinates autonomous development teams.
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from santiago_core.core.agent_framework import SantiagoAgent, Task, Message, EthicalOversight
from santiago_core.services.knowledge_graph import SantiagoKnowledgeGraph
from santiago_core.services.memory_coordinator import SantiagoMemoryCoordinator


class SantiagoProductManager(SantiagoAgent):
    """Product Manager agent for the Santiago autonomous development team"""

    def __init__(self, workspace_path: Path, knowledge_graph: SantiagoKnowledgeGraph, memory_coordinator: SantiagoMemoryCoordinator):
        super().__init__("santiago-pm", workspace_path)
        self.vision_holder_intent = ""
        self.current_hypotheses: List[Dict] = []
        self.feature_backlog: List[Dict] = []
        self.knowledge_graph = knowledge_graph
        self.memory_coordinator = memory_coordinator

    async def handle_custom_message(self, message: Message) -> None:
        """Handle PM-specific messages"""
        if message.message_type == "vision_update":
            await self.process_vision_update(message)
        elif message.message_type == "hypothesis_request":
            await self.generate_hypotheses(message)
        elif message.message_type == "feature_request":
            await self.create_feature_spec(message)

    async def process_vision_update(self, message: Message) -> None:
        """Process updates to the product vision"""
        self.vision_holder_intent = message.content
        self.logger.info(f"Updated vision: {self.vision_holder_intent[:100]}...")

        # Generate initial hypotheses based on vision
        await self.generate_initial_hypotheses()

    async def generate_initial_hypotheses(self) -> None:
        """Generate initial product hypotheses from vision"""
        if not self.vision_holder_intent:
            return

        # Simple hypothesis generation - in practice this would use more sophisticated analysis
        hypotheses = [
            {
                "title": "Core autonomous development capability",
                "description": "Enable Santiago agents to autonomously develop and deploy software features",
                "success_criteria": "Agents can complete a full development cycle without human intervention",
                "experiments": ["Create minimal autonomous team", "Implement task coordination", "Add ethical oversight"]
            },
            {
                "title": "Knowledge graph integration",
                "description": "Integrate RDF knowledge graph for persistent learning and decision making",
                "success_criteria": "Agents can query and update knowledge graph during development",
                "experiments": ["Set up RDF store", "Implement SPARQL queries", "Create learning feedback loops"]
            },
            {
                "title": "Ethical AI framework",
                "description": "Ensure all autonomous actions align with ethical principles",
                "success_criteria": "All agent actions pass ethical evaluation before execution",
                "experiments": ["Implement ethical oversight", "Create principle-based decision making", "Add human override mechanisms"]
            }
        ]

        self.current_hypotheses = hypotheses

        # Notify architect and developer of new hypotheses
        await self.broadcast_message(
            json.dumps({"hypotheses": hypotheses}),
            "hypothesis_update"
        )

    async def generate_hypotheses(self, message: Message) -> None:
        """Generate hypotheses for a specific request"""
        request_data = json.loads(message.content)
        context = request_data.get("context", "")

        # Generate hypotheses based on context
        hypotheses = self._analyze_requirements(context)

        # Send hypotheses back to requester
        await self.send_message(
            message.sender,
            json.dumps({"hypotheses": hypotheses}),
            "hypothesis_response"
        )

    def _analyze_requirements(self, context: str) -> List[Dict]:
        """Analyze requirements and generate hypotheses"""
        # Simple analysis - extract key concepts and generate hypotheses
        concepts = re.findall(r'\b[A-Z][a-z]+\b', context)

        hypotheses = []
        for concept in concepts[:3]:  # Limit to 3 hypotheses
            hypotheses.append({
                "title": f"Implement {concept.lower()} functionality",
                "description": f"Develop core {concept.lower()} capabilities for autonomous operation",
                "success_criteria": f"{concept} features work correctly and integrate with existing systems",
                "experiments": [f"Create {concept.lower()} prototype", "Test integration", "Validate performance"]
            })

        return hypotheses

    async def create_feature_spec(self, message: Message) -> None:
        """Create a feature specification from requirements"""
        request_data = json.loads(message.content)
        hypothesis = request_data.get("hypothesis", {})

        # Create a feature specification in BDD format
        feature_spec = self._create_bdd_feature(hypothesis)

        # Save feature spec to file
        feature_path = self.workspace_path / "santiago-pm" / "cargo-manifests" / f"{hypothesis.get('title', 'feature').lower().replace(' ', '-')}.feature"
        feature_path.parent.mkdir(parents=True, exist_ok=True)

        with open(feature_path, 'w') as f:
            f.write(feature_spec)

        # Add to backlog
        self.feature_backlog.append({
            "hypothesis": hypothesis,
            "feature_file": str(feature_path),
            "status": "specified"
        })

        # Notify team of new feature
        await self.broadcast_message(
            json.dumps({
                "feature_spec": feature_spec,
                "feature_file": str(feature_path)
            }),
            "feature_ready"
        )

    def _create_bdd_feature(self, hypothesis: Dict) -> str:
        """Create a BDD feature specification"""
        title = hypothesis.get("title", "New Feature")
        description = hypothesis.get("description", "")
        experiments = hypothesis.get("experiments", [])

        feature = f"""Feature: {title}

  As a Santiago autonomous development team
  I want {description.lower()}
  So that I can deliver value autonomously

"""

        for i, experiment in enumerate(experiments, 1):
            feature += f"""  Scenario: Experiment {i} - {experiment}
    Given the autonomous team is initialized
    When I run the {experiment.lower()} experiment
    Then the system should demonstrate {experiment.lower()} capability

"""

        return feature

    async def start_working_on_task(self, task: Task) -> None:
        """Start working on a product management task"""
        self.logger.info(f"Starting PM task: {task.title}")

        # Record task in knowledge graph
        self.knowledge_graph.record_task(task.id, task.title, task.description, "santiago-pm")

        # Evaluate task ethically
        ethical_review = EthicalOversight.evaluate_action(task.description)
        if not ethical_review["approved"]:
            self.logger.warning(f"Task failed ethical review: {ethical_review['concerns']}")
            await self.update_task_status(task.id, "blocked", ethical_concerns=ethical_review["concerns"])
            self.knowledge_graph.record_learning("santiago-pm", "ethical_review", f"Task '{task.title}' failed ethical review", "blocked")
            return

        # Process based on task type
        if "hypothesis" in task.title.lower():
            await self.generate_initial_hypotheses()
        elif "feature" in task.title.lower():
            await self.create_feature_spec(Message(
                sender="system",
                recipient=self.name,
                content=json.dumps({"hypothesis": {"title": task.title, "description": task.description}})
            ))

        await self.update_task_status(task.id, "completed")
        self.knowledge_graph.update_task_status(task.id, "completed", "santiago-pm")
        self.knowledge_graph.record_learning("santiago-pm", "task_completion", f"Successfully completed task '{task.title}'", "success")

        # Record in memory system
        self.memory_coordinator.record_personal_learning(
            "santiago-pm",
            "task_completion",
            f"Completed task: {task.title} - {task.description}",
            confidence=0.9,
            source="experience"
        )