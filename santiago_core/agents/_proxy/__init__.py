"""Proxy Agents - Phase 0 Fake Team

These are thin wrappers around external APIs/tools, used to bootstrap
the factory before real Santiagos exist.

Pattern: Each proxy implements the MCP interface but delegates to
external services. As real Santiagos are built, they replace proxies.
"""

from santiago_core.agents._proxy.base_proxy import (
    BaseProxyAgent,
    MCPTool,
    MCPManifest,
    ProxyConfig,
    ProxyBudgetExceeded,
    ProxySessionExpired,
)
from santiago_core.agents._proxy.pm_proxy import PMProxyAgent
from santiago_core.agents._proxy.ethicist_proxy import EthicistProxyAgent
from santiago_core.agents._proxy.architect_proxy import ArchitectProxyAgent
from santiago_core.agents._proxy.developer_proxy import DeveloperProxyAgent
from santiago_core.agents._proxy.qa_proxy import QAProxyAgent
from santiago_core.agents._proxy.ux_proxy import UXProxyAgent
from santiago_core.agents._proxy.platform_proxy import PlatformProxyAgent

__all__ = [
    # Base classes
    "BaseProxyAgent",
    "MCPTool",
    "MCPManifest",
    "ProxyConfig",
    "ProxyBudgetExceeded",
    "ProxySessionExpired",
    # Proxy agents
    "PMProxyAgent",
    "ArchitectProxyAgent",
    "DeveloperProxyAgent",
    "QAProxyAgent",
    "UXProxyAgent",
    "PlatformProxyAgent",
    "EthicistProxyAgent",
]
