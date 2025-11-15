Feature: NuSy PM Domain Restructuring

  As a Santiago domain expert
  I want the PM domain organized under a unified nusy_pm folder
  So that agents can autonomously discover and manage PM artifacts

  Background:
    Given the NuSy PM system exists
    And PM features include issues, experiments, plans, and notes

  Scenario: Create nusy_pm root folder with nautical subfolders
    Given no nusy_pm folder exists
    When the restructuring feature is activated
    Then create nusy_pm/ root folder
    And create subfolders:
      | Subfolder          | Purpose                          | Nautical Name      |
      | cargo-manifests    | Feature specifications           | Cargo Manifests    |
      | ships-logs         | Issue tracking                   | Ship's Logs        |
      | voyage-trials      | Experiment management            | Voyage Trials      |
      | navigation-charts  | Development plans                | Navigation Charts  |
      | captains-journals  | Knowledge capture                | Captain's Journals |
    And add agent-readable metadata files to each subfolder

  Scenario: Automatically update development plan
    Given a new PM feature is created
    When the feature is activated
    Then automatically update the development plan
    And add KG relations for the new structure
    And notify Santiago agents of the restructuring

  Scenario: Migrate existing artifacts
    Given existing features, issues, and experiments exist
    When migration is triggered
    Then move artifacts to appropriate nautical-named subfolders
    And update all references and KG relations
    And maintain backward compatibility links