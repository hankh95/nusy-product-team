"""Unit tests for Fishnet v2.0.0 BDD generation strategies

Tests the multi-strategy BDD generation system including:
- BehaviorSpec parsing from markdown
- BottomUpStrategy scenario generation
- Feature file generation with Gherkin formatting
- Complete end-to-end workflow
"""

import json
import pytest
from pathlib import Path
from nusy_orchestrator.santiago_builder.fishnet_strategies import (
    BehaviorSpec,
    BDDScenario,
    BDDFeatureFile,
    BottomUpStrategy,
)
from nusy_orchestrator.santiago_builder.fishnet import FishnetV2


class TestBehaviorSpec:
    """Test BehaviorSpec data class"""
    
    def test_behavior_spec_creation(self):
        """Test creating a BehaviorSpec"""
        behavior = BehaviorSpec(
            name="test_behavior",
            description="Test behavior description",
            capability_level="Journeyman",
            knowledge_scope="Lake",
            input_schema={"properties": {"param1": {"type": "string"}}},
            output_schema={"properties": {"result": {"type": "string"}}},
            mutates_kg=True,
            concurrency_safe=False,
            ontology_mapping="nusy:PMBehavior-Test",
            cli_example="nusy test --param1 value",
            source_file="test.md"
        )
        
        assert behavior.name == "test_behavior"
        assert behavior.capability_level == "Journeyman"
        assert behavior.mutates_kg is True


class TestBottomUpStrategy:
    """Test BottomUpStrategy implementation"""
    
    def test_strategy_name(self):
        """Test strategy name property"""
        strategy = BottomUpStrategy()
        assert strategy.strategy_name == "BottomUp"
    
    def test_generate_scenarios_count(self):
        """Test that 3 scenarios are generated per behavior"""
        strategy = BottomUpStrategy()
        behavior = BehaviorSpec(
            name="create_feature",
            description="Create a new feature",
            capability_level="Journeyman",
            knowledge_scope="Lake",
            input_schema={
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["title"]
            },
            output_schema={
                "properties": {
                    "feature_id": {"type": "string"}
                }
            },
            mutates_kg=True,
            concurrency_safe=False,
            ontology_mapping="nusy:PMBehavior-CreateFeature",
            cli_example="nusy create-feature --title 'My Feature'"
        )
        
        scenarios = strategy.generate_scenarios(behavior)
        
        assert len(scenarios) == 3
        assert scenarios[0].scenario_type == "happy_path"
        assert scenarios[1].scenario_type == "edge_case"
        assert scenarios[2].scenario_type == "error_handling"
    
    def test_scenario_has_required_steps(self):
        """Test that generated scenarios have all required Gherkin steps"""
        strategy = BottomUpStrategy()
        behavior = BehaviorSpec(
            name="test_tool",
            description="Test tool",
            capability_level="Apprentice",
            knowledge_scope="Pond",
            input_schema={"properties": {"param": {"type": "string"}}, "required": ["param"]},
            output_schema={"properties": {"result": {"type": "string"}}},
            mutates_kg=False,
            concurrency_safe=True,
            ontology_mapping="nusy:Test",
            cli_example="nusy test"
        )
        
        scenarios = strategy.generate_scenarios(behavior)
        
        for scenario in scenarios:
            assert len(scenario.given_steps) > 0, f"Scenario {scenario.scenario_name} missing Given steps"
            assert len(scenario.when_steps) > 0, f"Scenario {scenario.scenario_name} missing When steps"
            assert len(scenario.then_steps) > 0, f"Scenario {scenario.scenario_name} missing Then steps"
    
    def test_happy_path_includes_required_params(self):
        """Test that happy path scenario includes required parameters"""
        strategy = BottomUpStrategy()
        behavior = BehaviorSpec(
            name="create_feature",
            description="Create feature",
            capability_level="Journeyman",
            knowledge_scope="Lake",
            input_schema={
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["title", "description"]
            },
            output_schema={"properties": {"id": {"type": "string"}}},
            mutates_kg=True,
            concurrency_safe=False,
            ontology_mapping="nusy:Feature",
            cli_example="nusy create"
        )
        
        scenarios = strategy.generate_scenarios(behavior)
        happy_path = scenarios[0]
        
        # Should mention required parameters
        given_text = " ".join(happy_path.given_steps)
        assert "title" in given_text
        assert "description" in given_text
    
    def test_error_scenario_checks_missing_required(self):
        """Test that error scenario checks for missing required parameters"""
        strategy = BottomUpStrategy()
        behavior = BehaviorSpec(
            name="test_tool",
            description="Test",
            capability_level="Apprentice",
            knowledge_scope="Pond",
            input_schema={
                "properties": {"required_param": {"type": "string"}},
                "required": ["required_param"]
            },
            output_schema={"properties": {"result": {"type": "string"}}},
            mutates_kg=False,
            concurrency_safe=True,
            ontology_mapping="nusy:Test",
            cli_example="nusy test"
        )
        
        scenarios = strategy.generate_scenarios(behavior)
        error_scenario = scenarios[2]
        
        given_text = " ".join(error_scenario.given_steps)
        assert "missing" in given_text.lower() or "required_param" in given_text
    
    def test_generate_background(self):
        """Test background step generation"""
        strategy = BottomUpStrategy()
        behavior = BehaviorSpec(
            name="test_tool",
            description="Test",
            capability_level="Master",
            knowledge_scope="Sea",
            input_schema={"properties": {}},
            output_schema={"properties": {}},
            mutates_kg=False,
            concurrency_safe=True,
            ontology_mapping="nusy:Test",
            cli_example="nusy test"
        )
        
        background = strategy._generate_background(behavior)
        
        assert len(background) > 0
        assert any("MCP service" in step for step in background)
        assert any("Master" in step for step in background)


class TestFishnetV2:
    """Test FishnetV2 orchestrator"""
    
    @pytest.fixture
    def sample_behavior_markdown(self, tmp_path):
        """Create a sample behavior markdown file"""
        content = """---
source_id: test-behaviors
extraction_date: 2025-01-16
total_behaviors_extracted: 2
---

# Test Behaviors

## Category 1: Test

### Behavior 1.1: Test Query

**Name**: `test_query`  
**Description**: Query test data  
**Capability Level**: Apprentice  
**Knowledge Scope**: Pond  
**Mutates KG**: No  
**Concurrency Safe**: Yes

**Input Schema**:
```json
{
  "query": "string",
  "limit": "integer (optional)"
}
```

**Output Schema**:
```json
{
  "results": [{"id": "string"}],
  "count": "integer"
}
```

**Maps to Ontology**: `nusy:TestQuery`

**CLI Example**: `nusy test query --query "test"`

---

### Behavior 1.2: Test Create

**Name**: `test_create`  
**Description**: Create test item  
**Capability Level**: Journeyman  
**Knowledge Scope**: Lake  
**Mutates KG**: Yes  
**Concurrency Safe**: No

**Input Schema**:
```json
{
  "name": "string",
  "value": "string"
}
```

**Output Schema**:
```json
{
  "id": "string",
  "created_at": "timestamp"
}
```

**Maps to Ontology**: `nusy:TestCreate`

**CLI Example**: `nusy test create --name test`
"""
        behaviors_file = tmp_path / "test-behaviors.md"
        behaviors_file.write_text(content)
        return behaviors_file
    
    def test_load_behaviors(self, sample_behavior_markdown, tmp_path):
        """Test loading behaviors from markdown"""
        ontology_file = tmp_path / "ontology.ttl"
        ontology_file.write_text("# Empty ontology")
        output_dir = tmp_path / "output"
        
        fishnet = FishnetV2(
            behaviors_file=sample_behavior_markdown,
            ontology_file=ontology_file,
            output_dir=output_dir
        )
        
        behaviors = fishnet._load_behaviors()
        
        assert len(behaviors) == 2
        assert behaviors[0].name == "test_query"
        assert behaviors[1].name == "test_create"
        assert behaviors[0].capability_level == "Apprentice"
        assert behaviors[1].mutates_kg is True
    
    def test_parse_behavior_section(self, tmp_path):
        """Test parsing a single behavior section"""
        section = """
**Name**: `example_behavior`  
**Description**: This is an example  
**Capability Level**: Master  
**Knowledge Scope**: Sea  
**Mutates KG**: Yes  
**Concurrency Safe**: No

**Input Schema**:
```json
{
  "param1": "string"
}
```

**Output Schema**:
```json
{
  "result": "string"
}
```

**Maps to Ontology**: `nusy:Example`
**CLI Example**: `nusy example`
"""
        
        ontology_file = tmp_path / "ontology.ttl"
        ontology_file.write_text("# Empty")
        output_dir = tmp_path / "output"
        
        fishnet = FishnetV2(
            behaviors_file=tmp_path / "dummy.md",
            ontology_file=ontology_file,
            output_dir=output_dir
        )
        
        behavior = fishnet._parse_behavior_section(section, "test.md")
        
        assert behavior is not None
        assert behavior.name == "example_behavior"
        assert behavior.description == "This is an example"
        assert behavior.capability_level == "Master"
        assert behavior.knowledge_scope == "Sea"
    
    def test_generate_all_bdd_files(self, sample_behavior_markdown, tmp_path):
        """Test complete BDD file generation"""
        ontology_file = tmp_path / "ontology.ttl"
        ontology_file.write_text("# Empty ontology")
        output_dir = tmp_path / "output"
        
        fishnet = FishnetV2(
            behaviors_file=sample_behavior_markdown,
            ontology_file=ontology_file,
            output_dir=output_dir
        )
        
        results = fishnet.generate_all_bdd_files(strategy_names=["bottom_up"])
        
        assert results["total_behaviors"] == 2
        assert results["files_generated"] == 2
        assert results["scenarios_generated"] == 6  # 2 behaviors × 3 scenarios
        
        # Check files exist
        assert (output_dir / "test_query.feature").exists()
        assert (output_dir / "test_create.feature").exists()
    
    def test_feature_file_format(self, sample_behavior_markdown, tmp_path):
        """Test that generated feature files have correct Gherkin format"""
        ontology_file = tmp_path / "ontology.ttl"
        ontology_file.write_text("# Empty ontology")
        output_dir = tmp_path / "output"
        
        fishnet = FishnetV2(
            behaviors_file=sample_behavior_markdown,
            ontology_file=ontology_file,
            output_dir=output_dir
        )
        
        fishnet.generate_all_bdd_files(strategy_names=["bottom_up"])
        
        feature_file = output_dir / "test_query.feature"
        content = feature_file.read_text()
        
        # Check Gherkin structure
        assert "Feature: test_query" in content
        assert "Background:" in content
        assert "Scenario:" in content
        assert "Given" in content
        assert "When" in content
        assert "Then" in content
        
        # Check provenance comments
        assert "# Generated by Fishnet v2.0.0" in content
        assert "# Strategy:" in content
        
        # Check tags
        assert "@apprentice" in content.lower()
        assert "@pond" in content.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
