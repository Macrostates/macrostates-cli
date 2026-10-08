"""Content inventory and bounded extraction of GitHub source archives."""

import hashlib
import io
import re
import tarfile
from pathlib import Path
from typing import Any

from ._io import canonical, mapping, relative_path
from ._models import MacrostatesError, Package

MAX_ARCHIVE = 32 * 1024 * 1024
MAX_EXTRACTED = 128 * 1024 * 1024
MAX_FILES = 10000


def extract_archive(data: bytes, target: Path) -> None:
    if len(data) > MAX_ARCHIVE:
        raise MacrostatesError("Compressed archive exceeds 32 MiB")
    try:
        archive = tarfile.open(fileobj=io.BytesIO(data), mode="r:*")
    except tarfile.TarError as exc:
        raise MacrostatesError("Source is not a valid tar archive") from exc
    with archive:
        seen: set[str] = set()
        root: str | None = None
        total = 0
        plan: list[tuple[tarfile.TarInfo, str]] = []
        for member in archive:
            if len(seen) >= MAX_FILES:
                raise MacrostatesError("Archive exceeds 10000 entries")
            name = relative_path(member.name.rstrip("/"), "archive member")
            parts = name.split("/")
            if root is None:
                root = parts[0]
            if parts[0] != root:
                raise MacrostatesError("Archive must have exactly one root directory")
            folded = name.casefold()
            if folded in seen:
                raise MacrostatesError("Archive has duplicate or case-colliding members")
            seen.add(folded)
            if not (member.isfile() or member.isdir()):
                raise MacrostatesError("Archive links and special files are unsupported")
            if len(parts) == 1:
                if not member.isdir():
                    raise MacrostatesError("Archive files must live below its root directory")
                continue
            if member.size < 0:
                raise MacrostatesError("Archive has an invalid member size")
            total += member.size
            if total > MAX_EXTRACTED:
                raise MacrostatesError("Extracted archive exceeds 128 MiB")
            plan.append((member, "/".join(parts[1:])))
        if not plan:
            raise MacrostatesError("Archive contains no package files")
        try:
            for member, relative in plan:
                destination = target / relative
                if member.isdir():
                    destination.mkdir(parents=True, exist_ok=True)
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    stream = archive.extractfile(member)
                    if stream is None:
                        raise MacrostatesError("Archive member could not be read")
                    with stream, destination.open("xb") as output:
                        output.write(stream.read(member.size + 1))
                    if destination.stat().st_size != member.size:
                        raise MacrostatesError("Truncated archive member")
                    destination.chmod(0o755 if member.mode & 0o111 else 0o644)
        except (OSError, tarfile.TarError) as exc:
            raise MacrostatesError("Archive has conflicting or invalid file entries") from exc


def inventory(root: Path) -> dict[str, dict[str, Any]]:
    if root.is_symlink() or not root.is_dir():
        raise MacrostatesError("Package directory is missing or is a symbolic link")
    result: dict[str, dict[str, Any]] = {}
    seen: set[str] = set()
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise MacrostatesError("Package contains a symbolic link")
        relative = relative_path(path.relative_to(root).as_posix(), "package file")
        if relative.casefold() in seen:
            raise MacrostatesError("Package contains case-colliding paths")
        seen.add(relative.casefold())
        if path.is_dir():
            continue
        if not path.is_file():
            raise MacrostatesError("Package contains a special file")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                digest.update(chunk)
        result[relative] = {
            "sha256": digest.hexdigest(),
            "executable": bool(path.stat().st_mode & 0o111),
        }
    return result


def content_hash(files: dict[str, Any]) -> str:
    return hashlib.sha256(canonical(files)).hexdigest()


def binding(package: Package) -> dict[str, Any]:
    return {
        "name": package.name,
        "version": package.version,
        "path": package.path,
        "entrypoint": package.entrypoint,
        "source": package.source,
    }


def parse_lock(data: dict[str, Any]) -> dict[str, Any]:
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise MacrostatesError("Unsupported lock schema_version; supported: 1")
    packages = mapping(data.get("packages"), "lock.packages")
    for name, raw in packages.items():
        record = mapping(raw, "locked package")
        mapping(record.get("selection"), "lock selection")
        if not isinstance(record.get("commit"), str) or not re.fullmatch(
            r"[0-9a-f]{40}|[0-9a-f]{64}", record["commit"]
        ):
            raise MacrostatesError("Lock commit must be a full Git object ID")
        files = mapping(record.get("files"), "lock files")
        seen: set[str] = set()
        for path, value in files.items():
            relative_path(path, "locked file")
            if path.casefold() in seen:
                raise MacrostatesError("Lock has case-colliding file paths")
            seen.add(path.casefold())
            item = mapping(value, "locked file")
            if not isinstance(item.get("sha256"), str) or not re.fullmatch(
                r"[0-9a-f]{64}", item["sha256"]
            ):
                raise MacrostatesError("Invalid locked file checksum")
            if type(item.get("executable")) is not bool:
                raise MacrostatesError("Locked executable flag must be boolean")
        if record.get("content_sha256") != content_hash(files):
            raise MacrostatesError(f"Inconsistent lock checksum for {name}")
    return packages
