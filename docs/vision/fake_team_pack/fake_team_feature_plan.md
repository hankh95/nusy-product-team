# Faking the NuSy Team for Two Weeks
## Purpose
Spin up PM, Architect, Devs, Ethicist as MCP agents with minimal logic. Behind MCP, call external AI APIs for reasoning until DGX arrives.

## Capabilities
- Lightweight MCP servers per role.
- Proxy tools: `llm_query`, `bdd_help`, `arch_help`.
- Shared memory via repo `knowledge/`.
- Coordinator routes tasks to agents.
- Hank acts as Captain with final authority.

## Behavior
- Agents expose limited skills (Pond scope).
- Use external LLM for domain reasoning.
- Update team roster and logs.
- Produce scaffolds for real agents later.
