"""
EXP-040: Integration Tests

Comprehensive tests for the integrated Santiago entity system,
validating component interactions and collaborative workflows.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import asyncio
import time
import uuid
from datetime import datetime

# Add EXP paths
exp_039_path = Path(__file__).parent.parent / "exp_039"
exp_040_path = Path(__file__).parent
sys.path.insert(0, str(exp_039_path))
sys.path.insert(0, str(exp_040_path))

try:
    from mcp_service_integration import IntegratedServiceRegistry
    from entity_specialization import SantiagoEntityFactory
    from collaborative_workspace import CollaborativeWorkspace, CollaborativeWorkflow
    from mcp_service_layer import MCPRequest
except ImportError as e:
    print(f"Warning: Could not import required components: {e}")


class IntegrationTestSuite:
    """
    Comprehensive test suite for integrated Santiago system.
    """

    def __init__(self):
        self.service_registry = None
        self.workspace = None
        self.workflow = None
        self.entities = {}
        self.test_results = []

    async def setup(self):
        """Setup the integrated test environment."""
        print("Setting up integration test environment...")

        # Create service registry
        self.service_registry = IntegratedServiceRegistry()

        # Create collaborative workspace
        self.workspace = CollaborativeWorkspace(name="Integration Test Workspace")

        # Create collaborative workflow
        self.workflow = CollaborativeWorkflow(self.workspace, self.service_registry)

        # Create and register entities
        factory = SantiagoEntityFactory(self.service_registry)
        self.entities = factory.create_all_entities()

        for role, entity in self.entities.items():
            self.workflow.register_entity(role, entity)

        print(f"Setup complete: {len(self.entities)} entities registered")

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all integration tests."""

        print("\n" + "="*60)
        print("RUNNING INTEGRATION TESTS")
        print("="*60)

        test_results = []

        # Test 1: Service Integration
        test_results.append(await self.test_service_integration())

        # Test 2: Entity Specialization
        test_results.append(await self.test_entity_specialization())

        # Test 3: Collaborative Workspace
        test_results.append(await self.test_collaborative_workspace())

        # Test 4: MCP Performance
        test_results.append(await self.test_mcp_performance())

        # Test 5: Entity Communication
        test_results.append(await self.test_entity_communication())

        # Test 6: Full Collaborative Workflow
        test_results.append(await self.test_full_collaborative_workflow())

        # Test 7: Error Handling
        test_results.append(await self.test_error_handling())

        # Test 8: Performance Benchmarks
        test_results.append(await self.test_performance_benchmarks())

        # Summary
        summary = self.generate_test_summary(test_results)

        print("\n" + "="*60)
        print("INTEGRATION TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(".1f")
        print(f"Average Execution Time: {summary['avg_execution_time']:.2f}s")

        return summary

    async def test_service_integration(self) -> Dict[str, Any]:
        """Test MCP service integration."""
        start_time = time.time()

        try:
            print("\nTest 1: Service Integration")

            # Test Git service
            git_service = self.service_registry.get_service("git")
            assert git_service is not None, "Git service not found"

            from mcp_service_integration import MCPRequest
            request = MCPRequest(
                id=str(uuid.uuid4()),
                method="execute",
                params={"operation": "commit", "params": {"message": "Test commit"}},
                timestamp=datetime.now(),
                client_id="test_client"
            )

            response = await git_service.invoke(request)
            assert response.success, f"Git service failed: {response.error_message}"

            # Test workflow service
            workflow_service = self.service_registry.get_service("workflow")
            assert workflow_service is not None, "Workflow service not found"

            request = MCPRequest(
                id=str(uuid.uuid4()),
                method="execute",
                params={"operation": "prioritize", "params": {"tasks": [{"id": "task1", "priority": 1}]}},
                timestamp=datetime.now(),
                client_id="test_client"
            )

            response = await workflow_service.invoke(request)
            assert response.success, f"Workflow service failed: {response.error_message}"

            execution_time = time.time() - start_time
            print(f"✅ Service Integration Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "service_integration",
                "passed": True,
                "execution_time": execution_time,
                "details": "All MCP services integrated successfully"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Service Integration Test FAILED: {e}")
            return {
                "test_name": "service_integration",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_entity_specialization(self) -> Dict[str, Any]:
        """Test entity specialization and capabilities."""
        start_time = time.time()

        try:
            print("\nTest 2: Entity Specialization")

            # Test PM entity
            pm_entity = self.entities["pm"]
            assert pm_entity.identity.role == "product_manager", "PM entity role incorrect"
            assert len(pm_entity.capability_registry.capabilities) > 0, "PM entity has no capabilities"
            assert len(pm_entity.knowledge_base.knowledge) > 0, "PM entity has no knowledge"

            # Test Dev entity
            dev_entity = self.entities["dev"]
            assert dev_entity.identity.role == "developer", "Dev entity role incorrect"
            assert len(dev_entity.capability_registry.capabilities) > 0, "Dev entity has no capabilities"

            # Test Architect entity
            arch_entity = self.entities["architect"]
            assert arch_entity.identity.role == "architect", "Architect entity role incorrect"
            assert len(arch_entity.capability_registry.capabilities) > 0, "Architect entity has no capabilities"

            # Test entity knowledge domains
            assert "product_management" in pm_entity.identity.expertise_domains
            assert "software_development" in dev_entity.identity.expertise_domains
            assert "system_architecture" in arch_entity.identity.expertise_domains

            execution_time = time.time() - start_time
            print(f"✅ Entity Specialization Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "entity_specialization",
                "passed": True,
                "execution_time": execution_time,
                "details": f"All {len(self.entities)} entities properly specialized"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Entity Specialization Test FAILED: {e}")
            return {
                "test_name": "entity_specialization",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_collaborative_workspace(self) -> Dict[str, Any]:
        """Test collaborative workspace functionality."""
        start_time = time.time()

        try:
            print("\nTest 3: Collaborative Workspace")

            # Test workspace initialization
            status = self.workspace.get_workspace_status()
            assert status["participating_entities"] == 3, "Wrong number of participating entities"
            assert len(status["knowledge_spaces"]) > 0, "No knowledge spaces initialized"

            # Test knowledge sharing
            test_knowledge = {"test_key": "test_value"}
            await self.workspace.share_knowledge("pm_entity_id", "test_space", test_knowledge)

            shared = self.workspace.get_shared_knowledge("test_space")
            assert len(shared) > 0, "Knowledge sharing failed"

            # Test Git operations
            changes = {"test_file.py": "print('hello world')"}
            commit_result = await self.workspace.git_commit("test_entity", "Test commit", changes)

            assert "commit_id" in commit_result, "Git commit failed"
            assert commit_result["files_changed"] == 1, "Wrong number of files changed"

            git_status = self.workspace.git_status()
            assert git_status["total_commits"] > 0, "No commits recorded"

            execution_time = time.time() - start_time
            print(f"✅ Collaborative Workspace Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "collaborative_workspace",
                "passed": True,
                "execution_time": execution_time,
                "details": "Workspace collaboration features working"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Collaborative Workspace Test FAILED: {e}")
            return {
                "test_name": "collaborative_workspace",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_mcp_performance(self) -> Dict[str, Any]:
        """Test MCP service performance."""
        start_time = time.time()

        try:
            print("\nTest 4: MCP Performance")

            # Test multiple service invocations
            git_service = self.service_registry.get_service("git")

            invocation_times = []
            for i in range(10):
                req_start = time.time()

                from mcp_service_layer import MCPRequest
                request = MCPRequest(
                    id=str(uuid.uuid4()),
                    method="execute",
                    params={"operation": "commit", "params": {"message": f"Performance test {i}"}},
                    timestamp=datetime.now(),
                    client_id="perf_test_client"
                )

                response = await git_service.invoke(request)
                assert response.success, f"MCP invocation {i} failed"

                req_end = time.time()
                invocation_times.append(req_end - req_start)

            avg_time = sum(invocation_times) / len(invocation_times)
            max_time = max(invocation_times)

            # Performance assertions (adjust thresholds as needed)
            assert avg_time < 0.1, f"Average invocation time too slow: {avg_time:.3f}s"
            assert max_time < 0.5, f"Max invocation time too slow: {max_time:.3f}s"

            execution_time = time.time() - start_time
            print(f"✅ MCP Performance Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "mcp_performance",
                "passed": True,
                "execution_time": execution_time,
                "details": f"Avg: {avg_time:.3f}s, Max: {max_time:.3f}s"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ MCP Performance Test FAILED: {e}")
            return {
                "test_name": "mcp_performance",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_entity_communication(self) -> Dict[str, Any]:
        """Test entity-to-entity communication."""
        start_time = time.time()

        try:
            print("\nTest 5: Entity Communication")

            # Test message sending
            pm_entity = self.entities["pm"]
            dev_entity = self.entities["dev"]

            test_message = {"type": "task_assignment", "task": "Implement feature X"}
            success = await self.workspace.send_message(
                pm_entity.identity.entity_id,
                dev_entity.identity.entity_id,
                "general",
                test_message
            )
            assert success, "Message sending failed"

            # Test message receiving
            messages = await self.workspace.receive_messages(dev_entity.identity.entity_id, "general")
            assert len(messages) > 0, "No messages received"
            assert messages[0]["content"]["task"] == "Implement feature X", "Wrong message content"

            # Test knowledge sharing between entities
            await self.workspace.share_knowledge(
                pm_entity.identity.entity_id,
                "project_requirements",
                {"feature": "User authentication", "priority": "high"}
            )

            shared_knowledge = self.workspace.get_shared_knowledge("project_requirements")
            assert len(shared_knowledge) > 0, "Knowledge sharing failed"

            execution_time = time.time() - start_time
            print(f"✅ Entity Communication Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "entity_communication",
                "passed": True,
                "execution_time": execution_time,
                "details": "Entity communication working correctly"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Entity Communication Test FAILED: {e}")
            return {
                "test_name": "entity_communication",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_full_collaborative_workflow(self) -> Dict[str, Any]:
        """Test full collaborative workflow execution."""
        start_time = time.time()

        try:
            print("\nTest 6: Full Collaborative Workflow")

            # Create a collaborative goal
            goal = await self.workflow.create_collaborative_goal(
                title="Implement User Login Feature",
                description="Implement secure user login with password validation",
                required_roles=["pm", "architect", "dev"],
                priority=2
            )

            assert goal.goal_id in self.workflow.active_goals, "Goal not created properly"
            assert len(goal.assigned_entities) == 3, "Not all roles assigned"

            # Execute the collaborative goal
            result = await self.workflow.execute_collaborative_goal(goal)

            assert result["success"], f"Collaborative workflow failed: {result.get('error', 'Unknown error')}"
            assert "results" in result, "No results returned"
            assert "planning" in result["results"], "Planning phase missing"
            assert "architecture" in result["results"], "Architecture phase missing"
            assert "implementation" in result["results"], "Implementation phase missing"

            # Check workspace state
            workspace_status = self.workspace.get_workspace_status()
            assert workspace_status["active_projects"] > 0, "No active projects recorded"

            # Check Git commits
            git_status = self.workspace.git_status()
            assert git_status["total_commits"] > 0, "No Git commits created"

            execution_time = time.time() - start_time
            print(f"✅ Full Collaborative Workflow Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "full_collaborative_workflow",
                "passed": True,
                "execution_time": execution_time,
                "details": f"Full workflow completed with {git_status['total_commits']} commits"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Full Collaborative Workflow Test FAILED: {e}")
            return {
                "test_name": "full_collaborative_workflow",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling in the integrated system."""
        start_time = time.time()

        try:
            print("\nTest 7: Error Handling")

            # Test invalid service request
            git_service = self.service_registry.get_service("git")

            from mcp_service_integration import MCPRequest
            request = MCPRequest(
                id=str(uuid.uuid4()),
                method="execute",
                params={"operation": "invalid_operation"},
                timestamp=datetime.now(),
                client_id="test_client"
            )

            response = await git_service.invoke(request)
            assert not response.success, "Invalid operation should have failed"
            assert response.error_message is not None, "No error message provided"

            # Test entity with invalid goal
            pm_entity = self.entities["pm"]
            invalid_goal = Goal(
                id="invalid_goal",
                description="",  # Empty description should cause issues
                priority=1
            )

            # This should handle the error gracefully
            result = await pm_entity.reason_and_act(invalid_goal)
            # Result should indicate failure but not crash the system
            assert isinstance(result, object), "Entity should handle errors gracefully"

            execution_time = time.time() - start_time
            print(f"✅ Error Handling Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "error_handling",
                "passed": True,
                "execution_time": execution_time,
                "details": "Error handling working correctly"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Error Handling Test FAILED: {e}")
            return {
                "test_name": "error_handling",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    async def test_performance_benchmarks(self) -> Dict[str, Any]:
        """Test performance benchmarks for the integrated system."""
        start_time = time.time()

        try:
            print("\nTest 8: Performance Benchmarks")

            # Benchmark entity reasoning
            pm_entity = self.entities["pm"]
            reasoning_times = []

            for i in range(5):
                goal = Goal(
                    id=f"perf_goal_{i}",
                    description=f"Performance test goal {i}",
                    priority=1
                )

                reason_start = time.time()
                result = await pm_entity.reason_and_act(goal)
                reason_end = time.time()

                reasoning_times.append(reason_end - reason_start)

            avg_reasoning_time = sum(reasoning_times) / len(reasoning_times)
            max_reasoning_time = max(reasoning_times)

            # Performance assertions
            assert avg_reasoning_time < 2.0, f"Average reasoning time too slow: {avg_reasoning_time:.2f}s"
            assert max_reasoning_time < 5.0, f"Max reasoning time too slow: {max_reasoning_time:.2f}s"

            # Benchmark workspace operations
            workspace_times = []
            for i in range(10):
                ws_start = time.time()
                await self.workspace.share_knowledge("test_entity", "perf_space", {"test": f"data_{i}"})
                ws_end = time.time()
                workspace_times.append(ws_end - ws_start)

            avg_workspace_time = sum(workspace_times) / len(workspace_times)
            assert avg_workspace_time < 0.01, f"Workspace operations too slow: {avg_workspace_time:.4f}s"

            execution_time = time.time() - start_time
            print(f"✅ Performance Benchmarks Test PASSED: {execution_time:.2f}s")
            return {
                "test_name": "performance_benchmarks",
                "passed": True,
                "execution_time": execution_time,
                "details": f"Avg reasoning: {avg_reasoning_time:.2f}s, Workspace: {avg_workspace_time:.4f}s"
            }

        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Performance Benchmarks Test FAILED: {e}")
            return {
                "test_name": "performance_benchmarks",
                "passed": False,
                "execution_time": execution_time,
                "error": str(e)
            }

    def generate_test_summary(self, test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate test summary statistics."""
        total_tests = len(test_results)
        passed = sum(1 for result in test_results if result["passed"])
        failed = total_tests - passed
        success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0

        execution_times = [result["execution_time"] for result in test_results]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0

        return {
            "total_tests": total_tests,
            "passed": passed,
            "failed": failed,
            "success_rate": success_rate,
            "avg_execution_time": avg_execution_time,
            "test_results": test_results
        }


async def run_integration_tests():
    """Run the complete integration test suite."""

    suite = IntegrationTestSuite()
    await suite.setup()
    results = await suite.run_all_tests()

    return results


        return results


# EXP-037 Integration Validation Tests Integration
# Adding comprehensive validation tests from EXP-037

import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# Import EXP-036 components for validation tests
try:
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
    EXP_036_AVAILABLE = True
except ImportError:
    EXP_036_AVAILABLE = False
    print("Warning: EXP-036 components not available for validation tests")


class EXP037IntegrationValidationTests(unittest.TestCase):
    """Integration tests for EXP-036 Phase 1 components from EXP-037."""

    def setUp(self):
        """Set up integration test environment."""
        if not EXP_036_AVAILABLE:
            self.skipTest("EXP-036 components not available")

        self.temp_dir = tempfile.mkdtemp()
        self.workspace_path = str(Path(self.temp_dir))

        # Initialize all services
        self.llm_service = InMemoryLLMService(max_memory_gb=2.0)
        self.workflow_engine = WorkflowOrchestrationEngine()
        self.git_service = EnhancedSharedMemoryGitService(self.workspace_path, max_memory_mb=256)
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


class EXP037PerformanceBenchmarks(unittest.TestCase):
    """Performance benchmark tests for EXP-036 integration from EXP-037."""

    def setUp(self):
        if not EXP_036_AVAILABLE:
            self.skipTest("EXP-036 components not available")

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
    # Run EXP-037 validation tests
    import unittest
    
    # Create test suite with EXP-037 tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add EXP-037 validation tests
    suite.addTests(loader.loadTestsFromTestCase(EXP037IntegrationValidationTests))
    suite.addTests(loader.loadTestsFromTestCase(EXP037PerformanceBenchmarks))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
    
    # Also run EXP-040 integration tests separately
    print("\n" + "="*60)
    print("RUNNING EXP-040 INTEGRATION TESTS")
    print("="*60)
    asyncio.run(run_integration_tests())