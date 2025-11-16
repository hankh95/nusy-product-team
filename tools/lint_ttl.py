#!/usr/bin/env python3
import sys
import pathlib
from rdflib import Graph


def find_ttl_files(root: pathlib.Path):
    for p in root.rglob("*.ttl"):
        # Skip .git and virtual envs
        parts = set(p.parts)
        if ".git" in parts or ".venv" in parts or "node_modules" in parts:
            continue
        yield p


def lint_file(path: pathlib.Path) -> bool:
    g = Graph()
    try:
        g.parse(path.as_posix(), format="turtle")
        return True
    except Exception as e:
        print(f"TTL Lint Error: {path}: {e}")
        return False


def main():
    root = pathlib.Path.cwd()
    ttl_files = list(find_ttl_files(root))
    if not ttl_files:
        print("No .ttl files found.")
        return 0

    ok = True
    for f in ttl_files:
        if not lint_file(f):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
