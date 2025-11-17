#!/usr/bin/env python3
"""
Run Task 12: Navigator Expedition on santiago-pm Domain

Executes full fishing expedition to create santiago-pm-self-aware catch.
This validates Santiago can understand its own PM domain (bootstrap capability).
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from nusy_orchestrator.santiago_builder.navigator import Navigator


# 20 PM behaviors extracted in Task 11
SANTIAGO_PM_BEHAVIORS = [
    "status_query",
    "status_transition",
    "status_dashboard",
    "create_feature",
    "prioritize_backlog",
    "define_acceptance_criteria",
    "track_velocity",
    "update_backlog",
    "log_issue",
    "link_issue_to_feature",
    "design_experiment",
    "record_experiment_results",
    "analyze_experiment_outcomes",
    "create_note",
    "link_related_notes",
    "query_note_network",
    "define_vision",
    "create_roadmap",
    "run_quality_gate",
    "generate_quality_report",
]


async def run_santiago_pm_expedition():
    """Execute Navigator expedition on santiago-pm domain"""
    
    print("=" * 80)
    print("TASK 12: NAVIGATOR EXPEDITION ON SANTIAGO-PM DOMAIN")
    print("=" * 80)
    print()
    print("Goal: Create santiago-pm-self-aware catch")
    print("Behaviors: 20 PM tools")
    print("Sources: ~59 markdown files from santiago-pm/")
    print()
    
    # Initialize Navigator
    navigator = Navigator(workspace_path=project_root)
    
    # Collect santiago-pm sources
    santiago_pm_dir = project_root / "santiago-pm"
    sources = list(santiago_pm_dir.rglob("*.md"))
    
    print(f"📚 Found {len(sources)} markdown files in santiago-pm/")
    print()
    
    # Filter out very large files or test files
    sources = [s for s in sources if s.stat().st_size < 1_000_000]  # < 1MB
    sources = sources[:20]  # Limit to 20 files for reasonable processing time
    
    print(f"📋 Processing {len(sources)} source files:")
    for source in sources[:10]:
        print(f"   - {source.relative_to(project_root)}")
    if len(sources) > 10:
        print(f"   ... and {len(sources) - 10} more")
    print()
    
    # Define hypotheses
    hypotheses = [
        "Santiago can extract PM knowledge from its own documentation",
        "20 PM behaviors can be validated through BDD tests",
        "Self-aware MCP manifest enables Santiago to manage itself",
        "Bootstrap loop: Santiago uses its own domain to improve itself",
    ]
    
    # Run expedition
    try:
        expedition = await navigator.run_expedition(
            domain_name="santiago-pm",
            sources=sources,
            target_behaviors=SANTIAGO_PM_BEHAVIORS,
            hypotheses=hypotheses
        )
        
        print("\n" + "=" * 80)
        print("EXPEDITION RESULTS")
        print("=" * 80)
        print(f"✅ Status: {expedition.status}")
        print(f"🆔 Expedition ID: {expedition.expedition_id}")
        print(f"🔄 Cycles Completed: {len(expedition.cycles)}")
        print(f"⏱️  Total Time: {expedition.final_metrics.get('total_time_seconds', 0) / 60:.1f} minutes")
        print(f"📊 Final BDD Pass Rate: {expedition.final_metrics.get('final_bdd_pass_rate', 0) * 100:.1f}%")
        print(f"✅ Quality Gate Met: {expedition.final_metrics.get('quality_gate_met', False)}")
        print()
        
        # Show expedition artifacts
        print("📦 Expedition Artifacts:")
        catch_dir = project_root / "knowledge" / "catches" / "santiago-pm"
        if catch_dir.exists():
            print(f"   📁 Catch Directory: {catch_dir}")
            manifest = catch_dir / "mcp-manifest.json"
            if manifest.exists():
                print(f"   ✅ MCP Manifest: {manifest}")
            bdd_dir = catch_dir / "bdd-tests"
            if bdd_dir.exists():
                bdd_files = list(bdd_dir.glob("*.feature"))
                print(f"   ✅ BDD Tests: {len(bdd_files)} feature files")
        
        print()
        print("🎉 Task 12 Complete: Santiago-PM expedition successful!")
        print("   Santiago now understands its own PM domain!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Expedition Failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_santiago_pm_expedition())
    sys.exit(exit_code)
