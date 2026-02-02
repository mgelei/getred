"""Tests for data models."""

import pytest
from getred.models import Comment, Thread


class TestCommentToDict:
    """Tests for Comment.to_dict() method."""

    def test_comment_to_dict(self):
        """Serializes comment fields correctly."""
        comment = Comment(
            id="test123",
            author="test_user",
            body="Test comment body",
            score=42,
            created_utc="2021-01-01T00:00:00Z",
            depth=0,
            replies=[]
        )

        result = comment.to_dict()

        assert result == {
            "id": "test123",
            "author": "test_user",
            "body": "Test comment body",
            "score": 42,
            "created_utc": "2021-01-01T00:00:00Z",
            "depth": 0,
            "replies": []
        }

    def test_comment_to_dict_nested(self):
        """Serializes nested replies recursively."""
        child = Comment(
            id="child123",
            author="child_user",
            body="Child comment",
            score=10,
            created_utc="2021-01-01T01:00:00Z",
            depth=1,
            replies=[]
        )

        parent = Comment(
            id="parent123",
            author="parent_user",
            body="Parent comment",
            score=50,
            created_utc="2021-01-01T00:00:00Z",
            depth=0,
            replies=[child]
        )

        result = parent.to_dict()

        assert result["id"] == "parent123"
        assert result["depth"] == 0
        assert len(result["replies"]) == 1
        assert result["replies"][0]["id"] == "child123"
        assert result["replies"][0]["depth"] == 1
        assert result["replies"][0]["replies"] == []


class TestThreadToDict:
    """Tests for Thread.to_dict() method."""

    def test_thread_to_dict(self):
        """Serializes thread with comments."""
        comment = Comment(
            id="comment123",
            author="commenter",
            body="Great post!",
            score=25,
            created_utc="2021-01-01T01:00:00Z",
            depth=0,
            replies=[]
        )

        thread = Thread(
            id="thread123",
            title="Test Thread",
            author="thread_author",
            subreddit="python",
            url="https://reddit.com/r/python/comments/thread123/test_thread/",
            selftext="Thread body content",
            score=500,
            created_utc="2021-01-01T00:00:00Z",
            fetched_at="2021-01-01T02:00:00Z",
            comment_count=1,
            comments=[comment]
        )

        result = thread.to_dict()

        assert result["id"] == "thread123"
        assert result["title"] == "Test Thread"
        assert result["author"] == "thread_author"
        assert result["subreddit"] == "python"
        assert result["url"] == "https://reddit.com/r/python/comments/thread123/test_thread/"
        assert result["selftext"] == "Thread body content"
        assert result["score"] == 500
        assert result["created_utc"] == "2021-01-01T00:00:00Z"
        assert result["fetched_at"] == "2021-01-01T02:00:00Z"
        assert result["comment_count"] == 1
        assert len(result["comments"]) == 1
        assert result["comments"][0]["id"] == "comment123"
