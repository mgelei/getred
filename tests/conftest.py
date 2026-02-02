"""Shared fixtures for getred tests."""

import pytest


@pytest.fixture
def sample_comment_data():
    """Minimal comment structure from Reddit API."""
    return {
        "kind": "t1",
        "data": {
            "id": "comment123",
            "author": "test_user",
            "body": "This is a test comment",
            "score": 42,
            "created_utc": 1609459200.0,  # 2021-01-01 00:00:00 UTC
            "replies": ""
        }
    }


@pytest.fixture
def sample_comment_with_replies():
    """Comment with nested reply."""
    return {
        "kind": "t1",
        "data": {
            "id": "parent123",
            "author": "parent_user",
            "body": "Parent comment",
            "score": 100,
            "created_utc": 1609459200.0,
            "replies": {
                "kind": "Listing",
                "data": {
                    "children": [
                        {
                            "kind": "t1",
                            "data": {
                                "id": "child123",
                                "author": "child_user",
                                "body": "Child comment",
                                "score": 50,
                                "created_utc": 1609462800.0,  # 1 hour later
                                "replies": ""
                            }
                        }
                    ]
                }
            }
        }
    }


@pytest.fixture
def sample_thread_json():
    """Full 2-element Reddit API response."""
    return [
        {
            "kind": "Listing",
            "data": {
                "children": [
                    {
                        "kind": "t3",
                        "data": {
                            "id": "thread123",
                            "title": "Test Thread Title",
                            "author": "thread_author",
                            "subreddit": "python",
                            "url": "https://reddit.com/r/python/comments/thread123/test_thread_title/",
                            "selftext": "This is the thread body",
                            "score": 500,
                            "created_utc": 1609459200.0,
                            "num_comments": 2
                        }
                    }
                ]
            }
        },
        {
            "kind": "Listing",
            "data": {
                "children": [
                    {
                        "kind": "t1",
                        "data": {
                            "id": "comment1",
                            "author": "user1",
                            "body": "First comment",
                            "score": 10,
                            "created_utc": 1609462800.0,
                            "replies": ""
                        }
                    },
                    {
                        "kind": "more",
                        "data": {
                            "count": 5,
                            "children": ["abc", "def"]
                        }
                    }
                ]
            }
        }
    ]
