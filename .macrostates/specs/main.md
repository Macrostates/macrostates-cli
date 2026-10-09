# Macrostates CLI specifications

Create a reusable Python library and command-line application for composing,
installing, inspecting and checking Macrostates specification packages.

## Selected packages and reading order

1. [Meta 2.1.0](000_meta/README.md)
2. [Process 4.1.0](001_process/README.md)
3. [Repository 3.1.0](010_repository-1/README.md)
4. [Python 2.1.0](020_python-1/README.md)
5. [Python-library 1.1.0](031_python-library-1/README.md)
6. [CLI 0.5.0](051_cli/README.md)

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
The current specification revision is `spec-0.3.0`; implementation declaration is
[release.yaml](../implementation/release.yaml). Updates adopt verified tagged
archive snapshots in this repository; other consuming projects require their
own deliberate synchronization.

The implementation remains in bootstrapping pending first-baseline acceptance.
Earlier workflow closures are recorded in implementation history and are
distinct from first-baseline acceptance. Current changes have their own workflow.
The CLI is recommended but optional; equivalent manual verification preserves
the requirements and reports coverage. MIT license applies.
