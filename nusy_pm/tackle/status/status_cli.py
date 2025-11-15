#!/usr/bin/env python3
"""
NuSy PM Status CLI

Command-line interface for managing artifact status in the NuSy PM system.
"""

import argparse
import sys
from pathlib import Path
from typing import List

from .status_model import StatusManager, Status, StateReason

def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        description='NuSy PM Status Management CLI',
        prog='nusy-status'
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Query command
    query_parser = subparsers.add_parser('query', help='Query artifact status')
    query_parser.add_argument('--type', choices=['feature', 'ships-log', 'experiment', 'quality-assessment'],
                             help='Filter by artifact type')
    query_parser.add_argument('--status', choices=['open', 'in_progress', 'blocked', 'closed'],
                             help='Filter by status')
    query_parser.add_argument('--assignee', help='Filter by assignee')
    query_parser.add_argument('--state-reason', choices=['completed', 'cancelled', 'duplicate', 'not_planned', 'transferred'],
                             help='Filter by closure reason')
    query_parser.add_argument('--epic', help='Filter by epic')
    query_parser.add_argument('--limit', type=int, default=50, help='Maximum number of results')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update artifact status')
    update_parser.add_argument('file', help='Path to the artifact file')
    update_parser.add_argument('--status', required=True,
                              choices=['open', 'in_progress', 'blocked', 'closed'],
                              help='New status')
    update_parser.add_argument('--reason', choices=['completed', 'cancelled', 'duplicate', 'not_planned', 'transferred'],
                              help='Closure reason (required when status is closed)')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create new artifact with status')
    create_parser.add_argument('file', help='Path to create the artifact file')
    create_parser.add_argument('--id', required=True, help='Artifact ID')
    create_parser.add_argument('--type', required=True,
                              choices=['feature', 'ships-log', 'experiment', 'quality-assessment'],
                              help='Artifact type')
    create_parser.add_argument('--assignees', nargs='*', help='Initial assignees')
    create_parser.add_argument('--labels', nargs='*', help='Initial labels')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show status of a specific artifact')
    show_parser.add_argument('file', help='Path to the artifact file')

    return parser

def format_status_display(status):
    """Format status information for display."""
    lines = []
    lines.append(f"ID: {status.id}")
    lines.append(f"Type: {status.type}")
    lines.append(f"Status: {status.status.value}")
    if status.state_reason:
        lines.append(f"Reason: {status.state_reason.value}")
    lines.append(f"Created: {status.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append(f"Updated: {status.updated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    if status.assignees:
        lines.append(f"Assignees: {', '.join(status.assignees)}")
    if status.labels:
        lines.append(f"Labels: {', '.join(status.labels)}")
    if status.epic:
        lines.append(f"Epic: {status.epic}")
    if status.related_experiments:
        lines.append(f"Related Experiments: {', '.join(status.related_experiments)}")
    if status.related_artifacts:
        lines.append(f"Related Artifacts: {', '.join(status.related_artifacts)}")
    return '\n'.join(lines)

def cmd_query(args, manager: StatusManager):
    """Handle query command."""
    # This would need to be implemented with file discovery logic
    # For now, just show usage
    print("Query functionality requires integration with file discovery.")
    print("Use 'nusy-status show <file>' to view individual artifact status.")

def cmd_update(args, manager: StatusManager):
    """Handle update command."""
    status_enum = Status(args.status)
    reason_enum = StateReason(args.reason) if args.reason else None

    if status_enum == Status.CLOSED and not reason_enum:
        print("Error: Must specify --reason when closing an artifact")
        sys.exit(1)

    success = manager.update_status(args.file, status_enum, reason_enum)
    if success:
        print(f"Successfully updated status of {args.file}")
    else:
        print(f"Failed to update status of {args.file}")
        sys.exit(1)

def cmd_create(args, manager: StatusManager):
    """Handle create command."""
    # Check if file already exists
    if Path(args.file).exists():
        print(f"Error: File {args.file} already exists")
        sys.exit(1)

    # Create basic markdown content
    content = f"# {args.id}\n\nNew {args.type} artifact.\n"

    # Write the file first
    try:
        with open(args.file, 'w') as f:
            f.write(content)
    except Exception as e:
        print(f"Error creating file {args.file}: {e}")
        sys.exit(1)

    # Add status
    success = manager.create_new_artifact(
        args.file, args.id, args.type,
        args.assignees, args.labels
    )

    if success:
        print(f"Successfully created {args.type} artifact: {args.file}")
    else:
        print(f"Failed to initialize status for {args.file}")
        sys.exit(1)

def cmd_show(args, manager: StatusManager):
    """Handle show command."""
    status = manager.load_status_from_file(args.file)
    if status:
        print(format_status_display(status))
    else:
        print(f"No status information found in {args.file}")
        sys.exit(1)

def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    manager = StatusManager()

    commands = {
        'query': cmd_query,
        'update': cmd_update,
        'create': cmd_create,
        'show': cmd_show
    }

    commands[args.command](args, manager)

if __name__ == '__main__':
    main()