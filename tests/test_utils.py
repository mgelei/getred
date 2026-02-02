"""Tests for utility functions."""

import pytest
from getred.utils import validate_reddit_url, generate_slug


class TestValidateRedditUrl:
    """Tests for validate_reddit_url function."""

    def test_validate_reddit_url_valid(self):
        """Valid URLs with/without www should pass validation."""
        valid_urls = [
            "https://reddit.com/r/python/comments/abc123/cool_title/",
            "https://www.reddit.com/r/python/comments/abc123/cool_title/",
            "http://reddit.com/r/AskReddit/comments/xyz789/interesting_question/",
            "https://reddit.com/r/programming/comments/test123/test/extra/path/",
        ]
        for url in valid_urls:
            assert validate_reddit_url(url), f"Expected {url} to be valid"

    def test_validate_reddit_url_invalid(self):
        """Non-Reddit and malformed URLs should fail validation."""
        invalid_urls = [
            "https://example.com/r/python/comments/abc123/",
            "https://reddit.com/r/python/",  # Missing /comments/
            "https://reddit.com/comments/abc123/",  # Missing /r/subreddit/
            "not a url",
            "",
            "ftp://reddit.com/r/python/comments/abc123/",
        ]
        for url in invalid_urls:
            assert not validate_reddit_url(url), f"Expected {url} to be invalid"


class TestGenerateSlug:
    """Tests for generate_slug function."""

    def test_generate_slug_full_url(self):
        """Extracts {id}_{title} from complete URL."""
        url = "https://reddit.com/r/python/comments/abc123/cool_python_feature/"
        assert generate_slug(url) == "abc123_cool_python_feature"

    def test_generate_slug_id_only(self):
        """Handles URL without title, returns only ID."""
        url = "https://reddit.com/r/python/comments/xyz789/"
        assert generate_slug(url) == "xyz789"

    def test_generate_slug_with_extra_path(self):
        """Handles URLs with additional path segments."""
        url = "https://reddit.com/r/AskReddit/comments/test123/interesting_question/extra/path/"
        assert generate_slug(url) == "test123_interesting_question"

    def test_generate_slug_fallback(self):
        """Returns default for malformed URLs."""
        url = "https://reddit.com/not/a/valid/url/"
        assert generate_slug(url) == "reddit_thread"
