import json
import subprocess
import sys
from pathlib import Path

import yaml

from ..conftest import composition


def command(*arguments, cwd):
    executable = Path(sys.executable).parent / "macrostates"
    return subprocess.run(
        [str(executable), *arguments], cwd=cwd, capture_output=True, text=True, check=False
    )


def test_installed_command_help_and_version(tmp_path):
    assert command("--help", cwd=tmp_path).returncode == 0
    assert command("--version", cwd=tmp_path).stdout.strip() == "macrostates 0.1.0"


def test_json_success_and_failed_checks(project):
    result = command("info", "--json", cwd=project.root)
    assert result.returncode == 0
    assert json.loads(result.stdout)["packages"][0]["name"] == "meta"
    assert command("check", "--json", cwd=project.root).returncode == 0
    (project.specs / "000_meta/README.md").write_text("modified")
    result = command("verify", "--json", cwd=project.root)
    assert result.returncode == 1
    assert json.loads(result.stdout)["diagnostics"][0]["code"] == "integrity.modified"


def test_invalid_project_returns_structured_error(tmp_path):
    result = command("verify", "--json", cwd=tmp_path)
    assert result.returncode == 2
    assert json.loads(result.stdout)["error"]["code"] == "operation.invalid"
    assert "Traceback" not in result.stderr


def test_cli_initialization(tmp_path):
    manifest = tmp_path / "input.yaml"
    manifest.write_text(yaml.safe_dump(composition()))
    result = command("init", "--from", str(manifest), "--json", cwd=tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["ok"]
    assert (tmp_path / ".macrostates/specs/composition.yaml").exists()


def git(root, *arguments):
    return subprocess.run(["git", "-C", str(root), *arguments], capture_output=True, check=True)


def test_staged_snapshot_uses_index_instead_of_working_files(project):
    git(project.root, "init", "-b", "main")
    git(project.root, "add", ".")
    (project.specs / "000_meta/README.md").write_text("Unstaged modification")
    assert project.check(staged=True).ok
    assert not project.check().ok
    git(project.root, "add", ".macrostates/specs/000_meta/README.md")
    (project.specs / "000_meta/README.md").write_text("# Test specifications\n")
    assert project.check().ok
    assert not project.check(staged=True).ok
    assert command("check", "--staged", "--json", cwd=project.root).returncode == 1


def test_import_has_no_filesystem_network_or_logging_side_effects(tmp_path):
    script = """
import logging, pathlib, socket, subprocess
def forbidden(*args, **kwargs):
    raise AssertionError("Import performed unexpected I/O")
pathlib.Path.open = forbidden
socket.create_connection = forbidden
subprocess.run = forbidden
logging.basicConfig = forbidden
import macrostates
assert macrostates.Project
"""
    result = subprocess.run(
        [sys.executable, "-c", script], cwd=tmp_path, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr


def test_info_invalid_metadata_returns_controlled_error(project):
    (project.specs / "000_meta/package.yaml").write_text("name: meta\nversion: 1.0.0\n")
    result = command("info", "--json", cwd=project.root)
    assert result.returncode == 2
    assert json.loads(result.stdout)["error"]["code"] == "operation.invalid"
    assert "Traceback" not in result.stderr
