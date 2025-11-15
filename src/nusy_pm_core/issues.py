"""Issues Service."""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from rdflib import URIRef, Literal

from .models.issue import Issue, Comment, IssueStatus, IssuePriority
from .models.kg import KGNode, KGRelation
from .knowledge.graph import KnowledgeGraph, NUSY


class IssuesService:
    """Service for managing issues, comments, and tracking."""

    def __init__(self, issues_file: Optional[Path] = None, kg: Optional[KnowledgeGraph] = None):
        self.issues_file = issues_file or Path(__file__).resolve().parents[2] / "data" / "issues.json"
        self.issues_file.parent.mkdir(parents=True, exist_ok=True)
        self.kg = kg or KnowledgeGraph()
        self._issues: Dict[str, Issue] = {}
        self._load_issues()

    def _load_issues(self) -> None:
        """Load issues from storage."""
        if self.issues_file.exists():
            with open(self.issues_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for issue_data in data.get('issues', []):
                    issue = self._deserialize_issue(issue_data)
                    self._issues[issue.id] = issue

    def _save_issues(self) -> None:
        """Save issues to storage."""
        data = {
            'issues': [self._serialize_issue(issue) for issue in self._issues.values()]
        }
        with open(self.issues_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def _serialize_issue(self, issue: Issue) -> Dict[str, Any]:
        """Serialize an issue to dictionary."""
        return {
            'id': issue.id,
            'title': issue.title,
            'description': issue.description,
            'status': issue.status.value,
            'priority': issue.priority.value,
            'assignee': issue.assignee,
            'reporter': issue.reporter,
            'labels': issue.labels,
            'comments': [self._serialize_comment(c) for c in issue.comments],
            'linked_prs': issue.linked_prs,
            'linked_commits': issue.linked_commits,
            'created_at': issue.created_at,
            'updated_at': issue.updated_at
        }

    def _deserialize_issue(self, data: Dict[str, Any]) -> Issue:
        """Deserialize an issue from dictionary."""
        issue = Issue(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            status=IssueStatus(data['status']),
            priority=IssuePriority(data['priority']),
            assignee=data.get('assignee'),
            reporter=data['reporter'],
            labels=data.get('labels', []),
            comments=[self._deserialize_comment(c) for c in data.get('comments', [])],
            linked_prs=data.get('linked_prs', []),
            linked_commits=data.get('linked_commits', []),
            created_at=data['created_at'],
            updated_at=data['updated_at']
        )
        return issue

    def _serialize_comment(self, comment: Comment) -> Dict[str, Any]:
        """Serialize a comment to dictionary."""
        return {
            'id': comment.id,
            'author': comment.author,
            'content': comment.content,
            'created_at': comment.created_at
        }

    def _deserialize_comment(self, data: Dict[str, Any]) -> Comment:
        """Deserialize a comment from dictionary."""
        return Comment(
            id=data['id'],
            author=data['author'],
            content=data['content'],
            created_at=data['created_at']
        )

    def create_issue(self, title: str, description: str, reporter: str, priority: IssuePriority = IssuePriority.MEDIUM) -> Issue:
        """Create a new issue."""
        issue = Issue.create(title, description, reporter, priority)
        self._issues[issue.id] = issue
        self._save_issues()

        # Add to KG
        issue_uri = URIRef(f"{NUSY}issue/{issue.id}")
        self.kg.add_node(KGNode(issue_uri, title, NUSY.Issue))
        self.kg.add_relation(KGRelation(issue_uri, NUSY.description, Literal(description)))
        self.kg.add_relation(KGRelation(issue_uri, NUSY.status, Literal(issue.status.value)))
        self.kg.add_relation(KGRelation(issue_uri, NUSY.priority, Literal(issue.priority.value)))
        self.kg.add_relation(KGRelation(issue_uri, NUSY.reporter, Literal(reporter)))
        self.kg.save()

        return issue

    def get_issue(self, issue_id: str) -> Optional[Issue]:
        """Get an issue by ID."""
        return self._issues.get(issue_id)

    def list_issues(self, status_filter: Optional[IssueStatus] = None, label_filter: Optional[str] = None) -> List[Issue]:
        """List all issues, optionally filtered by status or label."""
        issues = list(self._issues.values())
        if status_filter:
            issues = [i for i in issues if i.status == status_filter]
        if label_filter:
            issues = [i for i in issues if label_filter in i.labels]
        return sorted(issues, key=lambda i: i.created_at, reverse=True)

    def assign_issue(self, issue_id: str, assignee: str) -> bool:
        """Assign an issue to a user."""
        issue = self._issues.get(issue_id)
        if not issue:
            return False

        issue.assign_to(assignee)
        self._save_issues()

        # Update KG
        issue_uri = URIRef(f"{NUSY}issue/{issue_id}")
        self.kg.add_relation(KGRelation(issue_uri, NUSY.assignee, Literal(assignee)))
        self.kg.save()

        return True

    def add_comment(self, issue_id: str, author: str, content: str) -> Optional[Comment]:
        """Add a comment to an issue."""
        issue = self._issues.get(issue_id)
        if not issue:
            return None

        comment = Comment.create(author, content)
        issue.add_comment(comment)
        self._save_issues()

        # Add to KG
        comment_uri = URIRef(f"{NUSY}comment/{comment.id}")
        issue_uri = URIRef(f"{NUSY}issue/{issue_id}")
        self.kg.add_node(KGNode(comment_uri, f"Comment by {author}", NUSY.Comment))
        self.kg.add_relation(KGRelation(issue_uri, NUSY.hasComment, comment_uri))
        self.kg.add_relation(KGRelation(comment_uri, NUSY.author, Literal(author)))
        self.kg.add_relation(KGRelation(comment_uri, NUSY.content, Literal(content)))
        self.kg.save()

        return comment

    def add_label(self, issue_id: str, label: str) -> bool:
        """Add a label to an issue."""
        issue = self._issues.get(issue_id)
        if not issue:
            return False

        issue.add_label(label)
        self._save_issues()

        # Update KG
        issue_uri = URIRef(f"{NUSY}issue/{issue_id}")
        self.kg.add_relation(KGRelation(issue_uri, NUSY.hasLabel, Literal(label)))
        self.kg.save()

        return True

    def link_pr(self, issue_id: str, pr_url: str) -> bool:
        """Link a pull request to an issue."""
        issue = self._issues.get(issue_id)
        if not issue:
            return False

        issue.link_pr(pr_url)
        self._save_issues()

        # Update KG
        issue_uri = URIRef(f"{NUSY}issue/{issue_id}")
        self.kg.add_relation(KGRelation(issue_uri, NUSY.linkedPR, Literal(pr_url)))
        self.kg.save()

        return True

    def update_status(self, issue_id: str, status: IssueStatus) -> bool:
        """Update an issue's status."""
        issue = self._issues.get(issue_id)
        if not issue:
            return False

        issue.status = status
        issue.updated_at = datetime.now(timezone.utc).isoformat()
        self._save_issues()

        # Update KG
        issue_uri = URIRef(f"{NUSY}issue/{issue_id}")
        self.kg.add_relation(KGRelation(issue_uri, NUSY.status, Literal(status.value)))
        self.kg.save()

        return True