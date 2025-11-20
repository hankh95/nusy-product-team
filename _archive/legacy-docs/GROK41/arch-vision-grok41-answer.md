# Santiago/NuSy Architecture Evolution: DGX Runtime and Self-Improvement Model

**Date:** November 20, 2025  
**Author:** Senior Architect (Grok-4-0709)  
**Version:** v1.0  
**Status:** Proposal  
**Purpose:** This document consolidates the vision analysis, current state, and recommendations for evolving the Santiago architecture toward an always-on, DGX-native runtime with integrated self-improvement. It proposes updates to core docs and plans.

## 1. Vision Summary (DGX + Runtime + Agents)

The vision, primarily drawn from `arch-vision-gpt51.md` and supporting documents like `Old man and the sea.md`, `Santiago-Trains-Manolin-v2.md`, `New man and the sea - a new arch plan ideas.md`, `santiago-component-architecture.md`, `nusy-components-analysis-v2.md`, and `docs/vision/README-START-HERE.md`, emphasizes Santiago as a self-building, neurosymbolic AI system inspired by the fisherman metaphor—building and repairing the boat (itself) while sailing (operating).

Key points:
- **Santiago-Core as NuSy Brain**: A core engine with a 4-layer knowledge model (raw sources → structured knowledge → computable logic → executable workflows). It uses fast graph-based memory for quick recall and reasoning, with in-memory Git/file-system-as-truth for managing artifacts, experiments, and state. This enables dynamic knowledge processing and adaptation.
- **Multi-Agent Crew**: A collaborative team of specialized agents (e.g., Architect for design, PM for planning, Dev for implementation, QA for validation, DevOps for operations, Ethicist for moral guidance, and Domain Experts for specific knowledge areas). Agents operate as a "crew on the boat," coordinating via shared memory and message buses, with ethical oversight built-in.
- **Role of the DGX**: The DGX is the high-performance hardware foundation (Soma), hosting the always-running Noesis platform. The vision leans toward a continuous loop where the team is always active on the DGX, blending domain work with self-improvement. There's ambiguity between an "always-on" model (constant evolution) and distinct modes ("at sea" for operations vs. "shipyard" for upgrades), but the emphasis is on seamless integration to maximize learning from experiments.
- **In-Memory Git & Knowledge Graphs**: Central to runtime—used for domain knowledge (e.g., product management expertise), self-improvement (e.g., learning new tools), and operational artifacts (e.g., BDD/TDD tests, CI/CD pipelines). This supports rapid experimentation, with graphs enabling neurosymbolic reasoning and Git providing versioned, in-memory workspaces for agents.

Overall, the vision aims for a self-sustaining ecosystem where Santiago autonomously builds domain experts, improves itself through data-driven experiments, and runs continuously on DGX hardware.

## 2. Current Architecture & Plan Summary

The current architecture (from `docs/ARCHITECTURE.md`) describes Santiago as a neurosymbolic AI factory for building domain-specific agents, using a factory pattern with phases (e.g., proxy agents to real agents). It emphasizes nautical theming (e.g., CatchFish for ingestion, FishNet for validation, Navigator for orchestration) and a hybrid file-system/knowledge-graph approach. Work is organized via Kanban boards (master and agent-specific), with expeditions for experiments and features in Gherkin files. Agents collaborate in shared workspaces, but there's no explicit always-on DGX runtime—focus is on local/dev environments with future DGX integration mentioned vaguely.

The development plan (from `docs/santiago-development-master-plan.md` or `docs/DEVELOPMENT_PLAN.md`) outlines phased implementation: Phase 0 (proxies), Phase 1 (MVP agents), Phase 2 (self-improvement), etc. It prioritizes Kanban integration, multi-agent concurrency, and basic DGX provisioning, but lacks detail on continuous runtime or self-improvement loops. DGX is treated as future hardware for scaling, not an always-active component. Conflicts: If both plans exist, the master plan focuses on milestones while DEVELOPMENT_PLAN.md emphasizes lean iterations, but neither fully addresses in-memory persistence or blended work/self-improvement modes.

## 3. DGX-Related Work in the Repo (Today)

- DGX provisioning and automation: `features/dgx-provisioning-automation.feature` (Gherkin spec for automated setup), `santiago-dev/workspace/crew-manifests/dgx-readiness-crew-manifest.yaml` (crew assignments for readiness), and `dgx_readiness_prioritization.py` (script for prioritizing DGX tasks).
- Monitoring and observability: `features/dgx-monitoring-observability.feature` (feature for metrics and logging on DGX), with partial implementation in `santiago_core/services/` (e.g., monitoring stubs).
- Storage and procurement: `features/dgx-storage-expansion-procurement.feature` (spec for expanding DGX storage).
- Autonomous workflow and multi-agent: `features/autonomous-workflow-execution.feature` and `features/multi-agent-framework.feature` (specs for agent coordination), with code in `santiago_core/agents/` (agent classes) and `expeditions/exp_036/` (workflow orchestration prototypes).
- Memory architecture (related to runtime): `research-logs/memory-architecture-analysis.md` and `research-logs/memory-architecture-comprehensive-stream.md` (analysis docs), with partial in-memory Git implementations in `expeditions/exp_036/enhanced_shared_memory_git_service.py` and `expeditions/exp_036/in_memory_llm_service.py`.
- Kanban and orchestration: `santiago-pm/tackle/kanban/` (CLI and models for work tracking), integrated with expeditions like `expeditions/exp_041/` (memory evolution).

Most DGX work is in planning/spec stages (features/expeditions), with some code prototypes (e.g., in-memory services) but no full always-on runtime implementation yet.

## 4. Answers to the Key Architecture Questions (A–C)

### A. DGX Runtime Model
1. **Recommendation: Yes, the Santiago crew should be constantly running on the DGX in an always-on self-improvement mode.** This aligns with the vision's emphasis on continuous evolution (building the boat while sailing), enabling seamless blending of domain work and self-improvement via data from experiments. Tradeoffs: Higher resource use (mitigated by DGX power) vs. simpler management (no mode-switching overhead). Dual modes add complexity and risk of "downtime" during switches. Reflect in docs as a new "Always-On DGX Runtime" section emphasizing loop-based operation.

2. **Explicit modes are not recommended**—they contradict the vision's fluid, adaptive nature. Instead, use prioritization in Kanban to dynamically allocate between work types.

### B. Knowledge Graphs & In-Memory Git per Santiago vs Shared
3. **Recommendation: Each Santiago-domain expert should run its own in-memory Git (as its "brain" for runtime state) and maintain a self-improvement KG/git.** This is a shared tool/capability (via `tackle` modules) that all Santiagos inherit, ensuring consistency while allowing specialization.

4. **Yes, Santiago-core should have two KGs/Gits**: One for running domain knowledge (operational expertise) and one for self-improvement (meta-learning and tools). This dual model supports the vision's layered knowledge while enabling isolated evolution.

5. **Alternative models are inferior**—a centralized self-improvement KG would create bottlenecks; the dual per-instance approach better fits autonomous, distributed agents.

### C. New “Always-in-memory” Approach
6. **Description**: The system runs in a continuous loop on DGX, with agents selecting from a unified Kanban backlog mixing domain and self-improvement tasks. In-memory Git holds active workspaces (artifacts, code), KG manages knowledge (domain + meta), and Kanban drives prioritization based on experiment data (e.g., success metrics). CI/CD runs in-memory for rapid testing, BDD/TDD validates changes, and ethics (via Ethicist agent) gates all actions. Safety is ensured through snapshotting (to persistent storage) and rollback via Git.

## 5. Proposed Updated Architecture Doc (TARGET_ARCHITECTURE.md)

# Target Santiago/NuSy Architecture

## Overview
Santiago is a self-improving neurosymbolic AI system running continuously on DGX hardware, with a multi-agent crew collaborating in shared in-memory workspaces.

## Runtime Architecture on DGX
- **Always-On Model**: The system operates in a continuous loop, blending domain work and self-improvement. Agents dynamically prioritize via Kanban, using experiment data for decisions.
- **Components**:
  - **In-Memory Git**: Per-agent workspaces for artifacts; shared for collaboration.
  - **Knowledge Graphs**: Dual per Santiago—domain KG for operations, self-improvement KG for evolution.
  - **Message Bus**: Redis for inter-agent coordination.
- **Workflow**: Agents select tasks, execute in-memory, validate via BDD/TDD, commit to shared Git, and learn via KG updates.

## Self-Improvement System
- **Dual KG/Git Model**: Each agent maintains separate graphs for domain expertise and meta-learning.
- **Learning Loop**: Observational pairing, experiment recording, and lean hypothesis testing feed self-improvement.

## Agents and Crew
- Core roles: PM, Architect, Dev, QA, DevOps, Ethicist, Domain Experts—all with ethical frameworks.

## Integration with CI/CD and Safety
- In-memory CI/CD for rapid cycles; ethics agent reviews all changes.

## 6. Proposed Updated Development Plan (REFACTOR_PLAN.md)

# Santiago Refactor and Development Plan

## Phase 1: DGX Foundation (2 weeks)
- Implement always-on DGX runtime loop.
- Integrate in-memory Git with existing agents.

## Phase 2: Dual KG/Git Implementation (3 weeks)
- Add self-improvement KG/git to Santiago-core.
- Update all agents to use dual model.

## Phase 3: Continuous Improvement Loop (4 weeks)
- Enhance Kanban for blended prioritization.
- Add experiment-driven learning (BDD/TDD integration).

## Phase 4: Full Deployment (2 weeks)
- Test on DGX; rollout to production.

## 7. Doc & Repo Cleanup Recommendations
- Mark older files like `SANTIAGO-ARCHITECTURE-SCENARIOS.md` as historical and move to `docs/history/`.
- Consolidate scattered ideas into a new "History & Influences" section in `TARGET_ARCHITECTURE.md`.
- Rename: `docs/ARCHITECTURE.md` to `docs/LEGACY_ARCHITECTURE.md`; create `docs/TARGET_ARCHITECTURE.md` and `docs/REFACTOR_PLAN.md` as proposed above.
- Archive redundant expeditions (e.g., pre-DGX ones) to `_archive/`.
