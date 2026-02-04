"""getred - A CLI tool to fetch Reddit threads and save them as structured JSON."""

import importlib.metadata

__version__ = importlib.metadata.version("getred")

from getred.models import Thread, Comment

__all__ = ["Thread", "Comment", "__version__"]
