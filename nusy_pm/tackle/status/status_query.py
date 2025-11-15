#!/usr/bin/env python3
"""
NuSy PM Status Query Tool

A simple CLI tool to query status of artifacts in the NuSy PM system.
This demonstrates the status system integration.
"""

import argparse
import yaml
import os
import glob
from datetime import datetime
from pathlib import Path

def load_frontmatter(file_path):
    """Load YAML frontmatter from a markdown file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        if content.startswith('---'):
            # Find the end of frontmatter
            end_pos = content.find('---', 3)
            if end_pos != -1:
                frontmatter = content[3:end_pos].strip()
                return yaml.safe_load(frontmatter)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return None

def find_artifacts(base_path, artifact_type=None):
    """Find all artifacts of a given type."""
    artifacts = []

    # Define search patterns for different artifact types
    patterns = {
        'feature': 'nusy_pm/cargo-manifests/*.feature',
        'ships-log': 'nusy_pm/ships-logs/*.md',
        'experiment': 'nusy_pm/expeditions/*/*.md',
        'quality-assessment': 'nusy_pm/quality-assessments/*.md'
    }

    if artifact_type and artifact_type in patterns:
        pattern = patterns[artifact_type]
    else:
        # Search all patterns
        pattern = 'nusy_pm/**/*.{feature,md}'

    for file_path in glob.glob(pattern, recursive=True):
        if os.path.isfile(file_path):
            frontmatter = load_frontmatter(file_path)
            if frontmatter:
                artifacts.append({
                    'file_path': file_path,
                    'frontmatter': frontmatter,
                    'filename': os.path.basename(file_path)
                })

    return artifacts

def query_status(args):
    """Query artifacts by status criteria."""
    artifacts = find_artifacts('.', args.type)

    filtered = []
    for artifact in artifacts:
        fm = artifact['frontmatter']

        # Apply filters
        if args.status and fm.get('status') != args.status:
            continue
        if args.assignee and args.assignee not in fm.get('assignees', []):
            continue
        if args.state_reason and fm.get('state_reason') != args.state_reason:
            continue
        if args.epic and fm.get('epic') != args.epic:
            continue

        filtered.append(artifact)

    # Sort by updated_at descending
    filtered.sort(key=lambda x: x['frontmatter'].get('updated_at', ''), reverse=True)

    # Display results
    if not filtered:
        print("No artifacts found matching criteria.")
        return

    print(f"Found {len(filtered)} artifacts:")
    print("-" * 80)

    for artifact in filtered:
        fm = artifact['frontmatter']
        print(f"ID: {fm.get('id', 'unknown')}")
        print(f"Type: {fm.get('type', 'unknown')}")
        print(f"Status: {fm.get('status', 'unknown')}")
        if fm.get('state_reason'):
            print(f"Reason: {fm.get('state_reason')}")
        print(f"Assignees: {', '.join(fm.get('assignees', []))}")
        print(f"Labels: {', '.join(fm.get('labels', []))}")
        print(f"File: {artifact['filename']}")
        print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description='NuSy PM Status Query Tool')
    parser.add_argument('--type', choices=['feature', 'ships-log', 'experiment', 'quality-assessment'],
                       help='Filter by artifact type')
    parser.add_argument('--status', choices=['open', 'in_progress', 'blocked', 'closed'],
                       help='Filter by status')
    parser.add_argument('--assignee', help='Filter by assignee')
    parser.add_argument('--state-reason', choices=['completed', 'cancelled', 'duplicate', 'not_planned', 'transferred'],
                       help='Filter by closure reason')
    parser.add_argument('--epic', help='Filter by epic')

    args = parser.parse_args()
    query_status(args)

if __name__ == '__main__':
    main()