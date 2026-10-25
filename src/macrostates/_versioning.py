"""Process 5 baseline declarations and honest, computed source identities."""

import re
from datetime import date
from pathlib import Path
from typing import Any, Literal

from ._io import mapping, read_yaml, safe_path, string, version
from ._models import MacrostatesError

Kind = Literal["specification", "implementation"]
PREFIXES = {"specification": "specs-", "implementation": "imp-"}
IMPACTS = ("none", "patch", "minor", "major")
IDENTIFIER = re.compile(r"[a-z0-9]+(?:[._-][a-z0-9]+)*\Z", flags=re.ASCII)
COMMIT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z", flags=re.ASCII)


def identifier(value: Any, label: str = "id") -> str:
    text = string(value, label)
    if not IDENTIFIER.fullmatch(text) or len(text) > 128:
        raise MacrostatesError(f"{label} must be a safe lowercase ASCII identifier")
    return text


def baseline(value: Any, kind: Kind) -> tuple[int, int, int]:
    text = string(value, kind)
    prefix = PREFIXES[kind]
    if not text.startswith(prefix):
        raise MacrostatesError(f"{kind} must be {prefix}MAJOR.MINOR.PATCH")
    return version(text.removeprefix(prefix))


def baseline_text(numbers: tuple[int, int, int], kind: Kind) -> str:
    return PREFIXES[kind] + ".".join(str(number) for number in numbers)


def calendar_date(value: Any) -> str:
    text = string(value, "release_date")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        raise MacrostatesError("release_date must be YYYY-MM-DD")
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise MacrostatesError("release_date must be a valid calendar date") from exc
    return text


def composition_path(root: Path) -> Path:
    directory = safe_path(root, ".macrostates/specs")
    found = [safe_path(directory, name) for name in ("composition.yaml", "composition.yml")]
    found = [path for path in found if path.exists()]
    if len(found) != 1:
        raise MacrostatesError("Process 5 needs one modern composition manifest")
    return found[0]


def declarations(root: Path) -> dict[str, Any]:
    """Read authoritative finalized/candidate numbers, never infer source readiness."""
    from ._validation import process_uses_prefixed_baselines

    manifest = composition_path(root)
    composition = read_yaml(manifest)
    packages = composition.get("packages")
    if not isinstance(packages, list):
        raise MacrostatesError("composition.packages must be a list")
    process = next(
        (item for item in packages if isinstance(item, dict) and item.get("name") == "process"),
        None,
    )
    if process is None or not process_uses_prefixed_baselines(
        string(process.get("version"), "process.version")
    ):
        raise MacrostatesError("This operation requires a supported Process 5.0, 5.1 or 6.0 policy")
    project = mapping(composition.get("project"), "composition.project")
    specification = string(project.get("version"), "project.version")
    spec_numbers = baseline(specification, "specification")
    release_path = safe_path(root, ".macrostates/implementation/release.yaml")
    release = read_yaml(release_path) if release_path.exists() else None
    implementation = None
    implementation_specification = None
    if release is not None:
        if release.get("schema_version") != 2 or isinstance(release.get("schema_version"), bool):
            raise MacrostatesError("Process 5 release declaration needs schema_version: 2")
        implementation = string(release.get("version"), "release.version")
        imp_numbers = baseline(implementation, "implementation")
        implementation_specification = string(release.get("specification"), "release.specification")
        implemented_spec = baseline(implementation_specification, "specification")
        calendar_date(release.get("release_date"))
        if imp_numbers[:2] != spec_numbers[:2] or imp_numbers[:2] != implemented_spec[:2]:
            raise MacrostatesError("Specification and implementation contract Major.Minor differ")
        if implemented_spec[2] > spec_numbers[2]:
            raise MacrostatesError("Implementation references a later specification patch")
    return {
        "specification": specification,
        "implementation": implementation,
        "implementation_specification": implementation_specification,
        "composition": composition,
        "manifest": manifest,
        "release": release,
        "release_path": release_path,
    }


def baselines(root: Path) -> dict[str, str | None]:
    """Validate Process 5 declarations and return their persisted baseline references."""
    current = declarations(root)
    return {
        key: current[key]
        for key in ("specification", "implementation", "implementation_specification")
    }


def aggregate(
    specification: str, implementation: str | None, impacts: list[dict[str, str]]
) -> dict[str, str | None]:
    """Aggregate a coherent release once; independent patches remain independent."""
    spec = baseline(specification, "specification")
    imp = baseline(implementation, "implementation") if implementation is not None else None
    for impact in impacts:
        if set(impact) != {"specification", "implementation"} or any(
            item not in IMPACTS for item in impact.values()
        ):
            raise MacrostatesError("Change impact must declare both supported impact values")
        if imp is None and impact["implementation"] != "none":
            raise MacrostatesError("Cannot finalize implementation changes without a baseline")
    highest = max((IMPACTS.index(value) for item in impacts for value in item.values()), default=0)
    if highest >= IMPACTS.index("minor"):
        contract = (spec[0] + 1, 0, 0) if highest == 3 else (spec[0], spec[1] + 1, 0)
        spec = contract
        if imp is not None:
            imp = contract
    else:
        if any(item["specification"] == "patch" for item in impacts):
            spec = (*spec[:2], spec[2] + 1)
        if imp is not None and any(item["implementation"] == "patch" for item in impacts):
            imp = (*imp[:2], imp[2] + 1)
    return {
        "specification": baseline_text(spec, "specification"),
        "implementation": baseline_text(imp, "implementation") if imp is not None else None,
    }


def _sanitized_branch(name: str) -> str:
    value = re.sub(r"[^a-z0-9._-]+", "-", name.lower(), flags=re.ASCII).strip(".-_")
    return value[:80] or "detached"


def identity(root: Path, work: str | None = None) -> dict[str, Any]:
    """Describe source identity without allocating numbers or modifying declarations."""
    from ._changes import load_changes, load_work
    from ._git import branch, commit, git

    current = declarations(root)
    pending = load_changes(root)
    selected = None
    if work is not None:
        identifier(work, "work")
        all_changes = {**load_changes(root, history=True), **pending, **load_work(root)}
        if work not in all_changes:
            raise MacrostatesError("Chosen work/change record does not exist")
        selected = all_changes[work]
    bases = {
        "specification": current["specification"],
        "implementation": current["implementation"],
    }
    if selected is not None:
        bases = {key: selected["origin"][key] for key in bases}
    plan_path = safe_path(root, ".macrostates/implementation/release-plan.yaml")
    candidate = plan_path.exists() and read_yaml(plan_path).get("status") == "candidate"
    result: dict[str, Any] = {
        "state": "unavailable",
        "specification": None,
        "implementation": None,
        "baselines": bases,
        "commit": None,
        "branch": None,
        "dirty": None,
        "work": work,
        "pending_changes": sorted(pending),
    }
    try:
        git_root = Path(git(root, "rev-parse", "--show-toplevel")).resolve()
        if git_root != root.resolve():
            result["message"] = (
                "Computed baseline identity requires a composition at its Git repository root; "
                "nested independent compositions retain their metadata for manual inspection."
            )
            return result
        source_commit = commit(root)
        dirty = bool(git(root, "status", "--porcelain"))
    except MacrostatesError:
        return result
    try:
        source_branch = branch(root)
    except MacrostatesError:
        source_branch = "detached"
    result.update(commit=source_commit, branch=source_branch, dirty=dirty)
    suffix = f"unreleased.g{source_commit[:12]}"
    result["state"] = "unreleased"
    if selected is not None:
        suffix = f"branch.{_sanitized_branch(source_branch)}.g{source_commit[:12]}"
        result["state"] = "development"
    elif candidate and not pending:
        suffix = f"candidate.g{source_commit[:12]}"
        result["state"] = "candidate"
    if selected is None and not pending and not dirty:
        # Exact annotated baselines and verified integrated candidates establish
        # finalization. Unrecorded later runtime changes remain unreleased.
        decisive = bases["implementation"] or bases["specification"]
        try:
            finalized = (
                git(root, "cat-file", "-t", f"refs/tags/{decisive}").strip() == "tag"
                and commit(root, f"refs/tags/{decisive}") == source_commit
            )
        except MacrostatesError:
            finalized = False
        if not finalized and candidate:
            from ._git import primary_ref
            from ._release import _check_candidate_delta, candidate_integrated

            plan = read_yaml(plan_path)
            targets = [plan.get("integration_ref")]
            try:
                targets.append(primary_ref(root))
            except MacrostatesError:
                pass
            for target in targets:
                if not isinstance(target, str) or not candidate_integrated(
                    root, plan, target=target
                ):
                    continue
                suffix = f"unreleased.g{source_commit[:12]}"
                result["state"] = "unreleased"
                try:
                    _check_candidate_delta(root, plan, current)
                    git(
                        root,
                        "merge-base",
                        "--is-ancestor",
                        source_commit,
                        commit(root, target),
                    )
                    finalized = True
                    break
                except MacrostatesError:
                    pass
        if finalized:
            suffix = ""
            result["state"] = "finalized"
    if dirty:
        suffix += ".dirty"
    for key, declared in bases.items():
        result[key] = f"{declared}-{suffix}" if declared is not None and suffix else declared
    return result
