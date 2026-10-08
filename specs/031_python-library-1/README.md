# Python library specification package

This package describes reusable conventions for Python libraries. It sits beside
the generic Python project conventions and directly defines the project shape,
tooling, public API, compatibility, packaging, and documentation expectations
needed by reusable libraries.

## Macrostates

This package is part of Macrostates, a project for composing reusable
specification packages into specs-driven development projects.

## Scope

- Public API ownership and compatibility expectations.
- Import-time side effect boundaries.
- Library repository layout and dependency posture.
- Formatting, linting, and type-checking expectations.
- Library packaging and metadata expectations.
- README and usage documentation expectations.
- Example code placement and maintenance expectations.
- Test expectations for reusable behavior.

Application runtime behavior, service deployment, and domain-specific API
details are out of scope for this package.

## Reading order

1. [Project Layout](001_project-layout.md)
2. [Dependency Management](002_dependency-management.md)
3. [Library API](003_library-api.md)
4. [Formatting](004_formatting.md)
5. [Linting](005_linting.md)
6. [Type Checking](006_type-checking.md)
7. [Testing](007_testing.md)
8. [Packaging](008_packaging.md)
9. [Documentation](009_documentation.md)
10. [Examples](010_examples.md)
