# Fishnet Architecture Specification

**Version**: 2.0.0  
**Author**: Copilot (Architecture Phase)  
**Date**: 2025-11-16  
**Purpose**: Multi-strategy BDD test generation for Santiago PM behaviors

---

## Overview

Fishnet generates BDD (Behavior-Driven Development) test files from extracted PM behaviors. Version 2.0 implements 5 distinct generation strategies as specified in `santiago-pm/cargo-manifests/fishnet-bdd-generation-strategies.feature.md`.

**Current State**: `nusy_orchestrator/santiago_builder/fishnet.py` exists as stub  
**Target State**: Full implementation with 5 strategies, CLI, and BDD file generation

---

## Architecture Principles

1. **Strategy Pattern**: Each BDD generation approach is a separate strategy class
2. **Pluggable**: Strategies can be selected via CLI or config
3. **Composable**: Multiple strategies can be run in sequence (validation loop)
4. **Provenance**: Track which strategy generated which scenarios
5. **Idempotent**: Re-running same strategy produces same output (deterministic)

---

## File Structure

```
nusy_orchestrator/santiago_builder/
├── fishnet.py                          # Main orchestrator (EXISTING STUB)
├── fishnet_strategies/                 # NEW DIRECTORY
│   ├── __init__.py
│   ├── base_strategy.py                # Abstract base class
│   ├── bottom_up_strategy.py           # Strategy 1: From extracted behaviors
│   ├── top_down_strategy.py            # Strategy 2: From domain ontology
│   ├── external_strategy.py            # Strategy 3: Research best practices
│   ├── logic_strategy.py               # Strategy 4: Computational validation
│   └── experiment_strategy.py          # Strategy 5: Unknown resolution
└── tests/
    └── test_fishnet_strategies.py      # Unit tests
```

---

## Class Diagram

```python
# base_strategy.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class BehaviorSpec:
    """Extracted behavior specification"""
    name: str
    description: str
    capability_level: str  # Apprentice, Journeyman, Master, Expert
    knowledge_scope: str   # Pond, Lake, Sea, Ocean
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    mutates_kg: bool
    concurrency_safe: bool
    ontology_mapping: str  # e.g., "nusy:PMBehavior-CreateFeature"
    cli_example: str
    sparql_query: str = ""

@dataclass
class BDDScenario:
    """Generated BDD scenario"""
    scenario_name: str
    scenario_type: str  # happy_path, edge_case, error_handling
    given_steps: List[str]
    when_steps: List[str]
    then_steps: List[str]
    strategy_used: str  # Which strategy generated this

@dataclass
class BDDFeatureFile:
    """Complete .feature file"""
    feature_name: str
    feature_description: str
    background_steps: List[str]
    scenarios: List[BDDScenario]
    tags: List[str]
    behavior_spec: BehaviorSpec

class BDDGenerationStrategy(ABC):
    """Abstract base for BDD generation strategies"""
    
    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Strategy identifier (e.g., 'BottomUp', 'TopDown')"""
        pass
    
    @abstractmethod
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Generate 3 scenarios (happy, edge, error) for a behavior.
        
        Args:
            behavior: Extracted behavior specification
            context: Additional context (ontology, examples, etc.)
            
        Returns:
            List of 3 BDDScenario objects
        """
        pass
    
    def generate_feature_file(
        self,
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> BDDFeatureFile:
        """
        Generate complete .feature file for a behavior.
        Calls generate_scenarios() and wraps in feature structure.
        """
        scenarios = self.generate_scenarios(behavior, context)
        return BDDFeatureFile(
            feature_name=f"MCP Tool: {behavior.name}",
            feature_description=behavior.description,
            background_steps=self._generate_background(behavior),
            scenarios=scenarios,
            tags=[f"@{behavior.capability_level}", f"@{behavior.knowledge_scope}"],
            behavior_spec=behavior
        )
    
    @abstractmethod
    def _generate_background(self, behavior: BehaviorSpec) -> List[str]:
        """Generate Background section (common setup steps)"""
        pass
```

---

## Strategy Implementations

### Strategy 1: Bottom-Up (DocumentFirst)

**Source**: `knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md`  
**Approach**: Generate scenarios directly from extracted behavior specifications

```python
# bottom_up_strategy.py
class BottomUpStrategy(BDDGenerationStrategy):
    """Generate BDD from extracted behavior documentation"""
    
    @property
    def strategy_name(self) -> str:
        return "BottomUp"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Generate scenarios from behavior input/output schemas:
        1. Happy path: Valid inputs → expected outputs
        2. Edge case: Boundary values, optional params
        3. Error handling: Invalid inputs → error responses
        """
        scenarios = []
        
        # Scenario 1: Happy path (use CLI example from behavior spec)
        scenarios.append(BDDScenario(
            scenario_name=f"Successfully execute {behavior.name}",
            scenario_type="happy_path",
            given_steps=self._extract_given_from_inputs(behavior.input_schema),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool"],
            then_steps=self._extract_then_from_outputs(behavior.output_schema),
            strategy_used="BottomUp"
        ))
        
        # Scenario 2: Edge case (boundary values, optional params)
        scenarios.append(BDDScenario(
            scenario_name=f"Handle edge cases for {behavior.name}",
            scenario_type="edge_case",
            given_steps=self._generate_edge_case_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool"],
            then_steps=self._generate_edge_case_assertions(behavior),
            strategy_used="BottomUp"
        ))
        
        # Scenario 3: Error handling (invalid/missing required params)
        scenarios.append(BDDScenario(
            scenario_name=f"Handle errors for {behavior.name}",
            scenario_type="error_handling",
            given_steps=self._generate_error_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool"],
            then_steps=["the MCP tool should return an error", 
                       "the error message should be descriptive"],
            strategy_used="BottomUp"
        ))
        
        return scenarios
    
    def _extract_given_from_inputs(self, input_schema: Dict) -> List[str]:
        """Convert input schema to Given steps"""
        steps = ["the Santiago PM knowledge graph is initialized"]
        required = input_schema.get("required", [])
        properties = input_schema.get("properties", {})
        
        for field in required:
            field_type = properties.get(field, {}).get("type", "string")
            steps.append(f"I have a valid '{field}' parameter ({field_type})")
        
        return steps
    
    def _extract_then_from_outputs(self, output_schema: Dict) -> List[str]:
        """Convert output schema to Then steps"""
        steps = ["the MCP tool should succeed"]
        properties = output_schema.get("properties", {})
        
        for field in properties.keys():
            steps.append(f"the response should contain '{field}'")
        
        steps.append("the knowledge graph should be updated")
        return steps
    
    def _generate_background(self, behavior: BehaviorSpec) -> List[str]:
        return [
            "Given the Santiago PM MCP service is running",
            "And the knowledge graph is initialized with test data",
            f"And I have {behavior.capability_level} level permissions"
        ]
```

### Strategy 2: Top-Down (SchemaDriven)

**Source**: `knowledge/ontologies/pm-domain-ontology.ttl`  
**Approach**: Generate scenarios from ontology constraints

```python
# top_down_strategy.py
class TopDownStrategy(BDDGenerationStrategy):
    """Generate BDD from ontology structure and constraints"""
    
    def __init__(self, ontology_path: str):
        self.ontology_path = ontology_path
        # Load ontology to extract constraints
    
    @property
    def strategy_name(self) -> str:
        return "TopDown"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Generate scenarios from ontology:
        1. Valid ontology instance creation
        2. Constraint violation (e.g., missing required property)
        3. Relationship validation (e.g., Feature → Issue link)
        """
        # Look up ontology class for this behavior
        onto_class = behavior.ontology_mapping  # e.g., "nusy:PMBehavior-CreateFeature"
        
        # Generate scenarios based on ontology rules
        # (Implementation would parse .ttl file or query loaded ontology)
        
        return [
            # Scenario 1: Valid ontology instance
            BDDScenario(
                scenario_name=f"Create valid {onto_class} instance",
                scenario_type="happy_path",
                given_steps=[
                    "the ontology defines required properties for " + onto_class,
                    "I provide all required properties"
                ],
                when_steps=[f"I invoke '{behavior.name}'"],
                then_steps=[
                    "a valid RDF triple should be created",
                    "the instance should conform to ontology constraints"
                ],
                strategy_used="TopDown"
            ),
            # Scenario 2: Constraint violation
            # Scenario 3: Relationship validation
            # ... (similar structure)
        ]
```

### Strategy 3: External (Research-Driven)

**Source**: External best practices, industry standards  
**Approach**: Look up common PM tool patterns (Jira, Linear, GitHub Issues)

```python
# external_strategy.py
class ExternalStrategy(BDDGenerationStrategy):
    """Generate BDD from external PM tool best practices"""
    
    @property
    def strategy_name(self) -> str:
        return "External"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Compare Santiago behavior to industry tools:
        1. Standard workflow (e.g., Jira issue creation)
        2. Edge case from real-world tool (e.g., bulk operations)
        3. Error pattern from industry (e.g., duplicate detection)
        """
        # Map behavior to industry equivalent
        industry_pattern = self._map_to_industry_tool(behavior.name)
        
        # Generate scenarios based on known patterns
        # (Could use GPT-4 to research, or static mapping)
        
        return [
            # Scenarios modeled after Jira/Linear/GitHub workflows
            # ...
        ]
```

### Strategy 4: Logic (Computational)

**Source**: State machines, business rules, formulas  
**Approach**: Generate scenarios from logical constraints

```python
# logic_strategy.py
class LogicStrategy(BDDGenerationStrategy):
    """Generate BDD from computational logic and state machines"""
    
    @property
    def strategy_name(self) -> str:
        return "Logic"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Generate scenarios from logic rules:
        1. State transition (e.g., Open → InProgress)
        2. Calculation verification (e.g., velocity = features/sprint)
        3. Invariant validation (e.g., status must be valid enum)
        """
        # For status_transition: Test state machine
        # For track_velocity: Test calculation formula
        # For prioritize_backlog: Test ranking algorithm
        
        return [
            # Scenarios testing computational correctness
            # ...
        ]
```

### Strategy 5: Experiment (Unknown Resolution)

**Source**: Gaps in other strategies  
**Approach**: Generate placeholder scenarios for manual refinement

```python
# experiment_strategy.py
class ExperimentStrategy(BDDGenerationStrategy):
    """Generate experimental scenarios for unknown edge cases"""
    
    @property
    def strategy_name(self) -> str:
        return "Experiment"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Generate scenarios for unknown behaviors:
        1. Hypothesis-driven test (requires user experiment)
        2. Ambiguous requirement clarification
        3. Performance/scalability edge case
        """
        return [
            BDDScenario(
                scenario_name=f"[EXPERIMENT] Test {behavior.name} under load",
                scenario_type="edge_case",
                given_steps=[
                    "[TODO] Define load test parameters",
                    "[TODO] Set up concurrent execution environment"
                ],
                when_steps=[f"I invoke '{behavior.name}' 100 times concurrently"],
                then_steps=[
                    "[TODO] Define acceptable latency",
                    "[TODO] Verify no race conditions"
                ],
                strategy_used="Experiment"
            ),
            # More experimental scenarios...
        ]
```

---

## Main Orchestrator

```python
# fishnet.py (enhance existing stub)
from pathlib import Path
from typing import List, Dict, Any
from fishnet_strategies import (
    BDDGenerationStrategy,
    BottomUpStrategy,
    TopDownStrategy,
    ExternalStrategy,
    LogicStrategy,
    ExperimentStrategy
)

class Fishnet:
    """Multi-strategy BDD test generator for Santiago PM behaviors"""
    
    def __init__(
        self,
        behaviors_file: Path,
        ontology_file: Path,
        output_dir: Path
    ):
        self.behaviors_file = behaviors_file
        self.ontology_file = ontology_file
        self.output_dir = output_dir
        
        # Initialize strategies
        self.strategies = {
            "bottom_up": BottomUpStrategy(),
            "top_down": TopDownStrategy(str(ontology_file)),
            "external": ExternalStrategy(),
            "logic": LogicStrategy(),
            "experiment": ExperimentStrategy()
        }
    
    def generate_all_bdd_files(
        self,
        strategy_names: List[str] = ["bottom_up"]
    ) -> Dict[str, Any]:
        """
        Generate BDD .feature files for all behaviors using specified strategies.
        
        Args:
            strategy_names: List of strategies to use (default: ["bottom_up"])
            
        Returns:
            Dict with generation results and statistics
        """
        # Load behaviors from extraction files
        behaviors = self._load_behaviors()
        
        results = {
            "total_behaviors": len(behaviors),
            "files_generated": 0,
            "strategies_used": strategy_names,
            "generation_time": 0
        }
        
        for behavior in behaviors:
            feature_file = self._generate_feature_file(
                behavior,
                strategy_names
            )
            
            # Write to disk
            output_path = self.output_dir / f"{behavior.name}.feature"
            self._write_feature_file(feature_file, output_path)
            results["files_generated"] += 1
        
        return results
    
    def _load_behaviors(self) -> List[BehaviorSpec]:
        """Load behaviors from pm-behaviors-extracted.md and passage-behaviors-extracted.md"""
        # Parse markdown files and extract behavior specs
        # Return list of BehaviorSpec objects (28 total)
        pass
    
    def _generate_feature_file(
        self,
        behavior: BehaviorSpec,
        strategy_names: List[str]
    ) -> str:
        """Generate Gherkin .feature file content"""
        # Run selected strategies
        all_scenarios = []
        for strategy_name in strategy_names:
            strategy = self.strategies[strategy_name]
            scenarios = strategy.generate_scenarios(behavior)
            all_scenarios.extend(scenarios)
        
        # Format as Gherkin
        return self._format_gherkin(behavior, all_scenarios)
    
    def _format_gherkin(
        self,
        behavior: BehaviorSpec,
        scenarios: List[BDDScenario]
    ) -> str:
        """Format scenarios as Gherkin syntax"""
        lines = []
        lines.append(f"Feature: {behavior.name}")
        lines.append(f"  {behavior.description}")
        lines.append("")
        lines.append("  Background:")
        for step in scenarios[0].strategy_used:  # Get background from strategy
            lines.append(f"    {step}")
        lines.append("")
        
        for scenario in scenarios:
            lines.append(f"  Scenario: {scenario.scenario_name}")
            for step in scenario.given_steps:
                lines.append(f"    Given {step}")
            for step in scenario.when_steps:
                lines.append(f"    When {step}")
            for step in scenario.then_steps:
                lines.append(f"    Then {step}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _write_feature_file(self, content: str, path: Path):
        """Write feature file to disk"""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate BDD tests for Santiago PM")
    parser.add_argument("--behaviors", required=True, help="Path to behaviors extraction file")
    parser.add_argument("--ontology", required=True, help="Path to ontology .ttl file")
    parser.add_argument("--output", required=True, help="Output directory for .feature files")
    parser.add_argument("--strategies", nargs="+", default=["bottom_up"],
                       choices=["bottom_up", "top_down", "external", "logic", "experiment"])
    
    args = parser.parse_args()
    
    fishnet = Fishnet(
        behaviors_file=Path(args.behaviors),
        ontology_file=Path(args.ontology),
        output_dir=Path(args.output)
    )
    
    results = fishnet.generate_all_bdd_files(strategy_names=args.strategies)
    print(f"Generated {results['files_generated']} BDD feature files")
```

---

## Acceptance Criteria

**For GitHub Agent Implementation**:

1. **Strategy Pattern Implemented**:
   - [x] `base_strategy.py` with abstract BDDGenerationStrategy class
   - [x] `bottom_up_strategy.py` fully implemented (primary strategy)
   - [ ] `top_down_strategy.py` implemented (ontology-driven)
   - [ ] `external_strategy.py` stub (can be simple mapping)
   - [ ] `logic_strategy.py` stub
   - [ ] `experiment_strategy.py` stub

2. **Behavior Loading**:
   - [x] Parse `pm-behaviors-extracted.md` (20 behaviors)
   - [x] Parse `passage-behaviors-extracted.md` (8 behaviors)
   - [x] Convert markdown to BehaviorSpec objects

3. **BDD File Generation**:
   - [x] Generate 84 .feature files (28 behaviors × 3 scenarios)
   - [x] Valid Gherkin syntax
   - [x] Background section with common setup
   - [x] Tags for capability level and knowledge scope
   - [x] Reference KG nodes in scenarios

4. **CLI Working**:
   ```bash
   python nusy_orchestrator/santiago_builder/fishnet.py \
     --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \
     --ontology knowledge/ontologies/pm-domain-ontology.ttl \
     --output knowledge/catches/santiago-pm-behaviors/bdd-tests/ \
     --strategies bottom_up
   ```

5. **Unit Tests**:
   - [x] Test BottomUpStrategy scenario generation
   - [x] Test Gherkin formatting
   - [x] Test behavior loading from markdown
   - [x] All tests pass with pytest

6. **Output Quality**:
   - [x] Each .feature file has 3 scenarios minimum
   - [x] Scenarios cover happy path, edge case, error handling
   - [x] Steps reference actual input/output schema fields
   - [x] No syntax errors (validate with behave --dry-run)

---

## Example Output

**File**: `knowledge/catches/santiago-pm-behaviors/bdd-tests/create_feature.feature`

```gherkin
Feature: create_feature
  Generate BDD feature specification from vision statement

  Background:
    Given the Santiago PM MCP service is running
    And the knowledge graph is initialized with test data
    And I have Journeyman level permissions

  Scenario: Successfully execute create_feature
    Given I have a valid 'title' parameter (string)
    And I have a valid 'vision_statement' parameter (string)
    And I have a valid 'hypothesis' parameter (string)
    When I invoke the 'create_feature' MCP tool
    Then the MCP tool should succeed
    And the response should contain 'feature_id'
    And the response should contain 'cargo_manifest_path'
    And the knowledge graph should be updated

  Scenario: Handle edge cases for create_feature
    Given I provide optional 'epic' parameter
    And I provide empty 'assignees' array
    When I invoke the 'create_feature' MCP tool
    Then the MCP tool should succeed
    And the feature should have no assignees
    And the feature should not belong to an epic

  Scenario: Handle errors for create_feature
    Given I am missing the required 'title' parameter
    When I invoke the 'create_feature' MCP tool
    Then the MCP tool should return an error
    And the error message should be descriptive
```

---

## Implementation Notes for GitHub Agent

1. **Start with BottomUpStrategy**: This is the most straightforward - parse behavior markdown, extract schemas, generate scenarios

2. **Markdown Parsing**: The behavior files have clear structure:
   ```
   ### Behavior X.Y: behavior_name
   **Input Schema**: ```json ... ```
   **Output Schema**: ```json ... ```
   ```
   Extract these sections and convert to BehaviorSpec objects

3. **Gherkin Format**: Use standard Gherkin keywords (Feature, Background, Scenario, Given, When, Then)

4. **File Naming**: Use `{behavior_name}.feature` (e.g., `create_feature.feature`)

5. **Testing**: Run `behave --dry-run <output_dir>` to validate syntax without executing

6. **Provenance**: Add comment header to each .feature file:
   ```gherkin
   # Generated by Fishnet v2.0.0
   # Strategy: BottomUp
   # Source: pm-behaviors-extracted.md
   # Generated: 2025-11-16
   ```
