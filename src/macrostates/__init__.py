"""The supported Macrostates Python API. Importing this package performs no I/O."""

from ._models import Diagnostic, MacrostatesError, Report
from ._project import Project
from ._sources import GitHubSource, SourceProvider

__all__ = ["Diagnostic", "GitHubSource", "MacrostatesError", "Project", "Report", "SourceProvider"]
__version__ = "0.1.0"
