#!/usr/bin/env python3
"""
DGX Readiness Prioritization Script

Uses the integrated neurosymbolic prioritizer to analyze all current work
and prioritize for DGX readiness (arrives tomorrow) vs team effectiveness.
"""

import sys
from pathlib import Path
import json
from datetime import datetime

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent / "santiago-pm"))
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tackle.kanban.kanban_service import KanbanService
from nusy_pm_core.adapters.neurosymbolic_prioritizer import NeurosymbolicPrioritizer


class DGXReadinessPrioritizer:
    """Prioritizes work for DGX readiness using neurosymbolic AI"""

    def __init__(self):
        self.kanban = KanbanService()
        self.prioritizer = NeurosymbolicPrioritizer(Path.cwd())
        self.board_id = "master_board"  # Use the master board

    def get_all_work_items(self):
        """Extract all work items from the Kanban board"""
        board = self.kanban.kanban_system.boards.get(self.board_id)
        if not board:
            print(f"❌ Board {self.board_id} not found")
            return []

        work_items = []
        for column_name, column in board.columns.items():
            for card in column.cards:
                work_item = {
                    'id': card.card_id,
                    'title': card.item_reference.title,
                    'type': card.item_reference.item_type.value,
                    'description': card.item_reference.description or "",
                    'column': column_name,
                    'assignee': card.item_reference.assignee,
                    'priority': card.item_reference.priority,
                    'estimated_effort': self._estimate_effort(card),
                    'blocked_by': [],  # TODO: Add dependency analysis
                    'blocks': [],     # TODO: Add dependency analysis
                    'required_skills': self._infer_required_skills(card),
                    'customer_value_hint': self._calculate_dgx_customer_value(card),
                    'learning_value_hint': self._calculate_learning_value(card),
                    'tags': card.tags,
                    'comments': len(card.comments)
                }
                work_items.append(work_item)

        return work_items

    def _estimate_effort(self, card):
        """Estimate effort based on item type and description"""
        item_type = card.item_reference.item_type.value
        title = card.item_reference.title.lower()
        description = (card.item_reference.description or "").lower()

        # Base effort by type
        effort_map = {
            'expedition': 13,  # Large exploratory work
            'feature': 8,      # Medium feature
            'task': 3,         # Small task
            'research_log': 5, # Research/analysis
            'bug': 2           # Bug fix
        }

        effort = effort_map.get(item_type, 5)

        # Adjust for complexity indicators
        if any(word in title + description for word in ['complex', 'hard', 'difficult', 'architectural']):
            effort *= 1.5
        if any(word in title + description for word in ['infrastructure', 'platform', 'system']):
            effort *= 1.3

        return min(int(effort), 21)  # Cap at 21 story points

    def _infer_required_skills(self, card):
        """Infer required skills from card content"""
        title = card.item_reference.title.lower()
        description = (card.item_reference.description or "").lower()
        assignee = card.item_reference.assignee or ""

        skills = []

        # DGX/Infrastructure skills
        if any(word in title + description for word in ['dgx', 'gpu', 'infrastructure', 'deployment', 'scaling']):
            skills.extend(['infrastructure', 'deployment', 'dgx'])

        # AI/ML skills
        if any(word in title + description for word in ['ai', 'ml', 'model', 'training', 'neural']):
            skills.extend(['ai', 'ml', 'deep-learning'])

        # Platform/DevOps skills
        if any(word in title + description for word in ['platform', 'devops', 'kubernetes', 'docker']):
            skills.extend(['platform', 'devops', 'containers'])

        # Testing/QA skills
        if any(word in title + description for word in ['test', 'qa', 'validation', 'quality']):
            skills.extend(['testing', 'qa'])

        # PM/Product skills
        if any(word in title + description for word in ['product', 'roadmap', 'stakeholder', 'requirements']):
            skills.extend(['product-management', 'stakeholder-management'])

        # Assign based on assignee hints
        if 'platform' in assignee:
            skills.extend(['platform', 'infrastructure'])
        elif 'ai' in assignee or 'ml' in assignee:
            skills.extend(['ai', 'ml'])
        elif 'qa' in assignee or 'test' in assignee:
            skills.extend(['testing', 'qa'])

        return list(set(skills))  # Remove duplicates

    def _calculate_dgx_customer_value(self, card):
        """Calculate customer value with DGX readiness bias"""
        title = card.item_reference.title.lower()
        description = (card.item_reference.description or "").lower()

        # Critical DGX readiness items (95% value)
        critical_dgx = [
            'dgx readiness', 'dgx deployment', 'gpu setup', 'infrastructure scaling',
            'performance optimization', 'model training pipeline', 'dgx migration'
        ]
        if any(keyword in title or keyword in description for keyword in critical_dgx):
            return 0.95

        # High value DGX enablers (85% value)
        high_dgx = [
            'platform reliability', 'monitoring system', 'deployment automation',
            'infrastructure as code', 'container orchestration'
        ]
        if any(keyword in title or keyword in description for keyword in high_dgx):
            return 0.85

        # Medium value supporting work (70% value)
        medium_dgx = [
            'testing framework', 'ci/cd pipeline', 'documentation',
            'team onboarding', 'process improvement'
        ]
        if any(keyword in title or keyword in description for keyword in medium_dgx):
            return 0.70

        # Default medium value for other work
        return 0.50

    def _calculate_learning_value(self, card):
        """Calculate learning value (how much uncertainty this reduces)"""
        title = card.item_reference.title.lower()
        description = (card.item_reference.description or "").lower()

        # High learning value (research, exploration, unknowns)
        high_learning = [
            'research', 'investigate', 'explore', 'unknown', 'experiment',
            'spike', 'proof of concept', 'evaluation', 'analysis'
        ]
        if any(keyword in title or keyword in description for keyword in high_learning):
            return 0.80

        # Medium learning value (new capabilities, complex problems)
        medium_learning = [
            'architectural', 'design', 'framework', 'system', 'integration',
            'optimization', 'scaling', 'performance'
        ]
        if any(keyword in title or keyword in description for keyword in medium_learning):
            return 0.65

        # Low learning value (routine work)
        return 0.30

    def create_dgx_context(self):
        """Create prioritization context focused on DGX readiness"""
        return {
            'available_workers': [
                {
                    'skills': ['infrastructure', 'deployment', 'dgx', 'platform'],
                    'capacity_remaining': 1.0  # Fully available for DGX work
                },
                {
                    'skills': ['ai', 'ml', 'deep-learning', 'training'],
                    'capacity_remaining': 0.9  # High priority but some existing commitments
                },
                {
                    'skills': ['platform', 'devops', 'containers', 'scaling'],
                    'capacity_remaining': 0.95  # Critical for DGX success
                },
                {
                    'skills': ['testing', 'qa', 'validation'],
                    'capacity_remaining': 0.7  # Important but lower priority
                },
                {
                    'skills': ['product-management', 'stakeholder-management'],
                    'capacity_remaining': 0.6  # Some availability for coordination
                }
            ],
            'hypotheses': [
                {
                    'related_to': 'dgx-readiness-preparation',
                    'confidence': 0.98  # Extremely high confidence in DGX importance
                },
                {
                    'related_to': 'infrastructure-scaling',
                    'confidence': 0.95
                },
                {
                    'related_to': 'ai-training-pipeline',
                    'confidence': 0.92
                },
                {
                    'related_to': 'platform-reliability',
                    'confidence': 0.90
                }
            ],
            'backlog_items': []  # Will be populated with all items for dependency analysis
        }

    def prioritize_for_dgx_readiness(self):
        """Run full DGX readiness prioritization"""
        print("🚀 DGX Readiness Prioritization Analysis")
        print("=" * 60)
        print("🎯 Goal: DGX arrives tomorrow - prioritize critical path items")
        print("📊 Using neurosymbolic AI with multi-factor scoring")
        print()

        # Get all work items
        work_items = self.get_all_work_items()
        if not work_items:
            print("❌ No work items found in the board")
            return

        print(f"📋 Found {len(work_items)} work items to prioritize")

        # Create DGX-focused context
        context = self.create_dgx_context()
        context['backlog_items'] = work_items  # For dependency analysis

        # Run prioritization
        print("\n🔄 Running neurosymbolic prioritization...")
        results = self.prioritizer.prioritize_backlog(work_items, context)

        # Analyze results
        self._analyze_and_display_results(results, work_items)

        # Generate action plan
        self._generate_dgx_action_plan(results, work_items)

        return results

    def _analyze_and_display_results(self, results, work_items):
        """Analyze and display prioritization results"""
        print(f"\n📊 DGX Readiness Prioritization Results ({len(results)} items)")
        print("=" * 60)

        # Group by category
        categories = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for result in results:
            categories[result.category].append(result)

        # Display by priority category
        for category in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            items = categories[category]
            if items:
                print(f"\n{category} PRIORITY ({len(items)} items):")
                print("-" * 40)

                for i, result in enumerate(items, 1):
                    # Get original item details
                    item = next((wi for wi in work_items if wi['id'] == result.item_id), {})
                    assignee = item.get('assignee', 'unassigned')
                    effort = item.get('estimated_effort', '?')
                    skills = item.get('required_skills', [])

                    print(f"{i}. {result.item_id}")
                    print(f"   📝 {item.get('title', 'Unknown')}")
                    print(f"   👤 {assignee} | ⏱️ {effort} pts | 🛠️ {', '.join(skills) if skills else 'general'}")
                    print(f"   🎯 Score: {result.priority_score:.2f}")

                    # Show key factors
                    factors = result.factors
                    factor_summary = []
                    if factors.customer_value >= 0.8:
                        factor_summary.append("💰 High Value")
                    if factors.unblock_impact >= 0.6:
                        factor_summary.append("🔓 Unblocks Work")
                    if factors.worker_availability >= 0.8:
                        factor_summary.append("👷 Available Skills")
                    if factors.learning_value >= 0.7:
                        factor_summary.append("🧠 High Learning")

                    if factor_summary:
                        print(f"   ⭐ {', '.join(factor_summary)}")

                    # Show rationale (first 2 lines)
                    rationale_lines = result.rationale.split('\n')[:2]
                    for line in rationale_lines:
                        if line.strip():
                            print(f"   💡 {line.strip()}")
                    print()

        # Summary stats
        print("\n📈 Summary Statistics:")
        print("-" * 30)
        total_items = len(results)
        critical_pct = len(categories['CRITICAL']) / total_items * 100
        high_pct = len(categories['HIGH']) / total_items * 100

        print(f"Total items: {total_items}")
        print(f"Critical priority: {len(categories['CRITICAL'])} ({critical_pct:.1f}%)")
        print(f"High priority: {len(categories['HIGH'])} ({high_pct:.1f}%)")
        print(f"Ready to execute: {len([r for r in results if r.category in ['CRITICAL', 'HIGH']])} items")

    def _generate_dgx_action_plan(self, results, work_items):
        """Generate actionable DGX readiness plan"""
        print("\n🚀 DGX Readiness Action Plan")
        print("=" * 60)

        # Get top 5 critical items
        critical_items = [r for r in results if r.category == 'CRITICAL'][:5]
        high_items = [r for r in results if r.category == 'HIGH'][:5]

        print("🎯 IMMEDIATE FOCUS (Next 24 hours - DGX arrives tomorrow):")
        print("-" * 50)

        for i, result in enumerate(critical_items, 1):
            item = next((wi for wi in work_items if wi['id'] == result.item_id), {})
            assignee = item.get('assignee', 'UNASSIGNED')
            effort = item.get('estimated_effort', '?')

            status = "🚨 UNASSIGNED" if assignee == 'UNASSIGNED' else f"👤 {assignee}"
            print(f"{i}. {item.get('title', 'Unknown')} ({effort} pts) - {status}")

        print("\n⚡ HIGH PRIORITY (Week 1 - Post DGX arrival):")
        print("-" * 45)

        for i, result in enumerate(high_items, 1):
            item = next((wi for wi in work_items if wi['id'] == result.item_id), {})
            assignee = item.get('assignee', 'UNASSIGNED')
            effort = item.get('estimated_effort', '?')

            status = "🚨 UNASSIGNED" if assignee == 'UNASSIGNED' else f"👤 {assignee}"
            print(f"{i}. {item.get('title', 'Unknown')} ({effort} pts) - {status}")

        # Resource allocation
        print("\n👥 Resource Allocation:")
        print("-" * 25)

        assigned_work = {}
        for result in results[:10]:  # Top 10 priorities
            item = next((wi for wi in work_items if wi['id'] == result.item_id), {})
            assignee = item.get('assignee', 'unassigned')
            if assignee not in assigned_work:
                assigned_work[assignee] = []
            assigned_work[assignee].append(item.get('title', 'Unknown'))

        for assignee, tasks in assigned_work.items():
            if assignee == 'unassigned':
                print(f"🚨 {assignee.upper()}: {len(tasks)} items need assignment")
            else:
                print(f"👤 {assignee}: {len(tasks)} items")

        print("\n💡 Recommendations:")
        print("- Assign unassigned critical items immediately")
        print("- Focus 80% of team capacity on top 5 priorities")
        print("- Set up daily standups for DGX readiness progress")
        print("- Prepare rollback plans for high-risk items")

        # Save detailed plan
        self._save_detailed_plan(results, work_items)

    def _save_detailed_plan(self, results, work_items):
        """Save detailed prioritization results to file"""
        plan_data = {
            'generated_at': str(datetime.now()),
            'total_items': len(results),
            'dgx_readiness_plan': []
        }

        for result in results:
            item = next((wi for wi in work_items if wi['id'] == result.item_id), {})
            plan_data['dgx_readiness_plan'].append({
                'rank': len(plan_data['dgx_readiness_plan']) + 1,
                'item_id': result.item_id,
                'title': item.get('title', 'Unknown'),
                'category': result.category,
                'priority_score': result.priority_score,
                'assignee': item.get('assignee', 'unassigned'),
                'estimated_effort': item.get('estimated_effort', 0),
                'required_skills': item.get('required_skills', []),
                'rationale': result.rationale,
                'factors': {
                    'customer_value': result.factors.customer_value,
                    'unblock_impact': result.factors.unblock_impact,
                    'worker_availability': result.factors.worker_availability,
                    'learning_value': result.factors.learning_value
                }
            })

        # Save to file
        with open('dgx-readiness-priorities.json', 'w') as f:
            json.dump(plan_data, f, indent=2)

        print(f"\n💾 Detailed plan saved to: dgx-readiness-priorities.json")


def main():
    """Run DGX readiness prioritization"""
    prioritizer = DGXReadinessPrioritizer()
    prioritizer.prioritize_for_dgx_readiness()


if __name__ == "__main__":
    main()