"""Data models for Reddit threads and comments."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class Comment:
    """Represents a Reddit comment."""

    id: str
    author: str
    body: str
    score: int
    created_utc: str
    depth: int
    replies: List['Comment'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert comment to dictionary format."""
        return {
            "id": self.id,
            "author": self.author,
            "body": self.body,
            "score": self.score,
            "created_utc": self.created_utc,
            "depth": self.depth,
            "replies": [reply.to_dict() for reply in self.replies]
        }


@dataclass
class Thread:
    """Represents a Reddit thread."""

    id: str
    title: str
    author: str
    subreddit: str
    url: str
    selftext: str
    score: int
    created_utc: str
    fetched_at: str
    comment_count: int
    comments: List[Comment] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert thread to dictionary format."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "subreddit": self.subreddit,
            "url": self.url,
            "selftext": self.selftext,
            "score": self.score,
            "created_utc": self.created_utc,
            "fetched_at": self.fetched_at,
            "comment_count": self.comment_count,
            "comments": [comment.to_dict() for comment in self.comments]
        }
