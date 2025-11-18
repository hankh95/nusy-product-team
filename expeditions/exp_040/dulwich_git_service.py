"""
Dulwich-Based In-Memory Git Service - EXP-040 Enhancement

Uses Dulwich library for real Git operations in memory, providing:
- Authentic Git functionality without GitHub API dependencies
- Branch management, commits, merges, and conflict resolution
- No authentication tokens required for testing
- Seamless integration with existing EXP-040 architecture

This replaces the custom shared memory Git with standard Git operations.
"""

import asyncio
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import threading

try:
    from dulwich.repo import Repo
    from dulwich import porcelain
    from dulwich.objects import Commit, Tree, Blob
    from dulwich.errors import NotGitRepository
    DULWICH_AVAILABLE = True
except ImportError:
    DULWICH_AVAILABLE = False
    print("Warning: Dulwich not available. Install with: pip install dulwich")


@dataclass
class GitOperation:
    """Represents a Git operation result."""
    success: bool
    result: Any = None
    error: Optional[str] = None
    commit_id: Optional[str] = None
    branch: Optional[str] = None


class DulwichInMemoryGitService:
    """
    In-memory Git service using Dulwich for authentic Git operations.

    Provides:
    - Real Git repository operations in memory
    - Branch management and merging
    - Conflict detection and resolution
    - No GitHub API dependencies
    - Thread-safe operations
    """

    def __init__(self, workspace_path: Optional[str] = None):
        if not DULWICH_AVAILABLE:
            raise ImportError("Dulwich library is required. Install with: pip install dulwich")

        self.workspace_path = Path(workspace_path or tempfile.mkdtemp(prefix="dulwich_git_"))
        self.workspace_path.mkdir(parents=True, exist_ok=True)

        # Create in-memory repository
        self.repo_path = self.workspace_path / "repo"
        self.repo_path.mkdir(exist_ok=True)

        # Initialize repository
        self.repo = porcelain.init(str(self.repo_path))

        # Thread safety
        self.lock = threading.RLock()

        # Performance tracking
        self.operation_count = 0
        self.commit_count = 0

        print(f"✅ Initialized Dulwich in-memory Git at: {self.repo_path}")

    def _ensure_repo(self):
        """Ensure repository exists and is valid."""
        if not self.repo_path.exists():
            self.repo = porcelain.init(str(self.repo_path))
        try:
            # Test repository validity
            porcelain.status(self.repo)
        except NotGitRepository:
            # Reinitialize if corrupted
            shutil.rmtree(self.repo_path, ignore_errors=True)
            self.repo_path.mkdir(parents=True, exist_ok=True)
            self.repo = porcelain.init(str(self.repo_path))

    async def commit_changes(self, message: str, author: str = "Santiago Agent",
                           files: Optional[Dict[str, str]] = None) -> GitOperation:
        """
        Commit changes to the repository.

        Args:
            message: Commit message
            author: Author name
            files: Dict of filename -> content to add/modify

        Returns:
            GitOperation with result
        """
        with self.lock:
            try:
                self._ensure_repo()

                if files:
                    # Write files to working directory
                    for filename, content in files.items():
                        file_path = self.repo_path / filename
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)

                        # Add to index
                        porcelain.add(self.repo, [str(filename)])

                # Create commit
                author_bytes = f"{author} <{author.lower().replace(' ', '.')}@santiago.local>".encode()
                commit_id = porcelain.commit(
                    self.repo,
                    message.encode('utf-8'),
                    author=author_bytes
                )

                self.commit_count += 1
                self.operation_count += 1

                return GitOperation(
                    success=True,
                    commit_id=commit_id.decode('ascii') if isinstance(commit_id, bytes) else str(commit_id),
                    result=f"Committed {len(files) if files else 0} files"
                )

            except Exception as e:
                return GitOperation(
                    success=False,
                    error=f"Commit failed: {str(e)}"
                )

    async def create_branch(self, branch_name: str, base_branch: str = "main") -> GitOperation:
        """Create a new branch from base branch."""
        with self.lock:
            try:
                self._ensure_repo()

                # Create and checkout new branch
                porcelain.branch_create(self.repo, branch_name.encode('utf-8'))
                porcelain.checkout(self.repo, branch_name.encode('utf-8'))

                self.operation_count += 1

                return GitOperation(
                    success=True,
                    branch=branch_name,
                    result=f"Created and checked out branch: {branch_name}"
                )

            except Exception as e:
                return GitOperation(
                    success=False,
                    error=f"Branch creation failed: {str(e)}"
                )

    async def switch_branch(self, branch_name: str) -> GitOperation:
        """Switch to a different branch."""
        with self.lock:
            try:
                self._ensure_repo()

                porcelain.checkout(self.repo, branch_name.encode('utf-8'))

                self.operation_count += 1

                return GitOperation(
                    success=True,
                    branch=branch_name,
                    result=f"Switched to branch: {branch_name}"
                )

            except Exception as e:
                return GitOperation(
                    success=False,
                    error=f"Branch switch failed: {str(e)}"
                )

    async def merge_branch(self, source_branch: str, target_branch: str = "main") -> GitOperation:
        """Merge source branch into target branch."""
        with self.lock:
            try:
                self._ensure_repo()

                # Switch to target branch
                porcelain.checkout(self.repo, target_branch.encode('utf-8'))

                # Merge source branch
                try:
                    result = porcelain.merge(
                        self.repo,
                        source_branch.encode('utf-8'),
                        no_commit=False
                    )

                    self.operation_count += 1

                    return GitOperation(
                        success=True,
                        result=f"Successfully merged {source_branch} into {target_branch}"
                    )

                except Exception as merge_error:
                    # Handle merge conflicts
                    return GitOperation(
                        success=False,
                        error=f"Merge conflict: {str(merge_error)}"
                    )

            except Exception as e:
                return GitOperation(
                    success=False,
                    error=f"Merge failed: {str(e)}"
                )

    def get_status(self) -> Dict[str, Any]:
        """Get repository status."""
        with self.lock:
            try:
                self._ensure_repo()

                status = porcelain.status(self.repo)

                return {
                    "staged": list(status.staged),
                    "unstaged": list(status.unstaged),
                    "untracked": list(status.untracked),
                    "total_commits": self.commit_count,
                    "total_operations": self.operation_count
                }

            except Exception as e:
                return {
                    "error": str(e),
                    "total_commits": self.commit_count,
                    "total_operations": self.operation_count
                }

    def get_branches(self) -> List[str]:
        """Get list of branches."""
        with self.lock:
            try:
                self._ensure_repo()

                branches = []
                for branch_name in porcelain.branch_list(self.repo):
                    branches.append(branch_name.decode('utf-8') if isinstance(branch_name, bytes) else str(branch_name))

                return branches

            except Exception:
                return []

    def get_commit_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commit history."""
        with self.lock:
            try:
                self._ensure_repo()

                commits = []
                walker = self.repo.get_walker()

                for i, entry in enumerate(walker):
                    if i >= limit:
                        break

                    commit = entry.commit
                    commits.append({
                        "id": commit.id.decode('ascii') if isinstance(commit.id, bytes) else str(commit.id),
                        "message": commit.message.decode('utf-8') if isinstance(commit.message, bytes) else str(commit.message),
                        "author": commit.author.decode('utf-8') if isinstance(commit.author, bytes) else str(commit.author),
                        "timestamp": datetime.fromtimestamp(commit.commit_time),
                        "parents": [p.decode('ascii') if isinstance(p, bytes) else str(p) for p in commit.parents]
                    })

                return commits

            except Exception:
                return []

    async def detect_conflicts(self, operations: List[Dict[str, Any]]) -> List[str]:
        """
        Detect potential conflicts for a set of operations.

        Args:
            operations: List of file operations

        Returns:
            List of conflicting file paths
        """
        with self.lock:
            try:
                self._ensure_repo()

                # Get current status
                status = porcelain.status(self.repo)

                # Check for conflicts with staged/unstaged files
                operation_files = {op.get("file_path") for op in operations if "file_path" in op}
                staged_files = set(status.staged)
                unstaged_files = set(status.unstaged)

                conflicts = list(operation_files & (staged_files | unstaged_files))

                return conflicts

            except Exception:
                return []

    def cleanup(self):
        """Clean up the in-memory repository."""
        with self.lock:
            try:
                if self.workspace_path.exists():
                    shutil.rmtree(self.workspace_path, ignore_errors=True)
            except Exception:
                pass

    def __del__(self):
        """Cleanup on destruction."""
        self.cleanup()


# Test the Dulwich service
async def test_dulwich_git_service():
    """Test the Dulwich-based Git service."""
    print("Testing Dulwich In-Memory Git Service...")

    service = DulwichInMemoryGitService()

    # Test basic operations
    print("\n1. Testing commit operation...")
    result = await service.commit_changes(
        "Initial commit",
        files={"README.md": "# Test Repository\n\nThis is a test."}
    )
    print(f"   Result: {'✅' if result.success else '❌'} {result.result}")
    if result.commit_id:
        print(f"   Commit ID: {result.commit_id[:8]}...")

    print("\n2. Testing branch creation...")
    branch_result = await service.create_branch("feature/test")
    print(f"   Result: {'✅' if branch_result.success else '❌'} {branch_result.result}")

    print("\n3. Testing additional commit on branch...")
    result2 = await service.commit_changes(
        "Add feature",
        files={"feature.py": "def test():\n    return 'Hello from feature!'"}
    )
    print(f"   Result: {'✅' if result2.success else '❌'} {result2.result}")

    print("\n4. Testing branch switch...")
    switch_result = await service.switch_branch("main")
    print(f"   Result: {'✅' if switch_result.success else '❌'} {switch_result.result}")

    print("\n5. Testing status...")
    status = service.get_status()
    print(f"   Status: {status}")

    print("\n6. Testing commit history...")
    history = service.get_commit_history(5)
    print(f"   Found {len(history)} commits")
    for commit in history[:2]:  # Show first 2
        print(f"   - {commit['id'][:8]}: {commit['message'][:30]}...")

    print("\n7. Testing branches...")
    branches = service.get_branches()
    print(f"   Branches: {branches}")

    # Cleanup
    service.cleanup()

    print("\n🎉 Dulwich Git service test completed!")


if __name__ == "__main__":
    if DULWICH_AVAILABLE:
        asyncio.run(test_dulwich_git_service())
    else:
        print("❌ Dulwich not available. Install with: pip install dulwich")