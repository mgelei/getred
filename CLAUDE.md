# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`getred` is a CLI tool that fetches Reddit threads and saves them as structured JSON files. It uses Reddit's public JSON API (no authentication required) to retrieve thread data including all nested comments.

## Development Commands

### Installation
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

### Running the CLI
```bash
# After installation
getred <reddit_url>

# Or directly via Python module
python -m getred <reddit_url>

# Common options
getred <url> -o /path/to/output.json  # Custom output path
getred <url> --no-pretty              # Compact JSON output
getred <url> -q                       # Quiet mode
```

## Architecture

### Data Flow
1. **CLI Layer** (`cli.py`): Handles command-line arguments and orchestrates the fetch-parse-save pipeline
2. **Fetcher** (`fetcher.py`): HTTP client that requests Reddit's `.json` endpoint using httpx
3. **Parser** (`parser.py`): Converts Reddit's JSON response into structured `Thread` and `Comment` models
4. **Models** (`models.py`): Dataclass definitions with `to_dict()` methods for serialization
5. **Utils** (`utils.py`): URL validation, slug generation, and file I/O helpers

### Key Design Patterns

**Reddit API Response Structure**: The API returns a 2-element list:
- `json_data[0]`: Post/thread data (single item listing)
- `json_data[1]`: Comments data (listing with nested replies)

**Comment Nesting**: Comments are recursively parsed with `depth` tracking. Each comment has a `replies` list containing nested `Comment` objects. The parser handles Reddit's "more" objects (kind='more') by skipping them - these indicate additional comments not included in the initial response.

**Output Format**: By default, files are saved to `~/Downloads/<thread_id>_<title_slug>.json` with pretty-printed JSON. Thread metadata includes `fetched_at` timestamp in ISO format.

## Project Structure
- `src/getred/`: Main package
  - `models.py`: Thread and Comment dataclasses
  - `fetcher.py`: RedditFetcher class (httpx-based HTTP client)
  - `parser.py`: Recursive comment parsing logic
  - `cli.py`: Click-based CLI entry point
  - `utils.py`: URL validation, slug generation, file operations
  - `__main__.py`: Module entry point for `python -m getred`
