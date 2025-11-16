# Fast Path to Success — DGX + NuSy Multi-Agent Rollout

This checklist tells Hank (Captain) and Copilot agents exactly what to do to bring the new Santiago/Manolin system online, including what can run in parallel while the DGX Spark (Manolin cluster) is on order.

## Phase 0 — Kickoff & Procurement (Week 0)

1. **Confirm Budget & Specs**
   - Validate DGX Spark configuration from `ocean-research/dgx_spark_nusy_report.md` (8× H100, 1.5 TB system RAM, 30 TB NVMe).
   - Capture vendor quote + lead times in `knowledge/shared/ships-log/YYYY-MM-DD-manolin-procurement.md`.
2. **Place Order**
   - Issue PO referencing `nusy_manolin_procurement_checklist.md` steps (power, cooling, rack space).
   - Assign Hank as accountable owner; note ETA and tracking info inside ships log.
3. **Prep Facility**
   - Schedule electrical + HVAC checks per procurement checklist; document status in `knowledge/domains/platform/site-readiness.md`.

## Phase 1 — Parallel Software Work While DGX Ships (Weeks 0–6)

1. **Shared Knowledge Foundations**
   - Create repo-level `knowledge/` tree exactly as outlined in `FOLDER_LAYOUT_PROPOSAL.md`.
   - Seed `knowledge/shared/working-agreements.md`, `.../bdd-practices.md`, `.../team-roster-and-capabilities.ttl` using scaffold templates.
   - Automate ships log + roster edits via CLI helper (`nusy_pm_core/cli.py`).
2. **MCP Agent Scaffolds**
   - Use `scaffolds/mcp-manifest-template.json` to draft manifests for Santiago-PM (Master/Sea) and Santiago-Ethicist (Journeyman/Lake).
   - Implement lightweight Typer/FastAPI services at `santiago_core/agents/<role>/service/main.py` exposing shared-memory tools.
   - Register endpoints in roster TTL and commit fake-team mode instructions referencing `ocean-research/fake_team_steps_for_hank_and_copilot.md`.
3. **NuSy Orchestrator Refactor (Local Mode)**
   - Introduce MCP registry + shared memory utilities inside `src/nusy_pm_core/services/`.
   - Add REST/MCP endpoints for session start, roster fetch, ships-log append; back these with the knowledge folder.
   - Provide VS Code prompt pack describing how to start orchestrator + two MCP agents locally.
4. **Testing & Concurrency Harness**
   - Convert `nusy_manolin_multi_agent_test_plans.md` scenarios into `features/concurrency/*.feature` + pytest async tests.
   - Run tests with mocked LLM (OpenAI/Azure) to validate orchestration logic before GPUs arrive.
5. **Infrastructure-as-Code Prep**
   - Promote scripts from `ocean-research/nusy_manolin_provisioning_automation.md` into `infrastructure/manolin/`.
   - Draft runbooks for provisioning, monitoring, rollback (`runbooks/manolin-cluster.md`).
   - Create Terraform/Ansible stubs for DGX host config (networking, users, storage).

## Phase 2 — DGX Arrival & Base Install (Week 6+)

1. **Hardware Acceptance**
   - Inspect shipment, run NVIDIA diagnostics, record serials + burn-in results in `knowledge/shared/ships-log/YYYY-MM-DD-dgx-arrival.md`.
2. **Base OS & Drivers**
   - Execute `infrastructure/manolin/provision_dgx_spark_base.sh` and `install_docker_and_nvidia_container_runtime.sh`.
   - Install monitoring agents (DCGM, Prometheus node exporter) per runbook.
3. **Model Runtime**
   - Deploy vLLM + Mistral-7B (or target foundation model) via `download_mistral_7b_instruct.sh` and container compose files.
   - Smoke-test inference latency; log metrics in `knowledge/domains/platform/perf-baselines.md`.
4. **NuSy Stack Deployment**
   - Containerize orchestrator + MCP agents; push to registry; deploy with `docker stack deploy` or systemd services.
   - Use roster TTL to point endpoints at DGX hostnames; update `knowledge/shared/tools-and-mcp-capabilities.md`.
5. **End-to-End Validation**
   - Re-run concurrency BDD suite against DGX inference backend.
   - Run first official evolution cycle (PM proposal → Ethicist review → Developer tasks) and log results.

## Phase 3 — Fast Iteration After Cutover

1. **Daily Rituals**
   - Require every merge to append a ships-log entry and ensure roster skill/scope changes are documented.
   - Keep `knowledge/shared/evolution-cycles/` current; Ethicist signs each cycle before execution.
2. **Scaling the Team**
   - Bring additional MCP agents online (Architect, QA, Platform, Hank interface) using manifest/roster scaffolds.
   - Automate roster validation (script compares TTL vs. manifest metadata).
3. **Observability & Guardrails**
   - Enable structured logging + telemetry dashboards (latency, queue depth, ethics reviews).
   - Expand concurrency tests to match `nusy_manolin_multi_agent_test_plans.md` stretch scenarios.

## Prompt Pack for Hank / Copilot

When instructing AI teammates, include:

- **Context Reminder:** “Repo root `nusy-product-team`; planning outputs live under `ocean-arch-redux/arch-redux-<model_name>-plan/`; shared knowledge folder is canonical truth.”
- **Role Target:** Specify which MCP agent or scaffold they are helping (e.g., “Help Santiago-PM expose read/write tools for working agreements”).
- **Hardware Mode:** Clarify `runtime_mode=fake-team` vs. `runtime_mode=dgx-manolin` so services select proper inference backend.
- **Logging Requirement:** “Every change must append to `knowledge/shared/ships-log/<today>.md` and update roster TTL if capabilities change.”
- **Ethics Hook:** “Before enabling new capabilities, request Santiago-Ethicist review and document outcome in `knowledge/domains/ethics/evolution-reviews.md`.”

Follow this doc sequentially to minimize idle time: start software foundations immediately, then slot DGX tasks as soon as hardware is inbound.
