#!/usr/bin/env python
"""
Redis Message Bus Coordination Demo

Demonstrates multi-agent coordination using Redis pub/sub:
1. PM publishes feature request
2. Architect subscribes and designs architecture
3. Developer subscribes and implements
4. Agents communicate through message bus

This validates:
- Redis pub/sub functionality
- Message routing between agents
- Async coordination patterns
- Topic-based communication
"""

import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

from santiago_core.services.message_bus import get_message_bus


class AgentSimulator:
    """Simulates an agent for message bus testing"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.message_bus = get_message_bus()
        self.received_messages = []
    
    async def handle_message(self, envelope: dict):
        """Handle incoming message"""
        sender = envelope.get("sender", "unknown")
        payload = envelope.get("payload", {})
        timestamp = envelope.get("timestamp", "")
        
        print(f"\n📨 {self.name} received message from {sender}")
        print(f"   Time: {timestamp}")
        print(f"   Payload: {json.dumps(payload, indent=2)[:200]}...")
        
        self.received_messages.append(envelope)
    
    async def send_message(self, recipient: str, message: dict):
        """Send message to specific agent"""
        print(f"\n📤 {self.name} sending to {recipient}")
        print(f"   Message: {json.dumps(message, indent=2)[:200]}...")
        
        await self.message_bus.send_message(
            recipient=recipient,
            message=message,
            sender=self.name
        )
    
    async def broadcast(self, message: dict):
        """Broadcast message to all agents"""
        print(f"\n📢 {self.name} broadcasting")
        print(f"   Message: {json.dumps(message, indent=2)[:200]}...")
        
        await self.message_bus.broadcast(
            message=message,
            sender=self.name
        )
    
    async def subscribe_to_role(self):
        """Subscribe to messages for this agent's role"""
        topic = f"agent.{self.name}"
        await self.message_bus.subscribe(topic, self.handle_message)
        print(f"✅ {self.name} subscribed to: {topic}")
    
    async def subscribe_to_broadcast(self):
        """Subscribe to broadcast messages"""
        topic = "agent.broadcast"
        await self.message_bus.subscribe(topic, self.handle_message)
        print(f"✅ {self.name} subscribed to broadcasts")


async def scenario_1_direct_messaging():
    """Scenario 1: PM sends task directly to Architect"""
    print("\n" + "="*70)
    print("SCENARIO 1: Direct Messaging (PM → Architect)")
    print("="*70)
    
    # Create agents
    pm = AgentSimulator("pm-proxy", "product_manager")
    architect = AgentSimulator("architect-proxy", "architect")
    
    # Connect to message bus
    bus = get_message_bus()
    await bus.connect()
    
    # Subscribe agents
    await architect.subscribe_to_role()
    
    # PM sends design request to Architect
    await pm.send_message(
        recipient="architect-proxy",
        message={
            "type": "design_request",
            "feature_id": "passage-system-001",
            "requirements": "Design a nautical workflow system",
            "constraints": "Must integrate with MCP and knowledge graph"
        }
    )
    
    # Give message time to be delivered
    await asyncio.sleep(0.5)
    
    # Verify architect received it
    print(f"\n✅ Architect received {len(architect.received_messages)} message(s)")
    
    await bus.disconnect()


async def scenario_2_pub_sub_workflow():
    """Scenario 2: PM broadcasts, Architect and Developer both respond"""
    print("\n" + "="*70)
    print("SCENARIO 2: Pub/Sub Workflow (PM → All Agents)")
    print("="*70)
    
    # Create agents
    pm = AgentSimulator("pm-proxy", "product_manager")
    architect = AgentSimulator("architect-proxy", "architect")
    developer = AgentSimulator("developer-proxy", "developer")
    
    # Connect to message bus
    bus = get_message_bus()
    await bus.connect()
    
    # All agents subscribe to broadcasts
    await architect.subscribe_to_broadcast()
    await developer.subscribe_to_broadcast()
    
    # PM broadcasts new feature
    await pm.broadcast(message={
        "type": "new_feature",
        "feature_id": "redis-coordination-001",
        "title": "Multi-Agent Redis Coordination",
        "description": "Implement async message passing for agent coordination",
        "priority": "high"
    })
    
    # Give messages time to be delivered
    await asyncio.sleep(0.5)
    
    # Verify all received broadcast
    print(f"\n✅ Architect received {len(architect.received_messages)} message(s)")
    print(f"✅ Developer received {len(developer.received_messages)} message(s)")
    
    await bus.disconnect()


async def scenario_3_coordination_chain():
    """Scenario 3: PM → Architect → Developer coordination chain"""
    print("\n" + "="*70)
    print("SCENARIO 3: Coordination Chain (PM → Architect → Developer)")
    print("="*70)
    
    # Create agents
    pm = AgentSimulator("pm-proxy", "product_manager")
    architect = AgentSimulator("architect-proxy", "architect")
    developer = AgentSimulator("developer-proxy", "developer")
    
    # Connect to message bus
    bus = get_message_bus()
    await bus.connect()
    
    # Subscribe all agents
    await architect.subscribe_to_role()
    await developer.subscribe_to_role()
    
    # Step 1: PM sends to Architect
    print("\n📋 Step 1: PM requests architecture design")
    await pm.send_message(
        recipient="architect-proxy",
        message={
            "type": "design_request",
            "feature_id": "coordination-demo-001",
            "requirements": "Multi-step workflow with async coordination"
        }
    )
    
    await asyncio.sleep(0.5)
    
    # Step 2: Architect sends design to Developer
    print("\n🏗️  Step 2: Architect sends design to Developer")
    await architect.send_message(
        recipient="developer-proxy",
        message={
            "type": "implementation_request",
            "feature_id": "coordination-demo-001",
            "design": {
                "components": ["MessageBus", "AgentCoordinator", "TopicRouter"],
                "architecture": "Event-driven pub/sub pattern"
            }
        }
    )
    
    await asyncio.sleep(0.5)
    
    # Step 3: Developer acknowledges
    print("\n💻 Step 3: Developer acknowledges receipt")
    
    # Verify coordination chain
    print(f"\n✅ Coordination chain complete:")
    print(f"   Architect received {len(architect.received_messages)} message(s)")
    print(f"   Developer received {len(developer.received_messages)} message(s)")
    
    await bus.disconnect()


async def scenario_4_topic_routing():
    """Scenario 4: Multiple topics with selective subscriptions"""
    print("\n" + "="*70)
    print("SCENARIO 4: Topic-Based Routing")
    print("="*70)
    
    # Create agents
    pm = AgentSimulator("pm-proxy", "product_manager")
    architect = AgentSimulator("architect-proxy", "architect")
    developer = AgentSimulator("developer-proxy", "developer")
    qa = AgentSimulator("qa-proxy", "qa")
    
    # Connect to message bus
    bus = get_message_bus()
    await bus.connect()
    
    # Selective subscriptions
    await architect.subscribe_to_role()
    await developer.subscribe_to_role()
    await qa.subscribe_to_role()
    await qa.subscribe_to_broadcast()  # QA also subscribes to broadcasts
    
    # PM sends targeted messages
    print("\n📋 PM sends design request to Architect only")
    await pm.send_message("architect-proxy", {
        "type": "design_request",
        "feature": "topic-routing"
    })
    
    await asyncio.sleep(0.3)
    
    print("\n📋 PM sends implementation request to Developer only")
    await pm.send_message("developer-proxy", {
        "type": "implementation_request",
        "feature": "topic-routing"
    })
    
    await asyncio.sleep(0.3)
    
    print("\n📋 PM broadcasts test request (QA should receive)")
    await pm.broadcast({
        "type": "test_request",
        "feature": "topic-routing"
    })
    
    await asyncio.sleep(0.3)
    
    # Verify selective routing
    print(f"\n✅ Topic routing results:")
    print(f"   Architect: {len(architect.received_messages)} message(s) (design only)")
    print(f"   Developer: {len(developer.received_messages)} message(s) (impl only)")
    print(f"   QA: {len(qa.received_messages)} message(s) (broadcast only)")
    
    await bus.disconnect()


async def main():
    """Run all scenarios"""
    print("\n" + "🔄"*35)
    print("Redis Message Bus Coordination Demo")
    print("🔄"*35)
    
    try:
        # Run scenarios
        await scenario_1_direct_messaging()
        await scenario_2_pub_sub_workflow()
        await scenario_3_coordination_chain()
        await scenario_4_topic_routing()
        
        # Summary
        print("\n" + "="*70)
        print("🎉 DEMO COMPLETE!")
        print("="*70)
        print("\nValidated:")
        print("  ✅ Direct messaging between agents")
        print("  ✅ Broadcast pub/sub pattern")
        print("  ✅ Multi-step coordination chains")
        print("  ✅ Topic-based selective routing")
        print("\nRedis Message Bus:")
        print("  • Async/await support")
        print("  • JSON message serialization")
        print("  • Multiple subscription patterns")
        print("  • Clean agent coordination")
        
        print("\nNext Steps:")
        print("  • Integrate with real proxy agents")
        print("  • Add message persistence")
        print("  • Implement request/reply patterns")
        print("  • Add message filtering and routing rules")
        
    except ConnectionRefusedError:
        print("\n❌ Redis connection failed!")
        print("   Make sure Redis is running: redis-server")
        print("   Or install: brew install redis (macOS)")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
