"""Deduplication and data normalisation helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Set


def deduplicate(items: Iterable[Any]) -> List[Any]:
    """Return a list of unique items preserving order."""
    seen: Set[Any] = set()
    result: List[Any] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


@dataclass
class NormalisedEntry:
    """Simple structure representing a normalised crawling result."""

    url: str
    title: str = ""
    content: str = ""
    extras: dict[str, Any] = field(default_factory=dict)


def normalize_entry(data: dict[str, Any]) -> NormalisedEntry:
    """Return ``NormalisedEntry`` with common fields present."""
    return NormalisedEntry(
        url=data.get("url", ""),
        title=data.get("title", ""),
        content=data.get("content", ""),
        extras={k: v for k, v in data.items() if k not in {"url", "title", "content"}},
    )
