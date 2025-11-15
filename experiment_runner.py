#!/usr/bin/env python3
"""
Autonomous Multi-Agent Experiment Runner

This script executes the autonomous multi-agent swarm experiment according to the
usability test framework. It runs without human intervention until completion,
queuing decisions that require human input.

Usage:
    python experiment_runner.py [--config CONFIG_FILE] [--dry-run]

Options:
    --config CONFIG_FILE    Path to experiment configuration file (default: config/experiment.json)
    --dry-run              Run in simulation mode without actual agent execution
"""

import asyncio
import json
import logging
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nusy_pm_core.models.experiment import ExperimentConfig, ExperimentPhase, DecisionQueue
from nusy_pm_core.services.experiment_runner import ExperimentRunnerService
from nusy_pm_core.adapters.agent_adapter import AgentAdapter
from nusy_pm_core.adapters.knowledge_adapter import KnowledgeAdapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/experiment_runner.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class AutonomousExperimentRunner:
    """Main runner for the autonomous multi-agent experiment."""

    def __init__(self, config_path: str = "config/experiment.json", dry_run: bool = False):
        self.config_path = Path(config_path)
        self.dry_run = dry_run
        self.config: Optional[ExperimentConfig] = None
        self.runner_service: Optional[ExperimentRunnerService] = None
        self.decision_queue: DecisionQueue = DecisionQueue()
        self.start_time: Optional[datetime] = None
        self.current_phase: Optional[ExperimentPhase] = None

        # Create necessary directories
        self._setup_directories()

    def _setup_directories(self):
        """Create required directories for the experiment."""
        dirs = ["logs", "data", "reports", "config"]
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)

    async def initialize(self) -> bool:
        """Initialize the experiment runner and validate configuration."""
        try:
            logger.info("Initializing autonomous experiment runner...")

            # Load configuration
            if not self.config_path.exists():
                await self._create_default_config()

            with open(self.config_path, 'r') as f:
                config_data = json.load(f)

            self.config = ExperimentConfig(**config_data)

            # Initialize services
            self.runner_service = ExperimentRunnerService(
                config=self.config,
                decision_queue=self.decision_queue
            )

            # Validate agent availability
            agent_adapter = AgentAdapter()
            available_agents = await agent_adapter.list_available_agents()

            required_agents = ["quartermaster", "pilot", "santiago"]
            missing_agents = [agent for agent in required_agents if agent not in available_agents]

            if missing_agents:
                logger.error(f"Missing required agents: {missing_agents}")
                await self._queue_decision(
                    "missing_agents",
                    f"Required agents not available: {missing_agents}",
                    ["Implement missing agents", "Modify experiment to use available agents"],
                    priority="high"
                )
                return False

            logger.info("Experiment runner initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize experiment runner: {e}")
            return False

    async def _create_default_config(self):
        """Create a default experiment configuration."""
        logger.info("Creating default experiment configuration...")

        default_config = {
            "experiment_name": "autonomous-multi-agent-swarm",
            "duration_days": 21,
            "phases": [
                {
                    "name": "bootstrapping",
                    "duration_days": 3,
                    "behaviors": ["agent_initialization", "communication_setup"],
                    "success_metrics": ["agent_startup_time", "communication_latency"]
                },
                {
                    "name": "knowledge_loading",
                    "duration_days": 4,
                    "behaviors": ["source_ingestion", "knowledge_validation"],
                    "success_metrics": ["ingestion_success_rate", "knowledge_integrity"]
                },
                {
                    "name": "autonomous_development",
                    "duration_days": 7,
                    "behaviors": ["feature_proposal", "implementation", "testing"],
                    "success_metrics": ["feature_velocity", "test_pass_rate"]
                },
                {
                    "name": "self_evaluation",
                    "duration_days": 7,
                    "behaviors": ["performance_analysis", "improvement_proposal"],
                    "success_metrics": ["analysis_completeness", "learning_rate"]
                }
            ],
            "decision_triggers": [
                "ethical_dilemmas",
                "architecture_changes",
                "resource_limits",
                "test_failures",
                "innovation_opportunities"
            ],
            "success_criteria": {
                "autonomy_level": 0.8,
                "feature_velocity": 0.5,
                "quality_maintenance": 0.9
            }
        }

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)

    async def run_experiment(self) -> bool:
        """Execute the autonomous experiment."""
        if not self.config or not self.runner_service:
            logger.error("Experiment not properly initialized")
            return False

        self.start_time = datetime.now()
        logger.info(f"Starting autonomous experiment: {self.config.experiment_name}")
        logger.info(f"Duration: {self.config.duration_days} days")
        logger.info(f"Dry run mode: {self.dry_run}")

        try:
            # Execute each phase
            for phase in self.config.phases:
                self.current_phase = phase
                logger.info(f"Starting phase: {phase.name}")

                success = await self._execute_phase(phase)
                if not success:
                    logger.error(f"Phase {phase.name} failed")
                    await self._handle_phase_failure(phase)
                    return False

                # Check for pending decisions
                await self._process_decision_queue()

            # Generate final assessment
            await self._generate_final_assessment()

            logger.info("Experiment completed successfully")
            return True

        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            await self._handle_experiment_failure(e)
            return False

    async def _execute_phase(self, phase: ExperimentPhase) -> bool:
        """Execute a single experiment phase."""
        phase_start = datetime.now()

        try:
            if self.dry_run:
                # Simulate phase execution
                await asyncio.sleep(1)  # Simulate work
                logger.info(f"Simulated execution of phase: {phase.name}")
                return True

            # Execute actual phase behaviors
            for behavior in phase.behaviors:
                logger.info(f"Executing behavior: {behavior}")
                success = await self.runner_service.execute_behavior(behavior)

                if not success:
                    logger.error(f"Behavior {behavior} failed")
                    return False

            # Validate success metrics
            metrics_valid = await self._validate_phase_metrics(phase)
            if not metrics_valid:
                logger.error(f"Phase {phase.name} metrics validation failed")
                return False

            phase_duration = datetime.now() - phase_start
            logger.info(f"Phase {phase.name} completed in {phase_duration}")
            return True

        except Exception as e:
            logger.error(f"Phase {phase.name} execution failed: {e}")
            return False

    async def _validate_phase_metrics(self, phase: ExperimentPhase) -> bool:
        """Validate that phase success metrics are met."""
        if self.dry_run:
            return True

        # Implement metric validation logic
        # This would check actual metrics against expected values
        logger.info(f"Validating metrics for phase: {phase.name}")
        return True  # Placeholder

    async def _process_decision_queue(self):
        """Process any pending decisions in the queue."""
        if self.decision_queue.has_pending_decisions():
            logger.info("Processing decision queue...")

            # In autonomous mode, we log decisions but don't wait for input
            decisions = self.decision_queue.get_pending_decisions()
            for decision in decisions:
                logger.warning(f"Decision required: {decision.title}")
                logger.warning(f"Context: {decision.context}")

                # For now, auto-approve non-critical decisions
                if decision.priority != "high":
                    await self.decision_queue.resolve_decision(decision.id, "auto_approved")
                    logger.info(f"Auto-approved decision: {decision.id}")
                else:
                    logger.error(f"High-priority decision requires human input: {decision.id}")

    async def _handle_phase_failure(self, phase: ExperimentPhase):
        """Handle phase execution failure."""
        logger.error(f"Handling failure for phase: {phase.name}")

        await self._queue_decision(
            f"phase_failure_{phase.name}",
            f"Phase {phase.name} failed to complete successfully",
            ["Retry phase", "Skip phase and continue", "Abort experiment"],
            priority="high"
        )

    async def _handle_experiment_failure(self, error: Exception):
        """Handle overall experiment failure."""
        logger.error(f"Handling experiment failure: {error}")

        await self._queue_decision(
            "experiment_failure",
            f"Experiment failed with error: {error}",
            ["Retry experiment", "Modify configuration", "Abort permanently"],
            priority="high"
        )

    async def _queue_decision(self, decision_id: str, context: str,
                            options: List[str], priority: str = "medium"):
        """Queue a decision for human review."""
        from nusy_pm_core.models.experiment import Decision

        decision = Decision(
            id=decision_id,
            title=f"Decision Required: {decision_id}",
            context=context,
            options=options,
            priority=priority,
            timestamp=datetime.now()
        )

        await self.decision_queue.add_decision(decision)
        logger.info(f"Queued decision: {decision_id} (priority: {priority})")

    async def _generate_final_assessment(self):
        """Generate final experiment assessment."""
        logger.info("Generating final experiment assessment...")

        assessment = {
            "experiment_name": self.config.experiment_name,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration": str(datetime.now() - self.start_time),
            "phases_completed": len(self.config.phases),
            "decisions_queued": len(self.decision_queue.decisions),
            "success_metrics": self.config.success_criteria,
            "recommendations": [
                "Review decision queue for pending items",
                "Analyze logs for performance insights",
                "Consider backlog items for next iteration"
            ]
        }

        assessment_path = Path("reports/final_assessment.json")
        with open(assessment_path, 'w') as f:
            json.dump(assessment, f, indent=2, default=str)

        logger.info(f"Final assessment saved to: {assessment_path}")

    async def generate_progress_report(self) -> Dict[str, Any]:
        """Generate a progress report for the current experiment state."""
        if not self.start_time:
            return {"status": "not_started"}

        elapsed = datetime.now() - self.start_time
        progress = min(elapsed.days / self.config.duration_days, 1.0) if self.config else 0

        return {
            "experiment_name": self.config.experiment_name if self.config else "unknown",
            "status": "running",
            "progress_percentage": progress * 100,
            "elapsed_days": elapsed.days,
            "total_days": self.config.duration_days if self.config else 0,
            "current_phase": self.current_phase.name if self.current_phase else "none",
            "pending_decisions": len(self.decision_queue.decisions),
            "last_updated": datetime.now().isoformat()
        }


async def main():
    """Main entry point for the experiment runner."""
    parser = argparse.ArgumentParser(description="Autonomous Multi-Agent Experiment Runner")
    parser.add_argument("--config", default="config/experiment.json",
                       help="Path to experiment configuration file")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run in simulation mode without actual execution")

    args = parser.parse_args()

    # Initialize and run experiment
    runner = AutonomousExperimentRunner(config_path=args.config, dry_run=args.dry_run)

    if not await runner.initialize():
        logger.error("Failed to initialize experiment runner")
        sys.exit(1)

    success = await runner.run_experiment()

    if success:
        logger.info("Experiment completed successfully")
        sys.exit(0)
    else:
        logger.error("Experiment failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())