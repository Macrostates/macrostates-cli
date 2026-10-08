"""Explicit format registry. New formats add readers without changing old readers."""

from typing import Any, Protocol

from .._models import Composition, MacrostatesError, Metadata
from .v0 import LegacyComposition
from .v1 import CompositionV1, MetadataV1


class CompositionReader(Protocol):
    def read(self, data: dict[str, Any]) -> Composition: ...


class MetadataReader(Protocol):
    def read(self, data: dict[str, Any]) -> Metadata: ...


COMPOSITION_READERS: dict[int, CompositionReader] = {0: LegacyComposition(), 1: CompositionV1()}
METADATA_READERS: dict[int, MetadataReader] = {1: MetadataV1()}


def select_version(data: dict[str, Any], default: int) -> int:
    selected = data.get("schema_version", default)
    if type(selected) is not int:
        raise MacrostatesError("schema_version must be an integer")
    return selected


def read_composition(data: dict[str, Any]) -> Composition:
    selected = select_version(data, 0)
    reader = COMPOSITION_READERS.get(selected)
    if reader is None:
        raise MacrostatesError(f"Unsupported composition schema_version: {selected}")
    return reader.read(data)


def read_metadata(data: dict[str, Any]) -> Metadata:
    selected = select_version(data, 1)
    reader = METADATA_READERS.get(selected)
    if reader is None:
        raise MacrostatesError(f"Unsupported package metadata schema_version: {selected}")
    return reader.read(data)
