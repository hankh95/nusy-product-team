#!/usr/bin/env python3
"""
Helper script to create the DGX/BMJ Kanban board and seed it with initial cards.

Board ID: voy-001-bmj-maiden

This script uses the SantiagoKanbanService MCP wrapper, so it should be run from
the repository root with the appropriate virtual environment activated:

    python tools/create_dgx_bmj_board.py
"""

import asyncio
from pathlib import Path

from santiago_core.services.kanban_service import SantiagoKanbanService


BOARD_ID = "voy-001-bmj-maiden"

CARDS = [
    {
        "item_id": "voy-001-bmj-voyage-yaml",
        "title": "Define VOY-001 BMJ voyage YAML",
        "item_type": "feature",
        "repository_path": "docs-arch-redux-3/noesis_clipper_go_package/voyages/voyage-VOY-001-BMJ-Maiden.yaml",
        "description": "Align VOY-001 YAML with VOYAGE_MODEL_SPECIFICATION: main objective, constraints, goals/measures, motivation, team roles, connections.",
        "priority": "high",
    },
    {
        "item_id": "voy-001-bmj-metrics-model",
        "title": "Define BMJ value & metrics model for VOY-001",
        "item_type": "research_log",
        "repository_path": "docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT.md",
        "description": "Specify metrics (BDD %, coverage, cycle time, etc.) and thresholds that map to BMJ value and voyage checkpoints.",
        "priority": "high",
    },
    {
        "item_id": "dgx-readiness-checklist-alignment",
        "title": "Align DGX readiness checklist with actual repo state",
        "item_type": "task",
        "repository_path": "docs/architecture/DGX_READINESS_CHECKLIST.md",
        "description": "Cross-check each checklist item against the repo and update paths/expectations; log missing items as follow-up cards.",
        "priority": "medium",
    },
    {
        "item_id": "dgx-scripts-stub-verification",
        "title": "Verify DGX pipeline script stubs (local)",
        "item_type": "task",
        "repository_path": "docs-arch-redux-3/noesis_clipper_go_package/dgx",
        "description": "Confirm run_bmj_pipeline.sh, run_santiago_bmj.sh, and compare_engines.sh exist and run in stub mode; capture gaps.",
        "priority": "medium",
    },
    {
        "item_id": "exp-dgx-llm-selection-cycle1",
        "title": "DGX LLM Selection – Cycle 1 Landscape & Shortlist",
        "item_type": "expedition",
        "repository_path": "docs/architecture/expeditions/EXP-DGX-LLM-SELECTION.md",
        "description": "Execute Cycle 1 of EXP-DGX-LLM-SELECTION: identify and shortlist DGX-capable reasoning/worker models.",
        "priority": "high",
    },
    {
        "item_id": "exp-dgx-knowledge-loading-map-surfaces",
        "title": "DGX Knowledge Loading – Map BMJ Project Surfaces",
        "item_type": "expedition",
        "repository_path": "docs/architecture/expeditions/EXP-DGX-KNOWLEDGE-LOADING-CADENCE.md",
        "description": "Cycle 1 of knowledge loading cadence: map BMJ artifacts to NusY-Core vs LLM vs both.",
        "priority": "high",
    },
    {
        "item_id": "bmj-project-brain-loader-design",
        "title": "Design BMJ Project Brain Loader",
        "item_type": "feature",
        "repository_path": "docs/architecture/expeditions/EXP-DGX-KNOWLEDGE-LOADING-CADENCE.md",
        "description": "Design a loader script/service that populates NusY-Core and/or a DGX LLM with BMJ project knowledge.",
        "priority": "medium",
    },
    {
        "item_id": "voy-001-mvp-cycle1-baseline",
        "title": "VOY-001 MVP – Cycle 1 Instrumentation & Baseline",
        "item_type": "expedition",
        "repository_path": "docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT.md",
        "description": "Implement Cycle A of the MVP experiment: wire metrics into DGX scripts and run a baseline topic (locally if needed).",
        "priority": "high",
    },
    {
        "item_id": "voy-001-mvp-cycle2-refactor-design",
        "title": "VOY-001 MVP – Cycle 2 Refactor & Re-run (Design Only)",
        "item_type": "expedition",
        "repository_path": "docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT.md",
        "description": "Draft improvement ideas and prioritization approach for Cycle B of the MVP experiment.",
        "priority": "medium",
    },
    {
        "item_id": "exp-dgx-direct-graph-mapping-understand",
        "title": "Direct Graph Mapping – Understand BMJ Spec & 4L Mapping",
        "item_type": "expedition",
        "repository_path": "docs/architecture/expeditions/EXP-DGX-DIRECT-GRAPH-MAPPING.md",
        "description": "Cycle 1 of direct graph mapping expedition: understand BMJ graph spec and current 4L mapping.",
        "priority": "low",
    },
    {
        "item_id": "ai-book-ingestion-bmj-design",
        "title": "AI Book Ingestion – Initial Design for BMJ Integration",
        "item_type": "feature",
        "repository_path": "domain/domain-features/specs/features/ai-book-ingestion.feature",
        "description": "Extend AI book ingestion feature with scenarios connecting ingested texts to BMJ graphs/pipelines.",
        "priority": "low",
    },
    {
        "item_id": "dgx-vllm-service-setup",
        "title": "DGX vLLM Service Config & Client Stub",
        "item_type": "feature",
        "repository_path": "configs/dgx/vllm_mistral7b.json",
        "description": "Define DGX vLLM config and VLLMClient wrapper for multi-agent inference.",
        "priority": "medium",
    },
]


async def main():
    workspace = Path(__file__).resolve().parents[1]
    service = SantiagoKanbanService(workspace)

    # Create board (idempotent: if it exists, keep going)
    create_res = await service.handle_tool_call(
        "kanban_create_board",
        {
            "board_id": BOARD_ID,
            "name": "VOY-001 BMJ DGX Readiness",
            "description": "DGX/BMJ readiness and VOY-001 BMJ Maiden Voyage work",
        },
    )
    if create_res.error:
        print(f"⚠️ Board creation error (may already exist): {create_res.error}")
    else:
        print(f"✅ Created board: {create_res.result}")

    # List boards for visibility
    list_res = await service.handle_tool_call("kanban_list_boards", {})
    if not list_res.error:
        print("Available boards:", list_res.result)

    # Add cards (skip if an item_id already exists on the board)
    for card in CARDS:
        params = {
            "board_id": BOARD_ID,
            "item_id": card["item_id"],
            "title": card["title"],
            "item_type": card["item_type"],
            "repository_path": card["repository_path"],
            "description": card["description"],
            "priority": card["priority"],
        }
        res = await service.handle_tool_call("kanban_add_card", params)
        if res.error:
            print(f"⚠️ Could not add card {card['item_id']}: {res.error}")
        else:
            print(f"✅ Added/updated card {card['item_id']}")


if __name__ == "__main__":
    asyncio.run(main())


