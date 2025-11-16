---
id: pm-artifact-cargo-manifest-TEMPLATE-YYYYMMDD
type: cargo-manifest
status: draft
created_at: {{CREATED_AT}}
updated_at: {{UPDATED_AT}}
assignees: []
labels:
  - type:feature
  - component:product
  - nautical:cargo-manifest
epic: {{EPIC_OR_PROJECT}}
domain: product-management
owners: ["santiago-pm"]
stakeholders: []
knowledge_scope: lake
skill_level: journeyman
artifact_kinds: ["feature-specification"]
related_artifacts: []
---

# 🧭 Cargo Manifest — {{FEATURE_TITLE}}
*Feature Specification (Nautical Theme)*

> **Purpose:** A Cargo Manifest describes the “payload” of a new capability the NuSy crew intends to deliver — including hypotheses, behaviors, risks, and expected value.  
> This artifact is read by: Santiago-PM, Santiago-Architect, Developers, QA, and Ethicist.

---

## 1. Summary (The Cargo at a Glance)

**Feature Title:** {{FEATURE_TITLE}}  
**Epic:** {{EPIC_OR_PROJECT}}  
**Primary Owner:** {{PRIMARY_OWNER}}  
**Crew Roles Involved:** {{ROLES}}  
**Motivation (Why Now):**  
{{SHORT_RATIONALE}}

**Expected Impact:**  
- {{IMPACT_1}}  
- {{IMPACT_2}}  
- {{IMPACT_3}}  

---

## 2. Problem Statement (Waters to Navigate)

Describe the user pain, workflow issue, technical blocker, or team limitation that this feature resolves.

**Current Condition:**  
{{CURRENT_STATE}}

**Why This Matters:**  
{{WHY_IT_MATTERS}}

**Success if Delivered:**  
{{SUCCESS_CRITERIA}}

---

## 3. Hypotheses & Signals (Cargo Labels)

Document the hypotheses that justify this feature. These guide experiments, measurements, and iterative improvement.

**Hypothesis 1:**  
{{HYPOTHESIS_1}}  
- **Signals to measure:** {{SIGNALS_1}}  
- **Risks if wrong:** {{RISKS_1}}

**Hypothesis 2:**  
{{HYPOTHESIS_2}}  
- **Signals:** {{SIGNALS_2}}  
- **Risks:** {{RISKS_2}}

---

## 4. Behavioral Requirements (How the Crew Should Operate)

Describe required behavior in terms of user actions, system responses, or agent interactions.

### BDD Scenarios  
(List at least 3 high-value scenarios)