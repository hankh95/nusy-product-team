"""Issues Domain Models."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import uuid4


class IssueStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class IssuePriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Comment:
    id: str
    author: str
    content: str
    created_at: str

    @staticmethod
    def create(author: str, content: str) -> "Comment":
        return Comment(
            id=uuid4().hex,
            author=author,
            content=content,
            created_at=datetime.now(timezone.utc).isoformat()
        )


@dataclass
class Issue:
    id: str
    title: str
    description: str
    status: IssueStatus
    priority: IssuePriority
    assignee: Optional[str]
    reporter: str
    labels: List[str]
    comments: List[Comment]
    linked_prs: List[str]  # Pull request URLs or IDs
    linked_commits: List[str]  # Commit hashes
    created_at: str
    updated_at: str

    @staticmethod
    def create(title: str, description: str, reporter: str, priority: IssuePriority = IssuePriority.MEDIUM) -> "Issue":
        now = datetime.now(timezone.utc).isoformat()
        return Issue(
            id=uuid4().hex,
            title=title,
            description=description,
            status=IssueStatus.OPEN,
            priority=priority,
            assignee=None,
            reporter=reporter,
            labels=[],
            comments=[],
            linked_prs=[],
            linked_commits=[],
            created_at=now,
            updated_at=now
        )

    def add_comment(self, comment: Comment) -> None:
        self.comments.append(comment)
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def assign_to(self, assignee: str) -> None:
        self.assignee = assignee
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_label(self, label: str) -> None:
        if label not in self.labels:
            self.labels.append(label)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def link_pr(self, pr_url: str) -> None:
        if pr_url not in self.linked_prs:
            self.linked_prs.append(pr_url)
            self.updated_at = datetime.now(timezone.utc).isoformat()

    def link_commit(self, commit_hash: str) -> None:
        if commit_hash not in self.linked_commits:
            self.linked_commits.append(commit_hash)
            self.updated_at = datetime.now(timezone.utc).isoformat()