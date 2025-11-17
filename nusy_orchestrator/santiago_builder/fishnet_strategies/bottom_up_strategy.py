"""Bottom-Up Strategy: Generate BDD from extracted behavior documentation

Primary strategy that generates scenarios directly from behavior specifications
in pm-behaviors-extracted.md and passage-behaviors-extracted.md.
"""

from typing import List, Dict, Any
from .base_strategy import BDDGenerationStrategy, BehaviorSpec, BDDScenario


class BottomUpStrategy(BDDGenerationStrategy):
    """Generate BDD from extracted behavior documentation"""
    
    @property
    def strategy_name(self) -> str:
        return "BottomUp"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """
        Generate scenarios from behavior input/output schemas:
        1. Happy path: Valid inputs → expected outputs
        2. Edge case: Boundary values, optional params
        3. Error handling: Invalid inputs → error responses
        """
        scenarios = []
        
        # Scenario 1: Happy path (use CLI example from behavior spec)
        scenarios.append(BDDScenario(
            scenario_name=f"Successfully execute {behavior.name}",
            scenario_type="happy_path",
            given_steps=self._extract_given_from_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool"],
            then_steps=self._extract_then_from_outputs(behavior),
            strategy_used="BottomUp"
        ))
        
        # Scenario 2: Edge case (boundary values, optional params)
        scenarios.append(BDDScenario(
            scenario_name=f"Handle edge cases for {behavior.name}",
            scenario_type="edge_case",
            given_steps=self._generate_edge_case_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool"],
            then_steps=self._generate_edge_case_assertions(behavior),
            strategy_used="BottomUp"
        ))
        
        # Scenario 3: Error handling (invalid/missing required params)
        scenarios.append(BDDScenario(
            scenario_name=f"Handle errors for {behavior.name}",
            scenario_type="error_handling",
            given_steps=self._generate_error_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool"],
            then_steps=[
                "the MCP tool should return an error", 
                "the error message should be descriptive"
            ],
            strategy_used="BottomUp"
        ))
        
        return scenarios
    
    def _extract_given_from_inputs(self, behavior: BehaviorSpec) -> List[str]:
        """Convert input schema to Given steps"""
        steps = ["the Santiago PM knowledge graph is initialized"]
        
        # Extract required fields from input schema
        required = behavior.input_schema.get("required", [])
        properties = behavior.input_schema.get("properties", {})
        
        for field in required:
            field_info = properties.get(field, {})
            field_type = field_info.get("type", "string")
            steps.append(f"I have a valid '{field}' parameter ({field_type})")
        
        return steps
    
    def _extract_then_from_outputs(self, behavior: BehaviorSpec) -> List[str]:
        """Convert output schema to Then steps"""
        steps = ["the MCP tool should succeed"]
        properties = behavior.output_schema.get("properties", {})
        
        for field in properties.keys():
            steps.append(f"the response should contain '{field}'")
        
        if behavior.mutates_kg:
            steps.append("the knowledge graph should be updated")
        
        return steps
    
    def _generate_edge_case_inputs(self, behavior: BehaviorSpec) -> List[str]:
        """Generate edge case Given steps"""
        steps = ["the Santiago PM knowledge graph is initialized"]
        
        # Look for optional parameters
        properties = behavior.input_schema.get("properties", {})
        required = behavior.input_schema.get("required", [])
        optional_params = [p for p in properties.keys() if p not in required]
        
        if optional_params:
            steps.append(f"I provide optional parameters: {', '.join(optional_params[:2])}")
        else:
            steps.append("I provide boundary value inputs")
        
        return steps
    
    def _generate_edge_case_assertions(self, behavior: BehaviorSpec) -> List[str]:
        """Generate edge case Then steps"""
        steps = ["the MCP tool should handle edge cases gracefully"]
        
        if behavior.mutates_kg:
            steps.append("the knowledge graph should remain consistent")
        
        steps.append("the response should be valid")
        return steps
    
    def _generate_error_inputs(self, behavior: BehaviorSpec) -> List[str]:
        """Generate error handling Given steps"""
        required = behavior.input_schema.get("required", [])
        
        if required:
            # Pick first required field for missing parameter test
            first_required = required[0]
            return [
                "the Santiago PM knowledge graph is initialized",
                f"I am missing the required '{first_required}' parameter"
            ]
        else:
            return [
                "the Santiago PM knowledge graph is initialized",
                "I provide invalid parameter types"
            ]
    
    def _generate_background(self, behavior: BehaviorSpec) -> List[str]:
        """Generate Background section (common setup steps)"""
        return [
            "Given the Santiago PM MCP service is running",
            "And the knowledge graph is initialized with test data",
            f"And I have {behavior.capability_level} level permissions"
        ]
