"""File transactions. Ordinary failures roll back; interrupted recovery is explicit."""

import shutil
from pathlib import Path

from ._models import MacrostatesError


def replace_paths(
    replacements: dict[Path, Path], workspace: Path, *, allow_existing: bool = True
) -> None:
    """Move prepared files/directories into place, retaining recoverable backups."""
    backups = workspace / "backups"
    backups.mkdir()
    applied: list[tuple[Path, Path, bool]] = []
    created_parents: list[Path] = []
    try:
        for number, (destination, prepared) in enumerate(replacements.items()):
            if not allow_existing and (destination.exists() or destination.is_symlink()):
                raise MacrostatesError(
                    "A destination appeared during initialization; it was preserved"
                )
            pending: list[Path] = []
            parent = destination.parent
            while not parent.exists():
                pending.append(parent)
                parent = parent.parent
            for parent in reversed(pending):
                parent.mkdir()
                created_parents.append(parent)
            backup = backups / str(number)
            existed = destination.exists()
            if existed:
                destination.rename(backup)
            applied.append((destination, backup, existed))
            prepared.rename(destination)
    except BaseException:
        try:
            for destination, backup, existed in reversed(applied):
                if destination.exists():
                    if destination.is_dir():
                        shutil.rmtree(destination)
                    else:
                        destination.unlink()
                if existed:
                    backup.rename(destination)
            for parent in reversed(created_parents):
                parent.rmdir()
        except OSError as recovery_error:
            raise MacrostatesError(
                f"Rollback failed; recovery files retained in {workspace}"
            ) from recovery_error
        raise
