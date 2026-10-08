import pytest
import yaml

from macrostates import MacrostatesError, Project

from ..conftest import FakeSource, composition


def modern_project(tmp_path):
    source = FakeSource()
    source.add("meta", "2.0.0")
    source.add(
        "process",
        "3.0.0",
        dependencies=[{"name": "meta", "version": "2.0.0", "constraint": "compatible"}],
    )
    data = composition(("meta", "process"), versions={"meta": "2.0.0", "process": "3.0.0"})
    data["project"]["version"] = "spec-0.2.1"
    project = Project.initialize(tmp_path, manifest=data, source=source)
    assert project.install().ok
    (project.implementation / "release.yaml").write_text(
        yaml.safe_dump(
            {"version": "0.2.3", "specification": "spec-0.2.0", "release_date": "2026-10-08"}
        )
    )
    return project


def test_latest_meta_process_work_together(tmp_path):
    project = modern_project(tmp_path)
    assert project.specs == tmp_path / ".macrostates/specs"
    assert project.implementation == tmp_path / ".macrostates/implementation"
    assert project.check().ok
    assert "take precedence" not in (project.specs / "main.md").read_text()
    (project.implementation / "release.yaml").write_text(
        'version: "0.3.0"\nspecification: "spec-0.3.0"\nrelease_date: "2026-10-08"\n'
    )
    assert "process.version_alignment" in {item.code for item in project.lint().diagnostics}


@pytest.mark.parametrize("name,selected", [("meta", "2.0.0"), ("process", "3.0.0")])
def test_latest_policies_refuse_legacy_initialization_without_writes(tmp_path, name, selected):
    data = composition((name,), versions={name: selected})
    with pytest.raises(MacrostatesError, match="requires"):
        Project.initialize(tmp_path, manifest=data, layout="legacy")
    assert not list(tmp_path.iterdir())


def test_meta2_requires_explicit_composition_format(tmp_path):
    data = composition(versions={"meta": "2.0.0"}, schema=None)
    with pytest.raises(MacrostatesError, match="schema_version"):
        Project.initialize(tmp_path, manifest=data)
    assert not list(tmp_path.iterdir())


def test_future_meta_policy_is_not_assumed(tmp_path):
    with pytest.raises(MacrostatesError, match="adapter"):
        Project.initialize(tmp_path, manifest=composition(versions={"meta": "2.1.0"}))
    assert not list(tmp_path.iterdir())


def test_explicitly_moved_modern_project_is_diagnosed(tmp_path):
    project = modern_project(tmp_path)
    project.specs.rename(tmp_path / "specs")
    project.implementation.rename(tmp_path / "implementation")
    loaded = Project.open(tmp_path)
    assert {"meta.layout", "process.layout"} <= {item.code for item in loaded.lint().diagnostics}


def test_directory_scope_is_component_and_checks_links(tmp_path):
    project = modern_project(tmp_path)
    scoped = tmp_path / "apps/reporting/.macrostates/specs"
    scoped.mkdir(parents=True)
    (scoped / "main.md").write_text("# Reporting\n\n[Interfaces](interfaces.md)\n")
    (scoped / "interfaces.md").write_text("# Component interfaces\n")
    assert Project.open(tmp_path / "apps/reporting").root == tmp_path
    assert project.info()["directory_specifications"] == [
        {"scope": "apps/reporting", "entrypoint": "apps/reporting/.macrostates/specs/main.md"}
    ]
    assert project.check().ok
    (scoped / "interfaces.md").unlink()
    assert "link.missing" in {item.code for item in project.lint().diagnostics}


@pytest.mark.parametrize("layout", ["modern", "legacy"])
def test_separate_composition_is_not_a_parent_directory_scope(tmp_path, layout):
    project = modern_project(tmp_path)
    child_root = tmp_path / "vendor/example-library"
    child_root.mkdir(parents=True)
    child = Project.initialize(child_root, manifest=composition(), layout=layout)
    (child.specs / "main.md").write_text("[Broken child link](absent.md)\n")
    nested = child_root / "src/component/.macrostates/specs"
    nested.mkdir(parents=True)
    (nested / "main.md").write_text("[Broken internal link](absent.md)\n")
    assert project.info()["directory_specifications"] == []
    assert project.check().ok


@pytest.mark.parametrize("selected", ["2.3.1", "2.4.0", "3.0.0"])
def test_known_process_shorthand_declares_contract(tmp_path, selected):
    project = Project.initialize(tmp_path, name="example", packages=[("process", selected)])
    assert yaml.safe_load(project.manifest.read_text())["project"]["version"] == "spec-0.1.0"


def test_process24_retains_declaration_checks(tmp_path):
    from .test_process_policies import prepare

    project = prepare(tmp_path, "2.4.0", spec=None)
    assert "process.spec_version" in {item.code for item in project.lint().diagnostics}


def test_current_official_dependency_chain_installs_together(tmp_path):
    from pathlib import Path

    records = yaml.safe_load(
        (Path(__file__).parents[1] / "fixtures/current-metadata.yaml").read_text()
    )
    source = FakeSource()
    versions = {item["name"]: item["version"] for item in records}
    for item in records:
        source.add(
            item["name"],
            item["version"],
            extra={"package.yaml": yaml.safe_dump(item["metadata"])},
        )
        for dependency in item["metadata"].get("dependencies", []) + item["metadata"].get(
            "optional_dependencies", []
        ):
            assert dependency["version"] == versions[dependency["name"]]
    data = composition(tuple(versions), versions=versions)
    data["project"]["version"] = "spec-0.1.0"
    project = Project.initialize(tmp_path, manifest=data, source=source)
    assert project.install().ok
    assert project.check().ok
