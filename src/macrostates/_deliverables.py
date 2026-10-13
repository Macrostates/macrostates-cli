"""Optional application policies, independent of repository baseline numbering."""

from pathlib import Path
from typing import Any

from ._io import mapping, parse_yaml, read_yaml, safe_path, string
from ._models import MacrostatesError, Report
from ._versioning import COMMIT_ID, baseline, baselines, calendar_date, identifier


def _entries(data: dict[str, Any], default_implementation: str | None) -> dict[str, dict[str, Any]]:
    if data.get("schema_version") != 1 or isinstance(data.get("schema_version"), bool):
        raise MacrostatesError("Deliverable policies require schema_version: 1")
    entries = mapping(data.get("deliverables"), "deliverables")
    result = {}
    for name, value in entries.items():
        identifier(name, "deliverable id")
        entry = dict(mapping(value, "deliverable"))
        strategy = entry.get("strategy", "implementation")
        if strategy not in {"implementation", "independent"}:
            raise MacrostatesError("Deliverable strategy must be implementation or independent")
        entry["strategy"] = strategy
        implementation = entry.get("implementation", default_implementation)
        if implementation is not None:
            baseline(implementation, "implementation")
        specification = entry.get("specification")
        if specification is not None:
            spec = baseline(specification, "specification")
            if implementation is None or spec[:2] != baseline(implementation, "implementation")[:2]:
                raise MacrostatesError("Deliverable provenance contract Major.Minor is not aligned")
        if strategy == "implementation":
            selected = implementation.removeprefix("imp-") if implementation else None
            if entry.get("version") is not None and entry["version"] != selected:
                raise MacrostatesError(
                    "Implementation-derived deliverables must not declare a competing version"
                )
            entry["version"] = selected
        else:
            string(entry.get("version"), "independent deliverable version")
        if "release_date" in entry:
            calendar_date(entry["release_date"])
            if specification is None or entry.get("implementation") is None:
                raise MacrostatesError(
                    "Application release metadata needs exact specification and implementation provenance"
                )
        if "source" in entry:
            source = mapping(entry["source"], "deliverable.source")
            if "commit" not in source and "tag" not in source:
                raise MacrostatesError(
                    "Application source needs an exact commit or immutable release tag"
                )
            if "commit" in source and not COMMIT_ID.fullmatch(
                string(source["commit"], "source.commit")
            ):
                raise MacrostatesError("Application source.commit must be a full Git identity")
            if "tag" in source:
                from ._git import ref

                ref(string(source["tag"], "source.tag"))
        if "android" in entry:
            android = mapping(entry["android"], "android")
            code = android.get("version_code")
            if (
                isinstance(code, bool)
                or not isinstance(code, int)
                or not 1 <= code <= 2_100_000_000
            ):
                raise MacrostatesError(
                    "Android version_code must be an integer from 1 through 2100000000"
                )
        result[name] = entry
    return result


def inspect_deliverables(root: Path) -> dict[str, dict[str, Any]]:
    path = safe_path(root, ".macrostates/implementation/deliverables.yaml")
    if not path.exists():
        return {}
    return _entries(read_yaml(path), baselines(root)["implementation"])


def check_deliverables(root: Path) -> Report:
    report = Report()
    try:
        inspect_deliverables(root)
    except (MacrostatesError, OSError) as exc:
        report.add("deliverable.invalid", str(exc))
    return report


def check_deliverable_changes(
    root: Path, target: str, *, repository_root: Path | None = None
) -> Report:
    """Check declared Android application ordering, without allocating counters."""
    from ._git import git

    report = check_deliverables(root)
    if not report.ok:
        return report
    current = inspect_deliverables(root)
    repository_root = root if repository_root is None else repository_root
    try:
        previous_data = parse_yaml(
            git(repository_root, "show", target + ":.macrostates/implementation/deliverables.yaml")
        )
    except MacrostatesError:
        return report
    try:
        previous_release = parse_yaml(
            git(repository_root, "show", target + ":.macrostates/implementation/release.yaml")
        )
        previous_implementation = previous_release.get("version")
        if isinstance(previous_implementation, str) and not previous_implementation.startswith(
            "imp-"
        ):
            previous_implementation = "imp-" + previous_implementation
        previous = _entries(previous_data, previous_implementation)
    except MacrostatesError as exc:
        report.add("deliverable.previous_invalid", str(exc))
        return report
    for name, entry in current.items():
        prior = previous.get(name)
        if prior and "android" in entry and "android" in prior:
            new_code, old_code = entry["android"]["version_code"], prior["android"]["version_code"]
            new_release = any(
                entry.get(field) != prior.get(field)
                for field in (
                    "version",
                    "implementation",
                    "specification",
                    "source",
                    "release_date",
                )
            )
            if new_code < old_code or (new_release and new_code <= old_code):
                report.add(
                    "deliverable.android_order",
                    f"{name}: a new application release needs a higher versionCode",
                )
    return report


def check_deliverable_publication(root: Path) -> Report:
    """Verify declared release source references; application publication remains external."""
    from ._git import commit, git

    report = check_deliverables(root)
    if not report.ok:
        return report
    for name, entry in inspect_deliverables(root).items():
        if "release_date" not in entry:
            continue
        source = entry.get("source")
        if not source:
            report.add(
                "deliverable.source_missing",
                f"{name}: release source identity must be recorded before publication",
            )
            continue
        try:
            resolved = None
            if source.get("tag"):
                selected = "refs/tags/" + source["tag"].removeprefix("refs/tags/")
                if git(root, "cat-file", "-t", selected) != "tag":
                    raise MacrostatesError("Application source tag must be annotated")
                resolved = commit(root, selected)
            if source.get("commit"):
                recorded = commit(root, source["commit"])
                if resolved is not None and resolved != recorded:
                    raise MacrostatesError("Application source tag and recorded commit disagree")
                resolved = recorded
            if resolved is not None:
                try:
                    tagged = parse_yaml(
                        git(
                            root,
                            "show",
                            resolved + ":.macrostates/implementation/deliverables.yaml",
                        )
                    )
                except MacrostatesError:
                    report.add(
                        "deliverable.artifact_review",
                        f"{name}: source reference resolves; verify application metadata using its declared release tooling",
                        warning=True,
                    )
                else:
                    tagged_specification = None
                    try:
                        tagged_release = parse_yaml(
                            git(
                                root, "show", resolved + ":.macrostates/implementation/release.yaml"
                            )
                        )
                        tagged_implementation = tagged_release.get("version")
                        if isinstance(
                            tagged_implementation, str
                        ) and not tagged_implementation.startswith("imp-"):
                            tagged_implementation = "imp-" + tagged_implementation
                        tagged_specification = tagged_release.get("specification")
                        if isinstance(
                            tagged_specification, str
                        ) and tagged_specification.startswith("spec-"):
                            tagged_specification = "specs-" + tagged_specification.removeprefix(
                                "spec-"
                            )
                    except MacrostatesError:
                        tagged_implementation = None
                    actual = _entries(tagged, tagged_implementation).get(name)
                    if not isinstance(actual, dict):
                        raise MacrostatesError(
                            "Application source snapshot does not contain the declared deliverable"
                        )
                    if tagged_implementation is not None and (
                        entry.get("implementation") != tagged_implementation
                        or entry.get("specification") != tagged_specification
                    ):
                        raise MacrostatesError(
                            "Application receipt does not reference the source snapshot's implementation baseline"
                        )
                    for field in ("implementation", "specification", "release_date", "android"):
                        if actual.get(field) != entry.get(field):
                            raise MacrostatesError(
                                "Application source snapshot provenance differs from the release declaration"
                            )
                    if (
                        actual.get("strategy") != entry["strategy"]
                        or actual.get("version") != entry["version"]
                    ):
                        raise MacrostatesError(
                            "Application source snapshot version differs from the release declaration"
                        )
        except MacrostatesError as exc:
            report.add("deliverable.source_invalid", f"{name}: {exc}")
    return report
