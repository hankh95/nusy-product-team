#!/usr/bin/env python3
"""
Basic tests for the NuSy PM Status Module
"""

import tempfile
import os
from datetime import datetime, timezone

from nusy_pm.modules.status import (
    ArtifactStatus,
    Status,
    StateReason,
    StatusManager
)

def test_artifact_status():
    """Test ArtifactStatus creation and transitions."""
    print("Testing ArtifactStatus...")

    # Create a new artifact
    status = ArtifactStatus(
        id="test-001",
        type="feature",
        status=Status.OPEN,
        assignees=["alice", "bob"],
        labels=["priority:high", "type:feature"]
    )

    assert status.id == "test-001"
    assert status.status == Status.OPEN
    assert status.assignees == ["alice", "bob"]

    # Test valid transition
    assert status.can_transition_to(Status.IN_PROGRESS)
    assert status.transition_to(Status.IN_PROGRESS)
    assert status.status == Status.IN_PROGRESS

    # Test invalid transition (closed without reason)
    assert not status.can_transition_to(Status.CLOSED)
    assert not status.transition_to(Status.CLOSED)

    # Test valid closure
    assert status.transition_to(Status.CLOSED, StateReason.COMPLETED)
    assert status.status == Status.CLOSED
    assert status.state_reason == StateReason.COMPLETED

    print("✓ ArtifactStatus tests passed")

def test_status_manager():
    """Test StatusManager file operations."""
    print("Testing StatusManager...")

    with tempfile.TemporaryDirectory() as tmpdir:
        manager = StatusManager(tmpdir)

        # Create a test file
        test_file = os.path.join(tmpdir, "test.md")
        with open(test_file, 'w') as f:
            f.write("# Test Feature\n\nThis is a test.\n")

        # Create new artifact
        success = manager.create_new_artifact(
            test_file, "test-001", "feature",
            assignees=["alice"], labels=["test"]
        )
        assert success

        # Load and verify
        loaded = manager.load_status_from_file(test_file)
        assert loaded is not None
        assert loaded.id == "test-001"
        assert loaded.type == "feature"
        assert loaded.status == Status.OPEN
        assert loaded.assignees == ["alice"]
        assert loaded.labels == ["test"]

        # Update status
        success = manager.update_status(test_file, Status.IN_PROGRESS)
        assert success

        loaded = manager.load_status_from_file(test_file)
        assert loaded is not None
        assert loaded.status == Status.IN_PROGRESS

        print("✓ StatusManager tests passed")

def test_yaml_serialization():
    """Test YAML serialization/deserialization."""
    print("Testing YAML serialization...")

    status = ArtifactStatus(
        id="test-002",
        type="experiment",
        status=Status.IN_PROGRESS,
        assignees=["charlie"],
        epic="test-epic"
    )

    # Convert to dict
    data = status.to_dict()
    assert data['id'] == "test-002"
    assert data['status'] == "in_progress"
    assert data['assignees'] == ["charlie"]
    assert data['epic'] == "test-epic"

    # Convert back
    restored = ArtifactStatus.from_dict(data)
    assert restored.id == status.id
    assert restored.status == status.status
    assert restored.assignees == status.assignees
    assert restored.epic == status.epic

    print("✓ YAML serialization tests passed")

def run_tests():
    """Run all tests."""
    print("Running NuSy PM Status Module Tests")
    print("=" * 40)

    try:
        test_artifact_status()
        test_status_manager()
        test_yaml_serialization()

        print("=" * 40)
        print("✓ All tests passed!")

    except Exception as e:
        print(f"✗ Test failed: {e}")
        raise

if __name__ == "__main__":
    run_tests()