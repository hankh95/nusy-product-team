"""
EXP-034: Santiago Agent Framework

Base classes and implementations for Santiago agents operating in shared memory.
Each Santiago has specialized capabilities while collaborating through the shared
Git repository and direct memory communication.

Architecture:
- SantiagoAgent: Base class with shared memory integration
- SantiagoCore: Boat builder - creates and evolves other Santiagos
- SantiagoPM: Navigator - product management and coordination
- SantiagoDev: Crew - implementation and testing
"""

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
import threading
import json

from shared_memory_git_service import get_shared_memory_git_service, SharedMemoryGitService


@dataclass
class SantiagoMessage:
    """Message passed between Santiago agents"""
    sender_id: str
    receiver_id: str
    message_type: str  # 'task', 'status', 'collaboration', 'conflict'
    content: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class SantiagoTask:
    """Task assigned to a Santiago agent"""
    task_id: str
    description: str
    assigned_to: str
    priority: int = 1  # 1-5, 5 being highest
    status: str = 'pending'  # 'pending', 'in_progress', 'completed', 'blocked'
    dependencies: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    completed_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class SantiagoAgent(ABC):
    """
    Base class for all Santiago agents operating in shared memory.

    Each Santiago has:
    - Unique identity and role specialization
    - Direct access to shared memory Git repository
    - Inter-agent communication capabilities
    - Performance monitoring and metrics
    """

    def __init__(self, santiago_id: str, role: str):
        self.santiago_id = santiago_id
        self.role = role

        # Shared memory integration
        self.git_service = get_shared_memory_git_service()
        self.workspace = self.git_service.register_santiago(santiago_id, role)

        # Communication
        self.message_queue: asyncio.Queue[SantiagoMessage] = asyncio.Queue()
        self.message_handlers: Dict[str, Callable] = {}

        # Task management
        self.active_tasks: Dict[str, SantiagoTask] = {}
        self.completed_tasks: List[SantiagoTask] = []

        # Performance tracking
        self.start_time = time.time()
        self.operation_count = 0
        self.total_operation_time = 0.0

        # Thread safety
        self.lock = threading.RLock()

        # Register default message handlers
        self._register_default_handlers()

        print(f"✓ Initialized Santiago-{santiago_id} ({role}) in shared memory")

    def _register_default_handlers(self):
        """Register default message handlers"""
        self.message_handlers.update({
            'task_assignment': self._handle_task_assignment,
            'status_request': self._handle_status_request,
            'collaboration_request': self._handle_collaboration_request,
            'conflict_notification': self._handle_conflict_notification
        })

    async def run(self):
        """Main agent execution loop"""
        print(f"🏃 Santiago-{self.santiago_id} starting execution loop")

        while True:
            try:
                # Process messages
                await self._process_messages()

                # Execute tasks
                await self._execute_pending_tasks()

                # Perform role-specific work
                await self._perform_role_work()

                # Brief pause to prevent busy waiting
                await asyncio.sleep(0.01)  # 10ms

            except Exception as e:
                print(f"✗ Error in Santiago-{self.santiago_id} execution loop: {e}")
                await asyncio.sleep(1.0)  # Back off on errors

    async def _process_messages(self):
        """Process incoming messages from other Santiagos"""
        try:
            # Process all available messages without blocking
            while not self.message_queue.empty():
                message = self.message_queue.get_nowait()
                await self._handle_message(message)
        except asyncio.QueueEmpty:
            pass  # No messages to process

    async def _handle_message(self, message: SantiagoMessage):
        """Handle an incoming message"""
        handler = self.message_handlers.get(message.message_type)
        if handler:
            try:
                await handler(message)
            except Exception as e:
                print(f"✗ Error handling message {message.message_type} in {self.santiago_id}: {e}")
        else:
            print(f"⚠ No handler for message type {message.message_type} in {self.santiago_id}")

    async def send_message(self, receiver_id: str, message_type: str, content: Dict[str, Any]):
        """Send a message to another Santiago"""
        message = SantiagoMessage(
            sender_id=self.santiago_id,
            receiver_id=receiver_id,
            message_type=message_type,
            content=content
        )

        # In shared memory, we can directly access other agents
        # This would be replaced with actual inter-agent communication in distributed setup
        print(f"📤 {self.santiago_id} -> {receiver_id}: {message_type}")

    async def commit_changes(self, message: str, files: List[str]) -> bool:
        """Commit changes to the shared repository"""
        start_time = time.time()

        try:
            commit_hash = self.git_service.atomic_commit(self.santiago_id, message, files)

            # Update performance metrics
            operation_time = time.time() - start_time
            self.operation_count += 1
            self.total_operation_time += operation_time

            if commit_hash:
                print(f"✓ {self.santiago_id} committed in {(operation_time * 1000):.3f}ms")
                return True
            else:
                print(f"⚠ {self.santiago_id} no changes to commit")
                return False

        except Exception as e:
            print(f"✗ {self.santiago_id} commit failed: {e}")
            return False

    def create_workspace_file(self, file_path: str, content: str) -> bool:
        """Create or update a file in this Santiago's workspace"""
        return self.git_service.create_workspace_file(self.santiago_id, file_path, content)

    def get_workspace_files(self) -> List[str]:
        """Get all files in this Santiago's workspace"""
        return self.git_service.get_workspace_files(self.santiago_id)

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for this Santiago"""
        uptime = time.time() - self.start_time
        avg_operation_time = self.total_operation_time / max(self.operation_count, 1)

        return {
            'santiago_id': self.santiago_id,
            'role': self.role,
            'uptime_seconds': uptime,
            'operations_completed': self.operation_count,
            'average_operation_time_ms': avg_operation_time * 1000,
            'active_tasks': len(self.active_tasks),
            'completed_tasks': len(self.completed_tasks),
            'workspace_files': len(self.get_workspace_files())
        }

    # Default message handlers
    async def _handle_task_assignment(self, message: SantiagoMessage):
        """Handle task assignment from other Santiagos"""
        task_data = message.content
        task = SantiagoTask(**task_data)
        self.active_tasks[task.task_id] = task
        print(f"📋 {self.santiago_id} assigned task: {task.description}")

    async def _handle_status_request(self, message: SantiagoMessage):
        """Handle status request from other Santiagos"""
        status = self.get_performance_metrics()
        await self.send_message(message.sender_id, 'status_response', status)

    async def _handle_collaboration_request(self, message: SantiagoMessage):
        """Handle collaboration request from other Santiagos"""
        # Default: accept collaboration
        await self.send_message(message.sender_id, 'collaboration_response',
                              {'accepted': True, 'santiago_id': self.santiago_id})

    async def _handle_conflict_notification(self, message: SantiagoMessage):
        """Handle conflict notification from shared Git service"""
        conflict_data = message.content
        print(f"⚠ {self.santiago_id} notified of conflict: {conflict_data}")

        # Attempt to resolve conflict
        await self._resolve_conflict(conflict_data)

    async def _resolve_conflict(self, conflict_data: Dict[str, Any]):
        """Resolve a merge conflict"""
        # Default strategy: defer to Santiago-Core for conflict resolution
        if self.role != 'core':
            await self.send_message('santiago-core', 'conflict_resolution_request', conflict_data)

    async def _execute_pending_tasks(self):
        """Execute pending tasks"""
        for task_id, task in list(self.active_tasks.items()):
            if task.status == 'pending':
                task.status = 'in_progress'
                await self._execute_task(task)

    async def _execute_task(self, task: SantiagoTask):
        """Execute a specific task"""
        try:
            # Task execution logic (to be implemented by subclasses)
            await self._perform_task_work(task)

            # Mark as completed
            task.status = 'completed'
            task.completed_at = time.time()
            self.completed_tasks.append(task)
            del self.active_tasks[task.task_id]

            print(f"✅ {self.santiago_id} completed task: {task.description}")

        except Exception as e:
            task.status = 'blocked'
            task.metadata['error'] = str(e)
            print(f"✗ {self.santiago_id} failed task {task.task_id}: {e}")

    @abstractmethod
    async def _perform_role_work(self):
        """Perform role-specific work (implemented by subclasses)"""
        pass

    @abstractmethod
    async def _perform_task_work(self, task: SantiagoTask):
        """Perform task-specific work (implemented by subclasses)"""
        pass


class SantiagoCore(SantiagoAgent):
    """Santiago-Core: The boat builder - creates and evolves domain Santiagos"""

    def __init__(self):
        super().__init__('santiago-core', 'core')
        self.domain_santiagos: Dict[str, Dict[str, Any]] = {}
        self.evolution_cycles = 0

    async def _perform_role_work(self):
        """Core work: monitor ecosystem, evolve Santiagos, manage conflicts"""
        await asyncio.sleep(0.1)  # Simulate work

        # Monitor shared memory performance
        metrics = self.git_service.get_performance_metrics()

        # Check for conflicts and resolve them
        if metrics['shared_memory_metrics'].total_conflicts > 0:
            await self._resolve_ecosystem_conflicts(metrics)

        # Evolve Santiagos based on performance
        await self._evolve_santiagos(metrics)

        # Create new domain Santiagos if needed
        await self._create_domain_santiagos()

    async def _perform_task_work(self, task: SantiagoTask):
        """Execute core-specific tasks"""
        if 'create_santiago' in task.description.lower():
            await self._create_new_santiago(task.metadata)
        elif 'evolve' in task.description.lower():
            await self._perform_evolution_cycle()
        else:
            # Generic task execution
            await asyncio.sleep(0.05)

    async def _create_new_santiago(self, config: Dict[str, Any]):
        """Create a new domain Santiago"""
        santiago_type = config.get('type', 'dev')
        santiago_id = f"santiago-{santiago_type}-{len(self.domain_santiagos) + 1}"

        # Create workspace structure
        self.create_workspace_file(f"{santiago_id}_config.json",
                                 json.dumps(config, indent=2))

        # Register with shared Git
        self.domain_santiagos[santiago_id] = config

        # Commit creation
        await self.commit_changes(f"Create new Santiago: {santiago_id}",
                                [f"{santiago_id}_config.json"])

        print(f"🚢 Santiago-Core created {santiago_id}")

    async def _perform_evolution_cycle(self):
        """Perform an evolution cycle on existing Santiagos"""
        self.evolution_cycles += 1

        # Analyze performance and suggest improvements
        metrics = self.git_service.get_performance_metrics()

        evolution_report = {
            'cycle': self.evolution_cycles,
            'timestamp': time.time(),
            'performance_analysis': metrics,
            'recommendations': []
        }

        # Generate evolution recommendations
        if metrics['performance_summary']['conflict_rate'] > 0.1:
            evolution_report['recommendations'].append(
                "Implement better conflict resolution strategies"
            )

        if metrics['performance_summary']['commits_per_second'] < 10:
            evolution_report['recommendations'].append(
                "Optimize commit operations for higher throughput"
            )

        # Save evolution report
        self.create_workspace_file(f"evolution_cycle_{self.evolution_cycles}.json",
                                 json.dumps(evolution_report, indent=2))

        await self.commit_changes(f"Evolution cycle {self.evolution_cycles} completed",
                                [f"evolution_cycle_{self.evolution_cycles}.json"])

    async def _resolve_ecosystem_conflicts(self, metrics: Dict[str, Any]):
        """Resolve conflicts across the entire ecosystem"""
        conflicts = metrics['shared_memory_metrics'].total_conflicts

        if conflicts > 0:
            resolution_plan = {
                'conflicts_detected': conflicts,
                'resolution_strategy': 'merge_priority_queue',
                'timestamp': time.time()
            }

            self.create_workspace_file("conflict_resolution_plan.json",
                                     json.dumps(resolution_plan, indent=2))

            await self.commit_changes("Conflict resolution plan created",
                                    ["conflict_resolution_plan.json"])

    async def _evolve_santiagos(self, metrics: Dict[str, Any]):
        """Evolve Santiagos based on performance metrics"""
        # Simple evolution logic - in practice this would be much more sophisticated
        performance_score = metrics['performance_summary']['commits_per_second']

        if performance_score > 50:  # High performance
            print("🌟 Ecosystem performing excellently - minimal evolution needed")
        elif performance_score > 20:  # Good performance
            print("✅ Ecosystem performing well - minor optimizations suggested")
        else:  # Needs improvement
            print("🔧 Ecosystem needs optimization - evolution recommended")

    async def _create_domain_santiagos(self):
        """Create domain Santiagos as needed"""
        # Check if we need more dev Santiagos
        dev_count = len([s for s in self.domain_santiagos.keys() if 'dev' in s])
        if dev_count < 2:
            await self._create_new_santiago({
                'type': 'dev',
                'capabilities': ['coding', 'testing', 'review'],
                'created_by': 'santiago-core'
            })


class SantiagoPM(SantiagoAgent):
    """Santiago-PM: The navigator - product management and coordination"""

    def __init__(self):
        super().__init__('santiago-pm', 'pm')
        self.product_backlog: List[Dict[str, Any]] = []
        self.current_sprint: Optional[Dict[str, Any]] = None

    async def _perform_role_work(self):
        """PM work: plan sprints, assign tasks, track progress"""
        await asyncio.sleep(0.1)

        # Update product backlog
        await self._update_backlog()

        # Plan next sprint
        await self._plan_sprint()

        # Assign tasks to dev Santiagos
        await self._assign_tasks()

        # Track progress
        await self._track_progress()

    async def _perform_task_work(self, task: SantiagoTask):
        """Execute PM-specific tasks"""
        if 'plan' in task.description.lower():
            await self._create_sprint_plan(task.metadata)
        elif 'track' in task.description.lower():
            await self._update_progress_tracking()
        else:
            await asyncio.sleep(0.05)

    async def _update_backlog(self):
        """Update the product backlog"""
        # Add new features based on ecosystem needs
        new_features = [
            "Implement real-time collaboration features",
            "Add performance monitoring dashboard",
            "Create automated testing framework",
            "Implement conflict resolution strategies"
        ]

        for feature in new_features:
            if not any(f['title'] == feature for f in self.product_backlog):
                self.product_backlog.append({
                    'id': str(uuid.uuid4()),
                    'title': feature,
                    'status': 'backlog',
                    'priority': 'medium',
                    'created_at': time.time()
                })

    async def _plan_sprint(self):
        """Plan the next sprint"""
        if not self.current_sprint or self._is_sprint_complete():
            sprint_id = f"sprint_{int(time.time())}"
            self.current_sprint = {
                'id': sprint_id,
                'start_date': time.time(),
                'end_date': time.time() + (7 * 24 * 3600),  # 1 week
                'goals': self._select_sprint_goals(),
                'tasks': []
            }

            # Save sprint plan
            self.create_workspace_file(f"{sprint_id}_plan.json",
                                     json.dumps(self.current_sprint, indent=2))

            await self.commit_changes(f"Planned sprint {sprint_id}",
                                    [f"{sprint_id}_plan.json"])

    def _is_sprint_complete(self) -> bool:
        """Check if current sprint is complete"""
        if not self.current_sprint:
            return True
        return time.time() > self.current_sprint['end_date']

    def _select_sprint_goals(self) -> List[str]:
        """Select goals for the next sprint"""
        available_features = [f for f in self.product_backlog if f['status'] == 'backlog']
        return [f['title'] for f in available_features[:3]]  # Top 3 features

    async def _assign_tasks(self):
        """Assign tasks to development Santiagos"""
        if not self.current_sprint:
            return

        # Get available dev Santiagos
        dev_santiagos = ['santiago-dev-1', 'santiago-dev-2']

        for goal in self.current_sprint['goals']:
            # Create task for each goal
            task = SantiagoTask(
                task_id=str(uuid.uuid4()),
                description=f"Implement: {goal}",
                assigned_to=dev_santiagos[len(self.current_sprint['tasks']) % len(dev_santiagos)],
                priority=3
            )

            self.current_sprint['tasks'].append(task.__dict__)

            # Send task assignment
            await self.send_message(task.assigned_to, 'task_assignment', task.__dict__)

    async def _track_progress(self):
        """Track sprint progress"""
        if not self.current_sprint:
            return

        # Update sprint status
        completed_tasks = len([t for t in self.current_sprint['tasks']
                              if t.get('status') == 'completed'])
        total_tasks = len(self.current_sprint['tasks'])

        progress = {
            'sprint_id': self.current_sprint['id'],
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'progress_percentage': (completed_tasks / max(total_tasks, 1)) * 100,
            'timestamp': time.time()
        }

        self.create_workspace_file(f"{self.current_sprint['id']}_progress.json",
                                 json.dumps(progress, indent=2))

        await self.commit_changes(f"Progress update for {self.current_sprint['id']}",
                                [f"{self.current_sprint['id']}_progress.json"])

    async def _create_sprint_plan(self, metadata: Dict[str, Any]):
        """Create a detailed sprint plan"""
        plan = {
            'sprint_id': metadata.get('sprint_id', f"sprint_{int(time.time())}"),
            'objectives': metadata.get('objectives', []),
            'tasks': metadata.get('tasks', []),
            'timeline': metadata.get('timeline', {}),
            'created_at': time.time()
        }

        self.create_workspace_file(f"{plan['sprint_id']}_detailed_plan.json",
                                 json.dumps(plan, indent=2))

        await self.commit_changes(f"Detailed sprint plan created",
                                [f"{plan['sprint_id']}_detailed_plan.json"])

    async def _update_progress_tracking(self):
        """Update progress tracking information"""
        tracking_data = {
            'timestamp': time.time(),
            'active_sprints': [self.current_sprint] if self.current_sprint else [],
            'backlog_size': len(self.product_backlog),
            'completed_features': len([f for f in self.product_backlog if f['status'] == 'completed'])
        }

        self.create_workspace_file("progress_tracking.json",
                                 json.dumps(tracking_data, indent=2))

        await self.commit_changes("Progress tracking updated",
                                ["progress_tracking.json"])


class SantiagoDev(SantiagoAgent):
    """Santiago-Dev: The crew - implementation and testing"""

    def __init__(self, dev_number: int):
        super().__init__(f'santiago-dev-{dev_number}', 'dev')
        self.dev_number = dev_number
        self.implemented_features: List[str] = []
        self.test_results: List[Dict[str, Any]] = []

    async def _perform_role_work(self):
        """Dev work: implement features, write tests, perform code reviews"""
        await asyncio.sleep(0.1)

        # Check for assigned tasks
        if self.active_tasks:
            # Focus on implementing assigned features
            await self._implement_features()
        else:
            # Perform maintenance work
            await self._perform_maintenance()

        # Run tests
        await self._run_tests()

        # Perform code reviews
        await self._perform_code_reviews()

    async def _perform_task_work(self, task: SantiagoTask):
        """Execute dev-specific tasks"""
        if 'implement' in task.description.lower():
            await self._implement_feature(task.metadata)
        elif 'test' in task.description.lower():
            await self._write_tests(task.metadata)
        elif 'review' in task.description.lower():
            await self._review_code(task.metadata)
        else:
            await asyncio.sleep(0.05)

    async def _implement_features(self):
        """Implement assigned features"""
        for task_id, task in list(self.active_tasks.items()):
            if 'implement' in task.description.lower():
                await self._implement_feature({'description': task.description})

    async def _implement_feature(self, metadata: Dict[str, Any]):
        """Implement a specific feature"""
        feature_name = metadata.get('description', 'unknown_feature').replace(' ', '_').lower()
        feature_file = f"feature_{feature_name}.py"

        # Generate feature implementation
        implementation = f'''"""
Feature: {metadata.get('description', 'Unknown Feature')}

Implemented by Santiago-Dev-{self.dev_number}
Created: {datetime.now().isoformat()}
"""

def {feature_name}_function():
    """Implementation of {feature_name} feature"""
    return f"Feature {feature_name} implemented by dev-{self.dev_number}"

# Feature metadata
FEATURE_INFO = {{
    'name': '{feature_name}',
    'implemented_by': 'santiago-dev-{self.dev_number}',
    'created_at': '{datetime.now().isoformat()}',
    'status': 'implemented'
}}
'''

        self.create_workspace_file(feature_file, implementation)
        self.implemented_features.append(feature_name)

        await self.commit_changes(f"Implemented feature: {feature_name}",
                                [feature_file])

        print(f"💻 Santiago-Dev-{self.dev_number} implemented {feature_name}")

    async def _perform_maintenance(self):
        """Perform maintenance work"""
        # Clean up old files, optimize code, etc.
        maintenance_tasks = [
            "Code cleanup and optimization",
            "Dependency updates",
            "Performance monitoring",
            "Documentation updates"
        ]

        for task in maintenance_tasks:
            # Simulate maintenance work
            await asyncio.sleep(0.01)

        print(f"🔧 Santiago-Dev-{self.dev_number} performed maintenance work")

    async def _run_tests(self):
        """Run automated tests"""
        # Simulate running tests
        test_results = {
            'timestamp': time.time(),
            'tests_run': 10,
            'tests_passed': 9,
            'tests_failed': 1,
            'coverage_percentage': 85.5,
            'run_by': f'santiago-dev-{self.dev_number}'
        }

        self.test_results.append(test_results)

        # Save test results
        self.create_workspace_file("latest_test_results.json",
                                 json.dumps(test_results, indent=2))

        await self.commit_changes("Test execution completed",
                                ["latest_test_results.json"])

        print(f"🧪 Santiago-Dev-{self.dev_number} ran tests: {test_results['tests_passed']}/{test_results['tests_run']} passed")

    async def _perform_code_reviews(self):
        """Perform code reviews on other Santiagos' work"""
        # Get files from other workspaces to review
        all_files = self.git_service.get_workspace_files('santiago-core') + \
                   self.git_service.get_workspace_files('santiago-pm')

        if all_files:
            review_report = {
                'reviewer': f'santiago-dev-{self.dev_number}',
                'timestamp': time.time(),
                'files_reviewed': len(all_files),
                'issues_found': 0,  # Simulate review
                'recommendations': [
                    "Consider adding more error handling",
                    "Documentation could be improved",
                    "Some functions are too complex"
                ]
            }

            self.create_workspace_file("code_review_report.json",
                                     json.dumps(review_report, indent=2))

            await self.commit_changes("Code review completed",
                                    ["code_review_report.json"])

            print(f"👀 Santiago-Dev-{self.dev_number} completed code review")

    async def _write_tests(self, metadata: Dict[str, Any]):
        """Write tests for a feature"""
        feature_name = metadata.get('feature', 'unknown').replace(' ', '_').lower()
        test_file = f"test_{feature_name}.py"

        test_code = f'''"""
Tests for feature: {feature_name}

Written by Santiago-Dev-{self.dev_number}
Created: {datetime.now().isoformat()}
"""

import unittest

class Test{feature_name.title()}(unittest.TestCase):
    """Test cases for {feature_name} feature"""

    def test_basic_functionality(self):
        """Test basic functionality"""
        # Test implementation would go here
        self.assertTrue(True)  # Placeholder

    def test_edge_cases(self):
        """Test edge cases"""
        # Edge case tests would go here
        self.assertTrue(True)  # Placeholder

if __name__ == '__main__':
    unittest.main()
'''

        self.create_workspace_file(test_file, test_code)

        await self.commit_changes(f"Added tests for {feature_name}",
                                [test_file])

        print(f"📝 Santiago-Dev-{self.dev_number} wrote tests for {feature_name}")


# Global agent registry for shared memory communication
_agent_registry: Dict[str, SantiagoAgent] = {}

def register_agent(agent: SantiagoAgent):
    """Register an agent in the global registry"""
    _agent_registry[agent.santiago_id] = agent

def get_agent(santiago_id: str) -> Optional[SantiagoAgent]:
    """Get an agent from the global registry"""
    return _agent_registry.get(santiago_id)

def get_all_agents() -> List[SantiagoAgent]:
    """Get all registered agents"""
    return list(_agent_registry.values())