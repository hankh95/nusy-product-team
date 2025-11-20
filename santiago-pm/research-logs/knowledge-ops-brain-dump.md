---
title: "KnowledgeOps Brain Dump – Knowledge as Code & CI/CD"
author: "Hank Head"
date: "2025-11-20"
status: "draft"
tags: ["knowledge-ops", "knowledge-as-code", "santiago-core", "nusy-prototype", "memory-architecture"]
---

# KnowledgeOps Brain Dump – Applying CI/CD to Knowledge

> Working notes on how to treat domain knowledge like code: ingest → validate → version → deploy to KG.

## 1. Motivation

- Why “knowledge as code” matters.
- Lessons from the neurosymbolic clinical prototype (NuSy prototype).

## 2. Current State (Today)

- How we ingest and store knowledge now:
  - CatchFish / knowledge loaders.
  - `knowledge/`, `santiago-pm/research-logs/`, `cargo-manifests/`, etc.
- How we deploy to the knowledge graph today (KGStore, SantiagoKnowledgeGraph).

## 3. Desired KnowledgeOps Pipeline

- Ingest → Validate → Version → Deploy:
  - What each stage means for knowledge (not code).
  - What tooling exists vs what’s missing.

## 4. Git vs KG Versioning

- Pros/cons of:
  - Git as authoritative store for knowledge artifacts.
  - KG-level versioning and snapshots.
- Initial position: Git is primary source of truth; KG is runtime projection.

## 5. Ownership & Responsibilities

- Likely home: **Santiago-Core** (shared KnowledgeOps capabilities).
- How Santiago-PM and other domains plug into it.

## 6. Open Questions & Next Experiments

- What do we need to test to feel confident?
- What would an EXP for KnowledgeOps look like (EXP-0xx)?
- How do we measure success (safety, reversibility, correctness, speed)?


