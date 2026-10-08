# Explicit version adapters and a shared library core

Status: accepted as an implementation choice within the authorized initial CLI.

## Context

Macrostates packages evolve independently. Existing consumers have unversioned
compositions and Git subtrees. The new CLI adds archive snapshots, a lockfile
and a hidden project layout. Applying the latest rules to every consumer would
reinterpret old projects. The definer also wants a supported Python library.

## Decision

Separate package release versions, persisted format versions and Process policy
versions. Normalize explicit format readers to domain models; retain existing
readers and fixtures. Add new adapters before enabling new formats. Reject
unknown formats instead of guessing. Select Process declaration behavior from
its actual selected package release. Do not automatically rewrite metadata,
change directories or convert Git provenance.

Use a typed Python package with a small root API and a console entrypoint as an
interface adapter. Keep networking injectable, imports side-effect-free, and
structural validation independent of CLI rendering. Use PyYAML as the sole
runtime dependency because both metadata and composition are YAML documents.
Use the specification-mandated uv, Ruff, Pyright and pytest development tools.
Commit uv.lock for reproducible contributor environments.

## Consequences

New versions can coexist with old readers. Compatibility remains bounded by
documented adapters; unsupported future policies are visible diagnostics.
Regression tests must exercise historical metadata and both persisted formats.
The public API and command outputs require deliberate compatibility decisions.

Initial archive installation handles GitHub only. Existing subtrees can gain a
verified integrity lock but keep their Git maintenance semantics. Migration and
automatic update planning are explicit future work.

The original release support set is historical. Current policy extensions and
self-adoption are recorded in [modern package adoption](0002-modern-package-adoption.md);
format adapter separation and retention remain applicable.
