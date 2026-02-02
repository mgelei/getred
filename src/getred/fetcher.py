"""HTTP client for fetching Reddit data."""

import httpx
from typing import Dict, Any


class RedditFetcher:
    """Fetches Reddit thread data using the public JSON API."""

    USER_AGENT = "getred/0.1.0 (Reddit Thread Fetcher CLI)"
    TIMEOUT = 30.0

    def __init__(self):
        """Initialize the fetcher with custom headers."""
        self.headers = {
            "User-Agent": self.USER_AGENT
        }

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
        # Ensure URL ends with .json
        json_url = url.rstrip('/') + '.json'

        with httpx.Client(headers=self.headers, timeout=self.TIMEOUT) as client:
            response = client.get(json_url)
            response.raise_for_status()
            return response.json()
