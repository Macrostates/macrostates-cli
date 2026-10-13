"""Local proposal preparation, independent of a hosting review service."""

import re
import tempfile
from pathlib import Path
from typing import Any

from ._git import commit, dirty, git, primary_ref, ref
from ._io import safe_path
from ._models import MacrostatesError, Report

OPEN = {"in_progress", "paused", "blocked"}
CLOSED = {"completed", "abandoned", "superseded"}


def closure_evidence(content: str) -> bool:
    field = re.search(r"(?im)^\s*-\s*Closure authorized by:\s*(\S[^\n]*)$", content)
    if field and field[1].strip().casefold() not in {"unknown", "pending", "todo", "tbd", "none"}:
        return True
    for heading, body in re.findall(r"(?ims)^##\s+([^\n]+)\n(.*?)(?=^##\s|\Z)", content):
        if heading.strip().casefold() in {
            "authorized closure",
            "definer-confirmed closure",
            "closure authorization",
        }:
            text = body.strip()
            if (
                text
                and not text.casefold().startswith(("todo", "pending", "tbd"))
                and re.search(r"(?i)definer|user|confirm|authoriz|approv", text)
            ):
                return True
    return False


def workflow_records(root: Path) -> list[dict[str, Any]]:
    base = safe_path(root, ".macrostates/implementation/workflows")
    result = []
    if not base.exists():
        return result
    if any(path.is_symlink() for path in base.rglob("*")):
        raise MacrostatesError("Workflow files and directories must not be symbolic links")
    for path in sorted(base.rglob("*.md")):
        if path.is_symlink():
            raise MacrostatesError("Workflow records must not be symbolic links")
        content = path.read_text(encoding="utf-8")
        statuses = re.findall(r"^\s*(?:-\s*)?Status:\s*(\S+)\s*$", content, re.M | re.I)
        if path.name.casefold() in {"readme.md", "main.md"} and not statuses:
            continue
        title = next(
            (line.lstrip("# ") for line in content.splitlines() if line.startswith("#")), path.stem
        )
        result.append(
            {
                "path": path.relative_to(root).as_posix(),
                "title": title,
                "status": statuses[0] if len(statuses) == 1 else "invalid",
                "closure_authorized": closure_evidence(content),
            }
        )
    return result


def open_workflows(root: Path) -> list[dict[str, Any]]:
    return [
        item
        for item in workflow_records(root)
        if item["status"] not in CLOSED or not item["closure_authorized"]
    ]


def check_workflows(root: Path) -> Report:
    report = Report()
    for item in workflow_records(root):
        if item["status"] in OPEN:
            report.add(
                "workflow.open",
                "Definer-authorized closure is required before proposal preparation",
                item["path"],
            )
        elif item["status"] not in CLOSED:
            report.add(
                "workflow.status",
                "Workflow needs exactly one recognized status, including in history",
                item["path"],
            )
        elif not item["closure_authorized"]:
            report.add(
                "workflow.authorization",
                "Closed workflow must preserve explicit definer closure authorization",
                item["path"],
            )
    return report


def closure_request(root: Path) -> dict[str, Any]:
    """Prepare the required permission request; this never closes a workflow."""
    records = open_workflows(root)
    lines = [
        "Please authorize closure of these workflows. Closure is required to prepare the integration proposal:"
    ]
    for index, record in enumerate(records, 1):
        lines.append(f"{index}. {record['title']} ({record['status']})")
    return {
        "workflows": records,
        "message": "\n".join(lines) if records else "No open workflows found.",
    }


def check_integration(
    root: Path, *, target: str | None = None, expected_target: str | None = None
) -> Report:
    """Validate exact combined contents locally; external approvals remain separate."""
    from ._changes import check_changes
    from ._deliverables import check_deliverable_changes
    from ._project import Project

    report = Report()
    target = ref(target) if target is not None else primary_ref(root)
    selected = commit(root, target)
    source = commit(root)
    if expected_target is not None and selected != expected_target:
        report.add(
            "integration.stale", "Target changed; repeat preparation against the current target"
        )
        return report
    if dirty(root):
        report.add(
            "integration.dirty", "Commit the proposed changes before exact integration validation"
        )
        return report
    try:
        tree = git(root, "merge-tree", "--write-tree", selected, source).splitlines()[0]
    except MacrostatesError:
        report.add(
            "integration.conflict",
            "The proposed integration has conflicts; resolve them on the development branch",
        )
        return report
    # Export only tracked combined contents. Workflows hidden in history are still inspected.
    with tempfile.TemporaryDirectory(prefix="macrostates-integration-") as directory:
        snapshot = Path(directory)
        import subprocess

        from ._integrity import extract_archive

        try:
            archive = subprocess.run(
                ["git", "-C", str(root), "archive", "--format=tar", "--prefix=snapshot/", tree],
                capture_output=True,
                timeout=120,
                check=True,
            ).stdout
            extract_archive(archive, snapshot)
            project = Project.open(snapshot)
            report.diagnostics.extend(project.check().diagnostics)
            report.diagnostics.extend(
                check_deliverable_changes(snapshot, selected, repository_root=root).diagnostics
            )
            report.diagnostics.extend(check_workflows(snapshot).diagnostics)
            report.diagnostics.extend(check_changes(snapshot).diagnostics)
            changed = git(root, "diff", "--name-only", selected, tree).splitlines()
            if changed:
                declared = False
                changes = safe_path(snapshot, ".macrostates/implementation/changes")
                if changes.exists():
                    for record in changes.glob("*.yaml"):
                        relative = record.relative_to(snapshot).as_posix()
                        try:
                            previous = git(root, "show", selected + ":" + relative)
                        except MacrostatesError:
                            previous = None
                        if previous != record.read_text(encoding="utf-8").strip():
                            declared = True
                            break
                # A release proposal consumes existing records rather than adding a new feature record.
                plan = safe_path(snapshot, ".macrostates/implementation/release-plan.yaml")
                if not declared and plan.exists():
                    try:
                        previous_plan = git(
                            root,
                            "show",
                            selected + ":.macrostates/implementation/release-plan.yaml",
                        )
                    except MacrostatesError:
                        previous_plan = None
                    if previous_plan != plan.read_text(encoding="utf-8").strip():
                        candidate_report = Project.open(root).check_release(target=target)
                        report.diagnostics.extend(candidate_report.diagnostics)
                        declared = candidate_report.ok
                if not declared:
                    report.add(
                        "integration.scope_missing",
                        "Changed integration contents need a new or updated explicit change record, including no-bump decisions, or a validated release-preparation plan",
                    )
        except (OSError, subprocess.SubprocessError, MacrostatesError) as exc:
            report.add(
                "integration.invalid",
                str(exc)
                if isinstance(exc, MacrostatesError)
                else "Combined snapshot could not be validated",
            )
    if commit(root, target) != selected or commit(root) != source or dirty(root):
        report.add("integration.stale", "Repository changed during validation; repeat preparation")
    report.add(
        "integration.external",
        f"Validated source {source} against cached target {selected}; obtain required external checks/reviews and refresh remote state before integration",
        warning=True,
    )
    return report
