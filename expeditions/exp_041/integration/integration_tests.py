# DGX Integration Testing Framework (Sub-EXP-041D)
# End-to-end validation of the Manolin Cluster deployment

import asyncio
import json
import logging
import time
import pytest
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import statistics

from manolin_cluster import ManolinCluster, AgentRole, AgentMessage

# Test configuration
NUSY_ROOT = Path("/opt/nusy")
TEST_RESULTS_DIR = NUSY_ROOT / "test_results"
LOG_DIR = NUSY_ROOT / "logs"

class DGXIntegrationTestSuite:
    """Comprehensive integration test suite for DGX deployment"""

    def __init__(self):
        self.cluster: Optional[ManolinCluster] = None
        self.test_results = []
        self.start_time = None
        self.end_time = None

        # Setup logging
        self.logger = logging.getLogger("dgx-integration-tests")
        self.logger.setLevel(logging.INFO)

        handler = logging.FileHandler(LOG_DIR / f"integration_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    async def setup_cluster(self):
        """Initialize the test cluster"""
        self.logger.info("Setting up test cluster...")
        self.cluster = ManolinCluster()
        await self.cluster.start()

        # Create all agent roles
        roles = list(AgentRole)
        for role in roles:
            await self.cluster.create_agent(role)

        self.logger.info("Test cluster setup complete")

    async def teardown_cluster(self):
        """Clean up the test cluster"""
        if self.cluster:
            await self.cluster.stop()
            self.logger.info("Test cluster torn down")

    def record_test_result(self, test_name: str, passed: bool, duration: float,
                          details: Dict[str, Any] = None):
        """Record a test result"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }

        self.test_results.append(result)
        self.logger.info(f"Test {test_name}: {'PASSED' if passed else 'FAILED'} ({duration:.2f}s)")

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run the complete integration test suite"""
        self.start_time = datetime.now()
        self.logger.info("Starting DGX integration test suite")

        try:
            await self.setup_cluster()

            # Run test categories
            await self.test_basic_cluster_operations()
            await self.test_agent_specialization()
            await self.test_concurrency_and_isolation()
            await self.test_model_runtime_performance()
            await self.test_end_to_end_workflows()
            await self.test_failure_recovery()
            await self.test_performance_under_load()

            # Generate final report
            report = await self.generate_test_report()

        finally:
            await self.teardown_cluster()

        self.end_time = datetime.now()
        return report

    async def test_basic_cluster_operations(self):
        """Test basic cluster startup and agent management"""
        test_start = time.time()

        try:
            # Verify cluster status
            status = await self.cluster.get_status()
            assert status["is_running"] == True
            assert status["agent_count"] == 7  # All 7 roles

            # Verify all agent roles are present
            expected_roles = {role.value for role in AgentRole}
            actual_roles = set(status["agents"].values())
            assert expected_roles == actual_roles

            # Test agent session creation
            pm_agent = self.cluster.agents["pm_1"]
            session_id = await pm_agent.create_session()
            assert session_id in pm_agent.sessions

            self.record_test_result("basic_cluster_operations", True, time.time() - test_start)

        except Exception as e:
            self.record_test_result("basic_cluster_operations", False, time.time() - test_start,
                                  {"error": str(e)})

    async def test_agent_specialization(self):
        """Test that agents have correct role-specific capabilities"""
        test_start = time.time()

        try:
            # Test each agent has appropriate capabilities
            for agent_id, agent in self.cluster.agents.items():
                session_id = await agent.create_session()

                # Test role-specific tool access
                if agent.role == AgentRole.DEVELOPER:
                    # Developer should have code-related tools
                    message = AgentMessage(
                        from_agent="test",
                        session_id=session_id,
                        message_type="tool_call",
                        payload={"tool": "code_generation", "parameters": {}}
                    )
                    response = await agent.process_message(message)
                    assert response.message_type == "tool_response"

                elif agent.role == AgentRole.QA_SPECIALIST:
                    # QA should have testing tools
                    message = AgentMessage(
                        from_agent="test",
                        session_id=session_id,
                        message_type="tool_call",
                        payload={"tool": "test_execution", "parameters": {}}
                    )
                    response = await agent.process_message(message)
                    assert response.message_type == "tool_response"

            self.record_test_result("agent_specialization", True, time.time() - test_start)

        except Exception as e:
            self.record_test_result("agent_specialization", False, time.time() - test_start,
                                  {"error": str(e)})

    async def test_concurrency_and_isolation(self):
        """Test concurrent agent operations with session isolation"""
        test_start = time.time()

        try:
            # Create multiple concurrent sessions
            tasks = []
            for i in range(10):
                agent_id = f"pm_{(i % 3) + 1}"  # Use first 3 PM agents
                agent = self.cluster.agents[agent_id]

                async def run_session(agent, session_num):
                    session_id = await agent.create_session({"test_session": session_num})
                    message = AgentMessage(
                        from_agent="test",
                        session_id=session_id,
                        message_type="inference_request",
                        payload={"prompt": f"Test prompt {session_num}"}
                    )
                    response = await agent.process_message(message)
                    return response

                tasks.append(run_session(agent, i))

            # Run all sessions concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Verify all sessions completed without cross-contamination
            successful_results = [r for r in results if not isinstance(r, Exception)]
            assert len(successful_results) == 10

            # Verify session isolation (no shared context)
            session_contexts = []
            for agent in self.cluster.agents.values():
                for session in agent.sessions.values():
                    session_contexts.append(session.context)

            # Each session should have unique context
            unique_contexts = set(str(ctx) for ctx in session_contexts)
            assert len(unique_contexts) >= 7  # At least one per agent

            self.record_test_result("concurrency_and_isolation", True, time.time() - test_start)

        except Exception as e:
            self.record_test_result("concurrency_and_isolation", False, time.time() - test_start,
                                  {"error": str(e)})

    async def test_model_runtime_performance(self):
        """Test shared model runtime performance"""
        test_start = time.time()

        try:
            # Test inference latency
            latencies = []
            for i in range(20):
                agent = self.cluster.agents["pm_1"]
                session_id = await agent.create_session()

                start_time = time.time()
                message = AgentMessage(
                    from_agent="test",
                    session_id=session_id,
                    message_type="inference_request",
                    payload={"prompt": f"Performance test {i}"}
                )
                response = await agent.process_message(message)
                end_time = time.time()

                latencies.append(end_time - start_time)
                assert response is not None

            # Calculate performance metrics
            avg_latency = statistics.mean(latencies)
            p95_latency = statistics.quantiles(latencies, n=20)[18]  # 95th percentile

            # Performance requirements (adjust based on hardware)
            assert avg_latency < 2.0  # Average under 2 seconds
            assert p95_latency < 6.0  # P95 under 6 seconds

            self.record_test_result("model_runtime_performance", True, time.time() - test_start,
                                  {"avg_latency": avg_latency, "p95_latency": p95_latency})

        except Exception as e:
            self.record_test_result("model_runtime_performance", False, time.time() - test_start,
                                  {"error": str(e)})

    async def test_end_to_end_workflows(self):
        """Test complete feature development workflows"""
        test_start = time.time()

        try:
            # Simulate a feature development workflow
            # 1. PM creates feature specification
            pm_agent = self.cluster.agents["pm_1"]
            pm_session = await pm_agent.create_session({"project": "test_feature"})

            pm_message = AgentMessage(
                from_agent="test",
                session_id=pm_session,
                message_type="inference_request",
                payload={"prompt": "Create a feature specification for user authentication"}
            )
            pm_response = await pm_agent.process_message(pm_message)

            # 2. Architect reviews and designs
            arch_agent = self.cluster.agents["architect-systems_1"]
            arch_session = await arch_agent.create_session({"feature_spec": pm_response.payload})

            arch_message = AgentMessage(
                from_agent="test",
                session_id=arch_session,
                message_type="inference_request",
                payload={"prompt": "Design the system architecture for this authentication feature"}
            )
            arch_response = await arch_agent.process_message(arch_message)

            # 3. Developer implements
            dev_agent = self.cluster.agents["developer_1"]
            dev_session = await dev_agent.create_session({
                "feature_spec": pm_response.payload,
                "architecture": arch_response.payload
            })

            dev_message = AgentMessage(
                from_agent="test",
                session_id=dev_session,
                message_type="inference_request",
                payload={"prompt": "Implement the authentication feature based on the spec and architecture"}
            )
            dev_response = await dev_agent.process_message(dev_message)

            # 4. QA tests
            qa_agent = self.cluster.agents["qa_1"]
            qa_session = await qa_agent.create_session({"implementation": dev_response.payload})

            qa_message = AgentMessage(
                from_agent="test",
                session_id=qa_session,
                message_type="inference_request",
                payload={"prompt": "Create comprehensive tests for the authentication feature"}
            )
            qa_response = await qa_agent.process_message(qa_message)

            # Verify workflow completed successfully
            assert all([pm_response, arch_response, dev_response, qa_response])

            self.record_test_result("end_to_end_workflows", True, time.time() - test_start)

        except Exception as e:
            self.record_test_result("end_to_end_workflows", False, time.time() - test_start,
                                  {"error": str(e)})

    async def test_failure_recovery(self):
        """Test system behavior under failure conditions"""
        test_start = time.time()

        try:
            # Test session cleanup
            agent = self.cluster.agents["pm_1"]

            # Create several sessions
            session_ids = []
            for i in range(5):
                session_id = await agent.create_session({"test": i})
                session_ids.append(session_id)

            # Manually expire some sessions
            for i in range(3):
                session = agent.sessions[session_ids[i]]
                session.last_activity = datetime.now() - timedelta(hours=2)

            # Trigger cleanup
            await agent._cleanup_expired_sessions()

            # Verify expired sessions were cleaned up
            active_sessions = len(agent.sessions)
            assert active_sessions <= 2  # At least 3 should be cleaned up

            self.record_test_result("failure_recovery", True, time.time() - test_start)

        except Exception as e:
            self.record_test_result("failure_recovery", False, time.time() - test_start,
                                  {"error": str(e)})

    async def test_performance_under_load(self):
        """Test system performance under sustained load"""
        test_start = time.time()
        test_duration = 60  # 1 minute load test

        try:
            async def load_worker(worker_id: int):
                """Worker that continuously sends requests"""
                agent = self.cluster.agents[f"pm_{(worker_id % 3) + 1}"]
                request_count = 0

                start_time = time.time()
                while time.time() - start_time < test_duration:
                    try:
                        session_id = await agent.create_session({"worker": worker_id})
                        message = AgentMessage(
                            from_agent=f"worker_{worker_id}",
                            session_id=session_id,
                            message_type="inference_request",
                            payload={"prompt": f"Load test request {request_count}"}
                        )
                        response = await agent.process_message(message)
                        request_count += 1
                        await asyncio.sleep(0.1)  # Small delay between requests
                    except Exception as e:
                        self.logger.warning(f"Worker {worker_id} error: {e}")
                        await asyncio.sleep(1)

                return request_count

            # Start multiple workers
            num_workers = 5
            workers = [load_worker(i) for i in range(num_workers)]
            results = await asyncio.gather(*workers)

            total_requests = sum(results)
            avg_requests_per_second = total_requests / test_duration

            # Performance requirements
            assert avg_requests_per_second >= 10  # At least 10 requests/second under load

            self.record_test_result("performance_under_load", True, time.time() - test_start,
                                  {"total_requests": total_requests, "avg_rps": avg_requests_per_second})

        except Exception as e:
            self.record_test_result("performance_under_load", False, time.time() - test_start,
                                  {"error": str(e)})

    async def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["passed"])
        failed_tests = total_tests - passed_tests

        total_duration = sum(r["duration"] for r in self.test_results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0

        report = {
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                "total_duration": total_duration,
                "average_duration": avg_duration,
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None
            },
            "results": self.test_results,
            "cluster_status": await self.cluster.get_status() if self.cluster else None,
            "recommendations": self._generate_recommendations()
        }

        # Save report to file
        TEST_RESULTS_DIR.mkdir(exist_ok=True)
        report_file = TEST_RESULTS_DIR / f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        self.logger.info(f"Test report saved to {report_file}")
        return report

    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []

        failed_tests = [r for r in self.test_results if not r["passed"]]

        if failed_tests:
            recommendations.append(f"Address {len(failed_tests)} failed tests before deployment")

        # Performance recommendations
        perf_tests = [r for r in self.test_results if "performance" in r["test_name"].lower()]
        for test in perf_tests:
            if test["passed"] and "details" in test:
                details = test["details"]
                if "avg_latency" in details and details["avg_latency"] > 1.0:
                    recommendations.append("Consider optimizing model inference latency")

        if not failed_tests:
            recommendations.append("All tests passed - ready for production deployment")

        return recommendations

async def run_integration_tests():
    """Main entry point for running integration tests"""
    test_suite = DGXIntegrationTestSuite()

    try:
        report = await test_suite.run_all_tests()

        print("\n" + "="*60)
        print("DGX INTEGRATION TEST RESULTS")
        print("="*60)
        print(f"Total Tests: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['passed']}")
        print(f"Failed: {report['summary']['failed']}")
        print(".1f")
        print(".2f")
        print("\nRecommendations:")
        for rec in report["recommendations"]:
            print(f"• {rec}")

        return report["summary"]["success_rate"] == 100.0

    except Exception as e:
        print(f"Integration test suite failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_integration_tests())
    exit(0 if success else 1)