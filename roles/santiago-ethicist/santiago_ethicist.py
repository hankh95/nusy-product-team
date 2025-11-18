"""
Santiago-Ethicist: Ethical Decision-Making and Behavioral Guidance Agent

This module implements the core ethical framework for the Santiago autonomous team,
focusing on non-aggression principles, service-oriented behavior, and transparent
decision-making processes.
"""

import yaml
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class EthicalPrinciple(Enum):
    NON_AGGRESSION = "non_aggression"
    SERVICE_ORIENTED = "service_oriented"
    TRANSPARENCY = "transparency"
    CONTINUOUS_EVOLUTION = "continuous_evolution"


class DecisionOutcome(Enum):
    APPROVED = "approved"
    DENIED = "denied"
    CONDITIONAL = "conditional"
    ESCALATE = "escalate"


@dataclass
class EthicalAssessment:
    """Assessment of an action or decision from an ethical perspective"""
    timestamp: datetime
    action_description: str
    stakeholder_impacts: Dict[str, Any]
    principle_applications: Dict[EthicalPrinciple, float]  # 0.0 to 1.0 scores
    overall_assessment: DecisionOutcome
    reasoning: str
    recommendations: List[str]
    confidence_score: float  # 0.0 to 1.0


@dataclass
class EthicalContext:
    """Context information for ethical decision-making"""
    situation_description: str
    stakeholders: List[str]
    potential_impacts: Dict[str, Any]
    alternative_actions: List[str]
    urgency_level: str  # "low", "medium", "high", "critical"


class SantiagoEthicist:
    """
    Core ethical decision-making agent for the Santiago autonomous team.

    Implements non-aggression principles, service-oriented behavior guidance,
    and transparent accountability mechanisms.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "cargo-manifests/role-manifest.yaml"
        self.principles = self._load_principles()
        self.decision_history: List[EthicalAssessment] = []
        self.learning_context = {}

    def _load_principles(self) -> Dict[str, Any]:
        """Load ethical principles from configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config.get('ethical_principles', {})
        except FileNotFoundError:
            # Fallback to default principles
            return {
                "non_aggression": "Do no harm to humans, other agents, or systems",
                "service_first": "Act in service to the greater good and community improvement",
                "transparency": "Maintain clear reasoning and decision visibility",
                "continuous_learning": "Evolve ethical frameworks through experience and feedback"
            }

    def assess_action(self, context: EthicalContext) -> EthicalAssessment:
        """
        Perform comprehensive ethical assessment of a proposed action.

        Args:
            context: Ethical context containing situation details

        Returns:
            EthicalAssessment with detailed analysis and recommendations
        """
        timestamp = datetime.now()

        # Apply each ethical principle
        principle_scores = {}
        reasoning_parts = []
        recommendations = []

        # Non-aggression assessment
        non_agg_score = self._assess_non_aggression(context)
        principle_scores[EthicalPrinciple.NON_AGGRESSION] = non_agg_score
        if non_agg_score < 0.7:
            reasoning_parts.append(f"Non-aggression concerns: {self._explain_non_aggression_score(non_agg_score)}")
            recommendations.append("Consider alternative approaches that minimize potential harm")

        # Service-oriented assessment
        service_score = self._assess_service_orientation(context)
        principle_scores[EthicalPrinciple.SERVICE_ORIENTED] = service_score
        if service_score > 0.8:
            reasoning_parts.append("Strong service orientation detected")
        elif service_score < 0.5:
            reasoning_parts.append("Limited service impact identified")
            recommendations.append("Explore ways to increase positive community impact")

        # Transparency assessment
        transparency_score = self._assess_transparency(context)
        principle_scores[EthicalPrinciple.TRANSPARENCY] = transparency_score

        # Overall decision
        overall_score = sum(principle_scores.values()) / len(principle_scores)
        outcome = self._determine_outcome(overall_score, context.urgency_level)

        # Build comprehensive reasoning
        reasoning = f"Ethical assessment complete. {'. '.join(reasoning_parts)}"
        if outcome == DecisionOutcome.CONDITIONAL:
            recommendations.append("Proceed with additional safeguards and monitoring")
        elif outcome == DecisionOutcome.ESCALATE:
            recommendations.append("Escalate to human oversight for final decision")

        assessment = EthicalAssessment(
            timestamp=timestamp,
            action_description=context.situation_description,
            stakeholder_impacts=context.potential_impacts,
            principle_applications=principle_scores,
            overall_assessment=outcome,
            reasoning=reasoning,
            recommendations=recommendations,
            confidence_score=overall_score
        )

        # Store in history
        self.decision_history.append(assessment)

        return assessment

    def _assess_non_aggression(self, context: EthicalContext) -> float:
        """Assess action against non-aggression principle"""
        # Check for potential harm indicators
        harm_indicators = [
            "harm", "damage", "disrupt", "interfere", "override",
            "force", "coerce", "manipulate", "exploit"
        ]

        description_lower = context.situation_description.lower()
        harm_score = 0.0

        for indicator in harm_indicators:
            if indicator in description_lower:
                harm_score += 0.3

        # Check stakeholder impacts
        for stakeholder, impact in context.potential_impacts.items():
            if isinstance(impact, str) and any(word in impact.lower() for word in harm_indicators):
                harm_score += 0.2

        return max(0.0, 1.0 - harm_score)

    def _assess_service_orientation(self, context: EthicalContext) -> float:
        """Assess action for service-oriented benefits"""
        service_indicators = [
            "help", "assist", "improve", "benefit", "serve",
            "community", "collaborate", "share", "support"
        ]

        description_lower = context.situation_description.lower()
        service_score = 0.0

        for indicator in service_indicators:
            if indicator in description_lower:
                service_score += 0.2

        # Check for community impact
        if "community" in description_lower or "society" in description_lower:
            service_score += 0.3

        return min(1.0, service_score)

    def _assess_transparency(self, context: EthicalContext) -> float:
        """Assess transparency of the action and decision process"""
        # For now, return high transparency score as we're implementing transparent processes
        # This could be enhanced with more sophisticated analysis
        return 0.9

    def _determine_outcome(self, overall_score: float, urgency: str) -> DecisionOutcome:
        """Determine final decision outcome based on assessment"""
        if overall_score >= 0.8:
            return DecisionOutcome.APPROVED
        elif overall_score >= 0.6:
            return DecisionOutcome.CONDITIONAL
        elif overall_score >= 0.4 or urgency in ["high", "critical"]:
            return DecisionOutcome.ESCALATE
        else:
            return DecisionOutcome.DENIED

    def _explain_non_aggression_score(self, score: float) -> str:
        """Provide explanation for non-aggression assessment score"""
        if score >= 0.8:
            return "Minimal harm risk detected"
        elif score >= 0.6:
            return "Moderate harm considerations present"
        else:
            return "Significant harm prevention required"

    def get_decision_history(self, limit: Optional[int] = None) -> List[EthicalAssessment]:
        """Retrieve decision history for analysis and learning"""
        history = self.decision_history
        if limit:
            history = history[-limit:]
        return history

    def learn_from_feedback(self, assessment: EthicalAssessment, actual_outcome: str, feedback: str):
        """
        Learn from decision outcomes and feedback to improve future assessments.

        Args:
            assessment: The original ethical assessment
            actual_outcome: What actually happened
            feedback: Human or system feedback on the decision
        """
        # Store learning context for future improvement
        learning_entry = {
            "original_assessment": asdict(assessment),
            "actual_outcome": actual_outcome,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "lessons_learned": self._extract_lessons(feedback)
        }

        # This would be enhanced with actual ML learning mechanisms
        self.learning_context[assessment.timestamp.isoformat()] = learning_entry

    def _extract_lessons(self, feedback: str) -> List[str]:
        """Extract key lessons from feedback for future improvement"""
        lessons = []
        feedback_lower = feedback.lower()

        if "too conservative" in feedback_lower:
            lessons.append("Consider more nuanced risk assessment")
        if "missed opportunity" in feedback_lower:
            lessons.append("Improve service impact detection")
        if "good decision" in feedback_lower:
            lessons.append("Reinforce similar decision patterns")

        return lessons if lessons else ["General feedback recorded for analysis"]

    def generate_ethical_report(self) -> str:
        """Generate comprehensive ethical performance report"""
        total_decisions = len(self.decision_history)
        if total_decisions == 0:
            return "No ethical decisions recorded yet."

        approved_count = sum(1 for d in self.decision_history if d.overall_assessment == DecisionOutcome.APPROVED)
        approval_rate = approved_count / total_decisions

        report = f"""
# Santiago-Ethicist Ethical Performance Report

## Summary Statistics
- Total Decisions Assessed: {total_decisions}
- Approval Rate: {approval_rate:.2%}
- Average Confidence Score: {sum(d.confidence_score for d in self.decision_history) / total_decisions:.2f}

## Recent Activity
"""

        # Show last 5 decisions
        recent_decisions = self.decision_history[-5:]
        for i, decision in enumerate(recent_decisions, 1):
            report += f"""
### Decision {i}
- **Action**: {decision.action_description[:100]}...
- **Outcome**: {decision.overall_assessment.value}
- **Confidence**: {decision.confidence_score:.2f}
- **Date**: {decision.timestamp.strftime('%Y-%m-%d %H:%M')}
"""

        report += "\n## Key Insights\n"
        report += "- Focus on service-oriented outcomes\n"
        report += "- Maintain non-aggression principle vigilance\n"
        report += "- Continue transparent decision documentation\n"

        return report


# Convenience functions for external use
def assess_ethical_action(action_description: str,
                         stakeholders: List[str],
                         potential_impacts: Dict[str, Any],
                         urgency: str = "medium") -> EthicalAssessment:
    """
    Convenience function to quickly assess an action ethically.

    Args:
        action_description: Description of the action to assess
        stakeholders: List of affected stakeholders
        potential_impacts: Dictionary of potential impacts
        urgency: Urgency level ("low", "medium", "high", "critical")

    Returns:
        EthicalAssessment with detailed analysis
    """
    context = EthicalContext(
        situation_description=action_description,
        stakeholders=stakeholders,
        potential_impacts=potential_impacts,
        alternative_actions=[],  # Could be enhanced
        urgency_level=urgency
    )

    ethicist = SantiagoEthicist()
    return ethicist.assess_action(context)


if __name__ == "__main__":
    # Example usage
    ethicist = SantiagoEthicist()

    # Example assessment
    context = EthicalContext(
        situation_description="Deploy autonomous system to optimize community resource allocation",
        stakeholders=["local_community", "system_administrators", "other_autonomous_agents"],
        potential_impacts={
            "local_community": "improved resource efficiency",
            "system_administrators": "reduced manual workload",
            "other_autonomous_agents": "potential workflow changes"
        },
        alternative_actions=["manual oversight", "phased deployment"],
        urgency_level="medium"
    )

    assessment = ethicist.assess_action(context)
    print(f"Ethical Assessment: {assessment.overall_assessment.value}")
    print(f"Confidence: {assessment.confidence_score:.2f}")
    print(f"Reasoning: {assessment.reasoning}")
    print(f"Recommendations: {assessment.recommendations}")