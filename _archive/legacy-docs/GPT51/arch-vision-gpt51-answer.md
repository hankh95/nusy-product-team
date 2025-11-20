## Santiago / NuSy DGX Runtime & Architecture Alignment  
**File:** `docs-arch-redux-3/GPT51/arch-vision-gpt51-answer.md` (proposed)  
**Date:** 2025-11-20  

---

## 1. Vision Summary (DGX + Runtime + Agents)

### 1.1 Story & Metaphor

Santiago is described as the captain of a small, strange ship: a **multi-agent NuSy crew** that builds software together while sailing an ocean made of other people’s knowledge.

- **The Ocean**: External knowledge sources and customer domains (guidelines, PDFs, books, repos, APIs, datasets).
- **The Ship (Santiago runtime)**: The running multi-agent system on the DGX, including:
  - Santiago-core (NuSy brain with a 4-layer knowledge model).
  - LLMs and MCP tools.
  - Knowledge graphs.
  - In-memory Git and Kanban as the “live hull” of artifacts.
- **The Crew**:
  - Architect, PM, Developers, QA, DevOps, Ethicist, plus domain experts.
  - They behave like a real software team, but all are NuSy agents.

### 1.2 Santiago-core as NuSy Brain

From the vision:

- **4-layer knowledge model**:
  - Narrative / raw domain sources.
  - Structured knowledge (triples, graphs).
  - Computable logic (rules, decision logic).
  - Executable workflows (MCP services, pipelines).
- **Fast graph-based memory**:
  - Concept / relationship / rule graphs underpin all reasoning.
- **In-memory Git & file-system-as-truth**:
  - All artifacts (features, expeditions, manifests, tests, logs) live as files.
  - Kanban is a **view on the file system**, not an independent DB.
  - In-memory Git provides a live collaboration substrate:
    - Branches, commits, and merges as “safe harbors” and voyage logs.

### 1.3 Multi-Agent Crew (Runtime Roles)

The crew is defined as:

- **Architect**: Maintains system structure, interfaces, and architectural integrity.
- **PM**: Manages Kanban/backlog, expeditions, priorities; hosts NuSy product management.
- **Developers**: Implement/refactor/test code and tools.
- **QA**: Owns BDD/TDD, regression safety, scenario validation.
- **DevOps**: CI/CD, observability, DGX orchestration, runtime reliability.
- **Ethicist**: Alignment, safety, consent, Baha’i-inspired principles, long-term stewardship.
- **Domain Experts**: NuSy-Domain Experts (daughter ships) for specific domains, loaded with specialized KGs/toolsets.

Each is both:

- A **role in the socio-technical process**, and  
- A **NuSy-configurable agent “character”** with its own domain knowledge and tools.

### 1.4 Role of DGX & Work Modes

The vision explicitly uses a **day/night** metaphor:

- **Day – “At Sea” mode**:
  - Crew focuses on external projects and domains.
  - Tasks:
    - Ingest external knowledge (the ocean).
    - Break it down and validate via BDD scenarios.
    - Turn it into executables (MCP tools, APIs, services).
- **Night – “In the Shipyard” mode** (DGX-centric self-work):
  - The DGX is the **shipyard**: place to improve Santiago-core and the crew.
  - Tasks:
    - Improve Santiago-core (knowledge engine, memory, tools).
    - Upgrade agent roles (Architect, PM, Dev, QA, DevOps, Ethicist).
    - Tighten workflows, tests, observability, and safety.

The same document also suggests a **unified always-on view**:

- “In one version of the story, the ‘day at sea’ and ‘night in the shipyard’ are just different modes of the **same always-on system**.”
- DGX hosts:
  - The ship (runtime).
  - In-memory Git and Kanban.
  - Multiple repos (core internal + per-customer).

Agents continuously choose between:

- **Domain / customer work**, and  
- **Self-improvement work**,  

based on lean flow and experiment data, with the Ethicist enforcing ethical constraints.

### 1.5 In-Memory Git & Knowledge Graphs

Key vision elements:

- **In-memory Git**:
  - Shared, high-performance workspace for all artifacts.
  - Periodic commits/snapshots as safe harbors and voyage logs.
- **Knowledge graphs (KGs)**:
  - Capture domain concepts, relationships, and rules.
  - Back:
    - Domain knowledge for NuSy-Domain Experts.
    - Self-improvement knowledge (methods, experiments, refactors).
    - Experiments, BDD/TDD suites, CI/CD decision surfaces.

Together with Kanban, these form an **always-in-memory operating loop**:

- Kanban: “What should we do next?”
- KGs: “What do we know and how does it relate?”
- In-memory Git: “What is the current working set and history?”
- CI/CD, BDD/TDD: “Is this change safe, correct, and aligned?”

---

## 2. Current Architecture & Plan Summary

### 2.1 Current Architecture (ARCHITECTURE.md)

The current active architecture is described in `ARCHITECTURE.md` at the project root (not under `docs/`). In summary:

- **Factory Pattern**:
  - The repo is a **Santiago Factory** for generating domain-specific Santiagos.
  - Components like CatchFish, FishNet, Navigator, and Passage map roughly to:
    - Ingestion.
    - Behavior validation.
    - Orchestration.
    - Workflow execution.
- **File-System-as-Truth**:
  - Artifacts (features, expeditions, manifests, logs) live as markdown/feature files.
  - Knowledge graphs and tests are meant to be tightly connected to these artifacts.
- **Work Organization**:
  - Kanban system as unified workflow view:
    - Root-level `kanban-boards.md` and `santiago-pm/kanban-boards.md`.
    - CLI in `santiago-pm/tackle/kanban/`.
  - Concepts:
    - **Features** (`features/*.feature`).
    - **Expeditions** (`expeditions/exp_0xx/`).
    - **Voyage Trials**.
  - Work is tracked via Kanban cards referencing real files.
- **Runtime**:
  - Primarily documented as a conceptual system:
    - Agents.
    - KG-dependent behavior.
    - Orchestration flows.
  - DGX is acknowledged as the target hardware, but:
    - The doc does **not** yet fully describe an always-on DGX runtime.
    - In-memory Git is mentioned mostly in vision-oriented material, not detailed as operational substrate.

### 2.2 Development Plan (DEVELOPMENT_PLAN.md)

`DEVELOPMENT_PLAN.md` at the project root is a **thin, Kanban-centric view** of current work:

- **Source of truth**: The Kanban board (`kanban-boards.md`).
- **Key priorities (next 24 hours – DGX)**:
  - DGX Readiness Preparation.
  - System Persistence & Safety Mechanisms.
  - Mistral LLM Integration & Role-Based AI Access.
  - Team Readiness Assessment.
- **Usage**:
  - View work via `kanban-boards.md`.
  - Use Kanban CLI or MCP to add/move work.
  - Run `dgx_readiness_prioritization.py` for AI-driven prioritization.

This plan expresses **immediate operational focus** (especially DGX deployment readiness), rather than long-term architecture.

### 2.3 Santiago Development Master Plan

`santiago-pm/navigation-charts/santiago-development-master-plan.md` contains a **multi-phase strategic plan**:

- **Phase 1 – Foundation & Architecture**:
  - Establish core architecture and PM domain integration.
  - Experiments on PM artifact management and agent communication.
- **Phase 2 – Knowledge & Learning Systems**:
  - Build feedback loops and learning cycles.
  - Ontology learning, hypothesis generation.
- **Phase 3 – Multi-Agent Swarm Evolution**:
  - Role specialization, swarm coordination, evolutionary learning.
- **Phase 4 – Domain Santiago Factory**:
  - Automated generation of domain Santiagos.
- **Phase 5 – Enterprise Integration & Scaling**:
  - Enterprise workflows, multi-project federation, compliance.
- **Phase 6 – Advanced AI Integration & Evolution**:
  - AGI safety, advanced models, quantum knowledge, emergent behavior.

This master plan:

- Explicitly includes **multi-agent swarms** and **self-improvement**.
- Treats DGX and runtime more as underlying infrastructure than as an explicitly modeled always-on loop.
- Uses Lean Hypothesis Testing: experiments + features + implementation tasks + success metrics per phase.

### 2.4 Gaps vs. the New Vision

Compared to the vision in `arch-vision-gpt51.md`:

- **DGX runtime**:
  - Current docs mention DGX but don’t clearly define:
    - Always-on vs dual-mode runtime.
    - How in-memory Git + KG + Kanban form a live loop.
- **In-memory Git & KG**:
  - Present more as aspirational / conceptual; not fully integrated into the “current truth.”
- **Self-improvement system**:
  - Phases describe learning and evolution, but:
    - There is no explicit dual-KG/git model per Santiago.
    - “Shipyard” self-improvement mode is not cleanly modeled in architecture docs.
- **Kanban as file-system view**:
  - The implementation already behaves this way; architecture docs could be clearer about it being a “view,” not a DB.

---

## 3. DGX-Related Work Found in the Repo (Today)

### 3.1 DGX Provisioning, Readiness, Observability, Storage

- **Features (Gherkin)**:
  - `features/dgx-provisioning-automation.feature`  
    - Automating DGX setup/provisioning workflows.
  - `features/dgx-monitoring-observability.feature`  
    - Metrics, health, logging, and observability for DGX.
  - `features/dgx-storage-expansion-procurement.feature`  
    - Storage expansion and procurement flows for DGX.

- **Workspace & Expedition Artifacts (DGX readiness)**:
  - `dgx_readiness_prioritization.py`  
    - AI-based prioritization for DGX-related backlog.
  - `santiago-dev/workspace/crew-manifests/dgx-readiness-crew-manifest.yaml`  
    - Crew roles and assignments for DGX readiness expedition.
  - `santiago-dev/workspace/cargo-manifests/dgx-readiness-preparation.feature`  
    - Readiness expedition feature specification.
  - `santiago-dev/workspace/cargo-manifests/dgx-infrastructure-setup.feature`  
    - Infrastructure setup for DGX.
  - `santiago-dev/workspace/cargo-manifests/dgx-deployment-commissioning.feature`  
    - Commissioning DGX deployments.
  - `santiago-dev/workspace/feature-dgx-*/*_report.md` & `*_results.json`  
    - Reports/results of specific DGX experiments.

- **Expeditions/Docs**:
  - `expeditions/exp_041/provisioning/provision_dgx.sh`  
    - Script for DGX provisioning in an expedition context.
  - `_archive/development/expeditions/EXPEDITION-dgx-readiness-preparation.md`  
    - Archived description of DGX readiness expedition.
  - `docs/vision/building-on-DGX/small_llms_for_dgx.md`  
    - Analysis of using small LLMs on DGX.
  - `docs/vision/building-on-DGX/dgx_spark_nusy_report.md`  
    - Report on DGX + Spark + NuSy integration.

### 3.2 Autonomous Workflow Execution, Multi-Agent, Orchestration, Memory

- **Features & Expeditions**:
  - `features/multi-agent-framework.feature`  
    - High-level feature spec for multi-agent frameworks.
  - `features/multi-agent-concurrency-testing.feature`  
    - Concurrency, coordination, and safety for multi-agent execution.
  - `santiago-pm/expeditions/autonomous-multi-agent-swarm/autonomous-multi-agent-swarm.md`  
    - Design & hypotheses for an autonomous multi-agent development swarm.
  - Memory architecture:
    - `research-logs/memory-architecture-comprehensive-stream.md`
    - `research-logs/memory-architecture-analysis.md`

- **In-Memory Git & Runtime-Adjacent Experiments**:
  - `expeditions/exp_036/in_memory_llm_service.py`
  - `expeditions/exp_036/test_in_memory_llm_service.py`
  - `expeditions/exp_036/enhanced_shared_memory_git_service.py`
  - `expeditions/exp_036/test_enhanced_shared_memory_git_service.py`  
    - Together, these explore:
      - In-memory LLM orchestration.
      - Enhanced shared memory Git services (core piece for “in-memory Git”).

- **Kanban / Tackle / In-Memory vs File-System State**:
  - `santiago-pm/tackle/kanban/kanban_model.py`
  - `santiago-pm/tackle/kanban/kanban_service.py`
  - `santiago-pm/tackle/kanban/kanban_cli.py`
  - `kanban-boards.md` and `santiago-pm/kanban-boards.md`
  - `kanban_regenerator.py`  
    - Implement the Kanban board as a **projection over file-system artifacts**.
  - `santiago_core/services/kanban_service.py`
  - `santiago_core/run_team.py`  
    - Generate kanban markdown and integrate with agent workflows.

### 3.3 Summary: What’s Implemented vs Vision

- **Implemented / partially implemented**:
  - DGX provisioning scripts and features.
  - Crew manifests and DGX-specific expeditions in `santiago-dev/workspace/`.
  - Kanban system tightly coupled to file-system artifacts.
  - In-memory Git / shared memory experiments in `expeditions/exp_036/`.
  - Multi-agent swarm design document and some supporting code paths.

- **Still largely in “vision” space**:
  - Fully specified **always-on DGX runtime loop**.
  - Dual KG/git per Santiago (domain vs self-improvement) as an explicit, enforced architecture constraint.
  - Clear modeling of “day at sea vs night in the shipyard” as two *modes within the same system* rather than separate runtimes.

---

## 4. Answers to the Key Architecture Questions (A–C)

### 4.1 A. DGX Runtime Model

**Q1. Should the Santiago crew be constantly running on the DGX and always in self-improvement mode?**

- **Recommendation**:  
  Yes, conceptualize Santiago as **always running on the DGX**, with a continuous loop that blends domain work and self-improvement.
- **Rationale**:
  - Matches the vision: DGX as the “shipyard” that also hosts the ship itself.
  - In-memory Git + KG + Kanban are inherently “live” systems.
  - Continuous operation maximizes learning from real work and experiments.
  - Operational complexity of stopping/starting the crew is higher than modulating focus via Kanban and priorities.

**Q2. Or should there be explicit “day at sea vs night in the shipyard” modes?**

- **Recommendation**:  
  Keep the **day/night metaphor** for human understanding, but implement them as **two prioritized work lanes within a single always-on system**, not as two completely separate runtime modes.

- **Concretely**:
  - **At Sea (External Work Lane)**:
    - Kanban lanes & tags: `type=domain`, `type=customer`.
    - The same DGX runtime; agents process domain features & expeditions.
  - **In Shipyard (Self-Work Lane)**:
    - Kanban lanes & tags: `type=self-improvement`, `type=meta`, `type=runtime`.
    - Agents work on Santiago-core, tools, observability, ethics, safety.

- **How to reflect in docs**:
  - In the “Runtime Architecture on DGX” section, explicitly:
    - Describe DGX as **always-on** host.
    - Describe **two classes of work** (domain vs self-improvement) rather than hard runtime mode switches.
    - Use the day/shipyard metaphor to explain how the Kanban board partitions and schedules work.

### 4.2 B. Knowledge Graphs & In-Memory Git per Santiago vs Shared

**Q3. For each Santiago-domain expert, do they each run their own in-memory Git and self-improvement KG/git?**

- **Recommendation**:
  - **Yes**, each Santiago-domain expert:
    - Has its own **in-memory Git workspace** for domain artifacts (code, tests, docs).
    - Has its own **domain KG** (knowledge of that specific domain).
    - Has access to a **shared self-improvement toolkit** (implemented as tackle modules and shared meta-KG patterns) but maintains:
      - A **local self-improvement KG/git** with:
        - What it has learned about its own performance.
        - Local experiments/hypotheses.
  - The self-improvement capability is implemented as a **shared pattern/service** (e.g., `tackle` capabilities and shared schemas), but each instance owns its **local data and history**.

**Q4. Does Santiago-core effectively have two KGs/Gits?**

- **Recommendation**:
  - **Yes**, Santiago-core should be modeled as having at least **two distinct but related knowledge spaces**:
    - **Domain KG/Git**:
      - Operational domain knowledge and artifacts used during “at sea” work.
      - E.g., PM-domain graph, healthcare-domain graph, etc.
    - **Self-Improvement KG/Git**:
      - Patterns, tools, experiments, and refactors about **Santiago itself**.
      - Includes:
        - Memory architecture experiments.
        - Agent role improvements.
        - Observability & safety patterns.
  - There can also be a **team-level shared KG/Git**:
    - Aggregates cross-Santiago learnings.
    - Feeds into templates, default behaviors, and shared tackle modules.

**Q5. Alternative model: centralized self-improvement KG vs per-Santiago**

- **Recommendation**:
  - Use a **hybrid**:
    - **Per-Santiago dual KGs/Gits** for:
      - Local autonomy.
      - Easier reasoning about “what this Santiago knows & remembers.”
    - **Shared meta-KG/Git** for:
      - Patterns and tools that all Santiagos can reuse.
      - This lives in the factory / tackle layer.
  - Avoid a single monolithic centralized self-improvement KG for everything:
    - Harder to reason about provenance and responsibility.
    - Bottleneck for experimentation and evolution.
    - Violates the “small ship with its own logs” metaphor.

- **How to reflect in docs**:
  - In a **“Self-Improvement System”** section:
    - Explicitly say “Each Santiago maintains two KGs/Gits: domain and self-improvement, and also integrates with a shared factory-level meta-KG.”

### 4.3 C. New “Always-in-memory” Approach

**Q6. How should the always-in-memory approach appear as a runtime architecture section?**

- **Core idea**:
  - **DGX-hosted always-on runtime**:
    - All active workspaces live in **in-memory Git**.
    - All knowledge lives in **active graphs**.
    - The Kanban board reads from and writes to these via file-system artifacts.
  - The system operates as a closed-loop:

    1. **Perception & Intake**:
       - Agents ingest new information (files, feedback, telemetry).
       - Update domain and self-improvement KGs.
    2. **Planning**:
       - PM + Architect + Ethicist consult Kanban and KGs.
       - Select tasks mixing domain and self-improvement work.
    3. **Execution**:
       - Dev/QA/DevOps agents work in in-memory Git.
       - Use BDD/TDD suites and CI pipelines.
    4. **Evaluation & Learning**:
       - Results logged as new artifacts and KG updates.
       - Self-improvement KG records patterns, successes, failures.
       - Ethicist reviews impact.

- **Interaction of In-Memory Git + Kanban + KG**:

  - **In-memory Git**:
    - Live workspace.
    - Branches for experiments; merges gated by tests and ethics.
  - **Kanban**:
    - Single source of **work state**:
      - Items are pointers to files/paths or KG nodes.
      - Column/state transitions reflect execution status.
  - **Knowledge Graphs**:
    - Single source of **semantic context**:
      - For tasks (why we’re doing them).
      - For artifacts (what they represent).
      - For history (how changes relate to past experiments).

- **CI/CD, BDD, TDD, Safety/Ethics in the loop**:

  - **BDD/TDD**:
    - Feature files and tests describe behaviors and constraints.
    - Run continuously against in-memory branches.
  - **CI/CD**:
    - Pipelines triggered on Git events in memory.
    - Can promote snapshots out to persistent repos / deployment targets.
  - **Safety/Ethics**:
    - Ethicist agent is wired into:
      - Kanban prioritization.
      - CI/CD decision gates (e.g., require ethical review of certain changes).
      - Rollback decisions when behavior deviates from ethical constraints.

---

## 5. Proposed Updated Architecture Doc (TARGET_ARCHITECTURE.md)

Below is a **proposed replacement / companion doc** for the target architecture, capturing the new DGX runtime model and self-improvement system. This is written as if it were the content of `docs/TARGET_ARCHITECTURE.md`.

### 5.1 Title & Overview

**Title:** Target Architecture – Santiago as a Self-Improving NuSy Crew on DGX  

**Overview:**  
Santiago is a multi-agent NuSy system that behaves like a seasoned software team sailing an ocean of knowledge. It runs continuously on DGX hardware, using in-memory Git and knowledge graphs as its primary runtime substrate, and Kanban as the single source of truth for work.

### 5.2 Core Concepts

- **Santiago-core (NuSy Brain)**:
  - Implements the 4-layer NuSy model:
    - Raw narratives → knowledge graphs → logic → workflows.
  - Maintains fast graph-based memory for:
    - Domain knowledge.
    - Self-improvement knowledge.
  - Integrates tightly with in-memory Git workspaces.

- **Agents / Crew**:
  - Architect, PM, Developers, QA, DevOps, Ethicist, Domain Experts.
  - Each agent:
    - Is a configured instance of the NuSy framework.
    - Has access to domain and self-improvement KGs and Git workspaces.
    - Interacts via tools, messages, and shared artifacts.

- **DGX Runtime Substrate**:
  - The DGX machine hosts:
    - In-memory Git workspaces per Santiago (domain + self).
    - Agent processes and LLM backends.
    - Shared message bus (e.g., Redis).
    - Observability stack.

### 5.3 Runtime Architecture on DGX

**5.3.1 Always-On Loop**

- Santiago runs continuously on DGX.
- All active work lives in:
  - **In-memory Git**: for code/docs/tests.
  - **Knowledge Graphs**: for semantic relationships and reasoning.
  - **Kanban**: for work state and coordination.

**5.3.2 Work Lanes: At Sea vs In Shipyard**

- **Domain Work (At Sea)**:
  - Tasks tagged `type=domain` / `type=customer`.
  - Focus:
    - Ingest domain knowledge.
    - Validate with BDD scenarios.
    - Expose capabilities as MCP tools/APIs.
- **Self-Improvement Work (Shipyard)**:
  - Tasks tagged `type=self-improvement` / `type=meta` / `type=runtime`.
  - Focus:
    - Improve Santiago-core (knowledge engine, memory, orchestrator).
    - Enhance Kanban, in-memory Git, observability, and safety.
    - Upgrade specific agents (e.g., Ethicist, PM).

**Implementation Note:**  
These are **not separate runtime environments**. They are **distinct Kanban lanes and priorities** executed within the same always-on DGX runtime.

**5.3.3 Agent Collaboration & Message Bus**

- Agents communicate via:
  - Direct tool calls.
  - Shared artifacts in in-memory Git.
  - Events on a message bus (e.g., Redis channels).
- Coordination patterns:
  - PM/Architect orchestrate tasks and experiments.
  - Dev/QA/DevOps execute and validate.
  - Ethicist reviews high-impact decisions.

### 5.4 Knowledge Graph & In-Memory Git Model

**5.4.1 Per-Santiago Dual KGs/Gits**

Each Santiago-domain expert maintains:

- **Domain KG/Git**:
  - Domain-specific knowledge (e.g., PM, healthcare).
  - Domain artifacts (features, expeditions, domain services).
- **Self-Improvement KG/Git**:
  - Observations about its own performance.
  - Experiments (hypotheses, results).
  - Tools and patterns for improving itself.

These are logically distinct but may share technical infrastructure.

**5.4.2 Shared Factory-Level Meta-KG**

- A **factory meta-KG** and shared repo:
  - Holds templates, patterns, and generic self-improvement tools (e.g., memory refactoring engines).
  - All Santiagos can:
    - Read from it (to reuse patterns).
    - Contribute back (when new patterns prove robust).

### 5.5 Kanban and File-System-as-Truth

- **Kanban**:
  - Single source of truth for **work state**.
  - Boards and cards:
    - Map directly to files (features, expeditions, manifests).
    - Are regenerated from the file system (`kanban-boards.md`).
- **File-system-as-Truth**:
  - All significant artifacts are files tracked by Git.
  - The knowledge graph references these artifacts by path and metadata.

### 5.6 CI/CD, BDD, TDD, and Ethics

- **BDD/TDD**:
  - Feature files encode desired behaviors.
  - Test suites run on in-memory Git branches before merges.
- **CI/CD**:
  - Pipelines run in DGX memory:
    - Build, test, and validate on branches.
    - On success, promote to persistent repos and deployments.
- **Safety & Ethics**:
  - Ethicist agent acts as:
    - A policy-checking tool in CI pipelines.
    - A reviewer of Kanban changes and high-risk experiments.
  - Ethics constraints:
    - Must be expressible as rules / tests.
    - Are versioned and auditable in Git.

### 5.7 Observability & Telemetry

- DGX hosts metrics, logs, traces:
  - For agents, pipelines, experiments, and knowledge graph operations.
- Telemetry flows into:
  - Self-improvement KG.
  - Kanban (e.g., as new work items when anomalies are detected).

---

## 6. Proposed Updated Development Plan (REFACTOR_PLAN.md)

Below is a **proposed development/refactor plan** aligned with the target architecture, written as if it were `docs/REFACTOR_PLAN.md`.

### 6.1 Goals

- Align the current implementation with the **DGX-native always-on runtime**.
- Implement **per-Santiago dual KG/Git** model.
- Integrate **Kanban + in-memory Git + KG** into a unified runtime loop.
- Ensure **safety, ethics, and observability** are first-class citizens.

### 6.2 Phase A – DGX Runtime Baseline (1–2 weeks)

**Objectives:**

- Stand up a stable always-on Santiago runtime on DGX.
- Integrate in-memory Git service and message bus.

**Key Tasks:**

- Configure DGX-based runtime stack:
  - LLM backends.
  - Redis (or equivalent) as message bus.
  - In-memory Git service instantiation.
- Create a **“runtime bootstrap” script** that:
  - Spins up Santiago-core and core agents.
  - Attaches them to in-memory Git + KG.
- Validate basic workflows:
  - Agents can read/write artifacts in in-memory Git.
  - Kanban CLI interacts correctly with DGX-hosted workspace.

**Success Criteria:**

- Stable DGX runtime running for 24+ hours without manual intervention.
- End-to-end flow:
  - Create Kanban card → agent task execution → code + tests in in-memory Git → CI pipeline run.

### 6.3 Phase B – Dual KG/Git Per Santiago (2–3 weeks)

**Objectives:**

- Implement explicit **domain vs self-improvement KG/Git** for Santiago-core and at least one domain expert (e.g., Santiago-PM).

**Key Tasks:**

- Extend KG schemas to distinguish:
  - Domain nodes vs self-improvement nodes.
- Implement configuration for:
  - `domain_repo` and `self_repo` for each Santiago instance.
- Update agents to:
  - Write experiment outcomes to self-improvement KG/Git.
  - Tag artifacts and Kanban items as `domain` vs `self-improvement`.

**Success Criteria:**

- At least one Santiago instance (e.g., PM) actively using:
  - Separate domain and self-improvement workspaces.
- Clear graph queries and Git history demonstrating:
  - Self-improvement experiments distinct from domain work.

### 6.4 Phase C – Kanban-Driven Dual-Lane Workflow (2–3 weeks)

**Objectives:**

- Encode **At Sea** and **In Shipyard** as Kanban lanes/tags.
- Ensure agents can dynamically balance work between lanes.

**Key Tasks:**

- Update Kanban schema and CLI to:
  - Tag items by work type.
  - Support filters for `domain` vs `self-improvement` boards.
- Implement simple **priority logic**:
  - E.g., always keep X% of WIP in self-improvement.
- Integrate Ethicist checks into:
  - Kanban operations (e.g., blocking unethical tasks).
  - CI/CD pipelines for high-risk changes.

**Success Criteria:**

- Kanban board clearly showing:
  - Domain and self-improvement work side by side.
- Agents can autonomously:
  - Pick tasks from both lanes.
  - Ensure self-improvement is not starved.

### 6.5 Phase D – Memory Architecture & Observability (3–4 weeks)

**Objectives:**

- Operationalize the **memory architecture** defined in memory-architecture analysis logs.
- Connect observability into self-improvement loops.

**Key Tasks:**

- Implement:
  - Memory snapshot service (snapshots of in-memory Git + KG).
  - Time-series analysis tools for memory evolution.
- Connect DGX observability (metrics/logs) to:
  - Self-improvement KG.
  - Kanban (as new issues or expeditions).
- Add safeguards:
  - Rollback to previous snapshots when tests/ethics fail.

**Success Criteria:**

- Automated snapshot/rollback pipeline.
- At least one improvement cycle where:
  - Telemetry → hypothesis → change → test → adoption/rollback.

### 6.6 Phase E – Consolidation & Documentation (2 weeks)

**Objectives:**

- Align all major docs with the new runtime.
- Clean up historical artifacts.

**Key Tasks:**

- Update:
  - `TARGET_ARCHITECTURE.md` (as above).
  - `REFACTOR_PLAN.md` (this plan).
  - Root `DEVELOPMENT_PLAN.md` to:
    - Reference DGX-native runtime.
    - Explain how Kanban represents both domain and self-improvement work.
- Add:
  - A “Runtime on DGX” section to the main architecture doc.
  - A “Self-Improvement System” section.
- Document:
  - How to bootstrap DGX runtime.
  - How to add a new Santiago-domain expert.

**Success Criteria:**

- All top-level architecture and plan docs:
  - Use consistent terminology.
  - Reflect always-on DGX model and dual KG/Git structure.
- Historical docs clearly marked and linked as influences.

---

## 7. Doc & Repo Cleanup Recommendations

### 7.1 Clarify Sources of Truth

- **Future Truth (Vision)**:
  - Keep `docs-arch-redux-3/GPT51/arch-vision-gpt51.md` and related vision files as the **north star**.
  - Add a small header block to those files:  
    - “Status: Vision / Future Truth – implementation may lag this document.”

- **Current Truth (Architecture & Plan)**:
  - Root-level `ARCHITECTURE.md`:
    - Either:
      - Rename to `LEGACY_ARCHITECTURE.md` and create `TARGET_ARCHITECTURE.md`, or
      - Integrate target architecture content directly with clear “Current vs Target” subsections.
  - `DEVELOPMENT_PLAN.md` and `santiago-development-master-plan.md`:
    - Cross-link them.
    - Clarify:
      - Root `DEVELOPMENT_PLAN.md` = **current Kanban-driven status + near-term priorities (DGX)**.
      - `santiago-development-master-plan.md` = **multi-phase strategic roadmap**.

### 7.2 Mark Historical / Background Files

- **Historical Strategy & Architecture**:
  - `SANTIAGO-ARCHITECTURE-SCENARIOS.md`.
  - Older strategic charts and architecture drafts in `_archive/`, `santiago-pm/strategic-charts/`, and legacy folders.
- For each, add a front-matter or header line:
  - “Status: Historical / Background – not active source of truth. Superseded by TARGET_ARCHITECTURE.md.”

- Consider creating:
  - `docs/History-And-Influences.md` summarizing:
    - Key ideas from older docs.
    - How they influenced the current architecture.

### 7.3 File & Section Renames (Optional but Recommended)

- **New docs under `docs/`**:
  - `TARGET_ARCHITECTURE.md` – content modeled on section 5 above.
  - `REFACTOR_PLAN.md` – content modeled on section 6 above.
  - `RUNTIME_ON_DGX.md` – could be a focused extraction of the runtime sections if you want a shorter operational reference.
  - `SELF_IMPROVEMENT_ARCHITECTURE.md` – or a section within `TARGET_ARCHITECTURE.md` describing dual KG/Git and self-work loops.

- **Kanban Docs**:
  - Ensure top-level comments in `kanban-boards.md` explain:
    - “This board is a **projection over file-system artifacts** and is regenerated from code and docs; do not edit card content by hand.”

### 7.4 Clean Up Redundancies

- When a concept appears in multiple places (e.g., “multi-agent swarm” described in expeditions, vision docs, and architecture docs):
  - Choose **one canonical location** (usually a doc under `docs/`).
  - In other files, replace detailed descriptions with:
    - A short summary + link (or explicit reference) to the canonical description.

---

This single document is self-contained and can be saved directly as `docs-arch-redux-3/GPT51/arch-vision-gpt51-answer.md`, while also serving as the blueprint for updating `TARGET_ARCHITECTURE.md`, `REFACTOR_PLAN.md`, and related docs in `docs/`.
