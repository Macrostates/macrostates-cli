# Dependency Management

Python libraries should keep runtime dependencies minimal and explicit.

## Tooling

Use `uv` as the normal local interface for virtual environments, dependency
resolution, and running project commands.

## Runtime Dependencies

Runtime dependencies should be declared in `pyproject.toml`.

Do not add a runtime dependency unless it is required by supported library
behavior. Optional integrations should use optional dependency groups or extras
when practical.

## Development Dependencies

Development-only tools such as test runners, linters, formatters, type checkers,
and coverage tools should be separated from runtime dependencies.

## Lockfiles

Reusable libraries may choose whether to commit a lockfile based on their
release and contributor workflow. The choice should be documented when it
matters for reproducibility.

