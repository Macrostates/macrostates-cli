import copy

import pytest
import yaml

from macrostates import MacrostatesError

from .test_integration_sync import codes, commit_all, git, make_project


def write_deliverables(project, entries, *, schema=1):
    path = project.implementation / "deliverables.yaml"
    path.write_text(yaml.safe_dump({"schema_version": schema, "deliverables": entries}))
    return path


def test_absent_application_policy_document_is_optional(tmp_path):
    project = make_project(tmp_path)
    assert project.deliverables() == {}
    assert not (project.implementation / "deliverables.yaml").exists()


def test_monorepo_application_versions_and_android_counter_are_independent(tmp_path):
    project = make_project(tmp_path)
    path = write_deliverables(
        project,
        {
            "python-library": {
                "strategy": "independent",
                "version": "4.12.3",
                "version_scheme": "semver",
            },
            "android-app": {"android": {"version_code": 84}},
        },
    )
    before = path.read_bytes()
    result = project.deliverables()
    assert result["python-library"]["version"] == "4.12.3"
    assert result["android-app"]["strategy"] == "implementation"
    assert result["android-app"]["version"] == "0.3.1"
    assert result["android-app"]["android"]["version_code"] == 84
    assert path.read_bytes() == before


def test_unchanged_application_preserves_its_historical_baseline_provenance(tmp_path):
    project = make_project(tmp_path)
    write_deliverables(
        project,
        {
            "android-app": {
                "strategy": "implementation",
                "specification": "specs-0.2.0",
                "implementation": "imp-0.2.3",
                "release_date": "2026-10-09",
                "android": {"version_code": 84},
                "source": {"tag": "android-app/v0.2.3"},
            }
        },
    )
    result = project.deliverables()["android-app"]
    assert result["version"] == "0.2.3"
    assert result["specification"] == "specs-0.2.0"
    assert result["implementation"] == "imp-0.2.3"
    assert result["android"]["version_code"] == 84
    assert result["source"]["tag"] == "android-app/v0.2.3"


@pytest.mark.parametrize(
    "version,code,valid",
    [("7.3.25", 84, False), ("7.3.25", 85, True), ("7.3.24", 83, False), ("7.3.24", 84, True)],
)
def test_android_release_order_is_checked_against_integration_target(
    tmp_path, version, code, valid
):
    project = make_project(tmp_path)
    git(tmp_path, "switch", "--quiet", "main")
    write_deliverables(
        project,
        {
            "android-app": {
                "strategy": "independent",
                "version": "7.3.24",
                "android": {"version_code": 84},
            }
        },
    )
    commit_all(tmp_path, "Existing Android application release")
    git(tmp_path, "switch", "--quiet", "feature/work")
    project.sync_branch(target="main", strategy="merge")
    project.create_change(
        "application-metadata",
        "Prepare independent application metadata",
        specification="none",
        implementation="none",
        origin_commit=git(tmp_path, "rev-parse", "main"),
    )
    write_deliverables(
        project,
        {
            "android-app": {
                "strategy": "independent",
                "version": version,
                "android": {"version_code": code},
            }
        },
    )
    commit_all(tmp_path, "Application candidate")
    report = project.check_integration()
    assert ("deliverable.android_order" not in codes(report)) == valid
    assert report.ok == valid, report.diagnostics


@pytest.mark.parametrize(
    "entry",
    [
        {"strategy": "unknown"},
        {"strategy": "independent"},
        {"version": "4.12.3"},
        {"implementation": "0.3.1"},
        {"specification": "specs-0.4.0", "implementation": "imp-0.3.1"},
        {"android": {"version_code": True}},
        {"android": {"version_code": 0}},
        {"android": {"version_code": 2_100_000_001}},
        {"android": {"version_code": "84"}},
        {"release_date": "2026-02-30"},
        {"release_date": "20261013"},
        {"release_date": "2026-10-13"},
        {"source": {"commit": "abcd"}},
        {"source": {"tag": "--help"}},
        {"source": {}},
    ],
)
def test_invalid_deliverable_metadata_is_not_silently_normalized(tmp_path, entry):
    project = make_project(tmp_path)
    path = write_deliverables(project, {"android-app": copy.deepcopy(entry)})
    before = path.read_bytes()
    with pytest.raises(MacrostatesError):
        project.deliverables()
    assert path.read_bytes() == before


@pytest.mark.parametrize("schema", [True, 2, "1"])
def test_deliverable_schema_is_explicit(tmp_path, schema):
    project = make_project(tmp_path)
    write_deliverables(project, {}, schema=schema)
    with pytest.raises(MacrostatesError):
        project.deliverables()
