"""Helpers for downloading files such as videos or attachments."""

from pathlib import Path
from typing import Optional

import requests


def download_file(url: str, dest: Path, chunk_size: int = 8192) -> Path:
    """Download *url* to *dest* and return the local path."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(chunk_size=chunk_size):
                if chunk:
                    fh.write(chunk)
    return dest
