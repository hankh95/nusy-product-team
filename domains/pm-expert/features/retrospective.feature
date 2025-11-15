Feature: PM Domain Retrospective Facilitation
  As a product team using Santiago PM
  I want autonomous retrospective facilitation
  So that we can continuously improve our process

  Background:
    Given the PM domain expert is initialized
    And the Pilot agent is available
    And the Quartermaster ethical overseer is available

  Scenario: Basic retrospective facilitation
    Given a completed sprint with ID "sprint-001"
    And team feedback has been collected
    And sprint metrics are available
    When the Pilot facilitates the retrospective
    Then retrospective guidance should be provided
    And the guidance should cover "what went well"
    And the guidance should cover "what could improve"
    And action items should be identified
    And the Quartermaster should ensure safe space
    And all voices should be heard equally

  Scenario: Retrospective with team conflicts
    Given a sprint where team disagreements occurred
    And feedback includes conflicting viewpoints
    When the Pilot facilitates the retrospective
    Then the approach should focus on learning not blame
    And the Quartermaster should validate psychological safety
    And constructive resolution should be encouraged
    And focus should remain on improvement

  Scenario: Retrospective celebrating success
    Given a highly successful sprint
    And team achieved all sprint goals
    When the Pilot facilitates the retrospective
    Then successes should be celebrated
    And learning from success should be captured
    And momentum should be maintained
    And gratitude should be expressed

  Scenario: Retrospective with performance issues
    Given a sprint with missed commitments
    And velocity was lower than expected
    When the Pilot facilitates the retrospective
    Then root causes should be explored non-judgmentally
    And systemic issues should be identified
    And actionable improvements should be proposed
    And team morale should be protected

  Scenario: Ethical validation of retrospective process
    Given a retrospective facilitation approach
    When the Quartermaster reviews the process
    Then the approach should create safe space
    And all team members should participate equally
    And focus should be on improvement not blame
    And actionable outcomes should result
    And team trust should be strengthened
