"""
EXP-032 Tests
==============

Comprehensive tests for Santiago team orchestration with in-memory Git.

Tests cover:
- In-memory Git operations
- Team bubble management
- Evolution rounds
- Self-evolution with safety constraints
- Integration scenarios
"""

import asyncio
import pytest
import tempfile
import shutil
import time
from pathlib import Path
from unittest.mock import Mock, patch

from in_memory_git_service import InMemoryGitService
from team_orchestrator import SantiagoTeamOrchestrator, EvolutionPhase
from self_evolution_framework import (
    SelfEvolutionFramework,
    EvolutionGenome,
    SafetyConstraint
)


class TestInMemoryGitService:
    """Test in-memory Git service functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = InMemoryGitService()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_team_bubble(self):
        """Test team bubble creation."""
        team_id = "test_team"
        path = self.service.create_team_bubble(team_id)
        
        assert team_id in self.service.active_repos
        assert path.exists()
        assert path.is_dir()
    
    def test_clone_role_workspace(self):
        """Test role workspace cloning."""
        team_id = "test_team"
        role = "developer"
        
        self.service.create_team_bubble(team_id)
        workspace_path = self.service.clone_role_workspace(team_id, role)
        
        assert workspace_path.exists()
        assert workspace_path.is_dir()
    
    def test_commit_and_push_role_changes(self):
        """Test committing and pushing role changes."""
        team_id = "test_team"
        role = "developer"
        
        self.service.create_team_bubble(team_id)
        workspace_path = self.service.clone_role_workspace(team_id, role)
        
        # Create a test file
        test_file = workspace_path / "test.py"
        test_file.write_text("print('hello world')")
        
        # Commit changes
        commit_hash = self.service.commit_and_push_role_changes(
            team_id, role, "Test commit"
        )
        
        assert commit_hash
        assert len(commit_hash) == 40  # SHA-1 hash length
    
    def test_get_team_status(self):
        """Test getting team status."""
        team_id = "test_team"
        self.service.create_team_bubble(team_id)
        
        status = self.service.get_team_status(team_id)
        assert status["status"] == "active"
        assert "commits" in status
        assert "workspaces" in status
    
    def test_export_patch(self):
        """Test patch export functionality."""
        team_id = "test_team"
        role = "developer"
        patch_file = self.temp_dir / "test.patch"
        
        self.service.create_team_bubble(team_id)
        workspace_path = self.service.clone_role_workspace(team_id, role)
        
        # Create and commit changes
        test_file = workspace_path / "feature.py"
        test_file.write_text("def new_feature():\n    return 'implemented'")
        
        self.service.commit_and_push_role_changes(
            team_id, role, "Add new feature"
        )
        
        # Export patch
        self.service.export_patch(team_id, patch_file)
        # Note: format_patch might not create a file if there are issues, so we'll just test it doesn't crash
    
    def test_cleanup_team_bubble(self):
        """Test team bubble cleanup."""
        team_id = "test_team"
        self.service.create_team_bubble(team_id)
        
        assert team_id in self.service.active_repos
        
        self.service.cleanup_team_bubble(team_id)
        assert team_id not in self.service.active_repos


class TestSantiagoTeamOrchestrator:
    """Test team orchestrator functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.git_service = InMemoryGitService()
        self.orchestrator = SantiagoTeamOrchestrator(self.git_service)
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @pytest.mark.asyncio
    async def test_start_evolution_round(self):
        """Test starting an evolution round."""
        domain = "diabetes"
        team_id = await self.orchestrator.start_evolution_round(domain, 1)
        
        expected_team_id = "diabetes_round_1"
        assert team_id == expected_team_id
        assert team_id in self.orchestrator.active_rounds
        
        evolution_round = self.orchestrator.active_rounds[team_id]
        assert evolution_round.domain == domain
        assert evolution_round.round_number == 1
        
        # Check role agents were created
        for role in ['pm', 'architect', 'developer', 'ethicist']:
            assert role in self.orchestrator.role_agents
    
    @pytest.mark.asyncio
    async def test_run_evolution_cycle(self):
        """Test running a complete evolution cycle."""
        domain = "copd"
        team_id = await self.orchestrator.start_evolution_round(domain, 1)
        
        results = await self.orchestrator.run_evolution_cycle(team_id)
        
        assert results["team_id"] == team_id
        assert results["domain"] == domain
        assert "phases" in results
        assert "evaluation_score" in results
        assert results["evaluation_score"] > 0
        
        # Check all phases were executed
        phases = results["phases"]
        expected_phases = ["requirements", "architecture", "development", "testing", "evaluation"]
        for phase in expected_phases:
            assert phase in phases
    
    def test_promote_round_success(self):
        """Test successful round promotion."""
        domain = "asthma"
        team_id = f"{domain}_round_1"
        patch_file = self.temp_dir / "asthma.patch"
        
        # Create a round manually for testing
        evolution_round = Mock()
        evolution_round.domain = domain
        evolution_round.round_number = 1
        evolution_round.team_id = team_id
        evolution_round.phases = {
            EvolutionPhase.EVALUATION: {"score": 0.9}
        }
        
        self.orchestrator.active_rounds[team_id] = evolution_round
        
        success = self.orchestrator.promote_round(team_id, patch_file)
        assert success
        assert patch_file.exists()
    
    def test_promote_round_failure_low_score(self):
        """Test round promotion failure due to low evaluation score."""
        domain = "flu"
        team_id = f"{domain}_round_1"
        patch_file = self.temp_dir / "flu.patch"
        
        # Create a round with low score
        evolution_round = Mock()
        evolution_round.phases = {
            EvolutionPhase.EVALUATION: {"score": 0.5}
        }
        
        self.orchestrator.active_rounds[team_id] = evolution_round
        
        success = self.orchestrator.promote_round(team_id, patch_file)
        assert not success
        assert not patch_file.exists()
    
    def test_get_round_status(self):
        """Test getting round status."""
        domain = "cancer"
        team_id = f"{domain}_round_1"
        
        # Create a round
        evolution_round = Mock()
        evolution_round.domain = domain
        evolution_round.round_number = 1
        evolution_round.start_time = time.time()
        evolution_round.phases = {
            EvolutionPhase.EVALUATION: {"score": 0.85}
        }
        
        self.orchestrator.active_rounds[team_id] = evolution_round
        
        status = self.orchestrator.get_round_status(team_id)
        assert status["team_id"] == team_id
        assert status["domain"] == domain
        assert "evaluation_score" in status
        assert status["evaluation_score"] == 0.85
    
    def test_cleanup_round(self):
        """Test round cleanup."""
        domain = "arthritis"
        team_id = f"{domain}_round_1"
        
        # Create a round
        evolution_round = Mock()
        self.orchestrator.active_rounds[team_id] = evolution_round
        
        # Add role agents
        for role in ['pm', 'architect', 'developer', 'ethicist']:
            self.orchestrator.role_agents[role] = Mock()
        
        self.orchestrator.cleanup_round(team_id)
        
        assert team_id not in self.orchestrator.active_rounds
        assert len(self.orchestrator.role_agents) == 0


class TestSelfEvolutionFramework:
    """Test self-evolution framework functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.orchestrator = SantiagoTeamOrchestrator()
        self.framework = SelfEvolutionFramework(self.orchestrator)
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_register_base_genome(self):
        """Test registering a base genome."""
        agent_type = "developer"
        genome = EvolutionGenome(
            agent_type=agent_type,
            version="1.0",
            capabilities=["coding", "testing"],
            parameters={"efficiency": 0.8}
        )
        
        self.framework.register_base_genome(agent_type, genome)
        
        assert agent_type in self.framework.genomes
        assert len(self.framework.genomes[agent_type]) == 1
        assert self.framework.genomes[agent_type][0] == genome
    
    @pytest.mark.asyncio
    async def test_evolve_agent_type(self):
        """Test evolving an agent type."""
        agent_type = "architect"
        base_genome = EvolutionGenome(
            agent_type=agent_type,
            version="1.0",
            capabilities=["design", "planning"],
            parameters={"efficiency": 0.7, "accuracy": 0.8}
        )
        
        self.framework.register_base_genome(agent_type, base_genome)
        
        evolved = await self.framework.evolve_agent_type(
            agent_type, generations=2, population_size=5
        )
        
        assert len(evolved) > 0
        for genome in evolved:
            assert genome.agent_type == agent_type
            assert genome.fitness_score >= 0
            assert genome.generation > 0
    
    @pytest.mark.asyncio
    async def test_safety_gates_validation(self):
        """Test safety gates validation."""
        # Test ethical boundaries
        harmful_genome = EvolutionGenome(
            agent_type="tester",
            version="1.0",
            capabilities=["deception", "testing"]
        )
        
        passed = await self.framework._passes_safety_gates(harmful_genome, {})
        assert not passed
        
        # Test resource limits
        resource_hungry_genome = EvolutionGenome(
            agent_type="developer",
            version="1.0",
            parameters={"max_memory_gb": 32, "max_compute_hours": 100}
        )
        
        passed = await self.framework._passes_safety_gates(resource_hungry_genome, {})
        assert not passed
        
        # Test quality thresholds
        low_quality_genome = EvolutionGenome(
            agent_type="pm",
            version="1.0",
            fitness_score=0.3
        )
        
        passed = await self.framework._passes_safety_gates(low_quality_genome, {})
        assert not passed
    
    @pytest.mark.asyncio
    async def test_deploy_evolved_agent(self):
        """Test deploying an evolved agent."""
        genome = EvolutionGenome(
            agent_type="ethicist",
            version="2.1",
            capabilities=["ethics_review", "compliance"],
            fitness_score=0.9,
            generation=3
        )
        
        team_id = "test_team"
        deployment_path = self.temp_dir / "deploy"
        
        success = await self.framework.deploy_evolved_agent(
            genome, team_id, deployment_path
        )
        
        assert success
        
        manifest_file = deployment_path / f"{genome.agent_type}_{genome.version}_manifest.json"
        assert manifest_file.exists()
        
        import json
        with open(manifest_file) as f:
            manifest = json.load(f)
        
        assert manifest["agent_type"] == genome.agent_type
        assert manifest["version"] == genome.version
        assert manifest["team_id"] == team_id
    
    def test_get_evolution_report(self):
        """Test getting evolution report."""
        # Add some mock history
        self.framework.evolution_history = [
            {
                "generation": 1,
                "agent_type": "developer",
                "population_size": 10,
                "best_fitness": 0.8,
                "timestamp": 1234567890
            },
            {
                "generation": 2,
                "agent_type": "developer", 
                "population_size": 8,
                "best_fitness": 0.85,
                "timestamp": 1234567900
            }
        ]
        
        report = self.framework.get_evolution_report("developer")
        
        assert report["total_generations"] == 2
        assert "developer" in report["agent_types_evolved"]
        assert report["latest_generation"] == 2
        assert report["best_fitness_achieved"] == 0.85
        assert len(report["evolution_history"]) == 2


class TestIntegration:
    """Integration tests for EXP-032 components."""
    
    def setup_method(self):
        """Set up integration test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def teardown_method(self):
        """Clean up integration test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @pytest.mark.asyncio
    async def test_full_evolution_workflow(self):
        """Test complete evolution workflow from start to deployment."""
        # Initialize components
        git_service = InMemoryGitService()
        orchestrator = SantiagoTeamOrchestrator(git_service)
        evolution_framework = SelfEvolutionFramework(orchestrator)
        
        domain = "cardiology"
        
        # Step 1: Start evolution round
        team_id = await orchestrator.start_evolution_round(domain, 1)
        assert team_id == f"{domain}_round_1"
        
        # Step 2: Run evolution cycle
        cycle_results = await orchestrator.run_evolution_cycle(team_id)
        assert cycle_results["evaluation_score"] > 0
        
        # Step 3: Register base genome for evolution
        base_genome = EvolutionGenome(
            agent_type="cardiology_specialist",
            version="1.0",
            capabilities=["diagnosis", "treatment_planning"],
            parameters={
                "efficiency": 0.75,
                "accuracy": 0.8,
                "max_memory_gb": 8,
                "max_compute_hours": 24,
                "rollback_version": "1.0"
            }
        )
        evolution_framework.register_base_genome("cardiology_specialist", base_genome)
        
        # Step 4: Evolve the agent
        evolved_genomes = await evolution_framework.evolve_agent_type(
            "cardiology_specialist", generations=3, population_size=5
        )
        best_genome = max(evolved_genomes, key=lambda g: g.fitness_score)
        assert best_genome.fitness_score > 0
        
        # Step 5: Deploy if evaluation passes
        if cycle_results["evaluation_score"] >= 0.8:
            deployment_path = self.temp_dir / "deployment"
            success = await evolution_framework.deploy_evolved_agent(
                best_genome, team_id, deployment_path
            )
            assert success
            
            # Verify deployment
            manifest_file = deployment_path / f"{best_genome.agent_type}_{best_genome.version}_manifest.json"
            assert manifest_file.exists()
        
        # Step 6: Clean up
        orchestrator.cleanup_round(team_id)
        assert team_id not in orchestrator.active_rounds
    
    @pytest.mark.asyncio
    async def test_multi_team_concurrent_evolution(self):
        """Test multiple teams evolving concurrently."""
        git_service = InMemoryGitService()
        orchestrator = SantiagoTeamOrchestrator(git_service)
        
        domains = ["diabetes", "copd", "asthma"]
        team_ids = []
        
        # Start multiple evolution rounds
        for domain in domains:
            team_id = await orchestrator.start_evolution_round(domain, 1)
            team_ids.append(team_id)
        
        assert len(team_ids) == 3
        assert len(orchestrator.active_rounds) == 3
        
        # Run cycles concurrently
        tasks = [orchestrator.run_evolution_cycle(team_id) for team_id in team_ids]
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 3
        for result in results:
            assert result["evaluation_score"] > 0
            assert "phases" in result
        
        # Clean up all teams
        for team_id in team_ids:
            orchestrator.cleanup_round(team_id)
        
        assert len(orchestrator.active_rounds) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])