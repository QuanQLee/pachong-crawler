"""Utility crawler package with URL discovery, fetching and storage helpers."""

# Import modules lazily to avoid requiring optional dependencies such as
# ``bs4`` unless they are actually used.  Consumers can still access the
# common helpers via ``crawler.<name>`` thanks to ``__getattr__`` below.

__all__ = [
    "discover_urls",
    "Fetcher",
    "download_file",
    "deduplicate",
    "normalize_entry",
    "Database",
    "ObjectStore",
    "AsyncCrawler",
    "SQLiteStore",
]

def __getattr__(name):
    """Dynamically import members when accessed."""
    if name == "discover_urls":
        from .discovery import discover_urls as attr
    elif name == "Fetcher":
        from .fetcher import Fetcher as attr
    elif name == "download_file":
        from .downloader import download_file as attr
    elif name == "deduplicate":
        from .cleaner import deduplicate as attr
    elif name == "normalize_entry":
        from .cleaner import normalize_entry as attr
    elif name == "Database":
        from .storage import Database as attr
    elif name == "ObjectStore":
        from .storage import ObjectStore as attr
    elif name == "AsyncCrawler":
        from .async_crawler import AsyncCrawler as attr
    elif name == "SQLiteStore":
        from .async_crawler import SQLiteStore as attr
    else:
        raise AttributeError(name)
    globals()[name] = attr
    return attr
