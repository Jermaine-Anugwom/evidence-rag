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


def _proposition_tokens(text: str) -> set[str]:
    stop = {
        "a",
        "an",
        "the",
        "is",
        "are",
        "was",
        "were",
        "does",
        "do",
        "not",
        "required",
        "require",
        "requires",
        "must",
        "for",
        "of",
        "to",
        "in",
    }
    return {token.removesuffix("s") for token in _tokens(text) - stop}


def answer(question: str, passages: list[Passage], minimum_overlap: int = 2) -> Answer:
    q = _tokens(question)
    ranked = sorted(
        ((len(q & _tokens(p.text)), p) for p in passages), key=lambda x: x[0], reverse=True
    )
    selected = [p for score, p in ranked if score >= minimum_overlap][:3]
    if not selected:
        return Answer("Insufficient evidence.", (), True, ())
    polarity: dict[str, list[tuple[str, set[str]]]] = {"required": [], "not required": []}
    for p in selected:
        text = p.text.lower()
        negative_spans = list(
            re.finditer(
                r"\b(?:is|are|was|were)?\s*not\s+required\b|\bdoes\s+not\s+require\b|\bno\s+\w+(?:\s+\w+){0,3}\s+required\b",
                text,
            )
        )
        if negative_spans:
            polarity["not required"].append((p.source_id, _proposition_tokens(text)))
        affirmative_text = text
        for match in reversed(negative_spans):
            affirmative_text = affirmative_text[: match.start()] + affirmative_text[match.end() :]
        if re.search(r"\brequired\b|\brequires?\b|\bmust\b", affirmative_text):
            polarity["required"].append((p.source_id, _proposition_tokens(affirmative_text)))
    conflict_sources: set[str] = set()
    for positive_id, positive_terms in polarity["required"]:
        for negative_id, negative_terms in polarity["not required"]:
            denominator = min(len(positive_terms), len(negative_terms))
            overlap = len(positive_terms & negative_terms) / denominator if denominator else 0
            if overlap >= 0.6:
                conflict_sources.update((positive_id, negative_id))
    conflicts = tuple(sorted(conflict_sources))
    if conflicts:
        return Answer(
            "Conflicting evidence requires review.",
            tuple(p.source_id for p in selected),
            True,
            conflicts,
        )
    return Answer(selected[0].text, tuple(p.source_id for p in selected), False, conflicts)
