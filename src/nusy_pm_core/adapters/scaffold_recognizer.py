"""
Santiago PM Domain Scaffold Recognition System

This module enables Santiago to learn domain organization patterns by studying
the santiago-pm/ folder structure. The folder structure synthesizes PM expertise
from multiple sources:
- EARS methodology (initial inspiration for project scaffolding)
- External PM thought leaders (Jeff Patton, Jeff Gothelf, Nielsen Norman, SAFe)
- Internal domain knowledge (vision docs, architecture patterns)
- Human PM experience (real-world practices)

Meta-learning: Santiago learns how to organize domains by studying itself.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set
import yaml
import re


@dataclass
class FolderPattern:
    """A recognized folder pattern that can be suggested for new domains."""
    
    name: str
    purpose: str
    typical_files: List[str]
    required_files: List[str]
    template_file: Optional[str]
    related_patterns: List[str]
    learned_from: str  # Which source contributed this pattern
    
    def similarity_score(self, existing_folder: Path) -> float:
        """Calculate similarity between this pattern and an existing folder."""
        if not existing_folder.exists():
            return 0.0
            
        existing_files = {f.name for f in existing_folder.iterdir() if f.is_file()}
        required_match = sum(1 for f in self.required_files if f in existing_files)
        typical_match = sum(1 for f in self.typical_files if f in existing_files)
        
        # Weight required files more heavily
        total_possible = len(self.required_files) * 2 + len(self.typical_files)
        if total_possible == 0:
            return 0.0
            
        score = (required_match * 2 + typical_match) / total_possible
        return score


@dataclass
class ScaffoldSuggestion:
    """A suggestion for creating a new folder based on learned patterns."""
    
    suggested_path: str
    pattern: FolderPattern
    confidence: float
    reasoning: str
    similar_to: List[str]  # Existing folders this is similar to
    

class ScaffoldRecognizer:
    """
    Learns folder structure patterns from santiago-pm/ and suggests
    contextually appropriate structures for new domains.
    """
    
    def __init__(self, santiago_pm_root: Path):
        self.root = santiago_pm_root
        self.patterns: Dict[str, FolderPattern] = {}
        self.folder_relationships: Dict[str, Set[str]] = {}
        
    def learn_patterns(self) -> Dict[str, FolderPattern]:
        """
        Scan santiago-pm/ to learn organizational patterns.
        
        Returns:
            Dictionary mapping pattern names to FolderPattern objects
        """
        # Learn PM artifact folder patterns
        self._learn_pm_artifact_patterns()
        
        # Learn tackle (implementation) patterns
        self._learn_tackle_patterns()
        
        # Learn relationship patterns
        self._learn_folder_relationships()
        
        return self.patterns
    
    def _learn_pm_artifact_patterns(self):
        """Learn patterns from PM artifact folders (cargo-manifests, ships-logs, etc.)"""
        pm_folders = [
            ("cargo-manifests", "Feature specifications (BDD/Gherkin)"),
            ("ships-logs", "Issue tracking and incident logs"),
            ("voyage-trials", "Experiment design and execution"),
            ("navigation-charts", "Development plans and roadmaps"),
            ("captains-journals", "Knowledge capture and insights"),
            ("research-logs", "Research findings and analysis"),
            ("crew-manifests", "Agent roles and responsibilities"),
            ("quality-assessments", "Testing and quality metrics"),
            ("strategic-charts", "Vision and strategic planning"),
        ]
        
        for folder_name, purpose in pm_folders:
            folder_path = self.root / folder_name
            if not folder_path.exists():
                continue
                
            # Analyze what files exist
            files = [f.name for f in folder_path.iterdir() if f.is_file()]
            
            # Identify template file
            template_file = next(
                (f for f in files if 'template' in f.lower()),
                None
            )
            
            # Create pattern
            self.patterns[folder_name] = FolderPattern(
                name=folder_name,
                purpose=purpose,
                typical_files=["README.md", template_file] if template_file else ["README.md"],
                required_files=["README.md"],
                template_file=template_file,
                related_patterns=[],  # Will be populated in relationship learning
                learned_from="santiago-pm PM artifact structure"
            )
    
    def _learn_tackle_patterns(self):
        """Learn patterns from tackle/ implementation folders."""
        tackle_path = self.root / "tackle"
        if not tackle_path.exists():
            return
            
        # Scan existing tackle implementations
        for tackle_folder in tackle_path.iterdir():
            if not tackle_folder.is_dir():
                continue
                
            tackle_name = tackle_folder.name
            files = [f.name for f in tackle_folder.iterdir() if f.is_file()]
            
            # Identify common implementation patterns
            has_models = any('model' in f for f in files)
            has_services = any('service' in f for f in files)
            has_cli = any('cli' in f for f in files)
            has_kg = any('kg' in f for f in files)
            has_tests = any('test' in f for f in files)
            has_dev_plan = 'development-plan.md' in files
            
            typical_files = []
            if has_models:
                typical_files.append(f"{tackle_name}_models.py")
            if has_services:
                typical_files.append(f"{tackle_name}_services.py")
            if has_cli:
                typical_files.append(f"{tackle_name}_cli.py")
            if has_kg:
                typical_files.append(f"{tackle_name}_kg.py")
            if has_tests:
                typical_files.extend([f"test_{tackle_name}.py"])
            if has_dev_plan:
                typical_files.append("development-plan.md")
            
            self.patterns[f"tackle_{tackle_name}"] = FolderPattern(
                name=f"tackle/{tackle_name}",
                purpose=f"Implementation module for {tackle_name} domain",
                typical_files=typical_files,
                required_files=["README.md", "development-plan.md"],
                template_file=None,
                related_patterns=[],
                learned_from=f"santiago-pm/tackle/{tackle_name} implementation"
            )
    
    def _learn_folder_relationships(self):
        """
        Learn which folders tend to work together.
        
        For example:
        - cargo-manifests (features) → voyage-trials (experiments to validate features)
        - ships-logs (issues) → quality-assessments (tests that caught issues)
        - navigation-charts (plans) → cargo-manifests (features in those plans)
        """
        # Read README files to understand relationships
        for pattern_name, pattern in self.patterns.items():
            folder_path = self.root / pattern_name.replace("tackle_", "tackle/")
            readme_path = folder_path / "README.md"
            
            if not readme_path.exists():
                continue
                
            # Simple heuristic: look for folder names mentioned in README
            content = readme_path.read_text()
            related = set()
            
            for other_pattern in self.patterns.keys():
                if other_pattern != pattern_name:
                    # Check if other pattern's folder is mentioned
                    folder_name = other_pattern.replace("tackle_", "")
                    if folder_name in content.lower():
                        related.add(other_pattern)
            
            pattern.related_patterns = list(related)
            self.folder_relationships[pattern_name] = related
    
    def suggest_missing_folders(self, current_structure: Path) -> List[ScaffoldSuggestion]:
        """
        Analyze current folder structure and suggest missing folders based on learned patterns.
        
        Args:
            current_structure: Path to analyze (could be santiago-pm/ or a new domain)
            
        Returns:
            List of suggestions for folders that should exist based on learned patterns
        """
        suggestions = []
        existing_folders = {f.name for f in current_structure.iterdir() if f.is_dir()}
        
        # Check for missing PM artifact folders
        pm_artifact_patterns = [
            p for p in self.patterns.values()
            if not p.name.startswith("tackle/")
        ]
        
        for pattern in pm_artifact_patterns:
            if pattern.name not in existing_folders:
                # Calculate confidence based on related folders that do exist
                related_present = sum(
                    1 for rel in pattern.related_patterns
                    if rel in existing_folders
                )
                confidence = related_present / max(len(pattern.related_patterns), 1)
                
                if confidence > 0.3:  # Only suggest if reasonably related folders exist
                    suggestions.append(ScaffoldSuggestion(
                        suggested_path=str(current_structure / pattern.name),
                        pattern=pattern,
                        confidence=confidence,
                        reasoning=f"Related folders exist: {[r for r in pattern.related_patterns if r in existing_folders]}",
                        similar_to=[r for r in pattern.related_patterns if r in existing_folders]
                    ))
        
        # Sort by confidence
        suggestions.sort(key=lambda s: s.confidence, reverse=True)
        return suggestions
    
    def suggest_tackle_implementation(self, domain_name: str, existing_tackles: List[str]) -> Optional[ScaffoldSuggestion]:
        """
        Suggest tackle implementation structure for a new domain based on learned patterns.
        
        Args:
            domain_name: Name of the domain to implement (e.g., "notes", "experiments")
            existing_tackles: List of existing tackle names to learn from
            
        Returns:
            Suggestion for implementing this tackle, or None if insufficient patterns
        """
        if not existing_tackles:
            return None
            
        # Find the most complete tackle implementation to use as template
        best_pattern = None
        best_score = 0
        
        for tackle_name in existing_tackles:
            pattern_key = f"tackle_{tackle_name}"
            if pattern_key in self.patterns:
                pattern = self.patterns[pattern_key]
                score = len(pattern.typical_files)
                if score > best_score:
                    best_score = score
                    best_pattern = pattern
        
        if not best_pattern:
            return None
            
        # Create suggestion based on best pattern
        return ScaffoldSuggestion(
            suggested_path=f"tackle/{domain_name}",
            pattern=FolderPattern(
                name=f"tackle/{domain_name}",
                purpose=f"Implementation module for {domain_name} domain",
                typical_files=[
                    f"{domain_name}_models.py",
                    f"{domain_name}_services.py",
                    f"{domain_name}_cli.py",
                    f"{domain_name}_kg.py",
                    f"test_{domain_name}.py",
                    "README.md",
                    "development-plan.md"
                ],
                required_files=["README.md", "development-plan.md"],
                template_file=None,
                related_patterns=best_pattern.related_patterns,
                learned_from=f"Synthesized from {best_pattern.learned_from}"
            ),
            confidence=0.9,  # High confidence since we have a good template
            reasoning=f"Following pattern from {best_pattern.name} which has {len(best_pattern.typical_files)} implementation files",
            similar_to=[best_pattern.name]
        )
    
    def export_learned_patterns(self, output_path: Path):
        """
        Export learned patterns to YAML for inspection and knowledge graph integration.
        
        Args:
            output_path: Path to write patterns YAML file
        """
        patterns_data = {
            "metadata": {
                "learned_from": str(self.root),
                "pattern_count": len(self.patterns),
                "sources": [
                    "santiago-pm PM artifact structure",
                    "santiago-pm/tackle implementations",
                    "EARS methodology (initial inspiration)",
                    "External PM thought leaders (Patton, Gothelf, Nielsen Norman, SAFe)",
                    "Internal vision docs and architecture patterns",
                    "Human PM experience"
                ]
            },
            "patterns": {}
        }
        
        for name, pattern in self.patterns.items():
            patterns_data["patterns"][name] = {
                "name": pattern.name,
                "purpose": pattern.purpose,
                "typical_files": pattern.typical_files,
                "required_files": pattern.required_files,
                "template_file": pattern.template_file,
                "related_patterns": pattern.related_patterns,
                "learned_from": pattern.learned_from
            }
        
        with open(output_path, 'w') as f:
            yaml.dump(patterns_data, f, default_flow_style=False, sort_keys=False)


def demo_scaffold_recognition():
    """Demo the scaffold recognition system on santiago-pm/"""
    santiago_pm_path = Path(__file__).parent.parent.parent.parent / "santiago-pm"
    
    print("=== Santiago PM Domain Scaffold Recognition Demo ===\n")
    print(f"Learning patterns from: {santiago_pm_path}\n")
    
    recognizer = ScaffoldRecognizer(santiago_pm_path)
    patterns = recognizer.learn_patterns()
    
    print(f"✅ Learned {len(patterns)} organizational patterns:\n")
    
    # Show PM artifact patterns
    pm_patterns = [p for p in patterns.values() if not p.name.startswith("tackle/")]
    print(f"📁 PM Artifact Patterns ({len(pm_patterns)}):")
    for pattern in pm_patterns:
        print(f"  - {pattern.name}: {pattern.purpose}")
        print(f"    Required: {pattern.required_files}")
        if pattern.template_file:
            print(f"    Template: {pattern.template_file}")
        if pattern.related_patterns:
            print(f"    Related to: {pattern.related_patterns[:3]}")
        print()
    
    # Show tackle patterns
    tackle_patterns = [p for p in patterns.values() if p.name.startswith("tackle/")]
    print(f"\n🔧 Tackle Implementation Patterns ({len(tackle_patterns)}):")
    for pattern in tackle_patterns:
        print(f"  - {pattern.name}")
        print(f"    Files: {len(pattern.typical_files)} typical implementation files")
        print(f"    Learned from: {pattern.learned_from}")
        print()
    
    # Suggest missing folders (simulate incomplete structure)
    print("\n💡 Suggestions for missing folders:")
    suggestions = recognizer.suggest_missing_folders(santiago_pm_path)
    if suggestions:
        for sugg in suggestions[:5]:  # Top 5
            print(f"  - {sugg.suggested_path}")
            print(f"    Confidence: {sugg.confidence:.1%}")
            print(f"    Reasoning: {sugg.reasoning}")
            print()
    else:
        print("  ✅ All expected folders present!")
    
    # Suggest tackle implementation for hypothetical "feedback" domain
    print("\n🆕 Suggesting tackle implementation for 'feedback' domain:")
    existing_tackles = [p.name.replace("tackle/", "") for p in tackle_patterns]
    feedback_suggestion = recognizer.suggest_tackle_implementation("feedback", existing_tackles)
    if feedback_suggestion:
        print(f"  Pattern: {feedback_suggestion.pattern.name}")
        print(f"  Files to create:")
        for file in feedback_suggestion.pattern.typical_files:
            print(f"    - {file}")
        print(f"  Confidence: {feedback_suggestion.confidence:.1%}")
        print(f"  Based on: {feedback_suggestion.similar_to}")
    
    # Export patterns
    output_path = santiago_pm_path.parent / "knowledge" / "catches" / "scaffold-patterns-learned.yaml"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    recognizer.export_learned_patterns(output_path)
    print(f"\n📄 Patterns exported to: {output_path}")
    
    print("\n✨ Meta-learning complete! Santiago learned how to organize domains by studying itself.")


if __name__ == "__main__":
    demo_scaffold_recognition()
