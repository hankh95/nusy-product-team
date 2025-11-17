# External PM Knowledge Extraction

**Version:** 1.0.0  
**Date:** 2025-01-16  
**Task:** Task 18 - External PM Thought Leader Knowledge Extraction  
**Sources:** 5 external websites (Jeff Patton, Jeff Gothelf, Nielsen Norman Group, SAFe PO/PM)  
**Focus:** Lean UX crossover with expedition-based learning, UX research competency for PMs  

---

## Executive Summary

This document extracts product management and UX research knowledge from leading thought leaders and frameworks, specifically focusing on **how to run expeditions to learn when we don't know something**—the crossover between Lean UX practices and Santiago's expedition-based learning methodology.

**Key Finding:** Lean UX, continuous discovery, user story mapping, and ResearchOps all share the expedition mindset: **hypothesis-driven exploration with rapid validation cycles to reduce uncertainty.**

While the `santiago-ux` role will have primary responsibility for UX research expeditions, **a competent PM must understand and participate in** discovery rituals, hypothesis formation, validation planning, and stakeholder synthesis.

---

## Category 1: Lean UX Principles & Continuous Discovery (Jeff Gothelf)

### Concept 1.1: Outcome-Based Planning vs Output-Based Planning

**Source:** Jeff Gothelf books ("Lean UX", "Sense and Respond", "Who Does What By How Much?")

**Core Principle:**  
Shift from measuring "features shipped" to "outcomes achieved." PMs run **learning expeditions** to validate which features actually drive customer behavior changes.

**Connection to Expeditions:**
- **Hypothesis:** "We believe [feature X] will cause [behavior Y]"
- **Experiment Design:** How to test cheapest/fastest? (prototype, interview, A/B test)
- **Validation Criteria:** What evidence proves/disproves hypothesis?
- **Iterate or Pivot:** Based on evidence, continue or change course

**PM Behavior Extracted:**
- `formulate_outcome_hypothesis`: Convert business goals → testable hypotheses
- `design_validation_experiment`: Choose cheapest test that yields valid evidence
- `interpret_experiment_results`: Analyze data → decide continue/pivot/kill

**Santiago Parallel:**  
Navigator's validation loops (Steps 6-8) are **discovery expeditions**. Each cycle tests: "Does this BDD spec capture real PM behavior?" The 3-5 iteration cycle mirrors Lean UX's "Build → Measure → Learn" loop.

---

### Concept 1.2: Lean UX Canvas - Lightweight Expedition Planning

**Source:** Jeff Gothelf's Lean UX framework

**Core Principle:**  
Don't write 50-page specs before learning. Use a **1-page canvas** to plan discovery:
1. **Problem Statement:** What customer pain are we addressing?
2. **Outcomes:** What behavior change indicates success?
3. **Users:** Who are we learning from?
4. **Benefits:** What value do they get?
5. **Solution Ideas:** Hypotheses to test
6. **Assumptions:** Riskiest unknowns (test these first)
7. **Hypothesis:** Testable statement
8. **Experiment:** How we'll test it
9. **Success Criteria:** Evidence threshold

**Connection to Expeditions:**  
This IS an expedition plan. Santiago-PM should adopt similar lightweight planning for each Navigator run:
- **Voyage Goal:** Extract PM domain knowledge
- **Catch Target:** 20-30 behaviors per fishing expedition
- **Validation Criteria:** ≥95% BDD pass rate, ≥90% KG completeness
- **Riskiest Assumption:** "Catchfish can extract accurate behaviors from unstructured docs"
- **Test Method:** Run Fishnet → validate BDD files → measure quality

**PM Behavior Extracted:**
- `create_lean_ux_canvas`: 1-page expedition plan for discovery work
- `prioritize_risky_assumptions`: Test highest-uncertainty hypotheses first
- `define_success_evidence`: Set quantitative thresholds before testing

---

### Concept 1.3: Continuous Discovery Habits (Weekly Customer Contact)

**Source:** Jeff Gothelf workshops on "product discovery"

**Core Principle:**  
Discovery is not a phase—it's a **continuous practice**. Effective PMs maintain **weekly customer touchpoints** to:
- Test small hypotheses rapidly
- Catch invalid assumptions before committing engineering time
- Build shared understanding across team

**Connection to Expeditions:**  
Santiago-PM Factory should institutionalize **continuous catching**:
- **Weekly Fishing:** Run 1-2 small Navigator expeditions per week (~30-60 min each)
- **Rapid Validation:** Each catch tested within 24-48 hours (BDD validation)
- **Shared Knowledge:** Every catch updates the Knowledge Graph (team learning artifact)

**PM Behavior Extracted:**
- `schedule_discovery_cadence`: Establish regular expedition rhythm (weekly/biweekly)
- `timebox_discovery_work`: Cap expeditions at 30-60 min to maintain velocity
- `share_discovery_insights`: Update shared artifacts (KG) after each expedition

**Santiago Implementation Note:**  
DGX Manolin Cluster enables **concurrent expeditions**. Multiple Santiagos can run discovery work in parallel → 10x throughput vs sequential.

---

## Category 2: UX Research Methods & ResearchOps (Nielsen Norman Group)

### Concept 2.1: Measuring UX and ROI - Quantifying Expedition Success

**Source:** Nielsen Norman Group course "Measuring UX and ROI"

**Core Principle:**  
UX research expeditions must produce **quantifiable evidence**, not just opinions. Metrics categories:
1. **Behavioral:** Task completion rate, time-on-task, error rate
2. **Attitudinal:** NPS, satisfaction scores, perceived effort
3. **Business:** Conversion rate, revenue impact, support ticket reduction

**Connection to Expeditions:**  
Santiago-PM already does this for **code quality metrics**:
- BDD pass rate ≥95% (behavioral: does code work?)
- Test coverage ≥95% (behavioral: is code tested?)
- KG completeness ≥90% (attitudinal: is knowledge captured?)

**PM Should Extend to UX Expeditions:**
- **User Research ROI:** "This 4-hour interview study prevented 80 hours of wasted dev time"
- **Prototype Testing ROI:** "5 users validated design → saved 2-week rework cycle"
- **Expedition Cost/Benefit:** Track time invested in discovery vs. rework avoided

**PM Behavior Extracted:**
- `calculate_research_roi`: Quantify discovery investment vs. waste prevented
- `track_expedition_velocity`: Measure catch rate (behaviors extracted per hour)
- `benchmark_quality_metrics`: Compare expedition outcomes (KG completeness, BDD pass rate)

---

### Concept 2.2: ResearchOps - Scaling Discovery Across Teams

**Source:** Nielsen Norman Group course "ResearchOps: Scaling User Research"

**Core Principle:**  
As organizations grow, **research operations** become critical:
- **Participant Recruitment:** Maintain pool of research subjects (users, SMEs)
- **Tool Infrastructure:** Shared tools for expeditions (prototyping, testing, synthesis)
- **Knowledge Management:** Centralized repository of insights (avoid re-learning)
- **Training & Enablement:** Upskill teams to run their own lightweight expeditions

**Connection to Expeditions:**  
Santiago-PM Factory IS a ResearchOps system for PM domain knowledge:
- **"Participants":** Documents, experts, existing codebases (sources of PM knowledge)
- **"Tool Infrastructure":** Catchfish, Fishnet, Navigator (expedition automation)
- **"Knowledge Management":** Knowledge Graph in RDF format (centralized PM ontology)
- **"Training":** santiago-pm/ folder structure teaches teams how to fish

**PM Behavior Extracted:**
- `establish_research_infrastructure`: Set up tools, participant pools, synthesis templates
- `centralize_discovery_insights`: One source of truth for team learnings (KG)
- `train_team_on_discovery`: Enable team members to run lightweight expeditions

**Santiago Factory Insight:**  
The Factory's **self-bootstrapping** nature means ResearchOps scales automatically:
- Fake Santiagos → build infrastructure
- Real Santiagos → use infrastructure to catch new domains
- Each domain caught → adds to organizational knowledge

---

### Concept 2.3: Stakeholder Engagement vs. Management

**Source:** Nielsen Norman Group course "Successful Stakeholder Relationships"

**Core Principle:**  
**Engagement ≠ Management.** Stakeholder management is directive ("I manage you"). Stakeholder engagement is collaborative ("We co-create").

For UX research expeditions:
- **Engage early:** Involve stakeholders in hypothesis formation (what should we learn?)
- **Co-synthesize:** Review findings together (what did we learn? what does it mean?)
- **Collaborative roadmapping:** Stakeholders help prioritize next expeditions

**Connection to Expeditions:**  
Santiago-PM treats **humans as stakeholders** in the bootstrapping process:
- Human PM provides vision documents → co-creates expedition scope
- Human reviews catches (BDD files, KG updates) → validates quality
- Human decides next expedition → collaborative prioritization

**PM Behavior Extracted:**
- `engage_stakeholders_in_discovery`: Involve stakeholders in expedition planning
- `facilitate_synthesis_sessions`: Lead collaborative review of expedition findings
- `co_prioritize_next_expeditions`: Stakeholders help decide what to learn next

---

## Category 3: User Story Mapping & Discovery (Jeff Patton)

### Concept 3.1: Story Maps as Shared Understanding Artifacts

**Source:** Jeff Patton's "User Story Mapping" methodology

**Core Principle:**  
User story maps are **visual conversation tools**, not just backlogs. They facilitate:
1. **Shared Understanding:** Whole team sees user journey → spots gaps
2. **Prioritization:** Identify MVP skeleton vs. walking skeleton vs. full feature set
3. **Discovery Planning:** Map reveals **knowledge gaps** (what don't we know yet?)

**Connection to Expeditions:**  
Santiago-PM could create **"Knowledge Maps"** showing PM domain coverage:
- **X-axis:** PM activities (strategy, discovery, delivery, measurement, stakeholder mgmt)
- **Y-axis:** Depth (basic → intermediate → advanced behaviors)
- **Gaps:** Areas needing more fishing expeditions

**Example PM Knowledge Map:**
```
Discovery       [████████░░] 80% coverage (16 of 20 behaviors caught)
Strategy        [██████░░░░] 60% coverage (12 of 20 behaviors caught)
Stakeholder     [████░░░░░░] 40% coverage (8 of 20 behaviors caught)  ← NEXT EXPEDITION TARGET
Measurement     [██░░░░░░░░] 20% coverage (4 of 20 behaviors caught)
```

**PM Behavior Extracted:**
- `create_knowledge_map`: Visualize domain coverage (what we know vs. gaps)
- `identify_knowledge_gaps`: Prioritize next expeditions based on coverage gaps
- `facilitate_map_walkthroughs`: Use maps to align team on current understanding

---

### Concept 3.2: Dual-Track Development (Discovery + Delivery in Parallel)

**Source:** Jeff Patton article "Dual Track Development is not Duel Track"

**Core Principle:**  
Teams should run **two parallel tracks**:
- **Discovery Track:** Expeditions to validate ideas (prototypes, experiments, research)
- **Delivery Track:** Engineering work on validated features

**Key Insight:** Discovery work stays ~1-2 sprints ahead of delivery. This prevents:
- Building the wrong thing (discovery invalidates before engineering starts)
- Discovery becoming a bottleneck (discovery runs continuously)

**Connection to Expeditions:**  
Santiago-PM's **hybrid coordination** approach IS dual-track:
- **Discovery Track:** Navigator expeditions extracting new PM behaviors (Fishnet + Catchfish)
- **Delivery Track:** GitHub agents implementing validated specs (PRs #8-11)

**Current Example (Mini Expedition):**
- **Phase 1:** Discovery work (architecture specs, GitHub issues) - 50 min
- **Phase 2:** Delivery work (agents implement code) - in progress
- **Phase 3:** Validation + integration - next

**PM Behavior Extracted:**
- `establish_dual_track_cadence`: Discovery work stays ahead of delivery
- `validate_before_engineering`: Don't code until discovery proves value
- `manage_parallel_work_streams`: Balance discovery + delivery in same sprint

---

### Concept 3.3: Outcome-Centric Thinking - Focus on Value, Not Output

**Source:** Jeff Patton website tagline "Focus on value"

**Core Principle:**  
"While finishing more work faster is valuable, none of that matters if your customers don't use and get value from your products."

For discovery expeditions:
- **Output Metric:** "We ran 10 user interviews this sprint"
- **Outcome Metric:** "We invalidated 3 risky assumptions, saving 120 hours of dev waste"

**Connection to Expeditions:**  
Santiago-PM should measure **catch quality**, not just quantity:
- ❌ Bad metric: "We caught 100 PM behaviors this month"
- ✅ Good metric: "95% of caught behaviors passed BDD validation on first try"
- ✅ Good metric: "Knowledge Graph completeness increased from 60% → 90%"

**PM Behavior Extracted:**
- `define_outcome_metrics`: Focus on impact (quality, waste avoided) not activity (volume)
- `validate_customer_value`: Ensure expeditions produce actionable insights
- `ruthlessly_deprioritize_low_value_work`: Kill expeditions that don't drive outcomes

---

## Category 4: SAFe Product Owner & Product Manager Practices

### Concept 4.1: Product Owner as "Voice of the Customer"

**Source:** SAFe Product Owner role definition

**Core Principle:**  
PO represents customer needs and ensures team backlog aligns with Solution Vision. Key responsibilities:
1. **Backlog Management:** Prioritize team-level work (stories, tasks)
2. **Customer Collaboration:** Daily interaction with end-users and stakeholders
3. **Acceptance Criteria:** Define "done" for each story
4. **Feedback Synthesis:** Gather insights from demos, testing, production metrics

**Connection to Expeditions:**  
Santiago-PO (if it existed) would:
- Maintain **catch backlog** (list of PM domains to extract)
- Define **acceptance criteria** for catches (BDD validation, KG integration)
- **Customer = Human PM:** PO ensures catches align with human PM's vision

**PM Behavior Extracted:**
- `manage_discovery_backlog`: Prioritized list of knowledge gaps to explore
- `define_catch_acceptance_criteria`: What makes a valid catch? (quality thresholds)
- `synthesize_expedition_feedback`: Aggregate insights from multiple expeditions

---

### Concept 4.2: Product Manager as Strategic Alignment Leader

**Source:** SAFe Product Manager role (note: page returned 404, but core principle well-known)

**Core Principle:**  
PM (vs PO) operates at **program/portfolio level**, aligning multiple teams around:
- **Product Vision:** Long-term outcome we're driving toward
- **Roadmap:** Sequenced expeditions to validate vision hypotheses
- **Feature Prioritization:** What capabilities to build (based on discovery evidence)
- **Business Metrics:** How we measure progress toward vision

**Connection to Expeditions:**  
Santiago-PM Factory needs **strategic PM** to:
- **Vision:** "Self-bootstrapping factory that generates domain-specific Santiagos in 30-60 min"
- **Roadmap:** Phase 0 (fake team) → Phase 1 (factory build) → Phase 2 (first catches) → Phase 3 (progressive replacement)
- **Prioritization:** Which domains to catch first? (PM domain = proof of concept)
- **Metrics:** Catchfish time (target <15 min), quality gates (≥95%/≥95%/≥90%)

**PM Behavior Extracted:**
- `articulate_product_vision`: Clear long-term outcome for expeditions
- `sequence_learning_roadmap`: Prioritize order of discovery work (riskiest first)
- `track_strategic_metrics`: Monitor progress toward vision (time, quality, coverage)

---

### Concept 4.3: Agile Team Partnership (PM + PO + UX + Eng)

**Source:** SAFe team topology (cross-functional Agile Teams)

**Core Principle:**  
PMs don't work in isolation. Effective discovery requires:
- **PM:** Strategic alignment, roadmap, business metrics
- **PO:** Backlog management, customer voice, acceptance criteria
- **UX:** Research methods, prototyping, usability validation
- **Engineering:** Technical feasibility, implementation estimates

**Connection to Expeditions:**  
Santiago Factory should eventually have **role-specific agents**:
- **Santiago-PM:** Defines expedition vision, prioritizes domains, tracks strategic metrics
- **Santiago-PO:** Manages catch backlog, defines quality gates, validates catches
- **Santiago-UX:** Designs research protocols, analyzes user data, synthesizes findings
- **Santiago-Engineer:** Implements validated features, maintains infrastructure

**Current State:**  
We're bootstrapping with **one generalist Santiago** (santiago-pm), but the vision includes role specialization.

**PM Behavior Extracted:**
- `coordinate_cross_functional_discovery`: Align PM/PO/UX/Eng on expedition goals
- `clarify_role_boundaries`: Who does what in discovery work?
- `facilitate_team_rituals`: Sprint planning, backlog refinement, retros (all involve discovery)

---

## Cross-Cutting Theme: Expedition-Based Learning Methodology

### The Lean UX → Santiago-PM Connection

**Core Insight:**  
Lean UX, continuous discovery, dual-track development, and user story mapping all embody the **expedition mindset**:

1. **Start with Uncertainty:** We don't know the right answer
2. **Form Hypothesis:** Testable guess about what's true
3. **Design Lightweight Test:** Cheapest experiment that yields valid evidence
4. **Run Expedition:** Execute test, gather data
5. **Synthesize Findings:** What did we learn? What does it mean?
6. **Decide Next Action:** Continue, pivot, or kill based on evidence
7. **Repeat Rapidly:** Short cycles (hours/days, not weeks/months)

**Santiago-PM Already Does This:**
- **Uncertainty:** What PM behaviors exist in domain?
- **Hypothesis:** "These docs contain 20-30 catchable behaviors"
- **Test Design:** Run Catchfish → generate BDD specs → validate with behave
- **Expedition:** Navigator 10-step process (30-60 min)
- **Synthesis:** Review BDD pass rate, KG completeness
- **Decision:** If ≥95% pass → integrate; if <95% → rework
- **Cadence:** Target 3-5 validation cycles per domain

**Key Learning for PMs:**  
**Discovery is expeditionary by nature.** You can't plan perfectly upfront—you must explore, validate, and adapt. Santiago-PM codifies this as a **repeatable, measurable system**.

---

## PM Behaviors Extracted (Summary)

### Discovery & Hypothesis Formation (8 behaviors)
1. `formulate_outcome_hypothesis`: Convert business goals → testable hypotheses
2. `design_validation_experiment`: Choose cheapest test that yields valid evidence
3. `prioritize_risky_assumptions`: Test highest-uncertainty hypotheses first
4. `define_success_evidence`: Set quantitative thresholds before testing
5. `create_lean_ux_canvas`: 1-page expedition plan for discovery work
6. `identify_knowledge_gaps`: Prioritize next expeditions based on coverage gaps
7. `manage_discovery_backlog`: Prioritized list of knowledge gaps to explore
8. `define_catch_acceptance_criteria`: What makes a valid catch? (quality thresholds)

### Expedition Execution & Synthesis (7 behaviors)
9. `schedule_discovery_cadence`: Establish regular expedition rhythm (weekly/biweekly)
10. `timebox_discovery_work`: Cap expeditions at 30-60 min to maintain velocity
11. `interpret_experiment_results`: Analyze data → decide continue/pivot/kill
12. `synthesize_expedition_feedback`: Aggregate insights from multiple expeditions
13. `share_discovery_insights`: Update shared artifacts (KG) after each expedition
14. `facilitate_synthesis_sessions`: Lead collaborative review of expedition findings
15. `engage_stakeholders_in_discovery`: Involve stakeholders in expedition planning

### Measurement & ROI (5 behaviors)
16. `calculate_research_roi`: Quantify discovery investment vs. waste prevented
17. `track_expedition_velocity`: Measure catch rate (behaviors extracted per hour)
18. `benchmark_quality_metrics`: Compare expedition outcomes (KG completeness, BDD pass rate)
19. `define_outcome_metrics`: Focus on impact (quality, waste avoided) not activity (volume)
20. `track_strategic_metrics`: Monitor progress toward vision (time, quality, coverage)

### Infrastructure & Enablement (5 behaviors)
21. `establish_research_infrastructure`: Set up tools, participant pools, synthesis templates
22. `centralize_discovery_insights`: One source of truth for team learnings (KG)
23. `train_team_on_discovery`: Enable team members to run lightweight expeditions
24. `establish_dual_track_cadence`: Discovery work stays ahead of delivery
25. `validate_before_engineering`: Don't code until discovery proves value

### Strategic Alignment (5 behaviors)
26. `articulate_product_vision`: Clear long-term outcome for expeditions
27. `sequence_learning_roadmap`: Prioritize order of discovery work (riskiest first)
28. `co_prioritize_next_expeditions`: Stakeholders help decide what to learn next
29. `coordinate_cross_functional_discovery`: Align PM/PO/UX/Eng on expedition goals
30. `ruthlessly_deprioritize_low_value_work`: Kill expeditions that don't drive outcomes

**Total: 30 PM behaviors related to UX research competency and expedition-based learning**

---

## Ontology Extension Recommendations

### New Classes (Layer 9: Discovery & Research)

1. **DiscoveryExpedition** (subclass of PMBehavior)
   - Properties: hasHypothesis, hasValidationMethod, hasDuration, hasSuccessCriteria

2. **LeanUXCanvas** (subclass of Artifact)
   - Properties: definesProblem, specifiesOutcomes, listsAssumptions, specifiesExperiment

3. **KnowledgeGap** (new concept)
   - Properties: priority, estimatedEffort, lastExplored, hasOwner

4. **ResearchOpsInfrastructure** (new concept)
   - Properties: hasTooling, hasParticipantPool, hasKnowledgeRepository, hasTrainingMaterial

5. **OutcomeMetric** (subclass of Metric)
   - Properties: measuresImpact, hasBaseline, hasTarget, hasActual

6. **DualTrack** (subclass of Process)
   - Properties: hasDiscoveryTrack, hasDeliveryTrack, leadsBy (duration)

### New Properties (13 properties)

1. `hasHypothesis` (domain: DiscoveryExpedition, range: string)
2. `hasValidationMethod` (domain: DiscoveryExpedition, range: string)
3. `hasSuccessCriteria` (domain: DiscoveryExpedition, range: string)
4. `calculateROI` (domain: DiscoveryExpedition, range: float)
5. `hasKnowledgeGap` (domain: PMDomain, range: KnowledgeGap)
6. `prioritizesGap` (domain: PMBehavior, range: KnowledgeGap)
7. `measuresOutcome` (domain: PMBehavior, range: OutcomeMetric)
8. `requiresInfrastructure` (domain: DiscoveryExpedition, range: ResearchOpsInfrastructure)
9. `engagesStakeholder` (domain: PMBehavior, range: Stakeholder)
10. `feedsIntoRoadmap` (domain: DiscoveryExpedition, range: Roadmap)
11. `hasDiscoveryTrack` (domain: DualTrack, range: DiscoveryExpedition)
12. `hasDeliveryTrack` (domain: DualTrack, range: EngineeringWork)
13. `leadsBy` (domain: DualTrack, range: duration) [discovery stays ahead of delivery]

---

## Santiago-UX Role Specification (Draft)

**Context:** User noted "ideally the santiago-ux will have responsibility for this for the team but a good PM should know how to do much of this work."

### Santiago-UX Primary Responsibilities

1. **Research Protocol Design**
   - Design user interviews, usability tests, surveys
   - Define participant recruiting criteria
   - Create research guides and scripts

2. **Expedition Execution**
   - Run user research sessions (interviews, testing)
   - Facilitate synthesis workshops
   - Prototype low/high-fidelity designs for validation

3. **Insight Synthesis**
   - Analyze qualitative data (interview transcripts, observations)
   - Identify patterns, themes, user needs
   - Document findings in accessible format

4. **Knowledge Repository Maintenance**
   - Maintain centralized insight repository (KG for UX domain)
   - Tag insights with relevant product areas, features
   - Enable team self-service (search past research)

5. **Team Enablement**
   - Train PMs, POs, Engineers on lightweight discovery methods
   - Provide templates, tools, best practices
   - Pair with team members on discovery work

### PM's UX Research Competency (What PM Must Know)

While santiago-ux owns execution, **PM must understand**:
- **When to run expeditions:** Recognize high-uncertainty situations requiring discovery
- **How to form hypotheses:** Translate business questions → testable statements
- **How to interpret findings:** Understand what evidence is valid/invalid
- **How to prioritize research:** Which unknowns are riskiest? Test those first
- **How to collaborate:** Effective partnership with santiago-ux (ask right questions, respect expertise)

**Analogy:** PM doesn't write code, but must understand software development enough to:
- Ask good questions
- Evaluate technical trade-offs
- Prioritize engineering work
- Recognize when estimates are off

**Same with UX research:** PM doesn't run studies, but must understand discovery enough to be an effective partner.

---

## Recommendations for Santiago-PM Development

### Immediate Actions (Next 1-2 Sprints)

1. **Extend Ontology with Layer 9: Discovery & Research**
   - Add 6 new classes (DiscoveryExpedition, LeanUXCanvas, KnowledgeGap, etc.)
   - Add 13 new properties (hasHypothesis, calculateROI, measuresOutcome, etc.)
   - Update ontology version to 1.2.0

2. **Extract 30 Discovery Behaviors into BDD Specs**
   - Use Fishnet + Navigator to catch these 30 behaviors
   - Validate with behave (target ≥95% pass rate)
   - Integrate into PM domain knowledge graph

3. **Create Lean UX Canvas Template for Navigator**
   - Add pre-expedition planning step to Navigator
   - Force explicit hypothesis, validation method, success criteria
   - Track ROI: time invested vs. rework avoided

4. **Build Knowledge Gap Tracker**
   - Visualize PM domain coverage (what we know vs. don't know)
   - Prioritize next expeditions based on gaps
   - Monitor completeness over time (target 90% → 95% → 98%)

### Strategic Initiatives (Next 3-6 Months)

1. **Develop Santiago-UX Agent**
   - Specialized in UX research methods
   - Partner with Santiago-PM on discovery work
   - Own ResearchOps infrastructure

2. **Implement Dual-Track Coordination**
   - Discovery Track: Navigator runs continuously
   - Delivery Track: GitHub agents implement validated catches
   - Discovery stays 1-2 expeditions ahead of delivery

3. **Measure Expedition ROI**
   - Track: time per expedition, quality metrics, rework avoided
   - Benchmark: compare serial vs. hybrid vs. parallel approaches
   - Optimize: target 30 min → 15 min per expedition

4. **Bootstrap Adjacent Domains**
   - Use Factory to catch: UX research, technical writing, DevOps, QA
   - Validate: Can Factory generalize beyond PM domain?
   - Scale: 10 concurrent Santiagos on DGX Manolin Cluster

---

## Completeness Assessment

**Sources Processed:** 5 of 5 (100%)
1. ✅ Jeff Gothelf (jeffgothelf.com) - Lean UX, OKRs, Sense & Respond
2. ✅ Nielsen Norman Group (nngroup.com) - UX research, ResearchOps, Measuring UX
3. ✅ Jeff Patton (jpattonassociates.com) - User story mapping, dual-track, outcome-centric
4. ✅ SAFe Product Owner (framework.scaledagile.com) - Voice of customer, backlog mgmt
5. ⚠️ SAFe Product Manager (framework.scaledagile.com) - Page returned 404, used general SAFe PM knowledge

**Knowledge Captured:**
- 30 PM behaviors related to UX research and expedition-based learning
- 4 categories: Discovery, Execution, Measurement, Infrastructure, Strategy
- 6 new ontology classes for Layer 9: Discovery & Research
- 13 new ontology properties
- Santiago-UX role specification (draft)
- Lean UX → Santiago-PM methodology crossover documented

**Completeness:** 0.90 (90%)  
**Reason for 90% vs 100%:** SAFe PM page content limited, but core principles well-established in industry.

**Next Steps:**
1. Extend ontology to v1.2.0 with Layer 9
2. Run Navigator to catch these 30 behaviors as BDD specs
3. Validate integration with existing 28 PM behaviors
4. Plan Santiago-UX agent development

---

## Appendix: Key Quotes

**Jeff Gothelf (Lean UX):**
> "We believe [X feature] will achieve [Y outcome]. We'll know we're right when we see [Z signal]."  
> → This is expedition thinking: hypothesis → test → evidence.

**Nielsen Norman Group (Measuring UX):**
> "Research is an investment. Quantify the return: time saved, errors prevented, revenue gained."  
> → Expeditions must demonstrate ROI, not just activity.

**Jeff Patton (Outcome-Centric):**
> "While finishing more work faster is valuable, none of that matters if your customers don't use and get value from your products."  
> → Catch quality > catch quantity.

**SAFe Product Owner:**
> "The PO is the 'voice of the customer,' representing the needs of end-users and the business."  
> → Santiago-PO would be voice of human PM, ensuring catches align with vision.

---

**Document Status:** COMPLETE ✅  
**Task 18 Status:** READY FOR REVIEW  
**Next Action:** Update DEVELOPMENT_PLAN.md, commit work, move to next task
