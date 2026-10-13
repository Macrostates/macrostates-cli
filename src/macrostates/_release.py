"""Reviewable release plans and guarded preparation, without commits or publication."""

import hashlib
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

from ._changes import changes_path, check_changes, load_changes, record_hashes
from ._git import commit, dirty, ensure_development, git, primary_ref, ref
from ._io import MAX_DOCUMENT, dump_yaml, mapping, parse_yaml, read_yaml, safe_path, string
from ._models import MacrostatesError, Report
from ._mutations import replace_paths
from ._versioning import COMMIT_ID, IMPACTS, aggregate, baseline, calendar_date, declarations

PLAN_LOCATION = ".macrostates/implementation/release-plan.yaml"


def _blob(root: Path, source: str, path: str) -> bytes:
    """Read exact tracked document bytes without archive export transformations."""
    import subprocess

    object_id = git(root, "rev-parse", source + ":" + path)
    if int(git(root, "cat-file", "-s", object_id)) > MAX_DOCUMENT:
        raise MacrostatesError("Tracked release document exceeds the document limit")
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "cat-file", "blob", object_id],
            capture_output=True,
            check=False,
            timeout=120,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise MacrostatesError("Tracked release document could not be read") from exc
    if result.returncode:
        raise MacrostatesError("Tracked release document could not be read")
    return result.stdout


def _entries_at(root: Path, source: str, directory: str) -> list[tuple[str, str]]:
    result = []
    for entry in git(root, "ls-tree", "-r", "-z", source, "--", directory).split("\0"):
        if entry:
            header, name = entry.split("\t", 1)
            result.append((header.split()[0], name))
    return result


def _record_hashes_at(root: Path, source: str, *, history: bool) -> dict[str, str]:
    from ._changes import validate_record

    directory = ".macrostates/implementation/changes/" + ("history/" if history else "")
    result = {}
    for mode, path in _entries_at(root, source, directory.rstrip("/")):
        name = path.removeprefix(directory)
        if "/" in name or not name.endswith((".yaml", ".yml")):
            continue
        if mode not in {"100644", "100755"} or not name.endswith(".yaml"):
            raise MacrostatesError("Tagged changes must use ordinary id.yaml records")
        payload = _blob(root, source, path)
        record = parse_yaml(payload)
        validate_record(record, expected_id=name.removesuffix(".yaml"))
        result[record["id"]] = hashlib.sha256(payload).hexdigest()
    return result


def _check_work_delta(root: Path, original: str, source: str) -> None:
    from ._changes import _capture_origin
    from ._versioning import identifier

    directory = ".macrostates/implementation/work"
    before = dict((path, mode) for mode, path in _entries_at(root, original, directory))
    after = dict((path, mode) for mode, path in _entries_at(root, source, directory))
    for path, mode in before.items():
        if after.get(path) != mode or _blob(root, original, path) != _blob(root, source, path):
            raise MacrostatesError("Existing captured work provenance must remain unchanged")
    for path, mode in after.items():
        if path in before:
            continue
        name = path.removeprefix(directory + "/")
        if "/" in name or not name.endswith(".yaml") or mode not in {"100644", "100755"}:
            raise MacrostatesError("New work tracking must be ordinary id.yaml origin records")
        data = parse_yaml(_blob(root, source, path))
        if data.get("schema_version") != 1 or isinstance(data.get("schema_version"), bool):
            raise MacrostatesError("Captured work needs schema_version: 1")
        work_id = identifier(data.get("id"), "work")
        if work_id != name.removesuffix(".yaml"):
            raise MacrostatesError("Captured work id must match its filename")
        origin = mapping(data.get("origin"), "origin")
        recorded = string(origin.get("commit"), "origin.commit")
        expected = _capture_origin(root, recorded)
        if any(origin.get(field) != value for field, value in expected.items()):
            raise MacrostatesError("New captured work provenance differs from its original commit")


def _check_workflows_at(root: Path, source: str) -> None:
    from ._integration import CLOSED, closure_evidence

    for mode, path in _entries_at(root, source, ".macrostates/implementation/workflows"):
        if mode not in {"100644", "100755"}:
            raise MacrostatesError(
                "Tagged workflow records must not be symbolic links or submodules"
            )
        if not path.endswith(".md"):
            continue
        content = _blob(root, source, path).decode("utf-8")
        statuses = re.findall(r"^\s*(?:-\s*)?Status:\s*(\S+)\s*$", content, re.M | re.I)
        if Path(path).name.casefold() in {"readme.md", "main.md"} and not statuses:
            continue
        if len(statuses) != 1 or statuses[0] not in CLOSED or not closure_evidence(content):
            raise MacrostatesError(
                "Finalized tagged baseline contains an open or unauthorized workflow"
            )


def _digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def _raise_report(report: Report) -> None:
    if not report.ok:
        raise MacrostatesError(
            "; ".join(item.message for item in report.diagnostics if item.severity == "error")
        )


def _baselines(current: dict[str, Any]) -> dict[str, str | None]:
    return {
        "specification": current["specification"],
        "implementation": current["implementation"],
        "implementation_specification": current["implementation_specification"],
    }


def candidate_integrated(root: Path, plan: dict[str, Any], *, target: str | None = None) -> bool:
    """Stored candidate becomes historical once its exact declaration is integrated."""
    try:
        _validate_plan(plan, status="candidate")
        target = ref(target) if target is not None else ref(plan["integration_ref"])
        integrated = parse_yaml(git(root, "show", f"{target}:{PLAN_LOCATION}"))
        if integrated != plan:
            return False
        current = declarations(root)
        candidate = mapping(plan.get("candidate"), "candidate")
        primary_composition = parse_yaml(
            git(root, "show", f"{target}:" + current["manifest"].relative_to(root).as_posix())
        )
        if mapping(primary_composition.get("project"), "primary project").get(
            "version"
        ) != candidate.get("specification"):
            return False
        if candidate.get("implementation") is not None:
            primary_release = parse_yaml(
                git(root, "show", f"{target}:.macrostates/implementation/release.yaml")
            )
            if primary_release != current["release"]:
                return False
        return (
            current["specification"] == candidate.get("specification")
            and current["implementation"] == candidate.get("implementation")
            and current["implementation_specification"]
            == candidate.get("implementation_specification")
        )
    except (MacrostatesError, OSError, UnicodeError):
        return False


def _current_binding(root: Path, target: str | None = None) -> dict[str, Any]:
    current = declarations(root)
    selected = ref(target) if target is not None else primary_ref(root)
    return {
        "target_commit": commit(root),
        "target_tree": git(root, "rev-parse", "HEAD^{tree}"),
        "integration_ref": selected,
        "integration_target": commit(root, selected),
        "baselines": _baselines(current),
        "records": record_hashes(root),
        "history_records": record_hashes(root, history=True),
        "declarations": {
            "composition_sha256": _digest(current["manifest"]),
            "release_sha256": _digest(current["release_path"]),
        },
    }


def plan_release(root: Path, *, target: str | None = None) -> dict[str, Any]:
    """Calculate a release against an exact committed tree, never modify it."""
    if dirty(root):
        raise MacrostatesError("Commit proposed records and source before release planning")
    current = declarations(root)
    selected_ref = ref(target) if target is not None else primary_ref(root)
    _raise_report(check_changes(root))
    records = load_changes(root)
    if not records:
        raise MacrostatesError("No pending changes to finalize")
    existing = safe_path(root, PLAN_LOCATION)
    if existing.exists():
        old_plan = read_yaml(existing)
        if old_plan.get("status") == "candidate" and not candidate_integrated(
            root, old_plan, target=selected_ref
        ):
            raise MacrostatesError("An unintegrated release candidate already exists")
    proposed = aggregate(
        current["specification"],
        current["implementation"],
        [record["impact"] for record in records.values()],
    )
    if (
        proposed["specification"] == current["specification"]
        and proposed["implementation"] == current["implementation"]
    ):
        raise MacrostatesError("Tracking-only changes do not allocate a release version")
    proposed["implementation_specification"] = (
        proposed["specification"]
        if proposed["implementation"] is not None
        and proposed["implementation"] != current["implementation"]
        else current["implementation_specification"]
    )
    binding = _current_binding(root, selected_ref)
    try:
        git(
            root,
            "merge-base",
            "--is-ancestor",
            binding["integration_target"],
            binding["target_commit"],
        )
    except MacrostatesError as exc:
        raise MacrostatesError(
            "Synchronize the release branch with the current primary before planning"
        ) from exc
    result = {
        "schema_version": 1,
        "status": "planned",
        **binding,
        "candidate": proposed,
        "impact": {
            side: max(
                (record["impact"][side] for record in records.values()),
                key=IMPACTS.index,
            )
            for side in ("specification", "implementation")
        },
        "deliverables": sorted(
            {name for record in records.values() for name in record["deliverables"]}
        ),
    }
    if binding != _current_binding(root, binding["integration_ref"]) or dirty(root):
        raise MacrostatesError("Repository changed during planning; calculate a fresh plan")
    return result


def _validate_hashes(value: Any, label: str) -> list[dict[str, str]]:
    if not isinstance(value, list):
        raise MacrostatesError(f"{label} must be a list of record hashes")
    seen = set()
    for item in value:
        entry = mapping(item, label)
        from ._versioning import identifier

        record_id = identifier(entry.get("id"))
        digest = string(entry.get("sha256"), "sha256")
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise MacrostatesError("Record sha256 must be a lowercase 64-character digest")
        if record_id in seen:
            raise MacrostatesError("Release plan repeats a change id")
        seen.add(record_id)
    return value


def _validate_plan(plan: dict[str, Any], *, status: str) -> None:
    if plan.get("schema_version") != 1 or isinstance(plan.get("schema_version"), bool):
        raise MacrostatesError("Release plan needs schema_version: 1")
    if plan.get("status") != status:
        raise MacrostatesError(f"Release plan must have status: {status}")
    ref(string(plan.get("integration_ref"), "integration_ref"))
    for field in ("target_commit", "target_tree", "integration_target"):
        text = string(plan.get(field), field)
        if not COMMIT_ID.fullmatch(text):
            raise MacrostatesError(f"{field} must be a full Git object ID")
    for field in ("baselines", "candidate"):
        values = mapping(plan.get(field), field)
        baseline(values.get("specification"), "specification")
        if "implementation" not in values or "implementation_specification" not in values:
            raise MacrostatesError(
                f"{field} must explicitly declare implementation and its baseline"
            )
        if values["implementation"] is not None:
            imp = baseline(values["implementation"], "implementation")
            spec = baseline(values["specification"], "specification")
            implemented = baseline(values["implementation_specification"], "specification")
            if imp[:2] != spec[:2] or imp[:2] != implemented[:2] or implemented[2] > spec[2]:
                raise MacrostatesError(
                    "Release-plan specification and implementation contracts differ"
                )
        elif values["implementation_specification"] is not None:
            raise MacrostatesError(
                "A specification-only plan cannot invent implementation provenance"
            )
    records = _validate_hashes(plan.get("records"), "records")
    history = _validate_hashes(plan.get("history_records"), "history_records")
    if not records or {item["id"] for item in records} & {item["id"] for item in history}:
        raise MacrostatesError("Plan needs distinct included and historical change identifiers")
    declarations_hash = mapping(plan.get("declarations"), "declarations")
    for field in ("composition_sha256", "release_sha256"):
        value = declarations_hash.get(field)
        if field == "release_sha256" and value is None:
            continue
        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(char not in "0123456789abcdef" for char in value)
        ):
            raise MacrostatesError("Plan declaration hashes must be sha256 identities")
    impact = mapping(plan.get("impact"), "impact")
    if any(impact.get(side) not in IMPACTS for side in ("specification", "implementation")):
        raise MacrostatesError("Plan needs both supported aggregate impact values")
    deliverables = plan.get("deliverables")
    if not isinstance(deliverables, list):
        raise MacrostatesError("Plan deliverables must be an explicit list")
    from ._versioning import identifier

    for name in deliverables:
        identifier(name, "deliverable")
    if status == "candidate":
        calendar_date(plan.get("release_date"))


def prepare_release(root: Path, plan: dict[str, Any], *, date: str) -> dict[str, Any]:
    """Apply a reviewed exact plan on a development branch, with ordinary rollback."""
    marker = safe_path(root, ".macrostates/implementation/.release-operation")
    if marker.exists():
        raise MacrostatesError("Release preparation marker exists; inspect prior recovery state")
    ensure_development(root)
    _validate_plan(plan, status="planned")
    stamp = calendar_date(date)
    expected = plan_release(root, target=plan["integration_ref"])
    if plan != expected:
        raise MacrostatesError(
            "Release plan is stale or was altered; calculate and review a fresh plan"
        )
    current = declarations(root)
    composition = current["composition"]
    composition["project"]["version"] = plan["candidate"]["specification"]
    prepared_plan = {**plan, "status": "candidate", "release_date": stamp}
    marker.parent.mkdir(parents=True, exist_ok=True)
    try:
        with marker.open("x", encoding="ascii") as stream:
            stream.write(
                "Release preparation in progress; inspect recovery files before retrying.\n"
            )
    except FileExistsError as exc:
        raise MacrostatesError(
            "Release preparation marker exists; inspect prior recovery state"
        ) from exc
    try:
        workspace = Path(tempfile.mkdtemp(prefix=".macrostates-release-", dir=root))
    except OSError:
        marker.unlink(missing_ok=True)
        raise
    keep_recovery = False
    try:
        prepared_changes = workspace / "changes"
        shutil.copytree(changes_path(root), prepared_changes, symlinks=True)
        history = prepared_changes / "history"
        history.mkdir(exist_ok=True)
        for record in plan["records"]:
            source = prepared_changes / (record["id"] + ".yaml")
            if hashlib.sha256(source.read_bytes()).hexdigest() != record["sha256"]:
                raise MacrostatesError("Change record changed during preparation")
            source.rename(history / source.name)
        manifest = workspace / "composition.yaml"
        if plan["candidate"]["specification"] == plan["baselines"]["specification"]:
            manifest.write_bytes(current["manifest"].read_bytes())
        else:
            manifest.write_text(dump_yaml(composition), encoding="utf-8")
        plan_file = workspace / "release-plan.yaml"
        plan_file.write_text(dump_yaml(prepared_plan), encoding="utf-8")
        replacements = {
            current["manifest"]: manifest,
            changes_path(root): prepared_changes,
            safe_path(root, PLAN_LOCATION): plan_file,
        }
        if plan["candidate"]["implementation"] != current["implementation"]:
            release = {
                **(current["release"] or {}),
                "schema_version": 2,
                "version": plan["candidate"]["implementation"],
                "specification": plan["candidate"]["implementation_specification"],
                "release_date": stamp,
            }
            declaration = workspace / "release.yaml"
            declaration.write_text(dump_yaml(release), encoding="utf-8")
            replacements[current["release_path"]] = declaration
        # The marker/workspace are intentionally untracked; compare actual bound
        # inputs rather than asking Git to call those operation files clean.
        live = _current_binding(root, plan["integration_ref"])
        if live != {key: plan[key] for key in live}:
            raise MacrostatesError(
                "Repository changed during preparation; no candidate was applied"
            )
        git(root, "diff", "--quiet", "HEAD", "--")
        replace_paths(replacements, workspace)
    except MacrostatesError as exc:
        keep_recovery = str(exc).startswith("Rollback failed;")
        raise
    finally:
        if not keep_recovery:
            shutil.rmtree(workspace)
            marker.unlink(missing_ok=True)
    return prepared_plan


def _tag(root: Path, name: str) -> str | None:
    try:
        git(root, "show-ref", "--verify", "refs/tags/" + name)
    except MacrostatesError:
        migration_path = safe_path(root, ".macrostates/implementation/version-migration.yaml")
        if not migration_path.exists():
            return None
        migrated = read_yaml(migration_path)
        if migrated.get("schema_version") != 1 or isinstance(migrated.get("schema_version"), bool):
            raise MacrostatesError("Unsupported migration provenance schema") from None
        side = "specification" if name.startswith("specs-") else "implementation"
        entry = migrated.get(side)
        if not isinstance(entry, dict) or entry.get("identity") != name:
            return None
        old = ("spec-" if side == "specification" else "v") + name.removeprefix(
            "specs-"
        ).removeprefix("imp-")
        if (
            entry.get("legacy_tag") != old
            or not isinstance(entry.get("commit"), str)
            or not COMMIT_ID.fullmatch(entry["commit"])
        ):
            raise MacrostatesError(
                "Migration baseline alias needs verified original tag provenance"
            ) from None
        if git(root, "cat-file", "-t", "refs/tags/" + old) != "tag":
            raise MacrostatesError(
                "Migration baseline alias must reference an annotated tag"
            ) from None
        original = commit(root, "refs/tags/" + old)
        if original != entry["commit"]:
            raise MacrostatesError(
                "Migration baseline tag moved from its recorded source commit"
            ) from None
        return original
    if git(root, "cat-file", "-t", "refs/tags/" + name) != "tag":
        raise MacrostatesError(f"Baseline {name} must use an annotated tag")
    return commit(root, "refs/tags/" + name)


def _specification_snapshot_matches(
    root: Path, tagged: str, source: str, manifest_name: str
) -> bool:
    before, after = _specification_inventory(root, tagged), _specification_inventory(root, source)
    if before == after:
        return True
    migration = safe_path(root, ".macrostates/implementation/version-migration.yaml")
    if not migration.exists():
        return False
    if set(before) != set(after) or any(
        before[name] != after[name] for name in before if name != manifest_name
    ):
        return False
    if before[manifest_name][0] != after[manifest_name][0]:
        return False
    old = parse_yaml(git(root, "show", tagged + ":" + manifest_name))
    new = parse_yaml(git(root, "show", source + ":" + manifest_name))
    old_project = mapping(old.get("project"), "tagged project")
    selected = old_project.get("version")
    if isinstance(selected, str) and selected.startswith("spec-"):
        old_project["version"] = "specs-" + selected.removeprefix("spec-")
    return old == new


def _specification_inventory(root: Path, source: str) -> dict[str, tuple[str, str]]:
    """Mirror directory-scope ownership using immutable Git inventories."""
    from ._scopes import IGNORED

    entries = {}
    for entry in git(root, "ls-tree", "-r", "-z", source).split("\0"):
        if not entry:
            continue
        header, name = entry.split("\t", 1)
        mode, _, object_id = header.split()
        entries[name] = (mode, object_id)
    boundaries = set()
    for name in entries:
        for ending in (
            "/.macrostates/specs/composition.yaml",
            "/.macrostates/specs/composition.yml",
            "/specs/composition.yaml",
            "/specs/composition.yml",
        ):
            if name.endswith(ending):
                boundaries.add(name.removesuffix(ending))
    roots = {".macrostates/specs/"}
    ending = "/.macrostates/specs/main.md"
    for name in entries:
        if not name.endswith(ending):
            continue
        directory = name.removesuffix(ending)
        parts = directory.split("/")
        if any(part in IGNORED or part.startswith(".") or part == "specs" for part in parts):
            continue
        if any(directory == owner or directory.startswith(owner + "/") for owner in boundaries):
            continue
        roots.add(directory + "/.macrostates/specs/")
    return {
        name: value
        for name, value in entries.items()
        if any(name.startswith(prefix) for prefix in roots)
    }


def _implementation_snapshot_matches(previous: dict[str, Any], current: dict[str, Any]) -> bool:
    if previous == current:
        return True
    selected = previous.get("version")
    spec = previous.get("specification")
    if not isinstance(selected, str) or not isinstance(spec, str) or not spec.startswith("spec-"):
        return False
    previous = {
        **previous,
        "schema_version": 2,
        "version": "imp-" + selected,
        "specification": "specs-" + spec.removeprefix("spec-"),
    }
    return previous == current


def _check_original_binding(root: Path, plan: dict[str, Any]) -> None:
    original = commit(root, plan["target_commit"])
    if git(root, "rev-parse", original + "^{tree}") != plan["target_tree"]:
        raise MacrostatesError("Release target tree does not match its recorded commit")
    current = declarations(root)
    manifest_name = current["manifest"].relative_to(root).as_posix()
    # Git show strips a final newline through the text wrapper; hash the exact
    # blob through cat-file with its known byte size instead.
    import subprocess

    for path, field in (
        (manifest_name, "composition_sha256"),
        (".macrostates/implementation/release.yaml", "release_sha256"),
    ):
        expected = plan["declarations"][field]
        try:
            object_id = git(root, "rev-parse", original + ":" + path)
        except MacrostatesError:
            if expected is None:
                continue
            raise MacrostatesError("Original declaration is missing") from None
        try:
            result = subprocess.run(
                ["git", "-C", str(root), "cat-file", "blob", object_id],
                capture_output=True,
                check=False,
                timeout=120,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise MacrostatesError("Original source declaration could not be read") from exc
        if result.returncode or hashlib.sha256(result.stdout).hexdigest() != expected:
            raise MacrostatesError("Original declaration hash does not match the target snapshot")
        data = parse_yaml(result.stdout)
        if (
            field == "composition_sha256"
            and mapping(data.get("project"), "original project").get("version")
            != plan["baselines"]["specification"]
        ):
            raise MacrostatesError("Original specification baseline was altered in the plan")
        if field == "release_sha256" and (
            data.get("version") != plan["baselines"]["implementation"]
            or data.get("specification") != plan["baselines"]["implementation_specification"]
        ):
            raise MacrostatesError("Original implementation baseline was altered in the plan")
    for history, field in ((False, "records"), (True, "history_records")):
        expected_records = {item["id"]: item["sha256"] for item in plan[field]}
        if _record_hashes_at(root, original, history=history) != expected_records:
            raise MacrostatesError("Original change records differ from the release plan binding")


def _check_candidate_delta(
    root: Path, plan: dict[str, Any], current: dict[str, Any], *, source: str | None = None
) -> None:
    """Preparation may finalize declarations, not silently alter planned behavior."""
    source = commit(root) if source is None else source
    original = plan["target_commit"]
    manifest_name = current["manifest"].relative_to(root).as_posix()
    permitted = {
        manifest_name,
        ".macrostates/implementation/release.yaml",
        PLAN_LOCATION,
        ".macrostates/implementation/application.yaml",
        ".macrostates/implementation/deliverables.yaml",
        ".macrostates/implementation/main.md",
        ".macrostates/implementation/release-notes.md",
    }
    changed = git(root, "diff", "--name-only", "-z", original, source, "--").split("\0")
    for path in changed:
        if not path or path in permitted:
            continue
        if path.startswith(
            (
                ".macrostates/implementation/changes/",
                ".macrostates/implementation/workflows/",
                ".macrostates/implementation/work/",
            )
        ):
            continue
        raise MacrostatesError(
            "Source changed after planning; return the work to pending state and replan"
        )
    original_composition = parse_yaml(git(root, "show", original + ":" + manifest_name))
    mapping(original_composition.get("project"), "original project")["version"] = plan["candidate"][
        "specification"
    ]
    if original_composition != current["composition"]:
        raise MacrostatesError("Composition changed beyond the planned specification version")
    if plan["baselines"]["implementation"] is not None:
        previous = parse_yaml(
            git(root, "show", original + ":.macrostates/implementation/release.yaml")
        )
        if plan["candidate"]["implementation"] != plan["baselines"]["implementation"]:
            previous.update(
                version=plan["candidate"]["implementation"],
                specification=plan["candidate"]["implementation_specification"],
                release_date=plan["release_date"],
            )
        if previous != current["release"]:
            raise MacrostatesError("Implementation declaration differs from planned finalization")
    _check_work_delta(root, original, source)


def _check_finalized_tag(
    root: Path, plan: dict[str, Any], current: dict[str, Any], tagged: str, target: str
) -> None:
    """Verify the immutable finalized snapshot, independently of later app metadata."""
    git(root, "merge-base", "--is-ancestor", plan["target_commit"], tagged)
    git(root, "merge-base", "--is-ancestor", tagged, target)
    if _blob(root, tagged, PLAN_LOCATION) != _blob(root, commit(root), PLAN_LOCATION):
        raise MacrostatesError("Historical release plan differs from its finalized tagged snapshot")
    tagged_current = dict(current)
    manifest_name = current["manifest"].relative_to(root).as_posix()
    tagged_current["composition"] = parse_yaml(_blob(root, tagged, manifest_name))
    tagged_current["specification"] = mapping(
        tagged_current["composition"].get("project"), "tagged project"
    ).get("version")
    if plan["candidate"]["implementation"] is not None:
        tagged_current["release"] = parse_yaml(
            _blob(root, tagged, ".macrostates/implementation/release.yaml")
        )
        tagged_current["implementation"] = tagged_current["release"].get("version")
        tagged_current["implementation_specification"] = tagged_current["release"].get(
            "specification"
        )
    if _baselines(tagged_current) != plan["candidate"]:
        raise MacrostatesError("Baseline tag does not contain the finalized declarations")
    _check_candidate_delta(root, plan, tagged_current, source=tagged)
    expected = {item["id"]: item["sha256"] for item in plan["history_records"] + plan["records"]}
    if _record_hashes_at(root, tagged, history=True) != expected or _record_hashes_at(
        root, tagged, history=False
    ):
        raise MacrostatesError("Baseline tag does not preserve the finalized change-record history")
    _check_workflows_at(root, tagged)


def _finalized_tags(
    root: Path, plan: dict[str, Any], current: dict[str, Any], target: str
) -> tuple[bool, dict[str, str | None]]:
    tags = {}
    changed = []
    for side in ("specification", "implementation"):
        name = plan["candidate"][side]
        if name is None:
            continue
        tags[name] = _tag(root, name)
        if name != plan["baselines"][side]:
            changed.append(name)
    finalized = bool(changed)
    for name in changed:
        tagged = tags[name]
        if tagged is None:
            finalized = False
            continue
        try:
            _check_finalized_tag(root, plan, current, tagged, target)
        except (MacrostatesError, OSError, UnicodeError, ValueError):
            finalized = False
    return finalized, tags


def check_release(root: Path, *, target: str | None = None, publication: bool = False) -> Report:
    """Validate candidate provenance; publication additionally requires integrated tags."""
    from ._integration import check_workflows

    report = Report()
    try:
        current = declarations(root)
        plan = read_yaml(safe_path(root, PLAN_LOCATION))
        _validate_plan(plan, status="candidate")
        _check_original_binding(root, plan)
        _check_candidate_delta(root, plan, current)
        selected_ref = ref(target) if target is not None else ref(plan["integration_ref"])
        selected_target = commit(root, selected_ref)
        source = commit(root)
        finalized, tags = _finalized_tags(root, plan, current, selected_target)
        if dirty(root):
            report.add("release.dirty", "Commit the exact release candidate before validation")
        actual = _baselines(current)
        if actual != plan["candidate"]:
            report.add(
                "release.declarations", "Candidate declarations do not match the release plan"
            )
        pending = load_changes(root)
        if pending:
            if not finalized or any(
                value != "none"
                for record in pending.values()
                for value in record["impact"].values()
            ):
                report.add(
                    "release.pending",
                    "Unconsumed version-affecting changes remain outside the finalized baseline",
                )
            else:
                report.diagnostics.extend(check_changes(root).diagnostics)
                if any(not record["evidence"] for record in pending.values()):
                    report.add(
                        "release.metadata_evidence",
                        "Independent application metadata work needs explicit validation evidence",
                    )
        archived = load_changes(root, history=True)
        expected_history = {
            item["id"]: item["sha256"] for item in plan["history_records"] + plan["records"]
        }
        actual_history = {item["id"]: item["sha256"] for item in record_hashes(root, history=True)}
        if expected_history != actual_history:
            report.add(
                "release.records", "Archived change records differ from the exact reviewed plan"
            )
        included = [archived[item["id"]] for item in plan["records"] if item["id"] in archived]
        recomputed = aggregate(
            plan["baselines"]["specification"],
            plan["baselines"]["implementation"],
            [item["impact"] for item in included],
        )
        if any(
            plan["candidate"][side] != recomputed[side]
            for side in ("specification", "implementation")
        ):
            report.add("release.impact", "Candidate versions do not match included change impacts")
        for record in included:
            impact = record["impact"]
            if (
                record["gaps"]
                or (any(value != "none" for value in impact.values()) and not record["evidence"])
                or (
                    any(value in ("minor", "major") for value in impact.values())
                    and not record["requirements"]
                )
            ):
                report.add(
                    "release.evidence",
                    "Included work has unresolved gaps or incomplete conformance evidence",
                )
        report.diagnostics.extend(check_workflows(root).diagnostics)
        if publication:
            from ._deliverables import check_deliverable_publication

            report.diagnostics.extend(check_deliverable_publication(root).diagnostics)
        git(root, "merge-base", "--is-ancestor", plan["target_commit"], source)
        try:
            git(root, "merge-base", "--is-ancestor", source, selected_target)
            integrated = True
        except MacrostatesError:
            integrated = False
        if publication and not integrated:
            report.add(
                "release.integration",
                "Publication requires the exact source to be integrated into the target",
            )
        if not integrated and not finalized and selected_target != plan["integration_target"]:
            report.add("release.stale", "Target changed after release planning; repeat preparation")
        for side in ("specification", "implementation"):
            name = plan["candidate"][side]
            if name is None:
                continue
            old = plan["baselines"][side]
            tagged = tags[name]
            if name == old:
                if tagged is None:
                    report.add(
                        "release.baseline_tag",
                        f"Unchanged baseline {name} has no annotated source tag",
                    )
                elif side == "specification":
                    manifest_name = current["manifest"].relative_to(root).as_posix()
                    tagged_declaration = parse_yaml(git(root, "show", tagged + ":" + manifest_name))
                    tag_identity = mapping(tagged_declaration.get("project"), "tagged project").get(
                        "version"
                    )
                    if tag_identity not in (
                        name,
                        "spec-" + name.removeprefix("specs-"),
                    ) or not _specification_snapshot_matches(root, tagged, source, manifest_name):
                        report.add(
                            "release.specification_snapshot",
                            "Unchanged specification tag does not identify the candidate specifications",
                        )
                else:
                    tagged_release = parse_yaml(
                        git(root, "show", tagged + ":.macrostates/implementation/release.yaml")
                    )
                    if not _implementation_snapshot_matches(tagged_release, current["release"]):
                        report.add(
                            "release.implementation_snapshot",
                            "Unchanged implementation baseline declaration was modified",
                        )
            elif tagged is not None and tagged != source:
                reusable = False
                if finalized:
                    try:
                        git(root, "merge-base", "--is-ancestor", tagged, source)
                        reusable = True
                    except MacrostatesError:
                        if not publication:
                            try:
                                git(root, "merge-base", "--is-ancestor", source, tagged)
                                reusable = True
                            except MacrostatesError:
                                pass
                if not reusable:
                    report.add(
                        "release.collision",
                        f"Version tag {name} does not identify this candidate or a validated finalized ancestor baseline",
                    )
            elif publication and tagged is None:
                report.add(
                    "release.tag_missing", f"Published baseline {name} requires an annotated tag"
                )
        if source != commit(root) or selected_target != commit(root, selected_ref):
            report.add("release.stale", "Repository changed during release validation")
        for name, resolved in tags.items():
            if _tag(root, name) != resolved:
                report.add("release.stale", "Baseline tag changed during release validation")
    except (MacrostatesError, OSError, UnicodeError, ValueError) as exc:
        report.add("release.invalid", str(exc))
    return report
