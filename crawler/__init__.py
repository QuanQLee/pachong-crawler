"""Utility crawler package with URL discovery, fetching and storage helpers."""

from .discovery import discover_urls
from .fetcher import Fetcher
from .downloader import download_file
from .cleaner import deduplicate, normalize_entry
from .storage import Database, ObjectStore

__all__ = [
    "discover_urls",
    "Fetcher",
    "download_file",
    "deduplicate",
    "normalize_entry",
    "Database",
    "ObjectStore",
]
