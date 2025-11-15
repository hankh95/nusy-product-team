Feature: PM Artifact Templates and Standards

  As a Santiago crew member
  I want standardized templates for all PM artifacts
  So that creation and maintenance follows nautical theming

  Background:
    Given the nusy_pm folder structure exists
    And nautical naming conventions are defined

  Scenario: Create templates for each artifact type
    Given nautical naming is established
    When templates are requested
    Then create template files in each subfolder:
      | Subfolder          | Template File              | Content Type       |
      | cargo-manifests    | cargo-manifest-template.md | Feature spec       |
      | ships-logs         | ships-log-template.md      | Issue report       |
      | voyage-trials      | voyage-trial-template.md   | Experiment plan    |
      | navigation-charts  | navigation-chart-template.md | Development plan |
      | captains-journals  | captains-journal-template.md | Note entry      |
    And include KG integration metadata in templates

  Scenario: Define naming conventions
    Given artifacts need consistent naming
    When naming standards are applied
    Then use format: "[Nautical Type] - [Descriptive Title]"
    And include creation date and author
    And ensure KG-compatible identifiers

  Scenario: Validate template usage
    Given a new artifact is created from template
    When validation runs
    Then check required fields are filled
    And KG relations are established
    And nautical theming is maintained