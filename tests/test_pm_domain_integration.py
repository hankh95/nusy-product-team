"""
Integration tests for PM Domain Synthesis

These tests validate the complete PM domain expert system including knowledge synthesis,
behavior execution, and autonomous learning cycles.
"""

import pytest
import asyncio
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent / "domains" / "pm-expert"))

from nusy_pm_core.adapters.agent_adapter import AgentAdapter
from models.pm_domain_model import initialize_core_pm_knowledge, PMMethodology
from models.knowledge_graph import create_pm_knowledge_graph
from models.pm_behaviors import PMServiceBehaviors
from models.ethical_framework import get_ethical_framework, BahaiPrinciple


class TestPMDomainSynthesis:
    """Integration tests for complete PM domain synthesis."""
    
    @pytest.fixture
    def pm_domain_system(self):
        """Create complete PM domain system."""
        # Initialize knowledge
        ontology = initialize_core_pm_knowledge()
        knowledge_graph = create_pm_knowledge_graph(ontology)
        
        # Initialize agents
        agent_adapter = AgentAdapter()
        
        # Initialize PM behaviors
        pm_behaviors = PMServiceBehaviors(agent_adapter, knowledge_graph)
        
        # Initialize ethical framework
        ethical_framework = get_ethical_framework()
        
        return {
            'ontology': ontology,
            'knowledge_graph': knowledge_graph,
            'agent_adapter': agent_adapter,
            'pm_behaviors': pm_behaviors,
            'ethical_framework': ethical_framework
        }
    
    def test_knowledge_ontology_initialization(self, pm_domain_system):
        """Test that PM knowledge ontology initializes correctly."""
        ontology = pm_domain_system['ontology']
        
        # Verify core concepts exist
        assert 'agile_manifesto' in ontology.concepts
        assert 'scrum_framework' in ontology.concepts
        assert 'lean_ux' in ontology.concepts
        assert 'user_story_mapping' in ontology.concepts
        
        # Verify methodologies
        assert PMMethodology.AGILE in ontology.methodologies
        assert PMMethodology.SCRUM in ontology.methodologies
        assert PMMethodology.LEAN_UX in ontology.methodologies
        
        # Verify knowledge sources
        assert 'jeff_patton' in ontology.knowledge_sources
        assert 'jeff_gothelf' in ontology.knowledge_sources
    
    def test_knowledge_graph_structure(self, pm_domain_system):
        """Test that knowledge graph is properly structured."""
        kg = pm_domain_system['knowledge_graph']
        
        # Get statistics
        stats = kg.get_statistics()
        assert stats['concepts'] > 0
        assert stats['methodologies'] > 0
        
        # Test concept retrieval
        agile_info = kg.get_concept_info('agile_manifesto')
        assert agile_info is not None
        assert agile_info['name'] == 'Agile Manifesto'
        assert len(agile_info['related']) > 0
    
    def test_ethical_framework_principles(self, pm_domain_system):
        """Test that ethical framework has all Baha'i principles."""
        framework = pm_domain_system['ethical_framework']
        
        # Verify all principles exist
        assert BahaiPrinciple.SERVICE_TO_HUMANITY in framework.principles
        assert BahaiPrinciple.UNITY_IN_DIVERSITY in framework.principles
        assert BahaiPrinciple.CONSULTATION in framework.principles
        assert BahaiPrinciple.PROGRESSIVE_REVELATION in framework.principles
        assert BahaiPrinciple.ELIMINATION_OF_PREJUDICE in framework.principles
        assert BahaiPrinciple.JUSTICE in framework.principles
        assert BahaiPrinciple.TRUSTWORTHINESS in framework.principles
        
        # Test getting principle guidance
        service_principle = framework.get_principle_guidance(BahaiPrinciple.SERVICE_TO_HUMANITY)
        assert service_principle is not None
        assert len(service_principle.validation_questions) > 0
    
    @pytest.mark.asyncio
    async def test_agent_availability(self, pm_domain_system):
        """Test that required agents are available."""
        agent_adapter = pm_domain_system['agent_adapter']
        
        # List available agents
        agents = await agent_adapter.list_available_agents()
        
        # Verify required agents
        assert 'quartermaster' in agents
        assert 'pilot' in agents
        assert 'santiago' in agents
        
        # Verify agent status
        quartermaster_status = await agent_adapter.get_agent_status('quartermaster')
        assert quartermaster_status is not None
        assert quartermaster_status['role'] == 'Ethicist'
        
        pilot_status = await agent_adapter.get_agent_status('pilot')
        assert pilot_status is not None
        assert pilot_status['role'] == 'PM Expert'
    
    @pytest.mark.asyncio
    async def test_sprint_planning_behavior(self, pm_domain_system):
        """Test sprint planning PM behavior."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute sprint planning
        result = await pm_behaviors.facilitate_sprint_planning(
            team_velocity=30,
            backlog_items=[
                {'id': 'item-1', 'title': 'User authentication', 'points': 5},
                {'id': 'item-2', 'title': 'Dashboard UI', 'points': 8},
                {'id': 'item-3', 'title': 'Data export', 'points': 3}
            ],
            sprint_goal="Implement core user features"
        )
        
        # Verify result
        assert result is not None
        assert result['status'] == 'completed'
        assert 'planning_guidance' in result
        assert 'ethical_review' in result
        assert len(result['planning_guidance']) > 50
    
    @pytest.mark.asyncio
    async def test_retrospective_behavior(self, pm_domain_system):
        """Test retrospective PM behavior."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute retrospective
        result = await pm_behaviors.conduct_retrospective(
            sprint_id="sprint-001",
            team_feedback=["Good collaboration", "Need better documentation"],
            metrics={'velocity': 28, 'quality': 0.92}
        )
        
        # Verify result
        assert result is not None
        assert result['status'] == 'completed'
        assert 'retrospective_guidance' in result
        assert 'ethical_review' in result
    
    @pytest.mark.asyncio
    async def test_backlog_refinement_behavior(self, pm_domain_system):
        """Test backlog refinement PM behavior."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute backlog refinement
        result = await pm_behaviors.refine_backlog(
            backlog_items=[
                {'id': f'item-{i}', 'title': f'Feature {i}'}
                for i in range(15)
            ],
            prioritization_criteria={'value': 'high', 'risk': 'medium'}
        )
        
        # Verify result
        assert result is not None
        assert result['status'] == 'completed'
        assert 'refinement_guidance' in result
    
    @pytest.mark.asyncio
    async def test_risk_assessment_behavior(self, pm_domain_system):
        """Test risk assessment PM behavior."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute risk assessment
        result = await pm_behaviors.assess_risks(
            project_context={
                'timeline': '3 months',
                'team_size': 5,
                'complexity': 'high'
            },
            known_risks=[
                {'risk': 'Technical debt', 'impact': 'medium'}
            ]
        )
        
        # Verify result
        assert result is not None
        assert result['status'] == 'completed'
        assert 'risk_analysis' in result
        assert 'ethical_review' in result
    
    @pytest.mark.asyncio
    async def test_user_story_mapping_behavior(self, pm_domain_system):
        """Test user story mapping PM behavior."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute user story mapping
        result = await pm_behaviors.facilitate_user_story_mapping(
            user_journey="User needs to complete tasks efficiently",
            existing_stories=[
                {'id': f'story-{i}', 'title': f'Story {i}'}
                for i in range(10)
            ]
        )
        
        # Verify result
        assert result is not None
        assert result['status'] == 'completed'
        assert 'mapping_guidance' in result
    
    @pytest.mark.asyncio
    async def test_discovery_session_behavior(self, pm_domain_system):
        """Test continuous discovery PM behavior."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute discovery session
        result = await pm_behaviors.conduct_discovery_session(
            hypothesis="Users want faster task creation",
            research_questions=[
                "What are current pain points?",
                "How do users create tasks now?"
            ]
        )
        
        # Verify result
        assert result is not None
        assert result['status'] == 'completed'
        assert 'discovery_guidance' in result
        assert 'ethical_review' in result
    
    @pytest.mark.asyncio
    async def test_complete_pm_cycle(self, pm_domain_system):
        """Test a complete PM cycle with multiple behaviors."""
        pm_behaviors = pm_domain_system['pm_behaviors']
        
        # Execute complete cycle
        results = []
        
        # 1. Sprint planning
        planning_result = await pm_behaviors.facilitate_sprint_planning(
            team_velocity=25,
            backlog_items=[{'id': f'item-{i}', 'points': 5} for i in range(8)],
            sprint_goal="Test complete cycle"
        )
        results.append(planning_result)
        
        # 2. Backlog refinement
        refinement_result = await pm_behaviors.refine_backlog(
            backlog_items=[{'id': f'item-{i}'} for i in range(10)],
            prioritization_criteria={'value': 'high'}
        )
        results.append(refinement_result)
        
        # 3. Retrospective
        retro_result = await pm_behaviors.conduct_retrospective(
            sprint_id="test-sprint",
            team_feedback=["Cycle completed successfully"],
            metrics={'velocity': 25}
        )
        results.append(retro_result)
        
        # Verify all behaviors completed
        assert all(r['status'] == 'completed' for r in results)
        
        # Verify behavior history
        history = pm_behaviors.get_behavior_history()
        assert len(history) >= 3
        
        # Verify statistics
        stats = pm_behaviors.get_behavior_statistics()
        assert stats.get('sprint_planning', 0) > 0
        assert stats.get('backlog_refinement', 0) > 0
        assert stats.get('retrospective', 0) > 0
    
    def test_knowledge_graph_export(self, pm_domain_system, tmp_path):
        """Test knowledge graph export to TTL format."""
        kg = pm_domain_system['knowledge_graph']
        
        # Export to file
        export_path = tmp_path / "pm_knowledge.ttl"
        kg.export_to_ttl(str(export_path))
        
        # Verify file exists and has content
        assert export_path.exists()
        assert export_path.stat().st_size > 0
        
        # Verify can import back
        from models.knowledge_graph import PMKnowledgeGraph
        new_kg = PMKnowledgeGraph()
        new_kg.import_from_ttl(str(export_path))
        
        # Verify imported graph has concepts
        new_stats = new_kg.get_statistics()
        assert new_stats['concepts'] > 0


class TestPMDomainAutonomousLearning:
    """Tests for autonomous learning capabilities."""
    
    @pytest.mark.asyncio
    async def test_learning_from_behavior_execution(self):
        """Test that system learns from behavior execution."""
        # Initialize system
        ontology = initialize_core_pm_knowledge()
        kg = create_pm_knowledge_graph(ontology)
        agent_adapter = AgentAdapter()
        pm_behaviors = PMServiceBehaviors(agent_adapter, kg)
        
        # Execute multiple iterations
        for i in range(3):
            await pm_behaviors.facilitate_sprint_planning(
                team_velocity=30,
                backlog_items=[{'id': f'item-{i}-{j}'} for j in range(5)],
                sprint_goal=f"Iteration {i+1}"
            )
        
        # Verify learning through behavior history
        history = pm_behaviors.get_behavior_history()
        assert len(history) >= 3
        
        # Verify patterns in execution
        stats = pm_behaviors.get_behavior_statistics()
        assert stats['sprint_planning'] >= 3
    
    @pytest.mark.asyncio
    async def test_ethical_oversight_in_all_behaviors(self):
        """Test that ethical oversight is applied to all behaviors."""
        ontology = initialize_core_pm_knowledge()
        kg = create_pm_knowledge_graph(ontology)
        agent_adapter = AgentAdapter()
        pm_behaviors = PMServiceBehaviors(agent_adapter, kg)
        
        # Execute behaviors that require ethical review
        behaviors_to_test = [
            pm_behaviors.facilitate_sprint_planning(team_velocity=30, backlog_items=[]),
            pm_behaviors.conduct_retrospective(sprint_id="test", team_feedback=[]),
            pm_behaviors.assess_risks(project_context={'test': True}),
            pm_behaviors.conduct_discovery_session(hypothesis="test"),
            pm_behaviors.manage_stakeholders(stakeholders=[])
        ]
        
        results = await asyncio.gather(*behaviors_to_test)
        
        # Verify all have ethical reviews
        for result in results:
            assert 'ethical_review' in result
            assert len(result['ethical_review']) > 0
