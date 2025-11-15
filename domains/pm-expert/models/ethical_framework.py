"""
Ethical Framework for PM Domain

This module implements the Baha'i ethical principles applied to product management
practices. All PM decisions and knowledge are validated through this ethical lens.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class BahaiPrinciple(Enum):
    """Core Baha'i principles applied to product management."""
    SERVICE_TO_HUMANITY = "service_to_humanity"
    UNITY_IN_DIVERSITY = "unity_in_diversity"
    CONSULTATION = "consultation"
    PROGRESSIVE_REVELATION = "progressive_revelation"
    ELIMINATION_OF_PREJUDICE = "elimination_of_prejudice"
    JUSTICE = "justice"
    TRUSTWORTHINESS = "trustworthiness"


@dataclass
class EthicalPrinciple:
    """An ethical principle with guidance for application."""
    principle: BahaiPrinciple
    description: str
    pm_application: str
    validation_questions: List[str] = field(default_factory=list)


@dataclass
class EthicalReview:
    """Result of an ethical review of a PM decision or practice."""
    decision_or_practice: str
    principles_assessed: List[BahaiPrinciple]
    alignment_score: float  # 0.0 to 1.0
    concerns: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    approved: bool = False
    reviewer: str = "Quartermaster"
    review_notes: Optional[str] = None


class EthicalFramework:
    """Framework for evaluating PM practices against Baha'i principles."""
    
    def __init__(self):
        self.principles = self._initialize_principles()
    
    def _initialize_principles(self) -> Dict[BahaiPrinciple, EthicalPrinciple]:
        """Initialize the ethical principles with PM-specific guidance."""
        return {
            BahaiPrinciple.SERVICE_TO_HUMANITY: EthicalPrinciple(
                principle=BahaiPrinciple.SERVICE_TO_HUMANITY,
                description="All work should serve the betterment of humanity",
                pm_application="Products and features should provide genuine value and benefit to users and society",
                validation_questions=[
                    "Does this product/feature genuinely help users?",
                    "Does it promote positive social impact?",
                    "Are we avoiding harmful or exploitative practices?",
                    "Does it respect user dignity and wellbeing?"
                ]
            ),
            BahaiPrinciple.UNITY_IN_DIVERSITY: EthicalPrinciple(
                principle=BahaiPrinciple.UNITY_IN_DIVERSITY,
                description="Embrace and celebrate diversity while maintaining unity of purpose",
                pm_application="Build inclusive teams and products that serve diverse users",
                validation_questions=[
                    "Is our team diverse and inclusive?",
                    "Does the product serve users from different backgrounds?",
                    "Are we considering accessibility and inclusion?",
                    "Do we value different perspectives in decision-making?"
                ]
            ),
            BahaiPrinciple.CONSULTATION: EthicalPrinciple(
                principle=BahaiPrinciple.CONSULTATION,
                description="Make decisions through collaborative consultation and consensus",
                pm_application="Foster collaborative decision-making and transparent communication",
                validation_questions=[
                    "Have we consulted all relevant stakeholders?",
                    "Are team members empowered to contribute?",
                    "Is decision-making transparent and inclusive?",
                    "Do we seek consensus where possible?"
                ]
            ),
            BahaiPrinciple.PROGRESSIVE_REVELATION: EthicalPrinciple(
                principle=BahaiPrinciple.PROGRESSIVE_REVELATION,
                description="Embrace continuous learning and improvement",
                pm_application="Adopt iterative development and continuous discovery practices",
                validation_questions=[
                    "Are we learning from users continuously?",
                    "Do we embrace change and adaptation?",
                    "Are we open to new ideas and approaches?",
                    "Do we reflect and improve regularly?"
                ]
            ),
            BahaiPrinciple.ELIMINATION_OF_PREJUDICE: EthicalPrinciple(
                principle=BahaiPrinciple.ELIMINATION_OF_PREJUDICE,
                description="Actively work to eliminate all forms of prejudice and bias",
                pm_application="Ensure fair, unbiased practices and products",
                validation_questions=[
                    "Have we identified and addressed potential biases?",
                    "Do our practices treat all people fairly?",
                    "Are we aware of our own unconscious biases?",
                    "Does the product avoid perpetuating stereotypes?"
                ]
            ),
            BahaiPrinciple.JUSTICE: EthicalPrinciple(
                principle=BahaiPrinciple.JUSTICE,
                description="Uphold justice and fairness in all actions",
                pm_application="Ensure fair distribution of work, recognition, and rewards",
                validation_questions=[
                    "Are team responsibilities distributed fairly?",
                    "Do we recognize contributions appropriately?",
                    "Are users treated fairly by our product?",
                    "Do we uphold ethical business practices?"
                ]
            ),
            BahaiPrinciple.TRUSTWORTHINESS: EthicalPrinciple(
                principle=BahaiPrinciple.TRUSTWORTHINESS,
                description="Maintain honesty, integrity, and trustworthiness",
                pm_application="Be honest with stakeholders, users, and team members",
                validation_questions=[
                    "Are we honest about progress and challenges?",
                    "Do we keep our commitments?",
                    "Are we transparent with users about data and privacy?",
                    "Do we maintain integrity in difficult situations?"
                ]
            )
        }
    
    def review_decision(self, decision_description: str, 
                       context: Optional[Dict] = None) -> EthicalReview:
        """Review a PM decision against ethical principles."""
        # This would use AI/LLM to analyze the decision
        # For now, provide a basic structure
        
        review = EthicalReview(
            decision_or_practice=decision_description,
            principles_assessed=list(self.principles.keys()),
            alignment_score=0.0,
            concerns=[],
            recommendations=[],
            approved=False
        )
        
        # In a full implementation, this would:
        # 1. Analyze decision against each principle
        # 2. Score alignment (0.0 to 1.0 per principle)
        # 3. Identify concerns
        # 4. Generate recommendations
        # 5. Determine if approved (>= 0.7 alignment)
        
        return review
    
    def get_principle_guidance(self, principle: BahaiPrinciple) -> EthicalPrinciple:
        """Get guidance for applying a specific principle."""
        return self.principles[principle]
    
    def validate_knowledge_source(self, source_description: str) -> EthicalReview:
        """Validate a knowledge source for ethical alignment."""
        # Check if knowledge source aligns with ethical principles
        review = EthicalReview(
            decision_or_practice=f"Knowledge Source: {source_description}",
            principles_assessed=[
                BahaiPrinciple.SERVICE_TO_HUMANITY,
                BahaiPrinciple.ELIMINATION_OF_PREJUDICE,
                BahaiPrinciple.TRUSTWORTHINESS
            ],
            alignment_score=0.0,
            approved=False
        )
        
        return review


def get_ethical_framework() -> EthicalFramework:
    """Get the singleton ethical framework instance."""
    return EthicalFramework()


# Example ethical guidelines for common PM practices
ETHICAL_PM_GUIDELINES = {
    "sprint_planning": [
        "Ensure fair distribution of work across team members",
        "Consider team wellbeing and sustainable pace",
        "Include diverse perspectives in planning decisions",
        "Be realistic and honest about commitments"
    ],
    "user_research": [
        "Respect user privacy and data protection",
        "Seek diverse user perspectives",
        "Be transparent about research purpose and use",
        "Ensure informed consent"
    ],
    "feature_prioritization": [
        "Prioritize features that serve humanity",
        "Consider impact on vulnerable users",
        "Balance business needs with user wellbeing",
        "Avoid addictive or manipulative patterns"
    ],
    "team_retrospective": [
        "Create safe space for honest feedback",
        "Focus on improvement, not blame",
        "Ensure all voices are heard equally",
        "Act on feedback with integrity"
    ],
    "stakeholder_communication": [
        "Be honest about progress and challenges",
        "Maintain transparency while respecting confidentiality",
        "Seek consultation on major decisions",
        "Build trust through consistent communication"
    ]
}
