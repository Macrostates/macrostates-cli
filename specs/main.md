# Macrostates CLI specifications

Create a reusable Python library and command-line application for composing,
installing, inspecting and checking Macrostates specification packages.

## Selected packages and reading order

1. [Meta 1.7.0](000_meta/README.md)
2. [Process 1.8.0](001_process/README.md)
3. [Repository 1.1.2](010_repository-1/README.md)
4. [Python 1.0.2](020_python-1/README.md)
5. [Python-library 0.3.0](031_python-library-1/README.md)
6. [CLI 0.1.0](051_cli/README.md)

The machine-readable selection and verified release sources are in
[composition.yaml](composition.yaml). Package requirements remain package-owned.
Process 1.8.0 satisfies Python-library's Process 1.x dependency; Process 2.x is
not selected for this repository. CLI consumer projects may select other versions.

## Authority

Highest to lowest: CLI, Python-library, Python, Repository, Process, Meta.
Directory specifications apply only to their enclosing component, below the
project CLI requirements. Numbering expresses browsing order, not authority.
The CLI's generated consumer layout is explicitly defined by the CLI package;
this repository retains the existing specs/ and implementation/ conventions.

The definer's explicit request authorizes initial specification preparation and
bootstrapping together. The implementation remains in bootstrapping pending
acceptance. Package-owned documents must remain unchanged. MIT license applies.
