"""Concurrent work, exact plans and immutable baselines in real temporary Git repos."""

import copy
import subprocess
from pathlib import Path

import pytest

from macrostates._changes import check_changes, create_change, load_changes, start_work
from macrostates._git import commit
from macrostates._io import dump_yaml, read_yaml
from macrostates._models import MacrostatesError
from macrostates._release import check_release, plan_release, prepare_release
from macrostates._versioning import aggregate, identity


def run(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def save(root: Path, message: str) -> str:
    run(root, "add", "--all")
    run(root, "commit", "-m", message)
    return commit(root)


@pytest.fixture
def repository(tmp_path):
    run(tmp_path, "init", "-b", "main")
    run(tmp_path, "config", "user.name", "Test Author")
    run(tmp_path, "config", "user.email", "test@example.invalid")
    specs = tmp_path / ".macrostates/specs"
    specs.mkdir(parents=True)
    (specs / "composition.yaml").write_text(
        dump_yaml(
            {
                "schema_version": 1,
                "project": {"name": "example", "version": "specs-0.3.0"},
                "packages": [{"name": "process", "version": "5.0.0"}],
            }
        ),
        encoding="utf-8",
    )
    (specs / "main.md").write_text("# Requirements\n\nOffline operation is required.\n")
    implementation = tmp_path / ".macrostates/implementation"
    implementation.mkdir()
    (implementation / "release.yaml").write_text(
        dump_yaml(
            {
                "schema_version": 2,
                "version": "imp-0.3.1",
                "specification": "specs-0.3.0",
                "release_date": "2026-10-01",
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "app.py").write_text("print('original')\n")
    save(tmp_path, "Initial finalized baseline")
    run(tmp_path, "tag", "-a", "specs-0.3.0", "-m", "Specification baseline")
    run(tmp_path, "tag", "-a", "imp-0.3.1", "-m", "Implementation baseline")
    run(tmp_path, "checkout", "-b", "feature/fix")
    return tmp_path


def record(root, name="fix", *, spec="none", imp="patch", evidence=True, requirements=None):
    return create_change(
        root,
        name,
        "Restore required offline behavior",
        spec,
        imp,
        evidence=["Offline test passes"] if evidence else [],
        requirements=requirements,
    )


def integrated_change(root, *, spec="none", imp="patch"):
    record(
        root,
        spec=spec,
        imp=imp,
        requirements=[
            {
                "requirement": "Offline operation",
                "implementation": "app.py",
                "verification": "Offline test",
            }
        ]
        if spec in {"minor", "major"} or imp in {"minor", "major"}
        else [],
    )
    save(root, "Completed feature and impact record")
    run(root, "checkout", "main")
    run(root, "merge", "--no-ff", "feature/fix", "-m", "Integrate feature")
    run(root, "checkout", "-b", "release/next")


def candidate(root, *, spec="none", imp="patch"):
    integrated_change(root, spec=spec, imp=imp)
    plan = plan_release(root)
    prepare_release(root, plan, date="2026-10-13")
    save(root, "Prepare release candidate")
    return plan


@pytest.mark.parametrize(
    "impacts,expected",
    [
        (
            [{"specification": "none", "implementation": "patch"}] * 2,
            {"specification": "specs-0.3.0", "implementation": "imp-0.3.2"},
        ),
        (
            [{"specification": "patch", "implementation": "none"}],
            {"specification": "specs-0.3.1", "implementation": "imp-0.3.1"},
        ),
        (
            [{"specification": "patch", "implementation": "patch"}],
            {"specification": "specs-0.3.1", "implementation": "imp-0.3.2"},
        ),
        (
            [{"specification": "minor", "implementation": "minor"}],
            {"specification": "specs-0.4.0", "implementation": "imp-0.4.0"},
        ),
        (
            [{"specification": "major", "implementation": "major"}],
            {"specification": "specs-1.0.0", "implementation": "imp-1.0.0"},
        ),
        (
            [{"specification": "none", "implementation": "none"}],
            {"specification": "specs-0.3.0", "implementation": "imp-0.3.1"},
        ),
    ],
)
def test_aggregate_is_per_release_not_per_record(impacts, expected):
    assert aggregate("specs-0.3.0", "imp-0.3.1", impacts) == expected


def test_development_identity_changes_without_rewriting_original_baseline(repository):
    original = commit(repository)
    path = record(repository)
    save(repository, "Record scope")
    first = identity(repository, "fix")
    origin = read_yaml(path)["origin"]
    run(repository, "checkout", "main")
    (repository / "README.md").write_text("New upstream documentation\n")
    save(repository, "Upstream change")
    run(repository, "checkout", "feature/fix")
    run(repository, "merge", "--no-ff", "main", "-m", "Synchronize with primary")
    second = identity(repository, "fix")
    assert read_yaml(path)["origin"] == origin
    assert origin["commit"] == original
    assert second["baselines"] == first["baselines"]
    assert first["implementation"] != second["implementation"]
    assert second["implementation"].startswith("imp-0.3.1-branch.feature-fix.g")


def test_captured_work_preserves_origin_when_scope_is_declared_after_sync(repository):
    original = commit(repository)
    work = start_work(repository, "offline")
    save(repository, "Capture work starting point")
    (repository / "app.py").write_text("print('offline')\n")
    save(repository, "Implement behavior before declaring scope")
    run(repository, "checkout", "main")
    (repository / "README.md").write_text("Concurrent upstream change\n")
    save(repository, "Upstream update")
    run(repository, "checkout", "feature/fix")
    run(repository, "merge", "--no-ff", "main", "-m", "Update development branch")
    changed = create_change(
        repository,
        "offline-change",
        "Offline correction",
        "none",
        "patch",
        work="offline",
        evidence=["Offline tests pass"],
    )
    assert read_yaml(changed)["origin"] == read_yaml(work)["origin"]
    assert read_yaml(changed)["origin"]["commit"] == original
    assert identity(repository, "offline")["baselines"]["implementation"] == "imp-0.3.1"


def test_late_scope_without_captured_origin_is_refused(repository):
    original = commit(repository)
    (repository / "app.py").write_text("print('changed')\n")
    save(repository, "Develop before recording provenance")
    with pytest.raises(MacrostatesError, match="Late work"):
        record(repository)
    path = create_change(
        repository, "fix", "Restore behavior", "none", "patch", origin_commit=original
    )
    assert read_yaml(path)["origin"]["commit"] == original


def test_explicit_legacy_origin_is_normalized_without_rewriting_its_commit(repository):
    manifest = repository / ".macrostates/specs/composition.yaml"
    data = read_yaml(manifest)
    data["project"]["version"] = "spec-0.3.0"
    manifest.write_text(dump_yaml(data))
    declaration = repository / ".macrostates/implementation/release.yaml"
    declaration.write_text(
        'version: "0.3.1"\nspecification: "spec-0.3.0"\nrelease_date: "2026-10-01"\n'
    )
    legacy = save(repository, "Historical legacy declarations")
    run(repository, "reset", "--hard", "main")
    path = start_work(repository, "historical", origin_commit=legacy)
    assert read_yaml(path)["origin"] == {
        "commit": legacy,
        "specification": "specs-0.3.0",
        "implementation": "imp-0.3.1",
    }


def test_unselected_pending_source_never_claims_old_stable_identity(repository):
    record(repository)
    save(repository, "Pending change")
    result = identity(repository)
    assert result["state"] == "unreleased"
    assert result["implementation"].startswith("imp-0.3.1-unreleased.g")
    (repository / "app.py").write_text("Uncommitted work\n")
    assert identity(repository)["implementation"].endswith(".dirty")


def test_no_git_archive_reports_identity_unavailable(repository):
    import shutil

    shutil.rmtree(repository / ".git")
    result = identity(repository)
    assert result["state"] == "unavailable"
    assert result["implementation"] is None
    assert result["baselines"]["implementation"] == "imp-0.3.1"


def test_nested_composition_does_not_claim_parent_git_identity(repository):
    import shutil

    nested = repository / "component"
    shutil.copytree(repository / ".macrostates", nested / ".macrostates")
    result = identity(nested)
    assert result["state"] == "unavailable"
    assert result["commit"] is None
    assert result["implementation"] is None
    assert result["baselines"]["implementation"] == "imp-0.3.1"
    assert "repository root" in result["message"]


def test_record_creation_accepts_incomplete_scope_but_readiness_does_not(repository):
    record(repository, spec="minor", imp="minor", evidence=False)
    assert check_changes(repository, readiness=False).ok
    codes = {item.code for item in check_changes(repository).diagnostics}
    assert codes == {"change.evidence_missing", "change.coverage_missing"}


def test_record_id_collision_and_open_gap_are_not_hidden_in_history(repository):
    path = record(repository)
    data = read_yaml(path)
    data["gaps"] = ["Offline behavior is incomplete"]
    path.write_text(dump_yaml(data))
    assert not check_changes(repository).ok
    history = path.parent / "history"
    history.mkdir()
    (history / path.name).write_bytes(path.read_bytes())
    with pytest.raises(MacrostatesError, match="Duplicate"):
        load_changes(repository)


def test_primary_branch_cannot_create_records_even_with_custom_name(repository):
    run(repository, "checkout", "main")
    run(repository, "branch", "-m", "production")
    run(repository, "config", "macrostates.primaryBranch", "production")
    with pytest.raises(MacrostatesError, match="primary"):
        record(repository)


def test_two_parallel_changes_merge_without_reserving_the_next_version(repository):
    base = commit(repository)
    record(repository, "first")
    save(repository, "First change")
    run(repository, "checkout", "-b", "feature/second", base)
    record(repository, "second")
    save(repository, "Second change")
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "feature/fix", "-m", "First integration")
    run(repository, "merge", "--no-ff", "feature/second", "-m", "Second integration")
    plan = plan_release(repository)
    assert [item["id"] for item in plan["records"]] == ["first", "second"]
    assert plan["candidate"]["implementation"] == "imp-0.3.2"
    assert (
        read_yaml(repository / ".macrostates/implementation/release.yaml")["version"] == "imp-0.3.1"
    )


@pytest.mark.parametrize("change", ["record", "history", "target", "plan"])
def test_stale_inputs_or_altered_plan_refuse_preparation_without_edits(repository, change):
    integrated_change(repository)
    plan = plan_release(repository)
    if change == "record":
        path = repository / ".macrostates/implementation/changes/fix.yaml"
        path.write_text(path.read_text() + "extension: changed\n")
        save(repository, "Alter planned record")
    elif change == "history":
        path = repository / ".macrostates/implementation/changes/fix.yaml"
        history = path.parent / "history"
        history.mkdir()
        path.rename(history / path.name)
        save(repository, "Consume planned work elsewhere")
    elif change == "target":
        run(repository, "checkout", "main")
        (repository / "README.md").write_text("Concurrent upstream work\n")
        save(repository, "Advance primary")
        run(repository, "checkout", "release/next")
    else:
        plan = copy.deepcopy(plan)
        plan["candidate"]["implementation"] = "imp-0.3.99"
    before = commit(repository)
    original_release = (repository / ".macrostates/implementation/release.yaml").read_bytes()
    with pytest.raises(MacrostatesError):
        prepare_release(repository, plan, date="2026-10-13")
    assert commit(repository) == before
    assert (
        repository / ".macrostates/implementation/release.yaml"
    ).read_bytes() == original_release
    assert not (repository / ".macrostates/implementation/release-plan.yaml").exists()


def test_release_source_and_integration_target_have_separate_bindings(repository):
    integrated_change(repository)
    upstream = commit(repository, "main")
    workflow = repository / ".macrostates/implementation/workflows/preparation.md"
    workflow.parent.mkdir()
    workflow.write_text(
        "# Preparation\n\n- Status: completed\n- Closure authorized by: Definer approved closure.\n"
    )
    save(repository, "Record authorized preparation workflow")
    plan = plan_release(repository)
    assert plan["integration_target"] == upstream
    assert plan["target_commit"] != upstream
    prepare_release(repository, plan, date="2026-10-13")
    save(repository, "Prepare candidate after workflow tracking")
    assert check_release(repository).ok


def test_release_planning_requires_current_primary_to_be_included(repository):
    record(repository)
    save(repository, "Unsynchronized development work")
    run(repository, "checkout", "main")
    (repository / "README.md").write_text("New primary requirements context\n")
    save(repository, "Primary advanced")
    run(repository, "checkout", "feature/fix")
    with pytest.raises(MacrostatesError, match="Synchronize"):
        plan_release(repository)


def test_detached_ci_plans_against_cached_remote_without_local_primary(repository):
    integrated_change(repository)
    target = commit(repository, "main")
    run(repository, "update-ref", "refs/remotes/origin/main", target)
    run(repository, "checkout", "--detach", "main")
    run(repository, "branch", "-D", "main")
    plan = plan_release(repository)
    assert plan["integration_ref"] == "refs/remotes/origin/main"
    assert plan["integration_target"] == target == plan["target_commit"]
    assert identity(repository)["branch"] == "detached"
    assert identity(repository)["state"] == "unreleased"


def test_explicit_upstream_target_does_not_update_stale_local_primary(repository):
    integrated_change(repository)
    local_primary = commit(repository, "main")
    run(repository, "checkout", "-b", "upstream/simulation", "main")
    (repository / "README.md").write_text("Upstream integrated documentation\n")
    upstream = save(repository, "Upstream accepted changes")
    run(repository, "update-ref", "refs/remotes/upstream/main", upstream)
    run(repository, "checkout", "release/next")
    run(repository, "merge", "--no-ff", "upstream/simulation", "-m", "Synchronize release source")
    plan = plan_release(repository, target="refs/remotes/upstream/main")
    assert plan["integration_ref"] == "refs/remotes/upstream/main"
    assert plan["integration_target"] == upstream
    prepare_release(repository, plan, date="2026-10-13")
    save(repository, "Prepare against explicit upstream")
    assert check_release(repository).ok
    assert commit(repository, "main") == local_primary


def test_detached_candidate_keeps_explicit_target_checks_and_honest_identity(repository):
    candidate(repository)
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "release/next", "-m", "Finalize baseline")
    merged = commit(repository)
    run(repository, "update-ref", "refs/remotes/origin/main", merged)
    run(repository, "checkout", "--detach", "main")
    run(repository, "branch", "-D", "main")
    assert not check_release(repository).ok  # Stored local ref is unavailable.
    assert check_release(repository, target="origin/main").ok
    assert (
        identity(repository)["state"] == "finalized"
    )  # Cached remote snapshot proves integration.
    run(repository, "tag", "-a", "imp-0.3.2", "-m", "Finalized implementation")
    assert check_release(repository, target="origin/main", publication=True).ok


def test_exact_commit_target_is_bound_and_can_be_overridden_after_integration(repository):
    integrated_change(repository)
    target = commit(repository, "main")
    plan = plan_release(repository, target=target)
    assert plan["integration_ref"] == target
    prepare_release(repository, plan, date="2026-10-13")
    save(repository, "Prepare against exact reviewed commit")
    assert check_release(repository).ok
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "release/next", "-m", "Finalize candidate")
    assert check_release(repository, target="main").ok


def test_remote_only_primary_can_capture_starting_work(repository):
    source = commit(repository)
    run(repository, "update-ref", "refs/remotes/origin/main", source)
    run(repository, "branch", "-D", "main")
    path = start_work(repository, "remote-start")
    assert read_yaml(path)["origin"]["commit"] == source


def test_editorial_spec_release_preserves_exact_old_implementation_declaration(repository):
    original = (repository / ".macrostates/implementation/release.yaml").read_bytes()
    candidate(repository, spec="patch", imp="none")
    assert (repository / ".macrostates/implementation/release.yaml").read_bytes() == original
    plan = read_yaml(repository / ".macrostates/implementation/release-plan.yaml")
    assert plan["candidate"]["implementation_specification"] == "specs-0.3.0"
    assert check_release(repository).ok


def test_candidate_check_does_not_require_new_tags_but_publication_does(repository):
    candidate(repository)
    assert check_release(repository).ok
    report = check_release(repository, publication=True)
    assert {item.code for item in report.diagnostics} == {
        "release.integration",
        "release.tag_missing",
    }
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "release/next", "-m", "Finalize release")
    run(repository, "tag", "-a", "imp-0.3.2", "-m", "Finalized implementation")
    assert check_release(repository, publication=True).ok
    assert identity(repository)["state"] == "finalized"


def test_tag_collision_or_missing_unchanged_specification_is_rejected(repository):
    candidate(repository)
    run(repository, "tag", "-a", "imp-0.3.2", "main", "-m", "Conflicting identity")
    assert "release.collision" in {item.code for item in check_release(repository).diagnostics}
    run(repository, "tag", "-d", "imp-0.3.2", "specs-0.3.0")
    assert "release.baseline_tag" in {item.code for item in check_release(repository).diagnostics}


def test_directory_scoped_specification_changes_cannot_reuse_unchanged_baseline(repository):
    scope = repository / "component/.macrostates/specs"
    scope.mkdir(parents=True)
    (scope / "main.md").write_text("# Additional component requirements\n")
    candidate(repository)
    assert "release.specification_snapshot" in {
        item.code for item in check_release(repository).diagnostics
    }


def test_independent_subproject_specifications_are_not_owned_by_parent_baseline(repository):
    scope = repository / "component/.macrostates/specs"
    scope.mkdir(parents=True)
    (scope / "main.md").write_text("# Independent requirements\n")
    (scope / "composition.yaml").write_text("schema_version: 1\nproject:\n  name: independent\n")
    candidate(repository)
    assert check_release(repository).ok


def test_open_workflow_cannot_hide_in_history(repository):
    candidate(repository)
    workflow = repository / ".macrostates/implementation/workflows/history/open.md"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("# Unfinished\n\n- Status: in_progress\n")
    save(repository, "Unfinished workflow moved into history")
    assert "workflow.open" in {item.code for item in check_release(repository).diagnostics}


def test_source_edit_after_preparation_invalidates_candidate(repository):
    candidate(repository)
    (repository / "app.py").write_text("print('unreviewed behavior')\n")
    save(repository, "Unclassified behavior after planning")
    report = check_release(repository)
    assert not report.ok
    assert any("Source changed" in item.message for item in report.diagnostics)


def test_archived_record_bytes_remain_bound_after_preparation(repository):
    candidate(repository)
    path = repository / ".macrostates/implementation/changes/history/fix.yaml"
    path.write_text(path.read_text() + "extension: tampered\n")
    save(repository, "Change archived evidence")
    assert "release.records" in {item.code for item in check_release(repository).diagnostics}


def test_preparation_rolls_back_ordinary_write_failure(repository, monkeypatch):
    integrated_change(repository)
    plan = plan_release(repository)
    before = {
        path.relative_to(repository).as_posix(): path.read_bytes()
        for path in (repository / ".macrostates").rglob("*")
        if path.is_file()
    }
    original = Path.rename
    failed = False

    def failing_rename(path, destination):
        nonlocal failed
        if (
            not failed
            and path.name == "release.yaml"
            and str(destination).endswith("implementation/release.yaml")
        ):
            failed = True
            raise OSError("Synthetic write failure")
        return original(path, destination)

    monkeypatch.setattr(Path, "rename", failing_rename)
    with pytest.raises(OSError, match="Synthetic"):
        prepare_release(repository, plan, date="2026-10-13")
    after = {
        path.relative_to(repository).as_posix(): path.read_bytes()
        for path in (repository / ".macrostates").rglob("*")
        if path.is_file()
    }
    assert after == before
    assert not list(repository.glob(".macrostates-release-*"))


def test_old_candidate_record_does_not_block_the_next_release(repository):
    candidate(repository)
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "release/next", "-m", "Finalize baseline")
    run(repository, "checkout", "-b", "feature/next")
    record(repository, "next")
    save(repository, "Next accepted fix")
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "feature/next", "-m", "Integrate next work")
    assert plan_release(repository)["candidate"]["implementation"] == "imp-0.3.3"


def test_unrecorded_runtime_commit_on_primary_does_not_claim_finalized_identity(repository):
    candidate(repository)
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "release/next", "-m", "Finalize baseline")
    assert identity(repository)["state"] == "finalized"
    (repository / "app.py").write_text("print('unrecorded behavior')\n")
    save(repository, "Unrecorded runtime modification")
    assert identity(repository)["state"] != "finalized"
    assert identity(repository)["implementation"].startswith("imp-0.3.2-")


def test_legacy_tag_alias_proves_same_snapshot_and_rejects_movement(repository):
    from macrostates._migration import migrate_versioning

    run(repository, "checkout", "main")
    manifest = repository / ".macrostates/specs/composition.yaml"
    previous = read_yaml(manifest)
    previous["project"]["version"] = "spec-0.3.0"
    manifest.write_text(dump_yaml(previous))
    declaration = repository / ".macrostates/implementation/release.yaml"
    declaration.write_text(
        'version: "0.3.1"\nspecification: "spec-0.3.0"\nrelease_date: "2026-10-01"\n'
    )
    original = save(repository, "Legacy canonical baseline")
    run(repository, "tag", "-d", "specs-0.3.0", "imp-0.3.1")
    run(repository, "tag", "-a", "spec-0.3.0", "-m", "Legacy specification")
    run(repository, "tag", "-a", "v0.3.1", "-m", "Legacy implementation")
    run(repository, "checkout", "-b", "feature/migrate")
    assert migrate_versioning(repository)["changed"]
    create_change(
        repository,
        "fix",
        "Implementation correction",
        "none",
        "patch",
        origin_commit=original,
        evidence=["Regression test passes"],
    )
    save(repository, "Migrate declarations and record a correction")
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "feature/migrate", "-m", "Integrate migration")
    run(repository, "checkout", "-b", "release/migrated")
    prepare_release(repository, plan_release(repository), date="2026-10-13")
    save(repository, "Prepare implementation release reusing legacy specs")
    assert check_release(repository).ok
    run(repository, "tag", "-f", "-a", "spec-0.3.0", "-m", "Moved identity")
    assert any("moved" in item.message for item in check_release(repository).diagnostics)


def test_specification_only_project_does_not_invent_implementation(repository):
    run(repository, "rm", ".macrostates/implementation/release.yaml")
    save(repository, "Specification-only state")
    create_change(
        repository,
        "fix",
        "Editorial specification change",
        "patch",
        "none",
        evidence=["Specification reviewed"],
        origin_commit=commit(repository),
    )
    save(repository, "Specification editorial change")
    plan = plan_release(repository)
    assert plan["candidate"]["implementation"] is None
    prepare_release(repository, plan, date="2026-10-13")
    assert not (repository / ".macrostates/implementation/release.yaml").exists()


def finalize_tagged_baseline(root):
    candidate(root)
    run(root, "checkout", "main")
    run(root, "merge", "--no-ff", "release/next", "-m", "Finalize baseline")
    run(root, "tag", "-a", "imp-0.3.2", "-m", "Finalized implementation")
    frozen = commit(root)
    run(root, "checkout", "-b", "application/metadata")
    return frozen


def test_independent_app_release_uses_immutable_baseline_with_complete_workflow(tmp_path):
    from .test_integration_sync import commit_all, git, make_project, workflow

    project = make_project(tmp_path)
    for name in ("specs-0.3.0", "imp-0.3.1"):
        git(tmp_path, "tag", "-a", name, "main", "-m", "Original baseline")
    project.create_change(
        "first",
        "Restore required behavior",
        specification="none",
        implementation="patch",
        evidence=["Behavior verified"],
    )
    commit_all(tmp_path, "Completed implementation work")
    git(tmp_path, "checkout", "main")
    git(tmp_path, "merge", "--no-ff", "feature/work", "-m", "Integrate feature")
    git(tmp_path, "checkout", "-b", "release/baseline")
    project.prepare_release(project.plan_release(), date="2026-10-13")
    commit_all(tmp_path, "Prepare baseline")
    git(tmp_path, "checkout", "main")
    git(tmp_path, "merge", "--no-ff", "release/baseline", "-m", "Finalize baseline")
    git(tmp_path, "tag", "-a", "imp-0.3.2", "-m", "Frozen implementation")
    frozen_tag = git(tmp_path, "rev-parse", "refs/tags/imp-0.3.2")
    frozen_plan = (project.implementation / "release-plan.yaml").read_bytes()
    frozen_declaration = (project.implementation / "release.yaml").read_bytes()
    git(tmp_path, "checkout", "-b", "application/mobile")
    project.start_work("mobile-release")
    (project.implementation / "deliverables.yaml").write_text(
        dump_yaml(
            {
                "schema_version": 1,
                "deliverables": {
                    "mobile": {
                        "strategy": "independent",
                        "version": "7.3.25",
                        "version_scheme": "semver",
                        "specification": "specs-0.3.0",
                        "implementation": "imp-0.3.2",
                        "release_date": "2026-10-13",
                        "android": {"version_code": 84},
                        "source": {"tag": "mobile-7.3.25"},
                    }
                },
            }
        )
    )
    change = project.create_change(
        "mobile-metadata",
        "Assign independent mobile release metadata",
        specification="none",
        implementation="none",
        work="mobile-release",
        deliverables=["mobile"],
        evidence=["Application release policy, metadata and unchanged behavior reviewed"],
    )
    workflow(project, history=True)
    commit_all(tmp_path, "Completed independent application preparation")
    assert project.check_integration().ok
    assert project.check_release().ok  # Baseline is finalized; app proposal is not yet integrated.
    assert not project.check_release(publication=True).ok
    git(tmp_path, "checkout", "main")
    git(
        tmp_path,
        "merge",
        "--no-ff",
        "application/mobile",
        "-m",
        "Integrate independent app metadata",
    )
    git(tmp_path, "tag", "-a", "mobile-7.3.25", "-m", "Independent application release")
    assert project.check_release(publication=True).ok
    assert change.exists()  # None records remain pending for a future real baseline release.
    assert git(tmp_path, "rev-parse", "refs/tags/imp-0.3.2") == frozen_tag
    assert (project.implementation / "release-plan.yaml").read_bytes() == frozen_plan
    assert (project.implementation / "release.yaml").read_bytes() == frozen_declaration
    with pytest.raises(MacrostatesError, match="Tracking-only"):
        project.plan_release()


@pytest.mark.parametrize("problem", ["evidence", "gap", "impact"])
def test_app_only_continuation_requires_none_scope_evidence_and_no_gaps(repository, problem):
    original = finalize_tagged_baseline(repository)
    metadata = repository / ".macrostates/implementation/release-notes.md"
    metadata.write_text("Independent application metadata preparation\n")
    create_change(
        repository,
        "metadata",
        "Reviewed metadata",
        "none",
        "patch" if problem == "impact" else "none",
        origin_commit=original,
        evidence=[] if problem == "evidence" else ["Metadata reviewed"],
        gaps=["Unverified application requirement"] if problem == "gap" else [],
    )
    save(repository, "Application preparation with missing readiness")
    report = check_release(repository)
    assert not report.ok
    expected = {
        "evidence": "release.metadata_evidence",
        "gap": "change.gaps",
        "impact": "release.pending",
    }[problem]
    assert expected in {item.code for item in report.diagnostics}


def test_app_metadata_cannot_hide_changed_behavior_in_the_tagged_baseline(repository):
    candidate(repository)
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "release/next", "-m", "Integrate baseline")
    (repository / "app.py").write_text("print('unreviewed behavior')\n")
    save(repository, "Unreviewed behavior before tagging")
    run(repository, "tag", "-a", "imp-0.3.2", "-m", "Incorrect baseline snapshot")
    (repository / "app.py").write_text("print('original')\n")
    (repository / ".macrostates/implementation/release-notes.md").write_text("Later metadata\n")
    save(repository, "Restore planned behavior and add metadata")
    assert "release.collision" in {
        item.code for item in check_release(repository, publication=True).diagnostics
    }


def test_app_only_records_are_consumed_only_with_a_future_real_baseline_bump(repository):
    original = finalize_tagged_baseline(repository)
    create_change(
        repository,
        "metadata",
        "Independent metadata",
        "none",
        "none",
        origin_commit=original,
        evidence=["Metadata reviewed"],
    )
    (repository / ".macrostates/implementation/release-notes.md").write_text("Reviewed metadata\n")
    save(repository, "Metadata-only application scope")
    run(repository, "checkout", "main")
    run(repository, "merge", "--no-ff", "application/metadata", "-m", "Integrate app metadata")
    assert check_release(repository, publication=True).ok
    run(repository, "checkout", "-b", "feature/next-fix")
    record(repository, "next-fix")
    save(repository, "Real implementation revision")
    run(repository, "checkout", "main")
    run(
        repository,
        "merge",
        "--no-ff",
        "feature/next-fix",
        "-m",
        "Integrate implementation revision",
    )
    run(repository, "checkout", "-b", "release/next-revision")
    plan = plan_release(repository)
    assert {item["id"] for item in plan["records"]} == {"metadata", "next-fix"}
    assert plan["candidate"]["implementation"] == "imp-0.3.3"
    prepare_release(repository, plan, date="2026-10-13")
    assert not load_changes(repository)
