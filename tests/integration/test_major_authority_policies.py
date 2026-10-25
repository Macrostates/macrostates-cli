"""Reviewed authority policies preserve technical formats and existing readiness gates."""

import pytest
import yaml

from macrostates import MacrostatesError, Project

from ..conftest import FakeSource, composition
from .test_integration_sync import codes, commit_all, git, workflow


def policy_project(root, *, meta, process):
    source = FakeSource()
    source.add("meta", meta)
    source.add(
        "process",
        process,
        dependencies=[{"name": "meta", "version": meta, "constraint": "at_least"}],
    )
    manifest = composition(("meta", "process"), versions={"meta": meta, "process": process})
    manifest["project"]["version"] = "specs-1.0.0"
    project = Project.initialize(root, manifest=manifest, source=source)
    assert project.install().ok
    (project.implementation / "release.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 2,
                "version": "imp-1.0.0",
                "specification": "specs-1.0.0",
                "release_date": "2026-10-14",
            }
        )
    )
    (project.implementation / "main.md").write_text("# Implementation\n\nProject phase: active\n")
    git(root, "init", "--quiet", "--initial-branch=main")
    git(root, "config", "user.name", "Implementer")
    git(root, "config", "user.email", "fixture@example.invalid")
    commit_all(root, "Established baseline fixture")
    git(root, "switch", "--quiet", "-c", "feature/policy")
    return project


@pytest.mark.parametrize(
    "meta,process",
    [("2.2.0", "5.0.0"), ("3.0.0", "5.1.0"), ("3.0.7", "5.1.4"), ("3.0.0", "6.0.0")],
)
def test_reviewed_policies_plan_major_scope_without_removing_workflow_closure(
    tmp_path, meta, process
):
    project = policy_project(tmp_path, meta=meta, process=process)
    assert project.check().ok
    overview = (project.specs / "main.md").read_text()
    assert "follow the selected Meta layout" in overview
    assert "take precedence" not in overview
    original = git(tmp_path, "rev-parse", "HEAD")
    project.start_work("contract-update")
    workflow(project, status="in_progress", closure=False)
    change = project.create_change(
        "contract-update",
        "Implement an incompatible contract update",
        specification="major",
        implementation="major",
        work="contract-update",
        requirements=[
            {
                "requirement": "Revised contract fixture",
                "implementation": "Verified fixture implementation",
                "verification": "Recorded conformance fixture",
            }
        ],
        evidence=["Revised contract conformance verified in the fixture"],
    )
    before = change.read_bytes()
    commit_all(tmp_path, "Recorded Major scope with evidence")
    assert project.identity(work="contract-update")["baselines"] == {
        "specification": "specs-1.0.0",
        "implementation": "imp-1.0.0",
    }
    assert yaml.safe_load(before)["origin"]["commit"] == original
    plan = project.plan_release(target="main")
    assert plan["candidate"] == {
        "specification": "specs-2.0.0",
        "implementation": "imp-2.0.0",
        "implementation_specification": "specs-2.0.0",
    }
    assert yaml.safe_load(project.manifest.read_text())["project"]["version"] == "specs-1.0.0"
    project.prepare_release(plan, date="2026-10-14")
    commit_all(tmp_path, "Prepared candidate fixture")
    assert (project.implementation / "changes/history/contract-update.yaml").read_bytes() == before
    assert codes(project.check_release(target="main")) == {"workflow.open"}
    closed = workflow(project)
    history = closed.parent / "history"
    history.mkdir()
    closed.rename(history / closed.name)
    commit_all(tmp_path, "Recorded workflow closure fixture")
    assert project.check_release(target="main").ok
    assert project.check_integration(target="main").ok


@pytest.mark.parametrize("process", ["5.2.0", "6.1.0", "7.0.0"])
def test_future_process_cannot_use_reviewed_baseline_operations(tmp_path, process):
    project = policy_project(tmp_path, meta="3.0.0", process=process)
    before = git(tmp_path, "status", "--porcelain")
    assert "process.unsupported_policy" in codes(project.lint())
    with pytest.raises(MacrostatesError, match="explicitly selected Process"):
        project.identity()
    with pytest.raises(MacrostatesError, match="explicitly selected Process"):
        project.start_work("unreviewed")
    assert git(tmp_path, "status", "--porcelain") == before


@pytest.mark.parametrize("process", ["5.0.0", "5.1.0", "6.0.0"])
def test_reviewed_process_keeps_specification_only_and_active_baseline_rules(tmp_path, process):
    project = policy_project(tmp_path, meta="3.0.0", process=process)
    (project.implementation / "release.yaml").unlink()
    overview = project.implementation / "main.md"
    overview.write_text("# Implementation\n\nProject phase: specification\n")
    assert project.lint().ok
    overview.write_text("# Implementation\n\nProject phase: active\n")
    assert "process.release_missing" in codes(project.lint())
