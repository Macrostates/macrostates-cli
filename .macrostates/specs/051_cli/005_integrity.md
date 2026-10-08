# Installation and integrity

## Canonical identity and lock

Resolve release tags, including annotated tags, to full commit IDs; download the
exact commit's tar snapshot. Obtaining specifications requires no clone, build
or code execution. Validate archives before writing destinations. Accept regular
files/directories under one root; reject traversal, links, special files,
duplicates, case collisions, Git metadata and excessive resource use. Limits must
be finite and errors clear; exact values/extraction algorithms belong in
implementation documentation.

`composition.lock.yaml` beside the composition has `schema_version: 1` and
`packages` keyed by external package name. Each record contains `selection`
(name, version, path, entrypoint, source), `commit`, `files`, `content_sha256`.
Each relative file has `sha256` and boolean `executable`. Identity covers file
inventory, bytes and whether executable, excluding compression, timestamps,
ownership and other permission bits; empty directories do not contribute.

The aggregate is SHA-256 of the UTF-8 JSON file map using sorted keys, compact
separators and unescaped Unicode. This is a persisted format interoperability
rule, independent of internal hashing choices. Validate record shapes, full
commit IDs, safe paths, digest formats, executable flags and aggregate consistency.
Locks are reviewable baselines, not signatures. Offline verification establishes
agreement with recorded data, not remote tag identity or edited-lock trust.

## Installation, updates and locking

Validate all candidate package metadata/dependencies, including local packages,
before replacing packages/lock. Leave local content untouched. Install missing
copies; replace existing content only if it matches the candidate or is a clean
copy of a previously locked release. Preserve modified or unrelated content.

For unchanged locked selections, re-resolve the tag, refuse moved commits and
changed canonical inventories, and download the resolved commit. Locked install
requires the exact unchanged external set/bindings and can restore a missing
copy. Ordinary updates require deliberate version/tag/selection changes and a
clean previous inventory. Do not rewrite the composition/human requirements or
automatically delete unselected package directories.

Canonical `lock` requires every external copy present and equivalent to its
selected release, including inventory and executable flags, before writing the
lock. Never adopt local edits as a baseline. Exclude local packages. Archive
install refuses subtree conversion; existing tagged subtree copies may gain a
verified lock without changing Git history.

## Failure behavior

Refuse competing CLI package operations. Detect composition, lock, existing-copy
and newly appearing destination changes during download before replacement;
preserve intervening edits. Do not promise complete isolation from arbitrary
external writes at every instant. Roll back ordinary replacement failures.
If rollback fails, retain recoverable files and identify their location.
Power-loss/process-crash atomicity is not guaranteed; consult
[Recovery](annex_recovery.md) before retrying interrupted operations.
