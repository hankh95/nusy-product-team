"""
EXP-037 Integration Validation Tests

Comprehensive integration tests to validate that all EXP-036 Phase 1 components
work together as a cohesive autonomous development system.

Tests cover:
1. Self-questioning tool ↔ In-memory LLM service integration
2. Workflow orchestration ↔ Shared memory Git atomic operations
3. End-to-end autonomous development scenarios
4. Performance validation against velocity targets
"""

import asyncio
import time
import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Import EXP-036 components
from expeditions.exp_036.in_memory_llm_service import InMemoryLLMService, LLMQuery
from expeditions.exp_036.workflow_orchestration_engine import (
    WorkflowOrchestrationEngine,
    WorkflowState,
    ProblemState,
    get_workflow_orchestration_engine
)
from expeditions.exp_036.enhanced_shared_memory_git_service import (
    EnhancedSharedMemoryGitService,
    get_enhanced_shared_memory_git_service
)
from domain.src.nusy_pm_core.tools.self_questioning_tool import SelfQuestioningTool


class TestIntegrationValidation(unittest.TestCase):
    """Integration tests for EXP-036 Phase 1 components."""

    def setUp(self):
        """Set up integration test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.workspace_path = Path(self.temp_dir)

        # Initialize all services
        self.llm_service = InMemoryLLMService(max_memory_gb=2.0)
        self.workflow_engine = WorkflowOrchestrationEngine()
        self.git_service = EnhancedSharedMemoryGitService(self.temp_dir, max_memory_mb=256)
        self.questioning_tool = SelfQuestioningTool()

    def tearDown(self):
        """Clean up test resources."""
        self.llm_service.cleanup()
        self.git_service.cleanup_memory()

    def test_self_questioning_llm_integration(self):
        """Test self-questioning tool integrates with in-memory LLM service."""
        # Test question that should be answered by local LLM
        question = "How should I structure error handling in Python functions?"

        result = self.questioning_tool.ask_question(question)

        # Verify it was answered via local LLM
        self.assertEqual(result.source.value, "local_llm")
        self.assertIn("confidence", result.confidence.value.lower())
        self.assertIsInstance(result.answer, str)
        self.assertGreater(len(result.answer), 10)

        # Verify LLM service was actually used
        stats = self.llm_service.get_stats()
        self.assertGreater(stats["total_queries"], 0)

    def test_workflow_git_atomic_operations(self):
        """Test workflow orchestration with shared memory Git atomic operations."""
        # Create workflow items
        item1_id = asyncio.run(self.workflow_engine.create_workflow_item(
            "Create user authentication module",
            tags={"backend", "security"}
        ))

        item2_id = asyncio.run(self.workflow_engine.create_workflow_item(
            "Add authentication tests",
            tags={"testing", "backend"},
            metadata={"dependencies": [item1_id]}
        ))

        # Move items through workflow
        asyncio.run(self.workflow_engine.transition_item(item1_id, WorkflowState.READY))
        asyncio.run(self.workflow_engine.transition_item(item1_id, WorkflowState.IN_PROGRESS))

        # Complete first item
        self.workflow_engine.items[item1_id].metadata["completion_criteria"] = [True]
        asyncio.run(self.workflow_engine.transition_item(item1_id, WorkflowState.REVIEW))
        self.workflow_engine.items[item1_id].metadata["approved"] = True
        asyncio.run(self.workflow_engine.transition_item(item1_id, WorkflowState.APPROVED))
        asyncio.run(self.workflow_engine.transition_item(item1_id, WorkflowState.INTEGRATED))
        asyncio.run(self.workflow_engine.transition_item(item1_id, WorkflowState.DONE))

        # Now second item should be able to proceed
        success = asyncio.run(self.workflow_engine.transition_item(item2_id, WorkflowState.READY))
        self.assertTrue(success)

        # Test atomic Git operations
        operations = [
            {"type": "create", "file_path": "auth.py", "content": "# Authentication module"},
            {"type": "create", "file_path": "test_auth.py", "content": "# Authentication tests"}
        ]

        op_id = asyncio.run(self.git_service.create_atomic_operation(operations))
        success = asyncio.run(self.git_service.execute_atomic_operation(op_id))
        self.assertTrue(success)

        # Verify files were created
        content1 = self.git_service.get_file_content("auth.py")
        content2 = self.git_service.get_file_content("test_auth.py")

        self.assertEqual(content1, "# Authentication module")
        self.assertEqual(content2, "# Authentication tests")

    def test_end_to_end_autonomous_workflow(self):
        """Test complete autonomous development workflow."""
        # Start with a development question
        question = "How should I implement a simple caching decorator in Python?"

        # Use self-questioning to get approach
        result = self.questioning_tool.ask_question(question)
        self.assertIsNotNone(result.answer)

        # Create workflow item based on the answer
        item_id = asyncio.run(self.workflow_engine.create_workflow_item(
            "Implement caching decorator",
            metadata={"approach": result.answer[:200]}  # Store approach
        ))

        # Execute the workflow
        states = [WorkflowState.READY, WorkflowState.IN_PROGRESS, WorkflowState.REVIEW,
                 WorkflowState.APPROVED, WorkflowState.INTEGRATED, WorkflowState.DONE]

        for state in states:
            if state == WorkflowState.REVIEW:
                self.workflow_engine.items[item_id].metadata["completion_criteria"] = [True]
            elif state == WorkflowState.APPROVED:
                self.workflow_engine.items[item_id].metadata["approved"] = True

            success = asyncio.run(self.workflow_engine.transition_item(item_id, state))
            self.assertTrue(success)

        # Verify workflow completion
        item = self.workflow_engine.items[item_id]
        self.assertEqual(item.state, WorkflowState.DONE)
        self.assertIsNotNone(item.completed_at)
        self.assertIsNotNone(item.cycle_time)

    def test_performance_validation(self):
        """Test performance meets 10x velocity targets."""
        # Measure baseline performance for question answering
        question = "What is the best way to handle exceptions in async Python code?"

        # Time local LLM response
        start_time = time.time()
        result = self.questioning_tool.ask_question(question)
        local_time = time.time() - start_time

        # Verify performance targets
        self.assertLess(local_time, 1.0)  # Should be < 1 second
        self.assertEqual(result.source.value, "local_llm")

        # Test workflow efficiency
        item_id = asyncio.run(self.workflow_engine.create_workflow_item("Performance test"))

        # Complete workflow quickly
        states = [WorkflowState.READY, WorkflowState.IN_PROGRESS, WorkflowState.REVIEW,
                 WorkflowState.APPROVED, WorkflowState.INTEGRATED, WorkflowState.DONE]

        for state in states:
            if state == WorkflowState.REVIEW:
                self.workflow_engine.items[item_id].metadata["completion_criteria"] = [True]
            elif state == WorkflowState.APPROVED:
                self.workflow_engine.items[item_id].metadata["approved"] = True
            asyncio.run(self.workflow_engine.transition_item(item_id, state))

        # Check cycle time
        item = self.workflow_engine.items[item_id]
        self.assertIsNotNone(item.cycle_time)
        self.assertGreater(item.cycle_time, 0)

    def test_concurrent_multi_agent_operations(self):
        """Test concurrent operations simulating multiple agents."""
        def agent_task(agent_id):
            """Simulate an agent performing development tasks."""
            # Create workflow item
            item_id = asyncio.run(self.workflow_engine.create_workflow_item(
                f"Task by agent {agent_id}",
                tags={f"agent_{agent_id}"}
            ))

            # Move through workflow
            asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.READY))
            asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.IN_PROGRESS))

            # Create file atomically
            operations = [{
                "type": "create",
                "file_path": f"agent_{agent_id}_file.py",
                "content": f"# Created by agent {agent_id}"
            }]

            op_id = asyncio.run(self.git_service.create_atomic_operation(operations))
            success = asyncio.run(self.git_service.execute_atomic_operation(op_id))

            # Complete workflow
            if success:
                self.workflow_engine.items[item_id].metadata["completion_criteria"] = [True]
                asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.REVIEW))
                self.workflow_engine.items[item_id].metadata["approved"] = True
                asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.APPROVED))
                asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.INTEGRATED))
                asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.DONE))

            return success

        # Run multiple agents concurrently
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(agent_task, i) for i in range(5)]
            results = [future.result() for future in as_completed(futures)]

        # All agents should succeed
        self.assertTrue(all(results))

        # Verify all files were created without conflicts
        for i in range(5):
            content = self.git_service.get_file_content(f"agent_{i}_file.py")
            self.assertEqual(content, f"# Created by agent {i}")

        # Check workflow metrics
        metrics = self.workflow_engine.get_workflow_metrics()
        self.assertGreater(metrics.current_wip, 0)  # Should have completed items

    def test_conflict_free_collaboration(self):
        """Test that shared memory Git prevents merge conflicts."""
        # Create multiple operations that could conflict
        operations1 = [
            {"type": "create", "file_path": "shared_module.py", "content": "# Version 1"}
        ]
        operations2 = [
            {"type": "create", "file_path": "shared_module.py", "content": "# Version 2"}
        ]

        # Create both operations
        op1_id = asyncio.run(self.git_service.create_atomic_operation(operations1))
        op2_id = asyncio.run(self.git_service.create_atomic_operation(operations2))

        # Execute first operation
        success1 = asyncio.run(self.git_service.execute_atomic_operation(op1_id))
        self.assertTrue(success1)

        # Second operation should detect conflict
        conflicts = self.git_service.detect_conflicts(op2_id)
        self.assertIn(op1_id, conflicts)

        # Trying to execute conflicting operation should fail
        success2 = asyncio.run(self.git_service.execute_atomic_operation(op2_id))
        self.assertFalse(success2)

    def test_bayesian_workflow_prioritization(self):
        """Test Bayesian prioritization in workflow engine."""
        from datetime import datetime, timedelta
        
        # Create items with different priority factors
        urgent_item = asyncio.run(self.workflow_engine.create_workflow_item(
            "Urgent security fix",
            tags={"security", "urgent"},
            metadata={"deadline": datetime.now() + timedelta(hours=1)}  # 1 hour deadline
        ))

        complex_item = asyncio.run(self.workflow_engine.create_workflow_item(
            "Complex architecture change",
            tags={"architecture", "complex"}
        ))

        simple_item = asyncio.run(self.workflow_engine.create_workflow_item(
            "Simple documentation update",
            tags={"documentation"}
        ))

        # Move all to ready state
        for item_id in [urgent_item, complex_item, simple_item]:
            asyncio.run(self.workflow_engine.transition_item(item_id, WorkflowState.READY))

        # Get prioritized items
        prioritized = asyncio.run(self.workflow_engine.get_prioritized_items(WorkflowState.READY, limit=3))

        # Urgent security item should be first
        self.assertEqual(len(prioritized), 3)
        self.assertEqual(prioritized[0].id, urgent_item)

        # All should have reasonable priority scores
        for item in prioritized:
            self.assertGreaterEqual(item.priority, 0.0)
            self.assertLessEqual(item.priority, 1.0)


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests for EXP-036 integration."""

    def setUp(self):
        self.llm_service = InMemoryLLMService(max_memory_gb=1.0)
        self.questioning_tool = SelfQuestioningTool()

    def tearDown(self):
        self.llm_service.cleanup()

    def test_question_answering_performance(self):
        """Benchmark question answering performance."""
        questions = [
            "How do I handle exceptions in Python?",
            "What is dependency injection?",
            "How should I structure a REST API?",
            "What are Python decorators?",
            "How do I optimize database queries?"
        ]

        response_times = []

        for question in questions:
            start_time = time.time()
            result = self.questioning_tool.ask_question(question)
            response_time = time.time() - start_time

            response_times.append(response_time)
            self.assertLess(response_time, 2.0)  # Should be fast
            self.assertEqual(result.source.value, "local_llm")

        # Calculate statistics
        avg_time = statistics.mean(response_times)
        p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile

        print(f"Average response time: {avg_time:.3f}s")
        print(f"95th percentile: {p95_time:.3f}s")

        # Performance targets
        self.assertLess(avg_time, 0.5)  # Target: < 500ms average
        self.assertLess(p95_time, 1.0)  # Target: < 1s p95

    def test_workflow_throughput(self):
        """Test workflow processing throughput."""
        engine = WorkflowOrchestrationEngine()

        # Create multiple items
        item_ids = []
        for i in range(10):
            item_id = asyncio.run(engine.create_workflow_item(f"Benchmark item {i}"))
            item_ids.append(item_id)

        start_time = time.time()

        # Process all items through workflow
        for item_id in item_ids:
            states = [WorkflowState.READY, WorkflowState.IN_PROGRESS, WorkflowState.REVIEW,
                     WorkflowState.APPROVED, WorkflowState.INTEGRATED, WorkflowState.DONE]

            for state in states:
                if state == WorkflowState.REVIEW:
                    engine.items[item_id].metadata["completion_criteria"] = [True]
                elif state == WorkflowState.APPROVED:
                    engine.items[item_id].metadata["approved"] = True
                asyncio.run(engine.transition_item(item_id, state))

        total_time = time.time() - start_time
        throughput = len(item_ids) / total_time

        print(f"Workflow throughput: {throughput:.2f} items/second")

if __name__ == "__main__":
    unittest.main()
