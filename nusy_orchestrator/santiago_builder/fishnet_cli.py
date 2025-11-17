#!/usr/bin/env python3
"""Fishnet CLI - Multi-Strategy BDD Test Generator

Command-line interface for generating BDD test files from PM behavior documentation.

Usage:
    python fishnet_cli.py \\
      --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \\
      --ontology knowledge/ontologies/pm-domain-ontology.ttl \\
      --output bdd-tests/ \\
      --strategies bottom_up
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from nusy_orchestrator.santiago_builder.fishnet import FishnetCLI
from nusy_orchestrator.santiago_builder.fishnet_strategies.bottom_up_strategy import BottomUpStrategy


def main():
    parser = argparse.ArgumentParser(
        description="Fishnet v2.0.0 - Multi-Strategy BDD Test Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate BDD tests using bottom-up strategy
  python fishnet_cli.py \\
    --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \\
    --ontology knowledge/ontologies/pm-domain-ontology.ttl \\
    --output bdd-tests/ \\
    --strategies bottom_up

  # Multiple strategies (future)
  python fishnet_cli.py \\
    --behaviors pm-behaviors-extracted.md \\
    --ontology pm-domain-ontology.ttl \\
    --output tests/ \\
    --strategies bottom_up,top_down
        """
    )
    
    parser.add_argument(
        "--behaviors",
        type=str,
        required=True,
        help="Path to pm-behaviors-extracted.md file"
    )
    
    parser.add_argument(
        "--ontology",
        type=str,
        required=True,
        help="Path to pm-domain-ontology.ttl file"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output directory for .feature files"
    )
    
    parser.add_argument(
        "--strategies",
        type=str,
        default="bottom_up",
        help="Comma-separated list of strategies (default: bottom_up)"
    )
    
    args = parser.parse_args()
    
    # Parse strategies
    strategy_names = [s.strip() for s in args.strategies.split(",")]
    
    # Validate paths
    behaviors_path = Path(args.behaviors)
    ontology_path = Path(args.ontology)
    
    if not behaviors_path.exists():
        print(f"❌ Error: Behaviors file not found: {behaviors_path}")
        return 1
    
    if not ontology_path.exists():
        print(f"⚠️  Warning: Ontology file not found: {ontology_path}")
        print("   Continuing without ontology validation...")
    
    # Create Fishnet CLI instance
    fishnet = FishnetCLI(
        behaviors_file=behaviors_path,
        ontology_file=ontology_path,
        output_dir=Path(args.output)
    )
    
    # Register available strategies
    fishnet.register_strategy("bottom_up", BottomUpStrategy())
    # Future strategies can be registered here:
    # fishnet.register_strategy("top_down", TopDownStrategy(ontology_path))
    # fishnet.register_strategy("external", ExternalStrategy())
    
    # Validate requested strategies
    available = set(fishnet.strategies.keys())
    requested = set(strategy_names)
    unknown = requested - available
    
    if unknown:
        print(f"❌ Error: Unknown strategies: {', '.join(unknown)}")
        print(f"   Available strategies: {', '.join(available)}")
        return 1
    
    try:
        # Generate BDD files
        results = fishnet.generate_all_bdd_files(strategy_names=strategy_names)
        
        print(f"\n✅ Success!")
        print(f"   Generated {results['files_generated']} feature files")
        print(f"   Covering {results['total_behaviors']} behaviors")
        print(f"   Total scenarios: {results['files_generated'] * 3}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
