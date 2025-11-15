Feature: PM Domain User Story Mapping
  As a product team using Santiago PM
  I want autonomous user story mapping facilitation
  So that we can organize work around user value

  Background:
    Given the PM domain expert is initialized
    And the Pilot agent has Jeff Patton methodology knowledge
    And the Pilot agent is available

  Scenario: Creating initial story map
    Given a product concept without story map
    And a defined user journey
    When the Pilot facilitates story mapping
    Then user activity backbone should be identified
    And user tasks should be mapped under activities
    And stories should be organized by priority
    And walking skeleton should be defined
    And MVP scope should be identified

  Scenario: Story mapping with existing stories
    Given 50 existing user stories
    And stories are not yet organized
    When the Pilot facilitates story mapping
    Then stories should be grouped by user activity
    And vertical slicing should be applied
    And release planning should be guided
    And outcome focus should be maintained

  Scenario: Identifying MVP scope
    Given a complete story map
    And budget constraints
    When the Pilot helps identify MVP
    Then essential user activities should be prioritized
    And walking skeleton should define core flow
    And nice-to-have features should be deferred
    And value delivery should be maximized

  Scenario: Story map for multiple user types
    Given a product serving different user personas
    When the Pilot facilitates story mapping
    Then each user type's journey should be mapped
    And shared activities should be identified
    And persona-specific needs should be captured
    And inclusive design should be promoted

  Scenario: Outcome-focused story mapping
    Given a story map draft
    When the Pilot reviews the map
    Then focus should shift from features to outcomes
    And user value should be explicit
    And success metrics should be defined
    And Jeff Patton's outcome thinking should be applied
