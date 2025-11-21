"""
Santiago Architect Agent

Defines system architecture and technical approaches for autonomous development.
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

from santiago_core.core.agent_framework import SantiagoAgent, Task, Message, EthicalOversight
from santiago_core.services.knowledge_graph import SantiagoKnowledgeGraph
from santiago_core.services.memory_coordinator import SantiagoMemoryCoordinator


class SantiagoArchitect(SantiagoAgent):
    """Architect agent for defining system architecture and technical approaches"""

    def __init__(self, workspace_path: Path, knowledge_graph: SantiagoKnowledgeGraph, memory_coordinator: SantiagoMemoryCoordinator):
        super().__init__("santiago-architect", workspace_path)
        self.architecture_patterns: Dict[str, Dict] = {}
        self.current_architecture: Dict = {}
        self.tech_stack = {
            "languages": ["python", "typescript"],
            "frameworks": ["fastapi", "pydantic", "crewai"],
            "infrastructure": ["docker", "kubernetes", "github-actions"],
            "storage": ["rdf", "postgresql", "redis"]
        }
        self.knowledge_graph = knowledge_graph
        self.memory_coordinator = memory_coordinator

    async def handle_custom_message(self, message: Message) -> None:
        """Handle architect-specific messages"""
        if message.message_type == "hypothesis_update":
            await self.evaluate_hypotheses(message)
        elif message.message_type == "architecture_request":
            await self.design_architecture(message)
        elif message.message_type == "feature_ready":
            await self.review_feature_architecture(message)

    async def evaluate_hypotheses(self, message: Message) -> None:
        """Evaluate hypotheses from a technical architecture perspective"""
        data = json.loads(message.content)
        hypotheses = data.get("hypotheses", [])

        evaluated_hypotheses = []
        for hypothesis in hypotheses:
            evaluation = self._evaluate_technical_feasibility(hypothesis)
            evaluated_hypotheses.append({
                **hypothesis,
                "technical_evaluation": evaluation
            })

        # Send evaluation back to PM
        await self.send_message(
            "santiago-pm",
            json.dumps({"evaluated_hypotheses": evaluated_hypotheses}),
            "hypothesis_evaluation"
        )

    def _evaluate_technical_feasibility(self, hypothesis: Dict) -> Dict:
        """Evaluate technical feasibility of a hypothesis"""
        title = hypothesis.get("title", "")
        experiments = hypothesis.get("experiments", [])

        # Simple feasibility evaluation
        feasibility_score = 0.8  # Default high feasibility
        concerns = []
        recommendations = []

        # Check for complex integrations
        if "integration" in title.lower():
            feasibility_score -= 0.1
            recommendations.append("Consider microservices architecture")

        # Check for AI/ML components
        if any(term in title.lower() for term in ["ai", "ml", "autonomous", "agent"]):
            if "crewai" not in self.tech_stack["frameworks"]:
                concerns.append("May need additional AI framework")
                recommendations.append("Evaluate CrewAI vs AutoGen vs LangChain")

        # Check for scalability requirements
        if "scale" in title.lower() or "performance" in title.lower():
            recommendations.append("Design for horizontal scaling from day one")

        return {
            "feasibility_score": feasibility_score,
            "concerns": concerns,
            "recommendations": recommendations,
            "estimated_complexity": "medium" if len(experiments) > 2 else "low"
        }

    async def design_architecture(self, message: Message) -> None:
        """Design system architecture for a feature or component"""
        data = json.loads(message.content)
        requirements = data.get("requirements", "")
        context = data.get("context", "")

        # Generate architecture design
        architecture = self._generate_architecture_design(requirements, context)

        # Save architecture documentation
        arch_path = self.workspace_path / "santiago-pm" / "strategic-charts" / "architecture_design.md"
        arch_path.parent.mkdir(parents=True, exist_ok=True)

        with open(arch_path, 'w') as f:
            f.write(architecture)

        # Update current architecture knowledge
        self.current_architecture["latest_design"] = architecture
        self.current_architecture["design_file"] = str(arch_path)

        # Notify team of architecture design
        await self.broadcast_message(
            json.dumps({"architecture": architecture, "file": str(arch_path)}),
            "architecture_ready"
        )

    def _generate_architecture_design(self, requirements: str, context: str) -> str:
        """Generate an architecture design document"""
        design = f"""# System Architecture Design

## Requirements
{requirements}

## Context
{context}

## Technical Approach

### Core Components
- **Agent Framework**: Async Python-based agent system with message passing
- **Knowledge Graph**: RDF triple store for persistent learning
- **Task Coordination**: Distributed task management with dependency tracking
- **Ethical Oversight**: Built-in ethical evaluation for all actions

### Architecture Patterns
- **Microservices**: Modular agent services that can be deployed independently
- **Event-Driven**: Message-based communication between agents
- **CQRS**: Separate command and query models for better scalability
- **Saga Pattern**: Long-running transaction management for complex workflows

### Technology Stack
- **Languages**: Python 3.11+, TypeScript (for interfaces)
- **Frameworks**: FastAPI, Pydantic, CrewAI
- **Infrastructure**: Docker, Kubernetes, GitHub Actions
- **Storage**: RDF (for knowledge), PostgreSQL (for data), Redis (for caching)

### Deployment Architecture
```
graph TD
    A[Santiago Core] --> B[Agent Services]
    B --> C[Knowledge Graph]
    B --> D[Task Coordinator]
    A --> E[Ethical Oversight]
    E --> F[Decision Gateway]
```

### Security Considerations
- All agent actions subject to ethical review
- Human override mechanisms for critical decisions
- Audit logging of all autonomous actions
- Secure communication channels between agents

### Scalability Considerations
- Horizontal scaling of agent instances
- Distributed knowledge graph replication
- Load balancing for task distribution
- Monitoring and alerting for performance issues
"""

        return design

    async def review_feature_architecture(self, message: Message) -> None:
        """Review feature implementation from architectural perspective"""
        data = json.loads(message.content)
        feature_spec = data.get("feature_spec", "")
        feature_file = data.get("feature_file", "")

        # Review the feature specification
        review = self._review_feature_spec(feature_spec)

        # Send review feedback
        await self.send_message(
            "santiago-developer",
            json.dumps({
                "feature_file": feature_file,
                "architectural_review": review
            }),
            "feature_review"
        )

    def _review_feature_spec(self, feature_spec: str) -> Dict:
        """Review a feature specification for architectural concerns"""
        issues = []
        recommendations = []

        # Check for architectural patterns
        if "microservice" not in feature_spec.lower() and "service" in feature_spec.lower():
            recommendations.append("Consider microservices architecture for scalability")

        # Check for data persistence
        if "store" not in feature_spec.lower() and "save" not in feature_spec.lower():
            issues.append("Missing data persistence requirements")

        # Check for error handling
        if "error" not in feature_spec.lower() and "fail" not in feature_spec.lower():
            recommendations.append("Add error handling scenarios")

        return {
            "approved": len(issues) == 0,
            "issues": issues,
            "recommendations": recommendations,
            "architectural_patterns": ["event-driven", "cqrs", "saga"]
        }

    async def start_working_on_task(self, task: Task) -> None:
        """Start working on an architecture task"""
        self.logger.info(f"Starting architecture task: {task.title}")

        # Record task in knowledge graph
        self.knowledge_graph.record_task(task.id, task.title, task.description, "santiago-architect")

        # Evaluate task ethically
        ethical_review = EthicalOversight.evaluate_action(task.description)
        if not ethical_review["approved"]:
            self.logger.warning(f"Task failed ethical review: {ethical_review['concerns']}")
            await self.update_task_status(task.id, "blocked", ethical_concerns=ethical_review["concerns"])
            self.knowledge_graph.record_learning("santiago-architect", "ethical_review", f"Task '{task.title}' failed ethical review", "blocked")
            return

        # Process architecture tasks
        if "architecture" in task.title.lower():
            await self.design_architecture(Message(
                sender="system",
                recipient=self.name,
                content=json.dumps({
                    "requirements": task.description,
                    "context": "Autonomous development system"
                })
            ))

        await self.update_task_status(task.id, "completed")
        self.knowledge_graph.update_task_status(task.id, "completed", "santiago-architect")
        self.knowledge_graph.record_learning("santiago-architect", "task_completion", f"Successfully completed architecture task '{task.title}'", "success")

        # Record in memory system
        self.memory_coordinator.record_personal_learning(
            "santiago-architect",
            "architecture_design",
            f"Designed architecture for: {task.title} - {task.description}",
            confidence=0.8,
            source="experience"
        )