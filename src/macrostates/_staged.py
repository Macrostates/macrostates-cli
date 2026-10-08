"""Read a Git index without executing hooks or changing the checkout."""

import os
import subprocess
from pathlib import Path

from ._integrity import MAX_EXTRACTED
from ._io import relative_path, safe_path
from ._models import MacrostatesError


def git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, check=False)
    if result.returncode:
        raise MacrostatesError(
            "Cannot inspect Git index; ensure the project is inside a Git repository"
        )
    return result.stdout


def export_index(project_root: Path, target: Path) -> Path:
    git_root = Path(
        os.fsdecode(git(project_root, "rev-parse", "--show-toplevel")).strip()
    ).resolve()
    relative_project = project_root.resolve().relative_to(git_root)
    entries = git(git_root, "ls-files", "--stage", "-z").split(b"\0")
    links: list[tuple[Path, str]] = []
    total = 0
    for entry in entries:
        if not entry:
            continue
        header, encoded_path = entry.split(b"\t", 1)
        mode, sha, stage = header.decode("ascii").split()
        if stage != "0":
            raise MacrostatesError("Git index has unresolved merge conflicts")
        if mode == "160000":
            # Submodule contents are outside this repository's staged snapshot.
            continue
        if mode not in ("100644", "100755", "120000"):
            raise MacrostatesError("Git index contains an unsupported file mode")
        name = relative_path(os.fsdecode(encoded_path), "staged path")
        destination = safe_path(target, name)
        contents = git(git_root, "cat-file", "blob", sha)
        total += len(contents)
        if total > MAX_EXTRACTED:
            raise MacrostatesError("Staged snapshot exceeds 128 MiB")
        destination.parent.mkdir(parents=True, exist_ok=True)
        if mode == "120000":
            links.append((destination, os.fsdecode(contents)))
        else:
            destination.write_bytes(contents)
            destination.chmod(0o755 if mode == "100755" else 0o644)
    # Creating links last prevents a staged link from directing writes elsewhere.
    for destination, contents in links:
        destination.symlink_to(contents)
    return target / relative_project
