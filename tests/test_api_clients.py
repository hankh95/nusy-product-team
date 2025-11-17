"""
Test real API client implementation in base_proxy.py

Verifies that the OpenAI and xAI client methods are properly implemented.
"""

import asyncio
import os
import pytest
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

from santiago_core.agents._proxy.pm_proxy import PMProxyAgent
from santiago_core.agents._proxy.architect_proxy import ArchitectProxyAgent
from santiago_core.services.llm_router import TaskComplexity


class TestAPIClients:
    """Test API client implementations"""

    def test_api_client_methods_exist(self):
        """Verify API client methods exist and are no longer stubs"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        pm = PMProxyAgent(workspace)
        
        # Verify methods exist
        assert hasattr(pm, "_call_openai_api")
        assert hasattr(pm, "_call_xai_api")
        assert hasattr(pm, "_build_prompt")
        
        # Verify they're not raising NotImplementedError (are implemented)
        import inspect
        
        # Get source code to check it's not just "raise NotImplementedError"
        openai_source = inspect.getsource(pm._call_openai_api)
        xai_source = inspect.getsource(pm._call_xai_api)
        
        assert "NotImplementedError" not in openai_source
        assert "NotImplementedError" not in xai_source
        assert "AsyncOpenAI" in openai_source
        assert "AsyncOpenAI" in xai_source

    @pytest.mark.asyncio
    async def test_openai_client_structure(self):
        """Test OpenAI client call structure (mocked)"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        pm = PMProxyAgent(workspace)
        
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"result": "test response"}'
        
        # Mock the LLM config
        from santiago_core.services.llm_router import LLMConfig, LLMProvider
        mock_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o-mini",
            api_key="test-key",
            api_base="https://api.openai.com/v1",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Mock AsyncOpenAI
        with patch("openai.AsyncOpenAI") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_instance
            
            # Call the method
            result = await pm._call_openai_api(
                mock_config,
                "test_tool",
                {"param": "value"}
            )
            
            # Verify result
            assert result == {"result": "test response"}
            
            # Verify OpenAI was called correctly
            mock_client.assert_called_once_with(
                api_key="test-key",
                base_url="https://api.openai.com/v1"
            )
            
            # Verify chat completion was called
            mock_instance.chat.completions.create.assert_called_once()
            call_args = mock_instance.chat.completions.create.call_args
            assert call_args.kwargs["model"] == "gpt-4o-mini"
            assert call_args.kwargs["temperature"] == 0.7
            assert call_args.kwargs["max_tokens"] == 2000

    @pytest.mark.asyncio
    async def test_xai_client_structure(self):
        """Test xAI client call structure (mocked)"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        architect = ArchitectProxyAgent(workspace)
        
        # Mock xAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"design": "test design"}'
        
        # Mock the LLM config for xAI
        from santiago_core.services.llm_router import LLMConfig, LLMProvider
        mock_config = LLMConfig(
            provider=LLMProvider.XAI,
            model="grok-beta",
            api_key="test-xai-key",
            api_base="https://api.x.ai/v1",
            temperature=0.8,
            max_tokens=4000
        )
        
        # Mock AsyncOpenAI (xAI uses OpenAI-compatible interface)
        with patch("openai.AsyncOpenAI") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_instance
            
            # Call the method
            result = await architect._call_xai_api(
                mock_config,
                "test_tool",
                {"param": "value"}
            )
            
            # Verify result
            assert result == {"design": "test design"}
            
            # Verify xAI client was created with correct endpoint
            mock_client.assert_called_once_with(
                api_key="test-xai-key",
                base_url="https://api.x.ai/v1"
            )
            
            # Verify chat completion was called
            mock_instance.chat.completions.create.assert_called_once()
            call_args = mock_instance.chat.completions.create.call_args
            assert call_args.kwargs["model"] == "grok-beta"
            assert call_args.kwargs["temperature"] == 0.8

    @pytest.mark.asyncio
    async def test_o1_model_special_handling(self):
        """Test that o1-preview models use special parameters"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        pm = PMProxyAgent(workspace)
        
        # Mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"result": "o1 response"}'
        
        # Mock config for o1-preview
        from santiago_core.services.llm_router import LLMConfig, LLMProvider
        mock_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="o1-preview",
            api_key="test-key",
            api_base="https://api.openai.com/v1",
            temperature=0.7,
            max_tokens=2000
        )
        
        with patch("openai.AsyncOpenAI") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_instance
            
            # Call the method
            result = await pm._call_openai_api(
                mock_config,
                "test_tool",
                {"param": "value"}
            )
            
            # Verify o1-specific parameters
            call_args = mock_instance.chat.completions.create.call_args
            
            # o1 should use max_completion_tokens instead of max_tokens
            assert "max_completion_tokens" in call_args.kwargs
            assert "max_tokens" not in call_args.kwargs
            
            # o1 should not have temperature parameter
            assert "temperature" not in call_args.kwargs
            
            # o1 should have user message with instructions embedded
            messages = call_args.kwargs["messages"]
            assert len(messages) == 1  # Only user message, no system message
            assert messages[0]["role"] == "user"

    def test_build_prompt_method(self):
        """Test prompt building from tool definitions"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        pm = PMProxyAgent(workspace)
        
        # Build a prompt for a known tool
        prompt = pm._build_prompt(
            "create_story",
            {"feature": "User authentication"}
        )
        
        # Verify prompt structure
        assert "create_story" in prompt
        assert "feature" in prompt
        assert "User authentication" in prompt
        assert "Parameters:" in prompt or "parameters" in prompt.lower()

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in API clients"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        pm = PMProxyAgent(workspace)
        
        # Mock config
        from santiago_core.services.llm_router import LLMConfig, LLMProvider
        mock_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o-mini",
            api_key="test-key",
            api_base="https://api.openai.com/v1",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Mock AsyncOpenAI to raise an exception
        with patch("openai.AsyncOpenAI") as mock_client:
            mock_client.side_effect = Exception("API Error")
            
            # Call should return error dict, not raise
            result = await pm._call_openai_api(
                mock_config,
                "test_tool",
                {"param": "value"}
            )
            
            # Verify error response structure
            assert "error" in result
            assert result["tool"] == "test_tool"
            assert result["provider"] == "openai"
            assert "API Error" in result["error"]

    @pytest.mark.asyncio
    async def test_non_json_response_handling(self):
        """Test handling of non-JSON responses from LLM"""
        workspace = Path("./test_workspace")
        workspace.mkdir(exist_ok=True)
        
        pm = PMProxyAgent(workspace)
        
        # Mock response with non-JSON content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is plain text, not JSON"
        
        from santiago_core.services.llm_router import LLMConfig, LLMProvider
        mock_config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o-mini",
            api_key="test-key",
            api_base="https://api.openai.com/v1",
            temperature=0.7,
            max_tokens=2000
        )
        
        with patch("openai.AsyncOpenAI") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.chat.completions.create = AsyncMock(return_value=mock_response)
            mock_client.return_value = mock_instance
            
            result = await pm._call_openai_api(
                mock_config,
                "test_tool",
                {"param": "value"}
            )
            
            # Should return structured response with raw text
            assert "raw_response" in result
            assert result["raw_response"] == "This is plain text, not JSON"
            assert result["tool"] == "test_tool"
