"""Explicit fetch and branch synchronization; never automate conflict resolution."""

from pathlib import Path
from typing import Any

from ._git import branch, commit, ensure_development, git, primary_ref, ref
from ._models import MacrostatesError


def branch_status(root: Path, *, target: str | None = None) -> dict[str, Any]:
    target = ref(target) if target is not None else primary_ref(root)
    current, upstream = commit(root), commit(root, target)
    ahead, behind = map(
        int, git(root, "rev-list", "--left-right", "--count", current + "..." + upstream).split()
    )
    try:
        current_branch = branch(root)
    except MacrostatesError:
        current_branch = "detached"
    return {
        "branch": current_branch,
        "commit": current,
        "target": target,
        "target_commit": upstream,
        "ahead": ahead,
        "behind": behind,
        "remote_freshness": "cached; no fetch performed",
    }


def synchronize(
    root: Path,
    *,
    target: str,
    strategy: str,
    primary: str | None = None,
    fetch_remote: str | None = None,
) -> dict[str, Any]:
    ensure_development(root, primary)
    if strategy not in {"merge", "rebase"}:
        raise MacrostatesError("Select the project's merge or rebase synchronization strategy")
    if fetch_remote is not None:
        remote = ref(fetch_remote)
        if remote not in git(root, "remote").splitlines():
            raise MacrostatesError("Fetch requires an explicitly configured remote name")
        git(root, "fetch", "--no-tags", remote)
    selected = commit(root, ref(target))
    before = commit(root)
    try:
        git(root, strategy, selected)
    except MacrostatesError as exc:
        raise MacrostatesError(
            "Synchronization did not complete. Inspect and resolve conflicts on this branch; local changes were not discarded and no force push was performed"
        ) from exc
    result = branch_status(root, target=target)
    result.update(
        {
            "previous_commit": before,
            "strategy": strategy,
            "message": "Original change provenance is retained; reassess requirements, evidence and release plans.",
        }
    )
    if fetch_remote is not None:
        result["remote_freshness"] = "fetched configured remote before synchronization"
    return result
