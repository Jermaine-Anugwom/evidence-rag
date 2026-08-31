import pytest

from evidence_rag.core import Passage, answer

DOCS = [
    Passage("A", "Remote inspections require a signed checklist."),
    Passage("B", "Remote inspection checklists are retained for seven years."),
    Passage("C", "Travel reimbursement is not required for remote inspections."),
]


@pytest.mark.parametrize(
    "q",
    [
        "What do remote inspections require?",
        "Is a signed remote checklist required?",
        "remote inspections signed checklist",
    ],
)
def test_retrieves(q):
    result = answer(q, DOCS)
    assert not result.abstained and "A" in result.citations


@pytest.mark.parametrize(
    "q", ["What is the moon made of?", "Unknown pension rule", "cafeteria hours"]
)
def test_abstains(q):
    assert answer(q, DOCS).abstained


def test_has_citations():
    assert answer("remote inspection checklist", DOCS).citations


def test_limits_citations():
    assert len(answer("remote inspections required", DOCS).citations) <= 3


def test_empty_corpus():
    assert answer("anything", []).abstained


def test_detects_contradiction():
    docs = [
        Passage("A", "Badge training is required."),
        Passage("B", "Badge training is not required."),
    ]
    assert answer("badge training required", docs, 1).contradictions == ("A", "B")


def test_deterministic():
    assert answer("remote inspection checklist", DOCS) == answer(
        "remote inspection checklist", DOCS
    )
