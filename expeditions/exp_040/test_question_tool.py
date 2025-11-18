"""
Test Question Tool Capability

Simple test to verify that the question tool capability has been
successfully added to all three Santiago entities.
"""

import sys
from pathlib import Path
import asyncio

# Add EXP paths
exp_039_path = Path(__file__).parent.parent / "exp_039"
exp_040_path = Path(__file__)
sys.path.insert(0, str(exp_039_path))
sys.path.insert(0, str(exp_040_path))

try:
    from entity_specialization import SantiagoEntityFactory
    from mcp_service_integration import IntegratedServiceRegistry
    from entity_architecture import Goal
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


async def test_question_tool():
    """Test that all entities have the question_asking capability."""

    print("Testing Question Tool Capability...")

    # Create service registry and entities
    registry = IntegratedServiceRegistry()
    factory = SantiagoEntityFactory(registry)
    entities = factory.create_all_entities()

    print(f"Created {len(entities)} entities")

    # Test each entity has question_asking capability
    for role, entity in entities.items():
        print(f"\n{role.upper()} Entity Capabilities:")
        capabilities = list(entity.capability_registry.capabilities.keys())
        print(f"  Total capabilities: {len(capabilities)}")
        print(f"  Capabilities: {capabilities}")

        # Check for question_asking capability
        has_question_tool = "question_asking" in capabilities
        print(f"  Has question_asking capability: {has_question_tool}")

        if has_question_tool:
            # Test executing the question capability
            question_goal = Goal(
                id=f"test_question_{role}",
                description="Question: What are the best practices for code reviews?",
                priority=1
            )

            try:
                result = await entity.capability_registry.get_capability("question_asking").interface(question_goal)
                print(f"  Question tool result: {result['question']} -> {result['answer'][:50]}...")
                print("  ✅ Question tool working")
            except Exception as e:
                print(f"  ❌ Question tool failed: {e}")
        else:
            print("  ❌ Missing question_asking capability")
    print("\nQuestion tool test completed!")


if __name__ == "__main__":
    asyncio.run(test_question_tool())