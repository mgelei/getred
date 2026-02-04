"""Parser for Reddit JSON responses."""

from datetime import datetime, timezone
from typing import Dict, Any, List
from getred.models import Thread, Comment


def parse_timestamp(timestamp: float) -> str:
    """Convert Unix timestamp to ISO format string."""
    return datetime.fromtimestamp(timestamp, timezone.utc).isoformat().replace('+00:00', 'Z')


def parse_comment(comment_data: Dict[str, Any], depth: int = 0) -> Comment:
    """
    Parse a comment from Reddit JSON data.

    Args:
        comment_data: Raw comment data from Reddit API
        depth: Nesting depth of the comment

    Returns:
        Comment object with nested replies
    """
    data = comment_data.get('data', {})

    # Handle deleted/removed comments
    author = data.get('author', '[deleted]')
    body = data.get('body', '[deleted]')

    comment = Comment(
        id=data.get('id', ''),
        author=author,
        body=body,
        score=data.get('score', 0),
        created_utc=parse_timestamp(data.get('created_utc', 0)),
        depth=depth,
        replies=[]
    )

    # Parse nested replies
    replies_data = data.get('replies')
    if replies_data and isinstance(replies_data, dict):
        replies_listing = replies_data.get('data', {}).get('children', [])
        for reply_data in replies_listing:
            # Skip "more" objects that indicate additional comments
            if reply_data.get('kind') == 't1':
                comment.replies.append(parse_comment(reply_data, depth + 1))

    return comment


def parse_comments(comments_listing: List[Dict[str, Any]]) -> List[Comment]:
    """
    Parse all top-level comments from the comments listing.

    Args:
        comments_listing: List of comment objects from Reddit API

    Returns:
        List of Comment objects
    """
    comments = []
    for item in comments_listing:
        # Only parse actual comments (kind = t1), skip "more" objects
        if item.get('kind') == 't1':
            comments.append(parse_comment(item, depth=0))

    return comments


def parse_thread(json_data: List[Dict[str, Any]]) -> Thread:
    """
    Parse a Reddit thread from JSON response.

    Args:
        json_data: Raw JSON response from Reddit API (list with 2 elements)

    Returns:
        Thread object with all data and nested comments
    """
    # Reddit API returns [post_data, comments_data]
    post_listing = json_data[0]['data']['children'][0]['data']
    comments_listing = json_data[1]['data']['children']

    thread = Thread(
        id=post_listing.get('id', ''),
        title=post_listing.get('title', ''),
        author=post_listing.get('author', '[deleted]'),
        subreddit=post_listing.get('subreddit', ''),
        url=post_listing.get('url', ''),
        selftext=post_listing.get('selftext', ''),
        score=post_listing.get('score', 0),
        created_utc=parse_timestamp(post_listing.get('created_utc', 0)),
        fetched_at=datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        comment_count=post_listing.get('num_comments', 0),
        comments=parse_comments(comments_listing)
    )

    return thread
