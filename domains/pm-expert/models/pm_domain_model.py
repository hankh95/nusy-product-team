"""
PM Domain Knowledge Model

This module defines the core product management domain concepts, relationships,
and knowledge structures for the Santiago autonomous PM expert system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Set
from enum import Enum


class PMMethodology(Enum):
    """Product Management methodologies."""
    AGILE = "agile"
    SCRUM = "scrum"
    KANBAN = "kanban"
    XP = "extreme_programming"
    LEAN_UX = "lean_ux"
    LEAN_STARTUP = "lean_startup"
    SAFE = "safe"
    DAD = "disciplined_agile_delivery"


class TeamRole(Enum):
    """Team member roles in product development."""
    PRODUCT_OWNER = "product_owner"
    SCRUM_MASTER = "scrum_master"
    DEVELOPER = "developer"
    UX_DESIGNER = "ux_designer"
    QA_ENGINEER = "qa_engineer"
    STAKEHOLDER = "stakeholder"


class CeremonyType(Enum):
    """Agile ceremonies and meetings."""
    SPRINT_PLANNING = "sprint_planning"
    DAILY_STANDUP = "daily_standup"
    SPRINT_REVIEW = "sprint_review"
    RETROSPECTIVE = "retrospective"
    BACKLOG_REFINEMENT = "backlog_refinement"
    DISCOVERY_SESSION = "discovery_session"


@dataclass
class PMConcept:
    """A core product management concept."""
    id: str
    name: str
    description: str
    methodology: PMMethodology
    related_concepts: List[str] = field(default_factory=list)
    source: Optional[str] = None
    confidence: float = 1.0


@dataclass
class UserStory:
    """A user story representing product functionality."""
    id: str
    title: str
    description: str
    as_a: str  # User role
    i_want: str  # Functionality
    so_that: str  # Benefit/outcome
    acceptance_criteria: List[str] = field(default_factory=list)
    story_points: Optional[int] = None
    priority: str = "medium"
    tags: List[str] = field(default_factory=list)


@dataclass
class Epic:
    """An epic representing a large body of work."""
    id: str
    title: str
    description: str
    objective: str
    user_stories: List[str] = field(default_factory=list)  # Story IDs
    business_value: Optional[str] = None
    estimated_duration: Optional[int] = None  # In sprints


@dataclass
class Sprint:
    """A sprint or iteration in Agile development."""
    id: str
    name: str
    goal: str
    start_date: datetime
    end_date: datetime
    committed_stories: List[str] = field(default_factory=list)
    completed_stories: List[str] = field(default_factory=list)
    velocity: Optional[int] = None
    retrospective_notes: Optional[str] = None


@dataclass
class PMCeremony:
    """An Agile ceremony or meeting."""
    id: str
    type: CeremonyType
    date: datetime
    participants: List[str]  # Team member IDs
    duration_minutes: int
    agenda: List[str] = field(default_factory=list)
    outcomes: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)


@dataclass
class Risk:
    """A project risk or impediment."""
    id: str
    title: str
    description: str
    impact: str  # high, medium, low
    probability: str  # high, medium, low
    mitigation_strategy: Optional[str] = None
    status: str = "open"  # open, mitigated, closed
    owner: Optional[str] = None


@dataclass
class Stakeholder:
    """A project stakeholder."""
    id: str
    name: str
    role: str
    influence: str  # high, medium, low
    interest: str  # high, medium, low
    communication_frequency: str
    concerns: List[str] = field(default_factory=list)


@dataclass
class PMKnowledgeSource:
    """A source of PM knowledge."""
    id: str
    title: str
    author: str
    type: str  # book, article, methodology, framework
    url: Optional[str] = None
    key_concepts: List[str] = field(default_factory=list)
    summary: Optional[str] = None
    ingested_date: Optional[datetime] = None


@dataclass
class PMDomainOntology:
    """Complete PM domain knowledge ontology."""
    concepts: Dict[str, PMConcept] = field(default_factory=dict)
    methodologies: Set[PMMethodology] = field(default_factory=set)
    knowledge_sources: Dict[str, PMKnowledgeSource] = field(default_factory=dict)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    
    def add_concept(self, concept: PMConcept) -> None:
        """Add a concept to the ontology."""
        self.concepts[concept.id] = concept
        self.methodologies.add(concept.methodology)
    
    def add_knowledge_source(self, source: PMKnowledgeSource) -> None:
        """Add a knowledge source to the ontology."""
        self.knowledge_sources[source.id] = source
    
    def get_concepts_by_methodology(self, methodology: PMMethodology) -> List[PMConcept]:
        """Get all concepts for a specific methodology."""
        return [c for c in self.concepts.values() if c.methodology == methodology]
    
    def get_related_concepts(self, concept_id: str) -> List[PMConcept]:
        """Get concepts related to a given concept."""
        if concept_id not in self.concepts:
            return []
        
        concept = self.concepts[concept_id]
        return [self.concepts[cid] for cid in concept.related_concepts if cid in self.concepts]


# Core PM knowledge base
def initialize_core_pm_knowledge() -> PMDomainOntology:
    """Initialize the core PM knowledge base with fundamental concepts."""
    ontology = PMDomainOntology()
    
    # Agile concepts
    ontology.add_concept(PMConcept(
        id="agile_manifesto",
        name="Agile Manifesto",
        description="Core values and principles of Agile software development",
        methodology=PMMethodology.AGILE,
        related_concepts=["scrum", "kanban", "xp"],
        source="agilemanifesto.org"
    ))
    
    # Scrum concepts
    ontology.add_concept(PMConcept(
        id="scrum_framework",
        name="Scrum Framework",
        description="Lightweight framework for managing complex work",
        methodology=PMMethodology.SCRUM,
        related_concepts=["sprint", "sprint_planning", "daily_scrum", "retrospective"],
        source="Scrum Guide"
    ))
    
    ontology.add_concept(PMConcept(
        id="sprint",
        name="Sprint",
        description="Time-boxed iteration of work, typically 1-4 weeks",
        methodology=PMMethodology.SCRUM,
        related_concepts=["sprint_goal", "sprint_planning", "sprint_review"],
        source="Scrum Guide"
    ))
    
    # Kanban concepts
    ontology.add_concept(PMConcept(
        id="kanban_method",
        name="Kanban Method",
        description="Method for managing knowledge work with emphasis on just-in-time delivery",
        methodology=PMMethodology.KANBAN,
        related_concepts=["wip_limits", "flow", "pull_system"],
        source="David Anderson"
    ))
    
    # Lean UX concepts (Jeff Gothelf)
    ontology.add_concept(PMConcept(
        id="lean_ux",
        name="Lean UX",
        description="Applying Lean principles to user experience design",
        methodology=PMMethodology.LEAN_UX,
        related_concepts=["hypothesis", "mvp", "continuous_discovery"],
        source="Jeff Gothelf"
    ))
    
    ontology.add_concept(PMConcept(
        id="continuous_discovery",
        name="Continuous Discovery",
        description="Ongoing process of learning about users and validating ideas",
        methodology=PMMethodology.LEAN_UX,
        related_concepts=["user_research", "prototype", "validation"],
        source="Jeff Gothelf"
    ))
    
    # User Story Mapping (Jeff Patton)
    ontology.add_concept(PMConcept(
        id="user_story_mapping",
        name="User Story Mapping",
        description="Visual practice for organizing user stories around user activities",
        methodology=PMMethodology.AGILE,
        related_concepts=["user_story", "user_journey", "backlog"],
        source="Jeff Patton"
    ))
    
    ontology.add_concept(PMConcept(
        id="discovery_practices",
        name="Discovery Practices",
        description="Techniques for discovering and understanding user needs",
        methodology=PMMethodology.AGILE,
        related_concepts=["user_research", "prototyping", "validation"],
        source="Jeff Patton"
    ))
    
    # Knowledge sources
    ontology.add_knowledge_source(PMKnowledgeSource(
        id="jeff_patton",
        title="User Story Mapping & Discovery",
        author="Jeff Patton",
        type="methodology",
        url="jpattonassociates.com",
        key_concepts=["user_story_mapping", "discovery_practices", "outcome_thinking"],
        summary="User-centered approach to product development focusing on user journeys and outcomes"
    ))
    
    ontology.add_knowledge_source(PMKnowledgeSource(
        id="jeff_gothelf",
        title="Lean UX & Continuous Discovery",
        author="Jeff Gothelf",
        type="methodology",
        url="jeffgothelf.com",
        key_concepts=["lean_ux", "continuous_discovery", "hypothesis_driven"],
        summary="Applying Lean principles to UX and product development with emphasis on learning"
    ))
    
    return ontology
