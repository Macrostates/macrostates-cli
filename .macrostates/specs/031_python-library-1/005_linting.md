# Linting

Python libraries should use linting to catch likely bugs and keep public code
maintainable.

## Tooling

Use Ruff as the normal linter and import sorter.

Lint configuration should live in `pyproject.toml` when practical.

## Posture

Lint rules should prioritize correctness, import hygiene, common Python
modernizations, and readable code. Avoid enabling broad rule sets that create
noise without improving maintainability.

Suppression comments should be narrow and explain intent when the reason is not
obvious.

