"""Hosting-independent Git operations bound to explicit repository state."""

import os
import re
import subprocess
from pathlib import Path

from ._models import MacrostatesError


def ref(value: str) -> str:
    if not isinstance(value, str) or not value or value.startswith("-"):
        raise MacrostatesError("Git references must be explicit, non-option identifiers")
    if any(ord(char) < 33 or ord(char) == 127 for char in value):
        raise MacrostatesError("Git references must not contain whitespace or control characters")
    return value


def git(root: Path, *args: str) -> str:
    """Run an argument-vector Git operation; never expose credential-bearing stderr."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            timeout=120,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            check=False,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise MacrostatesError("Git is unavailable or the operation did not complete") from exc
    if result.returncode:
        operation = args[0] if args else "inspection"
        raise MacrostatesError(f"Git {operation} failed; inspect repository access and state")
    return result.stdout.strip()


def commit(root: Path, selected: str = "HEAD") -> str:
    selected = ref(selected)
    result = git(root, "rev-parse", "--verify", "--end-of-options", selected + "^{commit}")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", result):
        raise MacrostatesError("Git returned an invalid commit identity")
    return result


def branch(root: Path) -> str:
    try:
        return git(root, "symbolic-ref", "--quiet", "--short", "HEAD")
    except MacrostatesError as exc:
        raise MacrostatesError("This operation requires an attached development branch") from exc


def dirty(root: Path) -> bool:
    return bool(git(root, "status", "--porcelain", "--untracked-files=normal"))


def primary_branch(root: Path) -> str:
    """Use explicit local configuration, remote default, or an unambiguous local default."""
    try:
        configured = git(root, "config", "--get", "macrostates.primaryBranch")
    except MacrostatesError:
        configured = None
    if configured is not None:
        return primary_name(configured)
    try:
        selected = git(root, "symbolic-ref", "refs/remotes/origin/HEAD")
        return ref(selected.removeprefix("refs/remotes/origin/"))
    except MacrostatesError:
        pass
    found = []
    for name in ("main", "master"):
        try:
            commit(root, "refs/heads/" + name)
            found.append(name)
        except MacrostatesError:
            pass
    if len(found) == 1:
        return found[0]
    if not found:
        remote_names = {
            match[1]
            for value in git(
                root, "for-each-ref", "--format=%(refname)", "refs/remotes"
            ).splitlines()
            if (match := re.fullmatch(r"refs/remotes/[^/]+/(main|master)", value))
        }
        if len(remote_names) == 1:
            return remote_names.pop()
    raise MacrostatesError(
        "Configure macrostates.primaryBranch or supply the primary branch explicitly"
    )


def primary_name(value: str) -> str:
    value = ref(value).removeprefix("refs/heads/")
    if value.startswith("refs/"):
        raise MacrostatesError(
            "The primary branch must be a local branch name or refs/heads reference"
        )
    return value


def primary_ref(root: Path) -> str:
    """Resolve the primary branch in a normal checkout or a detached CI checkout."""
    name = primary_branch(root)
    for value in ("refs/heads/" + name, "refs/remotes/origin/" + name):
        try:
            commit(root, value)
            return value
        except MacrostatesError:
            pass
    found = [
        value
        for value in git(root, "for-each-ref", "--format=%(refname)", "refs/remotes").splitlines()
        if value.endswith("/" + name)
    ]
    if len(found) == 1:
        return found[0]
    raise MacrostatesError("Select an explicit integration target reference")


def ensure_development(root: Path, primary: str | None = None, *, clean: bool = True) -> None:
    """Guard mutations; synchronization additionally requires a clean starting tree."""
    guarded = {primary_name(primary)} if primary is not None else set()
    try:
        guarded.add(primary_branch(root))
    except MacrostatesError:
        if primary is None:
            raise
    if branch(root) in guarded:
        raise MacrostatesError("Author changes on a development branch, not the primary branch")
    for name in ("MERGE_HEAD", "REBASE_HEAD", "CHERRY_PICK_HEAD", "rebase-merge", "rebase-apply"):
        path = Path(git(root, "rev-parse", "--git-path", name))
        if not path.is_absolute():
            path = root / path
        if path.exists():
            raise MacrostatesError("Resolve or explicitly abort the existing Git operation first")
    if clean and dirty(root):
        raise MacrostatesError("Commit or preserve local changes before this Git operation")
