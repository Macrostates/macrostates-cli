# Macrostates CLI implementation

Project phase: bootstrapping. Implementation version: 0.2.0.
[release.yaml](release.yaml) is the authoritative declaration for spec-0.2.0.
The definer requested both a CLI and a public Python API. Acceptance of this
first baseline remains a separate phase decision. All CLI workflows are closed
under the definer’s explicit instruction; closure does not itself change phase.

## Current behavior

`macrostates` is a console entrypoint backed by the public `macrostates` package.
It implements init, install, lock, verify, lint, info and check, including staged
index checks. The root README owns user instructions and API examples.

Specification directories are tracked snapshots. Installation downloads GitHub
tar archives at tag-resolved commits, validates package metadata/dependencies,
and writes package inventories plus source identities to a format-1 lockfile.
Unchanged selections reject moved tags. `lock` checks canonical bytes before
recording existing copies, including Git-subtree copies. `verify` is offline.
Project-owned packages are linted but remain editable.

The CLI's own composition uses .macrostates/specs with Meta 2.0, Process 3.0,
Repository 2.0, Python 2.0 and Python-library 1.0 as verified archive snapshots.
Its local CLI requirements remain editable. Implementation documentation and
release declarations live under .macrostates/implementation. Source stays in src.

## Architecture

- `_models.py`: normalized composition, package and diagnostic models.
- `_formats/`: composition and metadata reader protocols and explicit registries.
  `v0.py` retains unversioned compositions; `v1.py` owns format-1 conventions.
  `common.py` contains established field primitives shared by those formats.
- `_validation.py`: pure dependency checks, structural links and a release-selected
  policy registry: Meta 2.0 layout/format and Process 2.3/2.4/3.0 declarations.
  Process 3.0 also requires modern artifact locations. Earlier selected releases
  retain their own checks; unknown later policies return explicit diagnostics.
- `_scopes.py`: component entrypoint discovery and independent-composition
  boundaries. Scope roots contain .macrostates; local file links are linted.
- `_build_version.py`: standalone setuptools declaration reader in build isolation.
  `MANIFEST.in` retains the one required release declaration in source distributions.
- `_sources.py`: `SourceProvider` protocol and GitHub HTTP adapter with explicit
  authentication, bounded responses and credential-safe redirects.
- `_integrity.py`: validated archive extraction, file inventories, aggregate
  content hashes and lock format reader.
- `_project.py`: orchestration and supported project API; loads fresh configuration
  per operation and accepts injected source providers.
- `_mutations.py`: replacement transaction and rollback/recovery boundary.
- `_staged.py`: exports the Git index for offline checks without changing Git.
- `_cli.py`: arguments, output rendering and exit-code translation.

Ordinary imports perform no project-local or network I/O. Explicit __version__
access reads installed distribution metadata lazily. Only install/lock use the network. Init and package
operations write locally; no command stages, commits, pushes or changes branches.
All external processes use argument arrays. GitHub authentication is obtained
at the transport boundary and never serialized into project data.

## Extending compatible behavior

Read [the adapter decision](decisions/0001-versioned-format-adapters.md) and
[modern package adoption](decisions/0002-modern-package-adoption.md).
Add a separate reader for a new persisted format, register its explicit version,
and normalize it to the existing models. Keep old readers and historical
fixtures. Change shared field helpers only when the existing contracts are
preserved; format-specific differences belong in the new reader.

Source providers are independent of manifests and validators. A future source
type needs explicit source field validation and an implementation; it must not
silently fall back to GitHub. Process policy changes need a new release-scoped
adapter, with old/new fixtures. Lock changes need an additional reader before
changing the writer. Migrations must be separate explicit operations.

The command/JSON shapes, diagnostics, environment authentication variables,
public root exports and persistent formats are compatibility surfaces. Record
deliberate changes and retain regression tests. This is an initial 0.x API, but
existing documented use should still be treated carefully.

## Verification and limitations

Run the documented uv checks, build a wheel/sdist and exercise the installed
console entrypoint and Python API from a clean location. Tests include actual
metadata from all 21 prior releases and eight current Macrostates package releases, both manifest
formats/layouts, safe installation failure, staged-file integrity and Process
policy isolation. Test fixtures contain synthetic package content only, except
for public-intended specification package metadata.

Package transactions roll back ordinary failures. They do not promise an
atomic power-loss commit; interrupted operations leave inspectable markers and
recovery directories. Locks are reviewable baselines, not signatures. Local
links are checked conservatively for file targets, not Markdown heading anchors.
Scope discovery excludes tool/cache/build/temp and hidden implementation directories;
inspect those scopes manually. Scope semantics and authority need manual reading.
Index snapshots are bounded at 128 MiB and exclude submodule content. Branch-only
or commit-selected legacy sources need explicit tag migration. Git-subtree
updates remain Git operations; archive install refuses implicit conversion.

Semantic contradictions, implementation conformance, update planning, workflows,
remote releases and automatic migrations remain outside supported CLI commands.

Behavior-to-code verification is mapped in
[specification conformance](specification-conformance.md). Workflow records own
dated delivery and closure evidence.

Closed workflow records and dated verification are in
[workflow history](workflows/history/). There are no open CLI workflows.
