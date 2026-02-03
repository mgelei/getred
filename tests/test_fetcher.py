"""Tests for RedditFetcher URL handling and redirect safety."""

import httpx
import pytest

from getred.fetcher import RedditFetcher


def test_fetch_thread_preserves_query_params():
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(200, json=[{"ok": True}], request=request)

    fetcher = RedditFetcher(transport=httpx.MockTransport(handler))

    url = "https://www.reddit.com/r/python/comments/abc123/cool_title/?sort=top"
    data = fetcher.fetch_thread(url)

    assert data == [{"ok": True}]
    assert seen_urls == [
        "https://www.reddit.com/r/python/comments/abc123/cool_title/.json?sort=top"
    ]


def test_fetch_thread_does_not_double_append_json():
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(200, json={"ok": True}, request=request)

    fetcher = RedditFetcher(transport=httpx.MockTransport(handler))

    url = "https://www.reddit.com/r/python/comments/abc123/cool_title/.json?sort=top"
    data = fetcher.fetch_thread(url)

    assert data == {"ok": True}
    assert seen_urls == [url]


@pytest.mark.parametrize(
    ("input_url", "expected_json_url"),
    [
        (
            "https://www.reddit.com/r/python/comments/abc123/cool_title/",
            "https://www.reddit.com/r/python/comments/abc123/cool_title/.json",
        ),
        (
            "https://www.reddit.com/r/python/comments/abc123/cool_title",
            "https://www.reddit.com/r/python/comments/abc123/cool_title.json",
        ),
    ],
)
def test_fetch_thread_trailing_slash_variants(input_url: str, expected_json_url: str):
    seen_urls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        return httpx.Response(200, json={"ok": True}, request=request)

    fetcher = RedditFetcher(transport=httpx.MockTransport(handler))
    assert fetcher.fetch_thread(input_url) == {"ok": True}
    assert seen_urls == [expected_json_url]


def test_fetch_thread_follows_redirects():
    seen_urls: list[str] = []

    redirected_to = (
        "https://www.reddit.com/r/python/comments/abc123/cool_title/.json?sort=top"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        seen_urls.append(str(request.url))
        if len(seen_urls) == 1:
            return httpx.Response(
                302,
                headers={"Location": redirected_to},
                request=request,
            )
        return httpx.Response(200, json={"ok": True}, request=request)

    fetcher = RedditFetcher(transport=httpx.MockTransport(handler))

    url = "https://reddit.com/r/python/comments/abc123/cool_title/?sort=top"
    data = fetcher.fetch_thread(url)

    assert data == {"ok": True}
    assert seen_urls == [
        "https://reddit.com/r/python/comments/abc123/cool_title/.json?sort=top",
        redirected_to,
    ]


def test_fetch_thread_non_json_body_raises_clear_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            headers={"Content-Type": "text/html"},
            content=b"<html>not json</html>",
            request=request,
        )

    fetcher = RedditFetcher(transport=httpx.MockTransport(handler))

    url = "https://www.reddit.com/r/python/comments/abc123/cool_title/"
    with pytest.raises(ValueError) as excinfo:
        fetcher.fetch_thread(url)

    message = str(excinfo.value)
    assert "Non-JSON response" in message
    assert "content_type=text/html" in message

