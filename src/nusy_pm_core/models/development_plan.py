"""Development Plans Domain Models."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import uuid4


class PlanStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class MilestoneStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


@dataclass
class Task:
    id: str
    title: str
    description: str
    status: TaskStatus
    assignee: Optional[str]
    created_at: str
    updated_at: str
    estimated_hours: Optional[float]
    actual_hours: Optional[float]

    @staticmethod
    def create(title: str, description: str = "", assignee: Optional[str] = None, estimated_hours: Optional[float] = None) -> "Task":
        now = datetime.now(timezone.utc).isoformat()
        return Task(
            id=uuid4().hex,
            title=title,
            description=description,
            status=TaskStatus.TODO,
            assignee=assignee,
            created_at=now,
            updated_at=now,
            estimated_hours=estimated_hours,
            actual_hours=None
        )


@dataclass
class Milestone:
    id: str
    title: str
    description: str
    status: MilestoneStatus
    due_date: Optional[str]
    tasks: List[Task]
    dependencies: List[str]  # Milestone IDs this depends on
    created_at: str
    updated_at: str

    @staticmethod
    def create(title: str, description: str = "", due_date: Optional[str] = None) -> "Milestone":
        now = datetime.now(timezone.utc).isoformat()
        return Milestone(
            id=uuid4().hex,
            title=title,
            description=description,
            status=MilestoneStatus.PENDING,
            due_date=due_date,
            tasks=[],
            dependencies=[],
            created_at=now,
            updated_at=now
        )

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def get_progress(self) -> Dict[str, Any]:
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return {"percentage": 0, "completed": 0, "total": 0}

        completed = sum(1 for task in self.tasks if task.status == TaskStatus.DONE)
        percentage = (completed / total_tasks) * 100

        return {
            "percentage": round(percentage, 1),
            "completed": completed,
            "total": total_tasks
        }


@dataclass
class DevelopmentPlan:
    id: str
    title: str
    description: str
    status: PlanStatus
    milestones: List[Milestone]
    tags: List[str]
    created_at: str
    updated_at: str

    @staticmethod
    def create(title: str, description: str = "") -> "DevelopmentPlan":
        now = datetime.now(timezone.utc).isoformat()
        return DevelopmentPlan(
            id=uuid4().hex,
            title=title,
            description=description,
            status=PlanStatus.DRAFT,
            milestones=[],
            tags=[],
            created_at=now,
            updated_at=now
        )

    def add_milestone(self, milestone: Milestone) -> None:
        self.milestones.append(milestone)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def get_progress(self) -> Dict[str, Any]:
        total_milestones = len(self.milestones)
        if total_milestones == 0:
            return {"percentage": 0, "completed": 0, "total": 0}

        completed = sum(1 for m in self.milestones if m.status == MilestoneStatus.COMPLETED)
        percentage = (completed / total_milestones) * 100

        return {
            "percentage": round(percentage, 1),
            "completed": completed,
            "total": total_milestones
        }