"""
Workflow Orchestration Engine - EXP-036 Core Component

Implements sophisticated state machines for Santiago development workflows.
Handles 8 core states + 10 problem states with Bayesian prioritization,
lean flow metrics, and autonomous workflow optimization.

Key Features:
- State Machine Engine: Handles complex workflow transitions
- Bayesian Prioritization: Intelligent task ordering and resource allocation
- Lean Flow Metrics: Real-time efficiency tracking and optimization
- Problem State Management: Specialized handling for workflow blockages
- Self-Evolution Integration: Workflow improvement suggestions
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any, Callable
from collections import defaultdict, deque
import statistics
import math


class WorkflowState(Enum):
    """Core workflow states identified through expedition analysis."""
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    APPROVED = "approved"
    INTEGRATED = "integrated"
    DONE = "done"
    BLOCKED = "blocked"


class ProblemState(Enum):
    """Problem states that can cause workflow blockages."""
    MISSING_DEPENDENCIES = "missing_dependencies"
    TECHNICAL_UNCERTAINTY = "technical_uncertainty"
    CODE_REVIEW_FAILURES = "code_review_failures"
    TESTING_BLOCKAGES = "testing_blockages"
    RESOURCE_CONTENTION = "resource_contention"
    PRIORITY_CONFLICTS = "priority_conflicts"
    COMMUNICATION_GAPS = "communication_gaps"
    QUALITY_GATE_FAILURES = "quality_gate_failures"
    DEPLOYMENT_ISSUES = "deployment_issues"
    SCOPE_CREEP = "scope_creep"


@dataclass
class WorkflowItem:
    """Represents an item moving through the workflow."""
    id: str
    title: str
    description: str
    state: WorkflowState
    problem_state: Optional[ProblemState] = None
    priority: float = 1.0  # 0.0 = lowest, 1.0 = highest
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    assignee: Optional[str] = None
    tags: Set[str] = field(default_factory=set)
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Timing metrics
    time_in_state: Dict[WorkflowState, float] = field(default_factory=dict)
    total_blocked_time: float = 0.0
    total_active_time: float = 0.0

    # Flow metrics
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    cycle_time: Optional[float] = None  # Hours from start to completion


@dataclass
class WorkflowTransition:
    """Defines a valid transition between workflow states."""
    from_state: WorkflowState
    to_state: WorkflowState
    conditions: List[Callable[[WorkflowItem], bool]] = field(default_factory=list)
    actions: List[Callable[[WorkflowItem], None]] = field(default_factory=list)
    priority_boost: float = 0.0  # Priority increase on transition


@dataclass
class LeanFlowMetrics:
    """Real-time lean flow metrics for workflow optimization."""
    cycle_time_hours: float = 0.0  # Average time from start to completion
    flow_efficiency: float = 0.0   # Active time / total time
    wait_time_percentage: float = 0.0  # Time spent waiting / total time
    throughput_per_day: float = 0.0   # Items completed per day
    wip_limit: int = 5  # Work in progress limit
    current_wip: int = 0

    # Problem state metrics
    problem_state_counts: Dict[ProblemState, int] = field(default_factory=dict)
    average_resolution_time: Dict[ProblemState, float] = field(default_factory=dict)

    # Trend analysis
    cycle_time_trend: List[float] = field(default_factory=list)
    flow_efficiency_trend: List[float] = field(default_factory=list)


@dataclass
class BayesianPrioritization:
    """Bayesian network for intelligent task prioritization."""
    # Prior probabilities for different factors
    priority_factors: Dict[str, float] = field(default_factory=lambda: {
        "age": 0.3,          # Older items get priority
        "blockers": 0.25,    # Items blocking others get priority
        "complexity": 0.2,   # Complex items need attention
        "deadline": 0.15,    # Time-sensitive items
        "expertise": 0.1     # Items matching agent expertise
    })

    # Learned weights from workflow history
    learned_weights: Dict[str, float] = field(default_factory=dict)

    # Historical data for learning
    prioritization_history: List[Tuple[Dict[str, float], float]] = field(default_factory=list)


class WorkflowOrchestrationEngine:
    """
    Advanced workflow orchestration engine for Santiago development.

    Implements state machines, Bayesian prioritization, and lean flow metrics
    to optimize development velocity and efficiency.
    """

    def __init__(self):
        self.items: Dict[str, WorkflowItem] = {}
        self.transitions: List[WorkflowTransition] = []
        self.metrics = LeanFlowMetrics()

        # Bayesian prioritization engine
        self.prioritization = BayesianPrioritization()

        # Workflow queues by state
        self.state_queues: Dict[WorkflowState, deque] = {
            state: deque() for state in WorkflowState
        }

        # Problem state tracking
        self.problem_state_tracking: Dict[str, datetime] = {}

        # Metrics history for trend analysis
        self.metrics_history: List[Tuple[datetime, LeanFlowMetrics]] = []

        # Initialize default workflow transitions
        self._initialize_default_transitions()

    def _initialize_default_transitions(self):
        """Initialize the default workflow state machine transitions."""

        # Standard workflow transitions
        transitions = [
            WorkflowTransition(
                WorkflowState.BACKLOG, WorkflowState.READY,
                conditions=[lambda item: self._check_readiness(item)]
            ),
            WorkflowTransition(
                WorkflowState.READY, WorkflowState.IN_PROGRESS,
                actions=[lambda item: self._start_item(item)]
            ),
            WorkflowTransition(
                WorkflowState.IN_PROGRESS, WorkflowState.REVIEW,
                conditions=[lambda item: self._check_completion(item)]
            ),
            WorkflowTransition(
                WorkflowState.REVIEW, WorkflowState.APPROVED,
                conditions=[lambda item: self._check_approval(item)]
            ),
            WorkflowTransition(
                WorkflowState.APPROVED, WorkflowState.INTEGRATED,
                actions=[lambda item: self._integrate_item(item)]
            ),
            WorkflowTransition(
                WorkflowState.INTEGRATED, WorkflowState.DONE,
                actions=[lambda item: self._complete_item(item)]
            ),

            # Blocked state transitions
            WorkflowTransition(
                WorkflowState.BLOCKED, WorkflowState.READY,
                conditions=[lambda item: self._check_blocker_resolution(item)],
                priority_boost=0.2
            ),

            # Problem state resolution transitions
            WorkflowTransition(
                WorkflowState.BLOCKED, WorkflowState.IN_PROGRESS,
                conditions=[lambda item: self._check_problem_resolution(item)]
            ),
        ]

        # Add transitions for moving items back to blocked
        for state in [WorkflowState.READY, WorkflowState.IN_PROGRESS, WorkflowState.REVIEW]:
            transitions.append(WorkflowTransition(
                state, WorkflowState.BLOCKED,
                conditions=[lambda item: self._detect_blockage(item)]
            ))

        self.transitions = transitions

    def _check_readiness(self, item: WorkflowItem) -> bool:
        """Check if an item is ready to move from backlog to ready."""
        # Check dependencies
        dependencies = item.metadata.get("dependencies", [])
        for dep_id in dependencies:
            if dep_id in self.items:
                dep_item = self.items[dep_id]
                if dep_item.state != WorkflowState.DONE:
                    return False
        return True

    def _check_completion(self, item: WorkflowItem) -> bool:
        """Check if work on an item is complete."""
        # Check completion criteria from metadata
        criteria = item.metadata.get("completion_criteria", [])
        return all(criteria) if criteria else True

    def _check_approval(self, item: WorkflowItem) -> bool:
        """Check if an item has been approved in review."""
        return item.metadata.get("approved", False)

    def _check_blocker_resolution(self, item: WorkflowItem) -> bool:
        """Check if blockers have been resolved."""
        return item.problem_state is None

    def _check_problem_resolution(self, item: WorkflowItem) -> bool:
        """Check if the current problem has been resolved."""
        if item.problem_state is None:
            return True

        # Problem-specific resolution checks
        problem_checks = {
            ProblemState.MISSING_DEPENDENCIES: lambda: self._check_dependencies_resolved(item),
            ProblemState.TECHNICAL_UNCERTAINTY: lambda: self._check_technical_clarity(item),
            ProblemState.CODE_REVIEW_FAILURES: lambda: self._check_review_passed(item),
            ProblemState.TESTING_BLOCKAGES: lambda: self._check_tests_passing(item),
        }

        check_func = problem_checks.get(item.problem_state)
        return check_func() if check_func else False

    def _detect_blockage(self, item: WorkflowItem) -> bool:
        """Detect if an item should be moved to blocked state."""
        # Check for various blockage conditions
        if item.metadata.get("blocked", False):
            return True

        # Check for timeout in current state
        state_timeout = item.metadata.get("state_timeout_hours", 24)
        current_state_time = item.time_in_state.get(item.state, 0)
        if current_state_time > state_timeout:
            return True

        return False

    def _start_item(self, item: WorkflowItem):
        """Mark an item as started."""
        item.started_at = datetime.now()
        item.updated_at = datetime.now()

    def _integrate_item(self, item: WorkflowItem):
        """Handle item integration."""
        item.updated_at = datetime.now()

    def _complete_item(self, item: WorkflowItem):
        """Mark an item as completed."""
        item.completed_at = datetime.now()
        item.cycle_time = (item.completed_at - (item.started_at or item.created_at)).total_seconds() / 3600
        item.updated_at = datetime.now()

        # Update metrics
        self._update_lean_flow_metrics()

    def _check_dependencies_resolved(self, item: WorkflowItem) -> bool:
        """Check if missing dependencies have been resolved."""
        return self._check_readiness(item)

    def _check_technical_clarity(self, item: WorkflowItem) -> bool:
        """Check if technical uncertainty has been resolved."""
        return item.metadata.get("technical_clarity", False)

    def _check_review_passed(self, item: WorkflowItem) -> bool:
        """Check if code review has passed."""
        return item.metadata.get("review_passed", False)

    def _check_tests_passing(self, item: WorkflowItem) -> bool:
        """Check if tests are passing."""
        return item.metadata.get("tests_passing", False)

    async def create_workflow_item(self, title: str, description: str = "",
                                 priority: float = 1.0, tags: Set[str] = None,
                                 metadata: Dict[str, Any] = None) -> str:
        """Create a new workflow item."""
        item_id = f"item_{int(time.time() * 1000)}_{hash(title) % 1000}"

        item = WorkflowItem(
            id=item_id,
            title=title,
            description=description,
            state=WorkflowState.BACKLOG,
            priority=priority,
            tags=tags or set(),
            metadata=metadata or {}
        )

        self.items[item_id] = item
        self.state_queues[WorkflowState.BACKLOG].append(item_id)

        # Update Bayesian prioritization with new item
        await self._update_prioritization_model()

        return item_id

    async def transition_item(self, item_id: str, target_state: WorkflowState,
                            problem_state: Optional[ProblemState] = None) -> bool:
        """Attempt to transition an item to a new state."""
        if item_id not in self.items:
            return False

        item = self.items[item_id]

        # Find valid transition
        valid_transition = None
        for transition in self.transitions:
            if (transition.from_state == item.state and
                transition.to_state == target_state):

                # Check conditions
                if all(condition(item) for condition in transition.conditions):
                    valid_transition = transition
                    break

        if not valid_transition:
            return False

        # Execute transition
        old_state = item.state
        item.state = target_state
        item.problem_state = problem_state
        item.priority += valid_transition.priority_boost
        item.updated_at = datetime.now()

        # Update timing metrics
        state_time = (datetime.now() - item.updated_at).total_seconds() / 3600
        item.time_in_state[old_state] = item.time_in_state.get(old_state, 0) + state_time

        if target_state == WorkflowState.BLOCKED:
            item.total_blocked_time += state_time
        else:
            item.total_active_time += state_time

        # Execute transition actions
        for action in valid_transition.actions:
            action(item)

        # Update queues
        if item_id in self.state_queues[old_state]:
            self.state_queues[old_state].remove(item_id)
        self.state_queues[target_state].append(item_id)

        # Track problem states
        if problem_state:
            self.problem_state_tracking[item_id] = datetime.now()
            self.metrics.problem_state_counts[problem_state] = \
                self.metrics.problem_state_counts.get(problem_state, 0) + 1

        # Update metrics
        self._update_lean_flow_metrics()

        return True

    async def get_prioritized_items(self, state: WorkflowState, limit: int = 10) -> List[WorkflowItem]:
        """Get items in a state ordered by Bayesian prioritization."""
        if state not in self.state_queues:
            return []

        item_ids = list(self.state_queues[state])
        if not item_ids:
            return []

        # Calculate priorities using Bayesian model
        prioritized_items = []
        for item_id in item_ids:
            item = self.items[item_id]
            bayesian_priority = await self._calculate_bayesian_priority(item)
            prioritized_items.append((bayesian_priority, item))

        # Sort by priority (highest first)
        prioritized_items.sort(key=lambda x: x[0], reverse=True)

        return [item for _, item in prioritized_items[:limit]]

    async def _calculate_bayesian_priority(self, item: WorkflowItem) -> float:
        """Calculate Bayesian priority score for an item."""
        factors = {}

        # Age factor (older items get higher priority)
        age_hours = (datetime.now() - item.created_at).total_seconds() / 3600
        factors["age"] = min(age_hours / 168, 1.0)  # Cap at 1 week

        # Blocker factor (items blocking others)
        blockers = item.metadata.get("blocking", [])
        factors["blockers"] = min(len(blockers) * 0.2, 1.0)

        # Complexity factor (based on tags and metadata)
        complexity_indicators = ["complex", "high-risk", "architectural"]
        complexity_score = len(item.tags & set(complexity_indicators))
        factors["complexity"] = min(complexity_score * 0.3, 1.0)

        # Deadline factor
        deadline = item.metadata.get("deadline")
        if deadline and isinstance(deadline, datetime):
            time_to_deadline = (deadline - datetime.now()).total_seconds() / 3600
            factors["deadline"] = max(0, 1.0 - (time_to_deadline / 168))  # 1 week horizon
        else:
            factors["deadline"] = 0.0

        # Expertise factor (placeholder - would integrate with agent profiles)
        factors["expertise"] = 0.5

        # Calculate weighted score
        weights = self.prioritization.learned_weights or self.prioritization.priority_factors
        score = sum(factors[key] * weights.get(key, 0) for key in factors)

        # Normalize to 0-1 range
        return min(max(score, 0.0), 1.0)

    async def _update_prioritization_model(self):
        """Update Bayesian prioritization model based on workflow history."""
        if len(self.prioritization.prioritization_history) < 10:
            return  # Need more data

        # Simple learning: adjust weights based on successful completions
        recent_history = self.prioritization.prioritization_history[-50:]

        # Calculate correlation between factors and success
        factor_performance = defaultdict(list)

        for factors, success in recent_history:
            for factor, value in factors.items():
                factor_performance[factor].append((value, success))

        # Update weights based on correlation
        for factor, performances in factor_performance.items():
            if len(performances) >= 5:
                values, successes = zip(*performances)
                try:
                    correlation = statistics.correlation(values, successes)
                    # Adjust weight based on correlation
                    current_weight = self.prioritization.learned_weights.get(factor,
                        self.prioritization.priority_factors[factor])
                    self.prioritization.learned_weights[factor] = max(0.1,
                        current_weight + correlation * 0.1)
                except:
                    pass  # Skip if correlation calculation fails

    def _update_lean_flow_metrics(self):
        """Update real-time lean flow metrics."""
        completed_items = [item for item in self.items.values()
                          if item.state == WorkflowState.DONE and item.cycle_time]

        if completed_items:
            # Cycle time metrics
            cycle_times = [item.cycle_time for item in completed_items]
            self.metrics.cycle_time_hours = statistics.mean(cycle_times)

            # Flow efficiency (active time / total time)
            total_times = [item.total_active_time + item.total_blocked_time
                          for item in completed_items if item.total_active_time + item.total_blocked_time > 0]
            if total_times:
                flow_efficiencies = [item.total_active_time / total_time
                                   for item, total_time in zip(completed_items, total_times)
                                   if total_time > 0]
                self.metrics.flow_efficiency = statistics.mean(flow_efficiencies) if flow_efficiencies else 0.0

            # Throughput
            recent_completions = [item for item in completed_items
                                if item.completed_at and
                                (datetime.now() - item.completed_at).days <= 7]
            self.metrics.throughput_per_day = len(recent_completions) / 7

        # Current WIP
        self.metrics.current_wip = len([item for item in self.items.values()
                                      if item.state in [WorkflowState.IN_PROGRESS, WorkflowState.REVIEW]])

        # Update trends
        current_time = datetime.now()
        self.metrics.cycle_time_trend.append(self.metrics.cycle_time_hours)
        self.metrics.flow_efficiency_trend.append(self.metrics.flow_efficiency)

        # Keep only recent trend data
        if len(self.metrics.cycle_time_trend) > 50:
            self.metrics.cycle_time_trend.pop(0)
        if len(self.metrics.flow_efficiency_trend) > 50:
            self.metrics.flow_efficiency_trend.pop(0)

        # Store metrics history
        self.metrics_history.append((current_time, self.metrics))
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)

    def get_workflow_metrics(self) -> LeanFlowMetrics:
        """Get current lean flow metrics."""
        return self.metrics

    def get_blockage_analysis(self) -> Dict[str, Any]:
        """Analyze workflow blockages and bottlenecks."""
        analysis = {
            "top_blockages": dict(sorted(self.metrics.problem_state_counts.items(),
                                       key=lambda x: x[1], reverse=True)[:5]),
            "average_resolution_times": self.metrics.average_resolution_time,
            "current_blocked_items": len([item for item in self.items.values()
                                        if item.state == WorkflowState.BLOCKED]),
            "blockage_rate": len([item for item in self.items.values()
                                if item.state == WorkflowState.BLOCKED]) / max(len(self.items), 1)
        }
        return analysis

    async def optimize_workflow(self) -> List[str]:
        """Generate workflow optimization suggestions."""
        suggestions = []

        # Check WIP limits
        if self.metrics.current_wip > self.metrics.wip_limit:
            suggestions.append(f"WIP limit exceeded ({self.metrics.current_wip}/{self.metrics.wip_limit}). Consider completing items before starting new ones.")

        # Check flow efficiency
        if self.metrics.flow_efficiency < 0.8:
            suggestions.append(f"Flow efficiency is {self.metrics.flow_efficiency:.1%}, below 80% target. Focus on reducing wait times.")

        # Check cycle time trends
        if len(self.metrics.cycle_time_trend) >= 3:
            recent_avg = statistics.mean(self.metrics.cycle_time_trend[-3:])
            overall_avg = statistics.mean(self.metrics.cycle_time_trend)
            if recent_avg > overall_avg * 1.2:
                suggestions.append("Cycle time increasing. Review current bottlenecks and resource allocation.")

        # Check problem state patterns
        top_problems = sorted(self.metrics.problem_state_counts.items(),
                            key=lambda x: x[1], reverse=True)[:3]
        for problem, count in top_problems:
            if count > 5:
                suggestions.append(f"High incidence of {problem.value} ({count} items). Consider process improvements.")

        return suggestions


# Global workflow engine instance
_workflow_engine = None


def get_workflow_orchestration_engine() -> WorkflowOrchestrationEngine:
    """Get the global workflow orchestration engine instance."""
    global _workflow_engine
    if _workflow_engine is None:
        _workflow_engine = WorkflowOrchestrationEngine()
    return _workflow_engine
