Feature: KnowledgeOps Pipeline – Knowledge as Code CI/CD
  As Hank the Captain and Santiago-Core
  I want a clear KnowledgeOps pipeline for domain knowledge
  So that knowledge changes are ingested, validated, versioned, and deployed as safely as code

  Background:
    Given the KnowledgeOps vision is described in section 6.2 of "docs-arch-redux-3/arch-vision-merged-plan.md"
    And a brain dump exists at "santiago-pm/research-logs/knowledge-ops-brain-dump.md"

  @pipeline
  Scenario: Define stages of the KnowledgeOps pipeline
    When Santiago-PM reads "knowledge-ops-brain-dump.md"
    Then Santiago-PM SHOULD propose a pipeline with stages:
      | stage     |
      | ingest    |
      | validate  |
      | version   |
      | deploy    |
    And each stage SHOULD:
      | requirement                            |
      | map to concrete tools or services      |
      | define required artifacts and outputs  |
      | define failure/rollback behavior       |

  @git_vs_kg
  Scenario: Decide Git vs KG responsibilities
    Given knowledge artifacts live as files under "knowledge/" and domain folders
    And the KG stores runtime triples and provenance
    When Santiago-Core and Hank review the pros and cons
    Then the decision SHOULD be:
      | rule                                                   |
      | Git is the primary source of truth for knowledge files |
      | KG is the runtime projection of validated knowledge    |
    And this decision SHOULD be recorded in:
      | path                                          |
      | docs-arch-redux-3/arch-vision-merged-plan.md |
      | GLOSSARY.md                                  |

  @ownership
  Scenario: Clarify ownership and implementation location
    Given KnowledgeOps is a cross-domain concern
    When Santiago-Core and Santiago-PM discuss responsibilities
    Then the implementation home SHOULD be:
      | component      | responsibility                                     |
      | santiago-core  | shared KnowledgeOps services and orchestration     |
      | santiago-pm    | PM-domain knowledge artifacts and workflows        |
    And this SHOULD be reflected in:
      | artifact_type | path                                        |
      | doc           | docs-arch-redux-3/arch-migration-plan.md    |
      | doc           | santiago-pm/tackle/folder-structure.md      |


