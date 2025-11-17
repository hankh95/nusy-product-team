"""
Navigator Demo - 10-Step Fishing Process

Demonstrates the Navigator orchestrating a complete fishing expedition
to build a domain-specific Santiago (santiago-pm-safe-xp example).

This shows:
- 10-step process execution
- 3-5 validation cycles with quality gates
- Metrics tracking and improvement over cycles
- Expedition logging to voyage-trials/
- MCP manifest generation
"""

import asyncio
from pathlib import Path

from nusy_orchestrator.santiago_builder.navigator import Navigator


async def main():
    """Run Navigator demonstration"""
    
    print("="*80)
    print("           Navigator 10-Step Fishing Process Demo")
    print("="*80)
    print("\nBuilding: santiago-pm-safe-xp")
    print("Sources: SAFe + XP documentation")
    print("Target: Product Management behaviors\n")
    
    # Initialize Navigator
    workspace_path = Path(__file__).parent
    navigator = Navigator(
        workspace_path=workspace_path,
        min_cycles=3,
        max_cycles=5,
        target_bdd_pass_rate=0.95,
        target_extraction_time=900,  # 15 minutes
    )
    
    # Define expedition parameters
    domain_name = "santiago-pm-safe-xp"
    
    # Simulate source files (create dummy files for demo)
    sources_dir = workspace_path / "test_workspace" / "demo_sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    
    safe_source = sources_dir / "safe_agile_guide.md"
    xp_source = sources_dir / "xp_explained.md"
    
    # Create dummy sources
    safe_source.write_text("""# SAFe Agile Framework
    
Product Management in SAFe involves:
- Program backlog management
- Strategic themes alignment
- PI planning coordination
- Value stream optimization
""")
    
    xp_source.write_text("""# Extreme Programming Explained

XP Product Management practices:
- User stories with INVEST criteria
- Small batch sizes for rapid feedback
- Continuous planning and adaptation
- Test-first development
""")
    
    sources = [safe_source, xp_source]
    
    # Define target behaviors (MCP tools)
    target_behaviors = [
        "create_backlog",
        "prioritize_stories",
        "define_acceptance_criteria",
        "plan_iteration",
        "track_velocity",
    ]
    
    # Define hypotheses
    hypotheses = [
        "Combining SAFe strategic alignment with XP tactical practices yields better PM outcomes",
        "Small batch sizes from XP improve SAFe program increment planning",
        "Test-first thinking enhances SAFe acceptance criteria definition",
    ]
    
    # Run fishing expedition
    try:
        expedition = await navigator.run_expedition(
            domain_name=domain_name,
            sources=sources,
            target_behaviors=target_behaviors,
            hypotheses=hypotheses,
        )
        
        # Print final summary
        print("\n" + "="*80)
        print("                     Expedition Summary")
        print("="*80)
        print(f"\n📋 Expedition ID: {expedition.expedition_id}")
        print(f"🎯 Domain: {expedition.domain_name}")
        print(f"📊 Status: {expedition.status}")
        print(f"\n⏱️  Timeline:")
        print(f"   Started: {expedition.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Completed: {expedition.completed_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Duration: {expedition.final_metrics['total_time_seconds'] / 60:.1f} minutes")
        
        print(f"\n🔄 Validation Cycles: {expedition.final_metrics['total_cycles']}")
        for cycle in expedition.cycles:
            status_emoji = "✅" if cycle.status.value == "passed" else "❌"
            print(f"   {status_emoji} Cycle {cycle.cycle_number}: "
                  f"{cycle.bdd_pass_rate * 100:.1f}% pass rate, "
                  f"{cycle.extraction_time_seconds:.1f}s extraction")
        
        print(f"\n📈 Final Metrics:")
        print(f"   BDD Pass Rate: {expedition.final_metrics['final_bdd_pass_rate'] * 100:.1f}%")
        print(f"   Avg Extraction Time: {expedition.final_metrics['avg_extraction_time_seconds'] / 60:.1f} minutes")
        print(f"   Sources Processed: {expedition.final_metrics['sources_processed']}")
        print(f"   Behaviors Implemented: {expedition.final_metrics['behaviors_implemented']}")
        print(f"   Quality Gate Met: {expedition.final_metrics['quality_gate_met']}")
        
        print(f"\n💡 Hypotheses Validated:")
        for i, hypothesis in enumerate(expedition.hypotheses, 1):
            print(f"   {i}. {hypothesis}")
        
        print(f"\n📚 Lessons Learned:")
        learning_decision = next(
            (d for d in expedition.decisions if d.get("step") == "learning"),
            None
        )
        if learning_decision:
            for lesson in learning_decision.get("lessons_learned", []):
                print(f"   💡 {lesson}")
        
        print(f"\n📦 Deliverables:")
        catch_dir = workspace_path / "knowledge" / "catches" / domain_name
        if catch_dir.exists():
            print(f"   ✅ MCP Manifest: {catch_dir / 'mcp-manifest.json'}")
        
        voyage_trials_dir = workspace_path / "santiago-pm" / "voyage-trials"
        expedition_logs = list(voyage_trials_dir.glob(f"expedition_{domain_name}_*.json"))
        if expedition_logs:
            print(f"   ✅ Expedition Log: {expedition_logs[-1]}")
        
        print("\n" + "="*80)
        print("                  🎉 Expedition Complete! 🎉")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Expedition failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
