---
id: scaffold-project-001
type: feature
status: open
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["santiago-pm"]
labels: ["type:feature", "priority:high", "component:scaffolding", "nautical:theming"]
epic: santiago-core-architecture
domain: product-management
owners: ["santiago-pm"]
stakeholders: ["santiago-architect"]
skill_level: master
knowledge_scope: sea
artifact_kinds: ["template", "scaffold", "automation"]
related_experiments: []
related_artifacts:
  - ../templates/project-scaffold.md
  - ../../santiago_core/
mcp_tools_hint:
  - "nusy_pm.scaffold_project"
---

Feature: Scaffold new Santiago domain expert projects

  As Santiago-PM
  I want to create new Santiago domain expert projects
  So that each domain gets its own autonomous AI system with human-readable PM artifacts

  Background:
    Given santiago-pm has access to project scaffolding templates
    And the target domain is well-defined with clear boundaries
    And santiago-core scaffold structure exists as reference

  Scenario Outline: Scaffold complete project structure for new domain expert
    Given a new domain expert project "<project_name>" is requested
    And the domain description is "<domain_description>"
    When santiago-pm executes the scaffold command
    Then a new git repository is initialized with name "<project_name>"
    And the following folder structure is created at project root:
      | folder_path              | purpose                          |
      | cargo-manifests/         | Feature specifications           |
      | ships-logs/              | Issues and incidents             |
      | voyage-trials/           | Experiments                      |
      | navigation-charts/       | Development plans                |
      | captains-journals/       | Knowledge capture                |
      | crew-manifests/          | Agent roles                      |
      | strategic-charts/        | Vision and strategy              |
      | quality-assessments/     | QA and testing                   |
      | research-logs/           | Research findings                |
      | santiago-core/           | AI implementation (KG + agents)  |
    And each PM folder contains:
      | file_name                | content_type                     |
      | README.md                | Folder purpose and usage guide   |
      | [folder]-template.md     | Artifact creation template       |
    And santiago-core/ is initialized with:
      | component                | status                           |
      | basic agent framework    | scaffolded                       |
      | knowledge graph          | initialized                      |
      | core services            | stubbed                          |
      | configuration files      | created                          |
    And project files are created:
      | file_name                | content_type                     |
      | README.md                | Project overview                 |
      | pyproject.toml           | Python project configuration     |
      | requirements.txt         | Dependencies                     |
      | .gitignore               | Git ignore patterns              |
      | .env.example            | Environment template            |
    And initial PM artifacts are created:
      | artifact_type            | title                            |
      | strategic-chart          | Domain Vision and Strategy       |
      | navigation-chart         | Initial Development Plan         |
      | crew-manifest            | Core Agent Roles                 |
      | cargo-manifest           | Project Setup and Initialization |

    Examples:
      | project_name             | domain_description               |
      | santiago-medical-expert  | Healthcare and medical knowledge |
      | santiago-research-assistant | Academic research support     |
      | santiago-software-architect | System architecture design    |

  Scenario: Initialize Santiago-core with domain-specific configuration
    Given a new project scaffold is created
    When santiago-core is initialized
    Then the knowledge graph contains project metadata:
      | metadata_field           | value_source                     |
      | project_name             | scaffold parameter               |
      | domain_description       | scaffold parameter               |
      | creation_date            | current timestamp                |
      | santiago_version         | current framework version        |
      | pm_integration           | santiago-pm reference            |
    And initial agent roles are defined in crew-manifests/:
      | role_name                | specialization                   |
      | domain-expert            | core domain knowledge            |
      | knowledge-manager        | KG maintenance and querying      |
      | task-coordinator         | workflow and task management     |
    And agent communication protocols are established
    And basic API endpoints are scaffolded for external integration

  Scenario: Create initial PM artifacts for project bootstrap
    Given the project structure is scaffolded
    When initial PM artifacts are created
    Then strategic-charts/ contains domain vision document
    And navigation-charts/ contains development roadmap
    And crew-manifests/ contains agent role definitions
    And cargo-manifests/ contains project initialization features
    And all artifacts follow the established scaffold pattern:
      | requirement              | validation_method                |
      | YAML frontmatter         | metadata schema validation       |
      | KG-compatible IDs        | ID format checking               |
      | nautical theming         | terminology validation           |
      | cross-references         | relation establishment           |

  Scenario: Establish project development workflow
    Given the scaffolded project is ready
    When development begins
    Then ships-logs/ tracks all development activities
    And voyage-trials/ manages experimental features
    And quality-assessments/ validates deliverables
    And captains-journals/ captures lessons learned
    And research-logs/ documents domain discoveries
    And all artifacts integrate with the project KG
    And santiago-core agents can read/write PM artifacts autonomously
