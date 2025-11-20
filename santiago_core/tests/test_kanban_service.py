"""
Test suite for Santiago Kanban Service

Tests the Kanban MCP service functionality including issue closing
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from santiago_core.services.kanban_service import SantiagoKanbanService
from santiago_core.core.mcp_service import MCPToolResult


@pytest.fixture
def workspace_path(tmp_path):
    """Create temporary workspace"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def kanban_service(workspace_path):
    """Create kanban service instance"""
    return SantiagoKanbanService(workspace_path)


class TestKanbanCloseIssue:
    """Test kanban_close_issue tool functionality"""

    @pytest.mark.asyncio
    async def test_close_issue_success(self, kanban_service):
        """Should successfully close an issue by moving card to done"""
        # Mock the kanban service methods
        with patch.object(kanban_service.kanban_service, 'move_card_with_validation') as mock_move, \
             patch.object(kanban_service.kanban_service, 'add_comment_to_card') as mock_comment:

            mock_move.return_value = {"success": True, "card_id": "test-card-123"}

            # Test parameters
            params = {
                "board_id": "test-board",
                "card_id": "test-card-123",
                "closed_by": "santiago-developer",
                "close_reason": "Work completed following full development workflow"
            }

            # Call the handler
            result = await kanban_service._handle_close_issue(params)

            # Verify the result
            assert isinstance(result, MCPToolResult)
            assert result.error is None  # No error
            assert result.result is not None
            assert result.result["success"] is True
            assert result.result["card_id"] == "test-card-123"
            assert result.result["moved_to"] == "done"
            assert result.result["closed_by"] == "santiago-developer"

            # Verify the kanban service was called correctly
            mock_move.assert_called_once()
            args = mock_move.call_args[1]  # Get keyword arguments
            assert args["board_id"] == "test-board"
            assert args["card_id"] == "test-card-123"
            assert str(args["new_column"]) == "ColumnType.DONE"  # Check string representation
            assert args["moved_by"] == "santiago-developer"
            assert args["reason"] == "Work completed following full development workflow"

            # Verify comment was added
            mock_comment.assert_called_once_with(
                board_id="test-board",
                card_id="test-card-123",
                comment_text="✅ Issue closed by santiago-developer. Work completed following full development workflow",
                author="santiago-developer"
            )

    @pytest.mark.asyncio
    async def test_close_issue_with_defaults(self, kanban_service):
        """Should use default values when optional parameters not provided"""
        with patch.object(kanban_service.kanban_service, 'move_card_with_validation') as mock_move, \
             patch.object(kanban_service.kanban_service, 'add_comment_to_card') as mock_comment:

            mock_move.return_value = {"success": True, "card_id": "test-card-456"}

            # Test with minimal parameters
            params = {
                "board_id": "test-board",
                "card_id": "test-card-456"
            }

            result = await kanban_service._handle_close_issue(params)

            assert result.result["success"] is True
            assert result.result["closed_by"] == "santiago-developer"  # default value

            # Verify comment uses defaults
            mock_comment.assert_called_once_with(
                board_id="test-board",
                card_id="test-card-456",
                comment_text="✅ Issue closed by santiago-developer. Work completed successfully.",
                author="santiago-developer"
            )

    @pytest.mark.asyncio
    async def test_close_issue_failure(self, kanban_service):
        """Should handle errors when closing issue fails"""
        with patch.object(kanban_service.kanban_service, 'move_card_with_validation') as mock_move:
            mock_move.side_effect = Exception("Card not found")

            params = {
                "board_id": "test-board",
                "card_id": "nonexistent-card"
            }

            result = await kanban_service._handle_close_issue(params)

            assert isinstance(result, MCPToolResult)
            assert result.error is not None
            assert "Failed to close issue nonexistent-card" in result.error

    @pytest.mark.asyncio
    async def test_close_issue_tool_registration(self, kanban_service):
        """Should have kanban_close_issue tool registered"""
        # kanban_service.tools is a dict[str, MCPTool]
        assert "kanban_close_issue" in kanban_service.tools
        close_tool = kanban_service.tools["kanban_close_issue"]

        # Verify parameters
        assert "board_id" in close_tool.parameters
        assert "card_id" in close_tool.parameters
        assert close_tool.parameters["closed_by"]["required"] is False
        assert close_tool.parameters["close_reason"]["required"] is False

    @pytest.mark.asyncio
    async def test_close_issue_via_tool_call(self, kanban_service):
        """Should handle kanban_close_issue through the main tool call interface"""
        with patch.object(kanban_service, '_handle_close_issue') as mock_handler:
            mock_handler.return_value = MCPToolResult(result={"success": True})

            params = {
                "board_id": "test-board",
                "card_id": "test-card"
            }

            result = await kanban_service.handle_tool_call("kanban_close_issue", params)

            mock_handler.assert_called_once_with(params)
            assert result.result["success"] is True