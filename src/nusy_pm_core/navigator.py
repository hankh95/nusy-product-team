"""Navigator Module: Orchestrates the Neurosymbolic pipeline."""

from typing import Dict, List
from pathlib import Path
from .seawater import SeawaterProcessor
from .catchfish import CatchFishProcessor
from .fishnet import FishNetGenerator
from .knowledge.graph import KnowledgeGraph


class Navigator:
    """Orchestrates the complete Neurosymbolic pipeline."""

    def __init__(self, notes_dir: Path, kg: KnowledgeGraph):
        self.notes_dir = notes_dir
        self.kg = kg
        self.seawater = SeawaterProcessor(notes_dir)
        self.catchfish = CatchFishProcessor()
        self.fishnet = FishNetGenerator()

    def run_pipeline(self) -> Dict:
        """Run the complete pipeline: Seawater -> CatchFish -> FishNet."""
        results = {}

        # Step 1: Process notes with Seawater
        l0_content = self.seawater.process_notes_directory()
        results['l0_content'] = l0_content

        # Step 2: Convert to KG with CatchFish
        triples_added = self.catchfish.process_l0_content(l0_content, self.kg)
        results['triples_added'] = triples_added

        # Step 3: Generate BDD scenarios with FishNet
        scenarios = self.fishnet.generate_scenarios(self.kg)
        results['scenarios'] = scenarios

        return results

    def validate_coverage(self) -> Dict:
        """Validate that all note behaviors are covered."""
        # Generate scenarios
        scenarios = self.fishnet.generate_scenarios(self.kg)

        # Check KG coverage
        coverage = {
            'total_scenarios': len(scenarios),
            'kg_triples': len(list(self.kg.g)),
            'notes_processed': len(list(self.notes_dir.glob('*.md'))) if self.notes_dir.exists() else 0
        }

        return coverage