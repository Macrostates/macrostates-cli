"""Explicit impact records and evidence, separate from workflow lifecycle."""

import copy
import hashlib
from pathlib import Path
from typing import Any

from ._io import dump_yaml, mapping, parse_yaml, read_yaml, safe_path, string, version
from ._models import MacrostatesError, Report
from ._versioning import COMMIT_ID, IMPACTS, baseline, declarations, identifier


def changes_path(root: Path) -> Path:
    return safe_path(root, ".macrostates/implementation/changes")


def _strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise MacrostatesError(f"{label} must be an explicit list")
    return [string(item, label) for item in value]


def _validate_origin(value: Any) -> None:
    origin = mapping(value, "origin")
    if not isinstance(origin.get("commit"), str) or not COMMIT_ID.fullmatch(origin["commit"]):
        raise MacrostatesError("origin.commit must be a full lowercase Git commit ID")
    spec = baseline(origin.get("specification"), "specification")
    if "implementation" not in origin:
        raise MacrostatesError("origin.implementation must be explicit, including null")
    if origin["implementation"] is not None:
        imp = baseline(origin["implementation"], "implementation")
        if imp[:2] != spec[:2]:
            raise MacrostatesError("Original specification and implementation contracts differ")


def validate_record(data: dict[str, Any], *, expected_id: str | None = None) -> None:
    if data.get("schema_version") != 1 or isinstance(data.get("schema_version"), bool):
        raise MacrostatesError("Change records need schema_version: 1")
    record_id = identifier(data.get("id"))
    if expected_id is not None and record_id != expected_id:
        raise MacrostatesError("Change record id must match its filename")
    string(data.get("summary"), "summary")
    _validate_origin(data.get("origin"))
    if "work" in data:
        identifier(data["work"], "work")
    impact = mapping(data.get("impact"), "impact")
    if set(impact) != {"specification", "implementation"}:
        raise MacrostatesError("impact must declare exactly specification and implementation")
    for side in ("specification", "implementation"):
        if impact.get(side) not in IMPACTS:
            raise MacrostatesError(f"impact.{side} must be none, patch, minor or major")
    deliverables = _strings(data.get("deliverables"), "deliverables")
    if len(set(deliverables)) != len(deliverables):
        raise MacrostatesError("deliverables must not repeat identifiers")
    for item in deliverables:
        identifier(item, "deliverable")
    requirements = data.get("requirements")
    if not isinstance(requirements, list):
        raise MacrostatesError("requirements must be an explicit list")
    for requirement in requirements:
        item = mapping(requirement, "requirement coverage")
        for field in ("requirement", "implementation", "verification"):
            string(item.get(field), f"requirement coverage.{field}")
    _strings(data.get("evidence"), "evidence")
    _strings(data.get("gaps"), "gaps")


def _record_files(root: Path, *, history: bool) -> list[Path]:
    directory = changes_path(root)
    if history:
        directory = safe_path(directory, "history")
    if not directory.exists():
        return []
    if not directory.is_dir():
        raise MacrostatesError("Change-record locations must be directories")
    files = sorted(path for path in directory.iterdir() if path.suffix in (".yaml", ".yml"))
    for path in files:
        safe_path(directory, path.name)
        if path.suffix != ".yaml" or not path.is_file():
            raise MacrostatesError("Change records must be ordinary <id>.yaml files")
    return files


def load_changes(root: Path, *, history: bool = False) -> dict[str, dict[str, Any]]:
    """Read schema-valid records and reject duplicates across pending and history."""
    selected: dict[str, dict[str, Any]] = {}
    captured = load_work(root)
    ids: set[str] = set()
    for archived in (False, True):
        for path in _record_files(root, history=archived):
            record = read_yaml(path)
            validate_record(record, expected_id=path.stem)
            work = record.get("work")
            if work is not None and (
                work not in captured or record["origin"] != captured[work]["origin"]
            ):
                raise MacrostatesError(
                    "Change origin differs from its immutable captured work provenance"
                )
            record_id = record["id"]
            if record_id in ids:
                raise MacrostatesError(f"Duplicate change record id: {record_id}")
            ids.add(record_id)
            if archived == history:
                selected[record_id] = record
    return selected


def record_hashes(root: Path, *, history: bool = False) -> list[dict[str, str]]:
    load_changes(root, history=history)
    return [
        {"id": path.stem, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in _record_files(root, history=history)
    ]


def check_changes(root: Path, *, readiness: bool = True) -> Report:
    report = Report()
    try:
        current = declarations(root)
        records = load_changes(root)
    except (MacrostatesError, OSError, UnicodeError) as exc:
        report.add("change.invalid", str(exc))
        return report
    for record_id, record in records.items():
        path = f".macrostates/implementation/changes/{record_id}.yaml"
        impact = record["impact"]
        if current["implementation"] is None and impact["implementation"] != "none":
            report.add("change.implementation_missing", "No implementation baseline exists", path)
        if not readiness:
            continue
        if any(value != "none" for value in impact.values()) and not record["evidence"]:
            report.add(
                "change.evidence_missing", "Version-affecting work needs validation evidence", path
            )
        if (
            any(value in ("minor", "major") for value in impact.values())
            and not record["requirements"]
        ):
            report.add(
                "change.coverage_missing", "Contract changes need requirement coverage", path
            )
        if record["gaps"]:
            report.add("change.gaps", "Required implementation gaps remain", path)
    return report


def load_work(root: Path) -> dict[str, dict[str, Any]]:
    directory = safe_path(root, ".macrostates/implementation/work")
    if not directory.exists():
        return {}
    if not directory.is_dir():
        raise MacrostatesError("Captured work location must be a directory")
    records = {}
    for path in sorted(directory.glob("*.yaml")):
        safe_path(directory, path.name)
        data = read_yaml(path)
        if data.get("schema_version") != 1 or isinstance(data.get("schema_version"), bool):
            raise MacrostatesError("Captured work records need schema_version: 1")
        work_id = identifier(data.get("id"), "work")
        if work_id != path.stem:
            raise MacrostatesError("Captured work id must match its filename")
        _validate_origin(data.get("origin"))
        records[work_id] = data
    return records


def _capture_origin(root: Path, original: str | None) -> dict[str, Any]:
    from ._git import commit, git, primary_ref

    head = commit(root)
    if original is None:
        original = git(root, "merge-base", head, commit(root, primary_ref(root)))
        if original != head:
            raise MacrostatesError(
                "Late work needs captured provenance or an explicit original commit"
            )
    elif not COMMIT_ID.fullmatch(original):
        raise MacrostatesError("Original commit must be a full lowercase Git commit ID")
    selected = commit(root, original)
    manifests = []
    for location in (".macrostates/specs", "specs"):
        for filename in ("composition.yaml", "composition.yml"):
            try:
                content = git(root, "show", selected + ":" + location + "/" + filename)
            except MacrostatesError:
                continue
            manifests.append(parse_yaml(content))
    if len(manifests) != 1:
        raise MacrostatesError("Original commit needs one readable composition baseline")
    project = mapping(manifests[0].get("project"), "original project")
    spec = string(project.get("version"), "original specification")
    if spec.startswith("spec-"):
        spec = "specs-" + spec.removeprefix("spec-")
    baseline(spec, "specification")
    implementation = None
    for location in (".macrostates/implementation", "implementation"):
        try:
            content = git(root, "show", selected + ":" + location + "/release.yaml")
        except MacrostatesError:
            continue
        previous = parse_yaml(content)
        value = string(previous.get("version"), "original implementation")
        if not value.startswith("imp-"):
            version(value)
            value = "imp-" + value
        baseline(value, "implementation")
        implemented = string(previous.get("specification"), "original implementation specification")
        if implemented.startswith("spec-"):
            implemented = "specs-" + implemented.removeprefix("spec-")
        old_spec = baseline(implemented, "specification")
        if (
            old_spec[:2] != baseline(value, "implementation")[:2]
            or old_spec[2] > baseline(spec, "specification")[2]
        ):
            raise MacrostatesError(
                "Original implementation declaration has invalid specification provenance"
            )
        if implementation is not None:
            raise MacrostatesError("Original commit has ambiguous implementation declarations")
        implementation = value
    origin = {"commit": selected, "specification": spec, "implementation": implementation}
    _validate_origin(origin)
    return origin


def start_work(root: Path, id: str, *, origin_commit: str | None = None) -> Path:
    """Capture immutable starting provenance before the branch acquires commits."""
    from ._git import ensure_development

    ensure_development(root, clean=False)
    declarations(root)
    work_id = identifier(id, "work")
    if work_id in load_work(root):
        raise MacrostatesError(
            "Captured work id is already used; its original provenance is preserved"
        )
    data = {"schema_version": 1, "id": work_id, "origin": _capture_origin(root, origin_commit)}
    destination = safe_path(root, f".macrostates/implementation/work/{work_id}.yaml")
    _write_new(destination, data)
    return destination


def _write_new(destination: Path, data: dict[str, Any]) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("x", encoding="utf-8") as stream:
            stream.write(dump_yaml(data))
    except FileExistsError as exc:
        raise MacrostatesError("Record id appeared concurrently; it was preserved") from exc
    except BaseException:
        destination.unlink(missing_ok=True)
        raise


def create_change(
    root: Path,
    id: str,
    summary: str,
    specification: str,
    implementation: str,
    *,
    deliverables: list[str] | None = None,
    requirements: list[dict[str, Any]] | None = None,
    evidence: list[str] | None = None,
    gaps: list[str] | None = None,
    work: str | None = None,
    origin_commit: str | None = None,
) -> Path:
    from ._git import ensure_development

    record_id = identifier(id)
    declarations(root)
    ensure_development(root, clean=False)
    for archived in (False, True):
        if record_id in load_changes(root, history=archived):
            raise MacrostatesError("Change record id is already used")
    captured = load_work(root)
    selected_work = work if work is not None else record_id if record_id in captured else None
    if selected_work is not None:
        identifier(selected_work, "work")
        if origin_commit is not None:
            raise MacrostatesError("Choose captured work or an explicit original commit")
        if selected_work not in captured:
            raise MacrostatesError("Captured work id does not exist")
        origin = copy.deepcopy(captured[selected_work]["origin"])
    else:
        origin = _capture_origin(root, origin_commit)
    record = {
        "schema_version": 1,
        "id": record_id,
        "summary": summary,
        "origin": origin,
        "impact": {"specification": specification, "implementation": implementation},
        "deliverables": list(deliverables or []),
        "requirements": list(requirements or []),
        "evidence": list(evidence or []),
        "gaps": list(gaps or []),
    }
    if selected_work is not None:
        record["work"] = selected_work
    validate_record(record)
    destination = safe_path(changes_path(root), record_id + ".yaml")
    _write_new(destination, record)
    return destination
