# Packaging

Python libraries should be buildable and installable as ordinary Python
distributions.

## Package Metadata

The repository should include `pyproject.toml` with package name, version,
description, supported Python version, authors or maintainers, license metadata,
runtime dependencies, and build backend configuration.

The distribution name and import package name may differ, but the relationship
should be obvious and documented when they do.

## Versioning

Library versions should use semantic versioning once the public API is declared
stable.

Before stability, `0.x` versions may change more freely, but public README
examples and downstream users should still be treated with care.

This is an explicit library distribution policy: classify incompatible public
API or behavior changes, compatible additions, and fixes against the library's
supported surface. Its Major.Minor.Patch need not match the repository's
`specs-*` or `imp-*` baselines. A project-local specification can explicitly
override the library policy according to composition authority. An override
must identify its version scheme, public compatibility promises, version source,
assignment mechanism, required checks, and release conditions.

When no explicit application policy applies, use Process's default: the numeric
part of the finalized implementation baseline selected for that release, without
the `imp-` prefix or development suffix. This fallback does not replace an
effective stable-library semantic-versioning policy. Specification package
versions are separate and do not determine the library distribution version.

Process change records describe repository specification and implementation
impacts. Library release preparation additionally evaluates the library's public
API impact under its application policy; Macrostates tooling must not silently
assign an independent distribution version. A new repository baseline does not
automatically release every library in a monorepo. Unchanged published libraries
retain their original versions and exact baseline provenance.

## Authoritative Version Source

Maintain one editable authority for the distribution version. `pyproject.toml`
either contains it or configures the build backend's deterministic reading of
another tracked application declaration. The optional Process deliverables
document may describe that policy and its baseline references. Avoid competing
hand-edited version constants in package source, build configuration, and CI.

Distribution versions must satisfy Python version syntax. Raw Macrostates
development identities such as `imp-1.2.3-branch.feature-x.gabc123` are not
valid Python distribution versions. The application policy supplies an
appropriate development representation and provenance without claiming changed
development source is the unchanged stable release.

Builds must produce the declared distribution version without Git, network
lookup, local version settings, or a particular current working directory.
Include every authoritative version resource needed to rebuild a source
distribution. Ordinary builds must not advance versions, edit release records,
or create commits or tags. Exposed runtime version reporting must agree with the
installed distribution metadata.

## Release Preparation And Provenance

Follow Process and the selected repository policy for branch synchronization,
change records, closed integration-preparation workflows, current-target
validation, and reviewed baseline finalization. The library's release policy
separately governs distribution version assignment, tags, and publication. No
particular hosting platform or external changeset product is required.

Every finalized library release records its deliverable identity, distribution
version, exact specification and implementation baselines, and source commit.
Independent distribution versions need not share Major.Minor with their
Macrostates references. Preserve the original records of unchanged published
libraries; do not rewrite them to the latest repository baseline. Use
unambiguous application release/tag namespaces in a monorepo.

Before authorized publication, verify public API compatibility, candidate version
uniqueness, exact baseline references, and wheel/source-distribution metadata.
Test installation from built artifacts when practical. Source-distribution
rebuilding must work without the original Git checkout, and runtime version
reporting must match the installed artifact. Preserve published identities and
report candidate, tagged, and uploaded states distinctly.

## Build Outputs

Built package artifacts should be written to `./dist/` and should not be
committed unless an explicit release workflow requires it.

Package builds should include intended package source, package metadata, license
files, README files, typed package markers, and explicitly included resources.
