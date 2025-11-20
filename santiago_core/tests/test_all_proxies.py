"""
Tests for all 7 proxy agents

Validates that all proxy agents can be instantiated and have
correct manifests, configurations, and routing.
"""

import pytest
from pathlib import Path

from santiago_core.agents._proxy import (
    PMProxyAgent,
    ArchitectProxyAgent,
    DeveloperProxyAgent,
    QAProxyAgent,
    UXProxyAgent,
    PlatformProxyAgent,
    EthicistProxyAgent,
)
from santiago_core.services.llm_router import LLMProvider


class TestAllProxies:
    """Test all 7 proxy agents"""
    
    @pytest.fixture
    def workspace(self, tmp_path):
        """Create test workspace with role cards"""
        workspace = tmp_path / "test_workspace"
        workspace.mkdir()
        
        # Create knowledge/proxy-instructions directory
        instructions_dir = workspace / "knowledge" / "proxy-instructions"
        instructions_dir.mkdir(parents=True)
        
        # Create minimal role cards for each proxy
        role_cards = {
            "pm.md": "# PM Role Card\nProduct Manager",
            "architect.md": "# Architect Role Card\nArchitect",
            "developer.md": "# Developer Role Card\nDeveloper",
            "qa.md": "# QA Role Card\nQA Engineer",
            "ux.md": "# UX Role Card\nUX Researcher",
            "platform.md": "# Platform Role Card\nPlatform Engineer",
            "ethicist.md": "# Ethicist Role Card\nEthicist",
        }
        
        for filename, content in role_cards.items():
            (instructions_dir / filename).write_text(content)
        
        return workspace
    
    def test_pm_proxy_instantiation(self, workspace):
        """Test PM proxy can be created"""
        pm = PMProxyAgent(workspace)
        
        assert pm.name == "pm-proxy"
        assert pm.config.role_name == "pm_proxy"
        assert pm.manifest.role == "product_manager"
        assert len(pm.manifest.capabilities) > 0
        assert hasattr(pm, "llm_router")
    
    def test_architect_proxy_instantiation(self, workspace):
        """Test Architect proxy can be created"""
        architect = ArchitectProxyAgent(workspace)
        
        assert architect.name == "architect-proxy"
        assert architect.config.role_name == "architect_proxy"
        assert architect.manifest.role == "architect"
        assert "system_design" in architect.manifest.capabilities
        assert hasattr(architect, "llm_router")
    
    def test_developer_proxy_instantiation(self, workspace):
        """Test Developer proxy can be created"""
        developer = DeveloperProxyAgent(workspace)
        
        assert developer.name == "developer-proxy"
        assert developer.config.role_name == "developer_proxy"
        assert developer.manifest.role == "developer"
        assert "feature_implementation" in developer.manifest.capabilities
        assert hasattr(developer, "llm_router")
    
    def test_qa_proxy_instantiation(self, workspace):
        """Test QA proxy can be created"""
        qa = QAProxyAgent(workspace)
        
        assert qa.name == "qa-proxy"
        assert qa.config.role_name == "qa_proxy"
        assert qa.manifest.role == "qa"
        assert "test_execution" in qa.manifest.capabilities
        assert hasattr(qa, "llm_router")
    
    def test_ux_proxy_instantiation(self, workspace):
        """Test UX proxy can be created"""
        ux = UXProxyAgent(workspace)
        
        assert ux.name == "ux-proxy"
        assert ux.config.role_name == "ux_proxy"
        assert ux.manifest.role == "ux"
        assert "user_research" in ux.manifest.capabilities
        assert hasattr(ux, "llm_router")
    
    def test_platform_proxy_instantiation(self, workspace):
        """Test Platform proxy can be created"""
        platform = PlatformProxyAgent(workspace)
        
        assert platform.name == "platform-proxy"
        assert platform.config.role_name == "platform_proxy"
        assert platform.manifest.role == "platform"
        assert "infrastructure_management" in platform.manifest.capabilities
        assert hasattr(platform, "llm_router")
    
    def test_ethicist_proxy_instantiation(self, workspace):
        """Test Ethicist proxy can be created"""
        ethicist = EthicistProxyAgent(workspace)
        
        assert ethicist.name == "ethicist-proxy"
        assert ethicist.config.role_name == "ethicist_proxy"
        assert ethicist.manifest.role == "ethicist"
        assert "ethical_review" in ethicist.manifest.capabilities
        assert hasattr(ethicist, "llm_router")
    
    def test_all_proxies_have_llm_routing(self, workspace):
        """Test all proxies have LLM router configured"""
        proxies = [
            PMProxyAgent(workspace),
            ArchitectProxyAgent(workspace),
            DeveloperProxyAgent(workspace),
            QAProxyAgent(workspace),
            UXProxyAgent(workspace),
            PlatformProxyAgent(workspace),
            EthicistProxyAgent(workspace),
        ]
        
        for proxy in proxies:
            assert hasattr(proxy, "llm_router")
            assert proxy.llm_router is not None
    
    def test_xai_proxies_route_to_xai(self, workspace):
        """Test that architect and ethicist route to xAI"""
        import os
        os.environ["REQUIRE_API_KEYS"] = "false"
        
        architect = ArchitectProxyAgent(workspace)
        ethicist = EthicistProxyAgent(workspace)
        
        from santiago_core.services.llm_router import TaskComplexity
        
        arch_config = architect.llm_router.get_config("architect_proxy", TaskComplexity.COMPLEX)
        eth_config = ethicist.llm_router.get_config("ethicist_proxy", TaskComplexity.COMPLEX)
        
        assert arch_config.provider.value == LLMProvider.XAI.value
        assert eth_config.provider.value == LLMProvider.XAI.value
    
    def test_openai_proxies_route_to_openai(self, workspace):
        """Test that dev/qa/platform proxies route to OpenAI"""
        import os
        os.environ["REQUIRE_API_KEYS"] = "false"
        
        developer = DeveloperProxyAgent(workspace)
        qa = QAProxyAgent(workspace)
        platform = PlatformProxyAgent(workspace)
        
        from santiago_core.services.llm_router import TaskComplexity
        
        dev_config = developer.llm_router.get_config("developer_proxy", TaskComplexity.MODERATE)
        qa_config = qa.llm_router.get_config("qa_proxy", TaskComplexity.MODERATE)
        plat_config = platform.llm_router.get_config("platform_proxy", TaskComplexity.MODERATE)
        
        assert dev_config.provider.value == LLMProvider.OPENAI.value
        assert qa_config.provider.value == LLMProvider.OPENAI.value
        assert plat_config.provider.value == LLMProvider.OPENAI.value
    
    def test_all_proxies_have_manifests(self, workspace):
        """Test all proxies have complete manifests"""
        proxies = [
            PMProxyAgent(workspace),
            ArchitectProxyAgent(workspace),
            DeveloperProxyAgent(workspace),
            QAProxyAgent(workspace),
            UXProxyAgent(workspace),
            PlatformProxyAgent(workspace),
            EthicistProxyAgent(workspace),
        ]
        
        for proxy in proxies:
            manifest = proxy.manifest
            assert manifest.role is not None
            assert len(manifest.capabilities) > 0
            assert len(manifest.input_tools) > 0
            assert len(manifest.output_tools) > 0
            assert len(manifest.communication_tools) > 0
    
    def test_all_proxies_disable_budget_by_default(self, workspace):
        """Test budget tracking is disabled by default"""
        import os
        # Ensure env var is not set
        os.environ.pop("PROXY_BUDGET_TRACKING", None)
        
        proxies = [
            PMProxyAgent(workspace),
            ArchitectProxyAgent(workspace),
            DeveloperProxyAgent(workspace),
            QAProxyAgent(workspace),
            UXProxyAgent(workspace),
            PlatformProxyAgent(workspace),
            EthicistProxyAgent(workspace),
        ]
        
        for proxy in proxies:
            assert proxy.config.budget_tracking == False
