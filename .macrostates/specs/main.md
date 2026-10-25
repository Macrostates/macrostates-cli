# Macrostates CLI specifications

Create a reusable Python library and command-line application for composing,
installing, inspecting and checking Macrostates specification packages.

## Selected packages and reading order

1. [Meta 3.0.0](000_meta/README.md)
2. [Process 6.0.0](001_process/README.md)
3. [Repository 4.0.0](010_repository-1/README.md)
4. [Python 2.1.1](020_python-1/README.md)
5. [Python-library 2.0.0](031_python-library-1/README.md)
6. [CLI 3.0.0](051_cli/README.md)

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
The last finalized specification baseline is declared by `project.version` in
[composition.yaml](composition.yaml); the implementation baseline and exact
specification reference are in [release.yaml](../implementation/release.yaml).
Development retains those numeric baselines until a reviewed release proposal
finalizes pending scope. Updates adopt verified tagged
archive snapshots in this repository; other consuming projects require their
own deliberate synchronization.

Project phase and first-baseline acceptance are recorded in the
[implementation entrypoint](../implementation/main.md). Workflow closure and
phase acceptance are separate decisions. Earlier closures are preserved in
implementation history; current work has its own scoped records.
The CLI is recommended but optional; equivalent manual verification preserves
the requirements and reports coverage. MIT license applies.
