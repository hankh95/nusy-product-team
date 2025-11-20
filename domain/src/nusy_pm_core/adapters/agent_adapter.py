"""
Agent adapter for autonomous multi‑agent experiments.

This module provides a minimal, test‑friendly implementation of the
``AgentAdapter`` expected by the autonomous experiment runner and its tests.

Key design points:
- No hard dependency on any specific LLM client; instead we expose an
  ``openai_client`` attribute that tests can patch.
- Async methods to match the expected usage in
  ``self-improvement/santiago-pm/quality-assessments/test_experiment_runner.py``.
"""

from __future__ import annotations

from typing import Any, List


class AgentAdapter:
    """
    Lightweight adapter around LLM‑backed role agents used by the autonomous
    experiment runner.

    In production this can be extended to talk to a real LLM client. For now
    it provides just enough behavior for tests and higher‑level orchestration:

    - ``list_available_agents`` returns the core Santiago crew roles.
    - ``initialize_agent`` and ``send_message`` delegate to an injected
      ``openai_client`` (patched in tests) when available, otherwise they
      degrade gracefully with simple fallback behavior.
    """

    def __init__(self) -> None:
        # Core crew roles for the autonomous experiment.
        self.available_agents: List[str] = ["quartermaster", "pilot", "santiago"]

        # Placeholder LLM client. Tests patch this with a mock that provides
        # ``chat.completions.create``. We intentionally do not import any
        # external SDK here.
        self.openai_client: Any = None

    async def list_available_agents(self) -> List[str]:
        """
        Return the list of logical agent identifiers that can participate
        in the experiment.
        """
        return list(self.available_agents)

    async def initialize_agent(self, agent_name: str) -> bool:
        """
        Perform any boot‑strapping needed for a given agent.

        In tests this method is usually patched, so the default implementation
        is conservative: it optionally calls into the injected ``openai_client``
        but otherwise simply reports success for known agents.
        """
        if agent_name not in self.available_agents:
            return False

        # If no client is configured, succeed optimistically.
        if self.openai_client is None:
            return True

        try:
            prompt = (
                f"You are {agent_name} in the Santiago crew. "
                "Acknowledge that you are ready to participate in the experiment."
            )
            _ = await self._create_chat_completion(prompt)
            return True
        except Exception:
            # Tests assert boolean success, not specific error details.
            return False

    async def send_message(self, agent_name: str, message: str) -> str:
        """
        Send a message to a named agent and return its response text.

        Tests patch ``openai_client.chat.completions.create`` and assert that
        the returned string is non‑empty and does not start with ``\"Error\"``.
        """
        if self.openai_client is None:
            # Simple echo‑style fallback when no real client is configured.
            return f"[{agent_name}] {message}"

        try:
            prompt = message
            response_text = await self._create_chat_completion(prompt)
            return response_text or ""
        except Exception as exc:  # pragma: no cover - defensive path
            return f"Error sending message: {exc}"

    async def _create_chat_completion(self, prompt: str) -> str:
        """
        Internal helper that normalizes calls into the injected LLM client.

        This shape matches the OpenAI ``chat.completions.create`` interface
        that tests patch with an ``AsyncMock``.
        """
        if self.openai_client is None:
            return ""

        # The exact model name is not important for tests; they patch the call.
        response = await self.openai_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        # Tests assume ``choices[0].message.content`` exists on the mock.
        return response.choices[0].message.content



