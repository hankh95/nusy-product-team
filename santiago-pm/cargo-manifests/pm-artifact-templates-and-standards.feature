---
id: pm-artifact-templates-and-standards-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["santiago-pm", "santiago-architect"]
labels: ["type:feature", "priority:high", "component:standards", "nautical:theming"]
epic: nusy-v2-architecture
related_experiments: []
related_artifacts:
  - ../folder-structure.md
  - ../README.md
  - ../../templates/
  - ../../nusy_pm_core/
---

Feature: PM Artifact Templates and Standards

  As a Santiago crew member
  I want standardized templates for all PM artifacts
  So that creation and maintenance follows nautical theming

  Background:
    Given the santiago-pm folder structure exists
    And nautical naming conventions are defined
    And KG integration metadata standards are established

  Scenario: Create templates for each artifact type
    Given nautical naming is established
    When templates are requested
    Then create template files in each subfolder:
      | Subfolder          | Template File              | Content Type              | Nautical Theme     |
      | cargo-manifests    | cargo-manifest-template.md | Feature specification     | Cargo Manifest     |
      | ships-logs         | ships-log-template.md      | Issue report              | Ship's Log         |
      | voyage-trials      | voyage-trial-template.md   | Experiment plan           | Voyage Trial       |
      | navigation-charts  | navigation-chart-template.md | Development plan        | Navigation Chart   |
      | captains-journals  | captains-journal-template.md | Note entry             | Captain's Journal  |
      | crew-manifests     | crew-manifest-template.md  | Agent role specification  | Crew Manifest      |
      | strategic-charts   | strategic-chart-template.md | Architecture blueprint  | Strategic Chart    |
      | quality-assessments| quality-assessment-template.md | QA report            | Quality Assessment |
      | research-logs      | research-log-template.md   | Research findings        | Research Log       |
    And include KG integration metadata in templates
    And ensure templates follow nautical theming conventions

  Scenario: Define naming conventions
    Given artifacts need consistent naming
    When naming standards are applied
    Then use format: "[Nautical Type] - [Descriptive Title]"
    And include creation date and author
    And ensure KG-compatible identifiers
    And maintain chronological ordering in folder structures

  Scenario: Validate template usage
    Given a new artifact is created from template
    When validation runs
    Then check required fields are filled
    And KG relations are established
    And nautical theming is maintained
    And metadata standards are followed

  Scenario: Establish root level documentation standards
    Given the santiago-pm root contains documentation files
    When documentation standards are applied
    Then folder-structure.md follows folder organization template
    And README.md follows project documentation template
    And both include KG metadata headers
    And maintain consistency with nautical theming