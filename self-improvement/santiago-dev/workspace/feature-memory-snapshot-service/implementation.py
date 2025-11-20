#!/usr/bin/env python3
"""
Memory Snapshot Service - Git-Based System State Persistence

This service provides DevOps-style system state restoration capabilities
through git-based snapshots of agent memories, configurations, and system states.
"""

import os
import json
import hashlib
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict, field
import yaml

try:
    from dulwich import porcelain, repo
    from dulwich.errors import NotGitRepository
    DULWICH_AVAILABLE = True
except ImportError:
    DULWICH_AVAILABLE = False
    print("Warning: dulwich not available, git operations will be limited")

from pydantic import BaseModel, Field


@dataclass
class SnapshotMetadata:
    """Metadata for a system state snapshot"""
    snapshot_id: str
    timestamp: datetime
    agent_id: str
    snapshot_type: str  # "full", "incremental", "memory", "config"
    description: str
    tags: List[str] = field(default_factory=list)
    parent_snapshot: Optional[str] = None
    size_bytes: int = 0
    checksum: str = ""
    compression_ratio: float = 1.0


@dataclass
class SystemState:
    """Complete system state representation"""
    agent_memories: Dict[str, Any] = field(default_factory=dict)
    configurations: Dict[str, Any] = field(default_factory=dict)
    workflow_states: Dict[str, Any] = field(default_factory=dict)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


class MemorySnapshotService:
    """
    Git-based memory snapshot service for system state persistence and restoration.

    Provides DevOps-style capabilities for:
    - System state snapshots and restoration
    - Time-series analysis of state changes
    - Multi-agent memory synchronization
    - Collaborative development state sharing
    """

    def __init__(self, repo_path: str = ".memory_snapshots", auto_init: bool = True):
        """
        Initialize the memory snapshot service.

        Args:
            repo_path: Path to the git repository for snapshots
            auto_init: Automatically initialize repository if it doesn't exist
        """
        self.repo_path = Path(repo_path)
        self.snapshots: Dict[str, SnapshotMetadata] = {}
        self._ensure_repo(auto_init)

    def _ensure_repo(self, auto_init: bool):
        """Ensure the git repository exists and is initialized"""
        if not self.repo_path.exists() and auto_init:
            self.repo_path.mkdir(parents=True, exist_ok=True)
            if DULWICH_AVAILABLE:
                try:
                    porcelain.init(str(self.repo_path))
                    # Create initial commit
                    readme_path = self.repo_path / "README.md"
                    readme_path.write_text("# Memory Snapshot Repository\n\nGit-based system state snapshots for DevOps restoration.\n")
                    porcelain.add(str(self.repo_path), ["README.md"])
                    porcelain.commit(
                        str(self.repo_path),
                        message="Initial memory snapshot repository",
                        author="Memory Snapshot Service <memory@santiago.local>"
                    )
                except Exception as e:
                    print(f"Warning: Could not initialize git repo: {e}")
            else:
                print("Warning: dulwich not available, git operations disabled")

        self._load_snapshot_metadata()

    def _load_snapshot_metadata(self):
        """Load existing snapshot metadata from repository"""
        metadata_file = self.repo_path / ".snapshot_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    for snapshot_data in data.values():
                        # Convert timestamp string back to datetime
                        snapshot_data['timestamp'] = datetime.fromisoformat(snapshot_data['timestamp'])
                        snapshot = SnapshotMetadata(**snapshot_data)
                        self.snapshots[snapshot.snapshot_id] = snapshot
            except Exception as e:
                print(f"Warning: Could not load snapshot metadata: {e}")

    def _save_snapshot_metadata(self):
        """Save snapshot metadata to repository"""
        metadata_file = self.repo_path / ".snapshot_metadata.json"
        try:
            # Convert datetime objects to ISO strings for JSON serialization
            data = {}
            for snapshot_id, snapshot in self.snapshots.items():
                snapshot_dict = asdict(snapshot)
                snapshot_dict['timestamp'] = snapshot.timestamp.isoformat()
                data[snapshot_id] = snapshot_dict

            with open(metadata_file, 'w') as f:
                json.dump(data, f, indent=2)

            if DULWICH_AVAILABLE:
                porcelain.add(str(self.repo_path), [".snapshot_metadata.json"])
                porcelain.commit(
                    str(self.repo_path),
                    message=f"Update snapshot metadata - {len(self.snapshots)} snapshots",
                    author="Memory Snapshot Service <memory@santiago.local>"
                )
        except Exception as e:
            print(f"Warning: Could not save snapshot metadata: {e}")

    def create_snapshot(self,
                       system_state: SystemState,
                       snapshot_type: str = "full",
                       description: str = "",
                       tags: List[str] = None,
                       agent_id: str = "system") -> str:
        """
        Create a new system state snapshot.

        Args:
            system_state: Complete system state to snapshot
            snapshot_type: Type of snapshot ("full", "incremental", "memory", "config")
            description: Human-readable description of the snapshot
            tags: List of tags for categorization
            agent_id: ID of the agent creating the snapshot

        Returns:
            Snapshot ID for the created snapshot
        """
        timestamp = datetime.now()
        snapshot_id = f"{snapshot_type}_{agent_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}"

        # Create snapshot metadata
        metadata = SnapshotMetadata(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            agent_id=agent_id,
            snapshot_type=snapshot_type,
            description=description or f"{snapshot_type} snapshot created by {agent_id}",
            tags=tags or []
        )

        # Serialize system state
        state_data = asdict(system_state)
        state_data['timestamp'] = system_state.timestamp.isoformat()

        # Create snapshot file
        snapshot_file = self.repo_path / f"{snapshot_id}.json"
        with open(snapshot_file, 'w') as f:
            json.dump(state_data, f, indent=2, default=str)

        # Calculate checksum and size
        content = snapshot_file.read_text()
        metadata.checksum = hashlib.sha256(content.encode()).hexdigest()
        metadata.size_bytes = len(content.encode())

        # Store metadata
        self.snapshots[snapshot_id] = metadata
        self._save_snapshot_metadata()

        # Commit to git if available
        if DULWICH_AVAILABLE:
            try:
                porcelain.add(str(self.repo_path), [f"{snapshot_id}.json"])
                porcelain.commit(
                    str(self.repo_path),
                    message=f"Snapshot {snapshot_id}: {description}",
                    author=f"{agent_id} <{agent_id}@santiago.local>"
                )
            except Exception as e:
                print(f"Warning: Could not commit snapshot to git: {e}")

        return snapshot_id

    def restore_snapshot(self, snapshot_id: str) -> Optional[SystemState]:
        """
        Restore system state from a snapshot.

        Args:
            snapshot_id: ID of the snapshot to restore

        Returns:
            Restored SystemState object, or None if snapshot not found
        """
        if snapshot_id not in self.snapshots:
            print(f"Error: Snapshot {snapshot_id} not found")
            return None

        snapshot_file = self.repo_path / f"{snapshot_id}.json"
        if not snapshot_file.exists():
            print(f"Error: Snapshot file {snapshot_file} not found")
            return None

        try:
            with open(snapshot_file, 'r') as f:
                state_data = json.load(f)

            # Convert timestamp back to datetime
            if 'timestamp' in state_data:
                state_data['timestamp'] = datetime.fromisoformat(state_data['timestamp'])

            return SystemState(**state_data)
        except Exception as e:
            print(f"Error: Could not restore snapshot {snapshot_id}: {e}")
            return None

    def list_snapshots(self,
                      agent_id: Optional[str] = None,
                      snapshot_type: Optional[str] = None,
                      tags: List[str] = None,
                      limit: Optional[int] = None) -> List[SnapshotMetadata]:
        """
        List snapshots with optional filtering.

        Args:
            agent_id: Filter by agent ID
            snapshot_type: Filter by snapshot type
            tags: Filter by tags (snapshot must have all specified tags)
            limit: Maximum number of results to return

        Returns:
            List of matching SnapshotMetadata objects
        """
        snapshots = list(self.snapshots.values())

        # Apply filters
        if agent_id:
            snapshots = [s for s in snapshots if s.agent_id == agent_id]
        if snapshot_type:
            snapshots = [s for s in snapshots if s.snapshot_type == snapshot_type]
        if tags:
            snapshots = [s for s in snapshots if all(tag in s.tags for tag in tags)]

        # Sort by timestamp (newest first)
        snapshots.sort(key=lambda s: s.timestamp, reverse=True)

        if limit:
            snapshots = snapshots[:limit]

        return snapshots

    def get_snapshot_history(self,
                           agent_id: str,
                           hours: int = 24) -> List[SnapshotMetadata]:
        """
        Get snapshot history for an agent within a time window.

        Args:
            agent_id: Agent ID to get history for
            hours: Number of hours of history to retrieve

        Returns:
            List of snapshots for the agent within the time window
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [s for s in self.snapshots.values()
                if s.agent_id == agent_id and s.timestamp >= cutoff_time]

    def compare_snapshots(self, snapshot_id1: str, snapshot_id2: str) -> Dict[str, Any]:
        """
        Compare two snapshots to identify differences.

        Args:
            snapshot_id1: First snapshot ID
            snapshot_id2: Second snapshot ID

        Returns:
            Dictionary containing comparison results
        """
        state1 = self.restore_snapshot(snapshot_id1)
        state2 = self.restore_snapshot(snapshot_id2)

        if not state1 or not state2:
            return {"error": "Could not restore one or both snapshots"}

        comparison = {
            "snapshot1": snapshot_id1,
            "snapshot2": snapshot_id2,
            "timestamp1": state1.timestamp.isoformat(),
            "timestamp2": state2.timestamp.isoformat(),
            "differences": {}
        }

        # Compare each state component
        for key in ['agent_memories', 'configurations', 'workflow_states', 'performance_metrics']:
            val1 = getattr(state1, key, {})
            val2 = getattr(state2, key, {})

            if val1 != val2:
                comparison["differences"][key] = {
                    "changed": True,
                    "keys_only_in_1": set(val1.keys()) - set(val2.keys()),
                    "keys_only_in_2": set(val2.keys()) - set(val1.keys()),
                    "modified_keys": [k for k in val1.keys() & val2.keys() if val1[k] != val2[k]]
                }
            else:
                comparison["differences"][key] = {"changed": False}

        return comparison

    def cleanup_old_snapshots(self, retention_days: int = 30):
        """
        Clean up old snapshots beyond retention period.

        Args:
            retention_days: Number of days to retain snapshots
        """
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        snapshots_to_remove = []

        for snapshot_id, snapshot in self.snapshots.items():
            if snapshot.timestamp < cutoff_date:
                snapshots_to_remove.append(snapshot_id)

        for snapshot_id in snapshots_to_remove:
            # Remove snapshot file
            snapshot_file = self.repo_path / f"{snapshot_id}.json"
            if snapshot_file.exists():
                snapshot_file.unlink()

            # Remove from metadata
            del self.snapshots[snapshot_id]

        if snapshots_to_remove:
            self._save_snapshot_metadata()
            print(f"Cleaned up {len(snapshots_to_remove)} old snapshots")

    def get_repository_stats(self) -> Dict[str, Any]:
        """Get statistics about the snapshot repository"""
        total_snapshots = len(self.snapshots)
        total_size = sum(s.size_bytes for s in self.snapshots.values())

        # Group by type and agent
        by_type = {}
        by_agent = {}

        for snapshot in self.snapshots.values():
            by_type[snapshot.snapshot_type] = by_type.get(snapshot.snapshot_type, 0) + 1
            by_agent[snapshot.agent_id] = by_agent.get(snapshot.agent_id, 0) + 1

        return {
            "total_snapshots": total_snapshots,
            "total_size_bytes": total_size,
            "total_size_mb": total_size / (1024 * 1024),
            "snapshots_by_type": by_type,
            "snapshots_by_agent": by_agent,
            "oldest_snapshot": min((s.timestamp for s in self.snapshots.values()), default=None),
            "newest_snapshot": max((s.timestamp for s in self.snapshots.values()), default=None)
        }


# Convenience functions for easy integration
def create_system_snapshot(service: MemorySnapshotService,
                          agent_memories: Dict[str, Any] = None,
                          configurations: Dict[str, Any] = None,
                          workflow_states: Dict[str, Any] = None,
                          performance_metrics: Dict[str, Any] = None,
                          **kwargs) -> str:
    """
    Convenience function to create a system snapshot with individual components.

    Args:
        service: MemorySnapshotService instance
        agent_memories: Agent memory data
        configurations: System configuration data
        workflow_states: Current workflow states
        performance_metrics: Performance metrics
        **kwargs: Additional arguments for create_snapshot

    Returns:
        Snapshot ID
    """
    system_state = SystemState(
        agent_memories=agent_memories or {},
        configurations=configurations or {},
        workflow_states=workflow_states or {},
        performance_metrics=performance_metrics or {}
    )

    return service.create_snapshot(system_state, **kwargs)


def quick_restore(service: MemorySnapshotService, snapshot_id: str) -> bool:
    """
    Quick restore function that returns success status.

    Args:
        service: MemorySnapshotService instance
        snapshot_id: Snapshot ID to restore

    Returns:
        True if restoration successful, False otherwise
    """
    state = service.restore_snapshot(snapshot_id)
    return state is not None


if __name__ == "__main__":
    # Demo usage
    print("Memory Snapshot Service Demo")
    print("=" * 40)

    # Initialize service
    service = MemorySnapshotService()

    # Create a sample system state
    sample_state = SystemState(
        agent_memories={"agent1": {"task_count": 42, "last_action": "code_review"}},
        configurations={"debug_mode": True, "max_workers": 4},
        workflow_states={"active_tasks": ["task1", "task2"], "completed": 15},
        performance_metrics={"cpu_usage": 65.5, "memory_mb": 1024}
    )

    # Create snapshot
    snapshot_id = service.create_snapshot(
        sample_state,
        snapshot_type="full",
        description="Demo system state snapshot",
        tags=["demo", "full-system"],
        agent_id="demo_agent"
    )

    print(f"✓ Created snapshot: {snapshot_id}")

    # List snapshots
    snapshots = service.list_snapshots(limit=5)
    print(f"✓ Found {len(snapshots)} snapshots")

    # Restore snapshot
    restored_state = service.restore_snapshot(snapshot_id)
    if restored_state:
        print("✓ Successfully restored snapshot")
        print(f"  - Agent memories: {len(restored_state.agent_memories)} entries")
        print(f"  - Configurations: {len(restored_state.configurations)} settings")
    else:
        print("❌ Failed to restore snapshot")

    # Get repository stats
    stats = service.get_repository_stats()
    print(f"✓ Repository stats: {stats['total_snapshots']} snapshots, {stats['total_size_mb']:.2f} MB")

    print("\n🎉 Memory Snapshot Service operational!")