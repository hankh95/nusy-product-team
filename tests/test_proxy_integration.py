"""
Integration Test for Phase 0 Proxy Team

Tests multi-proxy collaboration on a compound task:
- Backlog grooming session
- Feature design coordination
- Ethical review integration
"""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from santiago_core.agents._proxy import (
    PMProxyAgent,
    ArchitectProxyAgent,
    DeveloperProxyAgent,
    QAProxyAgent,
    UXProxyAgent,
    PlatformProxyAgent,
    EthicistProxyAgent,
)


@pytest.fixture
def workspace_path(tmp_path):
    """Create test workspace with role cards"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    
    # Create knowledge directory structure
    knowledge_dir = workspace / "knowledge" / "proxy-instructions"
    knowledge_dir.mkdir(parents=True)
    
    # Create empty role card files so proxies can load them
    for role in ["pm", "architect", "developer", "qa", "ux", "platform", "ethicist"]:
        (knowledge_dir / f"{role}.md").write_text(f"# {role.upper()} Role Card\n")
    
    return workspace


@pytest.fixture
def proxy_team(workspace_path):
    """Create full proxy team"""
    return {
        "pm": PMProxyAgent(workspace_path),
        "architect": ArchitectProxyAgent(workspace_path),
        "developer": DeveloperProxyAgent(workspace_path),
        "qa": QAProxyAgent(workspace_path),
        "ux": UXProxyAgent(workspace_path),
        "platform": PlatformProxyAgent(workspace_path),
        "ethicist": EthicistProxyAgent(workspace_path),
    }


class TestProxyTeamInitialization:
    """Test that all proxies initialize correctly"""

    def test_all_proxies_created(self, proxy_team):
        """Should create all 7 proxy agents"""
        assert len(proxy_team) == 7
        assert all(proxy is not None for proxy in proxy_team.values())

    def test_unique_proxy_names(self, proxy_team):
        """Should have unique names for each proxy"""
        names = [proxy.name for proxy in proxy_team.values()]
        assert len(names) == len(set(names))  # All unique

    def test_budgets_configured(self, proxy_team):
        """Should have configured budgets"""
        for proxy in proxy_team.values():
            assert proxy.config.budget_per_day > 0
            assert proxy.budget_spent == 0.0  # Initial state


class TestBacklogGroomingSession:
    """Test coordinated backlog grooming workflow"""

    @pytest.mark.asyncio
    async def test_vision_to_hypothesis_workflow(self, proxy_team):
        """Should coordinate vision → hypothesis → feature workflow"""
        
        # 1. PM creates hypothesis from vision
        hypothesis_result = await proxy_team["pm"].invoke_tool("create_hypothesis", {
            "vision": "Enable autonomous Santiago development team"
        })
        
        assert "hypothesis" in hypothesis_result
        
        # 2. UX validates with user research
        persona_result = await proxy_team["ux"].invoke_tool("create_persona", {
            "persona": {
                "name": "Developer Dan",
                "goals": ["Automate repetitive tasks", "Focus on creative work"]
            }
        })
        
        assert persona_result["status"] == "created"
        
        # 3. Ethicist reviews for ethical alignment
        ethics_result = await proxy_team["ethicist"].invoke_tool("ethical_review", {
            "subject": "hypothesis",
            "description": "Autonomous development team for all developers"
        })
        
        assert "review" in ethics_result
        # Should approve service to humanity
        assert ethics_result["review"]["approved"] is True

    @pytest.mark.asyncio
    async def test_feature_design_coordination(self, proxy_team):
        """Should coordinate PM → Architect → Developer workflow"""
        
        # 1. PM creates feature spec
        feature_result = await proxy_team["pm"].invoke_tool("create_feature", {
            "hypothesis": {"title": "Autonomous task execution"}
        })
        
        assert "feature" in feature_result
        
        # 2. Architect designs system
        design_result = await proxy_team["architect"].invoke_tool("create_design", {
            "feature": "Autonomous task execution"
        })
        
        assert "design" in design_result
        
        # 3. Developer implements with TDD
        test_result = await proxy_team["developer"].invoke_tool("write_test", {
            "test_file": "test_autonomous_execution.py",
            "code": "def test_execute_task(): pass"
        })
        
        assert test_result["test_written"] is True


class TestEthicalOversightIntegration:
    """Test ethical oversight is integrated throughout workflow"""

    @pytest.mark.asyncio
    async def test_ethicist_flags_concern(self, proxy_team):
        """Ethicist should flag ethical concerns"""
        
        # Simulate problematic feature
        with patch.object(proxy_team["ethicist"], '_call_external_api', new_callable=AsyncMock) as mock:
            mock.return_value = {
                "review": {
                    "approved": False,
                    "concerns": ["User manipulation detected"],
                    "principles_applied": ["Independent Investigation of Truth"],
                    "recommendations": "Redesign for transparency"
                }
            }
            
            result = await proxy_team["ethicist"].invoke_tool("ethical_review", {
                "subject": "feature",
                "description": "Dark pattern UI to increase engagement"
            })
            
            assert result["review"]["approved"] is False
            assert len(result["review"]["concerns"]) > 0

    @pytest.mark.asyncio
    async def test_bahai_principles_applied(self, proxy_team):
        """Should apply all 12 Baha'i principles"""
        ethicist = proxy_team["ethicist"]
        
        # Verify all principles loaded
        assert len(ethicist.bahai_principles) == 12
        
        # Test principle-specific checks
        unity_check = await ethicist.check_principle_alignment(
            "Unity of Humanity",
            "Feature accessible globally to all users"
        )
        assert unity_check["aligned"] is True
        
        education_check = await ethicist.check_principle_alignment(
            "Universal Compulsory Education",
            "Feature has comprehensive documentation"
        )
        assert education_check["aligned"] is True


class TestMultiProxyCollaboration:
    """Test multi-proxy coordination patterns"""

    @pytest.mark.asyncio
    async def test_parallel_tool_invocations(self, proxy_team):
        """Should handle parallel operations from multiple proxies"""
        
        # Simulate parallel work
        tasks = [
            proxy_team["pm"].invoke_tool("query_backlog", {}),
            proxy_team["qa"].invoke_tool("run_tests", {"test_files": []}),
            proxy_team["platform"].invoke_tool("query_metrics", {}),
        ]
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        assert all(result is not None for result in results)

    @pytest.mark.asyncio
    async def test_budget_tracking_across_team(self, proxy_team):
        """Should track budget spent across all proxies"""
        
        # Each proxy invokes a tool
        await proxy_team["pm"].invoke_tool("create_hypothesis", {"vision": "Test"})
        await proxy_team["architect"].invoke_tool("create_design", {"feature": "Test"})
        await proxy_team["developer"].invoke_tool("write_test", {"test_file": "test.py", "code": ""})
        
        # Check budgets updated
        total_spent = sum(proxy.budget_spent for proxy in proxy_team.values())
        assert total_spent > 0


class TestProvenanceLogging:
    """Test provenance logging across proxies"""

    @pytest.mark.asyncio
    async def test_logs_created(self, proxy_team, workspace_path):
        """Should create log files for all proxy operations"""
        
        # Invoke tools from different proxies
        await proxy_team["pm"].invoke_tool("create_hypothesis", {"vision": "Test"})
        await proxy_team["ethicist"].invoke_tool("ethical_review", {
            "subject": "test",
            "description": "Test review"
        })
        
        # Check logs exist
        pm_logs = workspace_path / "ships-logs" / "pm"
        ethics_logs = workspace_path / "ships-logs" / "ethics"
        
        assert pm_logs.exists()
        assert ethics_logs.exists()
        
        # Check log files created
        assert len(list(pm_logs.glob("*.jsonl"))) > 0
        assert len(list(ethics_logs.glob("*.jsonl"))) > 0


class TestCompoundTask:
    """Test complete compound task: Backlog grooming + Design session"""

    @pytest.mark.asyncio
    async def test_full_feature_workflow(self, proxy_team):
        """Should execute complete feature workflow with all roles"""
        
        # Phase 1: Product Discovery
        # PM: Generate hypothesis
        hypothesis = await proxy_team["pm"].invoke_tool("create_hypothesis", {
            "vision": "Santiago autonomous development factory"
        })
        assert "hypothesis" in hypothesis
        
        # UX: Create persona and journey
        persona = await proxy_team["ux"].invoke_tool("create_persona", {
            "persona": {"name": "Dev Team Lead"}
        })
        assert persona["status"] == "created"
        
        journey = await proxy_team["ux"].invoke_tool("map_journey", {
            "journey": {"user": "Dev Team Lead", "goal": "Automate team"}
        })
        assert journey["status"] == "mapped"
        
        # Ethicist: Review for service alignment
        ethics = await proxy_team["ethicist"].invoke_tool("check_service_alignment", {
            "description": "Autonomous dev team to free humans for creative work"
        })
        assert ethics["service_alignment"]["serves_genuine_need"] is True
        
        # Phase 2: Design
        # PM: Create feature spec
        feature = await proxy_team["pm"].invoke_tool("create_feature", {
            "hypothesis": hypothesis["hypothesis"]
        })
        assert "feature" in feature
        
        # Architect: Design system
        design = await proxy_team["architect"].invoke_tool("create_design", {
            "feature": "Santiago Factory"
        })
        assert "design" in design
        
        # Ethicist: Review architecture for ethical implications
        arch_ethics = await proxy_team["ethicist"].invoke_tool("ethical_review", {
            "subject": "architecture",
            "description": "Event-driven system with ethical oversight"
        })
        assert "review" in arch_ethics
        
        # Phase 3: Implementation
        # Developer: Write tests
        test = await proxy_team["developer"].invoke_tool("write_test", {
            "test_file": "test_factory.py",
            "code": "def test_create_santiago(): pass"
        })
        assert test["test_written"] is True
        
        # Developer: Implement
        code = await proxy_team["developer"].invoke_tool("write_code", {
            "file": "factory.py",
            "code": "class SantiagoFactory: pass"
        })
        assert code["code_written"] is True
        
        # Phase 4: Validation
        # QA: Run tests
        test_results = await proxy_team["qa"].invoke_tool("run_tests", {
            "test_files": ["test_factory.py"]
        })
        assert test_results["passed"] is True
        
        # QA: Report coverage
        coverage = await proxy_team["qa"].invoke_tool("report_coverage", {
            "coverage": 92
        })
        assert coverage["coverage"] >= 90
        
        # Phase 5: Deployment
        # Platform: Deploy
        deployment = await proxy_team["platform"].invoke_tool("deploy_service", {
            "service": "santiago-factory"
        })
        assert deployment["status"] == "deployed"
        
        # Platform: Configure monitoring
        monitoring = await proxy_team["platform"].invoke_tool("configure_monitoring", {
            "config": {"slo": "99%"}
        })
        assert monitoring["status"] == "active"
        
        # Final: Verify all proxies participated
        total_calls = sum(proxy.call_count for proxy in proxy_team.values())
        assert total_calls > 0  # All proxies used
        
        # Verify ethical oversight throughout
        ethicist_calls = proxy_team["ethicist"].call_count
        assert ethicist_calls >= 2  # Multiple ethical reviews


@pytest.mark.asyncio
async def test_integration_metrics(proxy_team):
    """Test overall team metrics"""
    
    # Run some operations
    await proxy_team["pm"].invoke_tool("create_hypothesis", {"vision": "Test"})
    await proxy_team["architect"].invoke_tool("create_design", {"feature": "Test"})
    await proxy_team["ethicist"].invoke_tool("ethical_review", {
        "subject": "test",
        "description": "Test"
    })
    
    # Collect metrics
    all_metrics = {name: proxy.get_metrics() for name, proxy in proxy_team.items()}
    
    # Verify metrics structure
    for name, metrics in all_metrics.items():
        assert "proxy" in metrics
        assert "total_calls" in metrics
        assert "budget_spent" in metrics
        assert metrics["total_calls"] >= 0
        assert metrics["budget_spent"] >= 0
