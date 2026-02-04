import pytest

from click.testing import CliRunner

from getred.cli import main

from getred.fetcher import RedditFetcher

import importlib.metadata

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0
    expected_version = importlib.metadata.version("getred")
    assert expected_version in result.output

def test_user_agent_version():
    fetcher = RedditFetcher()
    ua = fetcher.headers["User-Agent"]
    expected_version = importlib.metadata.version("getred")
    assert expected_version in ua