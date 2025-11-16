---
id: pm-artifact-validation-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["santiago-pm"]
labels: ["type:feature", "priority:high", "component:standards", "nautical:theming"]
epic: nusy-v2-architecture
domain: product-management
owners: ["santiago-pm"]
stakeholders: ["santiago-architect", "santiago-ethicist"]
skill_level: master
knowledge_scope: sea
artifact_kinds: ["validation", "standard", "documentation"]
related_experiments: []
related_artifacts:
  - ../pm-artifact-templates-and-standards.feature
  - ../folder-structure.md
  - ../README.md
  - ../../templates/
---

Feature: Validate PM artifacts for metadata and nautical theming

  As Santiago-PM
  I want to validate PM artifacts created from templates
  So that they comply with KG metadata standards and nautical theming

  Background:
    Given the santiago-pm artifact templates and naming conventions are defined
    And the shared knowledge folder structure exists
    And KG integration metadata standards are established
    And artifact validation is a non-destructive check

  Scenario: Validate required metadata fields for a PM artifact
    Given a PM artifact file is created from a standard template
    When Santiago-PM validates the artifact metadata
    Then the artifact MUST include all required metadata fields:
      | field         |
      | id            |
      | type          |
      | status        |
      | created_at    |
      | updated_at    |
      | assignees     |
      | labels        |
      | epic          |
      | domain        |
      | owners        |
      | knowledge_scope |
      | skill_level   |
    And the metadata MUST be valid YAML frontmatter at the top of the file
    And the id MUST be globally unique within the PM artifact space

  Scenario: Validate naming and identifier conventions
    Given a PM artifact file exists in a nautical-themed subfolder
    When Santiago-PM validates naming conventions
    Then the human-facing title in the content MUST follow the format:
      """[Nautical Type] - [Descriptive Title]"""
    And the file name SHOULD avoid spaces and use kebab-case
    And the KG-compatible identifier MUST follow the pattern:
      """pm-artifact-<slug>-<YYYYMMDD>"""
    And chronological ordering MUST be supported by:
      | mechanism        |
      | created_at field |
      | ships-logs index |
      | folder structure |

  Scenario: Validate KG relations and theming
    Given a PM artifact has valid metadata and naming
    When Santiago-PM validates knowledge graph integration
    Then the artifact MUST declare its related artifacts where appropriate
    And KG relations MUST be derivable from:
      | source          |
      | related_artifacts list |
      | labels          |
      | epic            |
      | domain          |
    And nautical theming MUST be maintained in:
      | aspect          |
      | section titles  |
      | terminology     |
      | examples        |
    And any violations MUST be recorded in a validation report
      located under "ships-logs/pm-artifact-validation-report.md"

  Scenario: Validate root-level documentation standards
    Given the santiago-pm root contains folder-structure.md and README.md
    When Santiago-PM validates root documentation
    Then folder-structure.md MUST follow the folder organization template
    And README.md MUST follow the project documentation template
    And both MUST include KG metadata headers
    And both MUST be consistent with nautical theming conventions