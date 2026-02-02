"""Tests for Reddit JSON parser."""

import pytest
from getred.parser import parse_timestamp, parse_comment, parse_comments, parse_thread
from getred.models import Comment, Thread


class TestParseTimestamp:
    """Tests for parse_timestamp function."""

    def test_parse_timestamp(self):
        """Unix timestamp converts to ISO format."""
        timestamp = 1609459200.0  # 2021-01-01 00:00:00 UTC
        result = parse_timestamp(timestamp)
        assert result == "2021-01-01T00:00:00Z"


class TestParseComment:
    """Tests for parse_comment function."""

    def test_parse_comment_basic(self, sample_comment_data):
        """Parses comment fields correctly."""
        comment = parse_comment(sample_comment_data, depth=0)

        assert comment.id == "comment123"
        assert comment.author == "test_user"
        assert comment.body == "This is a test comment"
        assert comment.score == 42
        assert comment.created_utc == "2021-01-01T00:00:00Z"
        assert comment.depth == 0
        assert comment.replies == []

    def test_parse_comment_with_replies(self, sample_comment_with_replies):
        """Handles nested replies and depth tracking."""
        parent = parse_comment(sample_comment_with_replies, depth=0)

        assert parent.id == "parent123"
        assert parent.author == "parent_user"
        assert parent.depth == 0
        assert len(parent.replies) == 1

        child = parent.replies[0]
        assert child.id == "child123"
        assert child.author == "child_user"
        assert child.body == "Child comment"
        assert child.depth == 1
        assert child.replies == []

    def test_parse_comment_deleted(self):
        """Handles deleted/removed comments."""
        deleted_data = {
            "kind": "t1",
            "data": {
                "id": "deleted123",
                "author": "[deleted]",
                "body": "[removed]",
                "score": 0,
                "created_utc": 1609459200.0,
                "replies": ""
            }
        }
        comment = parse_comment(deleted_data, depth=0)

        assert comment.author == "[deleted]"
        assert comment.body == "[removed]"


class TestParseComments:
    """Tests for parse_comments function."""

    def test_parse_comments_filters_more(self):
        """Skips 'more' objects (kind != t1)."""
        comments_listing = [
            {
                "kind": "t1",
                "data": {
                    "id": "comment1",
                    "author": "user1",
                    "body": "Valid comment",
                    "score": 10,
                    "created_utc": 1609459200.0,
                    "replies": ""
                }
            },
            {
                "kind": "more",
                "data": {
                    "count": 5,
                    "children": ["abc", "def"]
                }
            },
            {
                "kind": "t1",
                "data": {
                    "id": "comment2",
                    "author": "user2",
                    "body": "Another valid comment",
                    "score": 20,
                    "created_utc": 1609462800.0,
                    "replies": ""
                }
            }
        ]

        comments = parse_comments(comments_listing)

        assert len(comments) == 2
        assert comments[0].id == "comment1"
        assert comments[1].id == "comment2"


class TestParseThread:
    """Tests for parse_thread function."""

    def test_parse_thread(self, sample_thread_json):
        """Full thread parsing with metadata and comments."""
        thread = parse_thread(sample_thread_json)

        assert thread.id == "thread123"
        assert thread.title == "Test Thread Title"
        assert thread.author == "thread_author"
        assert thread.subreddit == "python"
        assert thread.url == "https://reddit.com/r/python/comments/thread123/test_thread_title/"
        assert thread.selftext == "This is the thread body"
        assert thread.score == 500
        assert thread.created_utc == "2021-01-01T00:00:00Z"
        assert thread.comment_count == 2
        assert thread.fetched_at.endswith("Z")

        # Should only parse t1 comments, not 'more' objects
        assert len(thread.comments) == 1
        assert thread.comments[0].id == "comment1"
