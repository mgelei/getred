"""HTTP client for fetching Reddit data."""

from __future__ import annotations

from typing import Any, Dict, Optional
from urllib.parse import urlsplit, urlunsplit

import httpx


class RedditFetcher:
    """Fetches Reddit thread data using the public JSON API."""

    USER_AGENT = "getred/0.1.0 (Reddit Thread Fetcher CLI)"
    TIMEOUT = 30.0

    def __init__(self, transport: Optional[httpx.BaseTransport] = None):
        """Initialize the fetcher with custom headers."""
        self.headers = {
            "User-Agent": self.USER_AGENT
        }
        self._transport = transport

    @staticmethod
    def _build_json_url(url: str) -> str:
        """
        Construct a Reddit .json endpoint URL from a thread URL.

        - Preserves query parameters
        - Avoids double-appending .json
        - Drops fragments
        """
        parts = urlsplit(url)

        path = parts.path or "/"
        if not path.endswith(".json"):
            path = path + ".json"

        return urlunsplit((parts.scheme, parts.netloc, path, parts.query, ""))

    def fetch_thread(self, url: str) -> Dict[str, Any]:
        """
        Fetch a Reddit thread as JSON.

        Args:
            url: Reddit thread URL (will be converted to JSON endpoint)

        Returns:
            Dict containing Reddit API response

        Raises:
            httpx.HTTPError: If request fails
        """
        json_url = self._build_json_url(url)

        with httpx.Client(
            headers=self.headers,
            timeout=self.TIMEOUT,
            follow_redirects=True,
            transport=self._transport,
        ) as client:
            response = client.get(json_url)
            response.raise_for_status()
            try:
                return response.json()
            except ValueError as e:
                content_type = response.headers.get("Content-Type", "<missing>")
                raise ValueError(
                    f"Non-JSON response from Reddit endpoint "
                    f"(url={response.url!s}, status={response.status_code}, content_type={content_type})"
                ) from e
