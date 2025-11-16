---
id: pm-artifact-frontmatter-generation-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["santiago-pm"]
labels: ["type:feature", "priority:medium", "component:standards", "nautical:theming"]
epic: nusy-v2-architecture
domain: product-management
owners: ["santiago-pm"]
stakeholders: ["santiago-architect", "santiago-ethicist"]
skill_level: master
knowledge_scope: sea
artifact_kinds: ["template", "frontmatter", "automation"]
related_experiments: []
related_artifacts:
  - ./pm-artifact-templates-and-standards.feature
  - ./pm-artifact-validation.feature
---

Feature: Auto-generate PM artifact frontmatter from a short description

  As a Santiago crew member
  I want Santiago-PM to generate complete KG-compatible frontmatter from a short description
  So that creating new PM artifacts is fast, consistent, and nautical

  Background:
    Given PM artifact metadata standards are defined
    And naming conventions and identifier patterns are established
    And Santiago-PM can access existing epics, labels, and domains

  Scenario Outline: Generate frontmatter for a new PM artifact from a brief description
    Given a crew member provides a brief natural language description:
      """
      <Description>
      """
    And specifies the target nautical artifact type "<Nautical Type>"
    And specifies the epic "<Epic>"
    When frontmatter generation is requested from Santiago-PM
    Then Santiago-PM MUST propose a complete frontmatter block including:
      | field           |
      | id              |
      | type            |
      | status          |
      | created_at      |
      | updated_at      |
      | assignees       |
      | labels          |
      | epic            |
      | domain          |
      | owners          |
      | knowledge_scope |
      | skill_level     |
      | artifact_kinds  |
      | related_artifacts |
    And the id MUST follow the pattern:
      """pm-artifact-<slug>-<YYYYMMDD>"""
    And labels MUST include at least:
      | label             |
      | type:feature      |
      | component:standards |
    And knowledge_scope and skill_level MUST be inferred from:
      | signal               |
      | artifact purpose     |
      | target Nautical Type |
      | epic                 |
    And the generated frontmatter MUST be suitable for direct insertion
      at the top of a new artifact file

    Examples:
      | Description                                         | Nautical Type        | Epic                    |
      | "Define templates for QA quality assessments"       | Quality Assessment   | nusy-v2-architecture    |
      | "Document DGX/Manolin platform rollout strategy"    | Strategic Chart      | nusy-v2-platform        |
      | "Capture daily learnings from NuSy PM experiments"  | Captain's Journal    | nusy-v2-architecture    |

  Scenario: Store frontmatter suggestions in a reusable location
    Given Santiago-PM has generated frontmatter candidates
    When a crew member requests a list of suggested artifacts
    Then Santiago-PM MUST maintain a catalog in:
      """ships-logs/frontmatter-suggestions.md"""
    And each entry MUST include:
      | field           |
      | id              |
      | title           |
      | description     |
      | suggested_path  |
      | epic            |
      | status          |
    And the catalog MUST support filtering by:
      | filter          |
      | epic            |
      | type            |
      | status          |
      | domain          |