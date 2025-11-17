"""
Redis-based Message Bus for Santiago Factory

Lightweight message bus using Redis pub/sub for multi-agent orchestration.
Supports async message passing between Santiago agents on the same machine.
"""

import asyncio
import json
import logging
from typing import Any, Awaitable, Callable, Dict, Optional, Set, Union
from datetime import datetime

try:
    import redis.asyncio as redis
except ImportError:
    redis = None


class MessageBus:
    """
    Redis-based message bus for Santiago agent communication.
    
    Features:
    - Pub/sub messaging between agents
    - Topic-based routing
    - JSON message serialization
    - Async/await support
    """
    
    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """
        Initialize message bus.
        
        Args:
            redis_url: Redis connection URL
        """
        if redis is None:
            raise ImportError("redis package required. Install with: pip install redis")
        
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
        self.pubsub: Optional[redis.client.PubSub] = None
        self.handlers: Dict[str, Set[Callable[[Dict[str, Any]], Awaitable[None]]]] = {}
        self.logger = logging.getLogger(__name__)
        self._running = False
    
    async def connect(self) -> None:
        """Connect to Redis server"""
        self.redis_client = await redis.from_url(self.redis_url, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.logger.info(f"Connected to Redis: {self.redis_url}")
    
    async def disconnect(self) -> None:
        """Disconnect from Redis server"""
        self._running = False
        if self.pubsub:
            await self.pubsub.close()
        if self.redis_client:
            await self.redis_client.close()
        self.logger.info("Disconnected from Redis")
    
    async def publish(
        self,
        topic: str,
        message: Dict[str, Any],
        sender: str,
    ) -> None:
        """
        Publish message to a topic.
        
        Args:
            topic: Topic to publish to (e.g., "agent.pm", "agent.architect")
            message: Message payload as dictionary
            sender: Name of sending agent
        """
        if not self.redis_client:
            raise RuntimeError("Not connected to Redis")
        
        # Wrap message with metadata
        envelope = {
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
            "payload": message,
        }
        
        # Serialize and publish
        message_json = json.dumps(envelope)
        await self.redis_client.publish(topic, message_json)
        
        self.logger.debug(f"Published to {topic}: {sender} -> {message}")
    
    async def subscribe(
        self,
        topic: str,
        handler: Callable[[Dict[str, Any]], Awaitable[None]],
    ) -> None:
        """
        Subscribe to a topic.
        
        Args:
            topic: Topic to subscribe to
            handler: Async function to handle messages
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
        
        # Add handler
        if topic not in self.handlers:
            self.handlers[topic] = set()
            await self.pubsub.subscribe(topic)
        
        self.handlers[topic].add(handler)
        self.logger.info(f"Subscribed to topic: {topic}")
    
    async def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a topic"""
        if not self.pubsub:
            return
        
        if topic in self.handlers:
            await self.pubsub.unsubscribe(topic)
            del self.handlers[topic]
            self.logger.info(f"Unsubscribed from topic: {topic}")
    
    async def start_listening(self) -> None:
        """Start listening for messages (blocks until stopped)"""
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
        
        self._running = True
        self.logger.info("Message bus listening started")
        
        async for message in self.pubsub.listen():
            if not self._running:
                break
            
            if message["type"] != "message":
                continue
            
            topic = message["channel"]
            data = message["data"]
            
            try:
                # Parse message
                envelope = json.loads(data)
                
                # Call handlers
                if topic in self.handlers:
                    for handler in self.handlers[topic]:
                        try:
                            await handler(envelope)
                        except Exception as e:
                            self.logger.error(f"Handler error: {e}")
            
            except json.JSONDecodeError:
                self.logger.error(f"Invalid JSON in message: {data}")
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
    
    async def send_message(
        self,
        recipient: str,
        message: Dict[str, Any],
        sender: str,
    ) -> None:
        """
        Send direct message to a specific agent.
        
        Args:
            recipient: Name of recipient agent (e.g., "pm-proxy")
            message: Message payload
            sender: Name of sender agent
        """
        topic = f"agent.{recipient}"
        await self.publish(topic, message, sender)
    
    async def broadcast(
        self,
        message: Dict[str, Any],
        sender: str,
    ) -> None:
        """
        Broadcast message to all agents.
        
        Args:
            message: Message payload
            sender: Name of sender agent
        """
        await self.publish("agent.broadcast", message, sender)


# Singleton instance
_message_bus: Optional[MessageBus] = None


def get_message_bus(redis_url: Optional[str] = None) -> MessageBus:
    """
    Get or create message bus singleton.
    
    Args:
        redis_url: Redis connection URL (only used on first call)
        
    Returns:
        MessageBus instance
    """
    global _message_bus
    
    if _message_bus is None:
        import os
        url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        _message_bus = MessageBus(url)
    
    return _message_bus
