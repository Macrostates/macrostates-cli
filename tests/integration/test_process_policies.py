import pytest
import yaml

from macrostates import Project

from ..conftest import FakeSource, composition


def prepare(tmp_path, selected, *, spec="spec-1.2.3", release=None):
    source = FakeSource()
    source.add("process", selected)
    data = composition(("process",), versions={"process": selected})
    if spec is not None:
        data["project"]["version"] = spec
    project = Project.initialize(tmp_path, manifest=data, source=source)
    assert project.install().ok
    if release is not None:
        (project.implementation / "release.yaml").write_text(yaml.safe_dump(release))
    return project


@pytest.mark.parametrize("selected", ["1.7.0", "1.8.0", "2.0.0", "2.1.0", "2.2.0"])
def test_older_process_does_not_inherit_new_declarations(tmp_path, selected):
    project = prepare(tmp_path, selected, spec=None)
    assert project.lint().ok


def test_process_23_accepts_independent_revision_counters(tmp_path):
    project = prepare(
        tmp_path,
        "2.3.0",
        release={"version": "1.2.8", "specification": "spec-1.2.1", "release_date": "2026-01-01"},
    )
    assert project.lint().ok


@pytest.mark.parametrize(
    "release,code",
    [
        (
            {"version": "1.3.0", "specification": "spec-1.3.0", "release_date": "2026-01-01"},
            "process.version_alignment",
        ),
        (
            {"version": "1.2.0", "specification": "spec-1.2.4", "release_date": "2026-01-01"},
            "process.future_baseline",
        ),
        (
            {"version": "1.2.0", "specification": "spec-1.2.1", "release_date": "2026-02-30"},
            "process.release_invalid",
        ),
        (
            {"version": "1.2.0", "specification": "1.2.1", "release_date": "2026-01-01"},
            "process.release_invalid",
        ),
    ],
)
def test_process_23_invalid_release_declarations(tmp_path, release, code):
    project = prepare(tmp_path, "2.3.0", release=release)
    assert code in {item.code for item in project.lint().diagnostics}


def test_process_23_active_requires_release(tmp_path):
    project = prepare(tmp_path, "2.3.0")
    (project.implementation / "main.md").write_text("Project phase: active\n")
    assert "process.release_missing" in {item.code for item in project.lint().diagnostics}


def test_process_23_requires_composition_version(tmp_path):
    project = prepare(tmp_path, "2.3.0", spec=None)
    assert "process.spec_version" in {item.code for item in project.lint().diagnostics}


@pytest.mark.parametrize("selected", ["2.5.0", "3.1.0", "4.0.0"])
def test_future_process_policy_is_not_guessed(tmp_path, selected):
    project = prepare(tmp_path, selected)
    assert "process.unsupported_policy" in {item.code for item in project.lint().diagnostics}
