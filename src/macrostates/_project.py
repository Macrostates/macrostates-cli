"""Public project API; interface translation lives in the command-line boundary."""

import copy
import re
import shutil
import tempfile
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal

from ._formats import read_composition, read_metadata
from ._integrity import binding, content_hash, extract_archive, inventory, parse_lock
from ._io import dump_yaml, read_yaml, safe_path, string, version
from ._models import Composition, MacrostatesError, Report
from ._mutations import replace_paths
from ._scopes import directory_scopes
from ._sources import GitHubSource, SourceProvider, github_repository
from ._staged import export_index
from ._validation import (
    check_links,
    check_meta,
    check_process,
    has_contract_version,
    process_requires_modern_layout,
    validate_packages,
)

MANIFESTS = ("composition.yaml", "composition.yml")
LAYOUTS = {"modern": ".macrostates/specs", "legacy": "specs"}
LOCK_NAME = "composition.lock.yaml"


class Project:
    """A discovered composition. Read-only methods are offline and do not mutate files.

    Use open() to discover a project or initialize() to create one. Pass source
    explicitly to inject a transport or configure credentials without globals.
    The object reloads configuration at each operation to detect intervening edits.
    """

    def __init__(
        self, root: Path, specs: Path, manifest: Path, *, source: SourceProvider | None = None
    ) -> None:
        self.root = root
        self.specs = specs
        self.manifest = manifest
        self.implementation = (
            specs.parent / "implementation"
            if specs.parent.name == ".macrostates"
            else root / "implementation"
        )
        self.source: SourceProvider = source if source is not None else GitHubSource()

    @classmethod
    def open(cls, path: str | Path = ".", *, source: SourceProvider | None = None) -> "Project":
        start = Path(path).absolute()
        if start.is_file():
            start = start.parent
        for root in (start, *start.parents):
            found: list[Path] = []
            for directory in LAYOUTS.values():
                specs = safe_path(root, directory)
                found.extend(
                    safe_path(specs, name) for name in MANIFESTS if (specs / name).exists()
                )
            if len(found) > 1:
                raise MacrostatesError("Ambiguous composition: multiple manifests or layouts exist")
            if found:
                project = cls(root, found[0].parent, found[0], source=source)
                project._composition()
                return project
            if (root / ".git").exists():
                break
        raise MacrostatesError(
            "No composition found; run macrostates init or select the project directory"
        )

    @classmethod
    def initialize(
        cls,
        root: str | Path,
        *,
        name: str | None = None,
        packages: Sequence[tuple[str, str]] = (),
        manifest: dict[str, Any] | str | Path | None = None,
        layout: Literal["modern", "legacy"] = "modern",
        source: SourceProvider | None = None,
    ) -> "Project":
        directory = Path(root).absolute()
        if not directory.is_dir() or directory.is_symlink():
            raise MacrostatesError(
                "Initialization requires an existing directory without symbolic links"
            )
        if layout not in LAYOUTS:
            raise MacrostatesError("Unknown layout; choose modern or legacy")
        for location in LAYOUTS.values():
            candidate = safe_path(directory, location)
            if any((candidate / filename).exists() for filename in MANIFESTS):
                raise MacrostatesError(
                    "Project already has a composition; initialization will not overwrite it"
                )
        if manifest is not None:
            if packages or name:
                raise MacrostatesError("Use either a supplied manifest or name/package selections")
            data = (
                copy.deepcopy(manifest) if isinstance(manifest, dict) else read_yaml(Path(manifest))
            )
        else:
            if not packages:
                raise MacrostatesError(
                    "Select packages explicitly; no stack or latest versions are assumed"
                )
            selection = []
            conventional = {
                "meta": "000_meta",
                "process": "001_process",
                "repository-1": "010_repository-1",
                "docker-1": "011_docker-1",
                "python-1": "020_python-1",
                "python-project-1": "030_python-project-1",
                "python-library-1": "031_python-library-1",
                "android-app-1": "040_android-app-1",
            }
            for index, (package_name, selected) in enumerate(packages):
                version(selected)
                if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", package_name):
                    raise MacrostatesError("Package names must be portable identifiers")
                if package_name not in conventional:
                    raise MacrostatesError(
                        "Custom packages require a supplied manifest with a real source URL"
                    )
                selection.append(
                    {
                        "name": package_name,
                        "version": selected,
                        "path": conventional.get(package_name, f"{100 + index:03d}_{package_name}"),
                        "entrypoint": "README.md",
                        "source": {
                            "type": "github-archive",
                            "repository": f"https://github.com/Macrostates/macrostates-{package_name}.git",
                            "tag": "v" + selected,
                        },
                    }
                )
            order = [item["name"] for item in selection]
            data = {
                "schema_version": 1,
                "project": {"name": string(name, "name"), "entrypoint": "main.md"},
                "packages": selection,
                "authority_order": order,
                "reading_order": order,
            }
            process = next((item for item in selection if item["name"] == "process"), None)
            if process and has_contract_version(process["version"]):
                data["project"]["version"] = "spec-0.1.0"
        composition = read_composition(data)
        specs = safe_path(directory, LAYOUTS[layout])
        project = cls(directory, specs, specs / "composition.yaml", source=source)
        project._validate_paths(composition)
        layout_report = Report()
        check_meta(composition, specs, directory, layout_report)
        if not layout_report.ok:
            raise MacrostatesError("; ".join(item.message for item in layout_report.diagnostics))
        process = next((item for item in composition.packages if item.name == "process"), None)
        if process and process_requires_modern_layout(process.version) and layout != "modern":
            raise MacrostatesError(
                f"Process {process.version} requires the modern .macrostates/ layout"
            )
        package_lines = "\n".join(
            f"- [{package.name} {package.version}]({package.path}/{package.entrypoint})"
            for package in composition.packages
        )
        order_lines = "\n".join(
            f"{index}. {package}" for index, package in enumerate(composition.reading_order, 1)
        )
        authority = (
            ", ".join(composition.authority_order) or "Define explicitly before installation."
        )
        overview = f"# {composition.name} specifications\n\nDescribe the project's purpose and requirements here.\n\n## Selected packages\n\n{package_lines}\n\n## Reading order\n\n{order_lines}\n\n## Authority\n\nHighest to lowest: {authority}. Directory-scoped specifications apply only to their enclosing directory; define their authority here before use.\n\nSelection and sources: [composition.yaml](composition.yaml).\n"
        if composition.schema_version == 1:
            meta = next((item for item in composition.packages if item.name == "meta"), None)
            guidance = (
                "These locations and snapshot sources follow the selected Meta 2 layout."
                if meta and version(meta.version)[0] == 2
                else "These explicit project-level location and transport choices take precedence over selected packages' older layout and subtree conventions."
            )
            overview += f"\n## Layout and verification\n\nSpecification files live under `{specs.relative_to(directory).as_posix()}/`; implementation documentation lives under `{project.implementation.relative_to(directory).as_posix()}/`. Packages marked `github-archive` are tracked release snapshots checked against `composition.lock.yaml`. {guidance} Local packages remain editable. Process, when selected, owns composition/implementation version policy. CLI checks supplement specification reading and do not establish implementation conformance.\n"
        agent_target = (specs.relative_to(directory) / composition.entrypoint).as_posix()
        planned = {
            project.manifest: dump_yaml(data),
            safe_path(specs, composition.entrypoint): overview,
            safe_path(
                project.implementation, "main.md"
            ): "# Implementation\n\nProject phase: specification\n\nNo accepted implementation baseline exists.\n",
        }
        agents = directory / "AGENTS.md"
        if not agents.exists():
            planned[agents] = (
                f"Read [{agent_target}]({agent_target}) and follow its composition, reading order and authority rules.\n"
            )
        if any(path.exists() or path.is_symlink() for path in planned):
            raise MacrostatesError("Initialization would overwrite existing project files")
        workspace = Path(tempfile.mkdtemp(prefix=".macrostates-init-", dir=directory))
        try:
            replacements = {}
            for index, (destination, contents) in enumerate(planned.items()):
                prepared = workspace / str(index)
                prepared.write_text(contents, encoding="utf-8")
                replacements[destination] = prepared
            replace_paths(replacements, workspace, allow_existing=False)
        except MacrostatesError as exc:
            # Keep explicit recovery files if rollback itself failed.
            if not str(exc).startswith("Rollback failed;"):
                shutil.rmtree(workspace)
            raise
        except OSError as exc:
            shutil.rmtree(workspace)
            raise MacrostatesError("Initialization failed; created files were rolled back") from exc
        else:
            shutil.rmtree(workspace)
        return project

    def _composition(self) -> Composition:
        result = read_composition(read_yaml(self.manifest))
        self._validate_paths(result)
        return result

    def _validate_paths(self, composition: Composition) -> None:
        reserved = {composition.entrypoint, *MANIFESTS, LOCK_NAME, ".macrostates-operation"}
        for control in (*MANIFESTS, LOCK_NAME, ".macrostates-operation"):
            if (
                composition.entrypoint == control
                or composition.entrypoint.startswith(control + "/")
                or control.startswith(composition.entrypoint + "/")
            ):
                raise MacrostatesError("Project entrypoint overlaps a composition control file")
        for package in composition.packages:
            safe_path(self.specs, package.path)
            safe_path(self.specs, package.path + "/" + package.entrypoint)
            if any(
                package.path == path
                or package.path.startswith(path + "/")
                or path.startswith(package.path + "/")
                for path in reserved
            ):
                raise MacrostatesError("Package destination overlaps a composition control file")
            if package.source.get("type") in ("github-archive", "git-subtree"):
                github_repository(package.source["repository"])
            if package.source.get("type") == "git-subtree":
                actual = (self.specs.relative_to(self.root) / package.path).as_posix()
                if package.source["prefix"] != actual:
                    raise MacrostatesError(
                        "Git subtree prefix does not match its package destination"
                    )

    def _roots(self, composition: Composition) -> dict[str, Path]:
        return {
            package.name: safe_path(self.specs, package.path) for package in composition.packages
        }

    def lint(self) -> Report:
        """Check selected metadata, dependencies and local specification links offline."""
        composition = self._composition()
        report, _ = validate_packages(composition, self._roots(composition))
        entry = safe_path(self.specs, composition.entrypoint)
        if not entry.is_file():
            report.add("entrypoint.project_missing", "Project specification entrypoint is missing")
        for key, selected in (
            ("authority_order", composition.authority_order),
            ("reading_order", composition.reading_order),
        ):
            if not selected:
                report.add(
                    "order.manual",
                    f"Legacy {key} is not machine-readable; inspect the project entrypoint",
                    warning=True,
                )
        check_links(self.specs, self.root, report)
        for _, scoped_specs in directory_scopes(self.root, self.specs):
            check_links(scoped_specs, self.root, report)
        check_meta(composition, self.specs, self.root, report)
        check_process(composition, self.implementation, report)
        return report

    def info(self) -> dict[str, Any]:
        """Return composition and available package requirements without network access."""
        composition = self._composition()
        packages = []
        for package in composition.packages:
            item = binding(package)
            metadata = safe_path(self.specs, package.path + "/package.yaml")
            if metadata.is_file():
                parsed = read_metadata(read_yaml(metadata))
                item["dependencies"] = [asdict(dependency) for dependency in parsed.dependencies]
                item["optional_dependencies"] = [
                    asdict(dependency) for dependency in parsed.optional_dependencies
                ]
            packages.append(item)
        return {
            "project": composition.name,
            "schema_version": composition.schema_version,
            "specs": self.specs.relative_to(self.root).as_posix(),
            "packages": packages,
            "authority_order": list(composition.authority_order),
            "reading_order": list(composition.reading_order),
            "directory_specifications": [
                {
                    "scope": scope.relative_to(self.root).as_posix(),
                    "entrypoint": (local / "main.md").relative_to(self.root).as_posix(),
                }
                for scope, local in directory_scopes(self.root, self.specs)
            ],
        }

    def _lock_records(self, *, required: bool = True) -> dict[str, Any]:
        path = safe_path(self.specs, LOCK_NAME)
        if not path.exists():
            if required:
                raise MacrostatesError(
                    "No integrity lockfile; run install or lock against verified source releases"
                )
            return {}
        return parse_lock(read_yaml(path))

    def verify(self) -> Report:
        """Compare installed external packages with their recorded inventories offline."""
        composition = self._composition()
        external = {
            package.name: package
            for package in composition.packages
            if package.source.get("type") != "local"
        }
        report = Report()
        if not external:
            return report
        records = self._lock_records()
        for name in sorted(set(records) - set(external)):
            report.add("lock.unselected", f"Lock contains an unselected package: {name}")
        for name, package in external.items():
            record = records.get(name)
            if not record:
                report.add("lock.missing", f"No locked source for {name}")
                continue
            if record["selection"] != binding(package):
                report.add(
                    "lock.stale",
                    f"Selection changed for {name}; deliberately install the selected release",
                )
                continue
            try:
                actual = inventory(safe_path(self.specs, package.path))
            except (MacrostatesError, OSError) as exc:
                report.add("integrity.invalid", f"{name}: {exc}", package.path)
                continue
            expected = record["files"]
            for path in sorted(set(actual) | set(expected)):
                status = (
                    "added"
                    if path not in expected
                    else "missing"
                    if path not in actual
                    else "modified"
                    if actual[path] != expected[path]
                    else None
                )
                if status:
                    report.add(
                        "integrity." + status, f"{name}: {status} file", package.path + "/" + path
                    )
        return report

    def check(self, *, staged: bool = False) -> Report:
        """Combine lint and integrity checks, optionally against the Git index."""
        if staged:
            with tempfile.TemporaryDirectory(prefix="macrostates-index-") as directory:
                root = export_index(self.root, Path(directory))
                return Project.open(root, source=self.source).check()
        report = self.lint()
        try:
            report.diagnostics.extend(self.verify().diagnostics)
        except MacrostatesError as exc:
            report.add("lock.invalid", str(exc))
        return report

    def install(self, *, locked: bool = False) -> Report:
        """Install archive releases; refuse modified packages or subtree conversion.

        Existing selections reuse their locked commit and reject moved tags.
        locked=True also prohibits changed selections and a missing lockfile.
        """
        return self._synchronize(lock_only=False, locked=locked)

    def lock(self) -> Report:
        """Record integrity only after existing copies match canonical release contents."""
        return self._synchronize(lock_only=True, locked=False)

    def _synchronize(self, *, lock_only: bool, locked: bool) -> Report:
        composition = self._composition()
        records = self._lock_records(required=locked)
        lock_path = safe_path(self.specs, LOCK_NAME)
        original_lock = lock_path.read_bytes() if lock_path.exists() else None
        external = [
            package for package in composition.packages if package.source.get("type") != "local"
        ]
        for package in external:
            kind = package.source.get("type")
            if kind not in ("github-archive", "git-subtree"):
                raise MacrostatesError(f"{package.name} has no installable source")
            if kind == "git-subtree" and not lock_only:
                raise MacrostatesError(
                    "Archive install cannot convert Git subtrees; use Git subtree maintenance or an explicit migration"
                )
            if locked and records.get(package.name, {}).get("selection") != binding(package):
                raise MacrostatesError("Locked installation requires unchanged package selections")
        if locked and set(records) != {package.name for package in external}:
            raise MacrostatesError("Locked installation requires an exact selected package set")
        operation = safe_path(self.specs, ".macrostates-operation")
        try:
            operation.touch(exist_ok=False)
        except FileExistsError as exc:
            raise MacrostatesError(
                "Another package operation is running; inspect .macrostates-operation before recovery"
            ) from exc
        try:
            workspace = Path(
                tempfile.mkdtemp(prefix=".macrostates-install-", dir=self.specs.parent)
            )
        except OSError:
            operation.unlink(missing_ok=True)
            raise
        retain_workspace = False
        try:
            roots = self._roots(composition)
            new_records = {}
            replacements: dict[Path, Path] = {}
            originals: dict[Path, dict[str, Any]] = {}
            for index, package in enumerate(external):
                previous = records.get(package.name)
                selected = self.source.resolve(package.source["repository"], package.source["tag"])
                if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", selected):
                    raise MacrostatesError("Source returned an invalid commit ID")
                if (
                    previous
                    and previous["selection"] == binding(package)
                    and selected != previous["commit"]
                ):
                    raise MacrostatesError(
                        f"Release tag moved for {package.name}; its locked identity is preserved"
                    )
                destination = roots[package.name]
                prepared = workspace / f"package-{index}"
                prepared.mkdir()
                extract_archive(
                    self.source.download(package.source["repository"], selected), prepared
                )
                files = inventory(prepared)
                if (
                    previous
                    and previous["selection"] == binding(package)
                    and files != previous["files"]
                ):
                    raise MacrostatesError(
                        f"Source contents differ from the lock for {package.name}"
                    )
                if destination.exists():
                    current = inventory(destination)
                    originals[destination] = current
                    if current != files:
                        if lock_only or previous is None or current != previous["files"]:
                            raise MacrostatesError(
                                f"Local files differ for {package.name}; preserve or restore them before installing"
                            )
                elif lock_only:
                    raise MacrostatesError(f"Cannot lock missing package: {package.name}")
                if not lock_only:
                    replacements[destination] = prepared
                roots[package.name] = prepared
                new_records[package.name] = {
                    "selection": binding(package),
                    "commit": selected,
                    "content_sha256": content_hash(files),
                    "files": files,
                }
            report, _ = validate_packages(composition, roots)
            if not report.ok:
                return report
            lock_data = {"schema_version": 1, "packages": new_records}
            parse_lock(lock_data)
            prepared_lock = workspace / LOCK_NAME
            prepared_lock.write_text(dump_yaml(lock_data), encoding="utf-8")
            replacements[safe_path(self.specs, LOCK_NAME)] = prepared_lock
            # Recheck after network access, before the first destination changes.
            if self._composition().raw != composition.raw:
                raise MacrostatesError(
                    "Composition changed during installation; nothing was installed"
                )
            for destination, expected in originals.items():
                if inventory(destination) != expected:
                    raise MacrostatesError(
                        "Package files changed during installation; nothing was installed"
                    )
            for destination in replacements:
                if (
                    destination != lock_path
                    and destination not in originals
                    and destination.exists()
                ):
                    raise MacrostatesError(
                        "A package destination appeared during installation; it was preserved"
                    )
            current_lock = lock_path.read_bytes() if lock_path.exists() else None
            if current_lock != original_lock:
                raise MacrostatesError(
                    "Lockfile changed during installation; nothing was installed"
                )
            replace_paths(replacements, workspace)
            return report
        except MacrostatesError as exc:
            retain_workspace = str(exc).startswith("Rollback failed;")
            raise
        except OSError as exc:
            raise MacrostatesError("Package operation failed; changes were rolled back") from exc
        finally:
            operation.unlink(missing_ok=True)
            if not retain_workspace:
                shutil.rmtree(workspace)
