"""Explicit declaration migration; published Git history is never rewritten."""

import tempfile
from pathlib import Path
from typing import Any

from ._git import commit, ensure_development
from ._io import dump_yaml, read_yaml, version
from ._models import MacrostatesError
from ._mutations import replace_paths
from ._versioning import calendar_date


def migrate_versioning(root: Path) -> dict[str, Any]:
    ensure_development(root, clean=False)
    manifests = [
        root / ".macrostates/specs" / name for name in ("composition.yaml", "composition.yml")
    ]
    manifests = [item for item in manifests if item.is_file()]
    if len(manifests) != 1:
        raise MacrostatesError("Migration requires one modern composition manifest")
    manifest = manifests[0]
    composition = read_yaml(manifest)
    old_spec = composition.get("project", {}).get("version")
    release = root / ".macrostates/implementation/release.yaml"
    previous = read_yaml(release) if release.exists() else None
    if isinstance(old_spec, str) and old_spec.startswith("specs-"):
        if previous is None or (
            previous.get("schema_version") == 2
            and str(previous.get("version", "")).startswith("imp-")
        ):
            return {"changed": False, "message": "Version declarations already use the new format."}
        raise MacrostatesError("Mixed declaration formats need explicit repair before migration")
    if not isinstance(old_spec, str) or not old_spec.startswith("spec-"):
        raise MacrostatesError("Migration needs a valid legacy spec-MAJOR.MINOR.PATCH baseline")
    version(old_spec.removeprefix("spec-"))
    new_spec = "specs-" + old_spec.removeprefix("spec-")
    composition["project"]["version"] = new_spec
    mapping: dict[str, Any] = {
        "schema_version": 1,
        "specification": {"identity": new_spec, "legacy_tag": old_spec},
        "note": "Identity spelling migration preserves existing tags; it does not finalize current development contents.",
    }
    replacements_data = {manifest: composition}
    if previous is not None:
        old_imp = previous.get("version")
        version(old_imp)
        assert isinstance(old_imp, str)
        calendar_date(previous.get("release_date"))
        baseline = previous.get("specification")
        if not isinstance(baseline, str) or not baseline.startswith("spec-"):
            raise MacrostatesError("Legacy implementation needs an exact spec- baseline")
        version(baseline.removeprefix("spec-"))
        if version(old_imp)[:2] != version(baseline.removeprefix("spec-"))[:2]:
            raise MacrostatesError("Repair legacy contract alignment before migration")
        new_imp = "imp-" + old_imp
        previous.update(
            {
                "schema_version": 2,
                "version": new_imp,
                "specification": "specs-" + baseline.removeprefix("spec-"),
            }
        )
        replacements_data[release] = previous
        mapping["implementation"] = {"identity": new_imp, "legacy_tag": "v" + old_imp}
    for item in (mapping.get("specification"), mapping.get("implementation")):
        if item is not None:
            try:
                item["commit"] = commit(root, "refs/tags/" + item["legacy_tag"])
            except MacrostatesError:
                item["commit"] = None
    destination = root / ".macrostates/implementation/version-migration.yaml"
    if destination.exists():
        raise MacrostatesError(
            "Existing migration provenance must be preserved; inspect it before migrating"
        )
    replacements_data[destination] = mapping
    originals = {path: path.read_bytes() if path.exists() else None for path in replacements_data}
    with tempfile.TemporaryDirectory(prefix=".macrostates-migrate-", dir=root) as directory:
        workspace = Path(directory)
        replacements = {}
        for index, (path, data) in enumerate(replacements_data.items()):
            prepared = workspace / str(index)
            prepared.write_text(dump_yaml(data), encoding="utf-8")
            replacements[path] = prepared
        if any(
            (path.read_bytes() if path.exists() else None) != original
            for path, original in originals.items()
        ):
            raise MacrostatesError("Declarations changed during migration; nothing was replaced")
        replace_paths(replacements, workspace)
    return {
        "changed": True,
        "specification": new_spec,
        "message": "Declarations migrated; adopt verified packages, review pending state and application policies before integration.",
    }
