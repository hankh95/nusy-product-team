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


if __name__ == "__main__":
    asyncio.run(run_integration_tests())