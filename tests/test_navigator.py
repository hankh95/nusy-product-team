"""Tests for Navigator - 10-Step Fishing Process Orchestrator"""

import json
import pytest
from pathlib import Path
from nusy_orchestrator.santiago_builder.navigator import (
    Navigator,
    NavigationStep,
    StepResult,
    ValidationCycle,
    ExpeditionLog
)


class TestNavigatorDataClasses:
    """Test data classes"""
    
    def test_step_result_creation(self):
        """Test StepResult can be created"""
        result = StepResult(
            step=NavigationStep.VISION,
            success=True,
            duration_minutes=1.5,
            outputs={"behaviors": 28}
        )
        assert result.step == NavigationStep.VISION
        assert result.success is True
        assert result.duration_minutes == 1.5
        assert result.outputs == {"behaviors": 28}
        assert result.errors == []
        assert result.warnings == []
    
    def test_validation_cycle_creation(self):
        """Test ValidationCycle can be created"""
        cycle = ValidationCycle(
            cycle_number=1,
            bdd_pass_rate=0.92,
            coverage_percent=0.88,
            kg_completeness=0.85,
            extraction_time_minutes=5.2,
            gaps_identified=["Gap 1", "Gap 2"],
            improvements_made=["Improvement 1"]
        )
        assert cycle.cycle_number == 1
        assert cycle.bdd_pass_rate == 0.92
        assert cycle.coverage_percent == 0.88
        assert cycle.kg_completeness == 0.85
        assert len(cycle.gaps_identified) == 2
        assert len(cycle.improvements_made) == 1
    
    def test_expedition_log_creation(self):
        """Test ExpeditionLog can be created"""
        log = ExpeditionLog(
            expedition_id="test-123",
            domain="test-domain",
            target_behaviors=28
        )
        assert log.expedition_id == "test-123"
        assert log.domain == "test-domain"
        assert log.target_behaviors == 28
        assert log.step_results == {}
        assert log.validation_cycles == []
        assert log.final_bdd_pass_rate == 0.0
        assert log.deployment_ready is False


class TestNavigatorInitialization:
    """Test Navigator initialization"""
    
    def test_navigator_creation(self, tmp_path):
        """Test Navigator can be created with required parameters"""
        navigator = Navigator(
            domain="test-domain",
            source_dir=tmp_path / "sources",
            output_dir=tmp_path / "output",
            ontology_file=tmp_path / "ontology.ttl"
        )
        
        assert navigator.domain == "test-domain"
        assert navigator.min_cycles == 3
        assert navigator.max_cycles == 5
        assert navigator.target_bdd_pass_rate == 0.95
        assert navigator.target_coverage == 0.95
        assert navigator.target_kg_completeness == 0.90
        assert navigator.log.domain == "test-domain"
    
    def test_navigator_custom_thresholds(self, tmp_path):
        """Test Navigator with custom quality thresholds"""
        navigator = Navigator(
            domain="test",
            source_dir=tmp_path / "src",
            output_dir=tmp_path / "out",
            ontology_file=tmp_path / "ont.ttl",
            min_cycles=4,
            max_cycles=6,
            target_bdd_pass_rate=0.98,
            target_coverage=0.96,
            target_kg_completeness=0.92
        )
        
        assert navigator.min_cycles == 4
        assert navigator.max_cycles == 6
        assert navigator.target_bdd_pass_rate == 0.98
        assert navigator.target_coverage == 0.96
        assert navigator.target_kg_completeness == 0.92


class TestNavigatorSteps:
    """Test individual Navigator steps"""
    
    @pytest.fixture
    def navigator(self, tmp_path):
        """Create a Navigator instance for testing"""
        source_dir = tmp_path / "sources"
        source_dir.mkdir()
        output_dir = tmp_path / "output"
        output_dir.mkdir()
        
        # Create dummy source files
        (source_dir / "doc1.md").write_text("# Test Document 1")
        (source_dir / "doc2.md").write_text("# Test Document 2")
        
        return Navigator(
            domain="test-domain",
            source_dir=source_dir,
            output_dir=output_dir,
            ontology_file=tmp_path / "ontology.ttl"
        )
    
    def test_step_1_vision(self, navigator):
        """Test Step 1: Vision"""
        navigator._step_1_vision()
        
        assert NavigationStep.VISION in navigator.log.step_results
        result = navigator.log.step_results[NavigationStep.VISION]
        assert result.success is True
        assert result.step == NavigationStep.VISION
        assert "target_behaviors" in result.outputs
    
    def test_step_2_raw_materials(self, navigator):
        """Test Step 2: Raw Materials"""
        navigator._step_2_raw_materials()
        
        assert NavigationStep.RAW_MATERIALS in navigator.log.step_results
        result = navigator.log.step_results[NavigationStep.RAW_MATERIALS]
        assert result.success is True
        assert result.step == NavigationStep.RAW_MATERIALS
        assert "source_files" in result.outputs
        assert result.outputs["source_files"] == 2  # We created 2 files
    
    def test_step_3_catchfish(self, navigator):
        """Test Step 3: Catchfish Extraction"""
        result = navigator._step_3_catchfish()
        
        assert result.success is True
        assert result.step == NavigationStep.CATCHFISH_EXTRACTION
        assert "entities_extracted" in result.outputs
        assert "relationships_extracted" in result.outputs
    
    def test_step_4_indexing(self, navigator):
        """Test Step 4: Indexing"""
        result = navigator._step_4_indexing()
        
        assert result.success is True
        assert result.step == NavigationStep.INDEXING
        assert "indices_built" in result.outputs
    
    def test_step_5_ontology(self, navigator):
        """Test Step 5: Ontology Loading"""
        result = navigator._step_5_ontology()
        
        assert result.success is True
        assert result.step == NavigationStep.ONTOLOGY_LOADING
        assert "ontology_file" in result.outputs
    
    def test_step_6_kg_building(self, navigator):
        """Test Step 6: KG Building"""
        result = navigator._step_6_kg_building()
        
        assert result.success is True
        assert result.step == NavigationStep.KG_BUILDING
        assert "triples_stored" in result.outputs
    
    def test_step_7_fishnet(self, navigator):
        """Test Step 7: Fishnet BDD Generation"""
        result = navigator._step_7_fishnet()
        
        assert result.success is True
        assert result.step == NavigationStep.FISHNET_BDD_GENERATION
        assert "files_generated" in result.outputs
    
    def test_step_9_deployment(self, navigator):
        """Test Step 9: Deployment"""
        # Add some validation cycles first
        navigator.log.validation_cycles.append(
            ValidationCycle(
                cycle_number=1,
                bdd_pass_rate=0.96,
                coverage_percent=0.96,
                kg_completeness=0.91,
                extraction_time_minutes=3.0,
                gaps_identified=[],
                improvements_made=[]
            )
        )
        navigator.log.final_bdd_pass_rate = 0.96
        navigator.log.final_coverage = 0.96
        
        navigator._step_9_deployment()
        
        assert NavigationStep.DEPLOYMENT in navigator.log.step_results
        result = navigator.log.step_results[NavigationStep.DEPLOYMENT]
        assert result.success is True
        assert "deployment_dir" in result.outputs
        assert "manifest_path" in result.outputs
        
        # Check that manifest was created
        manifest_path = Path(result.outputs["manifest_path"])
        assert manifest_path.exists()
        
        # Validate manifest structure
        with open(manifest_path) as f:
            manifest = json.load(f)
        assert "service" in manifest
        assert "capabilities" in manifest
        assert "tools" in manifest
        assert "metadata" in manifest
    
    def test_step_10_learning(self, navigator):
        """Test Step 10: Learning"""
        # Add some validation cycles first
        navigator.log.validation_cycles = [
            ValidationCycle(1, 0.88, 0.90, 0.85, 5.0, [], []),
            ValidationCycle(2, 0.92, 0.93, 0.88, 4.5, [], []),
            ValidationCycle(3, 0.96, 0.96, 0.91, 4.0, [], [])
        ]
        
        navigator._step_10_learning()
        
        assert NavigationStep.LEARNING in navigator.log.step_results
        result = navigator.log.step_results[NavigationStep.LEARNING]
        assert result.success is True


class TestValidationLoop:
    """Test validation loop functionality"""
    
    @pytest.fixture
    def navigator(self, tmp_path):
        """Create a Navigator instance"""
        source_dir = tmp_path / "sources"
        source_dir.mkdir()
        (source_dir / "test.md").write_text("# Test")
        
        return Navigator(
            domain="test",
            source_dir=source_dir,
            output_dir=tmp_path / "output",
            ontology_file=tmp_path / "ont.ttl",
            min_cycles=3,
            max_cycles=5
        )
    
    def test_run_bdd_tests_metrics(self, navigator):
        """Test BDD test metrics generation"""
        metrics = navigator._run_bdd_tests(cycle_num=1)
        
        assert "pass_rate" in metrics
        assert "coverage" in metrics
        assert "completeness" in metrics
        assert "gaps" in metrics
        assert "improvements" in metrics
        
        # First cycle should have lower metrics
        assert 0.80 <= metrics["pass_rate"] <= 0.90
    
    def test_run_bdd_tests_improvement(self, navigator):
        """Test BDD metrics improve over cycles"""
        cycle1_metrics = navigator._run_bdd_tests(cycle_num=1)
        cycle3_metrics = navigator._run_bdd_tests(cycle_num=3)
        
        # Metrics should improve
        assert cycle3_metrics["pass_rate"] > cycle1_metrics["pass_rate"]
        assert cycle3_metrics["coverage"] > cycle1_metrics["coverage"]
    
    def test_check_quality_gates_passing(self, navigator):
        """Test quality gates with passing metrics"""
        navigator.log.validation_cycles = [
            ValidationCycle(1, 0.96, 0.96, 0.91, 3.0, [], []),
            ValidationCycle(2, 0.96, 0.96, 0.91, 2.5, [], []),
            ValidationCycle(3, 0.96, 0.96, 0.91, 2.0, [], [])
        ]
        
        assert navigator._check_quality_gates() is True
    
    def test_check_quality_gates_failing_bdd(self, navigator):
        """Test quality gates with failing BDD rate"""
        navigator.log.validation_cycles = [
            ValidationCycle(1, 0.92, 0.96, 0.91, 3.0, [], []),
            ValidationCycle(2, 0.93, 0.96, 0.91, 2.5, [], []),
            ValidationCycle(3, 0.94, 0.96, 0.91, 2.0, [], [])
        ]
        
        # BDD pass rate below 0.95
        assert navigator._check_quality_gates() is False
    
    def test_check_quality_gates_insufficient_cycles(self, navigator):
        """Test quality gates with insufficient cycles"""
        navigator.log.validation_cycles = [
            ValidationCycle(1, 0.96, 0.96, 0.91, 3.0, [], []),
            ValidationCycle(2, 0.96, 0.96, 0.91, 2.5, [], [])
        ]
        
        # Only 2 cycles, need at least 3
        assert navigator._check_quality_gates() is False


class TestFullExpedition:
    """Test complete expedition flow"""
    
    def test_run_expedition_success(self, tmp_path):
        """Test running a complete expedition"""
        source_dir = tmp_path / "sources"
        source_dir.mkdir()
        (source_dir / "doc.md").write_text("# Test Document")
        
        navigator = Navigator(
            domain="test-expedition",
            source_dir=source_dir,
            output_dir=tmp_path / "output",
            ontology_file=tmp_path / "ontology.ttl",
            min_cycles=3,
            max_cycles=3  # Limit to 3 for faster test
        )
        
        log = navigator.run_expedition()
        
        # Check expedition log
        assert log.domain == "test-expedition"
        assert len(log.validation_cycles) >= 3
        assert log.final_bdd_pass_rate > 0
        assert log.final_coverage > 0
        
        # Check step results recorded
        assert NavigationStep.VISION in log.step_results
        assert NavigationStep.RAW_MATERIALS in log.step_results
        assert NavigationStep.DEPLOYMENT in log.step_results
        assert NavigationStep.LEARNING in log.step_results
        
        # Check expedition log saved
        ships_logs_dir = Path("santiago-pm/ships-logs")
        log_files = list(ships_logs_dir.glob(f"{log.expedition_id}.md"))
        assert len(log_files) == 1
    
    def test_expedition_reaches_quality_gates(self, tmp_path):
        """Test expedition stops when quality gates met"""
        source_dir = tmp_path / "sources"
        source_dir.mkdir()
        (source_dir / "doc.md").write_text("# Test")
        
        navigator = Navigator(
            domain="test",
            source_dir=source_dir,
            output_dir=tmp_path / "output",
            ontology_file=tmp_path / "ont.ttl",
            min_cycles=3,
            max_cycles=5
        )
        
        log = navigator.run_expedition()
        
        # Should stop at 4 cycles when quality gates met
        # (cycle 1: 88%, cycle 2: 91%, cycle 3: 94%, cycle 4: 97%)
        assert 3 <= len(log.validation_cycles) <= 4
        assert log.final_bdd_pass_rate >= 0.95


class TestCLI:
    """Test CLI interface"""
    
    def test_main_function_exists(self):
        """Test that main() function exists"""
        from nusy_orchestrator.santiago_builder.navigator import main
        assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
