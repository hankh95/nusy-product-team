#!/usr/bin/env python3
"""
Analyze features for backlog prioritization using NeurosymbolicPrioritizer.
"""

import os
import sys
import yaml
from pathlib import Path

# Add src to path so we can import nusy_pm_core
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from nusy_pm_core.adapters.neurosymbolic_prioritizer import NeurosymbolicPrioritizer

def parse_feature_file(filepath):
    """Parse a feature file to extract basic info."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract title from first line
    lines = content.split('\n')
    title_line = next((line for line in lines if line.startswith('Feature:')), '')
    title = title_line.replace('Feature:', '').strip() if title_line else filepath.stem

    # Count scenarios as rough effort estimate
    scenarios = content.count('Scenario:')
    effort = max(3, min(13, scenarios * 2))  # 3-13 story points

    # Extract some context from background
    background_start = content.find('Background:')
    if background_start != -1:
        background_end = content.find('Scenario:', background_start)
        if background_end == -1:
            background_end = len(content)
        background = content[background_start:background_end]
    else:
        background = ""

    return {
        'id': f"F-{filepath.stem.upper().replace("-", "_")}",
        'title': title,
        'estimated_effort': effort,
        'description': background[:200] + '...' if len(background) > 200 else background,
        'filepath': str(filepath)
    }

def create_backlog_items():
    """Create backlog items from feature files."""
    features_dir = Path('/Users/hankhead/Projects/Personal/nusy-product-team/features')
    items = []

    for feature_file in features_dir.glob('*.feature'):
        item = parse_feature_file(feature_file)

        # Add some reasonable defaults for prioritization
        item.update({
            'blocked_by': [],  # Assume none are blocked initially
            'blocks': [],      # Assume none block others initially
            'required_skills': ['Technical-Architecture', 'Development'],  # Technical work
            'customer_value_hint': 0.3,  # Low priority as requested
            'learning_value_hint': 0.7,  # High learning value for technical features
            'type': 'feature-implementation'
        })

        items.append(item)

    return items

def main():
    """Run prioritization analysis."""
    print("🔄 Analyzing features for backlog prioritization...")

    # Create backlog items from features
    items = create_backlog_items()

    print(f"📊 Found {len(items)} feature files:")
    for item in items:
        print(f"  • {item['id']}: {item['title']} ({item['estimated_effort']} pts)")

    # Initialize prioritizer
    workspace_path = Path('/Users/hankhead/Projects/Personal/nusy-product-team')
    prioritizer = NeurosymbolicPrioritizer(workspace_path)

    # Create minimal context (no workers available, so availability will be low)
    context = {
        'available_workers': [],  # No workers specified = low availability
        'backlog_items': items,
        'hypotheses': []
    }

    # Prioritize backlog
    results = prioritizer.prioritize_backlog(items, context)

    print(f"\n📋 Prioritized Backlog ({len(results)} items):\n")
    print("Rank | ID | Priority | Category | Title")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        print("2d")

    print("\n📝 Detailed Analysis:")
    for result in results:
        print(f"\n{result.item_id}: {result.category} ({result.priority_score:.2f})")
        print(f"  Title: {result.rationale.split('because:')[0].strip()}")
        print(f"  Rationale: {result.rationale}")

    # Summary for PM review
    print(f"\n🎯 Recommendation for PM/Architect Review:")
    print(f"All {len(items)} features assigned LOW priority as requested.")
    print("These technical features should be reviewed by PM/Architect before implementation.")
    print("Consider dependencies between features and alignment with product strategy.")

if __name__ == "__main__":
    main()