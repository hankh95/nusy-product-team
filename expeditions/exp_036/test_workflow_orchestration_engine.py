"""
Test Workflow Orchestration Engine

Tests state machine transitions, Bayesian prioritization, lean flow metrics,
and problem state management for the workflow orchestration engine.
"""

import asyncio
import unittest
from datetime import datetime, timedelta
from workflow_orchestration_engine import (
    WorkflowOrchestrationEngine,
    WorkflowItem,
    WorkflowState,
    ProblemState,
    LeanFlowMetrics,
    BayesianPrioritization,
    get_workflow_orchestration_engine
)


class TestWorkflowOrchestrationEngine(unittest.TestCase):
    """Test cases for the workflow orchestration engine."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = WorkflowOrchestrationEngine()

    def test_initialization(self):
        """Test engine initialization."""
        self.assertIsInstance(self.engine.metrics, LeanFlowMetrics)
        self.assertIsInstance(self.engine.prioritization, BayesianPrioritization)
        self.assertEqual(len(self.engine.transitions), 9)  # Default transitions
        self.assertEqual(len(self.engine.items), 0)

    def test_create_workflow_item(self):
        """Test creating workflow items."""
        item_id = asyncio.run(self.engine.create_workflow_item(
            "Test Item",
            "A test workflow item",
            priority=0.8,
            tags={"test", "important"}
        ))

        self.assertIn(item_id, self.engine.items)
        item = self.engine.items[item_id]

        self.assertEqual(item.title, "Test Item")
        self.assertEqual(item.state, WorkflowState.BACKLOG)
        self.assertEqual(item.priority, 0.8)
        self.assertEqual(item.tags, {"test", "important"})

    def test_state_transitions(self):
        """Test basic state transitions."""
        # Create item
        item_id = asyncio.run(self.engine.create_workflow_item("Test Item"))
        item = self.engine.items[item_id]

        # Test BACKLOG -> READY
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.READY)

        # Test READY -> IN_PROGRESS
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.IN_PROGRESS)
        self.assertIsNotNone(item.started_at)

        # Test IN_PROGRESS -> REVIEW (requires completion criteria)
        item.metadata["completion_criteria"] = [True]
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.REVIEW))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.REVIEW)

        # Test REVIEW -> APPROVED (requires approval)
        item.metadata["approved"] = True
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.APPROVED))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.APPROVED)

        # Test APPROVED -> INTEGRATED -> DONE
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.INTEGRATED))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.INTEGRATED)

        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.DONE))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.DONE)
        self.assertIsNotNone(item.completed_at)
        self.assertIsNotNone(item.cycle_time)

    def test_blocked_state_transitions(self):
        """Test transitions involving blocked states."""
        # Create item and move to in progress
        item_id = asyncio.run(self.engine.create_workflow_item("Test Item"))
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))

        item = self.engine.items[item_id]

        # Move to blocked
        success = asyncio.run(self.engine.transition_item(
            item_id,
            WorkflowState.BLOCKED,
            ProblemState.TECHNICAL_UNCERTAINTY
        ))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.BLOCKED)
        self.assertEqual(item.problem_state, ProblemState.TECHNICAL_UNCERTAINTY)

        # Try to resolve - should fail without proper resolution
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))
        self.assertFalse(success)

        # Resolve the technical uncertainty
        item.metadata["technical_clarity"] = True
        success = asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))
        self.assertTrue(success)
        self.assertEqual(item.state, WorkflowState.IN_PROGRESS)
        self.assertIsNone(item.problem_state)

    def test_dependency_management(self):
        """Test workflow item dependencies."""
        # Create two items
        item1_id = asyncio.run(self.engine.create_workflow_item("Item 1"))
        item2_id = asyncio.run(self.engine.create_workflow_item("Item 2"))

        # Make item2 depend on item1
        item2 = self.engine.items[item2_id]
        item2.metadata["dependencies"] = [item1_id]

        # Try to move item2 to ready - should fail
        success = asyncio.run(self.engine.transition_item(item2_id, WorkflowState.READY))
        self.assertFalse(success)

        # Complete item1
        asyncio.run(self.engine.transition_item(item1_id, WorkflowState.READY))
        asyncio.run(self.engine.transition_item(item1_id, WorkflowState.IN_PROGRESS))
        self.engine.items[item1_id].metadata["completion_criteria"] = [True]
        asyncio.run(self.engine.transition_item(item1_id, WorkflowState.REVIEW))
        self.engine.items[item1_id].metadata["approved"] = True
        asyncio.run(self.engine.transition_item(item1_id, WorkflowState.APPROVED))
        asyncio.run(self.engine.transition_item(item1_id, WorkflowState.INTEGRATED))
        asyncio.run(self.engine.transition_item(item1_id, WorkflowState.DONE))

        # Now item2 should be able to move to ready
        success = asyncio.run(self.engine.transition_item(item2_id, WorkflowState.READY))
        self.assertTrue(success)

    def test_bayesian_prioritization(self):
        """Test Bayesian prioritization of workflow items."""
        # Create items with different characteristics
        item1_id = asyncio.run(self.engine.create_workflow_item(
            "Old Item",
            created_at=datetime.now() - timedelta(days=7)
        ))

        item2_id = asyncio.run(self.engine.create_workflow_item(
            "Blocker Item",
            metadata={"blocking": ["item3", "item4"]}
        ))

        item3_id = asyncio.run(self.engine.create_workflow_item(
            "Complex Item",
            tags={"complex", "architectural"}
        ))

        item4_id = asyncio.run(self.engine.create_workflow_item(
            "Urgent Item",
            metadata={"deadline": datetime.now() + timedelta(hours=24)}
        ))

        # Move all to READY state
        for item_id in [item1_id, item2_id, item3_id, item4_id]:
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))

        # Get prioritized items
        prioritized = asyncio.run(self.engine.get_prioritized_items(WorkflowState.READY))

        # Should have all 4 items
        self.assertEqual(len(prioritized), 4)

        # Check that prioritization considers factors
        priorities = [item.priority for item in prioritized]
        self.assertTrue(all(0.0 <= p <= 1.0 for p in priorities))

    def test_lean_flow_metrics(self):
        """Test lean flow metrics calculation."""
        # Create and complete some items
        for i in range(5):
            item_id = asyncio.run(self.engine.create_workflow_item(f"Item {i}"))

            # Simulate workflow progression
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))
            self.engine.items[item_id].metadata["completion_criteria"] = [True]
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.REVIEW))
            self.engine.items[item_id].metadata["approved"] = True
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.APPROVED))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.INTEGRATED))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.DONE))

        metrics = self.engine.get_workflow_metrics()

        # Check metrics are calculated
        self.assertGreater(metrics.cycle_time_hours, 0)
        self.assertGreaterEqual(metrics.flow_efficiency, 0.0)
        self.assertLessEqual(metrics.flow_efficiency, 1.0)
        self.assertGreaterEqual(metrics.throughput_per_day, 0)

    def test_problem_state_tracking(self):
        """Test problem state tracking and analysis."""
        # Create items and put them in blocked state with different problems
        problems = [
            ProblemState.MISSING_DEPENDENCIES,
            ProblemState.TECHNICAL_UNCERTAINTY,
            ProblemState.CODE_REVIEW_FAILURES,
            ProblemState.TESTING_BLOCKAGES
        ]

        for i, problem in enumerate(problems):
            item_id = asyncio.run(self.engine.create_workflow_item(f"Problem Item {i}"))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.BLOCKED, problem))

        # Check problem state counts
        analysis = self.engine.get_blockage_analysis()
        self.assertEqual(len(analysis["top_blockages"]), 4)

        for problem in problems:
            self.assertIn(problem, analysis["top_blockages"])
            self.assertEqual(analysis["top_blockages"][problem], 1)

        self.assertEqual(analysis["current_blocked_items"], 4)

    def test_workflow_optimization_suggestions(self):
        """Test workflow optimization suggestions."""
        # Create scenario with high WIP
        for i in range(10):
            item_id = asyncio.run(self.engine.create_workflow_item(f"Item {i}"))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))

        # Get optimization suggestions
        suggestions = asyncio.run(self.engine.optimize_workflow())

        # Should include WIP limit warning
        wip_suggestions = [s for s in suggestions if "WIP limit" in s]
        self.assertTrue(len(wip_suggestions) > 0)

    def test_timing_metrics(self):
        """Test timing and flow metrics."""
        item_id = asyncio.run(self.engine.create_workflow_item("Timing Test"))

        # Move through states
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.IN_PROGRESS))

        item = self.engine.items[item_id]

        # Check timing is tracked
        self.assertIn(WorkflowState.READY, item.time_in_state)
        self.assertIn(WorkflowState.IN_PROGRESS, item.time_in_state)

        # Complete the item
        item.metadata["completion_criteria"] = [True]
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.REVIEW))
        item.metadata["approved"] = True
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.APPROVED))
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.INTEGRATED))
        asyncio.run(self.engine.transition_item(item_id, WorkflowState.DONE))

        # Check completion metrics
        self.assertIsNotNone(item.completed_at)
        self.assertIsNotNone(item.cycle_time)
        self.assertGreater(item.cycle_time, 0)

    def test_state_queues(self):
        """Test that items are properly managed in state queues."""
        # Create multiple items
        item_ids = []
        for i in range(5):
            item_id = asyncio.run(self.engine.create_workflow_item(f"Queue Item {i}"))
            item_ids.append(item_id)

        # All should be in BACKLOG queue
        backlog_queue = list(self.engine.state_queues[WorkflowState.BACKLOG])
        self.assertEqual(len(backlog_queue), 5)
        self.assertTrue(all(item_id in backlog_queue for item_id in item_ids))

        # Move some to READY
        for item_id in item_ids[:3]:
            asyncio.run(self.engine.transition_item(item_id, WorkflowState.READY))

        # Check queue distribution
        backlog_queue = list(self.engine.state_queues[WorkflowState.BACKLOG])
        ready_queue = list(self.engine.state_queues[WorkflowState.READY])

        self.assertEqual(len(backlog_queue), 2)
        self.assertEqual(len(ready_queue), 3)


class TestGlobalEngine(unittest.TestCase):
    """Test the global workflow engine instance."""

    def test_get_engine_instance(self):
        """Test getting the global engine instance."""
        engine1 = get_workflow_orchestration_engine()
        engine2 = get_workflow_orchestration_engine()

        # Should be the same instance
        self.assertIs(engine1, engine2)
        self.assertIsInstance(engine1, WorkflowOrchestrationEngine)


if __name__ == "__main__":
    unittest.main()</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_036/test_workflow_orchestration_engine.py