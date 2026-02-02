"""getred - A CLI tool to fetch Reddit threads and save them as structured JSON."""

__version__ = "0.1.0"

from getred.models import Thread, Comment

__all__ = ["Thread", "Comment", "__version__"]
