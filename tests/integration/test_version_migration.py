from pathlib import Path

import pytest
import yaml

from macrostates import MacrostatesError, Project

from .test_integration_sync import commit_all, git, make_project


def legacy_project(tmp_path: Path, *, primary="main", implementation=True):
    project = make_project(tmp_path, primary=primary)
    manifest = yaml.safe_load(project.manifest.read_text())
    manifest["project"]["version"] = "spec-0.3.0"
    manifest["project"]["custom_note"] = "Keep application policy independent"
    project.manifest.write_text(yaml.safe_dump(manifest))
    release = project.implementation / "release.yaml"
    if implementation:
        release.write_text(
            yaml.safe_dump(
                {
                    "version": "0.3.1",
                    "specification": "spec-0.3.0",
                    "release_date": "2026-10-09",
                    "extension": {"preserved": True},
                }
            )
        )
    else:
        release.unlink()
    selected = commit_all(tmp_path, "Legacy declaration baseline")
    git(tmp_path, "tag", "--annotate", "spec-0.3.0", "-m", "Published specification")
    if implementation:
        git(tmp_path, "tag", "--annotate", "v0.3.1", "-m", "Published implementation")
    return project, selected


def snapshot(project):
    return {
        path.relative_to(project.root).as_posix(): path.read_bytes()
        for path in project.root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(project.root).parts
    }


def test_open_info_and_check_do_not_implicitly_migrate(tmp_path):
    project, _ = legacy_project(tmp_path)
    before = snapshot(project)
    opened = Project.open(tmp_path)
    assert opened.info()["packages"][0]["version"] == "5.0.0"
    report = opened.check()
    assert "process.release_invalid" in {item.code for item in report.diagnostics}
    assert snapshot(project) == before
    assert not (project.implementation / "version-migration.yaml").exists()


def test_explicit_migration_is_idempotent_and_preserves_published_refs(tmp_path):
    project, selected = legacy_project(tmp_path)
    previous_refs = git(tmp_path, "for-each-ref", "--format=%(refname) %(objectname)", "refs/tags")
    previous_history = git(tmp_path, "log", "--format=%H")
    result = project.migrate_versioning()
    assert result["changed"] is True
    assert result["specification"] == "specs-0.3.0"
    manifest = yaml.safe_load(project.manifest.read_text())
    assert manifest["project"]["version"] == "specs-0.3.0"
    assert manifest["project"]["custom_note"] == "Keep application policy independent"
    release = yaml.safe_load((project.implementation / "release.yaml").read_text())
    assert release == {
        "schema_version": 2,
        "version": "imp-0.3.1",
        "specification": "specs-0.3.0",
        "release_date": "2026-10-09",
        "extension": {"preserved": True},
    }
    provenance = yaml.safe_load((project.implementation / "version-migration.yaml").read_text())
    assert provenance["specification"] == {
        "identity": "specs-0.3.0",
        "legacy_tag": "spec-0.3.0",
        "commit": selected,
    }
    assert provenance["implementation"] == {
        "identity": "imp-0.3.1",
        "legacy_tag": "v0.3.1",
        "commit": selected,
    }
    assert git(tmp_path, "rev-parse", "HEAD") == selected
    assert git(tmp_path, "log", "--format=%H") == previous_history
    assert (
        git(tmp_path, "for-each-ref", "--format=%(refname) %(objectname)", "refs/tags")
        == previous_refs
    )
    assert project.check().ok
    after = snapshot(project)
    assert project.migrate_versioning()["changed"] is False
    assert snapshot(project) == after
    assert (
        git(tmp_path, "for-each-ref", "--format=%(refname) %(objectname)", "refs/tags")
        == previous_refs
    )


def test_specification_only_migration_does_not_invent_implementation(tmp_path):
    project, selected = legacy_project(tmp_path, implementation=False)
    assert project.migrate_versioning()["changed"] is True
    assert not (project.implementation / "release.yaml").exists()
    provenance = yaml.safe_load((project.implementation / "version-migration.yaml").read_text())
    assert "implementation" not in provenance
    assert provenance["specification"]["commit"] == selected
    assert project.migrate_versioning()["changed"] is False


@pytest.mark.parametrize("primary", ["main", "master"])
def test_migration_requires_a_development_branch(tmp_path, primary):
    project, _ = legacy_project(tmp_path, primary=primary)
    git(tmp_path, "switch", "--quiet", primary)
    before = snapshot(project)
    with pytest.raises(MacrostatesError, match="primary branch"):
        project.migrate_versioning()
    assert snapshot(project) == before


def test_older_selected_process_cannot_be_migrated_implicitly(tmp_path):
    project, _ = legacy_project(tmp_path)
    manifest = yaml.safe_load(project.manifest.read_text())
    manifest["packages"][0]["version"] = "4.1.0"
    manifest["packages"][0]["source"]["tag"] = "v4.1.0"
    project.manifest.write_text(yaml.safe_dump(manifest))
    before = snapshot(project)
    with pytest.raises(MacrostatesError, match="Process 5.0"):
        Project.open(tmp_path).migrate_versioning()
    assert snapshot(project) == before


@pytest.mark.parametrize(
    "changes",
    [
        {"version": "0.4.0"},
        {"version": "0.3.1-branch.work"},
        {"specification": "specs-0.3.0"},
        {"release_date": "2026-02-30"},
    ],
)
def test_invalid_legacy_declaration_is_preserved_for_explicit_repair(tmp_path, changes):
    project, _ = legacy_project(tmp_path)
    release_path = project.implementation / "release.yaml"
    data = yaml.safe_load(release_path.read_text())
    data.update(changes)
    release_path.write_text(yaml.safe_dump(data))
    before = snapshot(project)
    with pytest.raises(MacrostatesError):
        project.migrate_versioning()
    assert snapshot(project) == before


def test_mixed_formats_are_not_silently_repaired(tmp_path):
    project, _ = legacy_project(tmp_path)
    manifest = yaml.safe_load(project.manifest.read_text())
    manifest["project"]["version"] = "specs-0.3.0"
    project.manifest.write_text(yaml.safe_dump(manifest))
    before = snapshot(project)
    with pytest.raises(MacrostatesError, match="Mixed declaration formats"):
        project.migrate_versioning()
    assert snapshot(project) == before


def test_existing_migration_provenance_is_never_overwritten(tmp_path):
    project, _ = legacy_project(tmp_path)
    path = project.implementation / "version-migration.yaml"
    path.write_text("schema_version: 1\nnote: Preserve earlier migration evidence\n")
    before = snapshot(project)
    with pytest.raises(MacrostatesError, match="provenance must be preserved"):
        project.migrate_versioning()
    assert snapshot(project) == before
