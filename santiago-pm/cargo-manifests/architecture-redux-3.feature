Feature: Architecture Redux 3 – Target Runtime & Repo Alignment
  As Hank the Captain and the Santiago crew
  I want the repository structure and runtime behavior to match the merged architecture vision
  So that Noesis and all Santiagos run with a clean, consistent, and evolvable architecture

  Background:
    Given the merged architecture doc exists at "docs-arch-redux-3/arch-vision-merged-plan.md"
    And the migration plan exists at "docs-arch-redux-3/arch-migration-plan.md"

  @docs
  Scenario: Align architecture docs with merged plan
    Given the current architecture docs exist in "ARCHITECTURE.md" and "docs/"
    When Santiago-PM reviews "arch-vision-merged-plan.md"
    Then Santiago-PM SHOULD propose updates to:
      | doc_path                  |
      | ARCHITECTURE.md           |
      | docs/ARCHITECTURE/*.md    |
      | docs/vision/*.md          |
    And the updates SHOULD:
      | requirement                                |
      | reference the merged vision as target      |
      | mark legacy bootstrap docs as historical   |
      | avoid duplicating the merged plan content  |

  @folders
  Scenario: Plan folder and code migration
    Given the two-namespace model (domain/* vs self-improvement/*) is defined in the merged plan
    And the canonical self-improvement scaffold is defined by "santiago-pm/tackle/folder-structure.md"
    When Santiago-PM analyzes the current top-level folders
    Then Santiago-PM SHOULD update "arch-migration-plan.md" with:
      | section                       |
      | 1.3 Root Artifact Triage      |
      | additional folder mappings    |
    And no destructive changes SHOULD be made without:
      | gate            |
      | CI/CD checks    |
      | Ethicist review |
      | Hank approval   |

  @runtime
  Scenario: Harden DGX runtime against merged architecture
    Given the DGX runtime model is defined in section 2 of "arch-vision-merged-plan.md"
    When Santiago-Core is run via "santiago_core/run_team.py"
    Then the observed behavior SHOULD match the merged plan description for:
      | aspect           |
      | always-on loop   |
      | Kanban usage     |
      | KG integration   |
    And any deviations SHOULD be captured as:
      | artifact_type | path                                 |
      | issue         | santiago-pm/ships-logs/*.md         |
      | task          | santiago-pm/tasks/*.md              |
      | research-log  | santiago-pm/research-logs/*.md      |


