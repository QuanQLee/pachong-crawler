from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Any

from ..fetcher import Fetcher


class Platform(ABC):
    """Base class for platform-specific scrapers."""

    def __init__(self, fetcher: Fetcher | None = None) -> None:
        self.fetcher = fetcher or Fetcher()

    @abstractmethod
    def fetch_items(self) -> Iterable[dict[str, Any]]:
        """Return items gathered from the platform."""
        pass
