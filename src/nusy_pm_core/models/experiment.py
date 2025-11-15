"""
Experiment models for autonomous multi-agent experimentation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class DecisionPriority(Enum):
    """Priority levels for decisions requiring human input."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ExperimentStatus(Enum):
    """Status of an experiment phase or overall experiment."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class Decision:
    """A decision that requires human input."""
    id: str
    title: str
    context: str
    options: List[str]
    priority: str = DecisionPriority.MEDIUM.value
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    resolution: Optional[str] = None
    resolution_timestamp: Optional[datetime] = None


@dataclass
class DecisionQueue:
    """Queue for managing decisions requiring human input."""
    decisions: List[Decision] = field(default_factory=list)

    def add_decision(self, decision: Decision) -> None:
        """Add a decision to the queue."""
        self.decisions.append(decision)

    def get_pending_decisions(self) -> List[Decision]:
        """Get all pending (unresolved) decisions."""
        return [d for d in self.decisions if not d.resolved]

    def has_pending_decisions(self) -> bool:
        """Check if there are any pending decisions."""
        return len(self.get_pending_decisions()) > 0

    async def resolve_decision(self, decision_id: str, resolution: str) -> bool:
        """Resolve a decision with the given resolution."""
        for decision in self.decisions:
            if decision.id == decision_id and not decision.resolved:
                decision.resolved = True
                decision.resolution = resolution
                decision.resolution_timestamp = datetime.now()
                return True
        return False


@dataclass
class ExperimentPhase:
    """A phase within the experiment."""
    name: str
    duration_days: int
    behaviors: List[str]
    success_metrics: List[str]
    status: str = ExperimentStatus.NOT_STARTED.value
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    metrics_results: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentConfig:
    """Configuration for an autonomous experiment."""
    experiment_name: str
    duration_days: int
    phases: List[ExperimentPhase]
    decision_triggers: List[str]
    success_criteria: Dict[str, float]
    api_keys: Dict[str, str] = field(default_factory=dict)
    resource_limits: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentResult:
    """Results from running an experiment."""
    experiment_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = ExperimentStatus.NOT_STARTED.value
    phases_completed: int = 0
    total_phases: int = 0
    success_metrics: Dict[str, float] = field(default_factory=dict)
    failures: List[str] = field(default_factory=list)
    decisions_made: List[Decision] = field(default_factory=list)
    final_assessment: Dict[str, Any] = field(default_factory=dict)


@dataclass
class UsabilityTestResult:
    """Results from a usability test phase."""
    phase_name: str
    behaviors_tested: List[str]
    expected_results: List[str]
    actual_results: List[str]
    success_metrics: Dict[str, float]
    passed: bool = False
    issues_found: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)