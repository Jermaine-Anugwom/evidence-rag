# Evidence RAG

**Citation-first retrieval that abstains when evidence is insufficient.**

> All people, organizations, records, measurements, and outcomes in this
> repository are synthetic.

## The operational problem

A fluent answer is unsafe when users cannot inspect its support or contradictions.

## The proof

Deterministic retrieval, sentence citations, contradiction flags, abstention, and retrieval metrics.

## Why this is forward deployed

The project begins with the operator's decision, uncertainty, failure cost,
integration boundary, and handoff—not with a model demo. It makes policy and
evidence inspectable, preserves human authority for consequential cases, and
remains useful when the optional model layer is unavailable.

## Architecture

```mermaid
flowchart LR
  A[Public passages] --> B[Deterministic retrieval]
  Q[Question] --> B
  B --> C{Evidence overlap}
  C -->|insufficient| D[Abstain]
  C -->|supported| E[Answer + citations]
  E --> F{Contradiction?}
  F -->|yes| G[Expose conflicting sources]
```

## Quickstart

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest -q
evidence_rag
```

No API key or network connection is required.

## Evaluation and limitations

Run `pytest -q` for the reproducible evaluation. The fixture set is deliberately
synthetic and cannot establish production performance. A real deployment would
require operator observation, representative data, policy review, privacy review,
security testing, and a monitored rollout.

## Project documents

- [Field discovery and handoff](FIELD_NOTES.md)
- [Security boundaries](SECURITY.md)
- [Operating runbook](RUNBOOK.md)
- [Development provenance](DEVELOPMENT.md)
- [Release history](CHANGELOG.md)

## Topics

`rag`, `citations`, `ai-evals`, `retrieval`, `python`
