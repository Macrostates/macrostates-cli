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
- Independent library API versioning, authoritative build metadata, and release provenance.
- README and usage documentation expectations.
- Example code placement and maintenance expectations.
- Test expectations for reusable behavior.

Application runtime behavior, service deployment, and domain-specific API
details are out of scope for this package.

The stable public API uses this package's explicit semantic-versioning policy
unless an effective project specification overrides it. Macrostates `specs-*`
and `imp-*` baseline versions remain separate. Process's numeric implementation
default applies only when no explicit application policy governs the release.
Repository integration follows the selected repository policy; library releases
and publication follow the application's policy and authorization.

This release requires Process 5.0.0 and Repository-1 4.0.0 or later, with the
remaining minima declared in `package.yaml`. Earlier package releases retain
their original policies. Explicit `at_least` constraints permit newer selected
majors; review their meaning rather than assuming numeric eligibility proves
semantic compatibility.

## Macrostates artifacts

Follow the selected Meta package's project layout: numbered specification
packages and the project entrypoint are tracked under `.macrostates/specs/`.
Implementation documentation, decisions, workflows and release declarations,
when required by project rules, live under `.macrostates/implementation/`.
Application source, tests, build configuration and runtime configuration retain
their language/tool locations outside `.macrostates/`. This package does not
make the Macrostates CLI mandatory or change the scope of a subproject.

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

## License

This specification package, including its documentation, metadata, and bundled
resources, is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 Lucas Lopez.

## AI assistance

This project was developed with AI assistance.
