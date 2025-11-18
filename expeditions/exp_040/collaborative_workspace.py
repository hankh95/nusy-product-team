"""
EXP-040: Collaborative Workspace

Creates a shared workspace where Santiago entities can collaborate
on development work using in-memory Git and shared knowledge spaces.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import asyncio
import uuid
import json
from datetime import datetime
from dataclasses import dataclass, field

# Add EXP paths
exp_039_path = Path(__file__).parent.parent / "exp_039"
exp_040_path = Path(__file__).parent
sys.path.insert(0, str(exp_039_path))
sys.path.insert(0, str(exp_040_path))

try:
    from entity_architecture import SantiagoEntity, Goal, ActionResult
    from mcp_service_integration import IntegratedServiceRegistry
    from entity_specialization import SantiagoPMEntity, SantiagoDevEntity, SantiagoArchitectEntity
except ImportError as e:
    print(f"Warning: Could not import required components: {e}")
    # Create minimal mocks
    class SantiagoEntity:
        def __init__(self, identity): self.identity = identity
        async def reason_and_act(self, goal): return ActionResult(True, "mock", 0.1, 0.0)


@dataclass
class CollaborativeWorkspace:
    """
    Shared workspace for entity collaboration.

    Provides shared Git repository, knowledge spaces, and communication channels.
    """

    workspace_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Santiago Collaborative Workspace"
    created_at: datetime = field(default_factory=datetime.now)

    # Shared resources
    shared_git_repo: Dict[str, Any] = field(default_factory=dict)
    knowledge_spaces: Dict[str, Any] = field(default_factory=dict)
    active_projects: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Entity collaboration state
    participating_entities: Set[str] = field(default_factory=set)
    active_collaborations: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    # Communication channels
    message_channels: Dict[str, asyncio.Queue] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize workspace resources."""
        self._initialize_shared_resources()

    def _initialize_shared_resources(self):
        """Initialize shared workspace resources."""

        # Initialize shared Git repository
        self.shared_git_repo = {
            "branches": {"main": {"commits": [], "head": None}},
            "current_branch": "main",
            "working_directory": {},
            "staging_area": {},
            "commit_history": []
        }

        # Initialize knowledge spaces
        self.knowledge_spaces = {
            "project_requirements": {},
            "architecture_decisions": {},
            "implementation_notes": {},
            "testing_results": {},
            "deployment_status": {}
        }

        # Initialize communication channels
        self.message_channels = {
            "general": asyncio.Queue(),
            "urgent": asyncio.Queue(),
            "reviews": asyncio.Queue(),
            "planning": asyncio.Queue()
        }

    def add_entity(self, entity: SantiagoEntity):
        """Add an entity to the collaborative workspace."""
        self.participating_entities.add(entity.identity.entity_id)

        # Initialize entity-specific workspace state
        if entity.identity.entity_id not in self.active_projects:
            self.active_projects[entity.identity.entity_id] = {
                "assigned_tasks": [],
                "completed_work": [],
                "current_focus": None,
                "collaboration_history": []
            }

    async def share_knowledge(self, entity_id: str, space: str, knowledge: Dict[str, Any]):
        """Share knowledge in a workspace knowledge space."""
        if space not in self.knowledge_spaces:
            self.knowledge_spaces[space] = {}

        knowledge_entry = {
            "entity_id": entity_id,
            "content": knowledge,
            "timestamp": datetime.now(),
            "version": len(self.knowledge_spaces[space]) + 1
        }

        key = f"{entity_id}_{datetime.now().isoformat()}"
        self.knowledge_spaces[space][key] = knowledge_entry

    def get_shared_knowledge(self, space: str, entity_id: str = None) -> Dict[str, Any]:
        """Get knowledge from a shared space."""
        if space not in self.knowledge_spaces:
            return {}

        space_content = self.knowledge_spaces[space]

        if entity_id:
            # Filter by entity
            return {k: v for k, v in space_content.items() if v["entity_id"] == entity_id}

        return space_content

    async def git_commit(self, entity_id: str, message: str, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a collaborative Git commit."""
        # Stage changes
        for file_path, content in changes.items():
            self.shared_git_repo["staging_area"][file_path] = {
                "content": content,
                "modified_by": entity_id,
                "timestamp": datetime.now()
            }

        # Create commit
        commit = {
            "id": str(uuid.uuid4()),
            "message": message,
            "author": entity_id,
            "timestamp": datetime.now(),
            "changes": dict(self.shared_git_repo["staging_area"]),
            "parent": self.shared_git_repo["branches"][self.shared_git_repo["current_branch"]]["head"]
        }

        # Update repository state
        current_branch = self.shared_git_repo["current_branch"]
        self.shared_git_repo["branches"][current_branch]["commits"].append(commit["id"])
        self.shared_git_repo["branches"][current_branch]["head"] = commit["id"]
        self.shared_git_repo["commit_history"].append(commit)

        # Clear staging area
        self.shared_git_repo["staging_area"].clear()

        # Update working directory
        for file_path, change in commit["changes"].items():
            self.shared_git_repo["working_directory"][file_path] = change["content"]

        return {
            "commit_id": commit["id"],
            "branch": current_branch,
            "files_changed": len(commit["changes"])
        }

    def git_status(self) -> Dict[str, Any]:
        """Get Git repository status."""
        return {
            "current_branch": self.shared_git_repo["current_branch"],
            "staged_changes": len(self.shared_git_repo["staging_area"]),
            "working_directory_files": len(self.shared_git_repo["working_directory"]),
            "total_commits": len(self.shared_git_repo["commit_history"])
        }

    async def send_message(self, from_entity: str, to_entity: str, channel: str, message: Dict[str, Any]):
        """Send message between entities via workspace channels."""
        if channel not in self.message_channels:
            return False

        full_message = {
            "from": from_entity,
            "to": to_entity,
            "channel": channel,
            "content": message,
            "timestamp": datetime.now()
        }

        await self.message_channels[channel].put(full_message)
        return True

    async def receive_messages(self, entity_id: str, channel: str = "general") -> List[Dict[str, Any]]:
        """Receive messages for an entity from a channel."""
        if channel not in self.message_channels:
            return []

        messages = []
        # Check for messages addressed to this entity
        queue_size = self.message_channels[channel].qsize()
        for _ in range(queue_size):
            try:
                message = self.message_channels[channel].get_nowait()
                if message["to"] == entity_id or message["to"] == "all":
                    messages.append(message)
                else:
                    # Put back messages not for this entity
                    await self.message_channels[channel].put(message)
            except asyncio.QueueEmpty:
                break

        return messages

    def get_workspace_status(self) -> Dict[str, Any]:
        """Get overall workspace status."""
        return {
            "workspace_id": self.workspace_id,
            "name": self.name,
            "participating_entities": len(self.participating_entities),
            "active_projects": len(self.active_projects),
            "knowledge_spaces": len(self.knowledge_spaces),
            "git_status": self.git_status(),
            "created_at": self.created_at.isoformat()
        }


@dataclass
class CollaborativeGoal:
    """
    A goal that requires collaboration between multiple entities.
    """

    title: str
    description: str
    goal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    priority: int = 1
    deadline: Optional[datetime] = None

    # Collaboration details
    required_roles: List[str] = field(default_factory=list)  # ["pm", "dev", "architect"]
    assigned_entities: Dict[str, str] = field(default_factory=dict)  # role -> entity_id

    # Progress tracking
    status: str = "pending"  # pending, active, completed, failed
    subtasks: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # subtask_id -> details
    progress: float = 0.0

    # Results
    deliverables: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def assign_entity(self, role: str, entity_id: str):
        """Assign an entity to a role."""
        self.assigned_entities[role] = entity_id

    def add_subtask(self, subtask_id: str, description: str, assigned_role: str):
        """Add a subtask to the collaborative goal."""
        self.subtasks[subtask_id] = {
            "description": description,
            "assigned_role": assigned_role,
            "status": "pending",
            "created_at": datetime.now()
        }

    def update_subtask_progress(self, subtask_id: str, status: str, progress: float = 1.0):
        """Update subtask progress."""
        if subtask_id in self.subtasks:
            self.subtasks[subtask_id]["status"] = status
            self.subtasks[subtask_id]["progress"] = progress
            self.subtasks[subtask_id]["updated_at"] = datetime.now()

        # Recalculate overall progress
        if self.subtasks:
            completed_tasks = sum(1 for task in self.subtasks.values() if task["status"] == "completed")
            self.progress = completed_tasks / len(self.subtasks)


class CollaborativeWorkflow:
    """
    Manages collaborative workflows between specialized entities.
    """

    def __init__(self, workspace: CollaborativeWorkspace, service_registry: IntegratedServiceRegistry):
        self.workspace = workspace
        self.service_registry = service_registry
        self.entities: Dict[str, SantiagoEntity] = {}
        self.active_goals: Dict[str, CollaborativeGoal] = {}

    def register_entity(self, role: str, entity: SantiagoEntity):
        """Register an entity with a specific role."""
        self.entities[role] = entity
        self.workspace.add_entity(entity)

    async def create_collaborative_goal(self,
                                      title: str,
                                      description: str,
                                      required_roles: List[str],
                                      priority: int = 1) -> CollaborativeGoal:
        """Create a new collaborative goal."""

        goal = CollaborativeGoal(
            title=title,
            description=description,
            required_roles=required_roles,
            priority=priority
        )

        # Assign available entities to roles
        for role in required_roles:
            if role in self.entities:
                goal.assign_entity(role, self.entities[role].identity.entity_id)

        self.active_goals[goal.goal_id] = goal
        return goal

    async def execute_collaborative_goal(self, goal: CollaborativeGoal) -> Dict[str, Any]:
        """
        Execute a collaborative goal by coordinating between entities.
        """

        goal.status = "active"
        results = {}

        try:
            # Phase 1: Planning and requirements gathering (PM)
            if "pm" in goal.assigned_entities:
                pm_entity = self.entities["pm"]
                pm_goal = Goal(
                    id=f"{goal.goal_id}_planning",
                    description=f"Analyze requirements and create plan for: {goal.description}",
                    priority=goal.priority
                )

                pm_result = await pm_entity.reason_and_act(pm_goal)
                results["planning"] = pm_result.result

                # Share requirements in workspace
                await self.workspace.share_knowledge(
                    pm_entity.identity.entity_id,
                    "project_requirements",
                    {"goal_id": goal.goal_id, "requirements": pm_result.result}
                )

                goal.update_subtask_progress(f"{goal.goal_id}_planning", "completed")

            # Phase 2: Architecture design (Architect)
            if "architect" in goal.assigned_entities:
                architect_entity = self.entities["architect"]
                arch_goal = Goal(
                    id=f"{goal.goal_id}_design",
                    description=f"Design architecture for: {goal.description}",
                    priority=goal.priority
                )

                arch_result = await architect_entity.reason_and_act(arch_goal)
                results["architecture"] = arch_result.result

                # Share architecture decisions
                await self.workspace.share_knowledge(
                    architect_entity.identity.entity_id,
                    "architecture_decisions",
                    {"goal_id": goal.goal_id, "architecture": arch_result.result}
                )

                goal.update_subtask_progress(f"{goal.goal_id}_design", "completed")

            # Phase 3: Implementation (Dev)
            if "dev" in goal.assigned_entities:
                dev_entity = self.entities["dev"]
                dev_goal = Goal(
                    id=f"{goal.goal_id}_implementation",
                    description=f"Implement solution for: {goal.description}",
                    priority=goal.priority
                )

                dev_result = await dev_entity.reason_and_act(dev_goal)
                results["implementation"] = dev_result.result

                # Commit implementation to shared Git
                changes = {
                    f"implementation_{goal.goal_id}.py": dev_result.result.get("implementation", ""),
                    f"tests_{goal.goal_id}.py": dev_result.result.get("tests", "")
                }

                commit_result = await self.workspace.git_commit(
                    dev_entity.identity.entity_id,
                    f"Implement {goal.title}",
                    changes
                )

                results["git_commit"] = commit_result

                # Share implementation notes
                await self.workspace.share_knowledge(
                    dev_entity.identity.entity_id,
                    "implementation_notes",
                    {"goal_id": goal.goal_id, "implementation": dev_result.result}
                )

                goal.update_subtask_progress(f"{goal.goal_id}_implementation", "completed")

            # Phase 4: Review and validation (All entities)
            review_results = await self._conduct_collaborative_review(goal, results)
            results["review"] = review_results

            goal.status = "completed"
            goal.deliverables = results

            return {
                "success": True,
                "goal_id": goal.goal_id,
                "results": results,
                "workspace_status": self.workspace.get_workspace_status()
            }

        except Exception as e:
            goal.status = "failed"
            return {
                "success": False,
                "goal_id": goal.goal_id,
                "error": str(e),
                "partial_results": results
            }

    async def _conduct_collaborative_review(self, goal: CollaborativeGoal, results: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct collaborative review of the work."""

        review_results = {}

        # Each entity reviews the work from their perspective
        for role, entity_id in goal.assigned_entities.items():
            if role in self.entities:
                entity = self.entities[role]

                # Create review goal
                review_goal = Goal(
                    id=f"{goal.goal_id}_review_{role}",
                    description=f"Review {goal.title} from {role} perspective",
                    priority=goal.priority
                )

                review_result = await entity.reason_and_act(review_goal)
                review_results[role] = review_result.result

                # Share review feedback
                await self.workspace.share_knowledge(
                    entity.identity.entity_id,
                    "testing_results",
                    {"goal_id": goal.goal_id, "review": review_result.result, "reviewer_role": role}
                )

        return review_results

    def get_workflow_status(self) -> Dict[str, Any]:
        """Get status of the collaborative workflow."""
        return {
            "active_goals": len(self.active_goals),
            "completed_goals": len([g for g in self.active_goals.values() if g.status == "completed"]),
            "entities": list(self.entities.keys()),
            "workspace_status": self.workspace.get_workspace_status()
        }


# Test collaborative workspace
async def test_collaborative_workspace():
    """Test collaborative workspace functionality."""

    print("Testing Collaborative Workspace...")

    # Create workspace and service registry
    workspace = CollaborativeWorkspace(name="Test Santiago Workspace")
    service_registry = IntegratedServiceRegistry()

    # Create collaborative workflow
    workflow = CollaborativeWorkflow(workspace, service_registry)

    # Create and register entities
    from entity_specialization import SantiagoEntityFactory
    factory = SantiagoEntityFactory(service_registry)

    entities = factory.create_all_entities()
    for role, entity in entities.items():
        workflow.register_entity(role, entity)

    print(f"Registered entities: {list(entities.keys())}")

    # Create a collaborative goal
    goal = await workflow.create_collaborative_goal(
        title="Implement User Authentication Feature",
        description="Implement secure user authentication with JWT tokens",
        required_roles=["pm", "architect", "dev"],
        priority=2
    )

    print(f"Created collaborative goal: {goal.title}")

    # Execute the collaborative goal
    result = await workflow.execute_collaborative_goal(goal)

    print(f"Goal execution success: {result['success']}")
    print(f"Workspace status: {workspace.get_workspace_status()}")
    print(f"Git status: {workspace.git_status()}")

    print("\nCollaborative workspace test completed!")


if __name__ == "__main__":
    asyncio.run(test_collaborative_workspace())