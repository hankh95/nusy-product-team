"""
Test suite for Ethicist Proxy Agent

Tests ethical oversight based on Baha'i principles
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from santiago_core.agents._proxy.ethicist_proxy import EthicistProxyAgent
from santiago_core.core.agent_framework import Message, Task


@pytest.fixture
def workspace_path(tmp_path):
    """Create temporary workspace"""
    workspace = tmp_path / "test_workspace"
    workspace.mkdir()
    return workspace


@pytest.fixture
def ethicist_proxy(workspace_path):
    """Create Ethicist proxy instance"""
    return EthicistProxyAgent(workspace_path)


class TestEthicistProxyInitialization:
    """Test Ethicist proxy initialization"""

    def test_ethicist_proxy_creation(self, ethicist_proxy):
        """Should initialize with Ethicist-specific manifest"""
        assert ethicist_proxy.name == "ethicist-proxy"
        assert ethicist_proxy.manifest.role == "ethicist"
        assert "ethical_review" in ethicist_proxy.manifest.capabilities

    def test_bahai_principles_loaded(self, ethicist_proxy):
        """Should load all 12 Baha'i principles"""
        assert len(ethicist_proxy.bahai_principles) == 12
        assert "Unity of God" in ethicist_proxy.bahai_principles
        assert "Unity of Humanity" in ethicist_proxy.bahai_principles
        assert "Equality of Men and Women" in ethicist_proxy.bahai_principles

    def test_ethicist_tools_available(self, ethicist_proxy):
        """Should have ethical review tools"""
        tool_names = [tool.name for tool in ethicist_proxy.manifest.input_tools]
        assert "read_feature" in tool_names
        assert "read_decision" in tool_names
        assert "query_principles" in tool_names


class TestEthicalReview:
    """Test ethical review functionality"""

    @pytest.mark.asyncio
    async def test_review_feature(self, ethicist_proxy):
        """Should review feature against Baha'i principles"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "review": {
                    "approved": True,
                    "principles_applied": [
                        "Unity of Humanity",
                        "Universal Education",
                        "Independent Investigation of Truth"
                    ],
                    "concerns": [],
                    "recommendations": "Feature aligns with principles of service"
                }
            }

            result = await ethicist_proxy.invoke_tool("ethical_review", {
                "subject": "feature",
                "description": "Enable autonomous learning for all users"
            })

            assert result["review"]["approved"] is True
            assert len(result["review"]["principles_applied"]) > 0

    @pytest.mark.asyncio
    async def test_review_with_concerns(self, ethicist_proxy):
        """Should flag ethical concerns"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "review": {
                    "approved": False,
                    "principles_applied": ["Equality of Men and Women", "Elimination of Prejudice"],
                    "concerns": [
                        "Potential gender bias in training data",
                        "Lack of diversity testing"
                    ],
                    "recommendations": "Add bias testing and diverse user validation"
                }
            }

            result = await ethicist_proxy.invoke_tool("ethical_review", {
                "subject": "feature",
                "description": "User profiling system"
            })

            assert result["review"]["approved"] is False
            assert len(result["review"]["concerns"]) > 0

    @pytest.mark.asyncio
    async def test_principle_guidance(self, ethicist_proxy):
        """Should provide principle-based guidance"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "guidance": {
                    "principle": "Unity of Humanity",
                    "application": "Design for global accessibility",
                    "concrete_actions": [
                        "Support multiple languages",
                        "Consider diverse cultural contexts",
                        "Test with international users"
                    ]
                }
            }

            result = await ethicist_proxy.invoke_tool("principle_guidance", {
                "principle": "Unity of Humanity",
                "context": "Building user interface"
            })

            assert result["guidance"]["principle"] == "Unity of Humanity"
            assert len(result["guidance"]["concrete_actions"]) > 0


class TestConsultationFacilitation:
    """Test consultation facilitation"""

    @pytest.mark.asyncio
    async def test_convene_consultation(self, ethicist_proxy):
        """Should convene ethical consultation"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "consultation": {
                    "topic": "Data privacy approach",
                    "participants": ["pm", "developer", "platform", "ethicist"],
                    "status": "scheduled"
                }
            }

            result = await ethicist_proxy.invoke_tool("convene_consultation", {
                "topic": "Data privacy approach",
                "participants": ["pm", "developer", "platform"]
            })

            assert result["consultation"]["status"] == "scheduled"

    @pytest.mark.asyncio
    async def test_consultation_report(self, ethicist_proxy):
        """Should generate consultation report"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "report": {
                    "topic": "Feature prioritization",
                    "participants": ["pm", "architect", "ethicist"],
                    "synthesis": "Consensus reached on user benefit focus",
                    "decisions": ["Prioritize accessibility features"],
                    "dissent": None
                }
            }

            result = await ethicist_proxy.invoke_tool("consultation_report", {
                "consultation_id": "consult_001"
            })

            assert "synthesis" in result["report"]
            assert len(result["report"]["decisions"]) > 0


class TestServiceAlignment:
    """Test service to humanity alignment"""

    @pytest.mark.asyncio
    async def test_service_check(self, ethicist_proxy):
        """Should evaluate service to humanity"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "service_alignment": {
                    "serves_genuine_need": True,
                    "benefits": "Enables learning for underserved communities",
                    "potential_harms": "Minimal, privacy protected",
                    "recommendation": "Proceed with implementation"
                }
            }

            result = await ethicist_proxy.invoke_tool("check_service_alignment", {
                "description": "Free educational platform for remote learners"
            })

            assert result["service_alignment"]["serves_genuine_need"] is True

    @pytest.mark.asyncio
    async def test_flag_concern(self, ethicist_proxy):
        """Should flag ethical concerns to team"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "flag": {
                    "severity": "high",
                    "concern": "User manipulation detected",
                    "principle_violated": "Independent Investigation of Truth",
                    "action_required": "Immediate review and redesign"
                }
            }

            result = await ethicist_proxy.invoke_tool("flag_concern", {
                "concern": "Dark patterns in UI",
                "severity": "high"
            })

            assert result["flag"]["severity"] == "high"
            assert "principle_violated" in result["flag"]


class TestPrincipleApplication:
    """Test application of specific Baha'i principles"""

    @pytest.mark.asyncio
    async def test_unity_of_humanity_check(self, ethicist_proxy):
        """Should check Unity of Humanity principle"""
        result = await ethicist_proxy.check_principle_alignment(
            "Unity of Humanity",
            "Feature excludes users from certain countries"
        )

        # Should detect violation
        assert result["aligned"] is False

    @pytest.mark.asyncio
    async def test_equality_check(self, ethicist_proxy):
        """Should check gender equality principle"""
        result = await ethicist_proxy.check_principle_alignment(
            "Equality of Men and Women",
            "Feature provides equal access to all users"
        )

        # Should approve
        assert result["aligned"] is True

    @pytest.mark.asyncio
    async def test_education_principle(self, ethicist_proxy):
        """Should check Universal Education principle"""
        result = await ethicist_proxy.check_principle_alignment(
            "Universal Compulsory Education",
            "Feature has high learning curve, no documentation"
        )

        # Should flag concern
        assert result["aligned"] is False
        assert "education" in result["guidance"].lower()


class TestEthicalDecisionFramework:
    """Test ethical decision framework"""

    @pytest.mark.asyncio
    async def test_full_decision_framework(self, ethicist_proxy):
        """Should apply full ethical decision framework"""
        with patch.object(ethicist_proxy, '_call_external_api', new_callable=AsyncMock) as mock_api:
            mock_api.return_value = {
                "decision": {
                    "stakes": "Affects 10,000 users, data privacy implications",
                    "principles_applied": ["Independent Investigation of Truth", "Unity of Humanity"],
                    "consultation_needed": True,
                    "options_evaluated": 3,
                    "recommendation": "Option B with privacy safeguards",
                    "reasoning": "Balances user benefit with privacy protection"
                }
            }

            result = await ethicist_proxy.invoke_tool("apply_decision_framework", {
                "decision": "User data collection approach",
                "options": ["Option A", "Option B", "Option C"]
            })

            assert "recommendation" in result["decision"]
            assert len(result["decision"]["principles_applied"]) > 0
