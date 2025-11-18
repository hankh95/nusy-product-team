"""
Tests for PR Workflow Manager (F-030 Phases 1-4)
"""

import pytest
import json
from pathlib import Path
from src.nusy_pm_core.adapters.pr_workflow_manager import PRWorkflowManager


class TestPRWorkflowManager:
    """Test PR creation and issue linking functionality (Phase 1)."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create PR workflow manager with test repo."""
        return PRWorkflowManager(tmp_path)
    
    def test_get_current_branch(self, manager, monkeypatch):
        """Test getting current git branch."""
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
    """Test PR body formatting adheres to standards (Phase 1)."""
    
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


class TestReviewWorkflow:
    """Test review workflow automation (Phase 2)."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        return PRWorkflowManager(tmp_path)
    
    def test_check_pr_status_parsing(self, manager, monkeypatch):
        """Test PR status check parses GitHub response correctly."""
        import subprocess
        
        mock_response = {
            'state': 'OPEN',
            'reviewDecision': 'APPROVED',
            'mergeable': 'MERGEABLE',
            'statusCheckRollup': [
                {'conclusion': 'SUCCESS'}
            ]
        }
        
        def mock_run(*args, **kwargs):
            class Result:
                stdout = json.dumps(mock_response)
                returncode = 0
            return Result()
        
        monkeypatch.setattr(subprocess, 'run', mock_run)
        
        status = manager.check_pr_status(123)
        assert status['approved'] is True
        assert status['mergeable'] is True
        assert status['checks_passing'] is True
    
    def test_merge_pr_requires_approval(self, manager, monkeypatch):
        """Test merge fails if PR not approved."""
        import subprocess
        
        def mock_run(*args, **kwargs):
            class Result:
                stdout = json.dumps({
                    'reviewDecision': 'REVIEW_REQUIRED',
                    'mergeable': 'MERGEABLE',
                    'statusCheckRollup': []
                })
                returncode = 0
            return Result()
        
        monkeypatch.setattr(subprocess, 'run', mock_run)
        
        with pytest.raises(RuntimeError, match="not approved"):
            manager.merge_pr(123)


class TestChangesRequestedWorkflow:
    """Test changes requested workflow (Phase 3)."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        return PRWorkflowManager(tmp_path)
    
    def test_handle_changes_requested_groups_by_severity(self, manager, monkeypatch):
        """Test changes requested groups comments by severity."""
        import subprocess
        
        # Mock _get_pr_details
        def mock_get_pr_details(pr_num):
            return {'linked_issue': 42, 'title': 'Test', 'body': ''}
        
        monkeypatch.setattr(manager, '_get_pr_details', mock_get_pr_details)
        
        # Mock subprocess (for gh issue comment)
        call_count = [0]
        captured_comment = ['']
        
        def mock_run(*args, **kwargs):
            call_count[0] += 1
            if 'comment' in args[0]:
                # Capture comment body
                body_idx = args[0].index('--body') + 1
                captured_comment[0] = args[0][body_idx]
            
            class Result:
                stdout = ""
                returncode = 0
            return Result()
        
        monkeypatch.setattr(subprocess, 'run', mock_run)
        
        comments = [
            {'comment': 'Fix bug', 'severity': 'blocker'},
            {'comment': 'Add docs', 'severity': 'minor'},
            {'comment': 'Improve logic', 'severity': 'important'}
        ]
        
        result = manager.handle_changes_requested(123, 'reviewer', comments)
        
        assert result['pr_number'] == 123
        assert result['issue_number'] == 42
        assert result['blocker_count'] == 1
        
        # Check comment has severity grouping
        comment = captured_comment[0]
        assert '🔴' in comment  # blocker
        assert '🟡' in comment  # important
        assert '🟢' in comment  # minor


class TestMetricsAndReporting:
    """Test metrics and reporting (Phase 4)."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        # Create workflow logs directory
        log_dir = tmp_path / 'santiago-pm' / 'workflow-logs'
        log_dir.mkdir(parents=True)
        return PRWorkflowManager(tmp_path)
    
    def test_track_workflow_state(self, manager):
        """Test workflow state tracking."""
        manager.track_workflow_state(42, 'created', {'user': 'test'})
        manager.track_workflow_state(42, 'in_progress')
        
        log_file = manager.repo_path / 'santiago-pm' / 'workflow-logs' / 'issue-42.log'
        assert log_file.exists()
        
        with open(log_file) as f:
            lines = f.readlines()
            assert len(lines) == 2
            
            entry1 = json.loads(lines[0])
            assert entry1['state'] == 'created'
            assert entry1['metadata']['user'] == 'test'
    
    def test_calculate_cycle_time(self, manager):
        """Test cycle time calculation."""
        from datetime import datetime, timedelta, timezone
        
        # Create mock log with timestamps
        log_file = manager.repo_path / 'santiago-pm' / 'workflow-logs' / 'issue-42.log'
        
        now = datetime.now(timezone.utc)
        states = [
            {'timestamp': now.isoformat(), 'state': 'created', 'issue_number': 42, 'metadata': {}},
            {'timestamp': (now + timedelta(hours=2)).isoformat(), 'state': 'pr_created', 'issue_number': 42, 'metadata': {}},
            {'timestamp': (now + timedelta(hours=3)).isoformat(), 'state': 'in_review', 'issue_number': 42, 'metadata': {}},
            {'timestamp': (now + timedelta(hours=4)).isoformat(), 'state': 'approved', 'issue_number': 42, 'metadata': {}},
            {'timestamp': (now + timedelta(hours=4, minutes=5)).isoformat(), 'state': 'merged', 'issue_number': 42, 'metadata': {}},
            {'timestamp': (now + timedelta(hours=4, minutes=5)).isoformat(), 'state': 'closed', 'issue_number': 42, 'metadata': {}}
        ]
        
        with open(log_file, 'w') as f:
            for state in states:
                f.write(json.dumps(state) + '\n')
        
        metrics = manager.calculate_cycle_time(42)
        
        assert 'issue_to_pr_hours' in metrics
        assert abs(metrics['issue_to_pr_hours'] - 2.0) < 0.1
        
        assert 'pr_to_review_hours' in metrics
        assert abs(metrics['pr_to_review_hours'] - 1.0) < 0.1
        
        assert 'total_cycle_time_hours' in metrics
        assert abs(metrics['total_cycle_time_hours'] - 4.083) < 0.1
    
    def test_generate_workflow_report(self, manager):
        """Test workflow report generation."""
        from datetime import datetime, timedelta, timezone
        
        # Create logs for multiple issues
        now = datetime.now(timezone.utc)
        
        for issue_num in [1, 2]:
            log_file = manager.repo_path / 'santiago-pm' / 'workflow-logs' / f'issue-{issue_num}.log'
            states = [
                {'timestamp': now.isoformat(), 'state': 'created', 'issue_number': issue_num, 'metadata': {}},
                {'timestamp': (now + timedelta(hours=3)).isoformat(), 'state': 'pr_created', 'issue_number': issue_num, 'metadata': {}},
                {'timestamp': (now + timedelta(hours=5)).isoformat(), 'state': 'closed', 'issue_number': issue_num, 'metadata': {}}
            ]
            
            with open(log_file, 'w') as f:
                for state in states:
                    f.write(json.dumps(state) + '\n')
        
        report = manager.generate_workflow_report()
        
        assert report['total_issues'] == 2
        assert 'avg_cycle_time_hours' in report
        assert 'avg_issue_to_pr_hours' in report
        assert 'bottlenecks' in report


class TestPollingWorkflow:
    """Test PR polling functionality (Phase 5)."""
    
    @pytest.fixture
    def manager(self, tmp_path):
        """Create PR workflow manager with test repo."""
        return PRWorkflowManager(tmp_path)
    
    def test_poll_pr_becomes_ready(self, manager, monkeypatch):
        """Test polling until PR becomes ready."""
        import subprocess
        import time
        
        # Mock check_pr_status to return different states
        check_count = 0
        
        def mock_check_pr_status(pr_number):
            nonlocal check_count
            check_count += 1
            
            # First check: not ready (no approval)
            if check_count == 1:
                return {
                    'state': 'OPEN',
                    'approved': False,
                    'mergeable': True,
                    'checks_passing': True,
                    'reviews': []
                }
            # Second check: ready
            else:
                return {
                    'state': 'OPEN',
                    'approved': True,
                    'mergeable': True,
                    'checks_passing': True,
                    'reviews': []
                }
        
        monkeypatch.setattr(manager, 'check_pr_status', mock_check_pr_status)
        
        # Speed up test by reducing sleep time
        original_sleep = time.sleep
        def mock_sleep(seconds):
            original_sleep(0.1)  # Sleep for 0.1s instead
        monkeypatch.setattr(time, 'sleep', mock_sleep)
        
        result = manager.poll_pr(
            pr_number=14,
            interval_seconds=1,  # Fast interval for testing
            max_duration_minutes=1,
            auto_merge=False
        )
        
        assert result['ready'] is True
        assert result['pr_number'] == 14
        assert result['checks_count'] == 2
        assert result['timeout'] is False
        assert result['auto_merged'] is False
    
    def test_poll_pr_with_auto_merge(self, manager, monkeypatch):
        """Test polling with auto-merge enabled."""
        import time
        
        def mock_check_pr_status(pr_number):
            return {
                'state': 'OPEN',
                'approved': True,
                'mergeable': True,
                'checks_passing': True,
                'reviews': []
            }
        
        def mock_merge_pr(pr_number, merge_method='squash', delete_branch=True):
            return {
                'merged': True,
                'pr_number': pr_number,
                'merge_method': merge_method,
                'merged_at': '2025-11-17T20:00:00Z'
            }
        
        monkeypatch.setattr(manager, 'check_pr_status', mock_check_pr_status)
        monkeypatch.setattr(manager, 'merge_pr', mock_merge_pr)
        
        original_sleep = time.sleep
        def mock_sleep(seconds):
            original_sleep(0.01)
        monkeypatch.setattr(time, 'sleep', mock_sleep)
        
        result = manager.poll_pr(
            pr_number=14,
            interval_seconds=1,
            max_duration_minutes=1,
            auto_merge=True
        )
        
        assert result['ready'] is True
        assert result['auto_merged'] is True
    
    def test_poll_pr_timeout(self, manager, monkeypatch):
        """Test polling timeout."""
        import time
        
        def mock_check_pr_status(pr_number):
            return {
                'state': 'OPEN',
                'approved': False,
                'mergeable': True,
                'checks_passing': True,
                'reviews': []
            }
        
        monkeypatch.setattr(manager, 'check_pr_status', mock_check_pr_status)
        
        # Mock time to simulate fast timeout
        start_time = time.time()
        def mock_time():
            # Return start_time + 10 seconds on first call, then increment
            return start_time + 10
        
        original_sleep = time.sleep
        def mock_sleep(seconds):
            original_sleep(0.01)
        
        monkeypatch.setattr(time, 'sleep', mock_sleep)
        
        result = manager.poll_pr(
            pr_number=14,
            interval_seconds=1,
            max_duration_minutes=0.001,  # Very short timeout
            auto_merge=False
        )
        
        assert result['ready'] is False
        assert result['timeout'] is True


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
