"""Setuptools version source, evaluated only during a distribution build."""

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


def release_version() -> str:
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
