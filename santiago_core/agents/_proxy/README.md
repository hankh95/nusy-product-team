# Proxy Agents (Phase 0)

## Purpose

These are "fake team" stubs that allow the factory to bootstrap itself
before any real Santiagos exist. See `docs/vision/fake_team_pack/`.

## Pattern

Each proxy:
1. Implements the MCP interface (tools + resources)
2. Delegates to external API/service
3. Has minimal domain logic (just translation layer)
4. Registers with discovery service
5. Gets replaced by real Santiago once built

## Lifecycle

```
Phase 0: Proxy agents only (external APIs)
Phase 1: First real Santiago built (factory can self-improve)
Phase 2+: Real Santiagos replace proxies one by one
```

## Creating a Proxy

1. Define MCP manifest in `knowledge/proxy-instructions/<name>.json`
2. Implement thin wrapper in `santiago_core/agents/_proxy/<name>.py`
3. Register with discovery service
4. Mark as "proxy" in trust registry (capability_level: apprentice)

See `ARCHITECTURE.md` for full pattern.
