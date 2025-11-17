"""
Integration tests for Phase 0 LLM routing and message bus

Tests the routing of tasks to appropriate LLM providers based on
role and task complexity, plus Redis message bus for agent communication.
"""

import asyncio
import os
import pytest
from pathlib import Path

from santiago_core.services.llm_router import LLMRouter, TaskComplexity, LLMProvider


class TestLLMRouting:
    """Test LLM routing to appropriate providers"""
    
    def test_architect_routes_to_xai(self):
        """Architect role should route to xAI (Grok)"""
        router = LLMRouter()
        
        config = router.get_config("architect_proxy", TaskComplexity.COMPLEX)
        
        assert config.provider.value == LLMProvider.XAI.value
        assert config.model == "grok-beta"
    
    def test_developer_routes_to_openai(self):
        """Developer role should route to OpenAI"""
        router = LLMRouter()
        
        config = router.get_config("developer_proxy", TaskComplexity.SIMPLE)
        
        assert config.provider.value == LLMProvider.OPENAI.value
        assert config.model == "gpt-4o-mini"
    
    def test_ethicist_routes_to_xai(self):
        """Ethicist role should route to xAI (Grok)"""
        router = LLMRouter()
        
        config = router.get_config("ethicist_proxy", TaskComplexity.COMPLEX)
        
        assert config.provider.value == LLMProvider.XAI.value
        assert config.model == "grok-beta"
    
    def test_complexity_affects_model_selection_openai(self):
        """OpenAI model selection should vary by complexity"""
        router = LLMRouter()
        
        simple = router.get_config("developer_proxy", TaskComplexity.SIMPLE)
        moderate = router.get_config("developer_proxy", TaskComplexity.MODERATE)
        complex_task = router.get_config("developer_proxy", TaskComplexity.COMPLEX)
        critical = router.get_config("developer_proxy", TaskComplexity.CRITICAL)
        
        assert simple.model == "gpt-4o-mini"
        assert moderate.model == "gpt-4o"
        assert complex_task.model == "gpt-4o"
        assert critical.model == "o1-preview"
    
    def test_task_complexity_detection(self):
        """Test automatic complexity detection from tool names"""
        router = LLMRouter()
        
        assert router.get_task_complexity("read_feature") == TaskComplexity.SIMPLE
        assert router.get_task_complexity("write_code") == TaskComplexity.MODERATE
        assert router.get_task_complexity("design_architecture") == TaskComplexity.COMPLEX
        assert router.get_task_complexity("review_security") == TaskComplexity.CRITICAL
        assert router.get_task_complexity("test_integration") == TaskComplexity.MODERATE
    
    def test_all_roles_have_routing(self):
        """All proxy roles should have routing configured"""
        router = LLMRouter()
        
        roles = [
            "pm_proxy",
            "architect_proxy",
            "developer_proxy",
            "qa_proxy",
            "ethicist_proxy",
            "researcher_proxy",
            "coordinator_proxy",
        ]
        
        for role in roles:
            config = router.get_config(role, TaskComplexity.MODERATE)
            assert config.provider.value in [LLMProvider.XAI.value, LLMProvider.OPENAI.value]
            assert config.model is not None


@pytest.mark.asyncio
class TestMessageBus:
    """Test Redis message bus for agent communication"""
    
    @pytest.fixture
    async def message_bus(self):
        """Create message bus for testing"""
        from santiago_core.services.message_bus import MessageBus
        
        # Use test Redis instance
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/1")
        bus = MessageBus(redis_url)
        
        try:
            await bus.connect()
            yield bus
        finally:
            await bus.disconnect()
    
    async def test_message_bus_connect(self, message_bus):
        """Test message bus can connect to Redis"""
        assert message_bus.redis_client is not None
        assert message_bus.pubsub is not None
    
    async def test_publish_message(self, message_bus):
        """Test publishing messages to topics"""
        messages_received = []
        
        async def handler(envelope):
            messages_received.append(envelope)
        
        # Subscribe to topic
        await message_bus.subscribe("test.topic", handler)
        
        # Start listening in background
        listen_task = asyncio.create_task(message_bus.start_listening())
        
        # Give listener time to start
        await asyncio.sleep(0.1)
        
        # Publish message
        await message_bus.publish(
            "test.topic",
            {"content": "test message"},
            "test_sender"
        )
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Stop listening
        message_bus._running = False
        await listen_task
        
        # Verify message received
        assert len(messages_received) == 1
        assert messages_received[0]["sender"] == "test_sender"
        assert messages_received[0]["payload"]["content"] == "test message"
    
    async def test_direct_message(self, message_bus):
        """Test sending direct message to specific agent"""
        messages_received = []
        
        async def handler(envelope):
            messages_received.append(envelope)
        
        # Subscribe to agent topic
        await message_bus.subscribe("agent.pm-proxy", handler)
        
        # Start listening
        listen_task = asyncio.create_task(message_bus.start_listening())
        await asyncio.sleep(0.1)
        
        # Send direct message
        await message_bus.send_message(
            "pm-proxy",
            {"type": "task_assignment", "task_id": "T-123"},
            "coordinator-proxy"
        )
        
        await asyncio.sleep(0.1)
        message_bus._running = False
        await listen_task
        
        # Verify message
        assert len(messages_received) == 1
        assert messages_received[0]["sender"] == "coordinator-proxy"
        assert messages_received[0]["payload"]["type"] == "task_assignment"
    
    async def test_broadcast_message(self, message_bus):
        """Test broadcasting to all agents"""
        messages_received = []
        
        async def handler(envelope):
            messages_received.append(envelope)
        
        # Subscribe to broadcast topic
        await message_bus.subscribe("agent.broadcast", handler)
        
        # Start listening
        listen_task = asyncio.create_task(message_bus.start_listening())
        await asyncio.sleep(0.1)
        
        # Broadcast
        await message_bus.broadcast(
            {"type": "system_announcement", "message": "All agents stop"},
            "coordinator-proxy"
        )
        
        await asyncio.sleep(0.1)
        message_bus._running = False
        await listen_task
        
        # Verify broadcast received
        assert len(messages_received) == 1
        assert messages_received[0]["payload"]["type"] == "system_announcement"
    
    async def test_multiple_handlers(self, message_bus):
        """Test multiple handlers on same topic"""
        handler1_messages = []
        handler2_messages = []
        
        async def handler1(envelope):
            handler1_messages.append(envelope)
        
        async def handler2(envelope):
            handler2_messages.append(envelope)
        
        # Subscribe both handlers
        await message_bus.subscribe("test.multi", handler1)
        await message_bus.subscribe("test.multi", handler2)
        
        # Start listening
        listen_task = asyncio.create_task(message_bus.start_listening())
        await asyncio.sleep(0.1)
        
        # Publish message
        await message_bus.publish(
            "test.multi",
            {"content": "multi-handler test"},
            "test"
        )
        
        await asyncio.sleep(0.1)
        message_bus._running = False
        await listen_task
        
        # Both handlers should receive
        assert len(handler1_messages) == 1
        assert len(handler2_messages) == 1


@pytest.mark.asyncio
class TestProxyIntegration:
    """Test integration of proxies with LLM routing and message bus"""
    
    async def test_proxy_uses_correct_provider(self):
        """Test that proxy agents use correct LLM provider"""
        from santiago_core.agents._proxy.pm_proxy import PMProxyAgent
        
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        # Create PM proxy
        pm = PMProxyAgent(workspace)
        
        # Verify it has LLM router configured
        assert hasattr(pm, "llm_router")
        assert pm.llm_router is not None
        
        # PM should route to OpenAI for dev tasks
        config = pm.llm_router.get_config("pm_proxy", TaskComplexity.MODERATE)
        assert config.provider == LLMProvider.OPENAI.value
    
    async def test_ethicist_async_mode(self):
        """Test ethicist operates in async mode"""
        from santiago_core.agents._proxy.ethicist_proxy import EthicistProxyAgent
        
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        # Set async mode
        os.environ["PROXY_ETHICAL_MODE"] = "async"
        
        # Create ethicist proxy
        ethicist = EthicistProxyAgent(workspace)
        
        # Verify async mode
        assert ethicist.ethical_mode == "async"
        
        # Verify core principles configured
        assert "Service to Humanity" in str(ethicist.bahai_principles)
