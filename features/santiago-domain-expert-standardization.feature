Feature: Santiago Domain Expert Standardization

  As the Santiago Captain
  I want standardized naming for all domain experts
  So that the crew operates with clear roles and responsibilities

  Background:
    Given multiple Santiago agents exist
    And roles include Navigator, Quartermaster, Pilot, etc.

  Scenario: Define naming standard
    Given existing agents need standardization
    When naming rules are applied
    Then use format: "Santiago [Domain] [Role]"
    And define standard roles:
      | Role          | Responsibility                  |
      | Navigator     | Analysis and orchestration      |
      | Quartermaster | Ethics and resource management  |
      | Pilot         | Domain expertise                |
      | Architect     | Design and structure            |
      | Developer     | Implementation                  |
      | QA            | Validation and testing          |
      | Researcher    | Exploration and learning        |

  Scenario: Audit and rename existing agents
    Given agents in .github/agents/ and roles/
    When audit runs
    Then rename to standard format
    And update all references
    And create role definition documents

  Scenario: Create new agent template
    Given a new domain expert is needed
    When template is used
    Then follow naming standard
    And include role responsibilities
    And integrate with KG for agent discovery