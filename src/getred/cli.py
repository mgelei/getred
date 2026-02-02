"""Command-line interface for getred."""

import sys
import click
from pathlib import Path
from getred import __version__
from getred.fetcher import RedditFetcher
from getred.parser import parse_thread
from getred.utils import validate_reddit_url, get_default_output_path, save_json


@click.command()
@click.argument('url')
@click.option(
    '-o', '--output',
    type=click.Path(path_type=Path),
    help='Custom output path (default: ~/Downloads/<slug>.json)'
)
@click.option(
    '-p', '--pretty/--no-pretty',
    default=True,
    help='Pretty-print JSON (default: enabled)'
)
@click.option(
    '-q', '--quiet',
    is_flag=True,
    help='Suppress progress output'
)
@click.version_option(version=__version__, prog_name='getred')
def main(url: str, output: Path, pretty: bool, quiet: bool):
    """
    Fetch a Reddit thread and save it as structured JSON.

    URL should be a full Reddit thread URL like:
    https://www.reddit.com/r/python/comments/abc123/title/
    """
    # Validate URL
    if not validate_reddit_url(url):
        click.echo("Error: Invalid Reddit thread URL", err=True)
        click.echo("Expected format: https://www.reddit.com/r/SUBREDDIT/comments/ID/TITLE/", err=True)
        sys.exit(1)

    # Determine output path
    output_path = output if output else get_default_output_path(url)

    if not quiet:
        click.echo(f"Fetching thread from Reddit...")

    try:
        # Fetch thread data
        fetcher = RedditFetcher()
        json_data = fetcher.fetch_thread(url)

        if not quiet:
            click.echo(f"Parsing comments...")

        # Parse into structured format
        thread = parse_thread(json_data)

        if not quiet:
            click.echo(f"Found {thread.comment_count} comments (parsed {len(thread.comments)} top-level)")

        # Save to file
        save_json(thread.to_dict(), output_path, pretty=pretty)

        if not quiet:
            click.echo(f"✓ Saved to: {output_path}")
        else:
            click.echo(str(output_path))

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
