"""
Base Proxy Agent Framework for Phase 0 Bootstrap

Implements MCP (Model Context Protocol) interface for thin proxy agents
that delegate to external APIs (GPT-4, Claude, Copilot) before real Santiagos exist.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator

from santiago_core.core.agent_framework import SantiagoAgent, Message, Task
from santiago_core.services.llm_router import LLMRouter, TaskComplexity
from santiago_core.services.message_bus import get_message_bus, MessageBus


class MCPTool(BaseModel):
    """MCP tool definition"""
    name: str
    description: str
    parameters: Dict[str, str] = Field(default_factory=dict)


class MCPManifest(BaseModel):
    """MCP service manifest defining proxy capabilities"""
    role: str
    capabilities: List[str]
    input_tools: List[MCPTool]
    output_tools: List[MCPTool]
    communication_tools: List[MCPTool]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ProxyConfig(BaseModel):
    """Configuration for proxy agent"""
    role_name: str
    api_endpoint: str
    api_key: str
    session_ttl_hours: int = 1
    log_dir: str = "ships-logs/proxy/"
    cost_per_call: float = 0.02  # Default cost estimate
    budget_tracking: bool = False  # Disabled by default per user decision


class ProxyBudgetExceeded(Exception):
    """Raised when proxy budget is exceeded"""
    pass


class ProxySessionExpired(Exception):
    """Raised when proxy session has expired"""
    pass


class BaseProxyAgent(SantiagoAgent):
    """
    Base class for all proxy agents in Phase 0.
    
    Proxies are thin wrappers around external APIs that implement the MCP interface.
    They track budget, session TTL, and log all operations for provenance.
    """

    def __init__(
        self,
        name: str,
        workspace_path: Path,
        config: ProxyConfig,
        manifest: MCPManifest,
        role_instructions: Optional[str] = None,
    ):
        super().__init__(name, workspace_path)
        self.config = config
        self.manifest = manifest
        self.role_instructions = role_instructions or f"You are a {config.role_name}."
        self.budget_spent: float = 0.0
        self.session_start: datetime = datetime.now()
        self.call_count: int = 0
        self.calls_by_tool: Dict[str, int] = {}
        
        # Set up logging directory
        self.log_dir = workspace_path / config.log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tool cost tracking
        self._tool_costs: Dict[str, float] = {}
        
        # Initialize LLM router
        self.llm_router = LLMRouter()
        
        # Initialize message bus connection (lazy - connect on first use)
        self.message_bus: Optional[MessageBus] = None
        self._message_bus_connected = False

    async def invoke_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a tool through the proxy.
        
        This is the main entry point for proxy operations. It:
        1. Validates tool exists in manifest
        2. Checks budget and session
        3. Routes to external API
        4. Logs operation for provenance
        5. Tracks costs and metrics
        """
        # Validate tool exists
        if not self._tool_exists(tool_name):
            raise ValueError(f"Tool '{tool_name}' not found in manifest")
        
        # Estimate cost for tracking
        estimated_cost = self.estimate_tool_cost(tool_name)
        
        # Check budget (optional, disabled by default)
        if self.config.budget_tracking:
            budget_limit = getattr(self.config, "budget_per_day", float('inf'))
            if self.budget_spent + estimated_cost > budget_limit:
                raise ProxyBudgetExceeded(
                    f"Budget exceeded: {self.budget_spent:.2f} + {estimated_cost:.2f} > {budget_limit}"
                )
        
        # Check session TTL
        if not self._is_session_valid():
            raise ProxySessionExpired(
                f"Session expired. Started at {self.session_start}, TTL {self.config.session_ttl_hours}h"
            )
        
        # Route to external API
        try:
            result = await self._route_to_external_api(tool_name, params)
            
            # Track metrics
            self.budget_spent += estimated_cost
            self.call_count += 1
            self.calls_by_tool[tool_name] = self.calls_by_tool.get(tool_name, 0) + 1
            
            # Log for provenance
            await self._log_tool_call(tool_name, params, result, estimated_cost)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error invoking tool {tool_name}: {e}")
            await self._log_error(tool_name, params, str(e))
            raise

    async def _route_to_external_api(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Route tool call to external API using LLM router.
        
        Determines task complexity and routes to appropriate provider/model.
        Subclasses can override for custom routing logic.
        """
        # Import here to avoid circular dependency
        from santiago_core.services.llm_router import LLMProvider
        
        # Determine task complexity
        complexity = self.llm_router.get_task_complexity(tool_name)
        
        # Get LLM configuration
        llm_config = self.llm_router.get_config(self.config.role_name, complexity)
        
        # Make API call based on provider
        if llm_config.provider == LLMProvider.XAI:
            return await self._call_xai_api(llm_config, tool_name, params)
        elif llm_config.provider == LLMProvider.OPENAI:
            return await self._call_openai_api(llm_config, tool_name, params)
        else:
            raise ValueError(f"Unknown provider: {llm_config.provider}")
    
    async def _call_xai_api(
        self, 
        llm_config: Any,  # LLMConfig
        tool_name: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call xAI (Grok) API using OpenAI-compatible interface.
        
        xAI's API is OpenAI-compatible, so we use the OpenAI SDK
        with custom base_url and api_key.
        """
        try:
            from openai import AsyncOpenAI
            
            # Create xAI client (OpenAI-compatible)
            client = AsyncOpenAI(
                api_key=llm_config.api_key,
                base_url=llm_config.api_base,
            )
            
            # Build prompt from tool and params
            prompt = self._build_prompt(tool_name, params)
            
            # Call Grok API
            response = await client.chat.completions.create(
                model=llm_config.model,
                messages=[
                    {"role": "system", "content": self.role_instructions or f"You are a {self.config.role_name}."},
                    {"role": "user", "content": prompt},
                ],
                temperature=llm_config.temperature,
                max_tokens=llm_config.max_tokens,
            )
            
            # Parse response
            content = response.choices[0].message.content
            if not content:
                return {
                    "error": "Empty response from API",
                    "tool": tool_name,
                    "provider": "xai",
                }
            
            # Try to parse as JSON, fallback to text
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "tool": tool_name,
                    "result": content,
                    "raw_response": content,
                }
                
        except Exception as e:
            self.logger.error(f"xAI API error: {e}")
            return {
                "error": str(e),
                "tool": tool_name,
                "provider": "xai",
            }
    
    async def _call_openai_api(
        self, 
        llm_config: Any,  # LLMConfig
        tool_name: str, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call OpenAI API.
        
        Uses OpenAI SDK with GPT-4, GPT-4o, or o1-preview based on complexity.
        """
        try:
            from openai import AsyncOpenAI
            
            # Create OpenAI client
            client = AsyncOpenAI(
                api_key=llm_config.api_key,
                base_url=llm_config.api_base,
            )
            
            # Build prompt from tool and params
            prompt = self._build_prompt(tool_name, params)
            
            # Build request parameters based on model series
            # o1/o3 series: Use max_completion_tokens, no system message, no temperature
            # GPT-5 series: Use max_completion_tokens
            # Other models: Use max_tokens
            is_reasoning_model = llm_config.model.startswith(("o1", "o3"))
            is_gpt5_series = llm_config.model.startswith("gpt-5")
            
            if is_reasoning_model:
                # o1/o3: max_completion_tokens, no system, no temperature
                request_params = {
                    "model": llm_config.model,
                    "messages": [
                        {"role": "user", "content": f"{self.role_instructions or ''}\n\n{prompt}"},
                    ],
                }
                if llm_config.max_tokens:
                    request_params["max_completion_tokens"] = llm_config.max_tokens
            elif is_gpt5_series:
                # GPT-5: max_completion_tokens, system message allowed, temperature allowed
                request_params = {
                    "model": llm_config.model,
                    "messages": [
                        {"role": "system", "content": self.role_instructions or f"You are a {self.config.role_name}."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": llm_config.temperature,
                }
                if llm_config.max_tokens:
                    request_params["max_completion_tokens"] = llm_config.max_tokens
            else:
                # GPT-4 and earlier: max_tokens
                request_params = {
                    "model": llm_config.model,
                    "messages": [
                        {"role": "system", "content": self.role_instructions or f"You are a {self.config.role_name}."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": llm_config.temperature,
                }
                if llm_config.max_tokens:
                    request_params["max_tokens"] = llm_config.max_tokens
            
            response = await client.chat.completions.create(**request_params)
            
            # Parse response
            content = response.choices[0].message.content
            if not content:
                return {
                    "error": "Empty response from API",
                    "tool": tool_name,
                    "provider": "openai",
                }
            
            # Try to parse as JSON, fallback to text
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "tool": tool_name,
                    "result": content,
                    "raw_response": content,
                }
                
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return {
                "error": str(e),
                "tool": tool_name,
                "provider": "openai",
            }
    
    def _build_prompt(self, tool_name: str, params: Dict[str, Any]) -> str:
        """
        Build prompt for LLM from tool name and parameters.
        
        Args:
            tool_name: Name of the tool being invoked
            params: Tool parameters
            
        Returns:
            Formatted prompt string
        """
        # Find tool in manifest
        all_tools = (
            self.manifest.input_tools +
            self.manifest.output_tools +
            self.manifest.communication_tools
        )
        tool_def = next((t for t in all_tools if t.name == tool_name), None)
        
        if not tool_def:
            return f"Execute tool: {tool_name}\nParameters: {json.dumps(params, indent=2)}"
        
        # Build structured prompt
        prompt_parts = [
            f"Execute the following tool:",
            f"",
            f"Tool: {tool_name}",
            f"Description: {tool_def.description}",
            f"",
            f"Parameters:",
            json.dumps(params, indent=2),
            f"",
            f"Please provide a structured JSON response following this tool's expected output format.",
        ]
        
        return "\n".join(prompt_parts)

    def _tool_exists(self, tool_name: str) -> bool:
        """Check if tool exists in manifest"""
        all_tools = (
            self.manifest.input_tools +
            self.manifest.output_tools +
            self.manifest.communication_tools
        )
        return any(tool.name == tool_name for tool in all_tools)

    def _is_session_valid(self) -> bool:
        """Check if session is still valid"""
        elapsed = datetime.now() - self.session_start
        return elapsed < timedelta(hours=self.config.session_ttl_hours)

    async def renew_session(self) -> None:
        """Renew the proxy session"""
        self.session_start = datetime.now()
        self.budget_spent = 0.0
        self.call_count = 0
        self.calls_by_tool = {}
        self.logger.info(f"Session renewed for {self.name}")

    def estimate_tool_cost(self, tool_name: str) -> float:
        """Estimate cost for a tool call"""
        # Use cached cost if available
        if tool_name in self._tool_costs:
            return self._tool_costs[tool_name]
        
        # Default cost
        return self.config.cost_per_call

    async def _log_tool_call(
        self,
        tool_name: str,
        params: Dict[str, Any],
        result: Dict[str, Any],
        cost: float,
    ) -> None:
        """Log tool call for provenance"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "proxy": self.name,
            "tool": tool_name,
            "params": params,
            "result": result,
            "cost": cost,
            "budget_spent": self.budget_spent,
            "session_start": self.session_start.isoformat(),
        }
        
        # Write to jsonl log file
        log_file = self.log_dir / f"{self.name}_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    async def _log_error(self, tool_name: str, params: Dict[str, Any], error: str) -> None:
        """Log error for provenance"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "proxy": self.name,
            "tool": tool_name,
            "params": params,
            "error": error,
            "type": "error",
        }
        
        log_file = self.log_dir / f"{self.name}_errors_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def get_metrics(self) -> Dict[str, Any]:
        """Get proxy metrics"""
        metrics = {
            "proxy": self.name,
            "session_start": self.session_start.isoformat(),
            "total_calls": self.call_count,
            "calls_by_tool": self.calls_by_tool,
            "budget_spent": self.budget_spent,
        }
        
        # Add budget remaining if tracking is enabled
        if self.config.budget_tracking:
            budget_limit = getattr(self.config, "budget_per_day", None)
            if budget_limit is not None:
                metrics["budget_remaining"] = budget_limit - self.budget_spent
        
        return metrics

    def get_manifest_dict(self) -> Dict[str, Any]:
        """Get manifest as dictionary"""
        return self.manifest.model_dump()

    async def connect_to_message_bus(self) -> None:
        """Connect proxy to Redis message bus"""
        if self._message_bus_connected:
            return
        
        try:
            self.message_bus = get_message_bus()
            await self.message_bus.connect()
            
            # Subscribe to role-specific topic
            role_topic = f"agent.{self.name}"
            await self.message_bus.subscribe(role_topic, self._handle_bus_message)
            
            # Subscribe to broadcast topic
            await self.message_bus.subscribe("agent.broadcast", self._handle_bus_message)
            
            self._message_bus_connected = True
            self.logger.info(f"{self.name} connected to message bus")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to message bus: {e}")
            raise

    async def _handle_bus_message(self, envelope: Dict[str, Any]) -> None:
        """
        Handle message from message bus.
        
        Args:
            envelope: Message envelope with sender, timestamp, payload
        """
        sender = envelope.get("sender", "unknown")
        payload = envelope.get("payload", {})
        
        self.logger.info(f"{self.name} received message from {sender}: {payload}")
        
        # Handle different message types
        message_type = payload.get("type", "")
        
        if message_type == "task_assignment":
            await self._handle_task_assignment(payload, sender)
        elif message_type == "collaboration_request":
            await self._handle_collaboration_request(payload, sender)
        elif message_type == "status_query":
            await self._handle_status_query(payload, sender)
        else:
            # Delegate to proxy-specific handler
            await self._handle_proxy_specific_message(payload, sender)

    async def _handle_task_assignment(self, payload: Dict[str, Any], sender: str) -> None:
        """Handle task assignment from message bus"""
        task_id = payload.get("task_id", "")
        task_description = payload.get("description", "")
        
        self.logger.info(f"Received task assignment: {task_id}")
        
        # Acknowledge receipt
        await self.send_message(
            sender,
            {
                "type": "task_acknowledged",
                "task_id": task_id,
                "status": "accepted",
            }
        )

    async def _handle_collaboration_request(self, payload: Dict[str, Any], sender: str) -> None:
        """Handle collaboration request from another agent"""
        request_type = payload.get("request_type", "")
        
        self.logger.info(f"Collaboration request from {sender}: {request_type}")
        
        # Respond with availability
        await self.send_message(
            sender,
            {
                "type": "collaboration_response",
                "request_type": request_type,
                "available": True,
            }
        )

    async def _handle_status_query(self, payload: Dict[str, Any], sender: str) -> None:
        """Handle status query from another agent"""
        self.logger.info(f"Status query from {sender}")
        
        # Send current metrics
        metrics = self.get_metrics()
        await self.send_message(
            sender,
            {
                "type": "status_response",
                "metrics": metrics,
            }
        )

    async def _handle_proxy_specific_message(self, payload: Dict[str, Any], sender: str) -> None:
        """
        Handle proxy-specific messages.
        
        Override in subclasses for custom message handling.
        """
        self.logger.debug(f"No specific handler for message from {sender}: {payload}")

    async def send_message(self, recipient: str, message: Dict[str, Any]) -> None:
        """
        Send message to another agent via message bus.
        
        Args:
            recipient: Name of the recipient agent
            message: Message payload
        """
        if not self._message_bus_connected:
            await self.connect_to_message_bus()
        
        if self.message_bus:
            await self.message_bus.send_message(recipient, message, self.name)
        self.logger.debug(f"Sent message to {recipient}: {message}")

    async def broadcast_message(self, message: Dict[str, Any]) -> None:
        """
        Broadcast message to all agents via message bus.
        
        Args:
            message: Message payload
        """
        if not self._message_bus_connected:
            await self.connect_to_message_bus()
        
        if self.message_bus:
            await self.message_bus.broadcast(message, self.name)
        self.logger.debug(f"Broadcast message: {message}")

    async def disconnect_from_message_bus(self) -> None:
        """Disconnect from message bus"""
        if self.message_bus and self._message_bus_connected:
            await self.message_bus.disconnect()
            self._message_bus_connected = False
            self.logger.info(f"{self.name} disconnected from message bus")
