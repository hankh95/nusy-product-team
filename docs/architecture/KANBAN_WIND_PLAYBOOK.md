# Kanban Wind Creation Playbook – Unblocking Flow for Santiago / Noesis

This playbook captures a first draft of patterns for “creating wind” on the Kanban board – i.e., how to restore flow whenever work gets stuck between states. It’s meant for Santiago‑Architect, Santiago‑PM, and all crew members (human or agent).

It is backed by:

- `self_improvement/santiago-pm/cargo-manifests/kanban-wind-creation-board-unblocking.md`
- The architecture and runtime described in `docs/architecture/arch-vision-merged-plan.md`

Use this as a set of heuristics, not hard rules – and update it as we learn.

---

## 1. Journey Re‑framing Wind (Zoom Out to the Voyage)

**When to use:**  
- Many cards in `In Progress` / `Review`, few or none in `Ready`, and the team seems busy but not finishing.  

**Actions:**

1. Re‑articulate the **journey**:
   - Main objective (e.g. “Deliver complete, logic‑filled framed files for BMJ topic X on DGX in 4 weeks”).
   - Customer and their $/risk.
   - Time/budget constraints.
   - Success measures (BDD pass %, extraction completeness, cycle time, etc.).
2. Ensure there is a **voyage / epic manifest** that captures this in one place.
3. Add / refresh 1–2 small “clarify journey” cards:
   - e.g. “Validate VOY‑001 YAML and acceptance criteria for success”.

**Goal:** Make sure everyone can answer “What journey are we on? What counts as a win?” before pulling more work.

---

## 2. Hypothesis‑Driven Experiment Wind (Turn Stuck into Small Bets)

**When to use:**  
- Cards are blocked on uncertainty: “we don’t know which approach is better”, “we don’t know if this LLM or mapping will work”.

**Actions:**

1. Extract the underlying **hypothesis**:
   - e.g. “Running BMJ pipeline on DGX in memory will reduce cycle time by N%”,  
     or “We can map BMJ content directly to their graph spec without going through 4‑layer tagging”.
2. Create **tiny, time‑boxed experiment cards**:
   - Cycle 1:
     - Instrument current behavior (metrics, logs, snapshots).
     - Run the existing pipeline or behavior on a small slice (one topic, one scenario).
   - Cycle 2:
     - Apply a focused change (refactor, prompt tweak, new mapping).
     - Re‑run and compare metrics.
3. Encode a **decision rule** in the card/manifest:
   - “If improvement ≥ X on metric Y, promote approach A; otherwise, revert or try B.”

**Goal:** Replace indecision with explicit experiments and measurable outcomes.

---

## 3. Knowledge‑Loading Wind (Reduce “We Don’t Know” Latency)

**When to use:**  
- Work is blocked by repeated “What is X?” questions about code, domain, or architecture.

**Actions:**

1. Create **enabling cards** to load the project into a brain:
   - “Load BMJ pipeline code + topics + specs into NusY‑core or local LLM.”
   - “Build Q&A prompts for BMJ‑Doctor project (pipeline, domains, metrics).”
2. Define a simple **reload cadence**:
   - e.g. “Reload full BMJ project into NusY‑core/LLM every N cycles or at voyage checkpoints.”
3. Encourage agents/humans to:
   - Ask the loaded brain before spelunking across the repo.
   - Capture useful Q&A in research logs or knowledge graphs.

**Goal:** Turn basic understanding questions from multi‑hour detours into fast queries.

---

## 4. Slicing & WIP‑Limit Wind (Many Started, Few Finished)

**When to use:**  
- Too many large cards in `In Progress`, few or none reaching `Done`.

**Actions:**

1. Add **“slice this card”** tasks:
   - Identify the smallest vertical slices that deliver a learning or user‑visible outcome.
   - Split one large card into 2–4 smaller, independent cards with clear acceptance criteria.
2. Apply a temporary **no‑new‑starts rule**:
   - No one pulls new cards into `In Progress` until a minimum number of slices reach `Done`.
3. Optionally, lower WIP limits on columns that are overloaded.

**Goal:** Encourage small batches and visible progress, reducing the risk of “forever in progress” work.

---

## 5. Prioritizer Wind (Too Many Options, No Clear Next)

**When to use:**  
- The board or manifests have many possible improvements, but no one is sure which a few to start next.

**Actions:**

1. Create a **“run prioritizer”** card:
   - Gather 10–20 plausible improvements from manifests, logs, and team ideas.
   - Estimate:
     - Time to value (TTV),
     - Impact on journey goals (customer outcome, risk reduction, learning).
2. Sort and select:
   - Promote only the top 3–5 into `Ready`.
   - Move the rest back to Backlog with notes.
3. Make prioritization transparent:
   - Capture rationale in a short note for future revisits.

**Goal:** Turn “we could do anything” into a focused, small set of high‑value bets.

---

## 6. Decision & Escalation Wind (Unmade Decisions Block Flow)

**When to use:**  
- A card is blocked solely because a decision hasn’t been made (e.g., “which LLM?”, “what’s acceptable FHIR depth?”, “when to stop an experiment?”).

**Actions:**

1. Create explicit **decision cards**:
   - Title the decision.
   - List options, constraints, and a recommendation if available.
   - Assign to Captain/Ethicist/Architect as appropriate.
2. Encode **escalation rules**:
   - When should Architect/PM decide locally?
   - When must the Captain or Ethicist review?
3. After decision, **update downstream cards**:
   - Re‑prioritize or split work based on the chosen path.

**Goal:** Make decisions visible and time‑boxed, instead of silently blocking multiple cards.

---

## 7. How to Use This Playbook as a Team

- When the board feels stuck or “windless”:
  - Ask: **Which pattern fits this situation best?**
  - Create one or more small cards that enact the chosen pattern.
  - Keep WIP small and learning continuous.
- Over time:
  - Add concrete examples from voyages (BMJ, other domains).
  - Refine or add patterns based on what actually restores flow.

This playbook should evolve with each journey – especially as we run more DGX voyages and learn how Santiago and Noesis behave under real constraints.


