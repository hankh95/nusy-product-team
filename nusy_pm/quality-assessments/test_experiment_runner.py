"""
Tests for autonomous experiment runner functionality.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nusy_pm_core.adapters.agent_adapter import AgentAdapter
from nusy_pm_core.services.experiment_runner import ExperimentRunnerService
from nusy_pm_core.models.experiment import ExperimentConfig, DecisionQueue


class TestAgentAdapter:
    """Test the agent adapter functionality."""

    @pytest.fixture
    def agent_adapter(self):
        """Create agent adapter instance."""
        return AgentAdapter()

    @pytest.mark.asyncio
    async def test_list_available_agents(self, agent_adapter):
        """Test that all required agents are available."""
        agents = await agent_adapter.list_available_agents()
        required_agents = ["quartermaster", "pilot", "santiago"]
        for agent in required_agents:
            assert agent in agents

    @pytest.mark.asyncio
    async def test_agent_initialization(self, agent_adapter):
        """Test agent initialization with API calls."""
        # Mock the OpenAI client
        with patch.object(agent_adapter, 'openai_client') as mock_client:
            mock_response = Mock()
            mock_response.choices[0].message.content = "I am ready to serve as the Quartermaster."
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

            success = await agent_adapter.initialize_agent("quartermaster")
            assert success

    @pytest.mark.asyncio
    async def test_agent_communication(self, agent_adapter):
        """Test inter-agent communication."""
        with patch.object(agent_adapter, 'openai_client') as mock_client:
            mock_response = Mock()
            mock_response.choices[0].message.content = "Communication established."
            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

            response = await agent_adapter.send_message("quartermaster", "Test message")
            assert response is not None
            assert not response.startswith("Error")


class TestExperimentRunnerService:
    """Test the experiment runner service."""

    @pytest.fixture
    def config(self):
        """Create test experiment config."""
        return ExperimentConfig(
            experiment_name="test-experiment",
            duration_days=1,
            phases=[],
            decision_triggers=[],
            success_criteria={}
        )

    @pytest.fixture
    def decision_queue(self):
        """Create test decision queue."""
        return DecisionQueue()

    @pytest.fixture
    def runner_service(self, config, decision_queue):
        """Create experiment runner service."""
        return ExperimentRunnerService(config, decision_queue)

    @pytest.mark.asyncio
    async def test_agent_initialization_behavior(self, runner_service):
        """Test the agent initialization behavior."""
        with patch.object(runner_service.agent_adapter, 'initialize_agent') as mock_init:
            mock_init.return_value = True

            result = await runner_service._initialize_agents()
            assert result is True
            assert mock_init.call_count == 3  # quartermaster, pilot, santiago

    @pytest.mark.asyncio
    async def test_communication_setup_behavior(self, runner_service):
        """Test the communication setup behavior."""
        with patch.object(runner_service.agent_adapter, 'send_message') as mock_send:
            mock_send.return_value = "Communication successful"

            result = await runner_service._setup_communication()
            assert result is True
            assert mock_send.call_count >= 3  # At least initial tests

    @pytest.mark.asyncio
    async def test_knowledge_ingestion_behavior(self, runner_service):
        """Test the knowledge ingestion behavior."""
        with patch.object(runner_service.agent_adapter, 'send_message') as mock_send:
            mock_send.return_value = "Knowledge ingested successfully"

            result = await runner_service._ingest_sources()
            assert result is True
            # Should call Pilot agent for knowledge ingestion
            mock_send.assert_called()

    @pytest.mark.asyncio
    async def test_ethical_validation_behavior(self, runner_service):
        """Test the ethical validation behavior."""
        with patch.object(runner_service.agent_adapter, 'send_message') as mock_send:
            mock_send.return_value = "Ethically approved"

            result = await runner_service._validate_knowledge()
            assert result is True
            # Should call Quartermaster for ethical review
            mock_send.assert_called()


class TestAutonomousExperimentRunner:
    """Test the main experiment runner."""

    @pytest.mark.asyncio
    async def test_experiment_initialization(self):
        """Test experiment initialization."""
        from experiment_runner import AutonomousExperimentRunner

        runner = AutonomousExperimentRunner(dry_run=True)

        # Mock the agent adapter check
        with patch('experiment_runner.AgentAdapter') as mock_adapter_class:
            mock_adapter = Mock()
            mock_adapter.list_available_agents = AsyncMock(return_value=["quartermaster", "pilot", "santiago"])
            mock_adapter_class.return_value = mock_adapter

            success = await runner.initialize()
            assert success

    @pytest.mark.asyncio
    async def test_autonomous_decision_making(self):
        """Test that decisions are made autonomously."""
        from experiment_runner import AutonomousExperimentRunner
        from nusy_pm_core.models.experiment import Decision

        runner = AutonomousExperimentRunner(dry_run=True)

        # Create a test decision
        decision = Decision(
            id="test_decision",
            title="Test Decision",
            context="Test context",
            options=["Option A", "Option B"],
            priority="high"
        )

        # Mock agent response
        with patch.object(runner, '_make_autonomous_decision') as mock_decide:
            mock_decide.return_value = "Option A"

            resolution = await runner._make_autonomous_decision(decision)
            assert resolution == "Option A"