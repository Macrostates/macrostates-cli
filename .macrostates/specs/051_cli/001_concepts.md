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

Installation and canonical locking contact package sources. Explicit branch
synchronization may fetch a configured Git remote when requested. Initialization,
inspection, lint, integrity verification, planning and local readiness checks
operate offline against available files and Git refs.
Read-only operations preserve project files; staged checks may create temporary
snapshots without changing the checkout or index.

Git synchronization performs the explicitly selected merge or rebase on the
attached development branch, which may update the worktree/index and create or
rewrite development commits through Git. It must preserve unresolved conflicts
for the implementer and refuse unsafe starting states. Other operations do not
stage or commit changes. No command creates or switches branches, pushes,
force-pushes, creates release tags, publishes applications, changes Git
configuration, installs hooks, or executes downloaded package code.
Initialization creates specification scaffolding rather than application
behavior. Users may explicitly integrate checks into their hooks or CI.

The CLI is strongly recommended and optional in the selected specification system.
Its structural, inventory, documentary workflow and release checks assist
specification reading. They do not prove semantic consistency, truthful approval,
or complete implementation conformance. The implementer declares semantic impact
and reviews evidence under the selected specifications. Workflows require
explicit definer-authorized closure; the CLI can list required closure requests
and check recorded status, but never closes or approves workflows automatically.

Process 5 and 6 operations distinguish pending work, reviewed baseline finalization,
and separately versioned deliverables. Application policies are optional; the
default stable application version is the selected finalized implementation's
numeric part. Project-local policies can explicitly override it. Core operations
use Git refs and identities without a hosting-platform account. Remote reviews,
required external checks, application version assignment under independent
policies, dependency selection, tagging and publication remain project operations.

## Public document authoring

This project's selected Process policy requires anonymous, self-contained
documents from their first draft. Follow its
[document contract](../001_process/004_documents.md) for specifications, workflow
records, reports, temporary evidence and archived deliverables. Attribute work
by role and express neutral technical objectives. Preserve required public
licenses, dependency identities and immutable technical provenance.

CLI diagnostics and operation results are technical data, not automatically
anonymous documents. Before retaining them as evidence, the implementer selects
necessary result fields, reviews names/keys/values and embedded content in memory,
and writes only the reviewed representation. Never save raw output as a private
intermediate copy. Do not imply that existing structural checks establish
anonymity, truthful consent or semantic conformance.
