"""Setuptools version source, evaluated only during a distribution build."""

import hashlib
import json
import re
from collections.abc import Hashable
from datetime import date
from pathlib import Path
from typing import Any

import yaml


class DeclarationLoader(yaml.BaseLoader):
    """Build isolation cannot import the application; keep this reader standalone."""

    def construct_mapping(self, node: Any, deep: bool = False) -> dict[Hashable, Any]:
        result: dict[Hashable, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError("Invalid or duplicate build declaration key")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def numeric_version(value: Any) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value
    ):
        raise ValueError("Build version must be MAJOR.MINOR.REVISION")
    major, minor, revision = value.split(".")
    return int(major), int(minor), int(revision)


def source_digest(root: Path) -> str:
    """Fingerprint shipped inputs without Git or a self-referential declaration."""
    paths = [
        root / name
        for name in (
            "README.md",
            "LICENSE",
            "pyproject.toml",
            "MANIFEST.in",
            ".macrostates/implementation/release.yaml",
        )
    ]
    package = root / "src/macrostates"
    if package.is_symlink():
        raise ValueError("Application source must not be a symbolic link")
    paths += [
        path
        for path in package.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and not path.name.endswith((".pyc", ".pyo"))
    ]
    files = {}
    for path in sorted(paths):
        if path.is_symlink():
            raise ValueError("Application build inputs must not be symbolic links")
        if path.is_file():
            files[path.relative_to(root).as_posix()] = {
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "executable": bool(path.stat().st_mode & 0o111),
            }
    return hashlib.sha256(
        json.dumps(files, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def release_version() -> str:
    application = Path(__file__).parents[2] / ".macrostates/implementation/application.yaml"
    if application.is_symlink():
        raise ValueError("Application declaration must not be a symbolic link")
    if application.exists():
        if application.is_symlink():
            raise ValueError("Application declaration must not be a symbolic link")
        with application.open(encoding="utf-8") as stream:
            data = yaml.load(stream, Loader=DeclarationLoader)
        if not isinstance(data, dict) or data.get("schema_version") != "1":
            raise ValueError("Application version declaration needs schema_version: 1")
        selected = data.get("version")
        if not isinstance(selected, str) or not re.fullmatch(
            r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:(?:a|b|rc)[0-9]+)?(?:\.dev[0-9]+)?(?:\+[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?",
            selected,
        ):
            raise ValueError("Application version must use the declared Python distribution format")
        state = data.get("status")
        if state not in {"development", "candidate", "finalized"}:
            raise ValueError("Application declaration needs an explicit build state")
        if state == "development" and not re.search(r"(?:a|b|rc)[0-9]+|\.dev[0-9]+", selected):
            raise ValueError(
                "Development source must not build as an old stable application release"
            )
        if not str(data.get("specification", "")).startswith("specs-") or not str(
            data.get("implementation", "")
        ).startswith("imp-"):
            raise ValueError(
                "Application declaration needs exact specification and implementation references"
            )
        spec = numeric_version(str(data["specification"]).removeprefix("specs-"))
        imp = numeric_version(str(data["implementation"]).removeprefix("imp-"))
        if spec[:2] != imp[:2]:
            raise ValueError("Application provenance contract Major.Minor is not aligned")
        if state in {"candidate", "finalized"}:
            recorded = data.get("source_sha256")
            if not isinstance(recorded, str) or recorded != source_digest(
                Path(__file__).parents[2]
            ):
                raise ValueError(
                    "Application release source changed or lacks its verified source digest"
                )
        stamp = data.get("release_date")
        if not isinstance(stamp, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
            raise ValueError("Application release_date must be YYYY-MM-DD")
        date.fromisoformat(stamp)
        return selected
    declaration = Path(__file__).parents[2] / ".macrostates/implementation/release.yaml"
    if declaration.is_symlink():
        raise ValueError("Build declaration must not be a symbolic link")
    data = yaml.load(declaration.read_text(encoding="utf-8"), Loader=DeclarationLoader)
    if not isinstance(data, dict):
        raise ValueError("Build declaration must be a mapping")
    selected = data.get("version")
    current = numeric_version(selected)
    baseline = data.get("specification")
    if not isinstance(baseline, str) or not baseline.startswith("spec-"):
        raise ValueError("Build declaration needs specification: spec-MAJOR.MINOR.REVISION")
    if current[:2] != numeric_version(baseline.removeprefix("spec-"))[:2]:
        raise ValueError("Build declaration Major.Minor is not aligned")
    stamp = data.get("release_date")
    if not isinstance(stamp, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
        raise ValueError("Build declaration needs release_date: YYYY-MM-DD")
    date.fromisoformat(stamp)
    assert isinstance(selected, str)
    return selected


VERSION = release_version()
