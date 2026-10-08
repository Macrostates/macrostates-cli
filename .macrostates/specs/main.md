# Macrostates CLI specifications

Create a reusable Python library and command-line application for composing,
installing, inspecting and checking Macrostates specification packages.

## Selected packages and reading order

1. [Meta 2.0.2](000_meta/README.md)
2. [Process 3.0.2](001_process/README.md)
3. [Repository 2.0.2](010_repository-1/README.md)
4. [Python 2.0.2](020_python-1/README.md)
5. [Python-library 1.0.2](031_python-library-1/README.md)
6. [CLI 0.4.0](051_cli/README.md)

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
The current specification revision is `spec-0.2.3`; implementation declaration is
[release.yaml](../implementation/release.yaml). Updates adopt verified tagged
archive snapshots in this repository; other consuming projects require their
own deliberate synchronization.

The implementation remains in bootstrapping pending first-baseline acceptance.
Earlier workflow closures are recorded in implementation history and are
distinct from first-baseline acceptance. Current changes have their own workflow.
The CLI is recommended but optional; equivalent manual verification preserves
the requirements and reports coverage. MIT license applies.
