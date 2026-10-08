# Macrostates CLI specification

This local package defines the observable contract of the Macrostates command
and supported Python library: discovery, composition, installation, inspection,
verification and compatibility. Internal modules, algorithms and tooling
constants remain implementation choices.

Read it after the packages selected by the project entrypoint. Meta owns package
and composition conventions, Process owns workflows and project version policy,
and Python-library owns general library quality rules. This package supplies
CLI-specific requirements within that composition.

## Core reading order

1. [Concepts and boundaries](001_concepts.md)
2. [Python library](002_library.md)
3. [Commands and output](003_commands.md)
4. [Composition and discovery](004_composition.md)
5. [Installation and integrity](005_integrity.md)
6. [Versioning and compatibility](006_versioning.md)
7. [Verification expectations](007_verification.md)

## Conditional guidance

Read [Recovery and legacy maintenance](annex_recovery.md) when an operation
fails, a package was edited or removed, a tag moved, or a legacy subtree needs
maintenance. Core documents define routine behavior.

The repository README provides installation and usage examples. Implementation
documentation owns architecture, exact resource limits, dated evidence and
mapping these requirements to code and tests.
