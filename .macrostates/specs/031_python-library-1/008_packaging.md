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

## Build Outputs

Built package artifacts should be written to `./dist/` and should not be
committed unless an explicit release workflow requires it.

Package builds should include intended package source, package metadata, license
files, README files, typed package markers, and explicitly included resources.

