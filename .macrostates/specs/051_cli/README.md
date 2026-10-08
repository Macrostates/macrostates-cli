# CLI requirements

## Scope and reading order

This document defines the CLI contract. Read it after the packages in
the project entrypoint. The import package is macrostates, the distribution is
macrostates-cli, and the command is macrostates. Python minimum is 3.12.

## Commands

- init prepares a selected composition under .macrostates/specs by default.
  Require explicit package selections or a supplied manifest; preserve existing
  files and agent instructions, and never implement application behavior.
- install downloads immutable, tag-selected GitHub source snapshots, checks
  package metadata and dependencies, and records resolved commits and content
  hashes in a separate lockfile. Package directories remain tracked and numbered.
- verify checks downloaded package bytes, file inventory and executable flags
  against the lockfile offline. Local packages remain editable.
- lint checks metadata, selection, dependencies (including optional constraints
  only when selected), cycles, destinations, entrypoints, orders and local links.
- info exposes package versions, paths, sources, dependencies and explicit order.
- check combines lint and verify, and supports a staged Git snapshot for hooks.
- lock can establish a lock for already vendored packages only after verifying
  every file against its canonical source release; it must not bless local edits.

Provide human-readable output, JSON output for automation, and exit codes 0 for
success, 1 for failed checks, 2 for invalid inputs or execution errors. Network
access occurs only for install/lock, never lint/verify/info/check. No command
automatically stages, commits, pushes, changes branches or installs hooks.

## Compatibility

Separate manifest, package metadata, lock and process policy formats. Retain
unversioned composition readers as a legacy adapter, and introduce explicit
schema_version: 1 for new manifests. Preserve reading/authority orders; never
derive them from numbered directories. Detect specs/ and .macrostates/specs/
without moving files; reject ambiguous layouts or duplicate manifests.
Unknown persisted formats fail clearly before writes. Unsupported release policies
produce explicit check diagnostics. There are no implicit migrations.
Unknown extension data must survive init-from-manifest unchanged.
Legacy git-subtree compositions remain inspectable and lintable and can gain a
verified integrity lock; archive install refuses to convert subtree sources.
Git subtree maintenance remains Git's responsibility until explicit migration.

Package release versions are separate from package metadata format versions.
Existing unversioned package.yaml documents use metadata format 1. The new
explicit package schema_version: 1 is equivalent. Format adapters normalize
to domain models, and new formats must receive additional adapters and fixtures.

For Process 2.3.x, 2.4.x and 3.0.x consumers, check release declaration formatting and matching
Major.Minor when a declaration exists. Report missing declarations when an
implementation baseline is explicitly marked active. Process 1.x/2.0–2.2
consumers must not inherit that policy. Unknown Process major/policy versions
must be reported as unsupported for policy checks, not guessed from latest rules.

## Integrity and filesystem behavior

Hash extracted file contents and executable flags, not compressed archive bytes.
Bind locks to package name, version, destination, entrypoint and canonical source.
Locked reinstallation resolves the recorded commit; tag movement is reported
instead of silently adopting it. Do not overwrite modified or unrelated files.
Validate all downloads before writes; roll back ordinary write failures. Reject
unsafe paths, overlapping destinations, symlink escapes, archive links/devices,
duplicate members, case collisions and excessive archive sizes. Never extract
with unvalidated archive paths. Redact credentials from errors and logs.

## Library contract

Expose Project, MacrostatesError, Diagnostic and Report at the package root.
Project.open, initialize, install, lock, lint, verify, check and info constitute
the supported API. Imports perform no network or project-local file access;
the installed distribution metadata supplies __version__. Keep source transport,
filesystem access and version adapters separate and injectable for tests.

## Quality and scope

Use uv, Ruff formatter/linter, Pyright, installed-package pytest tests, py.typed,
an MIT license, an ordinary wheel/sdist and a committed contributor uv.lock.
Verify public commands, real historical metadata, offline operation, staged
checks, refusal of unsafe inputs and write failures. CI runs the same checks.
Automatic update planning, semantic contradiction detection, workflow automation, release
publication and automatic migrations are future work, not this initial release.

## Latest package adoption

Support Meta 2.0.x's .macrostates/specs layout and composition format 1. Process
3.0.x uses .macrostates/implementation and the established contract declarations.
Reject modern-policy selection in the legacy layout; earlier selected releases
retain their existing rules. Never guess future Meta/Process policies.

Detect directory-scoped entrypoints at <component>/.macrostates/specs/main.md;
the component is the scope root. Report scope paths in info and check their local
file links. Do not traverse separately composed subprojects as parent scopes.
Authority, semantic scope limits and workflow conformance still require reading.

This CLI's own tracked specification packages use the latest compatible published
releases, archive sources and a verified lock. The author explicitly requests
this migration; it does not authorize migrating other consuming projects.
The composition baseline is spec-0.2.0 and the implementation is 0.2.0.
Process owns the single .macrostates/implementation/release.yaml declaration.
Python builds consume its version, include that declaration in sdists, and
report the installed distribution version without reading project files at runtime.
Retain historical metadata/format/layout tests and validate real self-installation.
