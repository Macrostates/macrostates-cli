# Library API

Python libraries should expose a small, intentional public API.

## Public Surface

The package root should export the names that ordinary users are expected to
import. Internal helpers should stay in private modules or unexported modules
unless they are deliberately part of the supported API.

Public names should be documented or discoverable from the README. Removing,
renaming, or materially changing public behavior is a compatibility decision.

## Import Behavior

Importing a library should not perform surprising I/O, replace process-global
state, start background work, configure unrelated loggers, read project-local
files, or depend on the current working directory.

When a library needs process-global integration, expose an explicit function,
context manager, or object method that callers can choose at runtime.

## Configuration

Library defaults should be usable without configuration, but configuration
should be explicit at public boundaries.

Environment variables may provide integration hooks, but they should not be the
only way to configure supported behavior. Environment variables used by the
library are part of the public compatibility surface.

