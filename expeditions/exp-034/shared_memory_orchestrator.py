"""
EXP-034: Multi-Santiago Shared Memory Orchestrator

Orchestrates multiple Santiago agents operating in shared memory space,
demonstrating the performance benefits of collaborative AI development
without traditional disk I/O and network communication bottlenecks.

This experiment shows how Santiago agents can work together seamlessly
when operating in the same memory space with instant Git operations.
"""

import asyncio
import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import statistics

from shared_memory_git_service import get_shared_memory_git_service
from santiago_agents import (
    SantiagoCore, SantiagoPM, SantiagoDev,
    register_agent, get_agent, get_all_agents
)


@dataclass
class ExperimentMetrics:
    """Metrics collected during the shared memory experiment"""
    experiment_start: float = field(default_factory=time.time)
    experiment_duration: float = 0.0
    total_commits: int = 0
    total_merges: int = 0
    total_conflicts: int = 0
    average_commit_time_ms: float = 0.0
    average_merge_time_ms: float = 0.0
    inter_agent_messages: int = 0
    tasks_completed: int = 0
    features_implemented: int = 0
    tests_run: int = 0
    code_reviews_completed: int = 0
    memory_usage_mb: float = 0.0
    performance_samples: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SantiagoInstance:
    """Represents a running Santiago instance"""
    agent: Any
    task: Optional[asyncio.Task] = None
    start_time: float = field(default_factory=time.time)
    status: str = 'initializing'


class SharedMemoryOrchestrator:
    """
    Orchestrates the multi-Santiago shared memory experiment.

    Creates and manages Santiago-Core, Santiago-PM, and multiple Santiago-Dev
    instances, all operating within the same memory space with instant
    Git operations and direct inter-agent communication.
    """

    def __init__(self):
        self.git_service = get_shared_memory_git_service()
        self.metrics = ExperimentMetrics()

        # Santiago instances
        self.santiagos: Dict[str, SantiagoInstance] = {}
        self.orchestration_task: Optional[asyncio.Task] = None

        # Experiment control
        self.running = False
        self.experiment_duration_seconds = 300  # 5 minutes default
        self.performance_monitoring = True

        print("🎯 Initialized Shared Memory Santiago Orchestrator")

    async def initialize_ecosystem(self):
        """Initialize the complete Santiago ecosystem"""
        print("🏗️  Initializing Santiago ecosystem...")

        # Create Santiago-Core (the boat builder)
        core_agent = SantiagoCore()
        register_agent(core_agent)
        self.santiagos['santiago-core'] = SantiagoInstance(
            agent=core_agent,
            status='ready'
        )

        # Create Santiago-PM (the navigator)
        pm_agent = SantiagoPM()
        register_agent(pm_agent)
        self.santiagos['santiago-pm'] = SantiagoInstance(
            agent=pm_agent,
            status='ready'
        )

        # Create Santiago-Dev instances (the crew)
        for i in range(1, 3):  # Two dev Santiagos
            dev_agent = SantiagoDev(i)
            register_agent(dev_agent)
            self.santiagos[f'santiago-dev-{i}'] = SantiagoInstance(
                agent=dev_agent,
                status='ready'
            )

        print(f"✅ Initialized {len(self.santiagos)} Santiago agents in shared memory")

        # Save ecosystem configuration
        ecosystem_config = {
            'initialized_at': time.time(),
            'santiagos': list(self.santiagos.keys()),
            'shared_memory_enabled': True,
            'experiment_id': 'exp-034-multi-santiago-shared-memory-git'
        }

        # Commit initial configuration
        core_agent.create_workspace_file('ecosystem_config.json',
                                       json.dumps(ecosystem_config, indent=2))
        await core_agent.commit_changes("Initialize Santiago ecosystem",
                                      ['ecosystem_config.json'])

    async def start_experiment(self, duration_seconds: int = 300):
        """Start the shared memory collaboration experiment"""
        self.experiment_duration_seconds = duration_seconds
        self.running = True

        print(f"🚀 Starting EXP-034: Multi-Santiago Shared Memory Experiment")
        print(f"   Duration: {duration_seconds} seconds")
        print(f"   Santiagos: {len(self.santiagos)}")

        # Start all Santiago agents
        for santiago_id, instance in self.santiagos.items():
            instance.task = asyncio.create_task(self._run_santiago_agent(instance))
            instance.status = 'running'
            print(f"   ▶️  Started {santiago_id}")

        # Start orchestration
        self.orchestration_task = asyncio.create_task(self._orchestrate_experiment())

        # Start performance monitoring
        if self.performance_monitoring:
            asyncio.create_task(self._monitor_performance())

        print("🎬 Experiment running...")

    async def stop_experiment(self):
        """Stop the experiment and collect final metrics"""
        print("🛑 Stopping experiment...")
        self.running = False

        # Stop all Santiago tasks
        for santiago_id, instance in self.santiagos.items():
            if instance.task and not instance.task.done():
                instance.task.cancel()
                instance.status = 'stopped'

        # Stop orchestration
        if self.orchestration_task and not self.orchestration_task.done():
            self.orchestration_task.cancel()

        # Collect final metrics
        await self._collect_final_metrics()

        print("✅ Experiment completed")

    async def _run_santiago_agent(self, instance: SantiagoInstance):
        """Run a Santiago agent with error handling"""
        try:
            await instance.agent.run()
        except asyncio.CancelledError:
            print(f"🛑 {instance.agent.santiago_id} cancelled")
        except Exception as e:
            print(f"✗ Error in {instance.agent.santiago_id}: {e}")
            instance.status = 'error'

    async def _orchestrate_experiment(self):
        """Main orchestration loop"""
        start_time = time.time()
        last_metrics_collection = start_time

        while self.running and (time.time() - start_time) < self.experiment_duration_seconds:
            try:
                current_time = time.time()

                # Periodic coordination (every 10 seconds)
                if current_time - last_metrics_collection >= 10:
                    await self._coordinate_santiagos()
                    last_metrics_collection = current_time

                # Check for conflicts and resolve them
                await self._handle_conflicts()

                # Brief pause
                await asyncio.sleep(1.0)

            except Exception as e:
                print(f"✗ Orchestration error: {e}")
                await asyncio.sleep(5.0)

        # Experiment duration reached
        await self.stop_experiment()

    async def _coordinate_santiagos(self):
        """Coordinate activities between Santiagos"""
        # Get status from all Santiagos
        status_updates = {}
        for santiago_id, instance in self.santiagos.items():
            try:
                metrics = instance.agent.get_performance_metrics()
                status_updates[santiago_id] = metrics
            except Exception as e:
                print(f"✗ Failed to get status from {santiago_id}: {e}")

        # Santiago-Core coordinates overall strategy
        core_agent = self.santiagos['santiago-core'].agent
        coordination_data = {
            'timestamp': time.time(),
            'santiago_status': status_updates,
            'active_tasks': sum(s['active_tasks'] for s in status_updates.values()),
            'completed_tasks': sum(s['completed_tasks'] for s in status_updates.values())
        }

        core_agent.create_workspace_file('coordination_status.json',
                                       json.dumps(coordination_data, indent=2))
        await core_agent.commit_changes("Coordination status update",
                                      ['coordination_status.json'])

    async def _handle_conflicts(self):
        """Detect and handle conflicts in the shared repository"""
        git_metrics = self.git_service.get_performance_metrics()
        conflicts = git_metrics['shared_memory_metrics'].total_conflicts

        if conflicts > 0:
            # Notify Santiago-Core of conflicts
            core_agent = self.santiagos['santiago-core'].agent

            conflict_report = {
                'conflicts_detected': conflicts,
                'timestamp': time.time(),
                'resolution_strategy': 'shared_memory_merge',
                'affected_santiagos': list(self.santiagos.keys())
            }

            core_agent.create_workspace_file('conflict_report.json',
                                           json.dumps(conflict_report, indent=2))
            await core_agent.commit_changes("Conflict detected and reported",
                                          ['conflict_report.json'])

            print(f"⚠ Detected {conflicts} conflicts - Santiago-Core notified")

    async def _monitor_performance(self):
        """Monitor performance throughout the experiment"""
        while self.running:
            try:
                # Collect performance sample
                sample_time = time.time()
                git_metrics = self.git_service.get_performance_metrics()

                sample = {
                    'timestamp': sample_time,
                    'experiment_time_seconds': sample_time - self.metrics.experiment_start,
                    'git_metrics': git_metrics,
                    'santiago_metrics': {}
                }

                # Collect metrics from each Santiago
                for santiago_id, instance in self.santiagos.items():
                    try:
                        santiago_metrics = instance.agent.get_performance_metrics()
                        sample['santiago_metrics'][santiago_id] = santiago_metrics
                    except Exception as e:
                        print(f"✗ Failed to collect metrics from {santiago_id}: {e}")

                self.metrics.performance_samples.append(sample)

                # Update running totals
                self.metrics.total_commits = git_metrics['shared_memory_metrics'].total_commits
                self.metrics.total_merges = git_metrics['shared_memory_metrics'].total_merges
                self.metrics.total_conflicts = git_metrics['shared_memory_metrics'].total_conflicts
                self.metrics.memory_usage_mb = git_metrics['shared_memory_metrics'].memory_usage_mb

                # Brief pause between samples
                await asyncio.sleep(5.0)  # Sample every 5 seconds

            except Exception as e:
                print(f"✗ Performance monitoring error: {e}")
                await asyncio.sleep(10.0)

    async def _collect_final_metrics(self):
        """Collect and save final experiment metrics"""
        end_time = time.time()
        self.metrics.experiment_duration = end_time - self.metrics.experiment_start

        # Calculate averages
        if self.metrics.performance_samples:
            commit_times = [s['git_metrics']['shared_memory_metrics'].average_commit_time_ms
                          for s in self.metrics.performance_samples if s['git_metrics']['shared_memory_metrics'].average_commit_time_ms > 0]
            if commit_times:
                self.metrics.average_commit_time_ms = statistics.mean(commit_times)

            merge_times = [s['git_metrics']['shared_memory_metrics'].average_merge_time_ms
                         for s in self.metrics.performance_samples if s['git_metrics']['shared_memory_metrics'].average_merge_time_ms > 0]
            if merge_times:
                self.metrics.average_merge_time_ms = statistics.mean(merge_times)

        # Collect final Santiago metrics
        final_santiago_metrics = {}
        total_tasks_completed = 0
        total_features_implemented = 0
        total_tests_run = 0
        total_reviews_completed = 0

        for santiago_id, instance in self.santiagos.items():
            try:
                metrics = instance.agent.get_performance_metrics()
                final_santiago_metrics[santiago_id] = metrics

                # Aggregate metrics
                total_tasks_completed += metrics.get('completed_tasks', 0)

                # Role-specific metrics
                if 'dev' in santiago_id:
                    # Estimate features/tests/reviews from workspace files
                    workspace_files = instance.agent.get_workspace_files()
                    total_features_implemented += len([f for f in workspace_files if f.startswith('feature_')])
                    total_tests_run += len([f for f in workspace_files if f.startswith('test_')])
                    total_reviews_completed += len([f for f in workspace_files if 'review' in f])

            except Exception as e:
                print(f"✗ Failed to collect final metrics from {santiago_id}: {e}")

        # Update metrics
        self.metrics.tasks_completed = total_tasks_completed
        self.metrics.features_implemented = total_features_implemented
        self.metrics.tests_run = total_tests_run
        self.metrics.code_reviews_completed = total_reviews_completed

        # Create final report
        final_report = {
            'experiment': 'EXP-034: Multi-Santiago Shared Memory Git',
            'duration_seconds': self.metrics.experiment_duration,
            'santiagos_participating': len(self.santiagos),
            'performance_metrics': {
                'total_commits': self.metrics.total_commits,
                'total_merges': self.metrics.total_merges,
                'total_conflicts': self.metrics.total_conflicts,
                'average_commit_time_ms': self.metrics.average_commit_time_ms,
                'average_merge_time_ms': self.metrics.average_merge_time_ms,
                'peak_memory_usage_mb': self.metrics.memory_usage_mb,
                'commits_per_second': self.metrics.total_commits / max(self.metrics.experiment_duration, 1)
            },
            'productivity_metrics': {
                'tasks_completed': self.metrics.tasks_completed,
                'features_implemented': self.metrics.features_implemented,
                'tests_run': self.metrics.tests_run,
                'code_reviews_completed': self.metrics.code_reviews_completed,
                'tasks_per_second': self.metrics.tasks_completed / max(self.metrics.experiment_duration, 1)
            },
            'final_santiago_metrics': final_santiago_metrics,
            'performance_samples_count': len(self.metrics.performance_samples),
            'experiment_completed_at': end_time
        }

        # Save final report to shared repository
        core_agent = self.santiagos['santiago-core'].agent
        core_agent.create_workspace_file('exp_034_final_report.json',
                                       json.dumps(final_report, indent=2))
        await core_agent.commit_changes("EXP-034 Final Report: Shared Memory Santiago Orchestration",
                                      ['exp_034_final_report.json'])

        print("📊 Final experiment report saved to shared repository")
        print(f"   Duration: {self.metrics.experiment_duration:.1f} seconds")
        print(f"   Commits: {self.metrics.total_commits}")
        print(f"   Tasks Completed: {self.metrics.tasks_completed}")
        print(f"   Features Implemented: {self.metrics.features_implemented}")

    def get_experiment_status(self) -> Dict[str, Any]:
        """Get current experiment status"""
        elapsed = time.time() - self.metrics.experiment_start

        return {
            'running': self.running,
            'elapsed_seconds': elapsed,
            'remaining_seconds': max(0, self.experiment_duration_seconds - elapsed),
            'santiagos': {
                sid: {
                    'status': instance.status,
                    'uptime': time.time() - instance.start_time,
                    'metrics': instance.agent.get_performance_metrics() if hasattr(instance.agent, 'get_performance_metrics') else {}
                }
                for sid, instance in self.santiagos.items()
            },
            'git_metrics': self.git_service.get_performance_metrics(),
            'experiment_metrics': {
                'total_commits': self.metrics.total_commits,
                'total_merges': self.metrics.total_merges,
                'total_conflicts': self.metrics.total_conflicts,
                'tasks_completed': self.metrics.tasks_completed
            }
        }


async def run_shared_memory_experiment(duration_seconds: int = 300):
    """
    Run the complete EXP-034 shared memory Santiago experiment

    Args:
        duration_seconds: How long to run the experiment
    """
    print("🌊 EXP-034: Multi-Santiago Shared Memory Git Orchestration")
    print("=" * 60)

    # Create orchestrator
    orchestrator = SharedMemoryOrchestrator()

    try:
        # Initialize ecosystem
        await orchestrator.initialize_ecosystem()

        # Start experiment
        await orchestrator.start_experiment(duration_seconds)

        # Wait for completion
        while orchestrator.running:
            status = orchestrator.get_experiment_status()
            print(f"⏱️  Experiment running: {status['elapsed_seconds']:.1f}s elapsed, "
                  f"{status['remaining_seconds']:.1f}s remaining")
            print(f"   Commits: {status['experiment_metrics']['total_commits']}, "
                  f"Tasks: {status['experiment_metrics']['tasks_completed']}")

            # Show Santiago status
            for sid, santiago_status in status['santiagos'].items():
                metrics = santiago_status['metrics']
                print(f"   {sid}: {santiago_status['status']} "
                      f"({metrics.get('operations_completed', 0)} ops, "
                      f"{metrics.get('completed_tasks', 0)} tasks)")

            await asyncio.sleep(30)  # Status update every 30 seconds

    except KeyboardInterrupt:
        print("\n🛑 Experiment interrupted by user")
        await orchestrator.stop_experiment()

    except Exception as e:
        print(f"✗ Experiment failed: {e}")
        await orchestrator.stop_experiment()

    print("\n🎯 EXP-034 Complete!")
    print("Check the shared repository for detailed results and performance metrics.")


if __name__ == "__main__":
    # Run the experiment for 5 minutes
    asyncio.run(run_shared_memory_experiment(duration_seconds=300))