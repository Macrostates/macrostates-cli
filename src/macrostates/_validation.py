"""Structural validation and dependency checks over normalized metadata."""

import re
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

from ._formats import read_metadata
from ._formats.common import dependencies
from ._io import read_yaml, safe_path, version
from ._models import Composition, MacrostatesError, Metadata, Report


def validate_packages(
    composition: Composition, roots: dict[str, Path]
) -> tuple[Report, dict[str, Metadata]]:
    report = Report()
    metadata: dict[str, Metadata] = {}
    selected = {package.name: package for package in composition.packages}
    for package in composition.packages:
        root = roots[package.name]
        try:
            item = read_metadata(read_yaml(safe_path(root, "package.yaml")))
            if (item.name, item.version, item.entrypoint) != (
                package.name,
                package.version,
                package.entrypoint,
            ):
                report.add(
                    "package.mismatch",
                    f"Metadata does not match selection for {package.name}",
                    package.path,
                )
            if not safe_path(root, item.entrypoint).is_file():
                report.add(
                    "entrypoint.missing", f"Missing entrypoint for {package.name}", package.path
                )
            for key, raw in package.legacy_dependencies.items():
                expected = (
                    item.dependencies if key == "dependencies" else item.optional_dependencies
                )
                if dependencies(raw, key) != expected:
                    report.add(
                        "dependency.legacy_mismatch",
                        f"Legacy dependency copies disagree for {package.name}",
                        package.path,
                    )
            metadata[package.name] = item
        except (MacrostatesError, OSError) as exc:
            report.add("package.invalid", f"{package.name}: {exc}", package.path)
    graph: dict[str, list[str]] = {}
    for name, item in metadata.items():
        graph[name] = []
        for dependency in item.dependencies + item.optional_dependencies:
            if dependency.name not in selected:
                if dependency in item.dependencies:
                    report.add("dependency.missing", f"{name} requires {dependency.name}")
                continue
            actual = version(selected[dependency.name].version)
            required = version(dependency.version)
            satisfied = (
                actual == required if dependency.constraint == "exact" else actual >= required
            )
            if dependency.constraint == "compatible":
                satisfied = satisfied and actual[0] == required[0]
            if not satisfied:
                report.add(
                    "dependency.incompatible",
                    f"{name} requires {dependency.name} {dependency.constraint} {dependency.version}; selected {selected[dependency.name].version}",
                )
            graph[name].append(dependency.name)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(name: str) -> None:
        if name in visiting:
            report.add("dependency.cycle", f"Dependency cycle contains {name}")
            return
        if name in visited:
            return
        visiting.add(name)
        for target in graph.get(name, []):
            visit(target)
        visiting.remove(name)
        visited.add(name)

    for name in graph:
        visit(name)
    return report, metadata


def check_links(root: Path, boundary: Path, report: Report) -> None:
    # This is a conservative local-link checker, not a Markdown semantic parser.
    for path in sorted(root.rglob("*.md")):
        if path.is_symlink():
            report.add(
                "path.symlink",
                "Specification documents must not be symlinks",
                path.relative_to(boundary).as_posix(),
            )
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
        targets = re.findall(r"!?\[[^\]\n]*\]\(([^\n)]*)\)", text)
        targets += re.findall(r"^\s*\[[^\]]+\]:\s*(\S+)", text, flags=re.M)
        for raw in targets:
            target = raw.strip().split(' "', 1)[0].strip("<>")
            parsed = urlsplit(target)
            if not target or parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = path.parent / unquote(parsed.path)
            if not destination.resolve().is_relative_to(boundary.resolve()):
                report.add(
                    "link.escape",
                    "Local specification link escapes the project",
                    path.relative_to(boundary).as_posix(),
                )
            elif not destination.exists():
                report.add(
                    "link.missing",
                    f"Missing local link target: {parsed.path}",
                    path.relative_to(boundary).as_posix(),
                )


class Process23Policy:
    """Process 2.3.x declaration policy; earlier releases retain their own rules."""

    def check(self, composition: Composition, implementation: Path, report: Report) -> None:
        declared = composition.raw["project"].get("version")
        if not isinstance(declared, str) or not declared.startswith("spec-"):
            report.add(
                "process.spec_version",
                "Process 2.3 requires project.version: spec-MAJOR.MINOR.REVISION",
            )
            return
        try:
            spec = version(declared.removeprefix("spec-"))
            release = safe_path(implementation, "release.yaml")
            if not release.exists():
                overview = safe_path(implementation, "main.md")
                if overview.is_file() and re.search(
                    r"(?im)^\s*project phase:\s*active\b", overview.read_text()
                ):
                    report.add(
                        "process.release_missing", "Active implementation has no release.yaml"
                    )
                return
            data = read_yaml(release)
            current = version(data.get("version"))
            baseline_text = data.get("specification")
            if not isinstance(baseline_text, str) or not baseline_text.startswith("spec-"):
                raise MacrostatesError("release.specification must be spec-MAJOR.MINOR.REVISION")
            baseline = version(baseline_text.removeprefix("spec-"))
            stamp = data.get("release_date")
            if not isinstance(stamp, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
                raise MacrostatesError("release_date must be YYYY-MM-DD")
            date.fromisoformat(stamp)
            if current[:2] != baseline[:2] or current[:2] != spec[:2]:
                report.add(
                    "process.version_alignment",
                    "Composition, implementation and baseline Major.Minor differ",
                )
            if baseline[:2] == spec[:2] and baseline[2] > spec[2]:
                report.add(
                    "process.future_baseline",
                    "Implementation references a later specification revision",
                )
        except (MacrostatesError, ValueError, OSError) as exc:
            report.add("process.release_invalid", str(exc))


def check_process(composition: Composition, implementation: Path, report: Report) -> None:
    process = next((package for package in composition.packages if package.name == "process"), None)
    if process is None:
        return
    selected = version(process.version)
    if selected[0] == 1 or (selected[0] == 2 and selected[1] < 3):
        return
    if selected[:2] == (2, 3):
        Process23Policy().check(composition, implementation, report)
    else:
        report.add(
            "process.unsupported_policy", f"No process-policy adapter for Process {process.version}"
        )
