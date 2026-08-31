from __future__ import annotations

import json
from dataclasses import asdict

from .core import Passage, answer


def main() -> None:
    passages = [
        Passage(
            "PUB-01", "A synthetic permit is required for excavation in the public right of way."
        ),
        Passage("PUB-02", "Emergency surface repairs do not require the synthetic permit."),
    ]
    result = answer("Is a permit required for excavation in the public right of way?", passages)
    print(json.dumps({"synthetic": True, "result": asdict(result)}, indent=2))
