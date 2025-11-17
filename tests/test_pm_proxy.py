"""
Test suite for PM Proxy Agent

Tests the Product Manager proxy that delegates to external APIs
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from santiago_core.agents._proxy.pm_proxy import PMProxyAgent
from santiago_core.agents._proxy.base_proxy import MCPTool, MCPManifest, ProxyConfig
from santiago_core.core.agent_framework import Message, Task


@pytest.fixture
def workspace_path(tmp_path):
    """Create temporary workspace"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def pm_proxy(workspace_path):
    """Create PM proxy instance"""
    return PMProxyAgent(workspace_path)


class TestPMProxyInitialization:
    """Test PM proxy initialization"""

    def test_pm_proxy_creation(self, pm_proxy):
        """Should initialize with PM-specific manifest"""
        assert pm_proxy.name == "pm-proxy"
        assert pm_proxy.manifest.role == "product_manager"
        assert "hypothesis_generation" in pm_proxy.manifest.capabilities

    def test_pm_tools_available(self, pm_proxy):
        """Should have PM-specific tools"""
        tool_names = [tool.name for tool in pm_proxy.manifest.input_tools]
        assert "read_hypothesis" in tool_names
        assert "query_user_needs" in tool_names

    def test_pm_output_tools(self, pm_proxy):
        """Should have PM output tools"""
        tool_names = [tool.name for tool in pm_proxy.manifest.output_tools]
        assert "create_hypothesis" in tool_names
        assert "create_feature" in tool_names
        assert "update_backlog" in tool_names


class TestPMHypothesisGeneration:
    """Test PM hypothesis generation"""

    @pytest.mark.asyncio
    async def test_generate_hypothesis(self, pm_proxy):
        """Should generate hypothesis from vision"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "hypothesis": {
                    "title": "Santiago Autonomous Team",
                    "description": "Enable autonomous development",
                    "success_criteria": "Complete features without human intervention",
                }
            }

            result = await pm_proxy.invoke_tool("create_hypothesis", {
                "vision": "Build autonomous development team"
            })

            assert result["hypothesis"]["title"] == "Santiago Autonomous Team"
            assert "autonomous" in result["hypothesis"]["description"]

    @pytest.mark.asyncio
    async def test_hypothesis_to_feature(self, pm_proxy):
        """Should convert hypothesis to BDD feature"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "feature": {
                    "title": "Autonomous Task Execution",
                    "scenarios": [
                        {
                            "name": "Execute task without supervision",
                            "given": "Santiago team is initialized",
                            "when": "Task is assigned",
                            "then": "Task completes successfully",
                        }
                    ]
                }
            }

            result = await pm_proxy.invoke_tool("create_feature", {
                "hypothesis": {"title": "Autonomous execution"}
            })

            assert "feature" in result
            assert len(result["feature"]["scenarios"]) > 0


class TestPMBacklogManagement:
    """Test PM backlog operations"""

    @pytest.mark.asyncio
    async def test_update_backlog(self, pm_proxy):
        """Should update feature backlog"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "status": "success",
                "backlog_updated": True
            }

            result = await pm_proxy.invoke_tool("update_backlog", {
                "feature_id": "feat_001",
                "priority": "high"
            })

            assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_query_backlog(self, pm_proxy):
        """Should query backlog status"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "backlog": [
                    {"id": "feat_001", "status": "specified"},
                    {"id": "feat_002", "status": "in_progress"},
                ]
            }

            result = await pm_proxy.invoke_tool("query_backlog", {})

            assert len(result["backlog"]) == 2


class TestPMTeamCoordination:
    """Test PM team coordination"""

    @pytest.mark.asyncio
    async def test_message_architect(self, pm_proxy):
        """Should send design request to architect"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "message_sent": True,
                "recipient": "architect-proxy"
            }

            result = await pm_proxy.invoke_tool("message_role", {
                "role": "architect",
                "content": "Please design system for feature X"
            })

            assert result["message_sent"] is True

    @pytest.mark.asyncio
    async def test_broadcast_hypothesis(self, pm_proxy):
        """Should broadcast hypothesis to team"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "broadcast": True,
                "recipients": ["architect", "developer", "ux"]
            }

            result = await pm_proxy.invoke_tool("message_team", {
                "content": "New hypothesis available for review"
            })

            assert result["broadcast"] is True


class TestPMLeanPractices:
    """Test PM Lean UX practices"""

    @pytest.mark.asyncio
    async def test_create_user_story_map(self, pm_proxy):
        """Should create user story map"""
        with patch.object(pm_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "story_map": {
                    "backbone": ["Discover", "Learn", "Execute"],
                    "stories": [
                        {"activity": "Discover", "story": "As PM, identify user need"},
                        {"activity": "Learn", "story": "As PM, validate hypothesis"},
                    ]
                }
            }

            result = await pm_proxy.invoke_tool("create_story_map", {
                "feature": "Santiago Development Workflow"
            })

            assert "story_map" in result
            assert len(result["story_map"]["backbone"]) > 0
