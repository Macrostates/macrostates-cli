"""Find directory specifications without crossing independent compositions."""

from pathlib import Path

from ._io import safe_path

IGNORED = {".git", ".venv", "node_modules", "dist", "build", "tmp", "__pycache__"}


def directory_scopes(root: Path, specs: Path) -> list[tuple[Path, Path]]:
    relative = ".macrostates/specs" if specs.parent.name == ".macrostates" else "specs"
    result = []
    for directory, children, _ in root.walk(follow_symlinks=False):
        children[:] = sorted(
            name for name in children if name not in IGNORED and not name.startswith(".")
        )
        if "specs" in children:
            # Specification resources cannot establish implementation scopes.
            children.remove("specs")
        if directory == root:
            continue
        local = safe_path(directory, relative)
        if any(
            (safe_path(directory, location) / name).exists()
            for location in (".macrostates/specs", "specs")
            for name in ("composition.yaml", "composition.yml")
        ):
            # This is a separately composed context; its own checks cover internals.
            children.clear()
            continue
        entrypoint = safe_path(local, "main.md")
        if entrypoint.is_file():
            result.append((directory, local))
    return result
