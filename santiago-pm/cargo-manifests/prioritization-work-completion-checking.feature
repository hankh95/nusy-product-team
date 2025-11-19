# Cargo Manifest: Prioritization Tool Enhancement - Work Completion Checking

**Date**: 2025-11-17
**Type**: Feature
**Status**: proposed
**Priority**: medium
**Domain**: pm-workflow
**Triggered By**: Analysis of existing prioritization system capabilities

---

## Feature Overview

Enhance the **NeurosymbolicPrioritizer** to check for existing work completion status before suggesting new priorities. This prevents duplicate work and ensures the system considers what's already been accomplished.

**Key Innovation**: The prioritizer currently calculates optimal work order but doesn't verify if similar work has already been completed. This enhancement adds **work completion checking** to avoid redundant efforts and surface completed capabilities.

### Current State
- NeurosymbolicPrioritizer calculates priority scores based on customer value, unblock impact, worker availability, and learning value
- System uses KG queries for real-time state but doesn't check completion status
- Features in `features/` directory contain detailed specifications that may overlap with completed work

### Enhancement Scope
- Add completion status checking to prioritization algorithm
- Query KG for completed work that might duplicate proposed items
- Surface completion warnings in priority rationale
- Update priority scores for items that duplicate completed work

---

## User Stories

### Story 1: Check Work Completion Before Prioritization

```gherkin
Feature: Work Completion Status Checking
  As a product manager using Santiago's prioritization system
  I want the system to check if similar work has already been completed
  So that I don't prioritize duplicate or redundant work

  Scenario: Prioritizer detects completed work overlap
    Given a new backlog item is being prioritized
    And the item involves "multi-agent framework implementation"
    When Santiago checks the knowledge graph for completed work
    Then it should find completed items with similar titles or descriptions
    And reduce the priority score by 50% with completion warning
    And include completion rationale in priority explanation

  Scenario: Surface completed capabilities in rationale
    Given backlog prioritization is running
    When an item overlaps with completed work
    Then the priority rationale should include:
      """
      ⚠️ POTENTIAL DUPLICATE
      Similar work completed: "Multi-Agent Framework v1.0" (2025-10-15)
      Completion evidence: ships-logs/multi-agent-implementation.md
      Consider: Is this incremental improvement or duplicate effort?
      Priority reduced by 50% due to completion overlap.
      """
```

### Story 2: Query KG for Completion Evidence

```gherkin
Feature: Knowledge Graph Completion Queries
  As the prioritization system
  I want to query the knowledge graph for completion evidence
  So that I can identify when work has already been done

  Scenario: Query completed artifacts
    Given a backlog item with title "Personal Log Feature"
    When Santiago queries the KG for completion evidence
    Then it should check:
      | query_type | example_query |
      | artifact_status | status = "done" |
      | title_similarity | fuzzy match > 0.8 |
      | description_overlap | semantic similarity |
      | ships_logs | implementation evidence |

  Scenario: Calculate completion confidence
    Given multiple completion indicators exist
    When Santiago evaluates completion status
    Then confidence should be calculated as:
      """
      Completion Confidence = (artifact_status + title_match + description_match + evidence_strength) / 4

      Where:
      - artifact_status: 1.0 if status="done", 0.0 otherwise
      - title_match: fuzzy similarity score (0.0-1.0)
      - description_match: semantic similarity (0.0-1.0)
      - evidence_strength: 1.0 if ships-logs exist, 0.5 if mentioned, 0.0 if none
      """
```

### Story 3: Adjust Priority Based on Completion Status

```gherkin
Feature: Completion-Aware Priority Adjustment
  As the prioritization algorithm
  I want to adjust priority scores based on completion status
  So that completed work doesn't get reprioritized

  Scenario: Apply completion penalty
    Given an item has completion confidence > 0.7
    When calculating final priority score
    Then apply completion penalty:
      """
      completion_penalty = min(completion_confidence, 0.8)  # Max 80% reduction
      adjusted_score = raw_score * (1.0 - completion_penalty)
      """

  Scenario: Completion rationale in priority output
    Given priority calculation includes completion checking
    When generating rationale
    Then include completion status:
      """
      Priority Factors:
      - Customer value: 0.8
      - Unblock impact: 0.2
      - Worker availability: 0.9
      - Learning value: 0.6
      - Completion overlap: -0.7 (70% penalty)

      Final Score: 0.32 (was 0.75 before completion penalty)
      """
```

---

## Technical Implementation

### Code Changes Required

1. **Enhance NeurosymbolicPrioritizer** (`src/nusy_pm_core/adapters/neurosymbolic_prioritizer.py`):
   - Add `_calculate_completion_overlap()` method
   - Add completion_confidence to PriorityFactors dataclass
   - Update weighted score calculation to include completion penalty
   - Update rationale generation to include completion warnings

2. **KG Query Integration**:
   - Add completion status queries to KG store
   - Implement fuzzy matching for titles/descriptions
   - Add semantic similarity checking

3. **Completion Evidence Sources**:
   - Artifact status (done/completed)
   - Ships logs entries
   - Implementation documentation
   - Test coverage evidence

### Acceptance Criteria

- [ ] Prioritizer checks KG for completed work before calculating scores
- [ ] Completion confidence calculated from multiple evidence sources
- [ ] Priority scores reduced for items overlapping completed work
- [ ] Completion warnings included in priority rationale
- [ ] No performance regression in prioritization speed
- [ ] Integration tests verify completion checking logic

---

## Dependencies

- **NeurosymbolicPrioritizer**: Base prioritization system (exists)
- **Knowledge Graph**: For querying completion status (exists)
- **Ships Logs**: Evidence of completed work (exists)

## Effort Estimate

**Story Points**: 5
**Risk Level**: Low (enhancement to existing system)
**Dependencies**: None (all required systems exist)

---

## Success Metrics

- **Completion Detection Accuracy**: >90% of duplicate work identified
- **False Positive Rate**: <10% incorrect completion warnings
- **Priority Adjustment**: Completed work gets appropriately low priority
- **User Feedback**: PM finds completion warnings helpful for backlog refinement