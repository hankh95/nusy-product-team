"""
Tests for proxy agent message bus integration

Validates that proxies can connect to Redis and communicate via message bus.
"""

import asyncio
import pytest
import os
from pathlib import Path

from santiago_core.agents._proxy import PMProxyAgent, ArchitectProxyAgent


@pytest.mark.asyncio
class TestProxyMessageBus:
    """Test proxy integration with message bus"""
    
    @pytest.fixture
    def workspace(self, tmp_path):
        """Create test workspace"""
        workspace = tmp_path / "test_workspace"
        workspace.mkdir()
        
        # Create role card directory
        instructions_dir = workspace / "knowledge" / "proxy-instructions"
        instructions_dir.mkdir(parents=True)
        
        # Create minimal role cards
        (instructions_dir / "pm.md").write_text("# PM Role Card")
        (instructions_dir / "architect.md").write_text("# Architect Role Card")
        
        return workspace
    
    @pytest.fixture
    def redis_available(self):
        """Check if Redis is available"""
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 6379))
            sock.close()
            return result == 0
        except:
            return False
    
    async def test_proxy_connects_to_message_bus(self, workspace, redis_available):
        """Test proxy can connect to message bus"""
        if not redis_available:
            pytest.skip("Redis not available")
        
        pm = PMProxyAgent(workspace)
        
        try:
            await pm.connect_to_message_bus()
            assert pm._message_bus_connected == True
            assert pm.message_bus is not None
        finally:
            await pm.disconnect_from_message_bus()
    
    async def test_proxy_send_message(self, workspace, redis_available):
        """Test proxy can send message to another proxy"""
        if not redis_available:
            pytest.skip("Redis not available")
        
        pm = PMProxyAgent(workspace)
        architect = ArchitectProxyAgent(workspace)
        
        messages_received = []
        
        async def capture_message(envelope):
            messages_received.append(envelope)
        
        try:
            # Connect both proxies
            await pm.connect_to_message_bus()
            await architect.connect_to_message_bus()
            
            assert architect.message_bus is not None
            
            # Override architect's handler to capture message
            architect._handle_bus_message = capture_message
            await architect.message_bus.subscribe(f"agent.{architect.name}", capture_message)
            
            # Start listening in background
            listen_task = asyncio.create_task(architect.message_bus.start_listening())
            await asyncio.sleep(0.1)
            
            # PM sends message to architect
            await pm.send_message(
                architect.name,
                {
                    "type": "collaboration_request",
                    "request_type": "design_review",
                }
            )
            
            # Wait for message processing
            await asyncio.sleep(0.2)
            
            # Stop listening
            architect.message_bus._running = False
            await listen_task
            
            # Verify message received
            assert len(messages_received) > 0
            last_message = messages_received[-1]
            assert last_message["sender"] == pm.name
            assert last_message["payload"]["type"] == "collaboration_request"
            
        finally:
            await pm.disconnect_from_message_bus()
            await architect.disconnect_from_message_bus()
    
    async def test_proxy_broadcast_message(self, workspace, redis_available):
        """Test proxy can broadcast to all agents"""
        if not redis_available:
            pytest.skip("Redis not available")
        
        pm = PMProxyAgent(workspace)
        
        broadcast_received = []
        
        async def capture_broadcast(envelope):
            broadcast_received.append(envelope)
        
        try:
            await pm.connect_to_message_bus()
            
            assert pm.message_bus is not None
            
            # Subscribe to broadcast topic
            await pm.message_bus.subscribe("agent.broadcast", capture_broadcast)
            
            # Start listening
            listen_task = asyncio.create_task(pm.message_bus.start_listening())
            await asyncio.sleep(0.1)
            
            # Broadcast message
            await pm.broadcast_message({
                "type": "system_announcement",
                "message": "All agents report status"
            })
            
            await asyncio.sleep(0.2)
            pm.message_bus._running = False
            await listen_task
            
            # Verify broadcast received
            assert len(broadcast_received) > 0
            last_message = broadcast_received[-1]
            assert last_message["sender"] == pm.name
            assert last_message["payload"]["type"] == "system_announcement"
            
        finally:
            await pm.disconnect_from_message_bus()
    
    async def test_lazy_connection(self, workspace, redis_available):
        """Test message bus connects lazily on first use"""
        if not redis_available:
            pytest.skip("Redis not available")
        
        pm = PMProxyAgent(workspace)
        
        # Should not be connected initially
        assert pm._message_bus_connected == False
        
        try:
            # Sending message should trigger connection
            await pm.send_message("architect-proxy", {"type": "test"})
            
            # Should now be connected
            assert pm._message_bus_connected == True
            
        finally:
            await pm.disconnect_from_message_bus()
