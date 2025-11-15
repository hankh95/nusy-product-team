Feature: Scaffold NuSy Product Team Core
  As Hank’s NuSy Product Manager Agent
  I want to capture the vision, practices, roles, and backlog
  So that the team can deliver executable BDD specs with clear hypotheses.

  Scenario: Document scaffolding artifacts for the NuSy PM core
    Given the repository is empty of NuSy PM artifacts
    When I create README guidance, development plan, and practice documents
    And I add role instructions for Architect, Developer, QA, UX, and Platform agents
    And I author the first feature `scaffold_project.feature` and backlog hypotheses
    Then each role has a `*.agent.instructions.md` file under `roles/`
    And `DEVELOPMENT_PLAN.md` lists hypotheses, experiments, and next steps
    And `DEVELOPMENT_PRACTICES.md` enforces TDD/BDD, KG capture, and CI gates
    And the backlog table maps epics to hypotheses and metrics
