"""Base Strategy for BDD Generation

Abstract base class and data structures for multi-strategy BDD test generation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class BehaviorSpec:
    """Extracted behavior specification from PM documentation"""
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
    source_file: str = ""
    category: str = ""


@dataclass
class BDDScenario:
    """Generated BDD scenario"""
    scenario_name: str
    scenario_type: str  # happy_path, edge_case, error_handling
    given_steps: List[str] = field(default_factory=list)
    when_steps: List[str] = field(default_factory=list)
    then_steps: List[str] = field(default_factory=list)
    strategy_used: str = ""  # Which strategy generated this


@dataclass
class BDDFeatureFile:
    """Complete .feature file content"""
    feature_name: str
    feature_description: str
    background_steps: List[str] = field(default_factory=list)
    scenarios: List[BDDScenario] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    behavior_spec: Optional[BehaviorSpec] = None


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
            tags=[f"@{behavior.capability_level.lower()}", f"@{behavior.knowledge_scope.lower()}"],
            behavior_spec=behavior
        )
    
    @abstractmethod
    def _generate_background(self, behavior: BehaviorSpec) -> List[str]:
        """Generate Background section (common setup steps)"""
        pass
