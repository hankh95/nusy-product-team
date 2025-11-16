#!/usr/bin/env python3
"""
NuSy PM Status System Models and Logic

This module provides the core data structures and business logic for the
NuSy PM status system, enabling standardized tracking of all artifacts.
"""

import yaml
import os
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class Status(Enum):
    """Primary status values for all artifacts."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    CLOSED = "closed"

class StateReason(Enum):
    """Closure reasons for closed artifacts."""
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DUPLICATE = "duplicate"
    NOT_PLANNED = "not_planned"
    TRANSFERRED = "transferred"

@dataclass
class ArtifactStatus:
    """Represents the status of a NuSy PM artifact."""
    id: str
    type: str
    status: Status
    state_reason: Optional[StateReason] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    assignees: List[str] = field(default_factory=list)
    labels: List[str] = field(default_factory=list)
    epic: Optional[str] = None
    related_experiments: List[str] = field(default_factory=list)
    related_artifacts: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization."""
        data = {
            'id': self.id,
            'type': self.type,
            'status': self.status.value,
            'state_reason': self.state_reason.value if self.state_reason else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'assignees': self.assignees,
            'labels': self.labels,
        }
        if self.epic:
            data['epic'] = self.epic
        if self.related_experiments:
            data['related_experiments'] = self.related_experiments
        if self.related_artifacts:
            data['related_artifacts'] = self.related_artifacts
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ArtifactStatus':
        """Create from dictionary (YAML deserialization)."""
        # Parse enums
        status = Status(data['status'])
        state_reason = StateReason(data['state_reason']) if data.get('state_reason') else None

        # Parse timestamps
        created_at = datetime.fromisoformat(data['created_at']) if 'created_at' in data else datetime.now(timezone.utc)
        updated_at = datetime.fromisoformat(data['updated_at']) if 'updated_at' in data else datetime.now(timezone.utc)

        return cls(
            id=data['id'],
            type=data['type'],
            status=status,
            state_reason=state_reason,
            created_at=created_at,
            updated_at=updated_at,
            assignees=data.get('assignees', []),
            labels=data.get('labels', []),
            epic=data.get('epic'),
            related_experiments=data.get('related_experiments', []),
            related_artifacts=data.get('related_artifacts', [])
        )

    def can_transition_to(self, new_status: Status, new_reason: Optional[StateReason] = None) -> bool:
        """Check if a status transition is valid."""
        if self.status == new_status:
            return True  # No change is always allowed

        # Define valid transitions
        transitions = {
            Status.OPEN: [Status.IN_PROGRESS, Status.BLOCKED, Status.CLOSED],
            Status.IN_PROGRESS: [Status.OPEN, Status.BLOCKED, Status.CLOSED],
            Status.BLOCKED: [Status.OPEN, Status.IN_PROGRESS, Status.CLOSED],
            Status.CLOSED: []  # Closed items cannot be reopened
        }

        if new_status not in transitions[self.status]:
            return False

        # If closing, must have a reason
        if new_status == Status.CLOSED and not new_reason:
            return False

        return True

    def transition_to(self, new_status: Status, new_reason: Optional[StateReason] = None) -> bool:
        """Attempt to transition to a new status."""
        if not self.can_transition_to(new_status, new_reason):
            return False

        self.status = new_status
        if new_status == Status.CLOSED:
            self.state_reason = new_reason
        self.updated_at = datetime.now(timezone.utc)
        return True

class StatusManager:
    """Manages status operations for artifacts."""

    def __init__(self, base_path: str = "."):
        self.base_path = base_path

    def load_status_from_file(self, file_path: str) -> Optional[ArtifactStatus]:
        """Load status from a markdown file's frontmatter."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.startswith('---'):
                return None

            # Find end of frontmatter
            end_pos = content.find('---', 3)
            if end_pos == -1:
                return None

            frontmatter = content[3:end_pos].strip()
            data = yaml.safe_load(frontmatter)
            if data and 'id' in data:
                return ArtifactStatus.from_dict(data)

        except Exception as e:
            print(f"Error loading status from {file_path}: {e}")

        return None

    def save_status_to_file(self, file_path: str, status: ArtifactStatus) -> bool:
        """Save status to a markdown file's frontmatter."""
        try:
            # Read existing content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Prepare new frontmatter
            frontmatter = yaml.dump(status.to_dict(), default_flow_style=False, sort_keys=False)
            new_content = f"---\n{frontmatter}---\n"

            # Replace or add frontmatter
            if content.startswith('---'):
                end_pos = content.find('---', 3)
                if end_pos != -1:
                    body = content[end_pos + 3:].lstrip()
                    new_content += body
            else:
                new_content += content

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return True

        except Exception as e:
            print(f"Error saving status to {file_path}: {e}")
            return False

    def create_new_artifact(self, file_path: str, artifact_id: str, artifact_type: str,
                          assignees: Optional[List[str]] = None, labels: Optional[List[str]] = None) -> bool:
        """Create a new artifact with initial status."""
        status = ArtifactStatus(
            id=artifact_id,
            type=artifact_type,
            status=Status.OPEN,
            assignees=assignees or [],
            labels=labels or []
        )
        return self.save_status_to_file(file_path, status)

    def update_status(self, file_path: str, new_status: Status,
                     new_reason: Optional[StateReason] = None) -> bool:
        """Update the status of an existing artifact."""
        status = self.load_status_from_file(file_path)
        if not status:
            print(f"No status found in {file_path}")
            return False

        if not status.transition_to(new_status, new_reason):
            print(f"Invalid status transition for {file_path}")
            return False

        return self.save_status_to_file(file_path, status)