# Quality Assessment: [ASSESSMENT TITLE]

**Assessment ID:** [ASSESSMENT-ID]  
**Assessment Date:** [DATE]  
**Assessment Period:** [START-DATE] to [END-DATE]  
**Quality Officer:** [ASSESSOR]  
**Scope:** [SYSTEM/COMPONENT/FEATURE]  
**Status:** [PLANNED|IN-PROGRESS|COMPLETED|ACTION-REQUIRED]  

## Executive Summary

[High-level summary of quality status and key findings]

## Assessment Scope

### In Scope

- [Component/System 1]
- [Component/System 2]
- [Component/System 3]

### Out of Scope

- [Excluded component 1]
- [Excluded component 2]

## Quality Metrics

### Test Coverage

| Component | Unit Tests | Integration Tests | E2E Tests | Total Coverage |
|-----------|------------|-------------------|-----------|----------------|
| [Component 1] | [XX%] | [XX%] | [XX%] | [XX%] |
| [Component 2] | [XX%] | [XX%] | [XX%] | [XX%] |

### Code Quality

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Cyclomatic Complexity | < 10 | [X.X] | [PASS/FAIL] |
| Code Duplication | < 5% | [X.X%] | [PASS/FAIL] |
| Maintainability Index | > 70 | [XX] | [PASS/FAIL] |

### Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Response Time (95th percentile) | < 500ms | [XXXms] | [PASS/FAIL] |
| Error Rate | < 0.1% | [X.X%] | [PASS/FAIL] |
| Throughput | > 1000 req/s | [XXXX] | [PASS/FAIL] |

## Test Results

### Automated Tests

- **Total Tests:** [XXXX]
- **Passed:** [XXXX] ([XX%])
- **Failed:** [XX] ([X%])
- **Skipped:** [XX] ([X%])

### Manual Testing

- **Test Cases Executed:** [XX]
- **Passed:** [XX] ([XX%])
- **Failed:** [X] ([X%])
- **Blocked:** [X] ([X%])

## Issues Identified

### Critical Issues

1. **[ISSUE-001]** - [Description]
   - **Severity:** Critical
   - **Impact:** [Description]
   - **Recommendation:** [Action required]

2. **[ISSUE-002]** - [Description]
   - **Severity:** Critical
   - **Impact:** [Description]
   - **Recommendation:** [Action required]

### Major Issues

1. **[ISSUE-003]** - [Description]
   - **Severity:** Major
   - **Impact:** [Description]
   - **Recommendation:** [Action required]

### Minor Issues

1. **[ISSUE-004]** - [Description]
   - **Severity:** Minor
   - **Impact:** [Description]
   - **Recommendation:** [Action required]

## Security Assessment

### Vulnerabilities Found

- **High Risk:** [X] vulnerabilities
- **Medium Risk:** [X] vulnerabilities
- **Low Risk:** [X] vulnerabilities

### Compliance Status

- **Security Standards:** [COMPLIANT/NON-COMPLIANT]
- **Data Privacy:** [COMPLIANT/NON-COMPLIANT]
- **Access Control:** [COMPLIANT/NON-COMPLIANT]

## Recommendations

### Immediate Actions (Priority 1)

1. [Action 1] - [Owner] - [Due date]
2. [Action 2] - [Owner] - [Due date]

### Short-term Improvements (Priority 2)

1. [Action 1] - [Owner] - [Timeline]
2. [Action 2] - [Owner] - [Timeline]

### Long-term Enhancements (Priority 3)

1. [Action 1] - [Owner] - [Timeline]
2. [Action 2] - [Owner] - [Timeline]

## Quality Trends

[Analysis of quality metrics over time and improvement trends]

## Related Artifacts

- [LINK TO TEST PLANS]
- [LINK TO ISSUE REPORTS]
- [LINK TO KG QUALITY ENTRIES]

## Metadata

```yaml
id: [ASSESSMENT-ID]
type: quality-assessment
status: [STATUS]
created_at: [CREATION-DATE]
updated_at: [UPDATE-DATE]
assignees: ["santiago-qa"]
labels: ["type:assessment", "scope:[SCOPE]", "period:[PERIOD]"]
epic: quality-governance
related_experiments: []
related_artifacts: []
```