"""
LLM Router for Santiago Factory

Routes requests to appropriate LLM based on task complexity and role.
Supports xAI (Grok) and OpenAI with model selection.
"""

import os
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class TaskComplexity(Enum):
    """Task complexity levels for model selection"""
    SIMPLE = "simple"  # Quick responses, code completion
    MODERATE = "moderate"  # Standard development, testing
    COMPLEX = "complex"  # Architecture, design, ethical reasoning
    CRITICAL = "critical"  # System-wide decisions, safety reviews


class LLMProvider(Enum):
    """Available LLM providers"""
    XAI = "xai"
    OPENAI = "openai"


@dataclass
class LLMConfig:
    """Configuration for LLM API calls"""
    provider: LLMProvider
    model: str
    api_key: str
    api_base: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None


class LLMRouter:
    """Routes LLM requests to appropriate provider and model"""
    
    # Model mapping based on xAI and OpenAI capabilities
    MODEL_MAP = {
        # xAI models (Grok 4 Fast - latest as of Nov 2024)
        (LLMProvider.XAI, TaskComplexity.SIMPLE): "grok-4-fast",
        (LLMProvider.XAI, TaskComplexity.MODERATE): "grok-4-fast",
        (LLMProvider.XAI, TaskComplexity.COMPLEX): "grok-4-fast",
        (LLMProvider.XAI, TaskComplexity.CRITICAL): "grok-4-fast",
        
        # OpenAI models
        (LLMProvider.OPENAI, TaskComplexity.SIMPLE): "gpt-4o-mini",
        (LLMProvider.OPENAI, TaskComplexity.MODERATE): "gpt-4o",
        (LLMProvider.OPENAI, TaskComplexity.COMPLEX): "gpt-4o",
        (LLMProvider.OPENAI, TaskComplexity.CRITICAL): "o1-preview",
    }
    
    # Role to provider mapping (prefer xAI for architecture, OpenAI for dev)
    ROLE_PROVIDER = {
        "architect_proxy": LLMProvider.XAI,
        "ethicist_proxy": LLMProvider.XAI,  # Complex reasoning
        "researcher_proxy": LLMProvider.XAI,  # Research and analysis
        "pm_proxy": LLMProvider.OPENAI,
        "developer_proxy": LLMProvider.OPENAI,
        "qa_proxy": LLMProvider.OPENAI,
        "ux_proxy": LLMProvider.OPENAI,
        "coordinator_proxy": LLMProvider.OPENAI,
    }
    
    def __init__(self):
        self.xai_api_key = os.getenv("XAI_API_KEY", "")
        self.xai_api_base = os.getenv("XAI_API_BASE", "https://api.x.ai/v1")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        
        # Allow testing without API keys
        self.require_api_keys = os.getenv("REQUIRE_API_KEYS", "true").lower() == "true"
    
    def get_config(
        self,
        role: str,
        task_complexity: TaskComplexity = TaskComplexity.MODERATE,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> LLMConfig:
        """
        Get LLM configuration for a specific role and task.
        
        Args:
            role: The proxy role (architect, developer, etc.)
            task_complexity: Complexity of the task
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            LLMConfig with provider, model, and API details
        """
        # Determine provider based on role
        provider = self.ROLE_PROVIDER.get(role, LLMProvider.OPENAI)
        
        # Get model for provider and complexity
        model = self.MODEL_MAP.get((provider, task_complexity))
        
        if not model:
            raise ValueError(f"No model mapping for {provider}, {task_complexity}")
        
        # Get API credentials
        if provider == LLMProvider.XAI:
            api_key = self.xai_api_key
            api_base = self.xai_api_base
        else:
            api_key = self.openai_api_key
            api_base = self.openai_api_base
        
        if not api_key and self.require_api_keys:
            raise ValueError(f"API key not found for {provider.value}")
        
        return LLMConfig(
            provider=provider,
            model=model,
            api_key=api_key,
            api_base=api_base,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    
    def get_task_complexity(self, tool_name: str) -> TaskComplexity:
        """
        Determine task complexity based on tool name.
        
        Args:
            tool_name: Name of the tool being invoked
            
        Returns:
            TaskComplexity level
        """
        tool_lower = tool_name.lower()
        
        # Architecture and design tasks
        if any(keyword in tool_lower for keyword in ["design", "architecture", "adr", "evaluate"]):
            return TaskComplexity.COMPLEX
        
        # Security and critical review tasks
        if any(keyword in tool_lower for keyword in ["security", "critical", "consultation"]):
            return TaskComplexity.CRITICAL
        
        # Ethical review tasks
        if any(keyword in tool_lower for keyword in ["ethical", "review_"]):
            return TaskComplexity.CRITICAL
        
        # Simple queries and reads
        if any(keyword in tool_lower for keyword in ["read_", "query_", "get_", "list_"]):
            return TaskComplexity.SIMPLE
        
        # Code generation and implementation
        if any(keyword in tool_lower for keyword in ["write", "implement", "create", "generate"]):
            return TaskComplexity.MODERATE
        
        # Testing tasks
        if any(keyword in tool_lower for keyword in ["test", "qa", "validate"]):
            return TaskComplexity.MODERATE
        
        # Default to moderate
        return TaskComplexity.MODERATE
