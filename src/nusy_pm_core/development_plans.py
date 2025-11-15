"""Development Plans Service."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from rdflib import URIRef, Literal

from .models.development_plan import DevelopmentPlan, Milestone, Task, PlanStatus, MilestoneStatus, TaskStatus
from .models.kg import KGNode, KGRelation
from .knowledge.graph import KnowledgeGraph, NUSY


class DevelopmentPlansService:
    """Service for managing development plans, milestones, and tasks."""

    def __init__(self, plans_file: Optional[Path] = None, kg: Optional[KnowledgeGraph] = None):
        self.plans_file = plans_file or Path(__file__).resolve().parents[2] / "data" / "development_plans.json"
        self.plans_file.parent.mkdir(parents=True, exist_ok=True)
        self.kg = kg or KnowledgeGraph()
        self._plans: Dict[str, DevelopmentPlan] = {}
        self._load_plans()

    def _load_plans(self) -> None:
        """Load plans from storage."""
        if self.plans_file.exists():
            with open(self.plans_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for plan_data in data.get('plans', []):
                    plan = self._deserialize_plan(plan_data)
                    self._plans[plan.id] = plan

    def _save_plans(self) -> None:
        """Save plans to storage."""
        data = {
            'plans': [self._serialize_plan(plan) for plan in self._plans.values()]
        }
        with open(self.plans_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _serialize_plan(self, plan: DevelopmentPlan) -> Dict[str, Any]:
        """Serialize a plan to dictionary."""
        return {
            'id': plan.id,
            'title': plan.title,
            'description': plan.description,
            'status': plan.status.value,
            'milestones': [self._serialize_milestone(m) for m in plan.milestones],
            'tags': plan.tags,
            'created_at': plan.created_at,
            'updated_at': plan.updated_at
        }

    def _deserialize_plan(self, data: Dict[str, Any]) -> DevelopmentPlan:
        """Deserialize a plan from dictionary."""
        plan = DevelopmentPlan(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=PlanStatus(data['status']),
            milestones=[self._deserialize_milestone(m) for m in data.get('milestones', [])],
            tags=data.get('tags', []),
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        return plan

    def _serialize_milestone(self, milestone: Milestone) -> Dict[str, Any]:
        """Serialize a milestone to dictionary."""
        return {
            'id': milestone.id,
            'title': milestone.title,
            'description': milestone.description,
            'status': milestone.status.value,
            'due_date': milestone.due_date,
            'tasks': [self._serialize_task(t) for t in milestone.tasks],
            'dependencies': milestone.dependencies,
            'created_at': milestone.created_at,
            'updated_at': milestone.updated_at
        }

    def _deserialize_milestone(self, data: Dict[str, Any]) -> Milestone:
        """Deserialize a milestone from dictionary."""
        milestone = Milestone(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=MilestoneStatus(data['status']),
            due_date=data.get('due_date'),
            tasks=[self._deserialize_task(t) for t in data.get('tasks', [])],
            dependencies=data.get('dependencies', []),
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        return milestone

    def _serialize_task(self, task: Task) -> Dict[str, Any]:
        """Serialize a task to dictionary."""
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status.value,
            'assignee': task.assignee,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
            'estimated_hours': task.estimated_hours,
            'actual_hours': task.actual_hours
        }

    def _deserialize_task(self, data: Dict[str, Any]) -> Task:
        """Deserialize a task from dictionary."""
        task = Task(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=TaskStatus(data['status']),
            assignee=data.get('assignee'),
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            estimated_hours=data.get('estimated_hours'),
            actual_hours=data.get('actual_hours')
        )
        return task

    def create_plan(self, title: str, description: str = "") -> DevelopmentPlan:
        """Create a new development plan."""
        plan = DevelopmentPlan.create(title, description)
        self._plans[plan.id] = plan
        self._save_plans()

        # Add to KG
        plan_uri = URIRef(f"{NUSY}plan/{plan.id}")
        self.kg.add_node(KGNode(plan_uri, title, NUSY.DevelopmentPlan))
        self.kg.add_relation(KGRelation(plan_uri, NUSY.description, Literal(description)))
        self.kg.add_relation(KGRelation(plan_uri, NUSY.status, Literal(plan.status.value)))
        self.kg.save()

        return plan

    def get_plan(self, plan_id: str) -> Optional[DevelopmentPlan]:
        """Get a plan by ID."""
        return self._plans.get(plan_id)

    def list_plans(self, status_filter: Optional[PlanStatus] = None) -> List[DevelopmentPlan]:
        """List all plans, optionally filtered by status."""
        plans = list(self._plans.values())
        if status_filter:
            plans = [p for p in plans if p.status == status_filter]
        return sorted(plans, key=lambda p: p.created_at, reverse=True)

    def add_milestone(self, plan_id: str, title: str, description: str = "", due_date: Optional[str] = None) -> Optional[Milestone]:
        """Add a milestone to a plan."""
        plan = self._plans.get(plan_id)
        if not plan:
            return None

        milestone = Milestone.create(title, description, due_date)
        plan.add_milestone(milestone)
        self._save_plans()

        # Add to KG
        milestone_uri = URIRef(f"{NUSY}milestone/{milestone.id}")
        plan_uri = URIRef(f"{NUSY}plan/{plan_id}")
        self.kg.add_node(KGNode(milestone_uri, title, NUSY.Milestone))
        self.kg.add_relation(KGRelation(plan_uri, NUSY.hasMilestone, milestone_uri))
        self.kg.save()

        return milestone

    def add_task(self, plan_id: str, milestone_id: str, title: str, description: str = "", assignee: Optional[str] = None) -> Optional[Task]:
        """Add a task to a milestone."""
        plan = self._plans.get(plan_id)
        if not plan:
            return None

        milestone = next((m for m in plan.milestones if m.id == milestone_id), None)
        if not milestone:
            return None

        task = Task.create(title, description, assignee)
        milestone.add_task(task)
        self._save_plans()

        # Add to KG
        task_uri = URIRef(f"{NUSY}task/{task.id}")
        milestone_uri = URIRef(f"{NUSY}milestone/{milestone_id}")
        self.kg.add_node(KGNode(task_uri, title, NUSY.Task))
        self.kg.add_relation(KGRelation(milestone_uri, NUSY.hasTask, task_uri))
        if assignee:
            self.kg.add_relation(KGRelation(task_uri, NUSY.assignee, Literal(assignee)))
        self.kg.save()

        return task

    def update_task_status(self, plan_id: str, milestone_id: str, task_id: str, status: TaskStatus) -> bool:
        """Update a task's status."""
        plan = self._plans.get(plan_id)
        if not plan:
            return False

        milestone = next((m for m in plan.milestones if m.id == milestone_id), None)
        if not milestone:
            return False

        task = next((t for t in milestone.tasks if t.id == task_id), None)
        if not task:
            return False

        task.status = status
        task.updated_at = datetime.now(timezone.utc).isoformat()
        milestone.updated_at = datetime.now(timezone.utc).isoformat()
        plan.updated_at = datetime.now(timezone.utc).isoformat()
        self._save_plans()

        # Update KG
        task_uri = URIRef(f"{NUSY}task/{task_id}")
        self.kg.add_relation(KGRelation(task_uri, NUSY.status, Literal(status.value)))
        self.kg.save()

        return True