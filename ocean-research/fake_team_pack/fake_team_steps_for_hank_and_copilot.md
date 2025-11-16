# Steps for Hank & Copilot: Bootstrapping the Fake NuSy Team

## Step 1: Create minimal MCP agents
Roles: PM, Architect, Developer1, Developer2, Ethicist.  
Each exposes: `status`, `capabilities`, `request_help`.

## Step 2: Implement proxy tools
Each agent forwards reasoning requests to external LLM API via:
- `llm_proxy.call(model, prompt)`
- Simple JSON return.

## Step 3: Set up shared memory
Create:
- `knowledge/shared/working-agreements.md`
- `knowledge/shared/team-roster.ttl`
- `knowledge/shared/ships-log/`

## Step 4: Start the fake team locally
Run each agent as a local MCP server:
```
python agents/pm.py
python agents/architect.py
python agents/dev1.py
...
```

## Step 5: Run coordinator
Coordinator assigns tasks:
- PM → planning
- Architect → design
- Devs → implementation
- Ethicist → review

## Step 6: Begin evolutionary cycles
Keep all decisions in:
- `ships-log/`
- `evolution-reviews.md`
