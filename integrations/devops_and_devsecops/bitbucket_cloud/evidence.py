from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceResult:
    code: str
    name: str
    payload: dict


def collect_all() -> list[EvidenceResult]:
    """Collect all evidence items for this tool."""
    raise NotImplementedError()
