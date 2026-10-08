"""Run with: uv run python examples/inspect_project.py PATH."""

import sys

from macrostates import Project

if __name__ == "__main__":
    project = Project.open(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(project.info())
    for diagnostic in project.check().diagnostics:
        print(diagnostic.code, diagnostic.message)
