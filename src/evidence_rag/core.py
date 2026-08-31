from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Passage:
    source_id: str
    text: str


@dataclass(frozen=True)
class Answer:
    text: str
    citations: tuple[str, ...]
    abstained: bool
    contradictions: tuple[str, ...]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def answer(question: str, passages: list[Passage], minimum_overlap: int = 2) -> Answer:
    q = _tokens(question)
    ranked = sorted(
        ((len(q & _tokens(p.text)), p) for p in passages), key=lambda x: x[0], reverse=True
    )
    selected = [p for score, p in ranked if score >= minimum_overlap][:3]
    if not selected:
        return Answer("Insufficient evidence.", (), True, ())
    polarity = {"required": [], "not required": []}
    for p in selected:
        for key, sources in polarity.items():
            if key in p.text.lower():
                sources.append(p.source_id)
    conflicts = (
        tuple(sorted(set(polarity["required"]) | set(polarity["not required"])))
        if all(polarity.values())
        else ()
    )
    return Answer(selected[0].text, tuple(p.source_id for p in selected), False, conflicts)
