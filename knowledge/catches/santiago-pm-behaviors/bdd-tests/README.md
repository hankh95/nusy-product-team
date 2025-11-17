# Santiago PM Behaviors - BDD Test Suite

This directory contains 84 BDD .feature files for testing 28 PM behaviors.

## Test Coverage

- **Total Behaviors**: 28
- **Total Feature Files**: 28
- **Total Scenarios**: 84
- **Scenarios per Behavior**: 3 (happy path, edge case, error handling)

## Behavior Categories

### Experiment Management

- `design_experiment.feature`
- `record_experiment_results.feature`
- `analyze_experiment_outcomes.feature`

### Feature Management

- `create_feature.feature`
- `prioritize_backlog.feature`
- `define_acceptance_criteria.feature`
- `track_velocity.feature`
- `update_backlog.feature`

### Issue Tracking

- `log_issue.feature`
- `link_issue_to_feature.feature`

### Knowledge Capture

- `create_note.feature`
- `link_related_notes.feature`
- `query_note_network.feature`

### Passage Orchestration

- `define_passage.feature`
- `validate_passage.feature`
- `generate_passage_diagram.feature`
- `execute_passage.feature`
- `monitor_passage_execution.feature`
- `coordinate_mcp_invocation.feature`
- `analyze_passage_performance.feature`
- `manage_passage_lifecycle.feature`

### Quality Assurance

- `run_quality_gate.feature`
- `generate_quality_report.feature`

### Status Management

- `status_query.feature`
- `status_transition.feature`
- `status_dashboard.feature`

### Strategic Planning

- `define_vision.feature`
- `create_roadmap.feature`

## Running Tests

```bash
# Dry run to validate Gherkin syntax
behave --dry-run knowledge/catches/santiago-pm-behaviors/bdd-tests/

# Run specific category
behave --tags=@feature_management knowledge/catches/santiago-pm-behaviors/bdd-tests/

# Run by capability level
behave --tags=@capability_journeyman knowledge/catches/santiago-pm-behaviors/bdd-tests/
```

## Generated

This test suite was automatically generated from:
- `knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md` (20 behaviors)
- `knowledge/catches/santiago-pm-behaviors/passage-behaviors-extracted.md` (8 behaviors)
