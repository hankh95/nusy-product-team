"""
Simple vLLM client wrapper for DGX-hosted OpenAI-compatible inference.

This does not change the existing LLMRouter behavior; it provides a focused
entry point for DGX vLLM services that can be used by experiments or
integrated into the router in the future.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI


class VLLMClient:
    """
    Thin async client for a DGX-hosted vLLM OpenAI-compatible endpoint.

    Configuration is read from environment variables so it can be reused
    across services and experiments:

    - VLLM_BASE_URL: base URL of the vLLM server (e.g. http://localhost:8000/v1)
    - VLLM_MODEL_NAME: model name to use (e.g. mistral-7b-instruct)
    - VLLM_API_KEY: optional dummy key if the server enforces auth
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        self.base_url = base_url or os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
        self.model = model or os.getenv("VLLM_MODEL_NAME", "mistral-7b-instruct")
        # vLLM can run without auth; provide a dummy key if needed
        self.api_key = api_key or os.getenv("VLLM_API_KEY", "EMPTY")

        self._client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Call the vLLM chat completion endpoint.

        Args:
            messages: List of role/content dicts.
            temperature: Sampling temperature.
            max_tokens: Optional max completion tokens.
            **kwargs: Extra parameters forwarded to the client.

        Returns:
            A dict with at least 'content' and 'raw_response' keys.
        """
        params: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        if max_tokens is not None:
            params["max_completion_tokens"] = max_tokens

        params.update(kwargs)

        try:
            response = await self._client.chat.completions.create(**params)
        except Exception as e:  # pragma: no cover - network error handling
            return {
                "error": str(e),
                "provider": "vllm",
                "base_url": self.base_url,
            }

        choice = response.choices[0]
        content = getattr(choice.message, "content", "") if choice and choice.message else ""

        return {
            "content": content,
            "raw_response": response,
            "provider": "vllm",
            "model": self.model,
        }


