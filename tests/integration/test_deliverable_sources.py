"""Release provenance resolves real annotated Git snapshots without network."""

import copy

import pytest
import yaml

from macrostates._deliverables import check_deliverable_changes, check_deliverable_publication

from .test_deliverables import write_deliverables
from .test_integration_sync import codes, commit_all, git, make_project


def application_entry():
    return {
        "strategy": "independent",
        "version": "7.3.25",
        "version_scheme": "project-defined",
        "implementation": "imp-0.3.1",
        "specification": "specs-0.3.0",
        "release_date": "2026-10-13",
        "android": {"version_code": 84},
        "source": {"tag": "android/v7.3.25-84"},
    }


def published_application(tmp_path):
    project = make_project(tmp_path)
    entry = application_entry()
    write_deliverables(project, {"android-app": entry})
    source = commit_all(tmp_path, "Reviewed application snapshot")
    git(tmp_path, "tag", "-a", entry["source"]["tag"], "-m", "Application release")
    return project, entry, source


@pytest.mark.parametrize("reference", ["tag", "commit", "both"])
def test_application_source_references_resolve_to_matching_snapshot(tmp_path, reference):
    project, entry, source = published_application(tmp_path)
    entry["source"] = (
        {"tag": entry["source"]["tag"]}
        if reference == "tag"
        else {"commit": source}
        if reference == "commit"
        else {"tag": entry["source"]["tag"], "commit": source}
    )
    write_deliverables(project, {"android-app": entry})
    report = check_deliverable_publication(tmp_path)
    assert report.ok, report.diagnostics
    assert "deliverable.artifact_review" not in codes(report)


def test_application_tag_and_receipt_commit_must_agree(tmp_path):
    project, entry, _ = published_application(tmp_path)
    (tmp_path / "next.txt").write_text("A later source snapshot\n")
    later = commit_all(tmp_path, "Subsequent work")
    entry["source"]["commit"] = later
    write_deliverables(project, {"android-app": entry})
    report = check_deliverable_publication(tmp_path)
    assert "deliverable.source_invalid" in codes(report)
    assert not report.ok


@pytest.mark.parametrize("source", [None, {"tag": "android/missing"}])
def test_release_does_not_claim_missing_source_identity(tmp_path, source):
    project = make_project(tmp_path)
    entry = application_entry()
    if source is None:
        del entry["source"]
    else:
        entry["source"] = source
    write_deliverables(project, {"android-app": entry})
    report = check_deliverable_publication(tmp_path)
    assert not report.ok
    assert codes(report) & {"deliverable.source_missing", "deliverable.source_invalid"}


@pytest.mark.parametrize(
    "field,value",
    [
        ("version", "7.3.26"),
        ("implementation", "imp-0.3.2"),
        ("specification", "specs-0.3.1"),
        ("android", {"version_code": 85}),
    ],
)
def test_release_provenance_must_match_referenced_application_snapshot(tmp_path, field, value):
    project, entry, _ = published_application(tmp_path)
    entry[field] = value
    write_deliverables(project, {"android-app": entry})
    report = check_deliverable_publication(tmp_path)
    assert "deliverable.source_invalid" in codes(report)
    assert not report.ok


def test_source_snapshot_must_contain_the_named_deliverable(tmp_path):
    project, entry, _ = published_application(tmp_path)
    write_deliverables(project, {"different-app": entry})
    report = check_deliverable_publication(tmp_path)
    assert "deliverable.source_invalid" in codes(report)


def test_default_version_policy_cannot_relabel_an_independent_release_snapshot(tmp_path):
    project, entry, _ = published_application(tmp_path)
    entry["strategy"] = "implementation"
    del entry["version"]
    write_deliverables(project, {"android-app": entry})
    assert project.deliverables()["android-app"]["version"] == "0.3.1"
    report = check_deliverable_publication(tmp_path)
    assert "deliverable.source_invalid" in codes(report)
    assert not report.ok


def test_default_derived_application_snapshot_needs_no_competing_explicit_version(tmp_path):
    project = make_project(tmp_path)
    entry = application_entry()
    del entry["strategy"]
    del entry["version"]
    entry["source"]["tag"] = "android/v0.3.1-84"
    write_deliverables(project, {"android-app": entry})
    commit_all(tmp_path, "Implementation-derived application release")
    git(tmp_path, "tag", "-a", entry["source"]["tag"], "-m", "Application release")
    assert project.deliverables()["android-app"]["version"] == "0.3.1"
    report = check_deliverable_publication(tmp_path)
    assert report.ok, report.diagnostics


def test_custom_application_metadata_requires_explicit_artifact_review(tmp_path):
    project = make_project(tmp_path)
    (tmp_path / "native-app.json").write_text('{"release": "7.3.25"}\n')
    source = commit_all(tmp_path, "Native application metadata with custom tooling")
    entry = application_entry()
    entry["source"] = {"commit": source}
    write_deliverables(project, {"android-app": entry})
    report = check_deliverable_publication(tmp_path)
    assert report.ok
    assert "deliverable.artifact_review" in codes(report)
    assert any(item.severity == "warning" for item in report.diagnostics)


@pytest.mark.parametrize(
    "change",
    [{"implementation": "imp-0.3.2"}, {"source": {"tag": "android/new-source"}}],
)
def test_android_same_display_version_requires_higher_counter_for_new_source(tmp_path, change):
    project = make_project(tmp_path)
    original = application_entry()
    write_deliverables(project, {"android-app": original})
    target = commit_all(tmp_path, "Previous Android release")
    proposed = copy.deepcopy(original)
    proposed.update(change)
    write_deliverables(project, {"android-app": proposed})
    report = check_deliverable_changes(tmp_path, target)
    assert "deliverable.android_order" in codes(report)
    proposed["android"]["version_code"] = 85
    write_deliverables(project, {"android-app": proposed})
    assert check_deliverable_changes(tmp_path, target).ok


def test_unchanged_published_application_remains_valid_after_repository_contract_advances(tmp_path):
    project, entry, _ = published_application(tmp_path)
    manifest = yaml.safe_load(project.manifest.read_text())
    manifest["project"]["version"] = "specs-0.4.0"
    project.manifest.write_text(yaml.safe_dump(manifest))
    release = yaml.safe_load((project.implementation / "release.yaml").read_text())
    release.update(version="imp-0.4.0", specification="specs-0.4.0")
    (project.implementation / "release.yaml").write_text(yaml.safe_dump(release))
    current = project.deliverables()["android-app"]
    assert current["version"] == entry["version"]
    assert current["implementation"] == "imp-0.3.1"
    assert current["android"]["version_code"] == 84
    report = check_deliverable_publication(tmp_path)
    assert report.ok, report.diagnostics
