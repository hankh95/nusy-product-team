"""
EXP-032: Santiago Team on DGX with In-Memory Git
===============================================

In-Memory Git Service for Santiago autonomous development.

This service provides:
- In-memory Git repositories for fast team collaboration
- Dulwich-based implementation for pure Python Git operations
- Team bubble management for multi-role Santiago coordination
"""

import os
import tempfile
from pathlib import Path
from dulwich import porcelain
from dulwich.repo import Repo
from typing import Dict, List, Optional, Any
import json
import time


class InMemoryGitService:
    """
    Service for managing in-memory Git repositories for Santiago teams.
    
    Provides fast, ephemeral Git operations for autonomous development.
    """
    
    def __init__(self, base_path: Path = None):
        """
        Initialize the in-memory Git service.
        
        Args:
            base_path: Base directory for temporary repos (defaults to system temp)
        """
        self.base_path = base_path or Path(tempfile.gettempdir()) / "santiago_memory_git"
        self.base_path.mkdir(exist_ok=True)
        self.active_repos: Dict[str, Repo] = {}
        
    def create_team_bubble(self, team_id: str) -> Path:
        """
        Create a new in-memory team bubble (Git repository).
        
        Args:
            team_id: Unique identifier for the team
            
        Returns:
            Path to the team repository
        """
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        team_path = self.base_path / f"team_{team_id}_{unique_id}"
        team_path.mkdir(exist_ok=True)
        
        # Initialize bare repository
        try:
            repo = porcelain.init(team_path, bare=True)
            self.active_repos[team_id] = repo
        except FileExistsError:
            # If directory already exists, clean it and retry
            import shutil
            shutil.rmtree(team_path)
            team_path.mkdir(exist_ok=True)
            repo = porcelain.init(team_path, bare=True)
            self.active_repos[team_id] = repo
        
        return team_path
    
    def clone_role_workspace(self, team_id: str, role: str) -> Path:
        """
        Clone a role-specific workspace from the team repository.
        
        Args:
            team_id: Team identifier
            role: Role name (pm, architect, developer, ethicist)
            
        Returns:
            Path to the role workspace
        """
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        workspace_path = self.base_path / f"workspace_{team_id}_{role}_{unique_id}"
        workspace_path.mkdir(exist_ok=True)
        
        # Find the team repo (it might have a unique suffix)
        team_repo_path = None
        for path in self.base_path.glob(f"team_{team_id}_*"):
            if path.is_dir():
                team_repo_path = path
                break
        
        if team_repo_path is None:
            raise ValueError(f"No team repository found for {team_id}")
        
        # Clone from team repo
        try:
            porcelain.clone(str(team_repo_path), str(workspace_path))
        except FileExistsError:
            # Clean and retry if needed
            import shutil
            shutil.rmtree(workspace_path)
            workspace_path.mkdir(exist_ok=True)
            porcelain.clone(str(team_repo_path), str(workspace_path))
        
        return workspace_path
    
    def commit_and_push_role_changes(
        self, 
        team_id: str, 
        role: str, 
        message: str,
        files: Optional[List[str]] = None
    ) -> str:
        """
        Commit changes in a role workspace and push to team repo.
        
        Args:
            team_id: Team identifier
            role: Role name
            message: Commit message
            files: Specific files to commit (None = all)
            
        Returns:
            Commit hash
        """
        workspace_path = self.base_path / f"workspace_{team_id}_{role}"
        
        # Add files
        if files:
            for file in files:
                porcelain.add(str(workspace_path), [file])
        else:
            porcelain.add(str(workspace_path))
        
        # Commit
        commit_hash = porcelain.commit(
            str(workspace_path), 
            message=message,
            author="Santiago Agent <agent@santiago.pm>",
            committer="Santiago Agent <agent@santiago.pm>"
        )
        
        # Push to team repo
        team_path = self.base_path / f"team_{team_id}"
        porcelain.push(str(workspace_path), str(team_path), "HEAD")
        
        return commit_hash.decode('utf-8')
    
    def get_diff(self, team_id: str, role: str, ref1: str = "HEAD~1", ref2: str = "HEAD") -> str:
        """
        Get diff between two refs in a role workspace.
        
        Args:
            team_id: Team identifier
            role: Role name
            ref1: First reference
            ref2: Second reference
            
        Returns:
            Diff as string
        """
        workspace_path = self.base_path / f"workspace_{team_id}_{role}"
        
        diff = porcelain.diff_tree(
            str(workspace_path),
            ref1.encode(),
            ref2.encode()
        )
        
        return diff.decode('utf-8')
    
    def export_patch(self, team_id: str, output_path: Path) -> None:
        """
        Export team repository as a patch file for promotion to disk.
        
        Args:
            team_id: Team identifier
            output_path: Where to save the patch
        """
        team_path = self.base_path / f"team_{team_id}"
        
        # Create patch from all commits
        patch_content = porcelain.format_patch(
            str(team_path),
            "HEAD",
            output=output_path
        )
    
    def cleanup_team_bubble(self, team_id: str) -> None:
        """
        Clean up a team bubble and all its workspaces.
        
        Args:
            team_id: Team identifier
        """
        # Remove team repo
        team_path = self.base_path / f"team_{team_id}"
        if team_path.exists():
            import shutil
            shutil.rmtree(team_path)
        
        # Remove all role workspaces
        for role in ['pm', 'architect', 'developer', 'ethicist']:
            workspace_path = self.base_path / f"workspace_{team_id}_{role}"
            if workspace_path.exists():
                shutil.rmtree(workspace_path)
        
        # Remove from active repos
        if team_id in self.active_repos:
            del self.active_repos[team_id]
    
    def get_team_status(self, team_id: str) -> Dict[str, Any]:
        """
        Get status of a team bubble.
        
        Args:
            team_id: Team identifier
            
        Returns:
            Status dictionary
        """
        team_path = self.base_path / f"team_{team_id}"
        
        if not team_path.exists():
            return {"status": "not_found"}
        
        # Get commit count
        try:
            commits = list(porcelain.log(str(team_path)))
            commit_count = len(commits)
        except:
            commit_count = 0
        
        # Get workspace info
        workspaces = {}
        for role in ['pm', 'architect', 'developer', 'ethicist']:
            workspace_path = self.base_path / f"workspace_{team_id}_{role}"
            workspaces[role] = workspace_path.exists()
        
        return {
            "status": "active",
            "commits": commit_count,
            "workspaces": workspaces,
            "created": time.time()  # Approximate
        }


# CLI interface for the in-memory Git service
def main():
    """CLI entry point for in-memory Git service."""
    import argparse
    
    parser = argparse.ArgumentParser(description="EXP-032: In-Memory Git Service")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create team bubble
    create_parser = subparsers.add_parser('create-team', help='Create team bubble')
    create_parser.add_argument('team_id', help='Team identifier')
    
    # Clone role workspace
    clone_parser = subparsers.add_parser('clone-workspace', help='Clone role workspace')
    clone_parser.add_argument('team_id', help='Team identifier')
    clone_parser.add_argument('role', help='Role name')
    
    # Commit and push
    commit_parser = subparsers.add_parser('commit-push', help='Commit and push changes')
    commit_parser.add_argument('team_id', help='Team identifier')
    commit_parser.add_argument('role', help='Role name')
    commit_parser.add_argument('message', help='Commit message')
    commit_parser.add_argument('--files', nargs='*', help='Specific files to commit')
    
    # Get diff
    diff_parser = subparsers.add_parser('diff', help='Get diff between refs')
    diff_parser.add_argument('team_id', help='Team identifier')
    diff_parser.add_argument('role', help='Role name')
    diff_parser.add_argument('--ref1', default='HEAD~1', help='First ref')
    diff_parser.add_argument('--ref2', default='HEAD', help='Second ref')
    
    # Export patch
    export_parser = subparsers.add_parser('export-patch', help='Export as patch')
    export_parser.add_argument('team_id', help='Team identifier')
    export_parser.add_argument('output_path', help='Output patch file')
    
    # Get status
    status_parser = subparsers.add_parser('status', help='Get team status')
    status_parser.add_argument('team_id', help='Team identifier')
    
    # Cleanup
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up team bubble')
    cleanup_parser.add_argument('team_id', help='Team identifier')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    service = InMemoryGitService()
    
    try:
        if args.command == 'create-team':
            path = service.create_team_bubble(args.team_id)
            print(f"✅ Created team bubble: {path}")
            
        elif args.command == 'clone-workspace':
            path = service.clone_role_workspace(args.team_id, args.role)
            print(f"✅ Created workspace: {path}")
            
        elif args.command == 'commit-push':
            commit_hash = service.commit_and_push_role_changes(
                args.team_id, args.role, args.message, args.files
            )
            print(f"✅ Committed and pushed: {commit_hash}")
            
        elif args.command == 'diff':
            diff = service.get_diff(args.team_id, args.role, args.ref1, args.ref2)
            print(diff)
            
        elif args.command == 'export-patch':
            service.export_patch(args.team_id, Path(args.output_path))
            print(f"✅ Exported patch to: {args.output_path}")
            
        elif args.command == 'status':
            status = service.get_team_status(args.team_id)
            print(f"Team {args.team_id} Status:")
            print(json.dumps(status, indent=2))
            
        elif args.command == 'cleanup':
            service.cleanup_team_bubble(args.team_id)
            print(f"✅ Cleaned up team bubble: {args.team_id}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()