"""Format-1 field primitives; compatibility changes require new adapter modules."""

import re
from typing import Any

from .._io import mapping, relative_path, string, version
from .._models import Composition, Dependency, MacrostatesError, Package


def dependencies(raw: Any, label: str) -> tuple[Dependency, ...]:
    if not isinstance(raw, list):
        raise MacrostatesError(f"{label} must be a list")
    result = []
    for item in raw:
        item = mapping(item, label)
        name = string(item.get("name"), "dependency name")
        selected = string(item.get("version"), "dependency version")
        version(selected)
        constraint = string(item.get("constraint"), "dependency constraint")
        if constraint not in ("exact", "compatible", "at_least"):
            raise MacrostatesError(f"Unsupported dependency constraint: {constraint}")
        if name in {dependency.name for dependency in result}:
            raise MacrostatesError(f"Duplicate dependency: {name}")
        result.append(Dependency(name, selected, constraint))
    return tuple(result)


def composition_fields(data: dict[str, Any], schema: int) -> Composition:
    project = mapping(data.get("project"), "project")
    name = string(project.get("name"), "project.name")
    entrypoint = relative_path(project.get("entrypoint", "main.md"), "project.entrypoint")
    selected = data.get("packages")
    if not isinstance(selected, list) or not selected:
        raise MacrostatesError("packages must be a nonempty list")
    packages: list[Package] = []
    for item in selected:
        item = mapping(item, "package selection")
        package_name = string(item.get("name"), "package name")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", package_name):
            raise MacrostatesError("Package names must be portable identifiers")
        selected_version = string(item.get("version"), "package version")
        version(selected_version)
        path = relative_path(item.get("path"), "package path")
        entry = relative_path(item.get("entrypoint", "README.md"), "package entrypoint")
        if package_name in {package.name for package in packages}:
            raise MacrostatesError(f"Duplicate package name: {package_name}")
        for package in packages:
            left, right = package.path.casefold(), path.casefold()
            if left == right or left.startswith(right + "/") or right.startswith(left + "/"):
                raise MacrostatesError("Package destinations overlap or collide by case")
        source = mapping(item.get("source", {}), "source")
        if any(
            key.casefold()
            in {"token", "password", "credentials", "authorization", "access_token", "github_token"}
            for key in source
        ):
            raise MacrostatesError(
                "Source credentials belong in explicit authentication, not composition metadata"
            )
        if source.get("type") not in (None, "local", "github-archive", "git-subtree"):
            raise MacrostatesError("Unsupported package source type")
        if source.get("type") in ("github-archive", "git-subtree"):
            string(source.get("repository"), "source.repository")
            if source.get("tag") != "v" + selected_version:
                raise MacrostatesError("source.tag must equal v<selected package version>")
            if "commit" in source:
                raise MacrostatesError("Legacy source.commit needs an explicit tag migration")
            if source["type"] == "git-subtree":
                string(source.get("branch"), "source.branch")
                relative_path(source.get("prefix"), "source.prefix")
        legacy = {
            key: item[key] for key in ("dependencies", "optional_dependencies") if key in item
        }
        packages.append(Package(package_name, selected_version, path, entry, source, legacy))

    def order(key: str) -> tuple[str, ...]:
        values = data.get(key, [])
        if not isinstance(values, list):
            raise MacrostatesError(f"{key} must be a list")
        references = {
            reference: package.name
            for package in packages
            for reference in (package.name, package.path + "/" + package.entrypoint)
        }
        result = []
        for value in values:
            if not isinstance(value, str) or value not in references:
                raise MacrostatesError(f"{key} references an unselected package or entrypoint")
            if references[value] in result:
                raise MacrostatesError(f"{key} contains a duplicate package")
            result.append(references[value])
        return tuple(result)

    return Composition(
        schema,
        name,
        entrypoint,
        tuple(packages),
        order("authority_order"),
        order("reading_order"),
        data,
    )
