# Concepts and boundaries

## Product identity

The distribution is `macrostates-cli`, import package is `macrostates`, and
installed command is `macrostates`. Python 3.12 is the minimum supported version.
The command and library implement the same operations and validation rules.
Distribute an ordinary wheel and source distribution with typing information
and an MIT license.

## Project and package ownership

A composition selects exact package releases, sources, destinations, entrypoints,
reading order and authority order. Numbered directories aid browsing; they do
not determine precedence. Selection is deliberate: do not infer a stack, select
dependencies or fetch a latest version automatically.

External packages are tracked, readable snapshots with identity recorded in a
separate integrity lock. Project-owned packages marked `source.type: local`
remain editable and linted, and are excluded from external inventory verification.
Source omission in older manifests does not implicitly classify content as local.

New projects default to `.macrostates/specs/` and `.macrostates/implementation/`.
Source, tests and ordinary tool configuration retain their normal locations.
Legacy locations remain discoverable under [Versioning](006_versioning.md).

## Operation boundaries

Only installation and canonical locking contact package sources. Initialization,
inspection, lint, integrity verification and combined checks operate offline.
Read-only operations preserve project files; staged checks may create temporary
snapshots without changing the checkout or index.

No command automatically stages, commits, pushes, changes branches, modifies Git
configuration, installs hooks or executes downloaded code. Initialization creates
specification scaffolding rather than application behavior. Users may explicitly
integrate checks into their hooks or CI.

The CLI is strongly recommended and optional in the selected specification system.
Its structural and inventory checks assist specification reading; they do not
establish semantic consistency, workflow compliance or implementation conformance.
Automatic update planning, workflow management, remote release publication and
migrations are outside the supported command set.
