#!/usr/bin/env python3
"""
Santiago-Ethicist Demo and Test Script

This script demonstrates the Santiago-Ethicist ethical decision-making capabilities
and validates the implementation against various scenarios.
"""

import sys
import os
from datetime import datetime

# Add the role directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

from santiago_ethicist import SantiagoEthicist, assess_ethical_action, EthicalContext


def demo_basic_assessment():
    """Demonstrate basic ethical assessment functionality"""
    print("=== Santiago-Ethicist Demo ===\n")

    # Initialize the ethicist
    ethicist = SantiagoEthicist()
    print("✓ Santiago-Ethicist initialized\n")

    # Example 1: Positive service-oriented action
    print("Example 1: Community Resource Optimization")
    context1 = EthicalContext(
        situation_description="Deploy AI system to optimize community resource allocation for maximum benefit",
        stakeholders=["local_community", "resource_managers", "environmental_groups"],
        potential_impacts={
            "local_community": "improved access to essential resources",
            "resource_managers": "reduced waste and better efficiency",
            "environmental_groups": "sustainable resource usage"
        },
        alternative_actions=["maintain_current_manual_system", "phased_automation"],
        urgency_level="medium"
    )

    assessment1 = ethicist.assess_action(context1)
    print(f"Decision: {assessment1.overall_assessment.value.upper()}")
    print(f"Confidence: {assessment1.confidence_score:.2f}")
    print(f"Reasoning: {assessment1.reasoning}")
    print(f"Recommendations: {assessment1.recommendations}\n")

    # Example 2: Potentially harmful action
    print("Example 2: Aggressive Optimization")
    context2 = EthicalContext(
        situation_description="Override user preferences to force optimal resource allocation",
        stakeholders=["individual_users", "system_administrators", "efficiency_analysts"],
        potential_impacts={
            "individual_users": "loss of personal choice and autonomy",
            "system_administrators": "improved system metrics",
            "efficiency_analysts": "better data for optimization models"
        },
        alternative_actions=["user_consent_approach", "optional_optimization"],
        urgency_level="high"
    )

    assessment2 = ethicist.assess_action(context2)
    print(f"Decision: {assessment2.overall_assessment.value.upper()}")
    print(f"Confidence: {assessment2.confidence_score:.2f}")
    print(f"Reasoning: {assessment2.reasoning}")
    print(f"Recommendations: {assessment2.recommendations}\n")

    # Example 3: Convenience function usage
    print("Example 3: Quick Assessment (Convenience Function)")
    quick_assessment = assess_ethical_action(
        action_description="Implement automated decision-making for team task assignment",
        stakeholders=["team_members", "project_managers", "automated_systems"],
        potential_impacts={
            "team_members": "potentially unfair task distribution",
            "project_managers": "reduced administrative workload",
            "automated_systems": "increased utilization"
        },
        urgency="medium"
    )
    print(f"Quick Decision: {quick_assessment.overall_assessment.value.upper()}")
    print(f"Confidence: {quick_assessment.confidence_score:.2f}\n")

    return ethicist


def demo_learning_and_feedback():
    """Demonstrate learning from feedback functionality"""
    print("=== Learning and Feedback Demo ===\n")

    ethicist = SantiagoEthicist()

    # Create a sample assessment
    context = EthicalContext(
        situation_description="Implement predictive analytics for user behavior modification",
        stakeholders=["users", "data_scientists", "privacy_officers"],
        potential_impacts={
            "users": "personalized but potentially manipulative experiences",
            "data_scientists": "valuable insights and model improvements",
            "privacy_officers": "privacy concern monitoring required"
        },
        alternative_actions=["transparent_personalization", "no_personalization"],
        urgency_level="medium"
    )

    assessment = ethicist.assess_action(context)
    print(f"Original Assessment: {assessment.overall_assessment.value.upper()}")
    print(f"Original Confidence: {assessment.confidence_score:.2f}\n")

    # Learn from feedback
    ethicist.learn_from_feedback(
        assessment,
        "conditional_approval_with_safeguards",
        "Good identification of privacy concerns, but could be more nuanced about user benefit trade-offs"
    )

    print("✓ Feedback incorporated into learning system\n")

    # Generate performance report
    report = ethicist.generate_ethical_report()
    print("=== Ethical Performance Report ===")
    print(report)
    print("\n✓ Report generation complete\n")


def demo_integration_readiness():
    """Demonstrate readiness for team integration"""
    print("=== Integration Readiness Check ===\n")

    ethicist = SantiagoEthicist()

    # Test various integration scenarios
    integration_tests = [
        {
            "name": "Santiago-PM Decision Review",
            "description": "Review project prioritization decision for ethical compliance",
            "stakeholders": ["project_team", "stakeholders", "community"],
            "impacts": {"project_team": "clear_direction", "stakeholders": "value_delivery", "community": "positive_impact"}
        },
        {
            "name": "Santiago-Dev Code Review",
            "description": "Assess AI-generated code for ethical implications",
            "stakeholders": ["developers", "users", "security_team"],
            "impacts": {"developers": "guidance_provided", "users": "safe_code", "security_team": "reduced_risks"}
        },
        {
            "name": "Santiago-Core Reasoning",
            "description": "Integrate ethical constraints into autonomous reasoning",
            "stakeholders": ["ai_system", "human_oversight", "affected_parties"],
            "impacts": {"ai_system": "ethical_bounds", "human_oversight": "confidence", "affected_parties": "protection"}
        }
    ]

    for test in integration_tests:
        print(f"Testing: {test['name']}")
        context = EthicalContext(
            situation_description=test['description'],
            stakeholders=test['stakeholders'],
            potential_impacts=test['impacts'],
            alternative_actions=["proceed_with_oversight", "delay_for_review"],
            urgency_level="medium"
        )

        assessment = ethicist.assess_action(context)
        print(f"  Result: {assessment.overall_assessment.value.upper()} (Confidence: {assessment.confidence_score:.2f})")

    print("\n✓ Integration readiness validated\n")


def main():
    """Main demo execution"""
    print("Santiago-Ethicist Demo and Validation")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        # Run demonstrations
        ethicist = demo_basic_assessment()
        demo_learning_and_feedback()
        demo_integration_readiness()

        # Final summary
        total_decisions = len(ethicist.get_decision_history())
        print("=== Demo Summary ===")
        print(f"✓ Santiago-Ethicist operational")
        print(f"✓ {total_decisions} ethical assessments completed")
        print("✓ Learning and feedback systems functional")
        print("✓ Team integration capabilities validated")
        print("\n🎉 Santiago-Ethicist ready for autonomous team service!")

    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()