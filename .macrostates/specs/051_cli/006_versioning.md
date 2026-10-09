# Versioning and compatibility

## Independent identities

Distinguish package releases, persisted schemas, selected Meta/Process policies,
project specification versions and implementation versions. New package releases
do not imply new schemas or dictate the CLI's Major number. Meta owns local
package versioning. Process owns `spec-MAJOR.MINOR.REVISION` and implementation
`MAJOR.MINOR.REVISION`, sharing contract Major.Minor with independent revisions.
Editorial restructuring may advance spec revision without a runtime version bump
or rewriting a release's exact earlier baseline. Verify actual contract coverage;
matching numbers alone do not establish conformance.

## Formats and layouts

| Surface | Interpretation |
| --- | --- |
| Composition without schema, or explicit 0 | Legacy format 0 |
| Composition schema 1 | Explicit orders and archive-capable format 1 |
| Package metadata without schema, or explicit 1 | Metadata format 1 |
| Lock schema 1 | Inventory lock format 1 |
| Locations | Modern and legacy, subject to selected policies |

New shorthand uses format 1; supplied manifests retain format/extensions.
Unknown formats fail clearly without replacing installed packages or rewriting
existing documents. Downloaded metadata is checked before replacements. Reading
legacy contexts never migrates them. Future support must preserve older documented
behavior and regression fixtures; internal adapter design remains an implementer
choice. Branch-only/commit-selected sources need explicit tag migration.

## Release-selected policies

Meta 2.0.x and 2.1.x require `.macrostates/specs/` and composition format 1.
Meta 2.1's dependency authoring default does not make omitted constraints valid
or select newer packages automatically. Earlier releases do not inherit these
checks. Other Meta policies at Major 2 or above receive unsupported diagnostics;
initialization refuses unknown Meta layout policies.

Process 2.3.x, 2.4.x, 3.0.x, 4.0.x and 4.1.x require composition contract versions.
When a release declaration exists, validate numeric implementation version, specification baseline
and calendar-valid `release_date: YYYY-MM-DD`. Composition, implementation and
baseline Major.Minor must match; baseline spec revision cannot exceed the current
spec revision. Implementation revision is independent. An implementation `main.md`
explicitly declaring `Project phase: active` without release declaration receives
a missing-release diagnostic. This check does not infer acceptance or behavior.

Process 3.0.x, 4.0.x and 4.1.x additionally require
`.macrostates/implementation/`; initialization refuses legacy layout.
Process 4.0's feature-branch and PR requirements remain implementer responsibilities
and require manual workflow review; a passing CLI check does not establish them.
Process 4.1 changes dependency constraints without changing declaration validation.
Process 1.x and 2.0–2.2 retain earlier checks; other policies receive unsupported
diagnostics rather than guessed rules. Supplied-manifest initialization is not
full process/package conformance; review, install and lint.

## Distribution version

This repository's authoritative implementation declaration is
`.macrostates/implementation/release.yaml`. Isolated builds read its version,
refuse missing/invalid declarations, validate matching implementation/baseline
Major.Minor and calendar date, and include the declaration in the sdist.
Rebuilding version identity requires no local spec packages, Git state or network.

Installed version/API/command reporting uses distribution metadata without source
checkout access. Builds never edit declarations, create tags or publish releases;
normal dependency installation may still require an index. Preserve public API,
commands/output and persisted formats; document deliberate compatibility changes.
