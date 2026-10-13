import builtins
import importlib.util
import io
import tarfile
from pathlib import Path

import pytest
import yaml

import macrostates


def declaration(**changes):
    return {
        "schema_version": 1,
        "name": "macrostates-cli",
        "version": "0.4.0.dev0",
        "status": "development",
        "specification": "specs-0.5.0",
        "implementation": "imp-0.5.1",
        "release_date": "2026-10-13",
        **changes,
    }


def build_context(root, data):
    module_path = root / "src/macrostates/_build_version.py"
    module_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_bytes((Path(macrostates.__file__).parent / "_build_version.py").read_bytes())
    application = root / ".macrostates/implementation/application.yaml"
    application.parent.mkdir(parents=True, exist_ok=True)
    application.write_text(yaml.safe_dump(data))
    return module_path, application


def evaluate_module(module_path):
    specification = importlib.util.spec_from_file_location(
        "isolated_application_build", module_path
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def evaluate(module_path):
    return evaluate_module(module_path).VERSION


def candidate_context(root, *, status="candidate", version="7.3.25"):
    module_path, application = build_context(root, declaration())
    (root / "README.md").write_text("# Standalone application build\n")
    (root / "src/macrostates/runtime.py").write_text('MESSAGE = "Original behavior"\n')
    loaded = evaluate_module(module_path)
    data = declaration(version=version, status=status, source_sha256=loaded.source_digest(root))
    application.write_text(yaml.safe_dump(data))
    return module_path, application


def test_application_development_version_builds_without_git_or_installed_application(
    tmp_path, monkeypatch
):
    module_path, application = build_context(tmp_path, declaration())
    before = application.read_bytes()
    assert not (tmp_path / ".git").exists()
    assert not (application.parent / "release.yaml").exists()
    original_import = builtins.__import__

    def isolated_import(name, *args, **kwargs):
        if name == "macrostates" or name.startswith("macrostates."):
            raise AssertionError("The isolated version reader must not import the application")
        if name == "subprocess" or name.startswith("urllib."):
            raise AssertionError("Build identity must not consult Git or network services")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", isolated_import)
    assert evaluate(module_path) == "0.4.0.dev0"
    assert application.read_bytes() == before


@pytest.mark.parametrize("status", ["candidate", "finalized"])
def test_application_version_is_independent_of_repository_baseline_numbers(tmp_path, status):
    module_path, _ = candidate_context(tmp_path, status=status)
    assert evaluate(module_path) == "7.3.25"


@pytest.mark.parametrize("status", ["candidate", "finalized"])
def test_release_application_requires_verified_source_digest(tmp_path, status):
    module_path, _ = build_context(tmp_path, declaration(version="7.3.25", status=status))
    with pytest.raises(ValueError, match="source digest"):
        evaluate(module_path)


@pytest.mark.parametrize("relative", ["src/macrostates/runtime.py", "README.md"])
def test_source_change_invalidates_a_previously_prepared_application(tmp_path, relative):
    module_path, _ = candidate_context(tmp_path)
    assert evaluate(module_path) == "7.3.25"
    (tmp_path / relative).write_text("Changed shipped content\n")
    with pytest.raises(ValueError, match="source changed"):
        evaluate(module_path)


def test_application_declaration_does_not_include_its_own_hash(tmp_path):
    module_path, application = candidate_context(tmp_path)
    data = yaml.safe_load(application.read_text())
    digest = data["source_sha256"]
    data["version"] = "7.3.26"
    application.write_text(yaml.safe_dump(data))
    assert evaluate(module_path) == "7.3.26"
    assert evaluate_module(module_path).source_digest(tmp_path) == digest


def test_unshipped_workflow_changes_do_not_invalidate_application_digest(tmp_path):
    module_path, _ = candidate_context(tmp_path)
    workflow = tmp_path / ".macrostates/implementation/workflows/review.md"
    workflow.parent.mkdir()
    workflow.write_text("# Review\n\nStatus: in_progress\n")
    assert evaluate(module_path) == "7.3.25"


def test_development_source_cannot_emit_an_old_stable_version(tmp_path):
    module_path, _ = build_context(tmp_path, declaration(version="0.3.1"))
    with pytest.raises(ValueError, match="stable application release"):
        evaluate(module_path)


@pytest.mark.parametrize(
    "changes",
    [
        {"schema_version": 2},
        {"status": "unrecognized"},
        {"version": "imp-0.5.1-branch.work.gabc123"},
        {"version": "0.4.0.dev0\nother"},
        {"specification": "spec-0.5.0"},
        {"implementation": "0.5.1"},
        {"implementation": "imp-0.6.0"},
        {"release_date": "2026-02-30"},
        {"release_date": "20261013"},
    ],
)
def test_invalid_application_metadata_never_falls_back_to_old_release(tmp_path, changes):
    module_path, application = build_context(tmp_path, declaration(**changes))
    (application.parent / "release.yaml").write_text(
        'version: "0.3.1"\nspecification: "spec-0.3.0"\nrelease_date: "2026-10-09"\n'
    )
    with pytest.raises(ValueError):
        evaluate(module_path)


def test_duplicate_application_metadata_is_rejected(tmp_path):
    module_path, application = build_context(tmp_path, declaration())
    application.write_text(application.read_text() + 'version: "0.4.0.dev1"\n')
    with pytest.raises(ValueError, match="duplicate"):
        evaluate(module_path)


def test_application_declaration_symlink_is_not_followed(tmp_path):
    module_path, application = build_context(tmp_path, declaration())
    original = tmp_path / "external-application.yaml"
    application.rename(original)
    application.symlink_to(original)
    with pytest.raises(ValueError, match="symbolic link"):
        evaluate(module_path)


def test_archived_build_context_rebuilds_the_same_metadata_without_git(tmp_path):
    source = tmp_path / "source"
    module_path, application = build_context(source, declaration())
    expected = evaluate(module_path)
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for path in (module_path, application):
            archive.add(path, arcname=(Path("source") / path.relative_to(source)).as_posix())
    destination = tmp_path / "rebuild"
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(buffer.getvalue()), mode="r:gz") as archive:
        archive.extractall(destination, filter="data")
    rebuilt = destination / "source"
    before = {path: path.read_bytes() for path in rebuilt.rglob("*") if path.is_file()}
    assert not (rebuilt / ".git").exists()
    assert evaluate(rebuilt / "src/macrostates/_build_version.py") == expected
    assert {path: path.read_bytes() for path in before} == before


def test_archived_release_context_preserves_the_verified_source_digest(tmp_path):
    source = tmp_path / "source"
    module_path, _ = candidate_context(source, status="finalized")
    assert evaluate(module_path) == "7.3.25"
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w:gz") as archive:
        for path in source.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.add(path, arcname=(Path("source") / path.relative_to(source)).as_posix())
    destination = tmp_path / "archive"
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(buffer.getvalue()), mode="r:gz") as archive:
        archive.extractall(destination, filter="data")
    rebuilt = destination / "source"
    assert not (rebuilt / ".git").exists()
    assert evaluate(rebuilt / "src/macrostates/_build_version.py") == "7.3.25"
