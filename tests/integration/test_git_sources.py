import hashlib
import subprocess
from pathlib import Path

import pytest
import yaml

from macrostates import GitSource, MacrostatesError, Project

from ..conftest import composition, metadata


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


@pytest.fixture
def canonical(tmp_path):
    root = tmp_path / "canonical"
    root.mkdir()
    git(root, "init", "--quiet", "--initial-branch=main")
    git(root, "config", "user.name", "Test Maintainer")
    git(root, "config", "user.email", "maintainer@example.invalid")
    (root / "package.yaml").write_text(yaml.safe_dump(metadata("meta", "2.2.0")))
    (root / "README.md").write_text("# Synthetic specifications\n\n[Topic](docs/topic.md)\n")
    (root / "docs").mkdir()
    (root / "docs/topic.md").write_text("# Topic\n\nAn immutable test requirement.\n")
    (root / "check.sh").write_text("#!/bin/sh\nexit 0\n")
    (root / "check.sh").chmod(0o755)
    git(root, "add", ".")
    git(root, "commit", "--quiet", "-m", "Specification release")
    git(root, "tag", "--annotate", "v2.2.0", "-m", "Specification release")
    return root


def initialize(tmp_path, canonical, address=None):
    root = tmp_path / "consumer"
    root.mkdir()
    manifest = composition(versions={"meta": "2.2.0"}, source_type="git-archive")
    manifest["packages"][0]["source"]["repository"] = address or str(canonical)
    return Project.initialize(root, manifest=manifest)


@pytest.mark.parametrize("address_kind", ["absolute", "file", "relative"])
def test_git_archive_install_preserves_exact_tag_inventory(tmp_path, canonical, address_kind):
    address = {
        "absolute": str(canonical),
        "file": canonical.as_uri(),
        "relative": "../canonical",
    }[address_kind]
    project = initialize(tmp_path, canonical, address)
    assert project.install().ok
    assert project.check().ok

    installed = project.specs / "000_meta"
    lock = yaml.safe_load((project.specs / "composition.lock.yaml").read_text())
    record = lock["packages"]["meta"]
    assert record["commit"] == git(canonical, "rev-parse", "v2.2.0^{commit}")
    assert record["selection"]["source"]["repository"] == address
    assert set(record["files"]) == {"README.md", "package.yaml", "docs/topic.md", "check.sh"}
    for relative, details in record["files"].items():
        expected = (canonical / relative).read_bytes()
        assert (installed / relative).read_bytes() == expected
        assert details["sha256"] == hashlib.sha256(expected).hexdigest()
    assert record["files"]["check.sh"]["executable"] is True
    assert (installed / "check.sh").stat().st_mode & 0o111
    assert not (installed / ".git").exists()
    assert project.install(locked=True).ok


def test_moved_git_tag_cannot_replace_locked_package(tmp_path, canonical):
    project = initialize(tmp_path, canonical)
    assert project.install().ok
    lock_path = project.specs / "composition.lock.yaml"
    readme = project.specs / "000_meta/README.md"
    previous_lock, previous_readme = lock_path.read_bytes(), readme.read_bytes()
    (canonical / "README.md").write_text("# Changed release contents\n")
    git(canonical, "add", "README.md")
    git(canonical, "commit", "--quiet", "-m", "Changed contents")
    git(canonical, "tag", "--force", "--annotate", "v2.2.0", "-m", "Moved tag")

    with pytest.raises(MacrostatesError, match="tag moved"):
        project.install()
    assert lock_path.read_bytes() == previous_lock
    assert readme.read_bytes() == previous_readme
    assert not (project.specs / ".macrostates-operation").exists()


@pytest.mark.parametrize("tag_kind", ["lightweight", "missing"])
def test_nonrelease_git_tag_does_not_install_partial_contents(tmp_path, canonical, tag_kind):
    git(canonical, "tag", "--delete", "v2.2.0")
    if tag_kind == "lightweight":
        git(canonical, "tag", "v2.2.0")
    project = initialize(tmp_path, canonical)
    with pytest.raises(MacrostatesError):
        project.install()
    assert not (project.specs / "000_meta").exists()
    assert not (project.specs / "composition.lock.yaml").exists()
    assert not (project.specs / ".macrostates-operation").exists()


def test_modified_local_git_snapshot_is_preserved(tmp_path, canonical):
    project = initialize(tmp_path, canonical)
    assert project.install().ok
    readme = project.specs / "000_meta/README.md"
    readme.write_text("# Local uncommitted requirement\n")
    original = readme.read_bytes()
    with pytest.raises(MacrostatesError, match="Local files differ"):
        project.install()
    assert readme.read_bytes() == original


@pytest.mark.parametrize(
    "address",
    [
        "https://user:synthetic-secret@example.invalid/specs.git",
        "https://synthetic-secret@example.invalid/specs.git",
        "https://example.invalid/specs.git?token=synthetic-secret",
        "ssh://user:synthetic-secret@example.invalid/specs.git",
    ],
)
def test_credential_bearing_git_addresses_are_rejected_without_echo(address):
    with pytest.raises(MacrostatesError) as error:
        GitSource().resolve(address, "v2.2.0")
    assert "synthetic-secret" not in str(error.value)


def test_git_transport_errors_never_echo_credential_stderr(monkeypatch):
    def fail(args, **kwargs):
        return subprocess.CompletedProcess(
            args, 1, stdout="", stderr="remote rejected synthetic-secret credential"
        )

    monkeypatch.setattr("macrostates._sources.subprocess.run", fail)
    with pytest.raises(MacrostatesError) as error:
        GitSource().resolve("https://example.invalid/specs.git", "v2.2.0")
    assert "synthetic-secret" not in str(error.value)
    assert "example.invalid" not in str(error.value)


@pytest.mark.parametrize("tag", ["main", "v2.2.0\n--upload-pack=unsafe", "--help"])
def test_git_transport_rejects_nonrelease_and_option_tags(canonical, tag):
    with pytest.raises(MacrostatesError):
        GitSource().resolve(str(canonical), tag)
