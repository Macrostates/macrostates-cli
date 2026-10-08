import io
import tarfile
from pathlib import Path

import pytest
import yaml

from macrostates import MacrostatesError, Project

from ..conftest import FakeSource, archive, composition, metadata


@pytest.mark.parametrize("kind", ["modified", "missing", "added", "executable"])
def test_integrity_detects_changes(project, kind):
    readme = project.specs / "000_meta/README.md"
    if kind == "modified":
        readme.write_text("changed")
    elif kind == "missing":
        readme.unlink()
    elif kind == "added":
        (readme.parent / "unexpected.md").write_text("extra")
    else:
        readme.chmod(0o755)
    report = project.verify()
    assert not report.ok
    assert report.diagnostics[0].code == "integrity." + (
        "modified" if kind == "executable" else kind
    )


def test_read_only_methods_never_contact_source(project, source):
    source.calls.clear()
    assert project.verify().ok
    assert project.lint().ok
    assert project.check().ok
    assert project.info()["packages"][0]["name"] == "meta"
    assert source.calls == []


def test_modified_package_is_not_overwritten_or_blessed(project):
    path = project.specs / "000_meta/README.md"
    path.write_text("local edits")
    before = (project.specs / "composition.lock.yaml").read_bytes()
    for operation in (project.install, project.lock):
        with pytest.raises(MacrostatesError, match="Local files differ"):
            operation()
        assert path.read_text() == "local edits"
        assert (project.specs / "composition.lock.yaml").read_bytes() == before


def test_locked_install_restores_missing_directory(project):
    import shutil

    shutil.rmtree(project.specs / "000_meta")
    assert project.install(locked=True).ok
    assert project.check().ok


def test_moved_tag_is_rejected(project, source):
    source.add(text="changed upstream")
    with pytest.raises(MacrostatesError, match="tag moved"):
        project.install()
    assert project.verify().ok


def test_manual_version_update_replaces_clean_previous_release(project, source):
    source.add(version="1.1.0", text="# New release\n")
    data = yaml.safe_load(project.manifest.read_text())
    data["packages"][0]["version"] = "1.1.0"
    data["packages"][0]["source"]["tag"] = "v1.1.0"
    project.manifest.write_text(yaml.safe_dump(data))
    with pytest.raises(MacrostatesError, match="unchanged package selections"):
        project.install(locked=True)
    assert project.install().ok
    assert (project.specs / "000_meta/README.md").read_text() == "# New release\n"
    assert project.verify().ok


def test_unknown_lock_is_not_overwritten(project):
    path = project.specs / "composition.lock.yaml"
    path.write_text("schema_version: 99\npackages: {}\n")
    before = path.read_bytes()
    with pytest.raises(MacrostatesError, match="lock schema_version"):
        project.install()
    assert path.read_bytes() == before


def test_local_packages_remain_editable(tmp_path, source):
    data = composition(("meta", "project"))
    data["packages"][1]["source"] = {"type": "local"}
    project = Project.initialize(tmp_path, manifest=data, source=source)
    local = project.specs / "001_project"
    local.mkdir()
    (local / "package.yaml").write_text(yaml.safe_dump(metadata("project")))
    (local / "README.md").write_text("# Local requirements\n")
    assert project.install().ok
    (local / "README.md").write_text("# Changed local requirements\n")
    assert project.check().ok


def test_init_preserves_extensions_and_existing_agent_instructions(tmp_path):
    instructions = tmp_path / "AGENTS.md"
    instructions.write_text("Existing instructions")
    data = composition()
    data["extensions"] = {"future-integration": {"enabled": True}}
    project = Project.initialize(tmp_path, manifest=data)
    assert yaml.safe_load(project.manifest.read_text())["extensions"] == data["extensions"]
    assert instructions.read_text() == "Existing instructions"
    with pytest.raises(MacrostatesError, match="already has"):
        Project.initialize(tmp_path, manifest=data)


def test_legacy_subtree_lock_without_conversion(tmp_path, source):
    data = composition(schema=None, source_type="git-subtree")
    project = Project.initialize(tmp_path, manifest=data, layout="legacy", source=source)
    from macrostates._integrity import extract_archive

    package = project.specs / "000_meta"
    package.mkdir()
    extract_archive(
        source.download(
            "https://github.com/example/meta.git",
            source.resolve("https://github.com/example/meta.git", "v1.0.0"),
        ),
        package,
    )
    assert project.lock().ok
    assert Project.open(tmp_path, source=source).check().ok
    with pytest.raises(MacrostatesError, match="cannot convert Git subtrees"):
        project.install()
    assert "schema_version" not in yaml.safe_load(project.manifest.read_text())


def test_symlink_escape_rejected(project, tmp_path):
    (project.specs / "000_meta/escape").symlink_to(tmp_path.parent, target_is_directory=True)
    assert not project.verify().ok
    with pytest.raises(MacrostatesError, match="symbolic link"):
        project.install()


@pytest.mark.parametrize(
    "bad_name,kind",
    [
        ("snapshot/../../escape", "file"),
        ("snapshot/link", "symlink"),
        ("snapshot/device", "device"),
        ("snapshot/.git/config", "file"),
    ],
)
def test_unsafe_archives_leave_destinations_untouched(tmp_path, bad_name, kind):
    source = FakeSource()
    repository, commit = source.add()
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as stream:
        member = tarfile.TarInfo(bad_name)
        if kind == "symlink":
            member.type, member.linkname = tarfile.SYMTYPE, "/outside"
        elif kind == "device":
            member.type = tarfile.CHRTYPE
        stream.addfile(member)
    source.archives[commit] = buffer.getvalue()
    project = Project.initialize(tmp_path, manifest=composition(), source=source)
    with pytest.raises(MacrostatesError):
        project.install()
    assert not (project.specs / "000_meta").exists()
    assert not (project.specs / "composition.lock.yaml").exists()


def test_write_failure_rolls_back_package_and_lock(project, source, monkeypatch):
    source.add(version="1.1.0", text="# Updated\n")
    data = yaml.safe_load(project.manifest.read_text())
    data["packages"][0].update(version="1.1.0")
    data["packages"][0]["source"]["tag"] = "v1.1.0"
    project.manifest.write_text(yaml.safe_dump(data))
    before_package = (project.specs / "000_meta/README.md").read_bytes()
    before_lock = (project.specs / "composition.lock.yaml").read_bytes()
    rename = Path.rename
    failed = False

    def failing_rename(path, destination):
        nonlocal failed
        if (
            path.name == "composition.lock.yaml"
            and ".macrostates-install-" in str(path.parent)
            and not failed
        ):
            failed = True
            raise OSError("Simulated write failure")
        return rename(path, destination)

    monkeypatch.setattr(Path, "rename", failing_rename)
    with pytest.raises(MacrostatesError, match="rolled back"):
        project.install()
    assert failed
    assert (project.specs / "000_meta/README.md").read_bytes() == before_package
    assert (project.specs / "composition.lock.yaml").read_bytes() == before_lock


def test_competing_layouts_rejected(project):
    legacy = project.root / "specs"
    legacy.mkdir()
    (legacy / "composition.yaml").write_bytes(project.manifest.read_bytes())
    with pytest.raises(MacrostatesError, match="Ambiguous"):
        Project.open(project.root)


def test_missing_links_fail_lint(project):
    (project.specs / "000_meta/README.md").write_text(
        "[Missing](missing.md)\n```\n[Example](example.md)\n```\n"
    )
    report = project.lint()
    assert [diagnostic.code for diagnostic in report.diagnostics] == ["link.missing"]


def test_source_mutation_during_download_preserves_local_files(project, source):
    download = source.download
    path = project.specs / "000_meta/README.md"

    def changing_download(repository, commit):
        payload = download(repository, commit)
        path.write_text("Concurrent local edit")
        return payload

    source.download = changing_download
    with pytest.raises(MacrostatesError):
        project.install()
    assert path.read_text() == "Concurrent local edit"


def test_new_destination_during_download_is_preserved(tmp_path, source):
    project = Project.initialize(tmp_path, manifest=composition(), source=source)
    download = source.download

    def changing_download(repository, commit):
        payload = download(repository, commit)
        path = project.specs / "000_meta"
        path.mkdir()
        (path / "unrelated").write_text("Preserve")
        return payload

    source.download = changing_download
    with pytest.raises(MacrostatesError):
        project.install()
    assert (project.specs / "000_meta/unrelated").read_text() == "Preserve"


def test_unknown_metadata_does_not_install_any_package(tmp_path, source):
    repository, commit = source.add()
    data = metadata()
    data["schema_version"] = 9
    source.archives[commit] = archive({"package.yaml": yaml.safe_dump(data), "README.md": "# Test"})
    project = Project.initialize(tmp_path, manifest=composition(), source=source)
    report = project.install()
    assert not report.ok
    assert not (project.specs / "000_meta").exists()


def test_unknown_shorthand_package_does_not_invent_repository(tmp_path):
    with pytest.raises(MacrostatesError, match="real source"):
        Project.initialize(tmp_path, name="example", packages=[("unknown", "1.0.0")])


def test_yml_manifest_and_nested_discovery(project):
    renamed = project.manifest.with_suffix(".yml")
    project.manifest.rename(renamed)
    nested = project.root / "src/component"
    nested.mkdir(parents=True)
    assert Project.open(nested).manifest == renamed


def test_duplicate_manifest_rejected(project):
    project.manifest.with_suffix(".yml").write_bytes(project.manifest.read_bytes())
    with pytest.raises(MacrostatesError, match="Ambiguous"):
        Project.open(project.root)


def test_operation_marker_prevents_parallel_install(project):
    marker = project.specs / ".macrostates-operation"
    marker.touch()
    with pytest.raises(MacrostatesError, match="Another package operation"):
        project.install()
    assert marker.exists()


def test_shorthand_manifest_roundtrips_without_yaml_aliases(tmp_path):
    project = Project.initialize(
        tmp_path, name="example", packages=[("meta", "1.7.0"), ("process", "2.3.0")]
    )
    reopened = Project.open(tmp_path)
    assert reopened.info()["reading_order"] == ["meta", "process"]
    assert reopened.info()["authority_order"] == ["meta", "process"]
    assert yaml.safe_load(project.manifest.read_text())["project"]["version"] == "spec-0.1.0"
