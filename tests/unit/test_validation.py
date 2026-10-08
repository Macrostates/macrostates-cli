import pytest

from macrostates import Project

from ..conftest import FakeSource, composition


def dependency(name, version="1.0.0", constraint="compatible"):
    return {"name": name, "version": version, "constraint": constraint}


@pytest.mark.parametrize(
    "constraint,selected,expected",
    [
        ("compatible", "1.2.0", True),
        ("compatible", "2.0.0", False),
        ("exact", "1.0.1", False),
        ("at_least", "2.0.0", True),
        ("at_least", "0.9.0", False),
    ],
)
def test_dependency_constraints(tmp_path, constraint, selected, expected):
    source = FakeSource()
    source.add("meta", selected)
    source.add("process", dependencies=[dependency("meta", constraint=constraint)])
    project = Project.initialize(
        tmp_path,
        manifest=composition(("meta", "process"), versions={"meta": selected}),
        source=source,
    )
    assert project.install().ok == expected
    if not expected:
        assert not (project.specs / "000_meta").exists()
        assert not (project.specs / "composition.lock.yaml").exists()


def test_absent_optional_dependency_does_not_select_it(tmp_path):
    source = FakeSource()
    source.add(optional=[dependency("docker")])
    project = Project.initialize(tmp_path, manifest=composition(), source=source)
    assert project.install().ok


def test_cycles_fail_before_install(tmp_path):
    source = FakeSource()
    source.add(dependencies=[dependency("process")])
    source.add("process", dependencies=[dependency("meta")])
    project = Project.initialize(tmp_path, manifest=composition(("meta", "process")), source=source)
    report = project.install()
    assert any(item.code == "dependency.cycle" for item in report.diagnostics)
    assert not (project.specs / "000_meta").exists()


def test_missing_dependency_reported(tmp_path):
    source = FakeSource()
    source.add(dependencies=[dependency("missing")])
    project = Project.initialize(tmp_path, manifest=composition(), source=source)
    assert not project.install().ok
