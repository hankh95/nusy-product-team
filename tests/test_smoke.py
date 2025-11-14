from pathlib import Path


def test_repo_scaffold_exists():
    required = [
        "README.md",
        "DEVELOPMENT_PLAN.md",
        "DEVELOPMENT_PRACTICES.md",
        "features/scaffold_project.feature",
        "src/nusy_pm_core/api.py",
        "src/nusy_pm_core/cli.py",
    ]
    for rel_path in required:
        path = Path(rel_path)
        assert path.exists(), f"{rel_path} should exist"
