#!/usr/bin/env python3
"""Evaluate multi-model architecture review outputs.

Usage:
    python evaluation/evaluate_arch_reviews.py --plans-root ocean-arch-redux --config evaluation/models-config.yaml --out evaluation/results/metrics.json
  python evaluation/evaluate_arch_reviews.py --leaderboard evaluation/results/metrics.json
  python evaluation/evaluate_arch_reviews.py --append-manual --input evaluation/results/metrics.json --manual evaluation/manual_scores.yaml

Environment (optional):
  EMBEDDING_PROVIDER=openai|anthropic|none (placeholder)
  EMBEDDING_API_KEY=... (if similarity enabled)

This script intentionally avoids external dependencies beyond the standard library.
"""
from __future__ import annotations
import argparse
import json
import math
import os
import re
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Tuple

REQUIRED_FILES = [
    "ARCHITECTURE_PLAN.md",
    "MIGRATION_STEPS.md",
    "RELEVANCE_MAP.md",
    "ASSUMPTIONS_AND_RISKS.md",
]
OPTIONAL_FILES = ["FOLDER_LAYOUT_PROPOSAL.md"]
REFERENCE_DOCS = [
    "dgx_spark_nusy_report.md",
    "nusy_manolin_architecture.md",
    "nusy_manolin_provisioning_automation.md",
    "nusy_manolin_multi_agent_test_plans.md",
    "fake_team_feature_plan.md",
    "fake_team_steps_for_hank_and_copilot.md",
]
DATE_PATTERN = re.compile(r"20[2-3][0-9]-[0-1][0-9]-[0-3][0-9]")
TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_]+")

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def flesch_reading_ease(text: str) -> float:
    # Simple approximation: count sentences, words, syllables heuristic
    sentences = max(1, len(re.findall(r"[.!?]", text)))
    words = TOKEN_PATTERN.findall(text)
    word_count = max(1, len(words))
    syllables = sum(_approx_syllables(w) for w in words)
    # Flesch = 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)
    return round(206.835 - 1.015 * (word_count / sentences) - 84.6 * (syllables / word_count), 2)

def _approx_syllables(word: str) -> int:
    word = word.lower()
    groups = re.findall(r"[aeiouy]+", word)
    return max(1, len(groups))

def type_token_ratio(tokens: List[str]) -> float:
    if not tokens:
        return 0.0
    return round(len(set(tokens)) / len(tokens), 4)

def count_occurrences(text: str, pattern: str, flags=0) -> int:
    return len(re.findall(pattern, text, flags))

def detect_independence(relevance_text: str) -> bool:
    # Heuristic: calibration appendix only after first classification table or section
    calib = relevance_text.lower().find("calibration")
    if calib == -1:
        return True  # No calibration present yet
    first_class = relevance_text.lower().find("relevant")
    return first_class != -1 and calib > first_class

def citation_metrics(texts: Dict[str,str]) -> Tuple[int, float]:
    all_text = "\n".join(texts.values()).lower()
    total = 0
    matched = 0
    for doc in REFERENCE_DOCS:
        pattern = re.escape("ocean-research/" + doc)
        occurrences = len(re.findall(pattern, all_text))
        total += occurrences
        if occurrences > 0:
            matched += 1
    coverage_ratio = matched / len(REFERENCE_DOCS)
    return total, round(coverage_ratio, 3)

def coverage_flags(arch_text: str) -> Dict[str,bool]:
    lower = arch_text.lower()
    return {
        "mcp": "mcp" in lower,
        "knowledge": "knowledge" in lower,
        "dgx": "dgx" in lower or "manolin" in lower,
        "ethics_concurrency": ("ethic" in lower and "concurr" in lower) or "gating" in lower,
    }

def parse_migration(mig_text: str) -> Dict[str, float]:
    # Milestones: headings with 'Milestone' or enumerated lists
    milestone_matches = re.findall(r"(?im)^#+ .*milestone|Milestone\s+\d+", mig_text)
    milestone_count = len(milestone_matches) or max(1, len(re.findall(r"(?m)^\d+\. ", mig_text)))
    tasks = re.findall(r"- \[ \]", mig_text)
    if milestone_count == 0:
        milestone_count = 1
    avg_tasks = len(tasks) / milestone_count if milestone_count else 0
    acceptance = len(re.findall(r"acceptance", mig_text, re.IGNORECASE)) + len(re.findall(r"Acceptance Criteria", mig_text))
    return {
        "milestone_count": milestone_count,
        "avg_tasks_per_milestone": round(avg_tasks, 2),
        "acceptance_criteria_count": acceptance,
    }

def checklist_total(texts: Dict[str,str]) -> int:
    return sum(len(re.findall(r"- \[ \]", t)) for t in texts.values())

def evaluate_plan_dir(plan_dir: Path, baseline_dir: Path|None) -> Dict:
    model_name = plan_dir.name.replace("arch-redux-", "").replace("-v2-plan", "")
    files = {f.name: f for f in plan_dir.glob("*.md")}
    presence = {
        "architecture_plan": "ARCHITECTURE_PLAN.md" in files,
        "migration_steps": "MIGRATION_STEPS.md" in files,
        "folder_layout": "FOLDER_LAYOUT_PROPOSAL.md" in files,
        "relevance_map": "RELEVANCE_MAP.md" in files,
        "assumptions_and_risks": "ASSUMPTIONS_AND_RISKS.md" in files,
    }
    texts = {name: read_file(path) for name, path in files.items()}
    date_present = all(bool(DATE_PATTERN.search(texts.get(n, ""))) for n in REQUIRED_FILES if n in texts)
    arch_text = texts.get("ARCHITECTURE_PLAN.md", "")
    mig_text = texts.get("MIGRATION_STEPS.md", "")
    rel_text = texts.get("RELEVANCE_MAP.md", "")
    risks_text = texts.get("ASSUMPTIONS_AND_RISKS.md", "")

    cov = coverage_flags(arch_text)
    total_citations, coverage_ratio = citation_metrics(texts)
    interface_mentions = count_occurrences(arch_text, r"(?i)manifest|interface|contract|ttl|service")
    mig_metrics = parse_migration(mig_text)
    independence = detect_independence(rel_text)

    risk_count = count_occurrences(risks_text, r"(?i)risk")
    mitigation_count = count_occurrences(risks_text, r"(?i)mitigation")
    knowledge_cross = count_occurrences("\n".join(texts.values()), r"knowledge/")
    ships_log_links = count_occurrences("\n".join(texts.values()), r"ships-log")

    tokens = TOKEN_PATTERN.findall("\n".join(texts.values()))
    ttr = type_token_ratio(tokens)
    flesch = flesch_reading_ease("\n".join(texts.values()))

    ethics_concurrency_mentions = count_occurrences(arch_text, r"(?i)ethic") + count_occurrences(arch_text, r"(?i)concurr")
    assumption_count = count_occurrences(risks_text, r"(?i)assumption")
    checklist = checklist_total(texts)

    # Placeholder novelty (no embedding implementation here)
    novelty_similarity = None
    if baseline_dir and baseline_dir.exists() and baseline_dir != plan_dir:
        # naive overlap ratio of tokens
        baseline_tokens = TOKEN_PATTERN.findall("\n".join(read_file(f) for f in baseline_dir.glob("*.md")))
        overlap = len(set(tokens) & set(baseline_tokens))
        denom = len(set(tokens) | set(baseline_tokens)) or 1
        novelty_similarity = round(overlap / denom, 4)

    result = {
        "model_name": model_name,
        "plan_path": str(plan_dir),
        "presence": presence,
        "headings": {"date_present": date_present},
        "coverage": cov,
        "citations": {"total": total_citations, "coverage_ratio": coverage_ratio},
        "specificity": {"interfaces": interface_mentions},
        "migration": mig_metrics,
        "relevance": {"independence": independence},
        "risks": {"risk_count": risk_count, "mitigation_count": mitigation_count},
        "knowledge": {"cross_links": knowledge_cross, "ships_log_links": ships_log_links},
        "lexical": {"token_count": len(tokens), "type_token_ratio": ttr},
        "readability": {"flesch": flesch},
        "lint": {"markdown_pass": None},
        "novelty": {"embedding_similarity_baseline": novelty_similarity},
        "ethics": {"concurrency_mentions": ethics_concurrency_mentions},
        "assumptions": {"assumption_count": assumption_count},
        "checklist": {"total": checklist},
        "manual": {}
    }
    return result

def load_manual_scores(path: Path) -> Dict[str, Dict]:
    if not path.exists():
        return {}
    # very simple YAML subset: key: value pairs under model name headings
    content = path.read_text(encoding="utf-8")
    blocks = re.split(r"(?m)^model:\s*", content)
    scores = {}
    for block in blocks:
        if not block.strip():
            continue
        lines = block.strip().splitlines()
        model = lines[0].strip()
        data = {}
        for line in lines[1:]:
            if ":" in line:
                k,v = line.split(":",1)
                data[k.strip()] = v.strip()
        scores[model] = data
    return scores

def append_manual(results: List[Dict], manual: Dict[str, Dict]) -> None:
    for r in results:
        m = manual.get(r["model_name"], {})
        if m:
            r["manual"] = {
                "feasibility_score": int(m.get("feasibility", 0)) if m.get("feasibility") else None,
                "clarity_score": int(m.get("clarity", 0)) if m.get("clarity") else None,
                "risk_depth_score": int(m.get("risk_depth", 0)) if m.get("risk_depth") else None,
                "delta_quality_notes": m.get("notes")
            }

def parse_weights(config_path: Path) -> Dict[str,float]:
    if not config_path or not config_path.exists():
        return {}
    weights_section = False
    weights: Dict[str,float] = {}
    for line in config_path.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("weights:"):
            weights_section = True
            continue
        if weights_section:
            if not line.strip():
                break
            if re.match(r"^[A-Za-z_]+:\s*[0-9.]+", line.strip()):
                k,v = line.split(":",1)
                try:
                    weights[k.strip()] = float(v.strip())
                except ValueError:
                    pass
    return weights

def leaderboard(results: List[Dict], weights: Dict[str,float]|None=None) -> List[Tuple[str, float]]:
    # Default raw component weights if none supplied
    default_weights = {
        "presence": 1.0,
        "coverage": 1.0,
        "citations": 1.0,
        "specificity": 1.0,
        "migration": 1.0,
        "risks": 1.0,
        "readability": 0.5,
        "novelty": 0.5,
        "manual": 1.0,
    }
    if weights:
        default_weights.update(weights)
    scores = []
    for r in results:
        presence_norm = sum(r["presence"].values()) / len(r["presence"]) if r.get("presence") else 0
        coverage_norm = sum(1 for v in r["coverage"].values() if v) / len(r["coverage"]) if r.get("coverage") else 0
        citations_norm = r["citations"].get("coverage_ratio",0)
        specificity_norm = min(r["specificity"]["interfaces"], 50) / 50 if r.get("specificity") else 0
        migration_norm = min(r["migration"].get("milestone_count",0),7)/7 if r.get("migration") else 0
        risks_norm = min(r["risks"].get("risk_count",0),20)/20 if r.get("risks") else 0
        readability_norm = (r["readability"].get("flesch",0)/100) if r.get("readability") else 0
        novelty_norm = 1.0 - (r["novelty"].get("embedding_similarity_baseline") or 0) if r.get("novelty") else 0
        manual_scores = [r["manual"].get(k) for k in ["feasibility_score","clarity_score","risk_depth_score"] if r.get("manual")]
        manual_avg = statistics.mean([s for s in manual_scores if isinstance(s,int)]) / 5 if manual_scores else 0
        total = (
            presence_norm * default_weights["presence"] +
            coverage_norm * default_weights["coverage"] +
            citations_norm * default_weights["citations"] +
            specificity_norm * default_weights["specificity"] +
            migration_norm * default_weights["migration"] +
            risks_norm * default_weights["risks"] +
            readability_norm * default_weights["readability"] +
            novelty_norm * default_weights["novelty"] +
            manual_avg * default_weights["manual"]
        )
        scores.append((r["model_name"], round(total,4)))
    return sorted(scores, key=lambda x: x[1], reverse=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans-root", help="Root directory containing plan subdirectories")
    ap.add_argument("--out", help="Output JSON path")
    ap.add_argument("--leaderboard", help="Existing metrics JSON to summarize")
    ap.add_argument("--append-manual", action="store_true")
    ap.add_argument("--input", help="Existing metrics JSON for manual append")
    ap.add_argument("--manual", help="Manual scores YAML path")
    ap.add_argument("--config", help="Models config path (for weights)")
    args = ap.parse_args()

    if args.leaderboard:
        data = json.loads(Path(args.leaderboard).read_text())
        weights = parse_weights(Path(args.config)) if args.config else {}
        lb = leaderboard(data, weights)
        print("Model,Score")
        for model, score in lb:
            print(f"{model},{score}")
        return

    if args.append_manual:
        if not args.input or not args.manual:
            print("--append-manual requires --input and --manual", file=sys.stderr)
            sys.exit(1)
        results = json.loads(Path(args.input).read_text())
        manual = load_manual_scores(Path(args.manual))
        append_manual(results, manual)
        Path(args.input).write_text(json.dumps(results, indent=2))
        print(f"Manual scores appended to {args.input}")
        return

    root = Path(args.plans_root)
    if not root.exists():
        print(f"Plans root {root} not found", file=sys.stderr)
        sys.exit(1)

    baseline = root / "arch-redux-gpt-5-v2-plan"
    results = []
    for sub in root.iterdir():
        if sub.is_dir() and sub.name.startswith("arch-redux-") and sub.name.endswith("-v2-plan"):
            results.append(evaluate_plan_dir(sub, baseline))
    Path(args.out).write_text(json.dumps(results, indent=2))
    print(f"Metrics written to {args.out}")

if __name__ == "__main__":
    main()
