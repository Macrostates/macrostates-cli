"""The public API. Imports perform no network or project-local file access."""

from importlib.metadata import PackageNotFoundError, version

from ._models import Diagnostic, MacrostatesError, Report
from ._project import Project
from ._sources import GitHubSource, SourceProvider

__all__ = ["Diagnostic", "GitHubSource", "MacrostatesError", "Project", "Report", "SourceProvider"]


def __getattr__(name: str) -> str:
    if name != "__version__":
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    # Read distribution metadata only when a caller explicitly requests a version.
    try:
        return version("macrostates-cli")
    except PackageNotFoundError:
        return "0+uninstalled"


def __dir__() -> list[str]:
    return sorted([*globals(), "__version__"])
