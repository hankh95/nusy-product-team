"""Fishnet - BDD Test + MCP Manifest Generation

Generates behavior-driven development tests and service manifests from domain knowledge.

Version 2.0.0 implements multi-strategy BDD generation from extracted PM behaviors.

Primary Features:
1. Parse behavior markdown files (pm-behaviors-extracted.md, passage-behaviors-extracted.md)
2. Generate .feature files with Gherkin scenarios
3. Multi-strategy approach (BottomUp, TopDown, External, Logic, Experiment)
4. CLI interface for standalone execution

Capability Levels:
- Apprentice: Basic operations, guided workflows, high supervision
- Journeyman: Standard operations, moderate autonomy, routine tasks
- Master: Complex operations, high autonomy, strategic decisions
- Expert: Domain innovation, full autonomy, novel solutions

Knowledge Scope:
- Pond: Single task/feature scope (localized knowledge)
- Lake: Feature set scope (bounded domain)
- Sea: Domain scope (full domain knowledge)
- Ocean: Cross-domain scope (multi-domain integration)
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

# Handle both relative and absolute imports for CLI usage
try:
    from .fishnet_strategies import (
        BehaviorSpec,
        BDDScenario,
        BDDFeatureFile,
        BDDGenerationStrategy,
        BottomUpStrategy,
    )
except ImportError:
    # Running as script - add parent to path
    sys.path.insert(0, str(Path(__file__).parent))
    from fishnet_strategies import (
        BehaviorSpec,
        BDDScenario,
        BDDFeatureFile,
        BDDGenerationStrategy,
        BottomUpStrategy,
    )


class CapabilityLevel(Enum):
    """Agent capability maturity levels"""
    APPRENTICE = "apprentice"
    JOURNEYMAN = "journeyman"
    MASTER = "master"
    EXPERT = "expert"


class KnowledgeScope(Enum):
    """Knowledge breadth indicators"""
    POND = "pond"
    LAKE = "lake"
    SEA = "sea"
    OCEAN = "ocean"


@dataclass
class BDDScenario:
    """Single Gherkin scenario"""
    scenario_id: str
    name: str
    given_steps: List[str]
    when_steps: List[str]
    then_steps: List[str]
    tags: List[str] = field(default_factory=list)
    knowledge_refs: List[str] = field(default_factory=list)


@dataclass
class BDDFeature:
    """BDD feature file"""
    feature_id: str
    name: str
    description: str
    scenarios: List[BDDScenario] = field(default_factory=list)
    background_steps: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class MCPTool:
    """MCP service tool definition"""
    name: str
    description: str
    tool_type: str  # input, output, communication
    parameters: Dict[str, str] = field(default_factory=dict)
    returns: Dict[str, str] = field(default_factory=dict)
    concurrency_risk: bool = False
    mutates_kg: bool = False


@dataclass
class MCPManifest:
    """MCP service manifest"""
    service_name: str
    version: str
    description: str
    capability_level: CapabilityLevel
    knowledge_scope: KnowledgeScope
    tools: List[MCPTool] = field(default_factory=list)
    budget_hint_usd_per_day: float = 25.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CoverageReport:
    """Test coverage analysis"""
    total_behaviors: int
    behaviors_with_tests: int
    total_scenarios: int
    coverage_ratio: float
    gaps: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class FishnetV2:
    """
    Multi-strategy BDD test generator for Santiago PM behaviors.
    
    Version 2.0.0 - Parses behavior markdown files and generates .feature files
    using pluggable generation strategies.
    
    Usage:
        fishnet = FishnetV2(
            behaviors_file="pm-behaviors-extracted.md",
            ontology_file="pm-domain-ontology.ttl",
            output_dir="bdd-tests/"
        )
        results = fishnet.generate_all_bdd_files(strategy_names=["bottom_up"])
    """
    
    def __init__(
        self,
        behaviors_file: Path,
        ontology_file: Path,
        output_dir: Path
    ):
        self.behaviors_file = Path(behaviors_file)
        self.ontology_file = Path(ontology_file)
        self.output_dir = Path(output_dir)
        
        # Initialize strategies
        self.strategies: Dict[str, BDDGenerationStrategy] = {
            "bottom_up": BottomUpStrategy(),
        }
    
    def generate_all_bdd_files(
        self,
        strategy_names: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate BDD .feature files for all behaviors using specified strategies.
        
        Args:
            strategy_names: List of strategies to use (default: ["bottom_up"])
            
        Returns:
            Dict with generation results and statistics
        """
        if strategy_names is None:
            strategy_names = ["bottom_up"]
        
        print(f"\n🕸️  Fishnet v2.0.0: Multi-Strategy BDD Generation")
        print(f"   Behaviors File: {self.behaviors_file.name}")
        print(f"   Output Dir: {self.output_dir}")
        print(f"   Strategies: {', '.join(strategy_names)}")
        print()
        
        # Load behaviors from markdown
        behaviors = self._load_behaviors()
        print(f"   ✅ Loaded {len(behaviors)} behaviors")
        
        # Generate feature files
        results = {
            "total_behaviors": len(behaviors),
            "files_generated": 0,
            "scenarios_generated": 0,
            "strategies_used": strategy_names,
            "generation_time": datetime.now().isoformat(),
            "output_dir": str(self.output_dir)
        }
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        for behavior in behaviors:
            try:
                feature_file = self._generate_feature_file(behavior, strategy_names)
                output_path = self.output_dir / f"{behavior.name}.feature"
                self._write_feature_file(feature_file, output_path)
                results["files_generated"] += 1
                results["scenarios_generated"] += len(feature_file.scenarios)
                print(f"   ✅ Generated {behavior.name}.feature ({len(feature_file.scenarios)} scenarios)")
            except Exception as e:
                print(f"   ❌ Failed to generate {behavior.name}: {e}")
        
        print(f"\n   🎉 Complete: {results['files_generated']} files, {results['scenarios_generated']} scenarios")
        return results
    
    def _load_behaviors(self) -> List[BehaviorSpec]:
        """Load behaviors from markdown file(s)"""
        behaviors = []
        
        # Parse the behaviors file
        with open(self.behaviors_file, 'r') as f:
            content = f.read()
        
        behaviors.extend(self._parse_behaviors_markdown(content, str(self.behaviors_file)))
        
        # Also try to load passage-behaviors if in same directory
        passage_file = self.behaviors_file.parent / "passage-behaviors-extracted.md"
        if passage_file.exists():
            with open(passage_file, 'r') as f:
                passage_content = f.read()
            behaviors.extend(self._parse_behaviors_markdown(passage_content, str(passage_file)))
        
        return behaviors
    
    def _parse_behaviors_markdown(self, content: str, source_file: str) -> List[BehaviorSpec]:
        """Parse behaviors from markdown content"""
        behaviors = []
        
        # Split by behavior sections (### Behavior X.Y:)
        behavior_pattern = r'### Behavior \d+\.\d+: (.+?)(?=### Behavior|\Z)'
        behavior_sections = re.findall(behavior_pattern, content, re.DOTALL)
        
        for section in behavior_sections:
            try:
                behavior = self._parse_behavior_section(section, source_file)
                if behavior:
                    behaviors.append(behavior)
            except Exception as e:
                print(f"   ⚠️  Failed to parse behavior section: {e}")
        
        return behaviors
    
    def _parse_behavior_section(self, section: str, source_file: str) -> Optional[BehaviorSpec]:
        """Parse a single behavior section"""
        # Extract name
        name_match = re.search(r'\*\*Name\*\*: `(.+?)`', section)
        if not name_match:
            return None
        name = name_match.group(1)
        
        # Extract description
        desc_match = re.search(r'\*\*Description\*\*: (.+?)(?=\*\*|\n\n)', section, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""
        
        # Extract capability level
        cap_match = re.search(r'\*\*Capability Level\*\*: (\w+)', section)
        capability_level = cap_match.group(1) if cap_match else "Journeyman"
        
        # Extract knowledge scope
        scope_match = re.search(r'\*\*Knowledge Scope\*\*: (\w+)', section)
        knowledge_scope = scope_match.group(1) if scope_match else "Lake"
        
        # Extract mutates KG
        mutates_match = re.search(r'\*\*Mutates KG\*\*: (Yes|No)', section)
        mutates_kg = mutates_match.group(1) == "Yes" if mutates_match else False
        
        # Extract concurrency safe
        concur_match = re.search(r'\*\*Concurrency Safe\*\*: (Yes|No)', section)
        concurrency_safe = concur_match.group(1) == "Yes" if concur_match else True
        
        # Extract input schema (JSON)
        input_schema = self._extract_json_schema(section, "Input Schema")
        
        # Extract output schema (JSON)
        output_schema = self._extract_json_schema(section, "Output Schema")
        
        # Extract ontology mapping
        onto_match = re.search(r'\*\*Maps to Ontology\*\*: `(.+?)`', section)
        ontology_mapping = onto_match.group(1) if onto_match else f"nusy:PMBehavior-{name}"
        
        # Extract CLI example
        cli_match = re.search(r'\*\*CLI Example\*\*: `(.+?)`', section)
        cli_example = cli_match.group(1) if cli_match else f"nusy {name}"
        
        # Extract SPARQL query if present
        sparql_match = re.search(r'\*\*SPARQL Query\*\*:\s*```sparql\s*(.+?)\s*```', section, re.DOTALL)
        sparql_query = sparql_match.group(1).strip() if sparql_match else ""
        
        return BehaviorSpec(
            name=name,
            description=description,
            capability_level=capability_level,
            knowledge_scope=knowledge_scope,
            input_schema=input_schema,
            output_schema=output_schema,
            mutates_kg=mutates_kg,
            concurrency_safe=concurrency_safe,
            ontology_mapping=ontology_mapping,
            cli_example=cli_example,
            sparql_query=sparql_query,
            source_file=source_file
        )
    
    def _extract_json_schema(self, section: str, schema_name: str) -> Dict[str, Any]:
        """Extract JSON schema from markdown section"""
        pattern = rf'\*\*{schema_name}\*\*:\s*```json\s*(.+?)\s*```'
        match = re.search(pattern, section, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            # Clean up the JSON (remove comments in parentheses)
            json_str = re.sub(r'\s*\(.*?\)', '', json_str)
            try:
                schema = json.loads(json_str)
                # Infer required fields if not specified
                if "required" not in schema and "properties" in schema:
                    # Fields without "optional" in their type are required
                    required = []
                    for field, props in schema.items():
                        if isinstance(props, str) and "optional" not in props.lower():
                            required.append(field)
                    schema["required"] = required
                return schema
            except json.JSONDecodeError as e:
                print(f"   ⚠️  Failed to parse {schema_name} JSON: {e}")
                return {"properties": {}}
        
        return {"properties": {}}
    
    def _generate_feature_file(
        self,
        behavior: BehaviorSpec,
        strategy_names: List[str]
    ) -> BDDFeatureFile:
        """Generate complete .feature file for a behavior"""
        all_scenarios = []
        
        # Run each selected strategy
        for strategy_name in strategy_names:
            if strategy_name in self.strategies:
                strategy = self.strategies[strategy_name]
                scenarios = strategy.generate_scenarios(behavior)
                all_scenarios.extend(scenarios)
        
        # Get background from first strategy
        background_steps = []
        if strategy_names and strategy_names[0] in self.strategies:
            strategy = self.strategies[strategy_names[0]]
            background_steps = strategy._generate_background(behavior)
        
        return BDDFeatureFile(
            feature_name=behavior.name,
            feature_description=behavior.description,
            background_steps=background_steps,
            scenarios=all_scenarios,
            tags=[
                f"@{behavior.capability_level.lower()}",
                f"@{behavior.knowledge_scope.lower()}"
            ],
            behavior_spec=behavior
        )
    
    def _write_feature_file(self, feature_file: BDDFeatureFile, output_path: Path):
        """Write .feature file to disk with Gherkin formatting"""
        lines = []
        
        # Provenance header
        lines.append(f"# Generated by Fishnet v2.0.0")
        lines.append(f"# Strategy: {', '.join(s.strategy_used for s in feature_file.scenarios)}")
        lines.append(f"# Source: {feature_file.behavior_spec.source_file if feature_file.behavior_spec else 'unknown'}")
        lines.append(f"# Generated: {datetime.now().isoformat()}")
        lines.append("")
        
        # Feature header with tags
        if feature_file.tags:
            lines.append(" ".join(feature_file.tags))
        lines.append(f"Feature: {feature_file.feature_name}")
        lines.append(f"  {feature_file.feature_description}")
        lines.append("")
        
        # Background
        if feature_file.background_steps:
            lines.append("  Background:")
            for step in feature_file.background_steps:
                # Clean up "Given" prefix if already present
                step_clean = step.replace("Given ", "").replace("And ", "")
                lines.append(f"    {step_clean}")
            lines.append("")
        
        # Scenarios
        for scenario in feature_file.scenarios:
            lines.append(f"  @{scenario.scenario_type}")
            lines.append(f"  Scenario: {scenario.scenario_name}")
            
            for step in scenario.given_steps:
                lines.append(f"    Given {step}")
            for step in scenario.when_steps:
                lines.append(f"    When {step}")
            for step in scenario.then_steps:
                lines.append(f"    Then {step}")
            lines.append("")
        
        # Write to file
        output_path.write_text("\n".join(lines))


# Legacy Fishnet class for backward compatibility
class Fishnet:
    """
    Legacy Fishnet class - kept for backward compatibility.
    New code should use FishnetV2.
    """
    
    def __init__(self, workspace_path: Path):
        self.workspace_path = Path(workspace_path)
        
        # Setup directories
        self.catches_dir = self.workspace_path / "knowledge" / "catches"
        self.voyage_trials_dir = self.workspace_path / "santiago-pm" / "voyage-trials"
        
        self.catches_dir.mkdir(parents=True, exist_ok=True)
        self.voyage_trials_dir.mkdir(parents=True, exist_ok=True)
    
    async def generate_bdd_features(
        self,
        domain_name: str,
        behaviors: List[str],
        entities: List[Any],
        relationships: List[Any],
    ) -> List[BDDFeature]:
        """
        Generate BDD feature files from behaviors and knowledge.
        
        Args:
            domain_name: Domain being tested
            behaviors: List of behavior/tool names
            entities: Extracted entities from Catchfish
            relationships: Extracted relationships from Catchfish
            
        Returns:
            List of BDDFeature objects
        """
        print(f"\n🕸️  Fishnet: Generating BDD Features")
        print(f"   Domain: {domain_name}")
        print(f"   Behaviors: {len(behaviors)}")
        
        features = []
        
        for behavior in behaviors:
            feature = await self._generate_feature_for_behavior(
                domain_name, behavior, entities, relationships
            )
            features.append(feature)
        
        # Save features to files
        for feature in features:
            self._save_feature_file(domain_name, feature)
        
        print(f"   ✅ Generated {len(features)} feature files")
        return features
    
    async def generate_mcp_manifest(
        self,
        domain_name: str,
        behaviors: List[str],
        capability_level: CapabilityLevel = CapabilityLevel.JOURNEYMAN,
        knowledge_scope: KnowledgeScope = KnowledgeScope.LAKE,
        entities: Optional[List[Any]] = None,
    ) -> MCPManifest:
        """
        Generate MCP manifest from domain knowledge.
        
        Args:
            domain_name: Service name
            behaviors: List of tool names
            capability_level: Agent maturity level
            knowledge_scope: Knowledge breadth
            entities: Optional entities for metadata
            
        Returns:
            MCPManifest object
        """
        print(f"\n🕸️  Fishnet: Generating MCP Manifest")
        print(f"   Domain: {domain_name}")
        print(f"   Tools: {len(behaviors)}")
        print(f"   Capability: {capability_level.value}")
        print(f"   Scope: {knowledge_scope.value}")
        
        # Generate tools from behaviors
        tools = []
        for behavior in behaviors:
            tool = self._create_tool_from_behavior(behavior)
            tools.append(tool)
        
        # Create manifest
        manifest = MCPManifest(
            service_name=domain_name,
            version="1.0.0",
            description=f"Domain-specific Santiago for {domain_name}",
            capability_level=capability_level,
            knowledge_scope=knowledge_scope,
            tools=tools,
            metadata={
                "generated_at": datetime.now().isoformat(),
                "entity_count": len(entities) if entities else 0,
                "tool_count": len(tools),
            },
        )
        
        # Save manifest
        self._save_manifest(domain_name, manifest)
        
        print(f"   ✅ Manifest saved")
        return manifest
    
    async def analyze_coverage(
        self,
        domain_name: str,
        behaviors: List[str],
        features: List[BDDFeature],
    ) -> CoverageReport:
        """
        Analyze test coverage for behaviors.
        
        Args:
            domain_name: Domain being analyzed
            behaviors: All expected behaviors
            features: Generated BDD features
            
        Returns:
            CoverageReport with gaps and recommendations
        """
        print(f"\n🕸️  Fishnet: Analyzing Coverage")
        
        # Map features to behaviors
        feature_behaviors = {f.name.replace("_", " ").lower() for f in features}
        behavior_set = {b.replace("_", " ").lower() for b in behaviors}
        
        # Find covered behaviors
        behaviors_with_tests = feature_behaviors.intersection(behavior_set)
        
        # Calculate metrics
        total_scenarios = sum(len(f.scenarios) for f in features)
        coverage_ratio = len(behaviors_with_tests) / len(behaviors) if behaviors else 0.0
        
        # Find gaps
        gaps = list(behavior_set - feature_behaviors)
        
        # Generate recommendations
        recommendations = []
        if coverage_ratio < 0.8:
            recommendations.append("Coverage below 80% - add tests for missing behaviors")
        if gaps:
            recommendations.append(f"Add tests for: {', '.join(gaps)}")
        if total_scenarios < len(behaviors) * 2:
            recommendations.append("Average <2 scenarios per behavior - add edge cases")
        
        report = CoverageReport(
            total_behaviors=len(behaviors),
            behaviors_with_tests=len(behaviors_with_tests),
            total_scenarios=total_scenarios,
            coverage_ratio=coverage_ratio,
            gaps=gaps,
            recommendations=recommendations,
        )
        
        print(f"   Coverage: {coverage_ratio * 100:.1f}%")
        print(f"   Behaviors: {len(behaviors_with_tests)}/{len(behaviors)}")
        print(f"   Scenarios: {total_scenarios}")
        print(f"   Gaps: {len(gaps)}")
        
        return report
    
    async def _generate_feature_for_behavior(
        self,
        domain_name: str,
        behavior: str,
        entities: List[Any],
        relationships: List[Any],
    ) -> BDDFeature:
        """Generate BDD feature for single behavior"""
        
        feature_name = behavior.replace("_", " ").title()
        
        # Create 3 scenarios per behavior: basic, edge case, error
        scenarios = [
            self._create_basic_scenario(behavior),
            self._create_edge_case_scenario(behavior),
            self._create_error_scenario(behavior),
        ]
        
        feature = BDDFeature(
            feature_id=str(uuid4()),
            name=feature_name,
            description=f"Tests for {feature_name} behavior in {domain_name}",
            scenarios=scenarios,
            tags=[domain_name, "contract-test"],
        )
        
        return feature
    
    def _create_basic_scenario(self, behavior: str) -> BDDScenario:
        """Create basic happy-path scenario"""
        behavior_clean = behavior.replace("_", " ")
        
        return BDDScenario(
            scenario_id=str(uuid4()),
            name=f"Successfully {behavior_clean}",
            given_steps=[
                f"the {behavior_clean} service is available",
                "valid input parameters are provided",
            ],
            when_steps=[f"I request to {behavior_clean}"],
            then_steps=[
                "the operation succeeds",
                "a valid response is returned",
                "the result matches expected format",
            ],
            tags=["happy-path"],
        )
    
    def _create_edge_case_scenario(self, behavior: str) -> BDDScenario:
        """Create edge case scenario"""
        behavior_clean = behavior.replace("_", " ")
        
        return BDDScenario(
            scenario_id=str(uuid4()),
            name=f"{behavior_clean.title()} with edge cases",
            given_steps=[
                f"the {behavior_clean} service is available",
                "edge case parameters are provided",
            ],
            when_steps=[f"I request to {behavior_clean} with edge data"],
            then_steps=[
                "the operation handles edge cases correctly",
                "appropriate warnings or notifications are given",
                "the system remains stable",
            ],
            tags=["edge-case"],
        )
    
    def _create_error_scenario(self, behavior: str) -> BDDScenario:
        """Create error handling scenario"""
        behavior_clean = behavior.replace("_", " ")
        
        return BDDScenario(
            scenario_id=str(uuid4()),
            name=f"{behavior_clean.title()} error handling",
            given_steps=[
                f"the {behavior_clean} service is available",
                "invalid parameters are provided",
            ],
            when_steps=[f"I request to {behavior_clean} with invalid data"],
            then_steps=[
                "the operation fails gracefully",
                "a clear error message is returned",
                "no data corruption occurs",
            ],
            tags=["error-handling"],
        )
    
    def _create_tool_from_behavior(self, behavior: str) -> MCPTool:
        """Create MCP tool definition from behavior name"""
        
        # Infer tool type from behavior name
        if any(word in behavior.lower() for word in ["read", "get", "query", "list", "find"]):
            tool_type = "input"
        elif any(word in behavior.lower() for word in ["message", "send", "notify"]):
            tool_type = "communication"
        else:
            tool_type = "output"
        
        # Infer concurrency risk
        mutates_kg = any(word in behavior.lower() for word in ["create", "update", "delete", "modify"])
        
        return MCPTool(
            name=behavior,
            description=f"Tool for {behavior.replace('_', ' ')}",
            tool_type=tool_type,
            parameters={"input": "object"},
            returns={"result": "object"},
            concurrency_risk=mutates_kg,
            mutates_kg=mutates_kg,
        )
    
    def _save_feature_file(self, domain_name: str, feature: BDDFeature) -> None:
        """Save BDD feature to .feature file"""
        
        catch_dir = self.catches_dir / domain_name / "bdd-tests"
        catch_dir.mkdir(parents=True, exist_ok=True)
        
        feature_file = catch_dir / f"{feature.name.lower().replace(' ', '_')}.feature"
        
        # Generate Gherkin content
        content = self._generate_gherkin(feature)
        
        with open(feature_file, 'w') as f:
            f.write(content)
    
    def _generate_gherkin(self, feature: BDDFeature) -> str:
        """Generate Gherkin text from BDDFeature"""
        
        lines = []
        
        # Feature header
        if feature.tags:
            lines.append("@" + " @".join(feature.tags))
        lines.append(f"Feature: {feature.name}")
        lines.append(f"  {feature.description}")
        lines.append("")
        
        # Background
        if feature.background_steps:
            lines.append("  Background:")
            for step in feature.background_steps:
                lines.append(f"    {step}")
            lines.append("")
        
        # Scenarios
        for scenario in feature.scenarios:
            if scenario.tags:
                lines.append("  @" + " @".join(scenario.tags))
            lines.append(f"  Scenario: {scenario.name}")
            
            for step in scenario.given_steps:
                lines.append(f"    Given {step}")
            for step in scenario.when_steps:
                lines.append(f"    When {step}")
            for step in scenario.then_steps:
                lines.append(f"    Then {step}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _save_manifest(self, domain_name: str, manifest: MCPManifest) -> None:
        """Save MCP manifest to JSON file"""
        
        catch_dir = self.catches_dir / domain_name
        catch_dir.mkdir(parents=True, exist_ok=True)
        
        manifest_file = catch_dir / "mcp-manifest.json"
        
        manifest_data = {
            "service": {
                "name": manifest.service_name,
                "version": manifest.version,
                "description": manifest.description,
            },
            "capabilities": {
                "level": manifest.capability_level.value,
                "knowledge_scope": manifest.knowledge_scope.value,
            },
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "type": tool.tool_type,
                    "parameters": tool.parameters,
                    "returns": tool.returns,
                    "concurrency_risk": tool.concurrency_risk,
                    "mutates_kg": tool.mutates_kg,
                }
                for tool in manifest.tools
            ],
            "budget_hint_usd_per_day": manifest.budget_hint_usd_per_day,
            "metadata": manifest.metadata,
        }
        
        with open(manifest_file, 'w') as f:
            json.dump(manifest_data, f, indent=2)


# CLI Interface for standalone execution
def main():
    """CLI entry point for Fishnet v2.0.0"""
    parser = argparse.ArgumentParser(
        description='Fishnet v2.0.0 - Multi-strategy BDD test generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Generate BDD tests using BottomUp strategy
  python fishnet.py \
    --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \
    --ontology knowledge/ontologies/pm-domain-ontology.ttl \
    --output bdd-tests/ \
    --strategies bottom_up
        '''
    )
    
    parser.add_argument(
        '--behaviors',
        required=True,
        help='Path to behaviors extraction file (pm-behaviors-extracted.md)'
    )
    parser.add_argument(
        '--ontology',
        required=True,
        help='Path to ontology .ttl file (pm-domain-ontology.ttl)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output directory for .feature files'
    )
    parser.add_argument(
        '--strategies',
        nargs='+',
        default=['bottom_up'],
        choices=['bottom_up', 'top_down', 'external', 'logic', 'experiment'],
        help='BDD generation strategies to use (default: bottom_up)'
    )
    
    args = parser.parse_args()
    
    # Create Fishnet instance
    fishnet = FishnetV2(
        behaviors_file=Path(args.behaviors),
        ontology_file=Path(args.ontology),
        output_dir=Path(args.output)
    )
    
    # Generate BDD files
    results = fishnet.generate_all_bdd_files(strategy_names=args.strategies)
    
    # Print summary
    print(f"\n📊 Generation Summary:")
    print(f"   Total Behaviors: {results['total_behaviors']}")
    print(f"   Files Generated: {results['files_generated']}")
    print(f"   Scenarios Generated: {results['scenarios_generated']}")
    print(f"   Output Directory: {results['output_dir']}")
    print(f"\n✅ Validate with: behave --dry-run {results['output_dir']}")


if __name__ == '__main__':
    main()

