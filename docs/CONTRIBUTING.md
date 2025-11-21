<!-- markdownlint-disable MD022 MD032 MD031 MD040 MD009 MD047 MD024 -->

# Contributing to Clinical Intelligence Starter

This document outlines the contribution process and provides detailed examples for the Clinical Intelligence Starter project.

**For comprehensive development practices, see [docs/architecture/arch-vision-merged-plan.md](docs/architecture/arch-vision-merged-plan.md) - the single source of truth for all development standards.**

## Quick Links

- **[docs/architecture/arch-vision-merged-plan.md](docs/architecture/arch-vision-merged-plan.md)**: Universal development practices (TDD/BDD, code quality, testing)
- **[.cursorrules](.cursorrules)**: AI agent work practices
- **[README.md](README.md)**: Project overview and quick start
- **[docs/architecture/arch-migration-plan.md](docs/architecture/arch-migration-plan.md)**: Project roadmap

## Documentation Canonicalization

To prevent duplicate drift and speed up reviews:

- Superseded docs: Keep only the latest version under the canonical filename. Use a "Version History" section inside the doc to summarize prior changes. Rely on Git history for previous versions rather than keeping `-v1`, `-v2` file copies.
- Canonical strategic doc (Santiago-PM): `self-improvement/santiago-pm/strategic-charts/Santiago-Trains-Manolin.md` (see index in `self-improvement/santiago-pm/strategic-charts/README.md`).
- When replacing a document: remove the old file, promote the new content to the canonical name, and add a brief note to the top indicating the effective version/date if helpful.

---

## Development Workflow

### TDD/BDD Development Process

All development work follows Test-Driven Development (TDD) and Behavior-Driven Development (BDD) practices to ensure quality and maintainability:

#### 1. Create a Ticket (Issue)
- **Start with a GitHub Issue**: All work begins with a well-defined issue that describes the problem or feature
- **Clear Acceptance Criteria**: Include specific, measurable acceptance criteria
- **Labels**: Use appropriate labels (`bug`, `enhancement`, `module:<name>`, etc.)
- **Link to Development Plans**: Reference relevant sections in development plans when applicable

#### 2. TDD/BDD Development Cycle
Follow the Red-Green-Refactor cycle for all development:

**Red Phase - Write Failing Tests First:**
- Write unit tests that define the expected behavior
- Write BDD scenarios that describe the feature from a user perspective
- Ensure tests fail before implementing the feature

**Green Phase - Make Tests Pass:**
- Implement the minimal code to make tests pass
- Focus on functionality over perfection
- Run tests frequently to ensure progress

**Refactor Phase - Improve Code Quality:**
- Refactor code while maintaining test coverage
- Improve readability, performance, and maintainability
- Ensure all tests still pass after refactoring

#### 3. Testing Requirements
- **Unit Tests**: All new code must have comprehensive unit test coverage
- **Integration Tests**: Test component interactions and external dependencies
- **BDD Scenarios**: Validate business logic and user workflows
- **Test Quality**: Tests should be readable, maintainable, and provide clear failure messages

#### 3a. Kanban & Work Ownership

- **Claim work via Kanban**: Before starting, claim a card from the relevant board (e.g. `exp-057-migration`) using the Kanban tools, so only one agent/human owns it at a time.
- **Stay within your card**: Treat the card’s linked artifact (cargo manifest, domain feature, expedition doc) as your source spec; avoid scope‑creeping into unrelated work.
- **Definition of Done (per card)**:
  - Tests/linters run and passing for the areas you touched.
  - Changes committed (and pushed when appropriate) with a message referencing the card/manifest.
  - Any relevant personal/ships logs updated.
  - Kanban card moved to `review`/`done` with a short summary comment.

### Practical TDD/BDD Workflow Examples

#### Example 1: Adding a New Source Format Processor (CatchFish)

**Red Phase - Write Failing Tests First:**
```python
# tests/test_docx_processor.py
import pytest
from pathlib import Path
from catchfish.l0_processor import DocxProcessor, SourceMetadata

def test_can_process_docx_files():
    processor = DocxProcessor()
    assert processor.can_process(Path('test.docx'))
    assert not processor.can_process(Path('test.pdf'))

def test_extract_content_from_docx():
    processor = DocxProcessor()
    # This will fail until we implement the functionality
    content, metadata = processor.extract_content(Path('test.docx'))
    assert 'extracted content' in content
    assert metadata.format_type == 'docx'
```

**Green Phase - Implement Minimal Code:**
```python
# catchfish/l0_processor.py
class DocxProcessor:
    """Process Microsoft Word documents into L0 representation."""

    def __init__(self):
        try:
            from docx import Document
            self.has_docx = True
        except ImportError:
            self.has_docx = False

    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == '.docx' and self.has_docx

    def extract_content(self, file_path: Path) -> Tuple[str, SourceMetadata]:
        if not self.can_process(file_path):
            raise ValueError(f"Cannot process {file_path}")

        # Minimal implementation to make tests pass
        doc = Document(file_path)
        content = '\n'.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip()])
        metadata = SourceMetadata(
            format_type='docx',
            extraction_method='python-docx',
            quality_score=0.9
        )
        return content, metadata
```

**Refactor Phase - Improve Code Quality:**
```python
# catchfish/l0_processor.py (refactored)
class DocxProcessor:
    """Process Microsoft Word documents into L0 representation."""

    def __init__(self):
        try:
            from docx import Document
            self.has_docx = True
        except ImportError:
            self.has_docx = False

    def can_process(self, file_path: Path) -> bool:
        return file_path.suffix.lower() == '.docx' and self.has_docx

    def extract_content(self, file_path: Path) -> Tuple[str, SourceMetadata]:
        """Extract text content from DOCX file with table support."""
        if not self.can_process(file_path):
            raise ValueError(f"Cannot process {file_path}")

        doc = Document(file_path)
        content_parts = []

        # Extract paragraphs
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                content_parts.append(paragraph.text)

        # Extract tables as structured content
        for table in doc.tables:
            table_content = self._extract_table(table)
            content_parts.append(table_content)

        content = '\n\n'.join(content_parts)
        metadata = SourceMetadata(
            format_type='docx',
            extraction_method='python-docx',
            quality_score=0.9
        )

        return content, metadata

    def _extract_table(self, table) -> str:
        """Extract table content as markdown."""
        rows = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append('| ' + ' | '.join(cells) + ' |')

        if rows:
            # Add header separator
            header_sep = '| ' + ' | '.join(['---'] * len(table.columns)) + ' |'
            rows.insert(1, header_sep)

        return '\n'.join(rows)
```

#### Example 2: Adding a New BDD Generation Mode

**Red Phase - Write Failing Tests First:**
```python
# tests/test_clinical_guidelines_mode.py
import pytest
from bdd_fishnet.scripts.generate_qa import _load_mode_prompts

def test_clinical_guidelines_mode_prompt_loading():
    """Test that clinical guidelines mode prompt is loaded."""
    prompts = _load_mode_prompts(["clinical-guidelines"])
    assert "clinical-guidelines" in prompts
    assert "recommend" in prompts["clinical-guidelines"].lower()

def test_clinical_guidelines_mode_data_collection():
    """Test that clinical guidelines content is collected."""
    # This test will fail until we implement the mode
    mode_data = collect_clinical_guidelines_data(mock_context)
    assert "guidelines_content" in mode_data
    assert len(mode_data["guidelines_content"]) > 0
```

**Green Phase - Implement Minimal Code:**
```python
# bdd_fishnet/scripts/generate_qa.py
def _get_inline_mode_prompt(mode: str) -> str:
    """Get inline prompt for modes without dedicated files."""
    prompts = {
        "clinical-guidelines": """
### Clinical Guidelines Mode
Focus on extracting scenarios directly from clinical guideline recommendations.
Look for explicit statements like "recommend", "should", "consider", "do not".
Generate scenarios that test adherence to guideline recommendations.

Guidelines to follow:
- Extract one scenario per major recommendation
- Include contraindications and exceptions
- Focus on decision points rather than general statements
        """,
    }
    return prompts.get(mode, f"### {mode.title()} Mode\nGenerate scenarios using {mode} approach.")

# In mode data collection section:
if "clinical-guidelines" in mode_list:
    # Minimal implementation to make tests pass
    mode_data["clinical-guidelines"] = {
        "guidelines_content": [],
        "extraction_patterns": ["recommend", "should", "consider", "do not"]
    }
```

**Refactor Phase - Improve Implementation:**
```python
# bdd_fishnet/scripts/generate_qa.py (refactored)
if "clinical-guidelines" in mode_list:
    # Extract guideline-specific content
    guidelines_content = []
    for entry in context.littlefish_sections:
        file_path = context.version_dir / entry.get("file")
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")
            # Look for guideline-like content patterns
            if any(keyword in content.lower() for keyword in
                   ["recommend", "should", "consider", "guideline", "consensus"]):
                guidelines_content.append({
                    "section": entry.get("section"),
                    "content": content[:1000],  # Limit content
                })

    if guidelines_content:
        mode_data["clinical-guidelines"] = {
            "guidelines_content": guidelines_content,
            "extraction_patterns": ["recommend", "should", "consider", "do not"]
        }
    else:
        mode_errors.append("clinical-guidelines: No guideline content found")
```

#### Example 3: BDD Scenario Development

**Red Phase - Write Failing BDD Scenario:**
```gherkin
# tests/features/clinical_decision_support.feature
Feature: Clinical Decision Support for Type 2 Diabetes

  @generated @top-down
  Scenario: Metformin initiation for newly diagnosed Type 2 diabetes
    Given a patient with newly diagnosed Type 2 diabetes
    And HbA1c > 6.5%
    And no contraindications to metformin
    When evaluating initial treatment options
    Then metformin should be recommended as first-line therapy
    And the recommendation should include dosage titration
    And lifestyle counseling should be included
```

**Green Phase - Implement Supporting Code:**
```python
# Step definitions in tests/steps/clinical_decision_steps.py
from pytest_bdd import given, when, then, parsers

@given("a patient with newly diagnosed Type 2 diabetes")
def patient_with_new_diagnosis():
    return {
        "diagnosis": "type_2_diabetes",
        "duration": "new",
        "hba1c": None,
        "contraindications": []
    }

@given(parsers.parse("HbA1c > {value}%"))
def hba1c_above_threshold(patient, value: float):
    patient["hba1c"] = float(value) + 0.1  # Ensure above threshold
    return patient

@given("no contraindications to metformin")
def no_metformin_contraindications(patient):
    patient["contraindications"] = []  # Ensure no contraindications
    return patient

@when("evaluating initial treatment options")
def evaluate_treatment_options(patient):
    # Call the actual decision logic
    from clinical_decision_support import evaluate_initial_treatment
    return evaluate_initial_treatment(patient)

@then("metformin should be recommended as first-line therapy")
def metformin_recommended(result):
    assert "metformin" in result["recommendations"]
    assert result["recommendations"]["metformin"]["priority"] == "first_line"

@then("the recommendation should include dosage titration")
def dosage_titration_included(result):
    metformin_rec = result["recommendations"]["metformin"]
    assert "dosage_titration" in metformin_rec
    assert metformin_rec["dosage_titration"] is True

@then("lifestyle counseling should be included")
def lifestyle_counseling_included(result):
    assert "lifestyle_counseling" in result["recommendations"]
```

**Refactor Phase - Improve Step Definitions:**
```python
# tests/steps/clinical_decision_steps.py (refactored)
from pytest_bdd import given, when, then, parsers
from typing import Dict, Any

@given("a patient with newly diagnosed Type 2 diabetes", target_fixture="patient")
def patient_with_new_diagnosis() -> Dict[str, Any]:
    """Create a patient fixture for newly diagnosed Type 2 diabetes."""
    return {
        "diagnosis": "type_2_diabetes",
        "duration": "new",
        "hba1c": None,
        "contraindications": [],
        "comorbidities": [],
        "medications": []
    }

@given(parsers.parse("HbA1c > {value:g}%"), target_fixture="patient")
def hba1c_above_threshold(patient: Dict[str, Any], value: float) -> Dict[str, Any]:
    """Set HbA1c above specified threshold."""
    patient["hba1c"] = value + 0.1  # Ensure above threshold
    return patient

@given("no contraindications to metformin", target_fixture="patient")
def no_metformin_contraindications(patient: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure patient has no metformin contraindications."""
    # Check for common contraindications
    contraindications = ["renal_failure", "lactic_acidosis_history", "contrast_imaging"]
    patient["contraindications"] = [c for c in patient.get("contraindications", []) if c not in contraindications]
    return patient

@when("evaluating initial treatment options", target_fixture="evaluation_result")
def evaluate_treatment_options(patient: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate treatment options for the patient."""
    from clinical_decision_support.treatment_recommendations import evaluate_initial_treatment
    return evaluate_initial_treatment(patient)

@then("metformin should be recommended as first-line therapy")
def metformin_recommended(evaluation_result: Dict[str, Any]):
    """Verify metformin is recommended as first-line therapy."""
    recommendations = evaluation_result.get("recommendations", [])
    metformin_rec = next((r for r in recommendations if r["medication"] == "metformin"), None)
    assert metformin_rec is not None, "Metformin should be recommended"
    assert metformin_rec["priority"] == "first_line", "Metformin should be first-line"

@then("the recommendation should include dosage titration")
def dosage_titration_included(evaluation_result: Dict[str, Any]):
    """Verify dosage titration guidance is included."""
    metformin_rec = _get_metformin_recommendation(evaluation_result)
    assert metformin_rec.get("dosage_titration") is True, "Dosage titration should be included"

@then("lifestyle counseling should be included")
def lifestyle_counseling_included(evaluation_result: Dict[str, Any]):
    """Verify lifestyle counseling is included."""
    recommendations = evaluation_result.get("recommendations", [])
    lifestyle_rec = next((r for r in recommendations if r["type"] == "lifestyle_counseling"), None)
    assert lifestyle_rec is not None, "Lifestyle counseling should be recommended"

def _get_metformin_recommendation(evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to get metformin recommendation from evaluation result."""
    recommendations = evaluation_result.get("recommendations", [])
    metformin_rec = next((r for r in recommendations if r["medication"] == "metformin"), None)
    assert metformin_rec is not None, "Metformin recommendation not found"
    return metformin_rec
```

#### 4. Code Quality Checks
Before creating a PR, ensure:
- All tests pass locally
- Code follows project style guidelines
- Documentation is updated for any interface changes
- No linting errors or warnings
- CI/CD pipeline passes (if applicable)

#### 5. Save Session Context (F-027 Integration)

**For AI Agents**: After completing a chunk of work, save your session for context restoration:

```bash
# Quick save (raw transcript only)
python save-chat-log.py --paste --topic "feature-name"

# Full save with summary (RECOMMENDED)
python save-chat-log.py --paste --with-summary --topic "feature-name"
```

**Benefits**:
- **Context Restoration**: Next agent can restore context in <2 seconds
- **Full Provenance**: Raw transcript + summary log linked via metadata
- **Discovery**: F-029 scanner finds features/issues mentioned in logs
- **Learning**: Track patterns and decisions over time

**When to save**:
- ✅ After completing a feature or major task
- ✅ Before switching to different work
- ✅ When creating a PR (include in PR description)
- ✅ End of day/session

**Session log contents**:
- Raw transcript: Full conversation (verbatim)
- Summary log: Extracted metadata (files, features, decisions, artifacts)
- Both linked for full provenance chain

#### 6. Pull Request Process
- **PR Template**: Use the appropriate PR template (`default.md` or `sub-project.md`)
- **Clear Description**: Explain what was implemented and why
- **Reference Issues**: Link to related issues using keywords (`Closes #123`, `Fixes #123`)
- **Session Context**: Include link to personal log if available
- **Testing Evidence**: Include test results or screenshots demonstrating the feature works
- **Review Request**: Request review from relevant team members

**Formal Workflow Integration (F-030)**:
When using GitHub-based workflow, session saving becomes part of PR readiness:

```bash
# 1. Complete work and tests
pytest tests/

# 2. Save session context
python save-chat-log.py --paste --with-summary --topic "feature-name"

# 3. Create PR (include session log link)
gh pr create --title "feat: Feature name" --body "Closes #123

Session log: santiago-pm/personal-logs/agents/2025-11-17-copilot-claude-feature-name.md
..."

# 4. Mark PR as ready for review
# (session log provides context for reviewer)
```

**Future**: F-030 Phase 1 will automate this workflow with native MCP tools.

#### 7. Issue Closure
- **Automatic Closure**: Issues are automatically closed when PRs are merged using keywords in PR descriptions
- **Manual Verification**: Ensure the implemented solution meets all acceptance criteria
- **Documentation Updates**: Update any relevant documentation or development plans

### Development Workflow Summary

```
📝 Create Issue → 🔴 Write Tests → 🟢 Implement Code → 🔵 Refactor → ✅ Test → 💾 Save Session → 📤 Create PR → 🔒 Issue Closed
```

#### Visual Workflow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  1. Create      │    │  2. TDD Cycle   │    │  3. Quality     │
│     Issue       │    │                 │    │     Checks      │
│                 │    │  🔴 Red:        │    │                 │
│ • Description   │    │    Failing      │    │ • Tests pass    │
│ • Acceptance    │    │    Tests        │    │ • Code style    │
│   Criteria      │    │                 │    │ • Linting       │
│ • Labels        │    │  🟢 Green:      │    │ • Documentation │
└─────────────────┘    │    Implement    │    └─────────────────┘
                       │                 │              │
                       │  🔵 Refactor:   │              ▼
                       │    Improve      │    ┌─────────────────┐
                       │    Code         │    │  4. Save        │
                       └─────────────────┘    │     Session     │
                                │              │                 │
                                ▼              │ • Raw log       │
                       ┌─────────────────┐    │ • Summary       │
                       │  5. Create PR   │◄───│ • Metadata      │
                       │                 │    └─────────────────┘
                       │ • Use template  │
                       │ • Reference     │
                       │   issues        │
                       │ • Link session  │
                       │ • Request       │    ┌─────────────────┐
                       │   review        │    │  6. Merge &     │
                       │                 │    │     Close       │
                       │ • Use template  │    │                 │
                       │ • Reference     │    │ • Auto-close    │
                       │   issues        │    │   via keywords  │
                       │ • Request       │    │ • Update plans  │
                       │   review        │    │ • Documentation │
                       └─────────────────┘    └─────────────────┘
```

### Testing Standards

#### Unit Testing
- Test public interfaces and complex logic
- Use descriptive test names that explain the behavior being tested
- Follow the `test_function_name` or `TestClass::test_method_name` conventions
- Mock external dependencies to isolate unit behavior

#### BDD Testing
- Focus on business value and user workflows
- Use Gherkin syntax for scenario definitions
- Test end-to-end workflows, not just individual functions
- Validate both positive and negative scenarios

#### Test Organization
- Place tests alongside code in `tests/` directories
- Use clear naming conventions for test files and functions
- Group related tests in classes or modules
- Include setup/teardown methods for complex test scenarios

### Quality Gates

**Pre-Commit Checks:**
- ✅ All unit tests pass
- ✅ BDD scenarios pass
- ✅ Code style checks pass
- ✅ No linting errors
- ✅ Documentation updated

**Pre-Merge Requirements:**
- ✅ Peer review completed
- ✅ CI/CD pipeline passes
- ✅ Acceptance criteria met
- ✅ No breaking changes without migration plan

### Closing Issues

GitHub provides several ways to automatically close issues when PRs are merged:

#### Method 1: Keywords in PR Description (Recommended)
Include one of these keywords followed by the issue number in your PR description:
- `Closes #123` - Closes the issue when PR is merged
- `Fixes #123` - Indicates the PR fixes the issue
- `Resolves #123` - Indicates the PR resolves the issue

#### Method 2: Keywords in Commit Messages
Include keywords in commit messages (less preferred for visibility):
- `Closes #123`
- `Fixes #123`
- `Resolves #123`

#### Method 3: Manual Closure
After merging, manually close the issue and reference the PR.

**Best Practice**: Always use keywords in PR descriptions to automatically close issues upon merge and maintain clear traceability.

#### Issue Closure Checklist
Before closing an issue, ensure:
- ✅ All acceptance criteria are met
- ✅ Tests are passing and comprehensive
- ✅ Documentation is updated
- ✅ No regressions introduced
- ✅ Related development plans are updated (if applicable)

### Code Quality

- Follow the existing code style and conventions
- Add/update tests for new features and bug fixes
- Update documentation for any interface changes
- Ensure CI/CD pipelines pass

### Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers in commits when applicable
- Keep commits focused on single changes

### Testing

- Run unit tests locally before pushing
- Ensure integration tests pass
- Test across affected sub-projects for separated architecture changes

## Architecture Guidelines

See [`docs/architecture/arch-vision-merged-plan.md`](docs/architecture/arch-vision-merged-plan.md) for detailed architecture documentation.

### Sub-project Boundaries

- Maintain clear separation between CatchFish, BDD FishNet, Navigator, and AI Knowledge Review
- Use shared configuration through established patterns
- Avoid unintended coupling between sub-projects

## Development Plan Synchronization

The project maintains both GitHub Issues and development plan markdown files. Follow this process to keep them synchronized:

### Creating Issues from Plans

**When to create an issue**:
- Major phase transitions in development plans
- Cross-module dependencies that need coordination
- Blockers or risks identified in plans

**How to create**:
1. Create issue with descriptive title matching plan item
2. Add appropriate labels (including `module:<name>` if module-specific)
3. Reference the development plan section in issue description
4. Add to project board if applicable

### Updating Plans from Issues

**When an issue is closed**:
1. Update relevant development plan (module or master)
2. Mark completed items with `[x]` in plan checklists
3. Update "Current Phase" indicators if phase completes
4. Add notes about any significant findings or decisions

**When an issue is created**:
1. If it represents new scope, add to relevant development plan
2. If it's a bug or unplanned work, note in plan's "Next Steps" or risk section

### Development Plan Structure

All module development plans follow this standard structure:

1. **Overview**: Module purpose and mission
2. **Current Status**: Current phase with progress indicators
3. **Development Phases**: Roadmap with checkboxes
4. **Key Components**: Major deliverables and systems
5. **Success Criteria**: Measurable outcomes
6. **Integration Points**: Dependencies on other modules
7. **Next Steps**: Actionable items with checkboxes
8. **GitHub Issue Integration**: Process for linking to issues

### Master Development Plan

The master plan at [`docs/architecture/arch-migration-plan.md`](docs/architecture/arch-migration-plan.md) coordinates across all modules:
- Provides unified view of all module phases
- Documents cross-module dependencies
- Tracks system-level priorities and milestones
- References individual module plans for details

### Regular Sync Schedule

- **Weekly**: Review open issues against plan progress
- **Monthly**: Update plans with completed phases and milestones
- **Quarterly**: Review and adjust priorities in master plan

### Module Labels

Use these labels for module-specific issues:
- `module:catchfish` - CatchFish content generation
- `module:fishnet` - BDD FishNet QA validation
- `module:navigator` - Navigator orchestration
- `module:ai-review` - AI Knowledge Review evaluation

## Quick Reference

### Development Workflow
1. **Create Issue** → Define problem/feature with acceptance criteria
2. **TDD Cycle** → Red (failing tests) → Green (implementation) → Refactor
3. **Quality Checks** → Tests pass, code style, documentation updated
4. **Create PR** → Use template, reference issues, request review
5. **Merge & Close** → Automatic issue closure via keywords

### Testing Standards
- **Unit Tests**: Public interfaces, complex logic, external dependency mocking
- **BDD Tests**: Business workflows, end-to-end scenarios, Gherkin syntax
- **Test Organization**: `tests/` directory, clear naming, grouped by functionality

### Issue Management
- **Labels**: `bug`, `enhancement`, `module:<name>`, `good first issue`
- **Branching**: `feature/`, `bugfix/`, `hotfix/` from `main`
- **Closing**: Use `Closes #123` in PR descriptions for automatic closure

### Quality Gates
- ✅ Tests pass locally
- ✅ CI/CD pipeline passes
- ✅ Peer review completed
- ✅ Acceptance criteria met
- ✅ Documentation updated