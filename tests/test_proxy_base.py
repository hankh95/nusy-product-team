"""
Test suite for Proxy Agent Base Framework

Following TDD workflow: write tests first, then implement
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel

from santiago_core.agents._proxy.base_proxy import (
    MCPTool,
    MCPManifest,
    ProxyConfig,
    BaseProxyAgent,
    ProxyBudgetExceeded,
    ProxySessionExpired,
)
from santiago_core.core.agent_framework import Message, Task


class MockProxyAgent(BaseProxyAgent):
    """Mock proxy for testing"""

    async def handle_custom_message(self, message: Message) -> None:
        """Test implementation"""
        pass

    async def start_working_on_task(self, task: Task) -> None:
        """Test implementation"""
        self.logger.info(f"Working on task: {task.title}")

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Test implementation - mock API call"""
        return {"status": "success", "tool": tool_name, "params": params}


@pytest.fixture
def workspace_path(tmp_path):
    """Create temporary workspace"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def proxy_config():
    """Create test proxy configuration"""
    return ProxyConfig(
        role_name="test_proxy",
        api_endpoint="https://api.example.com",
        api_key="test_key",
        budget_per_day=25.0,
        session_ttl_hours=1,
        log_dir="ships-logs/test/"
    )


@pytest.fixture
def mcp_manifest():
    """Create test MCP manifest"""
    return MCPManifest(
        role="test_proxy",
        capabilities=["read", "write", "communicate"],
        input_tools=[
            MCPTool(name="read_data", description="Read test data", parameters={"id": "string"}),
        ],
        output_tools=[
            MCPTool(name="write_data", description="Write test data", parameters={"data": "object"}),
        ],
        communication_tools=[
            MCPTool(name="message_team", description="Send message", parameters={"content": "string"}),
        ],
    )


@pytest.fixture
def mock_proxy(workspace_path, proxy_config, mcp_manifest):
    """Create mock proxy agent"""
    return MockProxyAgent(
        name="test_proxy",
        workspace_path=workspace_path,
        config=proxy_config,
        manifest=mcp_manifest,
    )


class TestMCPModels:
    """Test MCP data models"""

    def test_mcp_tool_creation(self):
        """Should create MCP tool with name and description"""
        tool = MCPTool(
            name="test_tool",
            description="Test tool description",
            parameters={"param1": "string", "param2": "integer"}
        )
        assert tool.name == "test_tool"
        assert tool.description == "Test tool description"
        assert "param1" in tool.parameters

    def test_mcp_manifest_creation(self, mcp_manifest):
        """Should create MCP manifest with tools"""
        assert mcp_manifest.role == "test_proxy"
        assert len(mcp_manifest.capabilities) == 3
        assert len(mcp_manifest.input_tools) == 1
        assert mcp_manifest.input_tools[0].name == "read_data"


class TestProxyConfig:
    """Test proxy configuration"""

    def test_config_creation(self, proxy_config):
        """Should create proxy config with defaults"""
        assert proxy_config.role_name == "test_proxy"
        assert proxy_config.budget_per_day == 25.0
        assert proxy_config.session_ttl_hours == 1

    def test_config_validation(self):
        """Should validate budget is positive"""
        with pytest.raises(ValueError):
            ProxyConfig(
                role_name="test",
                api_endpoint="https://api.example.com",
                api_key="key",
                budget_per_day=-10.0  # Invalid
            )


class TestBaseProxyAgent:
    """Test base proxy agent"""

    def test_proxy_initialization(self, mock_proxy, proxy_config, mcp_manifest):
        """Should initialize proxy with config and manifest"""
        assert mock_proxy.name == "test_proxy"
        assert mock_proxy.config == proxy_config
        assert mock_proxy.manifest == mcp_manifest
        assert mock_proxy.budget_spent == 0.0

    @pytest.mark.asyncio
    async def test_tool_invocation(self, mock_proxy):
        """Should invoke tool and log to ships-logs"""
        result = await mock_proxy.invoke_tool(
            "read_data",
            {"id": "test123"}
        )

        assert result["status"] == "success"
        assert result["tool"] == "read_data"
        assert mock_proxy.budget_spent > 0

    @pytest.mark.asyncio
    async def test_budget_tracking(self, mock_proxy):
        """Should track budget spent per tool call"""
        initial_budget = mock_proxy.budget_spent

        await mock_proxy.invoke_tool("read_data", {"id": "test1"})
        
        assert mock_proxy.budget_spent > initial_budget

    @pytest.mark.asyncio
    async def test_budget_exceeded(self, mock_proxy):
        """Should raise error when budget exceeded"""
        mock_proxy.budget_spent = 30.0  # Exceed daily budget

        with pytest.raises(ProxyBudgetExceeded):
            await mock_proxy.invoke_tool("read_data", {"id": "test"})

    @pytest.mark.asyncio
    async def test_session_expiry(self, mock_proxy):
        """Should track session start and enforce TTL"""
        # Simulate expired session
        mock_proxy.session_start = datetime.now()
        mock_proxy.session_start = mock_proxy.session_start.replace(year=mock_proxy.session_start.year - 1)

        with pytest.raises(ProxySessionExpired):
            await mock_proxy.invoke_tool("read_data", {"id": "test"})

    @pytest.mark.asyncio
    async def test_provenance_logging(self, mock_proxy, workspace_path):
        """Should log all tool calls to ships-logs"""
        await mock_proxy.invoke_tool("read_data", {"id": "test123"})

        log_dir = workspace_path / "ships-logs" / "test"
        assert log_dir.exists()

        # Check log file exists
        log_files = list(log_dir.glob("*.jsonl"))
        assert len(log_files) > 0

    @pytest.mark.asyncio
    async def test_tool_not_in_manifest(self, mock_proxy):
        """Should raise error for unknown tool"""
        with pytest.raises(ValueError, match="not found in manifest"):
            await mock_proxy.invoke_tool("unknown_tool", {})

    @pytest.mark.asyncio
    async def test_session_renewal(self, mock_proxy):
        """Should allow session renewal"""
        old_start = mock_proxy.session_start

        await mock_proxy.renew_session()

        assert mock_proxy.session_start > old_start
        assert mock_proxy.budget_spent == 0.0

    def test_get_manifest_dict(self, mock_proxy):
        """Should return manifest as dictionary"""
        manifest_dict = mock_proxy.get_manifest_dict()

        assert manifest_dict["role"] == "test_proxy"
        assert "capabilities" in manifest_dict
        assert "input_tools" in manifest_dict


class TestProxyIntegration:
    """Test proxy integration with Santiago framework"""

    @pytest.mark.asyncio
    async def test_message_handling(self, mock_proxy):
        """Should handle messages from other agents"""
        message = Message(
            sender="santiago-pm",
            recipient="test_proxy",
            content=json.dumps({"action": "test"}),
            message_type="tool_request"
        )

        await mock_proxy.receive_message(message)
        # Message should be queued
        assert mock_proxy.message_queue.qsize() > 0

    @pytest.mark.asyncio
    async def test_task_assignment(self, mock_proxy):
        """Should handle task assignments"""
        task = Task(
            id="task_001",
            title="Test Task",
            description="Test task for proxy"
        )

        task_message = Message(
            sender="santiago-pm",
            recipient="test_proxy",
            content=task.model_dump_json(),
            message_type="task_assignment"
        )

        await mock_proxy.handle_task_assignment(task_message)

        assert "task_001" in mock_proxy.tasks
        assert mock_proxy.tasks["task_001"].status == "in_progress"


class TestProxyObservability:
    """Test proxy observability and metrics"""

    @pytest.mark.asyncio
    async def test_metrics_collection(self, mock_proxy):
        """Should collect metrics for tool invocations"""
        await mock_proxy.invoke_tool("read_data", {"id": "test1"})
        await mock_proxy.invoke_tool("write_data", {"data": {"test": "value"}})

        metrics = mock_proxy.get_metrics()

        assert metrics["total_calls"] == 2
        assert metrics["budget_spent"] > 0
        assert "read_data" in metrics["calls_by_tool"]
        assert "write_data" in metrics["calls_by_tool"]

    def test_cost_estimation(self, mock_proxy):
        """Should estimate cost per tool call"""
        cost = mock_proxy.estimate_tool_cost("read_data")
        assert cost > 0
        assert isinstance(cost, float)
