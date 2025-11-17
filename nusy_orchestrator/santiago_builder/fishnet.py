"""Fishnet - BDD Test + MCP Manifest Generation

Generates behavior-driven development tests and service manifests from domain knowledge:

1. BDD Feature Files (.feature)
   - Gherkin scenarios for each behavior/tool
   - Linked to knowledge nodes for traceability
   - Contract acceptance tests
   - Coverage tracking

2. MCP Manifest (mcp-manifest.json)
   - Service contract with tools
   - Capability levels (Apprentice/Journeyman/Master)
   - Knowledge scope (Pond/Lake/Sea/Ocean)
   - Concurrency risk annotations
   - Budget hints

3. Test Coverage Analysis
   - Coverage ratio per behavior
   - Gap detection for missing tests
   - Traceability to knowledge graph nodes

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

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


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


class Fishnet:
    """
    Generates BDD tests and MCP manifests from domain knowledge.
    
    Analyzes knowledge graph (entities, relationships, behaviors)
    and produces:
    - .feature files with Gherkin scenarios
    - mcp-manifest.json with service contract
    - Coverage reports with gap analysis
    
    Usage:
        fishnet = Fishnet(workspace_path)
        features = await fishnet.generate_bdd_features(
            domain_name="santiago-pm-safe-xp",
            behaviors=["create_backlog", "prioritize_stories"],
            entities=[...]
        )
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


class FishnetCLI:
    """CLI-focused orchestrator for multi-strategy BDD generation
    
    Loads behaviors from markdown files and generates .feature files
    using pluggable generation strategies.
    
    Usage:
        fishnet = FishnetCLI(
            behaviors_file="pm-behaviors-extracted.md",
            ontology_file="pm-domain-ontology.ttl",
            output_dir="bdd-tests/"
        )
        results = fishnet.generate_all_bdd_files(strategies=["bottom_up"])
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
        self.strategies = {}
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def register_strategy(self, name: str, strategy: Any) -> None:
        """Register a BDD generation strategy
        
        Args:
            name: Strategy name (e.g., "bottom_up")
            strategy: Strategy instance implementing BDDGenerationStrategy
        """
        self.strategies[name] = strategy
    
    def generate_all_bdd_files(
        self,
        strategy_names: List[str] = None
    ) -> Dict[str, Any]:
        """Generate BDD .feature files for all behaviors
        
        Args:
            strategy_names: List of strategies to use (default: all registered)
            
        Returns:
            Dict with generation results and statistics
        """
        if strategy_names is None:
            strategy_names = list(self.strategies.keys())
        
        # Validate strategies
        for name in strategy_names:
            if name not in self.strategies:
                raise ValueError(f"Unknown strategy: {name}")
        
        # Load behaviors from markdown files
        behaviors = self._load_behaviors()
        
        print(f"\n🕸️  Fishnet v2.0.0: Multi-Strategy BDD Generation")
        print(f"   Behaviors: {len(behaviors)}")
        print(f"   Strategies: {', '.join(strategy_names)}")
        print(f"   Output: {self.output_dir}")
        print()
        
        results = {
            "total_behaviors": len(behaviors),
            "files_generated": 0,
            "strategies_used": strategy_names,
            "files": []
        }
        
        # Generate feature files for each behavior
        for behavior in behaviors:
            for strategy_name in strategy_names:
                strategy = self.strategies[strategy_name]
                
                # Generate feature file
                feature_file = strategy.generate_feature_file(behavior)
                
                # Write to disk
                filename = f"{behavior.name}_{strategy_name}.feature"
                output_path = self.output_dir / filename
                
                with open(output_path, 'w') as f:
                    f.write(feature_file.to_gherkin())
                
                results["files_generated"] += 1
                results["files"].append(str(output_path))
                
                print(f"   ✅ {filename} ({len(feature_file.scenarios)} scenarios)")
        
        print(f"\n   📊 Generated {results['files_generated']} .feature files")
        print(f"   📁 Output directory: {self.output_dir}")
        
        return results
    
    def _load_behaviors(self) -> List[Any]:
        """Load behaviors from markdown files
        
        Parses pm-behaviors-extracted.md and passage-behaviors-extracted.md
        to extract BehaviorSpec objects.
        
        Returns:
            List of BehaviorSpec objects
        """
        from .fishnet_strategies.base_strategy import BehaviorSpec
        
        behaviors = []
        
        # Parse the main behaviors file
        if self.behaviors_file.exists():
            behaviors.extend(self._parse_behavior_file(self.behaviors_file))
        
        # Check for passage behaviors file in same directory
        passage_file = self.behaviors_file.parent / "passage-behaviors-extracted.md"
        if passage_file.exists():
            behaviors.extend(self._parse_behavior_file(passage_file))
        
        return behaviors
    
    def _parse_behavior_file(self, filepath: Path) -> List[Any]:
        """Parse a behavior markdown file
        
        Args:
            filepath: Path to markdown file
            
        Returns:
            List of BehaviorSpec objects
        """
        from .fishnet_strategies.base_strategy import BehaviorSpec
        
        behaviors = []
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Split by behavior sections (### Behavior X.Y:)
        behavior_sections = re.split(r'\n### Behavior \d+\.\d+:', content)
        
        for section in behavior_sections[1:]:  # Skip preamble
            behavior = self._parse_behavior_section(section, filepath.name)
            if behavior:
                behaviors.append(behavior)
        
        return behaviors
    
    def _parse_behavior_section(self, section: str, source_file: str) -> Any:
        """Parse a single behavior section
        
        Args:
            section: Markdown section text
            source_file: Source filename for provenance
            
        Returns:
            BehaviorSpec or None if parsing fails
        """
        from .fishnet_strategies.base_strategy import BehaviorSpec
        
        lines = section.strip().split('\n')
        
        # Extract basic info
        name = ""
        description = ""
        capability_level = "Journeyman"
        knowledge_scope = "Lake"
        mutates_kg = False
        concurrency_safe = True
        ontology_mapping = ""
        cli_example = ""
        sparql_query = ""
        
        # Parse markdown sections
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Title line (behavior name)
            if i == 0 and line:
                name = line.split(':')[0].strip() if ':' in line else line
                name = name.lower().replace(' ', '_').replace('-', '_')
            
            # Named fields
            if line.startswith("**Name**:"):
                name = line.split(":", 1)[1].strip().strip('`')
            elif line.startswith("**Description**:"):
                description = line.split(":", 1)[1].strip()
            elif line.startswith("**Capability Level**:"):
                capability_level = line.split(":", 1)[1].strip().split()[0]
            elif line.startswith("**Knowledge Scope**:"):
                knowledge_scope = line.split(":", 1)[1].strip().split()[0]
            elif line.startswith("**Mutates KG**:"):
                mutates_kg = "Yes" in line or "True" in line
            elif line.startswith("**Concurrency Safe**:"):
                concurrency_safe = "Yes" in line or "True" in line
            elif line.startswith("**Maps to Ontology**:"):
                ontology_mapping = line.split(":", 1)[1].strip().split()[0].strip('`')
            elif line.startswith("**CLI Example**:"):
                cli_example = line.split(":", 1)[1].strip().strip('`')
            
            i += 1
        
        # Extract JSON schemas (simplified - look for code blocks)
        input_schema = {"properties": {}, "required": []}
        output_schema = {"properties": {}}
        
        # Extract input schema
        input_match = re.search(r'\*\*Input Schema\*\*:\s*```json\s*(\{.*?\})\s*```', 
                                section, re.DOTALL)
        if input_match:
            try:
                input_schema = json.loads(input_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Extract output schema
        output_match = re.search(r'\*\*Output Schema\*\*:\s*```json\s*(\{.*?\})\s*```', 
                                 section, re.DOTALL)
        if output_match:
            try:
                output_schema = json.loads(output_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Extract SPARQL query
        sparql_match = re.search(r'\*\*SPARQL Query\*\*:\s*```sparql\s*(.*?)```', 
                                 section, re.DOTALL)
        if sparql_match:
            sparql_query = sparql_match.group(1).strip()
        
        if not name:
            return None
        
        return BehaviorSpec(
            name=name,
            description=description or f"Behavior for {name}",
            capability_level=capability_level,
            knowledge_scope=knowledge_scope,
            input_schema=input_schema,
            output_schema=output_schema,
            mutates_kg=mutates_kg,
            concurrency_safe=concurrency_safe,
            ontology_mapping=ontology_mapping,
            cli_example=cli_example,
            sparql_query=sparql_query,
            source_file=source_file,
            behavior_id=name
        )
