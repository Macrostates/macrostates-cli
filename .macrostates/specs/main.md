# Macrostates CLI specifications

Create a reusable Python library and command-line application for composing,
installing, inspecting and checking Macrostates specification packages.

## Selected packages and reading order

1. [Meta 2.0.0](000_meta/README.md)
2. [Process 3.0.0](001_process/README.md)
3. [Repository 2.0.0](010_repository-1/README.md)
4. [Python 2.0.0](020_python-1/README.md)
5. [Python-library 1.0.0](031_python-library-1/README.md)
6. [CLI 0.3.0](051_cli/README.md)

[composition.yaml](composition.yaml) records selection and sources;
[composition.lock.yaml](composition.lock.yaml) records verified release contents.
Every external package is an unchanged, tracked canonical release snapshot.
Package-owned dependencies determine compatibility; local CLI requirements are
editable under deliberate specification work.

## Authority and layout

Highest to lowest: CLI, Python-library, Python, Repository, Process, Meta.
Directory specifications apply only to their enclosing component, below project
CLI requirements. Numbering expresses browsing order, not authority.

Meta owns `.macrostates/specs/` and immutable external package installation.
Process owns `.macrostates/implementation/`, workflow and contract version rules.
The current specification revision is `spec-0.2.1`; implementation declaration is
[release.yaml](../implementation/release.yaml). This adoption was explicitly
requested, including new package major releases and migration from subtrees to
archive snapshots. It does not migrate other consuming projects.

The implementation remains in bootstrapping pending first-baseline acceptance.
Workflow closure was explicitly requested and is recorded in implementation
history; it is distinct from first-baseline acceptance. The CLI is recommended but optional; equivalent manual verification
preserves the requirements and reports coverage. MIT license applies.
