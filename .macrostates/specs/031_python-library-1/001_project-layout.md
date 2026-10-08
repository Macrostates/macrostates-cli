# Project Layout

Python libraries should use the `src` layout.

## Directory Structure

Library source code should live under `./src/`.

A typical library repository should use this shape:

```text
.macrostates/
  specs/
    main.md
    composition.yaml
    composition.lock.yaml
    000_meta/
    001_process/
  implementation/
    main.md
    release.yaml
    decisions/
    workflows/
      history/
src/
  <package_name>/
tests/
  unit/
  integration/
```

The concrete package name should be a valid Python package name, should be
stable once bootstrapped, and should match the library identity closely enough
that imports are easy to recognize.

## Source Package

Importable library code should live inside the package under `./src/`.

Python modules should be organized by responsibility. Keep public API assembly,
core behavior, adapters, and optional integration code separated when practical.

The package root should not become a dumping ground for unrelated modules.

## Tests

Tests should live outside `./src/` under `./tests/`.

Tests should import the installed package or the package as resolved by project
tooling, rather than relying on accidental imports from the repository root.

## Configuration Files

Python tooling configuration should normally live in `pyproject.toml` when the
tool supports it and when doing so keeps the repository easier to understand.

Generated, build, cache, virtual environment, and temporary files should not be
placed inside `./src/`.

