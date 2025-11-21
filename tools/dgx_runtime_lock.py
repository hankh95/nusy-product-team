#!/usr/bin/env python3
"""
DGX Runtime Lock Helper

Lightweight lock/ownership mechanism for long-running DGX services
(e.g., vLLM, poller, autonomous team).

Usage examples:

    # Acquire lock for vLLM service
    python tools/dgx_runtime_lock.py --service vllm --action acquire

    # Release lock
    python tools/dgx_runtime_lock.py --service vllm --action release

    # Check status
    python tools/dgx_runtime_lock.py --service vllm --action status

The lock records:
    - service name (vllm, poller, team, etc.)
    - owner (SANTIAGO_ACTOR or system user)
    - current git branch
    - optional Kanban card id (KANBAN_CARD_ID env var)
    - timestamp

This is not a hard security mechanism; it is a coordination tool to help
humans and agents respect DGX runtime ownership etiquette.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


LOCK_FILE = Path("logs/dgx_runtime_owner.json")


@dataclass
class RuntimeLock:
    service: str
    owner: str
    branch: str
    card_id: str
    timestamp: str


def _read_locks() -> Dict[str, Any]:
    if not LOCK_FILE.exists():
        return {}
    try:
        return json.loads(LOCK_FILE.read_text(encoding="utf-8"))
    except Exception:
        # Corrupt file; start fresh but keep a backup
        backup = LOCK_FILE.with_suffix(".backup")
        try:
            LOCK_FILE.replace(backup)
        except Exception:
            pass
        return {}


def _write_locks(data: Dict[str, Any]) -> None:
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCK_FILE.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


def acquire_lock(service: str) -> int:
    locks = _read_locks()
    existing = locks.get(service)

    branch = _current_branch()
    owner = os.getenv("SANTIAGO_ACTOR") or getpass.getuser()
    card_id = os.getenv("KANBAN_CARD_ID", "")

    # Enforce feature/exp/fix/chore branches for runtime operations
    allowed_prefixes = ("feature/", "exp/", "fix/", "chore/")
    if not any(branch.startswith(p) for p in allowed_prefixes):
        print(
            f"❌ DGX runtime operations must be run from a feature/exp/fix/chore branch "
            f"(current branch: {branch!r})."
        )
        return 1

    if existing:
        print(
            f"⚠️ Service '{service}' is already owned by "
            f"{existing.get('owner')} on branch {existing.get('branch')} "
            f"(card: {existing.get('card_id', '')})."
        )
        return 1

    lock = RuntimeLock(
        service=service,
        owner=owner,
        branch=branch,
        card_id=card_id,
        timestamp=datetime.utcnow().isoformat() + "Z",
    )
    locks[service] = asdict(lock)
    _write_locks(locks)

    print(
        f"✅ Acquired DGX runtime lock for service '{service}' "
        f"on branch {branch} (owner: {owner}, card: {card_id or 'n/a'})."
    )
    return 0


def release_lock(service: str) -> int:
    locks = _read_locks()
    existing = locks.get(service)
    if not existing:
        print(f"ℹ️ No existing lock found for service '{service}'. Nothing to release.")
        return 0

    owner = os.getenv("SANTIAGO_ACTOR") or getpass.getuser()
    # We don't strictly enforce same-owner release, but we can warn
    if existing.get("owner") != owner:
        print(
            f"⚠️ Releasing lock for '{service}' owned by {existing.get('owner')}; "
            f"current user is {owner}. (Proceeding anyway.)"
        )

    locks.pop(service, None)
    _write_locks(locks)
    print(f"✅ Released DGX runtime lock for service '{service}'.")
    return 0


def print_status(service: str) -> int:
    locks = _read_locks()
    existing = locks.get(service)
    if not existing:
        print(f"ℹ️ Service '{service}' is currently unlocked.")
        return 0

    print(
        f"🔒 Service '{service}' is locked by {existing.get('owner')} "
        f"on branch {existing.get('branch')} (card: {existing.get('card_id', '')}) "
        f"since {existing.get('timestamp')}."
    )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="DGX runtime lock helper")
    parser.add_argument(
        "--service",
        "-s",
        required=True,
        help="Service name (e.g. vllm, poller, team)",
    )
    parser.add_argument(
        "--action",
        "-a",
        choices=["acquire", "release", "status"],
        required=True,
        help="Action to perform on the lock",
    )
    args = parser.parse_args()

    if args.action == "acquire":
        raise SystemExit(acquire_lock(args.service))
    if args.action == "release":
        raise SystemExit(release_lock(args.service))
    if args.action == "status":
        raise SystemExit(print_status(args.service))


if __name__ == "__main__":
    main()


