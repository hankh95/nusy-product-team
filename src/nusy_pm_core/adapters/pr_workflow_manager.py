"""
PR/Issue Workflow Manager - F-030 Phase 1 MVP
==============================================
Automates PR creation, review workflow, and issue updates.

Phase 1 Scope:
- Agent creates PR with work summary and acceptance criteria
- Auto-links PR to issue using "Closes #N" keyword
- Adds PR reference comment to linked issue

Integration Points:
- F-027 (Personal Logs): Includes session log link in PR body
- GitHub API: PR/issue operations
- Git: Branch and commit information

Success Criteria:
- Agent can create PR with single command
- PR correctly links to issue
- Issue shows PR link in comments
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
import subprocess
import re
import os


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


# CLI interface for agents
def main():
    """CLI entry point for agents to create PRs."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create PR with automatic issue linking (F-030 Phase 1)"
    )
    parser.add_argument(
        'issue_number',
        type=int,
        help='GitHub issue number this PR closes'
    )
    parser.add_argument(
        '--title',
        help='PR title (defaults to "Closes #N: <issue title>")'
    )
    parser.add_argument(
        '--summary',
        help='Work summary (defaults to commit messages)'
    )
    parser.add_argument(
        '--session-log',
        help='Path to F-027 session log for context'
    )
    parser.add_argument(
        '--branch',
        help='Source branch (defaults to current branch)'
    )
    parser.add_argument(
        '--no-tests',
        action='store_true',
        help='Flag if tests are not passing'
    )
    
    args = parser.parse_args()
    
    # Initialize manager
    manager = PRWorkflowManager(Path.cwd())
    
    # Create PR
    try:
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
        print(f"   Branch: {result['branch']}")
        
    except Exception as e:
        print(f"❌ Failed to create PR: {e}")
        exit(1)


if __name__ == '__main__':
    main()
