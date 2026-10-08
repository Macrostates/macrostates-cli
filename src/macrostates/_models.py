"""Normalized domain models, independent of any persisted format."""

from dataclasses import dataclass, field
from typing import Any


class MacrostatesError(Exception):
    """Invalid configuration or an operation that cannot safely be performed."""


@dataclass(frozen=True)
class Diagnostic:
    """A stable machine-readable code and a human-readable check result."""

    code: str
    message: str
    path: str | None = None
    severity: str = "error"


@dataclass
class Report:
    """Check results. Warnings do not make a report unsuccessful."""

    diagnostics: list[Diagnostic] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(item.severity == "error" for item in self.diagnostics)

    def add(
        self, code: str, message: str, path: str | None = None, *, warning: bool = False
    ) -> None:
        self.diagnostics.append(Diagnostic(code, message, path, "warning" if warning else "error"))


@dataclass(frozen=True)
class Dependency:
    name: str
    version: str
    constraint: str


@dataclass(frozen=True)
class Package:
    name: str
    version: str
    path: str
    entrypoint: str
    source: dict[str, Any]
    legacy_dependencies: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Metadata:
    name: str
    version: str
    entrypoint: str
    dependencies: tuple[Dependency, ...]
    optional_dependencies: tuple[Dependency, ...]


@dataclass(frozen=True)
class Composition:
    schema_version: int
    name: str
    entrypoint: str
    packages: tuple[Package, ...]
    authority_order: tuple[str, ...]
    reading_order: tuple[str, ...]
    raw: dict[str, Any]
