"""Synthetic role-only workflows retain lifecycle checks and historical evidence."""

import subprocess

import pytest

from macrostates._integration import check_workflows

from .test_integration_sync import codes
from .test_major_authority_policies import policy_project


def role_workflow(status, *, authorized=False):
    content = (
        "# Implementation validation\n\n"
        "- Project phase: active\n"
        "- Workflow type: Implementation update\n"
        f"- Status: {status}\n"
        "- Requested by: Definer\n"
        "- Implementer: AI-assisted implementation\n"
        "- Started at: 2026-01-01 12:00 UTC\n"
        "- Last updated at: 2026-01-01 12:00 UTC\n\n"
        "## Objective and scope\n\n"
        "Validate role-attributed workflow records using repository-local evidence.\n"
    )
    if authorized:
        content += (
            "\n## Closure authorization\n\n"
            "- Closure authorized by: Definer\n"
            "Authorization applies to the synthetic fixture's documented scope.\n"
        )
    return content


@pytest.mark.parametrize("process", ["6.0.0", "6.0.4"])
def test_role_only_workflow_and_work_capture_need_no_identity_lookup(
    tmp_path, monkeypatch, process
):
    project = policy_project(tmp_path, meta="3.0.0", process=process)
    original_run = subprocess.run

    def without_identity_lookup(arguments, *args, **kwargs):
        command = [str(item) for item in arguments]
        if command and command[0] == "git" and "config" in command:
            assert not any(item.startswith("user.") for item in command)
            assert not {"--list", "-l", "--get-regexp"}.intersection(command)
        return original_run(arguments, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", without_identity_lookup)
    project.start_work("workflow-validation")
    assert project.identity(work="workflow-validation")["baselines"] == {
        "specification": "specs-1.0.0",
        "implementation": "imp-1.0.0",
    }
    path = project.implementation / "workflows/2026-01-01__000001__validation.md"
    path.parent.mkdir()
    path.write_text(role_workflow("in_progress"))
    assert codes(check_workflows(tmp_path)) == {"workflow.open"}
    requested = project.closure_request()
    assert len(requested["workflows"]) == 1
    assert requested["workflows"][0]["title"] == "Implementation validation"
    path.write_text(role_workflow("completed", authorized=True))
    before = path.read_bytes()
    assert check_workflows(tmp_path).ok
    assert project.closure_request()["workflows"] == []
    assert project.check().ok
    assert path.read_bytes() == before


@pytest.mark.parametrize("process", ["5.0.0", "5.1.0", "6.0.0"])
@pytest.mark.parametrize("status", ["completed", "abandoned", "superseded"])
def test_historical_role_closure_evidence_is_read_without_rewriting(tmp_path, process, status):
    project = policy_project(tmp_path, meta="3.0.0", process=process)
    path = project.implementation / "workflows/history/2026-01-01__000001__validation.md"
    path.parent.mkdir(parents=True)
    path.write_text(role_workflow(status, authorized=True))
    before = path.read_bytes()
    assert project.closure_request()["workflows"] == []
    assert check_workflows(tmp_path).ok
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    "status,authorized,expected",
    [
        ("in_progress", False, "workflow.open"),
        ("in_progress", True, "workflow.open"),
        ("paused", False, "workflow.open"),
        ("blocked", False, "workflow.open"),
        ("completed", False, "workflow.authorization"),
        ("abandoned", False, "workflow.authorization"),
        ("superseded", False, "workflow.authorization"),
        ("unknown", True, "workflow.status"),
    ],
)
def test_public_document_policy_preserves_status_and_authorization_distinctions(
    tmp_path, status, authorized, expected
):
    project = policy_project(tmp_path, meta="3.0.0", process="6.0.0")
    path = project.implementation / "workflows/history/2026-01-01__000001__validation.md"
    path.parent.mkdir(parents=True)
    path.write_text(role_workflow(status, authorized=authorized))
    before = path.read_bytes()
    assert codes(check_workflows(tmp_path)) == {expected}
    assert len(project.closure_request()["workflows"]) == 1
    assert path.read_bytes() == before
