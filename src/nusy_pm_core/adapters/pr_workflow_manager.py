"""
PR/Issue Workflow Manager - F-030 Phases 1-4
=============================================
Automates PR creation, review workflow, and issue updates.

Phase 1: PR Creation (✅ Complete)
- Agent creates PR with work summary and acceptance criteria
- Auto-links PR to issue using "Closes #N" keyword
- Adds PR reference comment to linked issue

Phase 2: Review Workflow Automation (🔄 In Progress)
- Auto-merge on approval
- Issue update with review summary
- Auto-close issue on merge

Phase 3: Changes Request Workflow
- Parse review comments into task list
- Update issue with structured change requests
- Track revision iterations

Phase 4: Metrics and Reporting
- Workflow state tracking
- Cycle time calculation
- Quality metrics

Integration Points:
- F-027 (Personal Logs): Includes session log link in PR body
- GitHub API: PR/issue operations
- Git: Branch and commit information
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
import subprocess
import re
import os
import json
import time


class PRWorkflowManager:
    """
    Manages PR creation and issue workflow automation.
    
    Phase 1: Basic PR creation with issue linking
    """
    
    def __init__(self, repo_path: Path):
        """
        Initialize PR workflow manager.
        
        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = Path(repo_path)
        self.github_token = os.getenv('GITHUB_TOKEN')
        if not self.github_token:
            print("Warning: GITHUB_TOKEN not set. PR creation will fail.")
    
    def create_pr(
        self,
        issue_number: int,
        title: Optional[str] = None,
        work_summary: Optional[str] = None,
        acceptance_criteria: Optional[List[str]] = None,
        session_log_path: Optional[str] = None,
        commits: Optional[List[str]] = None,
        tests_passing: bool = True,
        branch: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a PR for completed work with automatic issue linking.
        
        Args:
            issue_number: GitHub issue number this PR closes
            title: PR title (defaults to "Closes #N: <issue title>")
            work_summary: Summary of work completed
            acceptance_criteria: List of acceptance criteria met
            session_log_path: Path to F-027 session log (for context)
            commits: List of commit SHAs included in PR
            tests_passing: Whether all tests pass
            branch: Source branch (defaults to current branch)
            
        Returns:
            Dict with PR creation details:
                - pr_number: Created PR number
                - pr_url: URL to the PR
                - issue_number: Linked issue number
                - branch: Source branch name
                - created_at: Timestamp
        """
        # Get current branch if not specified
        if not branch:
            branch = self._get_current_branch()
        
        # Get issue details from GitHub
        issue_details = self._get_issue_details(issue_number)
        
        # Build PR title
        if not title:
            title = f"Closes #{issue_number}: {issue_details['title']}"
        
        # Build PR body
        pr_body = self._build_pr_body(
            issue_number=issue_number,
            work_summary=work_summary or "See commits for details.",
            acceptance_criteria=acceptance_criteria,
            session_log_path=session_log_path,
            commits=commits or self._get_branch_commits(branch),
            tests_passing=tests_passing
        )
        
        # Create PR via GitHub API
        pr_result = self._create_github_pr(
            title=title,
            body=pr_body,
            head=branch,
            base="main"
        )
        
        # Add comment to issue with PR link
        self._add_pr_comment_to_issue(issue_number, pr_result['number'], pr_result['url'])
        
        return {
            'pr_number': pr_result['number'],
            'pr_url': pr_result['url'],
            'issue_number': issue_number,
            'branch': branch,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
    
    def _get_current_branch(self) -> str:
        """Get the name of the current git branch."""
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    def _get_branch_commits(self, branch: str, base: str = "main") -> List[str]:
        """Get list of commits in branch not in base."""
        result = subprocess.run(
            ['git', 'log', f'{base}..{branch}', '--pretty=format:%H %s'],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                sha, *msg_parts = line.split(' ', 1)
                message = msg_parts[0] if msg_parts else ''
                commits.append(f"{sha[:7]}: {message}")
        return commits
    
    def _get_issue_details(self, issue_number: int) -> Dict[str, Any]:
        """
        Get issue details from GitHub API.
        
        For Phase 1, we'll use gh CLI. In Phase 2, we can use direct API calls.
        """
        try:
            result = subprocess.run(
                ['gh', 'issue', 'view', str(issue_number), '--json', 'title,body,labels'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            import json
            return json.loads(result.stdout)
        except subprocess.CalledProcessError:
            # Fallback if gh CLI not available
            return {
                'title': f'Issue #{issue_number}',
                'body': '',
                'labels': []
            }
    
    def _build_pr_body(
        self,
        issue_number: int,
        work_summary: str,
        acceptance_criteria: Optional[List[str]],
        session_log_path: Optional[str],
        commits: List[str],
        tests_passing: bool
    ) -> str:
        """Build comprehensive PR body with work summary and context."""
        body_parts = []
        
        # Issue link (triggers auto-linking)
        body_parts.append(f"Closes #{issue_number}")
        body_parts.append("")
        
        # Work summary
        body_parts.append("## Work Summary")
        body_parts.append("")
        body_parts.append(work_summary)
        body_parts.append("")
        
        # Session context (F-027 integration)
        if session_log_path:
            body_parts.append("## Session Context")
            body_parts.append("")
            body_parts.append(f"📋 **Session Log**: [`{Path(session_log_path).name}`]({session_log_path})")
            body_parts.append("")
            body_parts.append("*Full session context available in personal log for context restoration.*")
            body_parts.append("")
        
        # Acceptance criteria
        if acceptance_criteria:
            body_parts.append("## Acceptance Criteria")
            body_parts.append("")
            for criterion in acceptance_criteria:
                body_parts.append(f"- [x] {criterion}")
            body_parts.append("")
        
        # Commits
        if commits:
            body_parts.append("## Commits")
            body_parts.append("")
            for commit in commits:
                body_parts.append(f"- {commit}")
            body_parts.append("")
        
        # Test status
        body_parts.append("## Test Status")
        body_parts.append("")
        if tests_passing:
            body_parts.append("✅ All tests passing")
        else:
            body_parts.append("⚠️ Tests need attention")
        body_parts.append("")
        
        # Review checklist
        body_parts.append("## Review Checklist")
        body_parts.append("")
        body_parts.append("- [ ] Code quality meets project standards")
        body_parts.append("- [ ] All acceptance criteria are met")
        body_parts.append("- [ ] Tests are comprehensive and passing")
        body_parts.append("- [ ] Documentation is updated")
        body_parts.append("- [ ] No breaking changes without migration plan")
        body_parts.append("- [ ] Architecture follows project patterns")
        body_parts.append("- [ ] Security concerns addressed")
        body_parts.append("")
        
        # Labels
        body_parts.append("---")
        body_parts.append("")
        body_parts.append("*Created by Santiago-PM autonomous agent (F-030)*")
        
        return '\n'.join(body_parts)
    
    def _create_github_pr(
        self,
        title: str,
        body: str,
        head: str,
        base: str
    ) -> Dict[str, Any]:
        """
        Create PR using GitHub CLI.
        
        For Phase 1, we use gh CLI. In Phase 2, we can add direct API support.
        """
        try:
            # Use gh CLI to create PR
            result = subprocess.run(
                [
                    'gh', 'pr', 'create',
                    '--title', title,
                    '--body', body,
                    '--head', head,
                    '--base', base
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Extract PR URL from output
            pr_url = result.stdout.strip()
            
            # Extract PR number from URL
            pr_number_match = re.search(r'/pull/(\d+)', pr_url)
            pr_number = int(pr_number_match.group(1)) if pr_number_match else None
            
            return {
                'number': pr_number,
                'url': pr_url
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create PR: {e.stderr}")
    
    def _add_pr_comment_to_issue(self, issue_number: int, pr_number: int, pr_url: str):
        """Add a comment to the issue with PR link."""
        comment = f"""🔄 **Pull Request Created**

PR #{pr_number} has been created for this issue.

**Review**: {pr_url}

The PR includes:
- Work summary and acceptance criteria
- Session context for full provenance
- Review checklist for PM approval

---
*Automated by Santiago-PM (F-030)*"""
        
        try:
            subprocess.run(
                ['gh', 'issue', 'comment', str(issue_number), '--body', comment],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to add PR comment to issue: {e.stderr}")
    
    # Phase 2: Review Workflow Automation
    
    def check_pr_status(self, pr_number: int) -> Dict[str, Any]:
        """
        Check PR status including reviews and checks.
        
        Returns:
            Dict with PR status:
                - state: open/closed/merged
                - reviews: List of review states
                - approved: Whether PR is approved
                - mergeable: Whether PR can be merged
                - checks_passing: Whether all checks pass
        """
        try:
            result = subprocess.run(
                [
                    'gh', 'pr', 'view', str(pr_number),
                    '--json', 'state,reviews,reviewDecision,mergeable,statusCheckRollup'
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            
            # Check if all status checks pass
            checks_passing = True
            if data.get('statusCheckRollup'):
                for check in data['statusCheckRollup']:
                    if check.get('conclusion') not in ['SUCCESS', 'NEUTRAL', 'SKIPPED']:
                        checks_passing = False
                        break
            
            return {
                'state': data.get('state', 'UNKNOWN'),
                'reviews': data.get('reviews', []),
                'approved': data.get('reviewDecision') == 'APPROVED',
                'mergeable': data.get('mergeable') == 'MERGEABLE',
                'checks_passing': checks_passing,
                'review_decision': data.get('reviewDecision')
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to check PR status: {e.stderr}")
    
    def merge_pr(
        self,
        pr_number: int,
        merge_method: str = 'squash',
        delete_branch: bool = True
    ) -> Dict[str, Any]:
        """
        Merge an approved PR.
        
        Args:
            pr_number: PR number to merge
            merge_method: 'squash', 'merge', or 'rebase'
            delete_branch: Whether to delete branch after merge
            
        Returns:
            Dict with merge details
        """
        # Check PR is approved and mergeable
        status = self.check_pr_status(pr_number)
        
        if not status['approved']:
            raise RuntimeError(f"PR #{pr_number} is not approved. Cannot auto-merge.")
        
        if not status['checks_passing']:
            raise RuntimeError(f"PR #{pr_number} has failing checks. Cannot auto-merge.")
        
        if not status['mergeable']:
            raise RuntimeError(f"PR #{pr_number} is not mergeable. May have conflicts.")
        
        # Merge PR
        try:
            merge_args = ['gh', 'pr', 'merge', str(pr_number), f'--{merge_method}']
            if delete_branch:
                merge_args.append('--delete-branch')
            
            result = subprocess.run(
                merge_args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            return {
                'merged': True,
                'pr_number': pr_number,
                'merge_method': merge_method,
                'merged_at': datetime.now(timezone.utc).isoformat(),
                'branch_deleted': delete_branch
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to merge PR: {e.stderr}")
    
    def update_issue_on_merge(
        self,
        issue_number: int,
        pr_number: int,
        reviewer: str,
        review_summary: str,
        checklist_results: Optional[Dict[str, bool]] = None
    ):
        """
        Update issue with review summary and close on merge.
        
        Args:
            issue_number: Issue number to update
            pr_number: PR that was merged
            reviewer: Reviewer's username
            review_summary: Summary of the review
            checklist_results: Optional checklist item results
        """
        # Build review summary comment
        comment_parts = [
            "✅ **Work Approved and Merged**",
            "",
            f"**PR**: #{pr_number}",
            f"**Reviewer**: @{reviewer}",
            f"**Merged**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            "**Review Summary**:",
            review_summary,
            ""
        ]
        
        # Add checklist results if provided
        if checklist_results:
            comment_parts.append("**Checklist Results**:")
            for item, passed in checklist_results.items():
                icon = "✅" if passed else "❌"
                comment_parts.append(f"- {icon} {item}")
            comment_parts.append("")
        
        comment_parts.extend([
            "**Next Steps**:",
            "Issue closed automatically. Agent can proceed to next assigned work.",
            "",
            "---",
            "*Automated by Santiago-PM (F-030)*"
        ])
        
        comment = '\n'.join(comment_parts)
        
        # Add comment to issue
        try:
            subprocess.run(
                ['gh', 'issue', 'comment', str(issue_number), '--body', comment],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to add review comment: {e.stderr}")
        
        # Close issue with label
        try:
            subprocess.run(
                ['gh', 'issue', 'close', str(issue_number), '--reason', 'completed'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            # Add label
            subprocess.run(
                ['gh', 'issue', 'edit', str(issue_number), '--add-label', 'approved-merged'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to close issue: {e.stderr}")
    
    def handle_approved_pr(
        self,
        pr_number: int,
        reviewer: str,
        review_summary: str = "All acceptance criteria met. Code quality is high.",
        auto_merge: bool = True,
        merge_method: str = 'squash'
    ) -> Dict[str, Any]:
        """
        Handle complete approved PR workflow: merge + update issue + close.
        
        Args:
            pr_number: PR number that was approved
            reviewer: Reviewer's username
            review_summary: Summary from review
            auto_merge: Whether to auto-merge (default: True)
            merge_method: Merge method to use
            
        Returns:
            Dict with workflow results
        """
        # Get PR details to find linked issue
        pr_data = self._get_pr_details(pr_number)
        issue_number = pr_data.get('linked_issue')
        
        if not issue_number:
            raise RuntimeError(f"PR #{pr_number} has no linked issue. Cannot complete workflow.")
        
        result = {
            'pr_number': pr_number,
            'issue_number': issue_number,
            'approved': True,
            'merged': False,
            'issue_closed': False
        }
        
        # Merge PR if auto_merge enabled
        if auto_merge:
            try:
                merge_result = self.merge_pr(pr_number, merge_method)
                result['merged'] = True
                result['merge_details'] = merge_result
            except Exception as e:
                result['merge_error'] = str(e)
                print(f"❌ Failed to auto-merge: {e}")
                return result
        
        # Update issue with review summary and close
        try:
            self.update_issue_on_merge(
                issue_number=issue_number,
                pr_number=pr_number,
                reviewer=reviewer,
                review_summary=review_summary
            )
            result['issue_closed'] = True
        except Exception as e:
            result['issue_update_error'] = str(e)
            print(f"❌ Failed to update issue: {e}")
        
        return result
    
    def _get_pr_details(self, pr_number: int) -> Dict[str, Any]:
        """Get PR details including linked issue."""
        try:
            result = subprocess.run(
                ['gh', 'pr', 'view', str(pr_number), '--json', 'title,body,closingIssuesReferences'],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            data = json.loads(result.stdout)
            
            # Extract linked issue from closingIssuesReferences
            linked_issue = None
            if data.get('closingIssuesReferences'):
                refs = data['closingIssuesReferences']
                if refs and len(refs) > 0:
                    # Extract issue number from first reference
                    linked_issue = refs[0].get('number')
            
            # Fallback: parse "Closes #N" from body
            if not linked_issue and data.get('body'):
                match = re.search(r'Closes #(\d+)', data['body'])
                if match:
                    linked_issue = int(match.group(1))
            
            return {
                'title': data.get('title'),
                'body': data.get('body'),
                'linked_issue': linked_issue
            }
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to get PR details: {e.stderr}")
    
    # Phase 3: Changes Request Workflow
    
    def handle_changes_requested(
        self,
        pr_number: int,
        reviewer: str,
        review_comments: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Handle "changes requested" workflow.
        
        Args:
            pr_number: PR number with changes requested
            reviewer: Reviewer's username
            review_comments: List of review comments with structure:
                [
                    {
                        'file': 'path/to/file.py',
                        'line': 125,
                        'comment': 'Fix this issue',
                        'severity': 'blocker'|'important'|'minor'
                    },
                    ...
                ]
                
        Returns:
            Dict with workflow results
        """
        # Get PR details to find linked issue
        pr_data = self._get_pr_details(pr_number)
        issue_number = pr_data.get('linked_issue')
        
        if not issue_number:
            raise RuntimeError(f"PR #{pr_number} has no linked issue.")
        
        # Build structured comment
        comment_parts = [
            "⚠️ **Changes Requested on PR #{pr_number}**".replace('{pr_number}', str(pr_number)),
            "",
            f"**Reviewer**: @{reviewer}",
            f"**Reviewed**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            "",
            "**Issues Found**:"
        ]
        
        # Group by severity
        blockers = [c for c in review_comments if c.get('severity') == 'blocker']
        important = [c for c in review_comments if c.get('severity') == 'important']
        minor = [c for c in review_comments if c.get('severity') == 'minor']
        
        for severity_group, icon, items in [
            ('Blocker', '🔴', blockers),
            ('Important', '🟡', important),
            ('Minor', '🟢', minor)
        ]:
            if items:
                for item in items:
                    location = ""
                    if item.get('file'):
                        location = f" ({item['file']}"
                        if item.get('line'):
                            location += f":{item['line']}"
                        location += ")"
                    comment_parts.append(f"- {icon} **{severity_group}**: {item['comment']}{location}")
        
        comment_parts.extend([
            "",
            "**Next Steps**:",
            "Agent will address comments and update PR. Issue remains open pending resolution.",
            "",
            "---",
            "*Automated by Santiago-PM (F-030)*"
        ])
        
        comment = '\n'.join(comment_parts)
        
        # Add comment to issue
        try:
            subprocess.run(
                ['gh', 'issue', 'comment', str(issue_number), '--body', comment],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to add changes comment: {e.stderr}")
        
        # Update issue label
        try:
            subprocess.run(
                ['gh', 'issue', 'edit', str(issue_number), '--add-label', 'in-revision'],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to update issue label: {e.stderr}")
        
        return {
            'pr_number': pr_number,
            'issue_number': issue_number,
            'changes_requested': True,
            'comment_count': len(review_comments),
            'blocker_count': len(blockers)
        }
    
    # Phase 4: Metrics and Reporting
    
    def track_workflow_state(
        self,
        issue_number: int,
        state: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Track workflow state transition with timestamp.
        
        States: created, in_progress, pr_created, in_review, approved, 
                merged, closed, in_revision
                
        This writes to a workflow log for metrics analysis.
        """
        log_dir = self.repo_path / 'santiago-pm' / 'workflow-logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f'issue-{issue_number}.log'
        
        entry = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'issue_number': issue_number,
            'state': state,
            'metadata': metadata or {}
        }
        
        # Append to log file
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    
    def calculate_cycle_time(self, issue_number: int) -> Dict[str, Any]:
        """
        Calculate cycle time metrics for an issue.
        
        Returns:
            Dict with timing metrics:
                - issue_to_pr: Hours from issue created to PR created
                - pr_to_review: Hours from PR created to review started
                - review_to_approval: Hours from review to approval
                - approval_to_merge: Hours from approval to merge
                - total_cycle_time: Total hours from creation to close
        """
        log_file = self.repo_path / 'santiago-pm' / 'workflow-logs' / f'issue-{issue_number}.log'
        
        if not log_file.exists():
            return {'error': 'No workflow log found for issue'}
        
        # Read all state transitions
        states = []
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip():
                    states.append(json.loads(line))
        
        # Extract key timestamps
        timestamps = {}
        for state in states:
            state_name = state['state']
            if state_name not in timestamps:
                timestamps[state_name] = datetime.fromisoformat(state['timestamp'])
        
        # Calculate durations
        metrics = {}
        
        if 'created' in timestamps and 'pr_created' in timestamps:
            delta = timestamps['pr_created'] - timestamps['created']
            metrics['issue_to_pr_hours'] = delta.total_seconds() / 3600
        
        if 'pr_created' in timestamps and 'in_review' in timestamps:
            delta = timestamps['in_review'] - timestamps['pr_created']
            metrics['pr_to_review_hours'] = delta.total_seconds() / 3600
        
        if 'in_review' in timestamps and 'approved' in timestamps:
            delta = timestamps['approved'] - timestamps['in_review']
            metrics['review_to_approval_hours'] = delta.total_seconds() / 3600
        
        if 'approved' in timestamps and 'merged' in timestamps:
            delta = timestamps['merged'] - timestamps['approved']
            metrics['approval_to_merge_hours'] = delta.total_seconds() / 3600
        
        if 'created' in timestamps and 'closed' in timestamps:
            delta = timestamps['closed'] - timestamps['created']
            metrics['total_cycle_time_hours'] = delta.total_seconds() / 3600
        
        return metrics
    
    def generate_workflow_report(self, start_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate workflow performance report.
        
        Args:
            start_date: ISO format date to start report from (optional)
            
        Returns:
            Dict with aggregate metrics:
                - total_issues: Number of issues processed
                - avg_cycle_time: Average total cycle time
                - approval_rate: % of PRs approved first time
                - avg_review_iterations: Average review rounds
                - bottlenecks: Slowest workflow stages
        """
        log_dir = self.repo_path / 'santiago-pm' / 'workflow-logs'
        
        if not log_dir.exists():
            return {'error': 'No workflow logs found'}
        
        # Collect all issue logs
        issues = []
        for log_file in log_dir.glob('issue-*.log'):
            issue_num = int(log_file.stem.replace('issue-', ''))
            metrics = self.calculate_cycle_time(issue_num)
            if 'error' not in metrics:
                issues.append({
                    'issue_number': issue_num,
                    **metrics
                })
        
        if not issues:
            return {'error': 'No completed issues found'}
        
        # Calculate aggregate metrics
        report = {
            'total_issues': len(issues),
            'period_start': start_date or 'all_time'
        }
        
        # Average cycle times
        if any('total_cycle_time_hours' in i for i in issues):
            cycle_times = [i['total_cycle_time_hours'] for i in issues if 'total_cycle_time_hours' in i]
            report['avg_cycle_time_hours'] = sum(cycle_times) / len(cycle_times)
        
        # Stage durations
        for stage in ['issue_to_pr_hours', 'pr_to_review_hours', 'review_to_approval_hours']:
            values = [i[stage] for i in issues if stage in i]
            if values:
                report[f'avg_{stage}'] = sum(values) / len(values)
        
        # Identify bottlenecks
        bottlenecks = []
        for stage_key in ['issue_to_pr_hours', 'pr_to_review_hours', 'review_to_approval_hours']:
            if f'avg_{stage_key}' in report:
                bottlenecks.append({
                    'stage': stage_key.replace('_hours', ''),
                    'avg_hours': report[f'avg_{stage_key}']
                })
        
        bottlenecks.sort(key=lambda x: x['avg_hours'], reverse=True)
        report['bottlenecks'] = bottlenecks[:3]  # Top 3
        
        return report
    
    def poll_pr(
        self,
        pr_number: int,
        interval_seconds: int = 60,
        max_duration_minutes: int = 120,
        auto_merge: bool = False,
        on_ready_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Poll PR status until ready (approved + checks passing + mergeable).
        
        Phase 5: Polling and automation
        
        Args:
            pr_number: PR number to monitor
            interval_seconds: Seconds between status checks (default 60)
            max_duration_minutes: Maximum time to poll (default 120 minutes)
            auto_merge: Automatically merge when ready (default False)
            on_ready_callback: Optional callback when PR becomes ready
            
        Returns:
            dict with:
                - ready: bool (True if PR ready)
                - pr_number: int
                - status: dict (final status)
                - checks_count: int (number of checks performed)
                - elapsed_minutes: float (total time spent polling)
                - auto_merged: bool (True if auto-merged)
                - timeout: bool (True if max duration exceeded)
        """
        start_time = time.time()
        max_seconds = max_duration_minutes * 60
        checks_count = 0
        
        print(f"🔄 Starting PR #{pr_number} polling...")
        print(f"   Interval: {interval_seconds}s")
        print(f"   Max duration: {max_duration_minutes} minutes")
        print(f"   Auto-merge: {'enabled' if auto_merge else 'disabled'}")
        
        while True:
            elapsed = time.time() - start_time
            
            # Check timeout
            if elapsed > max_seconds:
                elapsed_minutes = elapsed / 60
                print(f"\n⏱️ Polling timeout after {elapsed_minutes:.1f} minutes")
                status = self.check_pr_status(pr_number)
                return {
                    'ready': False,
                    'pr_number': pr_number,
                    'status': status,
                    'checks_count': checks_count,
                    'elapsed_minutes': elapsed_minutes,
                    'auto_merged': False,
                    'timeout': True
                }
            
            # Check status
            checks_count += 1
            status = self.check_pr_status(pr_number)
            elapsed_minutes = elapsed / 60
            
            print(f"\n[Check #{checks_count} at {elapsed_minutes:.1f}m]")
            print(f"  State: {status['state']}")
            print(f"  Approved: {'✅' if status['approved'] else '❌'}")
            print(f"  Mergeable: {'✅' if status['mergeable'] else '❌'}")
            print(f"  Checks: {'✅' if status['checks_passing'] else '❌'}")
            
            # Check if ready
            ready = (
                status['state'] == 'OPEN' and
                status['approved'] and
                status['mergeable'] and
                status['checks_passing']
            )
            
            if ready:
                print(f"\n✅ PR #{pr_number} is READY!")
                
                # Call callback if provided
                if on_ready_callback:
                    try:
                        on_ready_callback(pr_number, status)
                    except Exception as e:
                        print(f"⚠️ Callback failed: {e}")
                
                # Auto-merge if enabled
                auto_merged = False
                if auto_merge:
                    print(f"🚀 Auto-merging PR #{pr_number}...")
                    try:
                        merge_result = self.merge_pr(pr_number)
                        auto_merged = merge_result['merged']
                        print(f"✅ Auto-merge successful!")
                    except Exception as e:
                        print(f"❌ Auto-merge failed: {e}")
                
                return {
                    'ready': True,
                    'pr_number': pr_number,
                    'status': status,
                    'checks_count': checks_count,
                    'elapsed_minutes': elapsed_minutes,
                    'auto_merged': auto_merged,
                    'timeout': False
                }
            
            # Check if PR was closed/merged by someone else
            if status['state'] in ['CLOSED', 'MERGED']:
                print(f"\n🛑 PR #{pr_number} is {status['state']}")
                return {
                    'ready': False,
                    'pr_number': pr_number,
                    'status': status,
                    'checks_count': checks_count,
                    'elapsed_minutes': elapsed_minutes,
                    'auto_merged': False,
                    'timeout': False
                }
            
            # Wait for next check
            print(f"  ⏳ Next check in {interval_seconds}s...")
            time.sleep(interval_seconds)


# CLI interface for agents
def main():
    """CLI entry point for agents to use PR workflow manager."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PR/Issue Workflow Manager (F-030 Phases 1-4)"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Phase 1: Create PR
    create_parser = subparsers.add_parser('create-pr', help='Create PR with automatic issue linking')
    create_parser.add_argument('issue_number', type=int, help='GitHub issue number')
    create_parser.add_argument('--title', help='PR title')
    create_parser.add_argument('--summary', help='Work summary')
    create_parser.add_argument('--session-log', help='Path to F-027 session log')
    create_parser.add_argument('--branch', help='Source branch')
    create_parser.add_argument('--no-tests', action='store_true', help='Tests not passing')
    
    # Phase 2: Check and merge PR
    status_parser = subparsers.add_parser('check-status', help='Check PR approval status')
    status_parser.add_argument('pr_number', type=int, help='PR number')
    
    merge_parser = subparsers.add_parser('merge-pr', help='Merge approved PR')
    merge_parser.add_argument('pr_number', type=int, help='PR number')
    merge_parser.add_argument('--method', default='squash', choices=['squash', 'merge', 'rebase'])
    merge_parser.add_argument('--no-delete-branch', action='store_true')
    
    approve_parser = subparsers.add_parser('handle-approval', help='Complete workflow on approval')
    approve_parser.add_argument('pr_number', type=int, help='PR number')
    approve_parser.add_argument('--reviewer', required=True, help='Reviewer username')
    approve_parser.add_argument('--summary', default='All acceptance criteria met.')
    approve_parser.add_argument('--no-auto-merge', action='store_true')
    
    # Phase 3: Handle changes requested
    changes_parser = subparsers.add_parser('handle-changes', help='Handle changes requested')
    changes_parser.add_argument('pr_number', type=int, help='PR number')
    changes_parser.add_argument('--reviewer', required=True, help='Reviewer username')
    changes_parser.add_argument('--comments-file', help='JSON file with review comments')
    
    # Phase 4: Metrics
    metrics_parser = subparsers.add_parser('cycle-time', help='Calculate cycle time for issue')
    metrics_parser.add_argument('issue_number', type=int, help='Issue number')
    
    report_parser = subparsers.add_parser('workflow-report', help='Generate workflow performance report')
    report_parser.add_argument('--since', help='Start date (ISO format)')
    
    # Phase 5: Polling
    poll_parser = subparsers.add_parser('poll-pr', help='Poll PR until ready for merge')
    poll_parser.add_argument('pr_number', type=int, help='PR number')
    poll_parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds (default: 60)')
    poll_parser.add_argument('--max-duration', type=int, default=120, help='Max polling duration in minutes (default: 120)')
    poll_parser.add_argument('--auto-merge', action='store_true', help='Automatically merge when ready')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = PRWorkflowManager(Path.cwd())
    
    try:
        if args.command == 'create-pr':
            result = manager.create_pr(
                issue_number=args.issue_number,
                title=args.title,
                work_summary=args.summary,
                session_log_path=args.session_log,
                branch=args.branch,
                tests_passing=not args.no_tests
            )
            print(f"✅ PR created successfully!")
            print(f"   PR #{result['pr_number']}: {result['pr_url']}")
            print(f"   Linked to issue #{result['issue_number']}")
            
        elif args.command == 'check-status':
            status = manager.check_pr_status(args.pr_number)
            print(f"PR #{args.pr_number} Status:")
            print(f"  State: {status['state']}")
            print(f"  Approved: {status['approved']}")
            print(f"  Mergeable: {status['mergeable']}")
            print(f"  Checks Passing: {status['checks_passing']}")
            
        elif args.command == 'merge-pr':
            result = manager.merge_pr(
                args.pr_number,
                merge_method=args.method,
                delete_branch=not args.no_delete_branch
            )
            print(f"✅ PR #{result['pr_number']} merged successfully!")
            print(f"   Method: {result['merge_method']}")
            print(f"   Merged at: {result['merged_at']}")
            
        elif args.command == 'handle-approval':
            result = manager.handle_approved_pr(
                args.pr_number,
                reviewer=args.reviewer,
                review_summary=args.summary,
                auto_merge=not args.no_auto_merge
            )
            print(f"✅ Approval workflow completed!")
            print(f"   PR #{result['pr_number']}")
            print(f"   Issue #{result['issue_number']}")
            print(f"   Merged: {result['merged']}")
            print(f"   Issue Closed: {result['issue_closed']}")
            
        elif args.command == 'handle-changes':
            # Load review comments from file
            import json
            if args.comments_file:
                with open(args.comments_file) as f:
                    comments = json.load(f)
            else:
                comments = []
            
            result = manager.handle_changes_requested(
                args.pr_number,
                reviewer=args.reviewer,
                review_comments=comments
            )
            print(f"⚠️ Changes requested workflow completed!")
            print(f"   PR #{result['pr_number']}")
            print(f"   Issue #{result['issue_number']}")
            print(f"   Comments: {result['comment_count']}")
            print(f"   Blockers: {result['blocker_count']}")
            
        elif args.command == 'cycle-time':
            metrics = manager.calculate_cycle_time(args.issue_number)
            if 'error' in metrics:
                print(f"❌ {metrics['error']}")
            else:
                print(f"Cycle Time Metrics for Issue #{args.issue_number}:")
                for key, value in metrics.items():
                    print(f"  {key}: {value:.2f} hours")
            
        elif args.command == 'workflow-report':
            report = manager.generate_workflow_report(args.since)
            if 'error' in report:
                print(f"❌ {report['error']}")
            else:
                print("Workflow Performance Report:")
                print(f"  Total Issues: {report['total_issues']}")
                if 'avg_cycle_time_hours' in report:
                    print(f"  Avg Cycle Time: {report['avg_cycle_time_hours']:.2f} hours")
                if 'bottlenecks' in report:
                    print("  Top Bottlenecks:")
                    for bottleneck in report['bottlenecks']:
                        print(f"    - {bottleneck['stage']}: {bottleneck['avg_hours']:.2f} hours")
        
        elif args.command == 'poll-pr':
            result = manager.poll_pr(
                pr_number=args.pr_number,
                interval_seconds=args.interval,
                max_duration_minutes=args.max_duration,
                auto_merge=args.auto_merge
            )
            
            if result['ready']:
                print(f"\n✅ PR #{result['pr_number']} is ready!")
                if result['auto_merged']:
                    print(f"🚀 Auto-merged successfully!")
            elif result['timeout']:
                print(f"\n⏱️ Polling timed out after {result['elapsed_minutes']:.1f} minutes")
            else:
                print(f"\n🛑 PR #{result['pr_number']} ended in state: {result['status']['state']}")
            
            print(f"\nPolling Summary:")
            print(f"  Checks performed: {result['checks_count']}")
            print(f"  Time elapsed: {result['elapsed_minutes']:.1f} minutes")
    
    except Exception as e:
        print(f"❌ Failed: {e}")
        exit(1)


if __name__ == '__main__':
    main()
