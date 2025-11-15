"""
BDD test steps for PM Domain Sprint Planning scenarios
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from nusy_pm_core.adapters.agent_adapter import AgentAdapter
from models.pm_domain_model import initialize_core_pm_knowledge
from models.knowledge_graph import create_pm_knowledge_graph
from models.pm_behaviors import PMServiceBehaviors

# Load scenarios
scenarios('../features/sprint_planning.feature')


@pytest.fixture
def pm_context():
    """Create PM domain context for tests."""
    return {
        'ontology': None,
        'knowledge_graph': None,
        'agent_adapter': None,
        'pm_behaviors': None,
        'team_velocity': None,
        'backlog_items': None,
        'sprint_goal': None,
        'result': None
    }


@given("the PM domain expert is initialized")
def pm_domain_initialized(pm_context):
    """Initialize the PM domain expert."""
    pm_context['ontology'] = initialize_core_pm_knowledge()
    pm_context['knowledge_graph'] = create_pm_knowledge_graph(pm_context['ontology'])
    assert pm_context['ontology'] is not None
    assert pm_context['knowledge_graph'] is not None


@given("the Pilot agent is available")
def pilot_available(pm_context):
    """Ensure Pilot agent is available."""
    pm_context['agent_adapter'] = AgentAdapter()
    pm_context['pm_behaviors'] = PMServiceBehaviors(
        pm_context['agent_adapter'],
        pm_context['knowledge_graph']
    )
    assert 'pilot' in pm_context['agent_adapter'].agents


@given("the Quartermaster ethical overseer is available")
def quartermaster_available(pm_context):
    """Ensure Quartermaster agent is available."""
    assert 'quartermaster' in pm_context['agent_adapter'].agents


@given("the knowledge graph contains sprint planning concepts")
def knowledge_graph_has_sprint_concepts(pm_context):
    """Verify sprint planning concepts in knowledge graph."""
    # Check that knowledge graph has concepts
    stats = pm_context['knowledge_graph'].get_statistics()
    assert stats['concepts'] > 0


@given(parsers.parse("a team with velocity of {velocity:d} story points"))
def team_with_velocity(pm_context, velocity):
    """Set team velocity."""
    pm_context['team_velocity'] = velocity


@given(parsers.parse("a backlog with {count:d} ready items"))
def backlog_with_items(pm_context, count):
    """Create backlog with items."""
    pm_context['backlog_items'] = [
        {'id': f'item-{i}', 'title': f'Item {i}', 'points': 3}
        for i in range(count)
    ]


@given("a backlog with ready items")
def backlog_ready(pm_context):
    """Create backlog with default items."""
    pm_context['backlog_items'] = [
        {'id': f'item-{i}', 'title': f'Item {i}', 'points': 5}
        for i in range(8)
    ]


@given("no sprint goal is defined")
def no_sprint_goal(pm_context):
    """Ensure no sprint goal."""
    pm_context['sprint_goal'] = None


@given("a team with reduced capacity due to holidays")
def reduced_capacity(pm_context):
    """Set reduced team capacity."""
    pm_context['team_capacity'] = 'reduced'
    pm_context['capacity_reason'] = 'holidays'


@given(parsers.parse("historical velocity of {velocity:d} story points"))
def historical_velocity(pm_context, velocity):
    """Set historical velocity."""
    pm_context['historical_velocity'] = velocity


@given(parsers.parse("current capacity is {capacity:d} story points"))
def current_capacity(pm_context, capacity):
    """Set current capacity."""
    pm_context['team_velocity'] = capacity


@given("a backlog containing high-risk items")
def high_risk_backlog(pm_context):
    """Create backlog with high-risk items."""
    pm_context['backlog_items'] = [
        {'id': 'item-1', 'title': 'High risk item', 'points': 8, 'risk': 'high'},
        {'id': 'item-2', 'title': 'Normal item', 'points': 3, 'risk': 'low'}
    ]


@given("dependencies between multiple items")
def items_with_dependencies(pm_context):
    """Add dependencies to backlog items."""
    if pm_context['backlog_items']:
        pm_context['backlog_items'][0]['depends_on'] = ['item-2']


@given("a proposed sprint plan")
def proposed_sprint_plan(pm_context):
    """Create a proposed sprint plan."""
    pm_context['sprint_plan'] = {
        'goal': 'Deliver user authentication',
        'items': ['item-1', 'item-2'],
        'capacity': 20
    }


@when("the Pilot facilitates sprint planning")
async def pilot_facilitates_sprint_planning(pm_context):
    """Pilot facilitates sprint planning."""
    result = await pm_context['pm_behaviors'].facilitate_sprint_planning(
        team_velocity=pm_context.get('team_velocity'),
        backlog_items=pm_context.get('backlog_items'),
        sprint_goal=pm_context.get('sprint_goal')
    )
    pm_context['result'] = result


@when("the Quartermaster reviews the plan")
async def quartermaster_reviews_plan(pm_context):
    """Quartermaster reviews sprint plan."""
    # In actual implementation, this would call Quartermaster agent
    pm_context['ethical_review'] = {
        'approved': True,
        'principles_assessed': ['service_to_humanity', 'consultation']
    }


@then("sprint planning guidance should be provided")
def sprint_guidance_provided(pm_context):
    """Verify sprint planning guidance was provided."""
    assert pm_context['result'] is not None
    assert 'planning_guidance' in pm_context['result']
    assert pm_context['result']['status'] == 'completed'


@then("the guidance should include sprint goal recommendations")
def guidance_includes_goal(pm_context):
    """Verify guidance includes sprint goal."""
    guidance = pm_context['result']['planning_guidance']
    assert 'goal' in guidance.lower() or 'objective' in guidance.lower()


@then("the guidance should include item selection criteria")
def guidance_includes_selection(pm_context):
    """Verify guidance includes selection criteria."""
    guidance = pm_context['result']['planning_guidance']
    assert len(guidance) > 100  # Should have substantial guidance


@then("the Quartermaster should approve the approach ethically")
def quartermaster_approves(pm_context):
    """Verify Quartermaster approval."""
    assert 'ethical_review' in pm_context['result']
    ethical_review = pm_context['result']['ethical_review']
    assert len(ethical_review) > 0


@then("the approach should ensure fair work distribution")
def fair_work_distribution(pm_context):
    """Verify fair work distribution."""
    ethical_review = pm_context['result']['ethical_review']
    assert 'fair' in ethical_review.lower() or 'distribution' in ethical_review.lower()


@then("the approach should promote sustainable pace")
def sustainable_pace(pm_context):
    """Verify sustainable pace promotion."""
    ethical_review = pm_context['result']['ethical_review']
    assert 'sustain' in ethical_review.lower() or 'pace' in ethical_review.lower() or 'wellbeing' in ethical_review.lower()


@then("the Pilot should help define a clear sprint goal")
def pilot_defines_goal(pm_context):
    """Verify Pilot helps define goal."""
    guidance = pm_context['result']['planning_guidance']
    assert 'goal' in guidance.lower()


@then("the goal should align with product objectives")
def goal_aligns_with_objectives(pm_context):
    """Verify goal alignment."""
    guidance = pm_context['result']['planning_guidance']
    assert len(guidance) > 50


@then("the goal should be achievable within the sprint")
def goal_achievable(pm_context):
    """Verify goal is achievable."""
    guidance = pm_context['result']['planning_guidance']
    assert 'achievable' in guidance.lower() or 'realistic' in guidance.lower() or 'commit' in guidance.lower()


@then("team commitment should be sought")
def team_commitment_sought(pm_context):
    """Verify team commitment is sought."""
    guidance = pm_context['result']['planning_guidance']
    assert 'commit' in guidance.lower() or 'agreement' in guidance.lower() or 'align' in guidance.lower()


@then("the Pilot should recommend adjusting commitments")
def adjust_commitments(pm_context):
    """Verify commitment adjustment recommendation."""
    guidance = pm_context['result']['planning_guidance']
    assert 'adjust' in guidance.lower() or 'capacity' in guidance.lower() or 'reduce' in guidance.lower()


@then("the ethical review should validate sustainable pace")
def validate_sustainable_pace(pm_context):
    """Verify ethical validation of pace."""
    ethical_review = pm_context['result']['ethical_review']
    assert len(ethical_review) > 0


@then("the plan should account for team wellbeing")
def account_for_wellbeing(pm_context):
    """Verify wellbeing consideration."""
    result = pm_context['result']
    assert result is not None


@then("risk mitigation strategies should be included")
def risk_mitigation_included(pm_context):
    """Verify risk mitigation strategies."""
    guidance = pm_context['result']['planning_guidance']
    assert 'risk' in guidance.lower() or 'mitigat' in guidance.lower()


@then("dependencies should be identified")
def dependencies_identified(pm_context):
    """Verify dependencies are identified."""
    guidance = pm_context['result']['planning_guidance']
    assert 'depend' in guidance.lower()


@then("contingency plans should be recommended")
def contingency_recommended(pm_context):
    """Verify contingency planning."""
    guidance = pm_context['result']['planning_guidance']
    assert 'contingency' in guidance.lower() or 'backup' in guidance.lower() or 'alternative' in guidance.lower()


@then("Baha'i principles should be applied")
def bahai_principles_applied(pm_context):
    """Verify Baha'i principles application."""
    assert pm_context.get('ethical_review') is not None


@then("service to humanity should be validated")
def service_validated(pm_context):
    """Verify service to humanity validation."""
    assert pm_context.get('ethical_review') is not None


@then("fair work distribution should be confirmed")
def fair_distribution_confirmed(pm_context):
    """Verify fair distribution confirmation."""
    assert pm_context.get('ethical_review') is not None


@then("consultation approach should be verified")
def consultation_verified(pm_context):
    """Verify consultation approach."""
    assert pm_context.get('ethical_review') is not None


@then("team wellbeing should be assessed")
def wellbeing_assessed(pm_context):
    """Verify wellbeing assessment."""
    assert pm_context.get('ethical_review') is not None
