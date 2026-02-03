"""Utility functions for URL validation, slug generation, and file operations."""

import json
import re
from pathlib import Path
from typing import Dict, Any


def validate_reddit_url(url: str) -> bool:
    """
    Validate that a URL is a Reddit thread URL.

    Args:
        url: URL to validate

    Returns:
        True if valid Reddit thread URL, False otherwise
    """
    pattern = r'^https?://(www\.)?reddit\.com/r/[^/]+/comments/[^/]+(?:[/?#]|$)'
    return bool(re.match(pattern, url))


def generate_slug(url: str) -> str:
    """
    Generate a filename slug from a Reddit URL.

    Extracts the thread ID and title from the URL.
    Example: https://reddit.com/r/python/comments/abc123/cool_title/
    Returns: abc123_cool_title

    Args:
        url: Reddit thread URL

    Returns:
        Slug string suitable for filename
    """
    # Extract thread ID and title from URL
    # Pattern: /r/subreddit/comments/ID/title/
    match = re.search(r'/comments/([^/]+)/([^/]+)', url)
    if match:
        thread_id = match.group(1)
        title_slug = match.group(2)
        return f"{thread_id}_{title_slug}"

    # Fallback to just using the thread ID
    match = re.search(r'/comments/([^/]+)', url)
    if match:
        return match.group(1)

    return "reddit_thread"


def get_default_output_path(url: str) -> Path:
    """
    Generate default output path in ~/Downloads.

    Args:
        url: Reddit thread URL

    Returns:
        Path object for output file
    """
    downloads_dir = Path.home() / "Downloads"
    slug = generate_slug(url)
    return downloads_dir / f"{slug}.json"


def save_json(data: Dict[str, Any], output_path: Path, pretty: bool = True) -> None:
    """
    Save data as JSON file.

    Args:
        data: Dictionary to save
        output_path: Path where to save the file
        pretty: Whether to pretty-print the JSON (default: True)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            json.dump(data, f, ensure_ascii=False)
