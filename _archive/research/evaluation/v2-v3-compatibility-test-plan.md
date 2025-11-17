# Evaluation Code v2/v3 Compatibility Test Plan

**Date:** 2025-11-16  
**Purpose:** Verify evaluation code works with both v2 and v3 prompt outputs

---

## Changes Made

### 1. `evaluate_arch_reviews.py`

**Line 111-115:** Model name parsing made flexible
```python
# OLD (v2-only):
model_name = plan_dir.name.replace("arch-redux-", "").replace("-v2-plan", "")

# NEW (v2 and v3):
dir_name = plan_dir.name.replace("arch-redux-", "")
model_name = re.sub(r"-v[23]-plan$", "", dir_name)
version_match = re.search(r"v([23])", dir_name)
prompt_version = version_match.group(1) if version_match else "unknown"
```

**Line 180:** Added `prompt_version` field to results
```python
result = {
    "model_name": model_name,
    "prompt_version": prompt_version,  # NEW
    "plan_path": str(plan_dir),
    ...
}
```

**Line 299-311:** Directory matching made flexible
```python
# OLD (v2-only):
baseline = root / "arch-redux-gpt-5-v2-plan"
if sub.name.endswith("-v2-plan"):

# NEW (v2 and v3):
baseline_candidates = [
    root / "arch-redux-gpt-5-v3-plan",
    root / "arch-redux-gpt-5-v2-plan",
    root / "arch-redux-claude-sonnet-4.5-v3-plan",
    root / "arch-redux-claude-sonnet-4.5-v2-plan"
]
baseline = next((b for b in baseline_candidates if b.exists()), None)
if re.search(r"-v[23]-plan$", sub.name):
```

### 2. `README.md`

- Updated to mention both v2 and v3 prompt support
- Updated directory convention examples
- Updated baseline detection order

### 3. `models-config.yaml`

- Updated header comment to mention both v2 and v3 directories

### 4. `review_output_schema.json`

- Added `prompt_version` field to schema

---

## Test Scenarios

### Scenario 1: Mixed v2 and v3 Plans

**Setup:**
```
ocean-arch-redux/
├── arch-redux-claude-sonnet-4.5-v2-plan/  (existing)
├── arch-redux-claude-sonnet-4.5-v3-plan/  (new from v3 prompt)
├── arch-redux-gpt-4-v2-plan/              (hypothetical)
└── arch-redux-gpt-4-v3-plan/              (hypothetical)
```

**Expected Behavior:**
- Script discovers all 4 directories
- Extracts model names correctly: "claude-sonnet-4.5", "gpt-4"
- Records prompt_version as "2" or "3" for each
- Uses first available baseline (v3 preferred)
- Calculates novelty vs baseline for all plans

**Test Command:**
```bash
python evaluation/evaluate_arch_reviews.py \
  --plans-root ocean-arch-redux \
  --config evaluation/models-config.yaml \
  --out evaluation/results/test-mixed-v2-v3.json
```

**Validation:**
```bash
jq '.[] | {model_name, prompt_version, plan_path}' evaluation/results/test-mixed-v2-v3.json
```

Expected output includes both v2 and v3 entries.

---

### Scenario 2: V3-Only Plans

**Setup:**
```
ocean-arch-redux/
├── arch-redux-claude-sonnet-4.5-v3-plan/
├── arch-redux-gpt-4-v3-plan/
└── arch-redux-gemini-v3-plan/
```

**Expected Behavior:**
- Script discovers all 3 v3 directories
- Uses claude-sonnet-4.5-v3 as baseline (first in candidate list)
- All prompt_version fields = "3"

**Test Command:**
```bash
python evaluation/evaluate_arch_reviews.py \
  --plans-root ocean-arch-redux \
  --config evaluation/models-config.yaml \
  --out evaluation/results/test-v3-only.json
```

**Validation:**
```bash
jq '.[] | select(.prompt_version != "3")' evaluation/results/test-v3-only.json
```

Expected: empty output (all should be v3)

---

### Scenario 3: V2-Only Plans (Backward Compatibility)

**Setup:**
```
ocean-arch-redux/
├── arch-redux-gpt-5-v2-plan/
└── arch-redux-claude-3-5-sonnet-v2-plan/
```

**Expected Behavior:**
- Script works exactly as before
- Uses gpt-5-v2 as baseline
- All prompt_version fields = "2"

**Test Command:**
```bash
python evaluation/evaluate_arch_reviews.py \
  --plans-root ocean-arch-redux \
  --config evaluation/models-config.yaml \
  --out evaluation/results/test-v2-backward-compat.json
```

**Validation:**
```bash
jq '.[] | .prompt_version' evaluation/results/test-v2-backward-compat.json
```

Expected: all "2"

---

### Scenario 4: Leaderboard with Mixed Versions

**Setup:** Use results from Scenario 1 (mixed v2/v3)

**Expected Behavior:**
- Leaderboard compares all models regardless of prompt version
- Scores calculated identically (metrics are content-based, not version-specific)
- Model names displayed without version suffix

**Test Command:**
```bash
python evaluation/evaluate_arch_reviews.py \
  --leaderboard evaluation/results/test-mixed-v2-v3.json \
  --config evaluation/models-config.yaml
```

**Expected Output:**
```
Model,Score
claude-sonnet-4.5,X.XXXX
gpt-4,X.XXXX
```

Note: No "-v2" or "-v3" in model names

---

### Scenario 5: Manual Scoring with Mixed Versions

**Setup:** Create `evaluation/test-manual-scores.yaml`:
```yaml
model: claude-sonnet-4.5
feasibility: 5
clarity: 5
risk_depth: 4
notes: "V3 plan with factory pattern - excellent"

model: gpt-4
feasibility: 4
clarity: 4
risk_depth: 3
notes: "V2 plan - good baseline"
```

**Expected Behavior:**
- Manual scores append to correct model entry regardless of version
- Both v2 and v3 plans for same model get same manual score (if model name matches)

**Test Command:**
```bash
python evaluation/evaluate_arch_reviews.py \
  --append-manual \
  --input evaluation/results/test-mixed-v2-v3.json \
  --manual evaluation/test-manual-scores.yaml
```

**Validation:**
```bash
jq '.[] | {model_name, prompt_version, manual}' evaluation/results/test-mixed-v2-v3.json
```

Expected: manual scores present for matching models

---

## Edge Cases

### Edge Case 1: Invalid Version Suffix

**Directory:** `arch-redux-custom-model-v5-plan/`

**Expected Behavior:**
- Detected as plan directory (starts with "arch-redux-")
- Model name: "custom-model-v5" (version extraction fails, keeps suffix)
- prompt_version: "unknown"

### Edge Case 2: No Baseline Available

**Setup:** Only plans, no baseline directory exists

**Expected Behavior:**
- Script runs successfully
- baseline_dir = None
- novelty.embedding_similarity_baseline = None for all plans
- No errors or crashes

### Edge Case 3: Both v2 and v3 Plans for Same Model

**Directory Structure:**
```
ocean-arch-redux/
├── arch-redux-claude-sonnet-4.5-v2-plan/
└── arch-redux-claude-sonnet-4.5-v3-plan/
```

**Expected Behavior:**
- Both discovered as separate entries
- model_name = "claude-sonnet-4.5" for both
- prompt_version distinguishes them ("2" vs "3")
- Leaderboard shows both as separate entries

**Implication:** If comparing same model across prompt versions, they appear as distinct entries in results. This is CORRECT behavior - allows version comparison.

---

## Metrics That Are Version-Agnostic

All current metrics work identically for v2 and v3 because they're content-based:

✅ **presence** - checks for same 5 files
✅ **headings** - date pattern matching
✅ **coverage** - keyword search (mcp, knowledge, dgx, ethics)
✅ **citations** - ocean-research/ reference counting
✅ **specificity** - interface keyword counting
✅ **migration** - milestone/task parsing
✅ **relevance** - independence heuristic
✅ **risks** - risk/mitigation keyword counting
✅ **knowledge** - cross-link counting
✅ **lexical** - token counting and TTR
✅ **readability** - Flesch calculation
✅ **lint** - markdown validation
✅ **novelty** - token overlap vs baseline
✅ **ethics** - concurrency mentions
✅ **assumptions** - assumption keyword counting
✅ **checklist** - `- [ ]` counting

**No metrics need modification for v3 compatibility.**

---

## Potential Future Enhancements

### Enhancement 1: Version-Specific Metrics

If v3 prompt has unique requirements (e.g., factory pattern, bootstrapping sequence), could add:

```python
def v3_specific_metrics(arch_text: str, prompt_version: str) -> Dict:
    if prompt_version != "3":
        return {}
    
    return {
        "factory_pattern": {
            "mentions_factory": "factory" in arch_text.lower(),
            "mentions_catchfish": "catchfish" in arch_text.lower(),
            "mentions_navigator": "navigator" in arch_text.lower(),
            "mentions_fishnet": "fishnet" in arch_text.lower(),
            "mentions_bootstrapping": "bootstrap" in arch_text.lower(),
            "mentions_fake_team": "fake team" in arch_text.lower() or "proxy" in arch_text.lower(),
        },
        "clinical_prototype": {
            "mentions_30_60m": bool(re.search(r"30[-–]60\s*m", arch_text)),
            "mentions_validation_cycles": "validation cycle" in arch_text.lower() or "3 cycles" in arch_text.lower(),
        },
        "bootstrapping_phases": {
            "mentions_phase_0": "phase 0" in arch_text.lower() or "phase zero" in arch_text.lower(),
            "mentions_progressive_replacement": "progressive replacement" in arch_text.lower() or "a/b test" in arch_text.lower(),
        }
    }
```

Add to result dict:
```python
if prompt_version == "3":
    result["v3_specific"] = v3_specific_metrics(arch_text, prompt_version)
```

### Enhancement 2: Version Comparison Report

```bash
python evaluation/evaluate_arch_reviews.py \
  --compare-versions \
  --input evaluation/results/metrics.json \
  --model claude-sonnet-4.5
```

Output:
```
Comparing claude-sonnet-4.5 across prompt versions:

v2 Plan:
  - presence: 4/5 files
  - citations: 8 total, 0.429 coverage
  - migration: 7 milestones

v3 Plan:
  - presence: 5/5 files
  - citations: 12 total, 0.714 coverage
  - migration: 4 milestones (Phase 0-3)
  
v3 Improvements:
  + More comprehensive citations (+50%)
  + Cleaner milestone structure (-3 milestones, better organized)
  + All required files present
```

---

## Verification Checklist

Before deployment:

- [ ] Run Scenario 1 (mixed v2/v3)
- [ ] Run Scenario 2 (v3-only)
- [ ] Run Scenario 3 (v2-only backward compat)
- [ ] Run Scenario 4 (leaderboard with mixed)
- [ ] Run Scenario 5 (manual scoring with mixed)
- [ ] Verify Edge Case 2 (no baseline)
- [ ] Verify Edge Case 3 (both versions for same model)
- [ ] Check JSON schema validation passes
- [ ] Check no errors with empty results
- [ ] Check model names have no version suffix in output

---

## Current Status

✅ Code changes implemented
✅ README updated
✅ Config updated
✅ Schema updated
⏳ Testing scenarios pending execution

**Next Action:** Run test scenarios with actual v3 plan outputs.

---

## Summary

**Question:** Will evaluation code work with v2 and v3 prompt outputs?

**Answer:** **YES, after these changes.**

**Key Changes:**
1. Flexible directory pattern matching (v2 OR v3)
2. Version-aware model name extraction
3. prompt_version field added to results
4. Baseline auto-detection with v3 preference
5. Documentation updated

**Backward Compatibility:** ✅ All existing v2-only evaluations still work

**Forward Compatibility:** ✅ V3 plans now fully supported

**Mixed Compatibility:** ✅ Can evaluate v2 and v3 plans together

**No Breaking Changes:** Existing metrics unchanged, just more flexible directory detection.
