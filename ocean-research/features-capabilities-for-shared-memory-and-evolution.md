# Santiago-PM & Santiago-Ethicist – Shared Memory & Evolution Plan  
_For use by AI agents (e.g., Grok Code Fast 1 / Copilot) working in VS Code_

## 1. Purpose

This document defines a **feature/capability plan** for building:

1. **Santiago-PM** – a Product Manager–domain Santiago agent with:
   - Long-term, shared **team memory**
   - Knowledge of **tools, working agreements, and BDD practices**
   - Awareness of **who is on the team and what they can do** (MCP capabilities)

2. **Santiago-Ethicist** – an early, always-on ethical advisor that:
   - Monitors the evolution of Santiago & Manolin agents
   - Helps enforce ethical constraints on capabilities and decisions

3. A pattern for **smaller Santiagos**:
   - **Apprentice / Journeyman / Master** skill levels
   - **Pond / Lake / Sea / Ocean** knowledge scopes
   - Packaged as **small MCP-capable domain capsules** that can be plugged into other Santiagos

The goal is to enable **evolutionary development** in cycles and to make **knowledge & capability modular**, so a VS Code AI agent can:

- Help implement these features incrementally
- Reuse prior knowledge instead of losing context across sessions
- Build a **long-running team** that gets better over time

---

## 2. Core Concepts & Metaphors

### 2.1 Santiago & Manolin

- **Santiago** = a mature, domain-capable NeuroSymbolic agent (e.g., Santiago-PM, Santiago-Ethicist, Santiago-Developer, etc.).
- **Manolin** = apprentice / supporting agent, often narrower in scope, learning from one or more Santiagos.

### 2.2 Skill Levels (Apprentice / Journeyman / Master)

Each Santiago-domain “capsule” can exist at three levels:

- **Apprentice**
  - Very focused, small slice of a domain.
  - Limited tools & responsibilities.
  - Good for experimentation / “shareable sub-Santiago.”

- **Journeyman**
  - Broader coverage.
  - Can work independently on well-scoped tasks.
  - Understands and applies BDD & working agreements.

- **Master**
  - Deep domain knowledge.
  - Can propose new capabilities, tools, and changes to the system.
  - Often a “team anchor” for that domain (e.g., Santiago-PM).

### 2.3 Knowledge Scope (Pond / Lake / Sea / Ocean)

Each Santiago-domain capsule also has a **knowledge scope**:

- **Pond** – small, highly focused set of knowledge (e.g., “BDD working agreements for PM”).
- **Lake** – medium-sized domain (e.g., “All NuSy team working agreements & practices”).
- **Sea** – large domain (e.g., “Product management in NuSy + MCP-based teams”).
- **Ocean** – very large, multi-domain knowledge (e.g., “Full NuSy + CDS + software product ecosystem”).

These are not just metaphors; they should appear as **attributes on each MCP manifest** and in the knowledge graph.

---

## 3. Shared Collective Memory vs Domain Memory

### 3.1 Requirements

- The **team** needs a **collective, long-term memory**, independent of:
  - VS Code session lifetime
  - Model/context length
  - Single-agent short-term context

- Each **Santiago-domain expert** can still have **local/domain memory**, but:
  - Core concepts about **how we work** (BDD, tools, agreements) must be:
    - Shared
    - Stable
    - Discoverable by all agents

### 3.2 Design

**Shared Memory (Team-Level)**

- Stored as versioned files + knowledge graph in the repo, plus structured logs:
  - `knowledge/shared/working-agreements.md`
  - `knowledge/shared/bdd-practices.md`
  - `knowledge/shared/tools-and-mcp-capabilities.md`
  - `knowledge/shared/ships-log/` (daily reports, evolution summaries)
  - `knowledge/shared/team-roster-and-capabilities.ttl` (RDF or similar)

- Accessible via MCP tools:
  - `team_memory.read_shared(section: str)`
  - `team_memory.append_ship_log(entry)`
  - `team_memory.query_kg(query)`

**Domain Memory (Per-Santiago)**

- Stored as domain-specific artifacts:
  - `knowledge/domains/pm/` (Santiago-PM)
  - `knowledge/domains/ethics/` (Santiago-Ethicist)
  - `knowledge/domains/<other-domain>/`

- Also exposed via MCP tools:
  - `domain_memory.get(domain, scope)`
  - `domain_memory.update(domain, scope, patch)`

The VS Code AI agent (Grok/Copilot) should prefer **reading from these files & KG** rather than relying solely on transient chat context.

---

## 4. Santiago-PM: Capabilities & Features

### 4.1 Primary Role

Santiago-PM is responsible for:

- Maintaining **team working agreements**, especially around:
  - BDD / TDD
  - Tool usage
  - Definition of done
  - Dev practices
- Knowing **who is on the team**, via:
  - MCP manifests
  - KG roster
- Coordinating **evolutionary cycles**:
  - Define hypotheses
  - Plan experiments
  - Review outcomes
  - Update team practices

### 4.2 Key Capabilities

1. **Team Roster & Capabilities Awareness**
   - Read MCP manifests for all registered agents.
   - Maintain a `team-roster` graph of:
     - Agents
     - Skill levels (Apprentice/Journeyman/Master)
     - Knowledge scope (Pond/Lake/Sea/Ocean)
     - Tools & permissions

2. **Working Agreements Manager**
   - Read/write files like:
     - `knowledge/shared/working-agreements.md`
   - Provide a summary for other agents when requested.

3. **Evolution Planner**
   - Propose evolutionary cycles:
     - “Next iteration we improve PM–Dev handoffs.”
   - Use BDD to express desired behavior.

4. **Missing Skill Detector**
   - When a task requires skills not present:
     - Suggest:
       - Use of external LLM API (temporary)
       - Creation of a new Santiago-domain agent (long-term).

---

## 5. Santiago-Ethicist: Capabilities & Features

### 5.1 Primary Role

Santiago-Ethicist:

- Monitors:
  - Planned features
  - New domain Santiagos
  - Tool additions
- Flags:
  - Ethical risks
  - Misuse potentials
  - Data sensitivity issues

### 5.2 Key Capabilities

1. **Ethical Review of Evolutions**
   - Receives proposed changes from Santiago-PM and/or Architect.
   - Reviews:
     - New roles
     - New tools
     - New data usage
   - Writes an ethics note to:
     - `knowledge/domains/ethics/evolution-reviews.md`.

2. **Guardrails Suggestion**
   - Suggests:
     - Additional constraints
     - Logging requirements
     - Approval flows for risky actions.

3. **Ethical MCP Capability Manifest**
   - Advertises:
     - Types of checks it can perform.
     - Domains it is competent in.
     - Known blind spots.

---

## 6. Smaller Santiagos as Packaged MCP Modules

### 6.1 Goal

Allow **small domain knowledge/capability packages** (Apprentice Santiagos) to be:

- Easily created
- Shared
- Composed inside other Santiagos

Examples:

- `Santiago-PM-Apprentice` → knows only:
  - BDD basics
  - Our working agreements file

- `Santiago-BDD-Coach` → small agent:
  - Specializes in writing/cleaning BDD feature files

### 6.2 Design

Each **small Santiago** is:

- An MCP service with:
  - A minimal manifest
  - One or a few tools
  - Limited knowledge scope (Pond/Lake)

- Registered with:
  - The PM
  - The KG roster

This lets **larger Santiagos**:
- Call these small MCP services for specific tasks.
- Be “composed” from smaller, reusable capabilities.

---

## 7. Evolutionary Cycles

### 7.1 Cycle Pattern

Each evolution cycle should follow:

1. **Hypothesis**
   - Example:
     > “If we add a Santiago-BDD-Coach apprentice, then the team will create better, more consistent BDD scenarios, reducing time in test triage.”

2. **Experiment Design**
   - PM + Developer define:
     - Scope
     - Metrics
     - Timebox

3. **Implementation**
   - Copilot/AI + human implement:
     - New Santiago agent (or capability)
     - New tests & logging

4. **Observation**
   - Logs, metrics, daily “ship’s logs” stored in:
     - `knowledge/shared/ships-log/`

5. **Reflection**
   - PM + Ethicist + Architect:
     - Review outcome
     - Decide whether to promote from Apprentice → Journeyman → Master
     - Update working agreements

### 7.2 Support from VS Code AI

The VS Code AI agent should:

- Use this pattern when proposing changes.
- Write/modify:
  - BDD scenarios
  - Implementation tasks
  - Documentation in the knowledge folder
- Always reference:
  - Current working agreements
  - Team roster
  - Last few ship’s logs

---

## 8. Feature Plan for VS Code AI to Implement

The following are **concrete features** the VS Code AI can start working on, in roughly this order.

### Feature 1 – Shared Memory File Layout

- [ ] Create folder structure under the repo:
  - `knowledge/shared/`
  - `knowledge/domains/pm/`
  - `knowledge/domains/ethics/`
  - `knowledge/shared/ships-log/`
- [ ] Create initial files:
  - `knowledge/shared/working-agreements.md`
  - `knowledge/shared/bdd-practices.md`
  - `knowledge/shared/tools-and-mcp-capabilities.md`
  - `knowledge/shared/team-roster-and-capabilities.ttl`
  - `knowledge/domains/ethics/evolution-reviews.md`

### Feature 2 – Santiago-PM Initial Spec & MCP Manifest

- [ ] Define `Santiago-PM` MCP manifest with:
  - role: `PM`
  - skill-level: `Master`
  - knowledge-scope: `Sea` (initially)
  - tools:
    - `read_working_agreements`
    - `update_working_agreements`
    - `read_team_roster`
    - `propose_evolution_cycle`

- [ ] Implement a minimal Santiago-PM agent that:
  - Reads/writes the shared knowledge files
  - Can summarize current team state for other agents

### Feature 3 – Santiago-Ethicist Initial Spec & MCP Manifest

- [ ] Define `Santiago-Ethicist` MCP manifest with:
  - role: `Ethicist`
  - skill-level: `Journeyman` (initially)
  - knowledge-scope: `Lake`
  - tools:
    - `review_evolution_plan`
    - `write_ethics_note`

- [ ] Implement a minimal Santiago-Ethicist agent that:
  - Reads planned feature/evolution docs
  - Writes ethics notes into `evolution-reviews.md`

### Feature 4 – Apprentice Santiago Packages

- [ ] Define a small “Apprentice” specification with:
  - limited tools
  - `knowledge-scope: Pond`
  - explicit dependencies (which Master/Journeyman they learn from)

- [ ] Implement one example:
  - `Santiago-BDD-Apprentice`
    - Tools:
      - `suggest_bdd_scenarios`
      - `normalize_bdd_format`

### Feature 5 – Team Roster & Capability Graph

- [ ] Implement `team-roster-and-capabilities.ttl` schema
- [ ] Add a simple Python utility:
  - `update_team_roster.py` to:
    - Read MCP manifests
    - Update the roster graph with:
      - agent name
      - skill level
      - knowledge scope
      - tools

### Feature 6 – Evolution Cycle Template

- [ ] Create:
  - `knowledge/shared/evolution-cycles/`
  - Template file for a new evolution cycle:
    - `YYYY-MM-DD-evolution-cycle-<name>.md`
- [ ] Add script or instructions for:
  - PM to generate a new cycle file
  - Ethicist to review it
  - Dev agent to derive implementation tasks

---

## 9. Instructions to the VS Code AI (Copilot / Grok Code Fast 1)

When using this document:

1. **Always check the `knowledge/` folder first**  
   - Read working agreements, tools, and team roster before proposing changes.

2. **When creating or changing agents:**
   - Ensure each agent has an **MCP manifest** declaring:
     - role, skill level, knowledge scope, tools.
   - Update the **team roster**.

3. **When proposing new capabilities:**
   - Suggest an **Apprentice version first** (Pond scope).
   - Design an evolutionary path to Journeyman and Master.

4. **When proposing significant changes:**
   - Invoke **Santiago-Ethicist** to review.
   - Record an entry in:
     - `evolution-reviews.md`
     - `ships-log/`

5. **Use BDD whenever possible** to express behaviors:
   - Especially for:
     - PM workflows
     - ethics reviews
     - agent collaboration patterns

---

_End of feature/capability plan._