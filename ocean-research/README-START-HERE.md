# 🚨 START HERE — Santiago Architecture Review

**If you're an AI model conducting an architecture review, READ THIS FIRST.**

---

## Step 1: Read the Architecture Pattern Document

📘 **[00-ARCHITECTURE-PATTERN.md](00-ARCHITECTURE-PATTERN.md)** ← Click here first

This document explains the critical architectural insight that defines the entire system:

> **Santiago is NOT a team of AI agents.**  
> **Santiago is a SELF-BOOTSTRAPPING FACTORY that generates domain-specific Santiagos on demand.**

**Do NOT proceed without reading this document.**

---

## Step 2: Read the Prompt

📋 **[../architecture-redux-prompt-v3.md](../architecture-redux-prompt-v3.md)**

Follow the instructions in the prompt to produce your architecture plan.

---

## Step 3: Study the Evidence

### 🎣 The Fishing Process

**[../santiago-pm/strategic-charts/Old man and the sea.md](../santiago-pm/strategic-charts/Old man and the sea.md)**

This is the literal 10-step process the factory executes for each Santiago catch:

1. Vision (what does this Santiago do?)
2. Raw Materials (collect sources)
3. **Catchfish (extract knowledge, 30-60m)**
4. Indexing
5. Ontology Loading
6. KG Building
7. **Fishnet (generate BDD tests)**
8. **Navigator (validate until quality threshold)**
9. Deployment
10. Learning

### 🧪 The Clinical Prototype Evidence

**[../nusy_prototype/](../nusy_prototype/)**

Key findings:
- **30-60 minutes** per guideline conversion
- **3 validation cycles** to reach quality threshold (23 clinical scenarios)
- Real-time in-memory query after conversion

**Architectural Implication:** This workflow IS the factory. Industrialize it.

### 🏗️ Development Patterns

**[../santiago-pm/expeditions/](../santiago-pm/expeditions/)** — Hypothesis-driven experiments  
**[../santiago-pm/tackle/](../santiago-pm/tackle/)** — Modular implementation units  
**[../santiago-pm/voyage-trials/](../santiago-pm/voyage-trials/)** — BDD test scenarios

**Key Insight:** These folders teach the fake team HOW to build the factory.

### 🖥️ DGX Deployment Specs

**[building-on-DGX/dgx_spark_nusy_report.md](building-on-DGX/dgx_spark_nusy_report.md)**

- DGX Spark: 128GB unified memory
- 4TB internal NVMe + 8-16TB external NVMe RAID
- Shared Mistral-7B-Instruct via vLLM/TensorRT-LLM
- 10+ concurrent Santiagos

### 👥 Fake Team Strategy

**[fake_team_pack/](fake_team_pack/)**

- Phase 0 of EVERY Santiago deployment
- Thin MCP wrappers to external APIs (OpenAI, Claude, Copilot)
- Fake team BUILDS the factory
- Real Santiagos progressively REPLACE fake team

---

## Step 4: Avoid Common Mistakes

### ❌ Mistake 1: "Build Santiago-PM first"
**Correct:** Build fake team (hours) → fake team builds factory (weeks) → factory catches real Santiago-PM

### ❌ Mistake 2: "Manually author domain knowledge"
**Correct:** Catchfish extracts it from sources in 30-60m (optimization target: <15m)

### ❌ Mistake 3: "Fake team is a fallback"
**Correct:** Fake team is Phase 0, always. It's the bootstrapping mechanism.

### ❌ Mistake 4: "Focus on MCP infrastructure"
**Correct:** Focus on Catchfish (30-60m extraction), Fishnet (BDD generation), Navigator (validation loops)

### ❌ Mistake 5: "Deploy all Santiagos at once"
**Correct:** Progressive replacement via A/B testing experiments (≥90% parity threshold)

---

## Step 5: Produce Your Deliverables

Follow the prompt to create:

```
ocean-arch-redux/arch-redux-<model-name>-v3-plan/
├── ARCHITECTURE_PLAN.md
├── MIGRATION_STEPS.md
├── FOLDER_LAYOUT_PROPOSAL.md
├── RELEVANCE_MAP.md
└── ASSUMPTIONS_AND_RISKS.md
```

**Critical Requirements:**

- Reference `00-ARCHITECTURE-PATTERN.md` and explain factory pattern
- Reference "Old Man and the Sea" 10-step fishing process
- Reference clinical prototype (30-60m, 3 cycles)
- Explain 4 phases (Fake Team → Factory → First Catch → Self-Sustaining)
- Include "Ethics & Concurrency Gating" section
- Include "References Cited" section

---

## Validation Checklist

Before submitting, verify:

- [ ] I read **00-ARCHITECTURE-PATTERN.md** BEFORE scanning code
- [ ] My plan starts with **Phase 0: Fake Team**
- [ ] My plan explains **fake team builds factory**
- [ ] My plan includes **factory catches real Santiagos** (30-60m, 3-5 cycles)
- [ ] My plan includes **A/B testing** before replacement
- [ ] My plan includes **progressive replacement** (one role at a time)
- [ ] I referenced **"Old Man and the Sea"**
- [ ] I referenced **clinical prototype**
- [ ] I explained **santiago-pm/ folder structure** teaching patterns
- [ ] My milestones reflect **4 phases**

---

## Need Help?

If you're confused, re-read:

1. **[00-ARCHITECTURE-PATTERN.md](00-ARCHITECTURE-PATTERN.md)** — The critical insight
2. **[../santiago-pm/strategic-charts/Old man and the sea.md](../santiago-pm/strategic-charts/Old man and the sea.md)** — The fishing process
3. Clinical prototype findings (30-60m, 3 cycles)

**Remember:** You're building a self-bootstrapping factory, not a team of agents.

Good luck! 🎣
