"""Storage layer stubs for database and object storage."""

from pathlib import Path
from typing import Any


class Database:
    """Very small placeholder database implementation."""

    def __init__(self) -> None:
        self.records = []

    def insert(self, data: dict[str, Any]) -> None:
        self.records.append(data)

    def all(self) -> list[dict[str, Any]]:
        return list(self.records)


class ObjectStore:
    """Simple object store stub that saves objects on the filesystem."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, name: str, data: bytes) -> Path:
        path = self.root / name
        with open(path, "wb") as fh:
            fh.write(data)
        return path
