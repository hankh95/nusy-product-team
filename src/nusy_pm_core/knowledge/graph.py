from dataclasses import dataclass
from typing import List


@dataclass
class Feature:
    id: str
    title: str
    description: str


def get_initial_features() -> List[Feature]:
    return [
        Feature(
            id="NUSY-FEAT-001",
            title="Scaffold the NuSy Product Project",
            description="Create core repo structure, docs, and first BDD feature.",
        )
    ]
