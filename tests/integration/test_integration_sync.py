import subprocess
from pathlib import Path

import pytest
import yaml

from macrostates import MacrostatesError, Project

from ..conftest import FakeSource, composition


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def commit_all(root: Path, message="Test change") -> str:
    git(root, "add", ".")
    git(root, "commit", "--quiet", "-m", message)
    return git(root, "rev-parse", "HEAD")


def make_project(tmp_path: Path, *, primary="main") -> Project:
    source = FakeSource()
    source.add("process", "5.0.0")
    manifest = composition(("process",), versions={"process": "5.0.0"})
    manifest["project"]["version"] = "specs-0.3.0"
    project = Project.initialize(tmp_path, manifest=manifest, source=source)
    assert project.install().ok
    (project.implementation / "release.yaml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 2,
                "version": "imp-0.3.1",
                "specification": "specs-0.3.0",
                "release_date": "2026-10-13",
            }
        )
    )
    git(tmp_path, "init", "--quiet", "--initial-branch=" + primary)
    git(tmp_path, "config", "user.name", "Test Maintainer")
    git(tmp_path, "config", "user.email", "maintainer@example.invalid")
    commit_all(tmp_path, "Finalized baseline")
    git(tmp_path, "switch", "--quiet", "-c", "feature/work")
    return project


def workflow(project, *, status="completed", history=False, closure=True, empty_closure=False):
    directory = project.implementation / "workflows"
    if history:
        directory /= "history"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / "2026-10-13__ABC123__work.md"
    content = "# Feature work\n\n"
    if status is not None:
        content += "Status: " + status + "\n"
    if closure:
        content += "\n## Authorized closure\n\n"
        if not empty_closure:
            content += "The definer explicitly approved closing this workflow on 2026-10-13.\n"
    path.write_text(content)
    return path


def codes(report):
    return {diagnostic.code for diagnostic in report.diagnostics}


@pytest.mark.parametrize("strategy", ["merge", "rebase"])
def test_synchronization_preserves_original_change_provenance(tmp_path, strategy):
    project = make_project(tmp_path)
    change = project.create_change(
        "feature-work",
        "Restore specified behavior",
        specification="none",
        implementation="patch",
        evidence=["Behavior regression checked"],
    )
    original_bytes = change.read_bytes()
    original_origin = yaml.safe_load(original_bytes)["origin"]
    before = commit_all(tmp_path, "Feature with impact record")
    git(tmp_path, "switch", "--quiet", "main")
    (tmp_path / "upstream.txt").write_text("Accepted upstream change\n")
    upstream = commit_all(tmp_path, "Upstream change")
    git(tmp_path, "switch", "--quiet", "feature/work")

    status = project.branch_status()
    assert (status["ahead"], status["behind"]) == (1, 1)
    result = project.sync_branch(target="main", strategy=strategy)
    assert result["previous_commit"] == before
    assert result["target_commit"] == upstream
    assert result["behind"] == 0
    assert result["branch"] == "feature/work"
    assert "cached" in result["remote_freshness"]
    assert change.read_bytes() == original_bytes
    assert yaml.safe_load(change.read_bytes())["origin"] == original_origin
    assert (tmp_path / "upstream.txt").read_text() == "Accepted upstream change\n"
    assert git(tmp_path, "status", "--porcelain") == ""


@pytest.mark.parametrize("primary", ["main", "master"])
def test_synchronization_refuses_detected_primary_branch(tmp_path, primary):
    project = make_project(tmp_path, primary=primary)
    git(tmp_path, "switch", "--quiet", primary)
    before = git(tmp_path, "rev-parse", "HEAD")
    with pytest.raises(MacrostatesError, match="primary branch"):
        project.sync_branch(target=primary, strategy="merge")
    assert git(tmp_path, "rev-parse", "HEAD") == before


@pytest.mark.parametrize("dirty_kind", ["untracked", "tracked", "staged"])
def test_synchronization_preserves_dirty_work_without_stashing(tmp_path, dirty_kind):
    project = make_project(tmp_path)
    path = tmp_path / "AGENTS.md" if dirty_kind != "untracked" else tmp_path / "local.txt"
    path.write_text("Unfinished developer work\n")
    if dirty_kind == "staged":
        git(tmp_path, "add", str(path.relative_to(tmp_path)))
    before = git(tmp_path, "status", "--porcelain")
    with pytest.raises(MacrostatesError, match="local changes"):
        project.sync_branch(target="main", strategy="merge")
    assert path.read_text() == "Unfinished developer work\n"
    assert git(tmp_path, "status", "--porcelain") == before
    assert git(tmp_path, "stash", "list") == ""


def test_synchronization_refuses_detached_head(tmp_path):
    project = make_project(tmp_path)
    git(tmp_path, "switch", "--quiet", "--detach", "HEAD")
    with pytest.raises(MacrostatesError, match="attached development branch"):
        project.sync_branch(target="main", strategy="rebase")


@pytest.mark.parametrize("strategy", ["merge", "rebase"])
def test_synchronization_leaves_conflicts_for_the_implementer(tmp_path, strategy):
    project = make_project(tmp_path)
    (tmp_path / "shared.txt").write_text("Feature branch content\n")
    commit_all(tmp_path, "Feature edit")
    git(tmp_path, "switch", "--quiet", "main")
    (tmp_path / "shared.txt").write_text("Upstream content\n")
    commit_all(tmp_path, "Conflicting upstream edit")
    git(tmp_path, "switch", "--quiet", "feature/work")
    with pytest.raises(MacrostatesError, match="resolve conflicts"):
        project.sync_branch(target="main", strategy=strategy)
    conflict = (tmp_path / "shared.txt").read_text()
    assert "Feature branch content" in conflict
    assert "Upstream content" in conflict
    assert "<<<<<<<" in conflict
    assert "AA shared.txt" in git(tmp_path, "status", "--porcelain")
    with pytest.raises(MacrostatesError):
        project.sync_branch(target="main", strategy=strategy)
    assert (tmp_path / "shared.txt").read_text() == conflict


@pytest.mark.parametrize("primary", ["main", "master"])
@pytest.mark.parametrize("override", ["qualified", "different"])
def test_primary_alias_or_override_cannot_bypass_the_guard(tmp_path, primary, override):
    project = make_project(tmp_path, primary=primary)
    git(tmp_path, "switch", "--quiet", primary)
    supplied = "refs/heads/" + primary if override == "qualified" else "feature/work"
    with pytest.raises(MacrostatesError, match="primary branch"):
        project.sync_branch(target=primary, strategy="merge", primary=supplied)


@pytest.mark.parametrize("primary", ["main", "master"])
def test_primary_configuration_accepts_a_full_local_branch_reference(tmp_path, primary):
    project = make_project(tmp_path, primary=primary)
    git(tmp_path, "config", "macrostates.primaryBranch", "refs/heads/" + primary)
    git(tmp_path, "switch", "--quiet", primary)
    with pytest.raises(MacrostatesError, match="primary branch"):
        project.sync_branch(target=primary, strategy="merge")


def test_explicit_custom_primary_branch_can_be_synchronized(tmp_path):
    project = make_project(tmp_path, primary="trunk")
    result = project.sync_branch(target="trunk", strategy="merge", primary="trunk")
    assert result["branch"] == "feature/work"
    assert result["behind"] == 0


def test_explicit_fetch_uses_configured_local_remote(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    project = make_project(root)
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "clone", "--quiet", "--bare", str(root), str(remote)], check=True)
    git(root, "remote", "add", "origin", str(remote))
    git(root, "switch", "--quiet", "main")
    (root / "upstream.txt").write_text("Fetched upstream work\n")
    selected = commit_all(root, "Advance remote primary")
    git(root, "push", "--quiet", "origin", "main")
    git(root, "update-ref", "-d", "refs/remotes/origin/main")
    git(root, "switch", "--quiet", "feature/work")

    result = project.sync_branch(target="origin/main", strategy="merge", fetch_remote="origin")
    assert result["target_commit"] == selected
    assert result["remote_freshness"] == "fetched configured remote before synchronization"
    assert result["behind"] == 0


@pytest.mark.parametrize("value", ["--help", "main\nunsafe", "main unsafe"])
def test_sync_ref_injection_is_rejected_without_changing_head(tmp_path, value):
    project = make_project(tmp_path)
    before = git(tmp_path, "rev-parse", "HEAD")
    with pytest.raises(MacrostatesError):
        project.sync_branch(target=value, strategy="merge")
    assert git(tmp_path, "rev-parse", "HEAD") == before


@pytest.mark.parametrize("status", ["in_progress", "paused", "blocked"])
@pytest.mark.parametrize("history", [False, True])
def test_open_workflows_block_preparation_even_when_archived(tmp_path, status, history):
    project = make_project(tmp_path)
    path = workflow(project, status=status, history=history)
    commit_all(tmp_path)
    request = project.closure_request()
    assert len(request["workflows"]) == 1
    assert request["workflows"][0]["path"] == path.relative_to(tmp_path).as_posix()
    assert "1. Feature work" in request["message"]
    assert "required" in request["message"]
    assert "workflow.open" in codes(project.check_integration())
    assert status in path.read_text()


@pytest.mark.parametrize("name", ["README.md", "main.md"])
@pytest.mark.parametrize("history", [False, True])
def test_renaming_open_workflow_as_an_index_cannot_bypass_the_gate(tmp_path, name, history):
    project = make_project(tmp_path)
    original = workflow(project, status="in_progress", history=history)
    path = original.with_name(name)
    original.rename(path)
    commit_all(tmp_path)
    assert "workflow.open" in codes(project.check_integration())
    assert any(
        record["path"] == path.relative_to(tmp_path).as_posix()
        for record in project.closure_request()["workflows"]
    )


def test_workflow_index_without_record_status_remains_allowed(tmp_path):
    project = make_project(tmp_path)
    project.create_change(
        "workflow-index",
        "Document completed workflow records",
        specification="none",
        implementation="none",
        origin_commit=git(tmp_path, "rev-parse", "main"),
    )
    record = workflow(project)
    (record.parent / "README.md").write_text(
        "# Completed workflows\n\n[Feature work](" + record.name + ")\n"
    )
    commit_all(tmp_path)
    assert project.check_integration().ok


@pytest.mark.parametrize("status", ["completed", "abandoned", "superseded"])
def test_closed_workflows_require_preserved_definer_authorization(tmp_path, status):
    project = make_project(tmp_path)
    project.create_change(
        "workflow-closure",
        "Record authorized workflow closure",
        specification="none",
        implementation="none",
        origin_commit=git(tmp_path, "rev-parse", "main"),
    )
    path = workflow(project, status=status, closure=False)
    commit_all(tmp_path)
    assert "workflow.authorization" in codes(project.check_integration())
    path.write_text(
        path.read_text() + "\n## Definer-confirmed closure\n\nDefiner approved closure.\n"
    )
    commit_all(tmp_path)
    report = project.check_integration()
    assert report.ok, report.diagnostics
    assert "integration.external" in codes(report)
    assert project.closure_request()["workflows"] == []


@pytest.mark.parametrize("relative", ["src/example.py", ".macrostates/implementation/notes.md"])
def test_changed_integration_contents_need_an_explicit_scope_record(tmp_path, relative):
    project = make_project(tmp_path)
    path = tmp_path / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("Changed project content\n")
    commit_all(tmp_path)
    assert "integration.scope_missing" in codes(project.check_integration())


def test_empty_closure_heading_does_not_fabricate_authorization(tmp_path):
    project = make_project(tmp_path)
    workflow(project, empty_closure=True)
    commit_all(tmp_path)
    assert "workflow.authorization" in codes(project.check_integration())


@pytest.mark.parametrize("status", [None, "unknown", "completed\nStatus: completed"])
def test_missing_unknown_or_duplicate_workflow_status_blocks_integration(tmp_path, status):
    project = make_project(tmp_path)
    workflow(project, status=status)
    commit_all(tmp_path)
    assert "workflow.status" in codes(project.check_integration())


def test_readiness_checks_the_combined_tree_including_target_history(tmp_path):
    project = make_project(tmp_path)
    (tmp_path / "feature.txt").write_text("Feature work\n")
    commit_all(tmp_path, "Feature change")
    git(tmp_path, "switch", "--quiet", "main")
    inherited = workflow(project, status="paused", history=True)
    commit_all(tmp_path, "Historical target workflow")
    git(tmp_path, "switch", "--quiet", "feature/work")
    assert not inherited.exists()
    report = project.check_integration()
    assert "workflow.open" in codes(report)
    assert any(
        item.path == inherited.relative_to(tmp_path).as_posix() for item in report.diagnostics
    )


def test_integration_checks_explicit_requirement_gaps(tmp_path):
    project = make_project(tmp_path)
    project.create_change(
        "incomplete",
        "Compatible requirement addition",
        specification="minor",
        implementation="minor",
        requirements=[
            {
                "requirement": "Works offline",
                "implementation": "Pending offline command",
                "verification": "Partial behavior check",
            }
        ],
        evidence=["Partial check"],
        gaps=["Required offline path is missing"],
    )
    commit_all(tmp_path)
    assert "change.gaps" in codes(project.check_integration())


def test_changed_target_invalidates_preparation(tmp_path):
    project = make_project(tmp_path)
    expected = git(tmp_path, "rev-parse", "main")
    git(tmp_path, "switch", "--quiet", "main")
    (tmp_path / "accepted.txt").write_text("Later integration\n")
    commit_all(tmp_path)
    git(tmp_path, "switch", "--quiet", "feature/work")
    assert "integration.stale" in codes(project.check_integration(expected_target=expected))


def test_target_moving_during_validation_invalidates_the_result(tmp_path, monkeypatch):
    project = make_project(tmp_path)
    original_check = Project.check
    moved = False

    def check_and_advance(snapshot, **kwargs):
        nonlocal moved
        result = original_check(snapshot, **kwargs)
        if not moved and snapshot.root != tmp_path:
            tree = git(tmp_path, "rev-parse", "main^{tree}")
            parent = git(tmp_path, "rev-parse", "main")
            replacement = git(
                tmp_path, "commit-tree", tree, "-p", parent, "-m", "Concurrent integration"
            )
            git(tmp_path, "update-ref", "refs/heads/main", replacement, parent)
            moved = True
        return result

    monkeypatch.setattr(Project, "check", check_and_advance)
    assert "integration.stale" in codes(project.check_integration())
    assert moved


def test_dirty_integration_source_is_not_exported_as_validated(tmp_path):
    project = make_project(tmp_path)
    (tmp_path / "uncommitted.txt").write_text("Uncommitted work\n")
    assert "integration.dirty" in codes(project.check_integration())


def test_integration_conflicts_are_reported_without_mutating_the_worktree(tmp_path):
    project = make_project(tmp_path)
    (tmp_path / "shared.txt").write_text("Feature\n")
    feature = commit_all(tmp_path)
    git(tmp_path, "switch", "--quiet", "main")
    (tmp_path / "shared.txt").write_text("Target\n")
    commit_all(tmp_path)
    git(tmp_path, "switch", "--quiet", "feature/work")
    assert "integration.conflict" in codes(project.check_integration())
    assert git(tmp_path, "rev-parse", "HEAD") == feature
    assert git(tmp_path, "status", "--porcelain") == ""
    assert (tmp_path / "shared.txt").read_text() == "Feature\n"
