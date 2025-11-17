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
    budget_per_day: float = 25.0
    session_ttl_hours: int = 1
    log_dir: str = "ships-logs/proxy/"
    cost_per_call: float = 0.02  # Default cost estimate

    @field_validator("budget_per_day")
    @classmethod
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError("Budget must be positive")
        return v


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
    ):
        super().__init__(name, workspace_path)
        self.config = config
        self.manifest = manifest
        self.budget_spent: float = 0.0
        self.session_start: datetime = datetime.now()
        self.call_count: int = 0
        self.calls_by_tool: Dict[str, int] = {}
        
        # Set up logging directory
        self.log_dir = workspace_path / config.log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tool cost tracking
        self._tool_costs: Dict[str, float] = {}

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
        
        # Check budget
        estimated_cost = self.estimate_tool_cost(tool_name)
        if self.budget_spent + estimated_cost > self.config.budget_per_day:
            raise ProxyBudgetExceeded(
                f"Budget exceeded: {self.budget_spent:.2f} + {estimated_cost:.2f} > {self.config.budget_per_day}"
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
        Route tool call to external API.
        
        Subclasses override this to implement actual API calls.
        """
        raise NotImplementedError("Subclasses must implement _route_to_external_api")

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
        return {
            "proxy": self.name,
            "session_start": self.session_start.isoformat(),
            "total_calls": self.call_count,
            "calls_by_tool": self.calls_by_tool,
            "budget_spent": self.budget_spent,
            "budget_remaining": self.config.budget_per_day - self.budget_spent,
        }

    def get_manifest_dict(self) -> Dict[str, Any]:
        """Get manifest as dictionary"""
        return self.manifest.model_dump()
