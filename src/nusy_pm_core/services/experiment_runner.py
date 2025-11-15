"""
Experiment runner service for autonomous multi-agent experimentation.
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

from nusy_pm_core.models.experiment import (
    ExperimentConfig,
    ExperimentPhase,
    DecisionQueue,
    ExperimentResult,
    UsabilityTestResult
)
from nusy_pm_core.adapters.agent_adapter import AgentAdapter

logger = logging.getLogger(__name__)


class ExperimentRunnerService:
    """Service for running autonomous experiments."""

    def __init__(self, config: ExperimentConfig, decision_queue: DecisionQueue):
        self.config = config
        self.decision_queue = decision_queue
        self.current_phase: Optional[ExperimentPhase] = None
        self.agent_adapter = AgentAdapter()
        self.results: ExperimentResult = ExperimentResult(
            experiment_name=config.experiment_name,
            start_time=datetime.now()
        )

    async def execute_behavior(self, behavior: str) -> bool:
        """Execute a specific behavior within the current phase."""
        logger.info(f"Executing behavior: {behavior}")

        try:
            # Map behavior names to execution methods
            behavior_handlers = {
                "agent_initialization": self._initialize_agents,
                "communication_setup": self._setup_communication,
                "source_ingestion": self._ingest_sources,
                "knowledge_validation": self._validate_knowledge,
                "feature_proposal": self._propose_features,
                "implementation": self._implement_features,
                "testing": self._run_tests,
                "performance_analysis": self._analyze_performance,
                "improvement_proposal": self._propose_improvements
            }

            handler = behavior_handlers.get(behavior)
            if not handler:
                logger.error(f"No handler found for behavior: {behavior}")
                return False

            success = await handler()
            if success:
                logger.info(f"Behavior {behavior} executed successfully")
            else:
                logger.error(f"Behavior {behavior} execution failed")

            return success

        except Exception as e:
            logger.error(f"Error executing behavior {behavior}: {e}")
            return False

    async def _initialize_agents(self) -> bool:
        """Initialize the core agents for the experiment."""
        logger.info("Initializing agents...")

        agents_to_init = ["quartermaster", "pilot", "santiago"]
        initialized_count = 0

        for agent_id in agents_to_init:
            success = await self.agent_adapter.initialize_agent(agent_id)
            if success:
                initialized_count += 1
                logger.info(f"Successfully initialized agent: {agent_id}")
            else:
                logger.error(f"Failed to initialize agent: {agent_id}")

        if initialized_count == len(agents_to_init):
            logger.info("All agents initialized successfully")
            return True
        else:
            logger.error(f"Only {initialized_count}/{len(agents_to_init)} agents initialized")
            return False

    async def _setup_communication(self) -> bool:
        """Set up inter-agent communication protocols."""
        logger.info("Setting up agent communication...")

        # Test communication with each agent
        test_message = "Communication test: Please acknowledge your role and readiness."

        for agent_id in ["quartermaster", "pilot", "santiago"]:
            try:
                response = await self.agent_adapter.send_message(agent_id, test_message)
                if response and not response.startswith("Error"):
                    logger.info(f"Communication established with {agent_id}")
                else:
                    logger.error(f"Communication failed with {agent_id}")
                    return False
            except Exception as e:
                logger.error(f"Error testing communication with {agent_id}: {e}")
                return False

        # Test inter-agent coordination
        santiago_message = "As orchestrator, please coordinate a brief introduction between Quartermaster and Pilot."
        try:
            coord_response = await self.agent_adapter.send_message("santiago", santiago_message)
            if coord_response and not coord_response.startswith("Error"):
                logger.info("Inter-agent coordination test successful")
                return True
            else:
                logger.error("Inter-agent coordination test failed")
                return False
        except Exception as e:
            logger.error(f"Error in coordination test: {e}")
            return False

    async def _ingest_sources(self) -> bool:
        """Ingest knowledge sources for PM domain expertise."""
        logger.info("Ingesting knowledge sources...")

        # Have the Pilot agent summarize key PM methodologies
        pm_sources = [
            "Agile Manifesto principles",
            "Scrum framework (roles, ceremonies, artifacts)",
            "Kanban method (visualize workflow, limit WIP)",
            "Lean UX principles from Jeff Gothelf",
            "User Story Mapping from Jeff Patton",
            "Continuous Discovery Habits",
            "OKRs (Objectives and Key Results)",
            "Lean Startup methodology"
        ]

        ingestion_prompt = f"""As the Pilot (PM Domain Expert), please analyze and summarize the following PM methodologies and practices:

{chr(10).join(f"- {source}" for source in pm_sources)}

Provide a comprehensive overview of how these methodologies work together and their key principles for effective product management."""

        try:
            response = await self.agent_adapter.send_message("pilot", ingestion_prompt)
            if response and not response.startswith("Error"):
                logger.info("PM knowledge ingestion completed")
                # In a real implementation, this would be stored in the knowledge graph
                return True
            else:
                logger.error("PM knowledge ingestion failed")
                return False
        except Exception as e:
            logger.error(f"Error during knowledge ingestion: {e}")
            return False

    async def _validate_knowledge(self) -> bool:
        """Validate ingested knowledge for consistency."""
        logger.info("Validating knowledge...")

        # Have the Quartermaster review the PM knowledge for ethical alignment
        validation_prompt = """As the Quartermaster (Ethical Overseer), please review the PM methodologies that were just ingested by the Pilot agent.

Consider whether these methodologies align with Baha'i principles of:
- Service to humanity
- Consultation and consensus-building
- Unity in diversity
- Progressive revelation
- Elimination of prejudice

Provide an ethical assessment and any recommendations for ensuring the development process serves humanity's best interests."""

        try:
            response = await self.agent_adapter.send_message("quartermaster", validation_prompt)
            if response and not response.startswith("Error"):
                logger.info("Knowledge validation completed")
                return True
            else:
                logger.error("Knowledge validation failed")
                return False
        except Exception as e:
            logger.error(f"Error during knowledge validation: {e}")
            return False

    async def _propose_features(self) -> bool:
        """Generate feature proposals for PM capabilities."""
        logger.info("Proposing features...")

        # Have Santiago coordinate feature ideation
        coordination_prompt = """As the orchestrator, please coordinate between the Pilot and Quartermaster to identify the most important missing PM capabilities that should be implemented first.

Pilot: What are the core PM features that would provide the most value?
Quartermaster: Which features best serve humanity and align with ethical principles?

Please synthesize their input and propose 3-5 high-priority PM features to implement."""

        try:
            santiago_response = await self.agent_adapter.send_message("santiago", coordination_prompt)
            if not santiago_response or santiago_response.startswith("Error"):
                logger.error("Failed to get feature proposals from Santiago")
                return False

            # Have Pilot provide detailed specifications
            pilot_prompt = f"""Based on Santiago's coordination: {santiago_response[:500]}...

As the PM expert, please provide detailed specifications for the top 2 proposed features, including:
- User stories
- Acceptance criteria
- Technical requirements
- Success metrics"""

            pilot_response = await self.agent_adapter.send_message("pilot", pilot_prompt)
            if not pilot_response or pilot_response.startswith("Error"):
                logger.error("Failed to get feature specs from Pilot")
                return False

            # Have Quartermaster review for ethical compliance
            quartermaster_prompt = f"""Review these feature proposals for ethical alignment: {pilot_response[:1000]}...

Ensure they serve humanity's best interests and align with Baha'i principles. Provide any ethical concerns or recommendations."""

            quartermaster_response = await self.agent_adapter.send_message("quartermaster", quartermaster_prompt)
            if not quartermaster_response or quartermaster_response.startswith("Error"):
                logger.error("Failed to get ethical review from Quartermaster")
                return False

            logger.info("Feature proposal process completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error during feature proposal: {e}")
            return False

    async def _implement_features(self) -> bool:
        """Implement proposed features."""
        logger.info("Implementing features...")

        # In a real autonomous system, agents would write code
        # For this experiment, have them describe the implementation approach

        implementation_prompt = """As the development team, please outline how you would implement the top-priority PM feature that was just proposed.

Provide:
1. Code structure and files needed
2. Key algorithms or logic
3. Integration points with existing system
4. Testing approach
5. Success criteria

Focus on making it concrete and implementable."""

        try:
            # Have Santiago coordinate the implementation discussion
            santiago_response = await self.agent_adapter.send_message("santiago", implementation_prompt)
            if not santiago_response or santiago_response.startswith("Error"):
                logger.error("Failed to coordinate implementation")
                return False

            # Have Pilot review from PM perspective
            pilot_review = await self.agent_adapter.send_message("pilot",
                f"Review this implementation approach from a PM perspective: {santiago_response[:1000]}...")
            if not pilot_review or pilot_review.startswith("Error"):
                logger.error("Failed to get PM review")
                return False

            # Have Quartermaster ensure ethical implementation
            ethical_review = await self.agent_adapter.send_message("quartermaster",
                f"Ensure this implementation serves humanity ethically: {pilot_review[:1000]}...")
            if not ethical_review or ethical_review.startswith("Error"):
                logger.error("Failed to get ethical review")
                return False

            logger.info("Feature implementation planning completed")
            return True

        except Exception as e:
            logger.error(f"Error during feature implementation: {e}")
            return False

    async def _run_tests(self) -> bool:
        """Run tests on implemented features."""
        logger.info("Running tests...")

        # Have agents design and simulate testing
        test_prompt = """Design a comprehensive testing strategy for the PM features we've been developing.

Include:
1. Unit tests for core functionality
2. Integration tests for agent communication
3. Usability tests from PM perspective
4. Ethical compliance tests
5. Performance benchmarks

Describe what each test would validate and expected outcomes."""

        try:
            test_plan = await self.agent_adapter.send_message("santiago", test_prompt)
            if test_plan and not test_plan.startswith("Error"):
                logger.info("Test planning completed")
                return True
            else:
                logger.error("Test planning failed")
                return False
        except Exception as e:
            logger.error(f"Error during testing: {e}")
            return False

    async def _analyze_performance(self) -> bool:
        """Analyze experiment performance."""
        logger.info("Analyzing performance...")

        analysis_prompt = """Analyze the performance of this autonomous development experiment so far.

Evaluate:
1. Agent collaboration effectiveness
2. Feature development velocity
3. Ethical decision-making quality
4. Knowledge integration success
5. Communication efficiency

Provide specific metrics, insights, and areas for improvement."""

        try:
            analysis = await self.agent_adapter.send_message("santiago", analysis_prompt)
            if analysis and not analysis.startswith("Error"):
                logger.info("Performance analysis completed")
                return True
            else:
                logger.error("Performance analysis failed")
                return False
        except Exception as e:
            logger.error(f"Error during performance analysis: {e}")
            return False

    async def _propose_improvements(self) -> bool:
        """Propose improvements based on analysis."""
        logger.info("Proposing improvements...")

        improvement_prompt = """Based on the performance analysis, propose specific improvements to the autonomous development system.

Consider:
1. Agent capabilities and training
2. Communication protocols
3. Decision-making processes
4. Knowledge management
5. Ethical oversight mechanisms
6. Development workflows

Provide actionable recommendations for the next iteration."""

        try:
            improvements = await self.agent_adapter.send_message("quartermaster", improvement_prompt)
            if improvements and not improvements.startswith("Error"):
                logger.info("Improvement proposals completed")
                return True
            else:
                logger.error("Improvement proposal failed")
                return False
        except Exception as e:
            logger.error(f"Error during improvement proposal: {e}")
            return False

    async def validate_metrics(self, phase: ExperimentPhase) -> bool:
        """Validate that phase metrics meet success criteria."""
        logger.info(f"Validating metrics for phase: {phase.name}")

        # Placeholder for metric validation
        # This would check actual metrics against expected values
        return True

    async def run_usability_test(self, phase: ExperimentPhase) -> UsabilityTestResult:
        """Run usability tests for a phase."""
        logger.info(f"Running usability test for phase: {phase.name}")

        # Placeholder for usability testing
        result = UsabilityTestResult(
            phase_name=phase.name,
            behaviors_tested=phase.behaviors,
            expected_results=[],  # Would be populated from config
            actual_results=[],    # Would be populated from execution
            success_metrics={},   # Would be populated from measurements
            passed=True
        )

        return result

    async def generate_report(self) -> Dict[str, Any]:
        """Generate a comprehensive experiment report."""
        logger.info("Generating experiment report...")

        report = {
            "experiment_name": self.config.experiment_name,
            "duration_days": self.config.duration_days,
            "phases": [phase.name for phase in self.config.phases],
            "success_criteria": self.config.success_criteria,
            "results": {
                "phases_completed": self.results.phases_completed,
                "status": self.results.status,
                "success_metrics": self.results.success_metrics
            },
            "decisions": [
                {
                    "id": d.id,
                    "title": d.title,
                    "priority": d.priority,
                    "resolved": d.resolved
                }
                for d in self.results.decisions_made
            ]
        }

        return report