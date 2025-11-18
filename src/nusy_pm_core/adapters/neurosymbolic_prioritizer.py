"""
Neurosymbolic Backlog Prioritization - F-026 Phase 1
=====================================================
Implements intelligent work prioritization using KG queries + probabilistic reasoning.

Key Innovation:
- Not static formulas (WSJF, MoSCoW)
- Queries KG for real-time state (workers, dependencies, value, capacity)
- Probabilistic evaluation with confidence scores
- Explainable reasoning (provenance + rationale)

Formula:
priority_score = (customer_value * 0.4) + (unblock_impact * 0.3) + 
                 (worker_availability * 0.2) + (learning_value * 0.1)

Success Criteria:
- Priority scores match human judgment 85% of time
- Explanations include rationale for each factor
- Blocked items automatically deprioritized (50% penalty)
- Real-time recalculation when KG state changes
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import math


@dataclass
class PriorityFactors:
    """
    Factors used in neurosymbolic priority calculation.
    All factors are normalized 0.0-1.0.
    """
    customer_value: float  # 0.0-1.0 (from hypothesis confidence, user importance)
    unblock_impact: float  # 0.0-1.0 (number of downstream items this unblocks)
    worker_availability: float  # 0.0-1.0 (skill match with available workers)
    learning_value: float  # 0.0-1.0 (how much uncertainty this reduces)
    
    # Penalties
    blocked_penalty: float = 0.0  # 0.5 if blocked by other items
    
    # Metadata
    confidence: float = 1.0  # Confidence in factor calculations
    
    def __post_init__(self):
        """Validate all factors are in valid range."""
        for field in [self.customer_value, self.unblock_impact, 
                     self.worker_availability, self.learning_value]:
            if not 0.0 <= field <= 1.0:
                raise ValueError(f"Factor must be between 0.0 and 1.0, got {field}")


@dataclass
class PriorityResult:
    """
    Result of priority calculation with explanation.
    """
    item_id: str
    priority_score: float  # 0.0-1.0 final weighted score
    factors: PriorityFactors
    rationale: str  # Human-readable explanation
    category: str  # CRITICAL, HIGH, MEDIUM, LOW
    confidence: float  # Confidence in this score (0.0-1.0)
    calculated_at: str  # ISO timestamp


class NeurosymbolicPrioritizer:
    """
    Neurosymbolic backlog prioritization engine.
    
    Uses KG queries + probabilistic reasoning to calculate optimal work order.
    Explainable: Every score comes with rationale.
    Adaptive: Learns from outcomes over time (Phase 2).
    """
    
    def __init__(self, workspace_path: Path, kg_store=None):
        """
        Initialize prioritizer with workspace and optional KG.
        
        Args:
            workspace_path: Root of workspace
            kg_store: Optional KGStore instance (for querying state)
        """
        self.workspace_path = Path(workspace_path)
        self.kg_store = kg_store
        
        # Weights for priority formula (can be learned over time)
        self.weights = {
            'customer_value': 0.4,
            'unblock_impact': 0.3,
            'worker_availability': 0.2,
            'learning_value': 0.1
        }
        
        # Category thresholds
        self.thresholds = {
            'CRITICAL': 0.90,  # Drop everything
            'HIGH': 0.70,      # Top 3 priority
            'MEDIUM': 0.40,    # Important but not urgent
            'LOW': 0.0         # Nice to have
        }
    
    
    def calculate_priority(
        self,
        item: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> PriorityResult:
        """
        Calculate priority score for backlog item.
        
        Args:
            item: Backlog item dict with:
                - id: Item ID (e.g., "F-027", "BI-042")
                - title: Brief description
                - estimated_effort: Story points (1-21)
                - blocked_by: List of blocking item IDs
                - blocks: List of items this unblocks
                - required_skills: Skills needed
                - customer_value_hint: Optional explicit value (0.0-1.0)
                - learning_value_hint: Optional explicit learning value
            
            context: Optional context dict with:
                - available_workers: List of worker dicts with skills
                - backlog_items: All backlog items (for dependency analysis)
                - hypotheses: Customer hypotheses with confidence scores
        
        Returns:
            PriorityResult with score, factors, rationale, category
        
        Example:
            result = prioritizer.calculate_priority(
                item={'id': 'F-027', 'title': 'Personal Logs', 
                      'estimated_effort': 5, 'blocks': ['F-029']},
                context={'available_workers': [{'skills': ['PM']}]}
            )
            print(f"Priority: {result.priority_score:.2f}")
            print(f"Rationale: {result.rationale}")
        """
        # Extract context (or use defaults)
        if context is None:
            context = self._get_default_context()
        
        # Calculate each factor
        factors = self._calculate_factors(item, context)
        
        # Calculate weighted score
        raw_score = self._weighted_score(factors)
        
        # Apply blocked penalty if needed
        final_score = raw_score
        if item.get('blocked_by'):
            final_score = raw_score * (1.0 - factors.blocked_penalty)
        
        # Determine category
        category = self._score_to_category(final_score)
        
        # Generate rationale
        rationale = self._generate_rationale(item, factors, final_score, category)
        
        # Return result
        return PriorityResult(
            item_id=item['id'],
            priority_score=final_score,
            factors=factors,
            rationale=rationale,
            category=category,
            confidence=factors.confidence,
            calculated_at=datetime.now().isoformat()
        )
    
    
    def prioritize_backlog(
        self,
        items: List[Dict[str, Any]],
        context: Optional[Dict[str, Any]] = None
    ) -> List[PriorityResult]:
        """
        Prioritize all backlog items and return sorted list.
        
        Args:
            items: List of backlog item dicts
            context: Optional context for all items
        
        Returns:
            List of PriorityResults sorted by score (highest first)
        
        Example:
            results = prioritizer.prioritize_backlog([
                {'id': 'F-027', 'title': 'Personal Logs', ...},
                {'id': 'F-029', 'title': 'Continuous Discovery', ...}
            ])
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.item_id}: {result.priority_score:.2f}")
        """
        # Calculate priority for each item
        results = []
        for item in items:
            result = self.calculate_priority(item, context)
            results.append(result)
        
        # Sort by priority score (descending)
        results.sort(key=lambda r: r.priority_score, reverse=True)
        
        return results
    
    
    # ========================================================================
    # FACTOR CALCULATION (Internal)
    # ========================================================================
    
    def _calculate_factors(
        self,
        item: Dict[str, Any],
        context: Dict[str, Any]
    ) -> PriorityFactors:
        """Calculate all priority factors for an item."""
        # Customer value (0.0-1.0)
        customer_value = self._calculate_customer_value(item, context)
        
        # Unblock impact (0.0-1.0)
        unblock_impact = self._calculate_unblock_impact(item, context)
        
        # Worker availability (0.0-1.0)
        worker_availability = self._calculate_worker_availability(item, context)
        
        # Learning value (0.0-1.0)
        learning_value = self._calculate_learning_value(item, context)
        
        # Blocked penalty (0.5 if blocked)
        blocked_penalty = 0.5 if item.get('blocked_by') else 0.0
        
        # Confidence (average of factor confidences)
        confidence = 0.8  # Default (Phase 2: calculate from factor certainty)
        
        return PriorityFactors(
            customer_value=customer_value,
            unblock_impact=unblock_impact,
            worker_availability=worker_availability,
            learning_value=learning_value,
            blocked_penalty=blocked_penalty,
            confidence=confidence
        )
    
    
    def _calculate_customer_value(
        self,
        item: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """
        Calculate customer value factor (0.0-1.0).
        
        Sources:
        - Explicit customer_value_hint in item
        - Hypothesis confidence from research logs
        - User importance indicators
        - ROI calculations
        """
        # Check for explicit hint
        if 'customer_value_hint' in item:
            return float(item['customer_value_hint'])
        
        # Check for hypothesis confidence (from research logs)
        hypotheses = context.get('hypotheses', [])
        related_hypotheses = [h for h in hypotheses if h.get('related_to') == item['id']]
        if related_hypotheses:
            # Use highest confidence hypothesis
            confidences = [h.get('confidence', 0.5) for h in related_hypotheses]
            return max(confidences)
        
        # Check for ROI calculations
        if 'roi_percentage' in item:
            # Normalize ROI to 0.0-1.0 (assume 100% ROI = 1.0 value)
            roi = item['roi_percentage'] / 100.0
            return min(roi, 1.0)
        
        # Default: medium value
        return 0.5
    
    
    def _calculate_unblock_impact(
        self,
        item: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """
        Calculate unblock impact (0.0-1.0).
        
        Based on how many downstream items this unblocks.
        Formula: min(num_unblocked / 5, 1.0)  # Cap at 5 items
        """
        blocks = item.get('blocks', [])
        
        if not blocks:
            return 0.0
        
        # Normalize: 5+ items = max impact
        num_blocked = len(blocks)
        return min(num_blocked / 5.0, 1.0)
    
    
    def _calculate_worker_availability(
        self,
        item: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """
        Calculate worker availability (0.0-1.0).
        
        Based on:
        - Skill match with available workers
        - Worker capacity remaining
        """
        required_skills = set(item.get('required_skills', []))
        available_workers = context.get('available_workers', [])
        
        if not required_skills:
            # No specific skills needed → anyone can work on it
            return 1.0 if available_workers else 0.0
        
        if not available_workers:
            return 0.0
        
        # Find workers with matching skills
        matching_workers = []
        for worker in available_workers:
            worker_skills = set(worker.get('skills', []))
            if required_skills.issubset(worker_skills):
                matching_workers.append(worker)
        
        if not matching_workers:
            return 0.0
        
        # Calculate availability based on capacity
        total_capacity = sum(w.get('capacity_remaining', 0.0) for w in matching_workers)
        max_capacity = len(matching_workers) * 1.0  # Assume 1.0 = full capacity
        
        return min(total_capacity / max_capacity, 1.0) if max_capacity > 0 else 0.0
    
    
    def _calculate_learning_value(
        self,
        item: Dict[str, Any],
        context: Dict[str, Any]
    ) -> float:
        """
        Calculate learning value (0.0-1.0).
        
        Based on how much uncertainty this reduces.
        Higher value for:
        - Research tasks (investigate unknowns)
        - Experiments (test hypotheses)
        - Hard problems (new capabilities)
        """
        # Check for explicit hint
        if 'learning_value_hint' in item:
            return float(item['learning_value_hint'])
        
        # Check item type
        item_type = item.get('type', '').lower()
        if 'research' in item_type:
            return 0.8
        elif 'experiment' in item_type:
            return 0.7
        elif 'spike' in item_type:
            return 0.6
        
        # Check for "hard problem" indicators
        title = item.get('title', '').lower()
        description = item.get('description', '').lower()
        hard_indicators = ['hard problem', 'unknown', 'investigate', 'research', 
                          'uncertainty', 'experiment', 'explore']
        
        if any(indicator in title or indicator in description for indicator in hard_indicators):
            return 0.7
        
        # Default: moderate learning value
        return 0.5
    
    
    def _weighted_score(self, factors: PriorityFactors) -> float:
        """Calculate weighted priority score from factors."""
        score = (
            factors.customer_value * self.weights['customer_value'] +
            factors.unblock_impact * self.weights['unblock_impact'] +
            factors.worker_availability * self.weights['worker_availability'] +
            factors.learning_value * self.weights['learning_value']
        )
        return score
    
    
    def _score_to_category(self, score: float) -> str:
        """Convert score to category (CRITICAL, HIGH, MEDIUM, LOW)."""
        if score >= self.thresholds['CRITICAL']:
            return 'CRITICAL'
        elif score >= self.thresholds['HIGH']:
            return 'HIGH'
        elif score >= self.thresholds['MEDIUM']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    
    def _generate_rationale(
        self,
        item: Dict[str, Any],
        factors: PriorityFactors,
        score: float,
        category: str
    ) -> str:
        """Generate human-readable rationale for priority score."""
        lines = []
        
        # Category + score
        lines.append(f"{category} priority ({score:.2f}) because:")
        
        # Explain each significant factor
        if factors.customer_value >= 0.7:
            lines.append(f"  • Strong customer value ({factors.customer_value:.2f})")
        elif factors.customer_value <= 0.3:
            lines.append(f"  • Low customer value ({factors.customer_value:.2f})")
        
        if factors.unblock_impact >= 0.5:
            num_unblocked = int(factors.unblock_impact * 5)
            lines.append(f"  • Unblocks {num_unblocked}+ downstream items")
        elif factors.unblock_impact == 0:
            lines.append(f"  • Does not unblock other work")
        
        if factors.worker_availability >= 0.7:
            lines.append(f"  • Workers available with right skills ({factors.worker_availability:.2f})")
        elif factors.worker_availability <= 0.3:
            lines.append(f"  • Limited worker availability ({factors.worker_availability:.2f})")
        
        if factors.learning_value >= 0.6:
            lines.append(f"  • High learning value - reduces uncertainty ({factors.learning_value:.2f})")
        
        if factors.blocked_penalty > 0:
            lines.append(f"  • ⚠️ BLOCKED by other items (50% penalty applied)")
        
        return '\n'.join(lines)
    
    
    def _get_default_context(self) -> Dict[str, Any]:
        """Get default context when none provided."""
        return {
            'available_workers': [],
            'backlog_items': [],
            'hypotheses': []
        }


# ============================================================================
# CLI INTERFACE (for testing)
# ============================================================================

def main():
    """CLI interface for testing prioritization."""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(
        description="Neurosymbolic Backlog Prioritizer"
    )
    
    parser.add_argument("--items", required=True, help="JSON file with backlog items")
    parser.add_argument("--context", help="JSON file with context (workers, hypotheses)")
    parser.add_argument("--output", help="Output file for results")
    
    args = parser.parse_args()
    
    # Load items
    with open(args.items) as f:
        items = json.load(f)
    
    # Load context (optional)
    context = None
    if args.context:
        with open(args.context) as f:
            context = json.load(f)
    
    # Initialize prioritizer
    workspace_path = Path.cwd()
    prioritizer = NeurosymbolicPrioritizer(workspace_path)
    
    # Prioritize backlog
    print("🔄 Prioritizing backlog...")
    results = prioritizer.prioritize_backlog(items, context)
    
    # Display results
    print(f"\n📊 Prioritized Backlog ({len(results)} items):\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. [{result.category}] {result.item_id} ({result.priority_score:.2f})")
        print(f"   {result.rationale}")
        print()
    
    # Save results (optional)
    if args.output:
        output_data = [
            {
                'rank': i,
                'item_id': r.item_id,
                'priority_score': r.priority_score,
                'category': r.category,
                'rationale': r.rationale,
                'factors': {
                    'customer_value': r.factors.customer_value,
                    'unblock_impact': r.factors.unblock_impact,
                    'worker_availability': r.factors.worker_availability,
                    'learning_value': r.factors.learning_value
                }
            }
            for i, r in enumerate(results, 1)
        ]
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✅ Saved results to: {args.output}")


if __name__ == "__main__":
    main()
