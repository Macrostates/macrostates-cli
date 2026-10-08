# Type Checking

Python libraries should expose useful type information at public boundaries.

## Tooling

Use Pyright as the normal static type checker.

Type checking should focus first on public API behavior, stable boundaries, and
code paths that downstream users are likely to depend on.

## Typed Packages

When the public API has meaningful type annotations, the package should include
a `py.typed` marker so downstream type checkers can use those annotations.

Type annotations should clarify behavior. They should not force awkward code
when the runtime behavior is intentionally dynamic.

