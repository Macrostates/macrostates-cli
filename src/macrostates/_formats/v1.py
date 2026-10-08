"""Version 1 archive composition and existing package metadata readers."""

import re
from datetime import datetime
from typing import Any

from .._io import relative_path, string, version
from .._models import Composition, MacrostatesError, Metadata
from .common import composition_fields, dependencies


class CompositionV1:
    def read(self, data: dict[str, Any]) -> Composition:
        result = composition_fields(data, 1)
        names = {package.name for package in result.packages}
        for field in (result.authority_order, result.reading_order):
            if set(field) != names:
                raise MacrostatesError(
                    "Format 1 requires complete authority_order and reading_order"
                )
        return result


class MetadataV1:
    def read(self, data: dict[str, Any]) -> Metadata:
        name = string(data.get("name"), "package.name")
        selected = string(data.get("version"), "package.version")
        version(selected)
        string(data.get("description"), "package.description")
        stamp = string(data.get("versioned_at"), "package.versioned_at")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", stamp):
            raise MacrostatesError("versioned_at must be YYYY-MM-DD HH:mm")
        try:
            datetime.strptime(stamp, "%Y-%m-%d %H:%M")
        except ValueError as exc:
            raise MacrostatesError("versioned_at must be YYYY-MM-DD HH:mm") from exc
        entry = relative_path(data.get("entrypoint"), "package.entrypoint")
        return Metadata(
            name,
            selected,
            entry,
            dependencies(data.get("dependencies", []), "dependencies"),
            dependencies(data.get("optional_dependencies", []), "optional_dependencies"),
        )
