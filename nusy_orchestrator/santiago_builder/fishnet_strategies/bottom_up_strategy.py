"""Bottom-Up Strategy for BDD Generation

Generate BDD scenarios directly from extracted behavior documentation.
This is the PRIMARY strategy for Fishnet v2.0.0.
"""

from typing import Any, Dict, List

from .base_strategy import BDDGenerationStrategy, BDDScenario, BehaviorSpec


class BottomUpStrategy(BDDGenerationStrategy):
    """Generate BDD from extracted behavior documentation (DocumentFirst)
    
    This strategy uses the input/output schemas, CLI examples, and descriptions
    from the extracted behavior specifications to generate realistic test scenarios.
    """
    
    @property
    def strategy_name(self) -> str:
        return "BottomUp"
    
    def generate_scenarios(
        self, 
        behavior: BehaviorSpec,
        context: Dict[str, Any] = None
    ) -> List[BDDScenario]:
        """Generate scenarios from behavior input/output schemas
        
        Creates three scenarios:
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
            strategy_used=self.strategy_name,
            tags=["happy-path"]
        ))
        
        # Scenario 2: Edge case (boundary values, optional params)
        scenarios.append(BDDScenario(
            scenario_name=f"Handle edge cases for {behavior.name}",
            scenario_type="edge_case",
            given_steps=self._generate_edge_case_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool with edge case data"],
            then_steps=self._generate_edge_case_assertions(behavior),
            strategy_used=self.strategy_name,
            tags=["edge-case"]
        ))
        
        # Scenario 3: Error handling (invalid/missing required params)
        scenarios.append(BDDScenario(
            scenario_name=f"Handle errors for {behavior.name}",
            scenario_type="error_handling",
            given_steps=self._generate_error_inputs(behavior),
            when_steps=[f"I invoke the '{behavior.name}' MCP tool with invalid data"],
            then_steps=[
                "the MCP tool should return an error",
                "the error message should be descriptive",
                "no partial data should be committed to the knowledge graph"
            ],
            strategy_used=self.strategy_name,
            tags=["error-handling"]
        ))
        
        return scenarios
    
    def _extract_given_from_inputs(self, behavior: BehaviorSpec) -> List[str]:
        """Convert input schema to Given steps"""
        steps = ["the Santiago PM knowledge graph is initialized"]
        
        input_schema = behavior.input_schema
        required = input_schema.get("required", [])
        properties = input_schema.get("properties", {})
        
        # Add required parameters
        for field in required:
            field_info = properties.get(field, {})
            field_type = field_info.get("type", "string")
            field_desc = field_info.get("description", "")
            
            if field_desc:
                steps.append(f"I have a valid '{field}' parameter ({field_type}) - {field_desc}")
            else:
                steps.append(f"I have a valid '{field}' parameter ({field_type})")
        
        # Mention optional parameters if they exist
        optional = [k for k in properties.keys() if k not in required]
        if optional:
            steps.append(f"I optionally provide: {', '.join(optional)}")
        
        return steps
    
    def _extract_then_from_outputs(self, behavior: BehaviorSpec) -> List[str]:
        """Convert output schema to Then steps"""
        steps = ["the MCP tool should succeed"]
        
        output_schema = behavior.output_schema
        properties = output_schema.get("properties", {})
        
        # Add assertions for each output field
        for field, field_info in properties.items():
            field_type = field_info.get("type", "")
            if field_type:
                steps.append(f"the response should contain '{field}' ({field_type})")
            else:
                steps.append(f"the response should contain '{field}'")
        
        # Add knowledge graph mutation check
        if behavior.mutates_kg:
            steps.append("the knowledge graph should be updated with new data")
        else:
            steps.append("the knowledge graph should remain unchanged")
        
        return steps
    
    def _generate_edge_case_inputs(self, behavior: BehaviorSpec) -> List[str]:
        """Generate edge case Given steps"""
        steps = ["the Santiago PM knowledge graph is initialized"]
        
        input_schema = behavior.input_schema
        properties = input_schema.get("properties", {})
        
        # Edge cases based on common patterns
        edge_cases = []
        for field, field_info in properties.items():
            field_type = field_info.get("type", "")
            
            if field_type == "string":
                edge_cases.append(f"{field} is an empty string")
            elif field_type == "array":
                edge_cases.append(f"{field} is an empty array")
            elif field_type == "integer":
                edge_cases.append(f"{field} is zero or negative")
        
        if edge_cases:
            steps.append("I provide edge case values:")
            steps.extend([f"  - {case}" for case in edge_cases[:3]])  # Limit to 3 examples
        else:
            steps.append("I provide minimal valid input with no optional parameters")
        
        return steps
    
    def _generate_edge_case_assertions(self, behavior: BehaviorSpec) -> List[str]:
        """Generate edge case Then steps"""
        steps = [
            "the MCP tool should handle the edge case gracefully",
            "the response should indicate any assumptions or defaults applied"
        ]
        
        if behavior.mutates_kg:
            steps.append("the knowledge graph should remain in a consistent state")
        
        return steps
    
    def _generate_error_inputs(self, behavior: BehaviorSpec) -> List[str]:
        """Generate error case Given steps"""
        steps = ["the Santiago PM knowledge graph is initialized"]
        
        input_schema = behavior.input_schema
        required = input_schema.get("required", [])
        
        if required:
            missing_field = required[0]  # Pick first required field
            steps.append(f"I do NOT provide the required '{missing_field}' parameter")
        else:
            steps.append("I provide data in an invalid format")
        
        return steps
    
    def _generate_background(self, behavior: BehaviorSpec) -> List[str]:
        """Generate Background section for this behavior"""
        return [
            "Given the Santiago PM MCP service is running",
            "And the knowledge graph is initialized with test data",
            f"And I have {behavior.capability_level} level permissions"
        ]
