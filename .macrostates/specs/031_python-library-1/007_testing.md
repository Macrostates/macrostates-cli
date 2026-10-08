# Testing

Python libraries should test public behavior from the installed package
perspective.

## Unit Tests

Unit tests should cover the public API and edge cases that downstream users are
likely to depend on.

Tests should avoid relying on accidental imports from the repository root.

## Integration Tests

When the library integrates with process-global state, files, subprocesses,
network services, or third-party APIs, include focused integration tests for the
supported integration contract.

## Compatibility Tests

When a behavior is documented in the README or depended on by a consuming
project, keep a regression test for it where practical.

Libraries that intentionally integrate with process-global state should test
that installation and cleanup leave the process in a usable state.

