# Option 1 – BMJ Delivery Accelerator Voyage

**Objective:**  
Use Santiago and the DGX to **improve the existing BMJ pipeline codebase** (which you and agents wrote) so that it can deliver a complete, logic-filled, FHIR-capable semantic graph for BMJ topics **much faster**.

Initial win:  
> Deliver all framed files to spec for one BMJ topic, with logic gaps and missing authored content filled, in **4 weeks**.

## 1. Goals

1. Run the BMJ repo **inside Santiago** on the DGX.
2. Replace all external AI API calls with DGX-local LLM calls.
3. Fill semantic gaps:
   - missing logic
   - missing time and sequence modeling
   - missing content that should have been authored
4. Produce:
   - L0/L1/L2 frames
   - logic-complete L3
   - FHIR Clinical Reasoning–ready artifacts (or close approximations)
5. Reduce topic cycle time as much as possible while preserving quality.
6. Provide BMJ with clear evidence that:
   - their original semantic-only graph could not answer 10–15% of questions
   - the improved pipeline now can.

## 2. Weekly Cadence (21 hours / 3 days)

Typically: **Mon–Wed** (or equivalent).

### Day Pattern

- **Start of day**
  - Pick 1–3 BMJ topics or pipeline pain points.
  - Review any learnings from Option 2 (Santiago-Doctor-BMJ experiments).

- **Core work**
  - Run the pipeline on DGX with:
    ```bash
    ./dgx/run_bmj_pipeline.sh <topic_id>
    ```
  - Inspect metrics, failures, and gaps.
  - Use Santiago to:
    - propose refactors
    - generate better extraction prompts/logic
    - implement missing content generation where appropriate

- **End of day**
  - Capture:
    - time per topic
    - BDD pass rate
    - remaining logic gaps
  - Log improvements and TODOs in a voyage/ships-log markdown.

## 3. Scope of Changes

- You **may** refactor BMJ repo scripts, as you are the original author.
- You **will**:
  - introduce Santiago-friendly wrappers
  - centralise LLM calls through DGX
  - add instrumentation (logging, metrics)
  - codify framed-file generation

## 4. DGX Usage (Option 1)

Use:

```bash
./dgx/run_bmj_pipeline.sh <topic_id>
```

This should:

1. Start or connect to the local DGX LLM service.
2. Load the BMJ repo pipeline configuration.
3. Run the full extraction → graph → framed-file pipeline for the given topic.
4. Run BDD tests against the produced artifacts (if available).
5. Emit:
   - framed files
   - logs
   - metrics
   - a topic-specific snapshot for comparison.
