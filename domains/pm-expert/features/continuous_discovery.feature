Feature: PM Domain Continuous Discovery
  As a product team using Santiago PM
  I want autonomous continuous discovery facilitation
  So that we can learn from users and validate assumptions

  Background:
    Given the PM domain expert is initialized
    And the Pilot agent has Lean UX knowledge from Jeff Gothelf
    And the Pilot agent is available
    And the Quartermaster ethical overseer is available

  Scenario: Formulating hypotheses
    Given a product idea without validated assumptions
    When the Pilot facilitates discovery
    Then clear hypotheses should be formulated
    And assumptions should be identified
    And success criteria should be defined
    And experiments should be designed

  Scenario: Designing validation experiments
    Given a hypothesis to test
    And limited research budget
    When the Pilot designs validation experiment
    Then lean experiment approach should be recommended
    And build-measure-learn cycle should be applied
    And minimum viable prototype should be suggested
    And success metrics should be defined

  Scenario: Planning user research
    Given research questions to answer
    When the Pilot guides research planning
    Then appropriate research methods should be recommended
    And sample size should be determined
    And ethical research practices should be ensured
    And the Quartermaster should validate user respect

  Scenario: Ethical user research
    Given a proposed user research plan
    When the Quartermaster reviews the plan
    Then user privacy should be protected
    And informed consent should be required
    And data protection should be ensured
    And user time should be respected
    And unbiased methods should be validated

  Scenario: Learning from discovery
    Given completed discovery experiments
    And research findings
    When the Pilot analyzes results
    Then learnings should be synthesized
    And next experiments should be recommended
    And knowledge should be shared with team
    And progressive revelation principle should be applied

  Scenario: Rapid prototyping guidance
    Given a hypothesis to validate quickly
    When the Pilot recommends prototyping approach
    Then appropriate fidelity level should be suggested
    And focus should be on learning not polish
    And feedback loops should be tight
    And iteration should be encouraged
