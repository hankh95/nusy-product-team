"""
Tests for PR Workflow Manager (F-030 Phase 1)
"""

import pytest
from pathlib import Path
from src.nusy_pm_core.adapters.pr_workflow_manager import PRWorkflowManager


class TestPRWorkflowManager:
    """Test PR creation and issue linking functionality."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create PR workflow manager with test repo."""
        return PRWorkflowManager(tmp_path)
    
    def test_get_current_branch(self, manager, monkeypatch):
        """Test getting current git branch."""
        # Mock subprocess to return test branch
        import subprocess
        
        def mock_run(*args, **kwargs):
            class Result:
                stdout = "feature/test-branch\n"
                returncode = 0
            return Result()
        
        monkeypatch.setattr(subprocess, 'run', mock_run)
        
        branch = manager._get_current_branch()
        assert branch == "feature/test-branch"
    
    def test_build_pr_body(self, manager):
        """Test PR body generation."""
        body = manager._build_pr_body(
            issue_number=42,
            work_summary="Implemented feature X with tests",
            acceptance_criteria=["Feature works", "Tests pass"],
            session_log_path="logs/session-123.md",
            commits=["abc123: Add feature", "def456: Add tests"],
            tests_passing=True
        )
        
        assert "Closes #42" in body
        assert "Implemented feature X with tests" in body
        assert "[x] Feature works" in body
        assert "[x] Tests pass" in body
        assert "abc123: Add feature" in body
        assert "✅ All tests passing" in body
        assert "session-123.md" in body
    
    def test_build_pr_body_minimal(self, manager):
        """Test PR body with minimal information."""
        body = manager._build_pr_body(
            issue_number=42,
            work_summary="Basic work",
            acceptance_criteria=None,
            session_log_path=None,
            commits=[],
            tests_passing=False
        )
        
        assert "Closes #42" in body
        assert "Basic work" in body
        assert "⚠️ Tests need attention" in body
        assert "Review Checklist" in body


class TestPRBodyFormat:
    """Test PR body formatting adheres to standards."""
    
    def test_pr_body_has_required_sections(self):
        """Verify PR body has all required sections."""
        manager = PRWorkflowManager(Path.cwd())
        
        body = manager._build_pr_body(
            issue_number=1,
            work_summary="Test",
            acceptance_criteria=["A", "B"],
            session_log_path="test.md",
            commits=["commit1"],
            tests_passing=True
        )
        
        required_sections = [
            "## Work Summary",
            "## Session Context",
            "## Acceptance Criteria",
            "## Commits",
            "## Test Status",
            "## Review Checklist"
        ]
        
        for section in required_sections:
            assert section in body, f"Missing required section: {section}"
    
    def test_pr_body_issue_linking(self):
        """Verify PR body uses correct issue linking syntax."""
        manager = PRWorkflowManager(Path.cwd())
        
        body = manager._build_pr_body(
            issue_number=42,
            work_summary="Test",
            acceptance_criteria=None,
            session_log_path=None,
            commits=[],
            tests_passing=True
        )
        
        # GitHub recognizes "Closes #N" syntax
        assert body.startswith("Closes #42\n") or body.startswith("Closes #42 ")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
