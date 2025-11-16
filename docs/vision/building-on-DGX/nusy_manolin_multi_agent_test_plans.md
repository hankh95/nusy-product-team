# Role-Specific Test Plans for Multi-Agent Concurrency  
*NuSy Manolin Cluster – Santiago-Based Team*

This document outlines **test plans** to validate multi-agent concurrency for the NuSy Product Team:

- Product Manager (PM)
- Architect – NuSy
- Architect – Systems/Platform
- Developer
- QA Specialist
- UX Researcher/Designer
- Platform/Deployment Engineer

All agents share a **Santiago (Mistral-7B-Instruct)** core and operate concurrently via the NuSy Orchestrator.

---

## 1. Global Concurrency Objectives

We want to ensure:

1. Multiple agents can **operate concurrently** without:
   - Dropping requests
   - Excessive latency
   - Cross-contamination of sessions
2. Each role:
   - Receives the correct **context and tools**
   - Produces **role-appropriate outputs**
3. The orchestrator:
   - Correctly routes requests
   - Enforces isolation between sessions
   - Logs activity per role and session

---

## 2. Cross-Cutting Test Scenarios

### 2.1 Load & Concurrency Baseline

**Goal:** Verify that the system can handle concurrent tasks from multiple agents.

- **Scenario:**
  - 10 agents (mix of PM, Dev, QA, Architect, UX, Platform) concurrently request:
    - Small reasoning tasks (e.g., summarization)
    - Medium tasks (e.g., BDD generation, code review)
  - Measure:
    - Average latency
    - Error rate
    - GPU utilization

- **Checks:**
  - No agent receives another agent’s prompt or results.
  - No request is silently dropped.
  - Latency stays within defined SLO (e.g., P95 < 4–6 seconds).

---

### 2.2 Session Isolation

**Goal:** Ensure that concurrent sessions remain logically separated.

- **Scenario:**
  - Start 3 concurrent sessions:
    - Session A: PM working on “Stroke Guideline MCP”
    - Session B: Developer working on “NuSy Orchestrator Feature”
    - Session C: QA working on “BDD Coverage Audit”
  - Each session runs 10+ turns of conversation and tool calls.

- **Checks:**
  - Context from Session A never appears in B or C.
  - Orchestrator tags logs with session IDs.
  - Vector DB / KG queries are scoped properly (if filters are used).

---

### 2.3 Tool Invocation Race Conditions

**Goal:** Validate that simultaneous tool calls are handled safely.

- **Scenario:**
  - PM, Developer, and Architect agents all:
    - Query Git forge
    - Update product board
    - Query KG
  - Some calls overlap in time, some cause write operations (e.g., create issue, create feature).

- **Checks:**
  - No duplicate or conflicting writes beyond what’s expected.
  - Appropriate locking or idempotency in adapters.
  - Clear error handling if a resource is temporarily locked.

---

## 3. Role-Specific Concurrency Tests

### 3.1 Product Manager (PM)

**Role Focus:** Hypothesis shaping, feature creation, BDD definition, prioritization.

#### PM-1: Parallel Feature Creation

- **Given** 3 active products (A, B, C)
- **When** the PM agent is asked (in three concurrent sessions) to:
  - Define features and BDD for each product
- **Then**:
  - Each session’s backlog is created independently
  - No cross-leakage of feature names/requirements
  - All BDD files are written to the correct product directories

#### PM-2: Race on Priority Changes

- **Given**:
  - A shared product board
- **When**:
  - Two PM sessions concurrently reprioritize the same set of features
- **Then**:
  - Conflicts are either:
    - Resolved deterministically, or
    - Clearly detected and reported
  - The final board state is consistent

---

### 3.2 Architect – NuSy

**Role Focus:** Knowledge graph design, reasoning patterns, NuSy ontology evolution.

#### AR-NUSY-1: Concurrent KG Extensions

- **Given**:
  - A live NuSy KG
- **When**:
  - Architect – NuSy runs two parallel tasks:
    - Adding new classes and properties for a domain
    - Adding new reasoning patterns (e.g., 4-layer mappings)
- **Then**:
  - No partial or corrupted KG states
  - Changes are versioned (e.g., graph snapshots)
  - Conflicts (same class/URI) are clearly surfaced

#### AR-NUSY-2: Query Load Under Development

- **Scenario:**
  - Multiple agents issue KG queries while Architect – NuSy runs a schema migration script.
- **Checks:**
  - Queries either:
    - See the old schema, or
    - See the new schema,
    - But do not see half-migrated states (unless explicitly allowed).
  - Orchestrator can retry or queue queries if migration is in progress.

---

### 3.3 Architect – Systems/Platform

**Role Focus:** Overall system architecture, infra, scaling strategies.

#### AR-SYS-1: Simultaneous Infra Proposals

- **Scenario:**
  - Architect – Systems and PM both request new infra plans in parallel.
- **Checks:**
  - Each plan is produced in the correct session context.
  - Shared references (e.g., cluster names, storage plans) are consistent.

#### AR-SYS-2: Infrastructure Plan vs Live System

- **Scenario:**
  - Architect – Systems generates plan updates while Platform/Deployment Engineer is applying changes.
- **Checks:**
  - No confusion between “proposed state” vs “actual state”.
  - Logs clearly separate them.

---

### 3.4 Developer

**Role Focus:** Implementing features, writing code/tests.

#### DEV-1: Concurrent Feature Implementation

- **Scenario:**
  - Two Developer sessions work on:
    - Feature X (Orchestrator CLI)
    - Feature Y (API endpoint)
  - Both generate code changes and tests.

- **Checks:**
  - Generated code is directed to correct files/modules.
  - Tests are co-located with the right features.
  - No accidental overwrites due to concurrency.

#### DEV-2: Code Review & Refactor Under Load

- **Scenario:**
  - Developer agent is asked to refactor several modules concurrently (e.g., via multiple sessions).
- **Checks:**
  - File locks or branch isolation strategy is respected.
  - CI catches conflicts or failing tests.

---

### 3.5 QA Specialist

**Role Focus:** Extending tests, validating behavior, stress/concurrency tests.

#### QA-1: Concurrent Test Extension

- **Scenario:**
  - QA agent is asked to:
    - Extend unit tests for Feature A
    - Extend BDD for Feature B
    - Run regression tests on the last release
    all at once.

- **Checks:**
  - Test files are consistently formatted and located.
  - No collisions in test names.
  - Test runs are labeled by scenario and session.

#### QA-2: Load & Soak Testing

- **Scenario:**
  - QA agent orchestrates a soak test with:
    - N agents each sending traffic to the NuSy Orchestrator.
- **Checks:**
  - Concurrency metrics recorded (latency, throughput).
  - Resource usage does not exceed safe thresholds.
  - System recovers cleanly after the load test.

---

### 3.6 UX Researcher/Designer

**Role Focus:** User flows, story maps, research synthesis.

#### UX-1: Parallel Journey Mapping

- **Scenario:**
  - Two UX sessions:
    - One mapping onboarding flow.
    - One mapping “author new guideline” flow.
- **Checks:**
  - Journeys stored under correct product/feature.
  - No mixing of flow elements between journeys.

#### UX-2: Concurrent Insight Synthesis

- **Scenario:**
  - UX agent processes transcripts from multiple sources in parallel.
- **Checks:**
  - Summaries and insights are labeled with correct source IDs.
  - No cross-leakage of confidential context.

---

### 3.7 Platform/Deployment Engineer

**Role Focus:** Deploying services, managing runtime environments.

#### PLAT-1: Deployment Under Feature Workload

- **Scenario:**
  - Platform agent deploys a new version of the NuSy Orchestrator while:
    - Dev and PM agents are actively working with the previous version.
- **Checks:**
  - Zero or minimal downtime.
  - Sessions are either gracefully drained or reconnected.
  - Logs clearly indicate version boundaries.

#### PLAT-2: Rollback Under Load

- **Scenario:**
  - Rollback triggered during concurrent agent activity.
- **Checks:**
  - No corruption of data stores.
  - Clients (agents) are re-routed correctly to the rolled-back version.

---

## 4. Test Implementation Strategy

- Represent many of these scenarios as:
  - **BDD features** (e.g., `features/concurrency/pm.feature`, `features/concurrency/dev.feature`)
  - **Integration tests** (Python/pytest) invoking orchestrator endpoints.
- Include:
  - Load profiles (e.g., Locust, k6, custom async clients).
  - Observability:
    - Correlate logs to sessions, roles, and features.
- Define SLOs:
  - Acceptable latency & throughput.
  - Acceptable error rates.

---

## 5. Success Criteria

The Manolin Cluster passes concurrency testing when:

1. **Correctness:** No agent sees another agent’s private context unless explicitly designed.  
2. **Stability:** Under typical concurrent load, error rates remain low and recoverable.  
3. **Performance:** Latency and throughput remain within agreed SLOs.  
4. **Clarity:** Logs and metrics clearly show what’s happening per role and per session.  
5. **Resilience:** Deployments, rollbacks, and migrations can occur while agents are active, without corrupting state.

This document is meant to be **iterated** as NuSy evolves. New roles, tools, and behaviors should come with corresponding concurrency test additions.
