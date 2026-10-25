"""Public command boundaries for the baseline and application workflow."""

import json

import pytest
import yaml

from macrostates import Project
from macrostates._cli import main

from .test_integration_sync import codes, commit_all, git, make_project, workflow


def invoke(project, capsys, *arguments, global_first=False):
    options = ["--project", str(project.root), "--json"]
    status = main([*options, *arguments] if global_first else [*arguments, *options])
    output = capsys.readouterr()
    assert "Traceback" not in output.err
    return status, json.loads(output.out)


@pytest.mark.parametrize(
    "command,option",
    [
        ("identity", "--work"),
        ("start-work", "--origin-commit"),
        ("change-create", "--implementation-impact"),
        ("branch-sync", "--fetch-remote"),
        ("integration-check", "--expected-target"),
        ("release-prepare", "--plan"),
        ("release-check", "--publication"),
    ],
)
def test_versioning_commands_explain_their_options(capsys, command, option):
    with pytest.raises(SystemExit) as stopped:
        main([command, "--help"])
    assert stopped.value.code == 0
    assert option in capsys.readouterr().out


@pytest.mark.parametrize("global_first", [False, True])
def test_identity_json_accepts_global_options_on_either_side(tmp_path, capsys, global_first):
    project = make_project(tmp_path)
    before = git(tmp_path, "status", "--porcelain")
    status, payload = invoke(project, capsys, "identity", global_first=global_first)
    assert status == 0
    assert payload["baselines"] == {
        "specification": "specs-0.3.0",
        "implementation": "imp-0.3.1",
    }
    assert payload["branch"] == "feature/work"
    assert payload["dirty"] is False
    assert git(tmp_path, "status", "--porcelain") == before


def test_cli_captured_origin_survives_new_primary_baseline(tmp_path, capsys):
    project = make_project(tmp_path)
    origin = git(tmp_path, "rev-parse", "HEAD")
    status, captured = invoke(project, capsys, "start-work", "--id", "offline")
    assert status == 0
    path = project.root / captured["path"]
    original_bytes = path.read_bytes()
    commit_all(tmp_path, "Capture feature origin")
    git(tmp_path, "switch", "--quiet", "main")
    release = yaml.safe_load((project.implementation / "release.yaml").read_text())
    release["version"] = "imp-0.3.2"
    (project.implementation / "release.yaml").write_text(yaml.safe_dump(release))
    commit_all(tmp_path, "New accepted baseline")
    git(tmp_path, "switch", "--quiet", "feature/work")
    status, synced = invoke(
        project, capsys, "branch-sync", "--target", "main", "--strategy", "merge"
    )
    assert status == 0
    assert synced["behind"] == 0
    status, created = invoke(
        project,
        capsys,
        "change-create",
        "--id",
        "offline-fix",
        "--work",
        "offline",
        "--summary",
        "Restore required offline behavior",
        "--specification-impact",
        "none",
        "--implementation-impact",
        "patch",
        "--evidence",
        "Offline regression passes",
    )
    assert status == 0
    record = yaml.safe_load((project.root / created["path"]).read_text())
    assert record["origin"]["commit"] == origin
    assert record["origin"]["implementation"] == "imp-0.3.1"
    assert path.read_bytes() == original_bytes
    status, identity = invoke(project, capsys, "identity", "--work", "offline")
    assert status == 0
    assert identity["implementation"].startswith("imp-0.3.1-branch.feature-work.g")


def test_cli_release_plan_round_trips_into_candidate_preparation(tmp_path, capsys):
    project = make_project(tmp_path)
    status, _ = invoke(
        project,
        capsys,
        "change-create",
        "--id",
        "fix",
        "--summary",
        "Restore specified behavior",
        "--specification-impact",
        "none",
        "--implementation-impact",
        "patch",
        "--evidence",
        "Regression test passed",
    )
    assert status == 0
    commit_all(tmp_path, "Completed implementation work")
    before = git(tmp_path, "status", "--porcelain")
    status, planned = invoke(project, capsys, "release-plan")
    assert status == 0
    assert planned["candidate"]["implementation"] == "imp-0.3.2"
    assert git(tmp_path, "status", "--porcelain") == before
    plan_file = tmp_path.parent / (tmp_path.name + "-plan.json")
    plan_file.write_text(json.dumps(planned))
    status, candidate = invoke(
        project, capsys, "release-prepare", "--plan", str(plan_file), "--date", "2026-10-13"
    )
    assert status == 0
    assert candidate["status"] == "candidate"
    assert (project.implementation / "changes/history/fix.yaml").is_file()
    assert not (project.implementation / "changes/fix.yaml").exists()
    assert (
        yaml.safe_load((project.implementation / "release.yaml").read_text())["version"]
        == "imp-0.3.2"
    )


def test_cli_reports_defaults_and_independent_application_without_writes(tmp_path, capsys):
    project = make_project(tmp_path)
    path = project.implementation / "deliverables.yaml"
    path.write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "deliverables": {
                    "library": {
                        "strategy": "independent",
                        "version": "4.12.3",
                        "version_scheme": "semver",
                    },
                    "android": {"android": {"version_code": 84}},
                },
            }
        )
    )
    before = path.read_bytes()
    status, payload = invoke(project, capsys, "deliverables")
    assert status == 0
    entries = payload.get("deliverables", payload)
    assert entries["android"]["version"] == "0.3.1"
    assert entries["library"]["version"] == "4.12.3"
    assert path.read_bytes() == before


def test_cli_closure_request_is_read_only_and_lists_every_open_workflow(tmp_path, capsys):
    project = make_project(tmp_path)
    first = workflow(project, status="in_progress", closure=False)
    second = first.with_name("2026-10-13__ABC124__paused.md")
    second.write_text("# Paused separate work\nStatus: paused\n")
    before = {path.name: path.read_bytes() for path in (first, second)}
    status, payload = invoke(project, capsys, "closure-request")
    assert status == 0
    assert len(payload["workflows"]) == 2
    assert "1." in payload["message"] and "2." in payload["message"]
    assert "required" in payload["message"]
    assert {path.name: path.read_bytes() for path in (first, second)} == before


def test_cli_distinguishes_failed_readiness_from_invalid_operation(tmp_path, capsys):
    project = make_project(tmp_path)
    invoke(
        project,
        capsys,
        "change-create",
        "--id",
        "unfinished",
        "--summary",
        "Pending fix",
        "--specification-impact",
        "none",
        "--implementation-impact",
        "patch",
        "--gap",
        "Fix still absent",
    )
    status, failed = invoke(project, capsys, "change-check")
    assert status == 1
    assert failed["ok"] is False
    assert "change.gaps" in {item["code"] for item in failed["diagnostics"]}
    status, invalid = invoke(project, capsys, "identity", "--work", "does-not-exist")
    assert status == 2
    assert invalid["error"]["code"] == "operation.invalid"


def test_late_cli_change_creation_needs_an_explicit_original_commit(tmp_path, capsys):
    project = make_project(tmp_path)
    origin = git(tmp_path, "rev-parse", "HEAD")
    (tmp_path / "app.py").write_text("print('new behavior')\n")
    commit_all(tmp_path, "Develop before declaring scope")
    arguments = [
        "change-create",
        "--id",
        "late",
        "--summary",
        "Completed behavior fix",
        "--specification-impact",
        "none",
        "--implementation-impact",
        "patch",
        "--evidence",
        "Regression passed",
    ]
    status, refused = invoke(project, capsys, *arguments)
    assert status == 2
    assert "provenance" in refused["error"]["message"]
    assert not (project.implementation / "changes/late.yaml").exists()
    status, accepted = invoke(project, capsys, *arguments, "--origin-commit", origin)
    assert status == 0
    assert yaml.safe_load((tmp_path / accepted["path"]).read_text())["origin"]["commit"] == origin


@pytest.mark.parametrize(
    "meta,process",
    [
        ("2.2.0", "5.0.0"),
        ("3.0.0", "5.1.0"),
        ("3.0.7", "5.1.4"),
        ("3.0.0", "6.0.0"),
        ("3.0.0", "6.0.4"),
    ],
)
def test_cli_new_policy_shorthand_creates_only_specification_seed(tmp_path, capsys, meta, process):
    status = main(
        [
            "init",
            "--project",
            str(tmp_path),
            "--name",
            "example",
            "--package",
            "meta@" + meta,
            "--package",
            "process@" + process,
            "--json",
        ]
    )
    assert status == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    project = Project.open(tmp_path)
    assert yaml.safe_load(project.manifest.read_text())["project"]["version"] == "specs-0.1.0"
    assert not (project.implementation / "release.yaml").exists()


def test_process5_allows_specification_only_but_refuses_active_without_implementation(tmp_path):
    project = make_project(tmp_path)
    (project.implementation / "release.yaml").unlink()
    overview = project.implementation / "main.md"
    overview.write_text("# Implementation\n\nProject phase: specification\n")
    assert project.lint().ok
    overview.write_text("# Implementation\n\nProject phase: active\n")
    assert "process.release_missing" in codes(project.lint())
