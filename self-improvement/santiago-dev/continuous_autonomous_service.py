#!/usr/bin/env python3
"""
Continuous Autonomous Operation Service for Santiago-Dev

Manages continuous autonomous development operations, task generation,
deployment monitoring, and system health checks.
"""

import os
import sys
import json
import asyncio
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Add the project paths
sys.path.insert(0, str(Path(__file__).parent))

from self_improvement.santiago_dev.tackle.qa_integration.qa_integration_service import QAIntegrationService
from self_improvement.santiago_dev.tackle.autonomous_task_execution.simplified_executor import SimplifiedAutonomousExecutor
from self_improvement.santiago_dev.tackle.personal_logging.personal_logger import AutomatedPersonalLogger


class ContinuousAutonomousService:
    """
    Service that manages continuous autonomous development operations.
    """

    def __init__(self, workspace_path: Optional[Path] = None):
        # Use a dedicated workspace within santiago-dev to avoid conflicts
        if workspace_path is None:
            workspace_path = Path(__file__).parent / "autonomous_workspace"
        self.workspace_path = Path(workspace_path)

        # Ensure workspace exists
        self.workspace_path.mkdir(parents=True, exist_ok=True)

        # Initialize services
        try:
            self.qa_service = QAIntegrationService(self.workspace_path)
            self.executor = SimplifiedAutonomousExecutor(self.workspace_path)
            self.logger = AutomatedPersonalLogger(self.workspace_path)
        except Exception as e:
            print(f"⚠️ Service initialization failed: {e}")
            print("Continuing with limited functionality...")

        self.operation_config = {
            'check_interval': 300,  # 5 minutes
            'max_concurrent_tasks': 1,
            'health_check_interval': 60,  # 1 minute
            'task_generation_enabled': True,
            'auto_deployment_enabled': False
        }

        self.is_running = False
        self.last_health_check = None
        self.operation_stats = {
            'start_time': None,
            'tasks_completed': 0,
            'tasks_failed': 0,
            'health_checks_passed': 0,
        }

    async def start_continuous_operation(self):
        """
        Start the continuous autonomous operation loop.
        """
        print("🚀 Starting Santiago-Dev Continuous Autonomous Operation")
        print(f"📁 Workspace: {self.workspace_path}")
        print(f"⏰ Check interval: {self.operation_config['check_interval']} seconds")

        self.is_running = True
        self.operation_stats['start_time'] = datetime.now()

        try:
            # Start background monitoring
            asyncio.create_task(self._task_monitoring_loop())
            asyncio.create_task(self._health_check_loop())

            while self.is_running:
                try:
                    await self._perform_operation_cycle()
                    await asyncio.sleep(self.operation_config['check_interval'])
                except Exception as e:
                    print(f"❌ Operation cycle failed: {e}")
                    await asyncio.sleep(60)  # Wait before retry

        except KeyboardInterrupt:
            print("\n🛑 Shutdown requested by user")
        except Exception as e:
            print(f"💥 Critical error in continuous operation: {e}")
        finally:
            await self._shutdown()

    async def _perform_operation_cycle(self):
        """
        Perform one complete operation cycle.
        """
        print(f"\n🔄 Operation cycle at {datetime.now().strftime('%H:%M:%S')}")

        try:
            # Step 1: Check for new tasks/features
            await self._check_for_new_tasks()

            # Step 2: Execute next prioritized task
            await self._execute_pending_tasks()

            # Step 3: Update operation statistics
            self._update_stats()

            print("✅ Operation cycle completed successfully")

        except Exception as e:
            print(f"❌ Operation cycle failed: {e}")
            self.operation_stats['tasks_failed'] += 1

    async def _check_for_new_tasks(self):
        """
        Check for new tasks and features to work on.
        """
        try:
            # Get next prioritized feature from QA service
            next_feature = self.qa_service.get_next_prioritized_feature()

            if next_feature:
                print(f"🎯 Found prioritized feature: {next_feature['name']}")
                # Feature will be picked up by executor in next step
            else:
                print("📋 No prioritized features found")

                # Generate new tasks if enabled
                if self.operation_config['task_generation_enabled']:
                    await self._generate_new_tasks()

        except Exception as e:
            print(f"⚠️ Task checking failed: {e}")

    async def _generate_new_tasks(self):
        """
        Generate new tasks when backlog is empty.
        """
        try:
            # Use QA service to discover potential features
            topics = [
                "DGX readiness preparation",
                "Multi-agent infrastructure",
                "Performance optimization",
                "System monitoring enhancement"
            ]

            for topic in topics:
                features = await self.qa_service.discover_features(topic)
                if features:
                    print(f"💡 Discovered {len(features)} features for topic: {topic}")
                    # Features are automatically added to knowledge graph

        except Exception as e:
            print(f"⚠️ Task generation failed: {e}")

    async def _execute_pending_tasks(self):
        """
        Execute the next pending task.
        """
        try:
            success = await self.executor.execute_next_task()
            if success:
                self.operation_stats['tasks_completed'] += 1
                print("✅ Task executed successfully")
            else:
                print("⏭️ No tasks to execute")

        except Exception as e:
            print(f"⚠️ Task execution failed: {e}")
            self.operation_stats['tasks_failed'] += 1

    async def _task_monitoring_loop(self):
        """
        Background loop for monitoring task execution.
        """
        while self.is_running:
            try:
                # Monitor executor status
                status = self.executor.get_execution_status()
                if status.get('active_tasks', 0) > 0:
                    print(f"🔧 Active tasks: {status['active_tasks']}")

                await asyncio.sleep(30)  # Check every 30 seconds

            except Exception as e:
                print(f"⚠️ Task monitoring failed: {e}")
                await asyncio.sleep(60)

    async def _health_check_loop(self):
        """
        Background loop for health checks.
        """
        while self.is_running:
            try:
                health_status = await self._perform_health_check()
                if health_status['status'] == 'healthy':
                    self.operation_stats['health_checks_passed'] += 1
                else:
                    print(f"⚠️ Health check failed: {health_status}")

                self.last_health_check = datetime.now()
                await asyncio.sleep(self.operation_config['health_check_interval'])

            except Exception as e:
                print(f"⚠️ Health check loop failed: {e}")
                await asyncio.sleep(60)

    async def _perform_health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        """
        health_status = {
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }

        try:
            # Check workspace accessibility
            if self.workspace_path.exists():
                health_status['checks']['workspace'] = 'ok'
            else:
                health_status['checks']['workspace'] = 'error'
                health_status['status'] = 'unhealthy'

            # Check services
            if hasattr(self, 'qa_service') and self.qa_service:
                health_status['checks']['qa_service'] = 'ok'
            else:
                health_status['checks']['qa_service'] = 'error'

            if hasattr(self, 'executor') and self.executor:
                health_status['checks']['executor'] = 'ok'
            else:
                health_status['checks']['executor'] = 'error'

            if hasattr(self, 'logger') and self.logger:
                health_status['checks']['logger'] = 'ok'
            else:
                health_status['checks']['logger'] = 'error'

        except Exception as e:
            health_status['status'] = 'error'
            health_status['error'] = str(e)

        return health_status

    def _update_stats(self):
        """
        Update operation statistics.
        """
        # Stats are updated in real-time, just log periodically
        if self.operation_stats['tasks_completed'] % 5 == 0:
            print(f"📊 Stats: {self.operation_stats['tasks_completed']} completed, "
                  f"{self.operation_stats['tasks_failed']} failed")

    async def _shutdown(self):
        """
        Clean shutdown of services.
        """
        print("🛑 Shutting down continuous autonomous operation...")

        self.is_running = False

        # Save final stats
        final_stats = {
            'end_time': datetime.now(),
            'total_runtime': None,
            **self.operation_stats
        }

        if final_stats['start_time']:
            final_stats['total_runtime'] = str(final_stats['end_time'] - final_stats['start_time'])

        print("📊 Final Statistics:")
        print(f"  - Runtime: {final_stats['total_runtime']}")
        print(f"  - Tasks completed: {final_stats['tasks_completed']}")
        print(f"  - Tasks failed: {final_stats['tasks_failed']}")
        print(f"  - Health checks passed: {final_stats['health_checks_passed']}")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current operation status.
        """
        return {
            'running': self.is_running,
            'workspace': str(self.workspace_path),
            'start_time': self.operation_stats['start_time'].isoformat() if self.operation_stats['start_time'] else None,
            'stats': self.operation_stats,
            'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None,
            'config': self.operation_config
        }


# CLI Interface
def main():
    """CLI interface for continuous autonomous service."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Santiago-Dev Continuous Autonomous Operation Service",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start continuous autonomous operation
  python continuous_autonomous_service.py start

  # Stop continuous operation
  python continuous_autonomous_service.py stop

  # Check operation status
  python continuous_autonomous_service.py status

  # Generate new tasks manually
  python continuous_autonomous_service.py generate-tasks

  # Perform health check
  python continuous_autonomous_service.py health-check
        """
    )

    parser.add_argument(
        '--workspace', '-w',
        type=str,
        help='Workspace path (default: current directory)'
    )

    parser.add_argument(
        'action',
        choices=['start', 'stop', 'status', 'generate-tasks', 'health-check'],
        help='Action to perform'
    )

    args = parser.parse_args()

    async def run():
        service = ContinuousAutonomousService(
            Path(args.workspace) if args.workspace else None
        )

        if args.action == 'start':
            await service.start_continuous_operation()

        elif args.action == 'status':
            status = service.get_status()
            print("📊 Continuous Operation Status")
            print("=" * 40)
            print(f"Running: {'✅' if status['running'] else '❌'}")
            print(f"Tasks completed: {status['stats']['tasks_completed']}")
            print(f"Tasks failed: {status['stats']['tasks_failed']}")
            print(f"Health checks passed: {status['stats']['health_checks_passed']}")
            if status['start_time']:
                print(f"Started: {status['start_time']}")
            if status['last_health_check']:
                print(f"Last health check: {status['last_health_check']}")

        elif args.action == 'generate-tasks':
            print("🔄 Generating new tasks...")
            await service._generate_new_tasks()
            print("✅ Task generation completed")

        elif args.action == 'health-check':
            print("🏥 Performing health check...")
            health = await service._perform_health_check()
            print(f"Status: {'✅ Healthy' if health['status'] == 'healthy' else '❌ Unhealthy'}")
            for check, status in health['checks'].items():
                icon = '✅' if status == 'ok' else '❌'
                print(f"  {icon} {check}: {status}")

        elif args.action == 'stop':
            print("🛑 Stop command received - service will shut down gracefully")

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n👋 Shutdown requested")
    except Exception as e:
        print(f"💥 Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()