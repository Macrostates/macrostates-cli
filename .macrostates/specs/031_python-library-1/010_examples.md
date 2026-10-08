# Examples

Python libraries may include example code when it helps downstream users
understand supported usage.

## Location

Runnable examples should live under a top-level `./examples/` directory.

Examples should not live under `./src/` because they are not part of the
importable library package. They should not live only in tests because their
primary audience is a library user, not just a maintainer.

## Scope

Examples should be small, focused, and runnable from a clean checkout when their
declared dependencies are available.

Examples should demonstrate realistic use of the public API without copying
large application files, private project behavior, credentials, datasets, or
environment-specific paths from a consuming project.

When an example is inspired by code from another project, reduce it to mock or
synthetic behavior that illustrates the library usage pattern. Do not preserve
unrelated domain logic merely because it appeared in the source material.

## Dependencies

Examples should prefer the library's normal runtime dependencies and the Python
standard library.

If an example requires an optional or third-party dependency, document that
dependency near the example and keep it isolated from examples that should run
without optional extras.

## Imports

Examples should import the library through its public package API.

Avoid imports from private modules or from repository layout paths such as
`vendor.<library>`.

## Verification

Important examples should be exercised by lightweight tests or smoke commands
when practical. Example verification should not require private external
services, secrets, or large local datasets.

