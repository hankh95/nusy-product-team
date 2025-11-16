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
domain: product-management
owners: ["santiago-pm"]
stakeholders: ["santiago-architect", "santiago-ethicist"]
skill_level: master
knowledge_scope: sea
artifact_kinds: ["template", "standard", "documentation"]
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
  So that creation and maintenance follows nautical theming and KG standards

  Background:
    Given the santiago-core folder structure exists
    And nautical naming conventions are defined
    And KG integration metadata standards are established
    And the shared knowledge folder structure is agreed

  # 1. TEMPLATE CREATION

  Scenario Outline: Create template for a PM artifact type
    Given nautical naming is established
    And the "<Subfolder>" subfolder exists or is created under the PM area
    When a template is requested for "<Content Type>"
    Then Santiago-PM MUST create "<Template File>" in "<Subfolder>"
    And the template MUST include KG integration metadata placeholders
    And the template MUST include sections appropriate for "<Content Type>"
    And the template MUST follow the "<Nautical Theme>" conventions in:
      | aspect          |
      | title           |
      | headings        |
      | examples        |

    Examples:
      | Subfolder           | Template File                 | Content Type             | Nautical Theme       |
      | cargo-manifests     | cargo-manifest-template.md    | Feature specification    | Cargo Manifest       |
      | ships-logs          | ships-log-template.md         | Issue report             | Ship's Log           |
      | voyage-trials       | voyage-trial-template.md      | Experiment plan          | Voyage Trial         |
      | navigation-charts   | navigation-chart-template.md  | Development plan         | Navigation Chart     |
      | captains-journals   | captains-journal-template.md  | Note entry               | Captain's Journal    |
      | crew-manifests      | crew-manifest-template.md     | Agent role specification | Crew Manifest        |
      | strategic-charts    | strategic-chart-template.md   | Architecture blueprint   | Strategic Chart      |
      | quality-assessments | quality-assessment-template.md| QA report                | Quality Assessment   |
      | research-logs       | research-log-template.md      | Research findings        | Research Log         |

  # 2. NAMING & IDENTIFIER CONVENTIONS

  Scenario: Define naming conventions for PM artifacts
    Given PM artifacts need consistent naming and identifiers
    When naming standards are applied
    Then the human-facing title inside the artifact MUST follow the format:
      """[Nautical Type] - [Descriptive Title]"""
    And the file name SHOULD use kebab-case and avoid spaces
    And the KG-compatible identifier MUST follow the pattern:
      """pm-artifact-<slug>-<YYYYMMDD>"""
    And chronological ordering MUST be supported through:
      | mechanism             |
      | created_at field      |
      | ships-logs indexing   |
      | folder structure      |
    And the template documentation MUST explain these conventions with examples

  # 3. VALIDATION OF TEMPLATE-DERIVED ARTIFACTS

  Scenario: Validate required metadata fields for a PM artifact
    Given a PM artifact file is created from a standard template
    When Santiago-PM validates the artifact metadata
    Then the artifact MUST include all required metadata fields:
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
    And the metadata MUST be valid YAML frontmatter at the top of the file
    And the id MUST be globally unique within the PM artifact space
    And the id MUST conform to the pattern:
      """pm-artifact-<slug>-<YYYYMMDD>"""

  Scenario: Validate KG relations and nautical theming
    Given a PM artifact has valid metadata and naming
    When Santiago-PM validates knowledge graph integration
    Then the artifact MUST declare its related artifacts where appropriate
    And KG relations MUST be inferable from:
      | source                |
      | related_artifacts list|
      | labels                |
      | epic                  |
      | domain                |
    And nautical theming MUST be maintained in:
      | aspect          |
      | section titles  |
      | terminology     |
      | narrative style |
    And any violations MUST be recorded in a validation report
      located under "ships-logs/pm-artifact-validation-report.md"

  # 4. AUTO-GENERATING FRONTMATTER FROM A SHORT DESCRIPTION

  Scenario Outline: Auto-generate frontmatter for a new PM artifact
    Given a crew member provides a brief natural language description:
      """
      <Description>
      """
    And specifies the target nautical artifact type "<Nautical Type>"
    And specifies the epic "<Epic>"
    When frontmatter generation is requested from Santiago-PM
    Then Santiago-PM MUST propose a complete frontmatter block including:
      | field             |
      | id                |
      | type              |
      | status            |
      | created_at        |
      | updated_at        |
      | assignees         |
      | labels            |
      | epic              |
      | domain            |
      | owners            |
      | knowledge_scope   |
      | skill_level       |
      | artifact_kinds    |
      | related_artifacts |
    And the id MUST follow the pattern:
      """pm-artifact-<slug>-<YYYYMMDD>"""
    And labels MUST include at least:
      | label              |
      | type:feature       |
      | component:standards|
    And knowledge_scope and skill_level MUST be inferred from:
      | signal               |
      | artifact purpose     |
      | target Nautical Type |
      | epic                 |
    And the generated frontmatter MUST be suitable for direct insertion
      at the top of a new artifact file

    Examples:
      | Description                                         | Nautical Type        | Epic                 |
      | "Define templates for QA quality assessments"       | Quality Assessment   | nusy-v2-architecture |
      | "Document DGX/Manolin platform rollout strategy"    | Strategic Chart      | nusy-v2-platform     |
      | "Capture daily learnings from NuSy PM experiments"  | Captain's Journal    | nusy-v2-architecture |

  Scenario: Catalog generated frontmatter suggestions
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

  # 5. LINTING EXISTING ARTIFACTS AGAINST STANDARDS

  Scenario: Run a non-destructive lint pass over PM artifacts
    Given existing PM artifacts are stored under the santiago-pm folders
    And linting MUST NOT modify artifacts
    When a PM artifact lint run is triggered
    Then Santiago-PM MUST scan artifacts in:
      | path                    |
      | ./                      |
      | ../                     |
      | ../../templates/        |
      | ../../knowledge/shared/ |
    And Santiago-PM MUST identify violations in at least these categories:
      | rule_category              |
      | missing_metadata_fields    |
      | invalid_metadata_format    |
      | invalid_naming_convention  |
      | missing_nautical_theming   |
      | inconsistent_labels        |
      | missing_related_artifacts  |
    And Santiago-PM MUST produce a lint report at:
      """ships-logs/pm-standards-lint.md"""

  Scenario: Structure of the lint report for future remediation
    Given the lint report has been generated
    When a crew member opens ships-logs/pm-standards-lint.md
    Then the report MUST contain entries grouped by severity:
      | severity   |
      | error      |
      | warning    |
      | info       |
    And each entry MUST include:
      | field          |
      | artifact_path  |
      | rule_category  |
      | severity       |
      | message        |
      | suggested_fix  |
    And the report MUST include a summary section with:
      | summary_field   |
      | total_artifacts |
      | total_errors    |
      | total_warnings  |
      | total_infos     |
    And the report structure MUST support mapping entries to:
      | consumer                     |
      | future cleanup milestones    |
      | specific standards features  |
      | Santiago-Ethicist review     |

  # 6. ROOT-LEVEL DOCUMENTATION STANDARDS

  Scenario: Establish root-level documentation standards
    Given the santiago-pm root contains documentation files
    And at least folder-structure.md and README.md exist
    When documentation standards are applied
    Then folder-structure.md MUST follow the folder organization template
    And README.md MUST follow the project documentation template
    And both MUST include KG metadata headers
    And both MUST remain consistent with nautical theming conventions