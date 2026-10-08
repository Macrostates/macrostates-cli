"""Strict YAML and filesystem boundaries shared by the format adapters."""

import json
import re
from collections.abc import Hashable
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

from ._models import MacrostatesError

MAX_DOCUMENT = 2 * 1024 * 1024


class StrictLoader(yaml.SafeLoader):
    def compose_node(self, parent: Any, index: Any) -> Any:
        if self.check_event(yaml.AliasEvent):
            raise MacrostatesError("YAML aliases are unsupported; use explicit values")
        return super().compose_node(parent, index)

    def construct_mapping(self, node: Any, deep: bool = False) -> dict[Hashable, Any]:
        mapping: dict[Hashable, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise MacrostatesError("YAML mapping keys must be strings")
            if key in mapping:
                raise MacrostatesError(f"Duplicate YAML key: {key}")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


# Dates stay strings. Do not alter PyYAML's global resolver state.
StrictLoader.yaml_implicit_resolvers = {
    key: [(tag, pattern) for tag, pattern in values if tag != "tag:yaml.org,2002:timestamp"]
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def parse_yaml(data: bytes | str) -> dict[str, Any]:
    if len(data) > MAX_DOCUMENT:
        raise MacrostatesError("YAML document exceeds the 2 MiB limit")
    try:
        result = yaml.load(data, Loader=StrictLoader)
    except (yaml.YAMLError, UnicodeError, RecursionError) as exc:
        raise MacrostatesError("Invalid YAML document") from exc
    return mapping(result, "document")


def read_yaml(path: Path) -> dict[str, Any]:
    if path.is_symlink():
        raise MacrostatesError("YAML documents must not be symbolic links")
    with path.open("rb") as stream:
        return parse_yaml(stream.read(MAX_DOCUMENT + 1))


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.dump(data, Dumper=ExplicitDumper, sort_keys=False, allow_unicode=True)


class ExplicitDumper(yaml.SafeDumper):
    def ignore_aliases(self, data: Any) -> bool:
        return True


def mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise MacrostatesError(f"{label} must be a mapping")
    return value


def string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MacrostatesError(f"{label} must be a nonempty string")
    if any(ord(char) < 32 for char in value):
        raise MacrostatesError(f"{label} contains control characters")
    return value


def relative_path(value: Any, label: str) -> str:
    text = string(value, label).rstrip("/")
    parts = text.split("/")
    if (
        not text
        or PurePosixPath(text).is_absolute()
        or any(part in ("", ".", "..", ".git") for part in parts)
        or "\\" in text
        or ":" in text
    ):
        raise MacrostatesError(f"{label} must be a safe relative POSIX path")
    return text


def safe_path(root: Path, relative: str) -> Path:
    normalized = relative_path(relative, "path")
    current = root
    if root.is_symlink():
        raise MacrostatesError("Project directories must not be symbolic links")
    for part in normalized.split("/"):
        current = current / part
        if current.is_symlink():
            raise MacrostatesError("Symbolic links are not allowed in managed paths")
    if not current.resolve().is_relative_to(root.resolve()):
        raise MacrostatesError("Path escapes the project directory")
    return current


def version(value: Any) -> tuple[int, int, int]:
    text = string(value, "version")
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", text):
        raise MacrostatesError("Versions must be MAJOR.MINOR.PATCH without suffixes")
    major, minor, patch = text.split(".")
    return int(major), int(minor), int(patch)


def canonical(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
