# Concepts

## Specifications and implementation

Specifications describe intended behavior. Implementation documentation
describes current behavior. Decision records explain meaningful choices where
the specifications intentionally leave room.

A good specification is like a macrostate: it defines the properties that must
be true while leaving room for many acceptable microstates. An implementation is
one concrete microstate compatible with that specification.

Specifications should define everything the definer cares about: externally
observable behavior, compatibility, safety, ownership, and important operating
constraints. They should avoid prescribing private implementation details when
multiple implementations could satisfy the same intent.

## Roles

A **definer** owns intended behavior: requirements, product intent, authority
decisions, and specification changes.

An **implementer** realizes intended behavior: code, tests, implementation
documentation, decision records, and updates to non-authoritative documentation.

In normal use, the definer is a human and the implementer is an agent. The roles
are not tied to identity: a definer may be another agent, and an implementer may
be a human when explicitly acting in that role.

## Authority

When a reusable process rule conflicts with a project-local specification
entrypoint, the project-local authority order decides the conflict.

## Project phase

Project phase describes the broad development stage. It helps the implementer
choose the right workflow.

Use these phases:

- `specification`: the intended behavior or process baseline is still being
  defined, and no accepted implementation baseline exists.
- `bootstrapping`: an accepted specification baseline exists, and the first
  implementation baseline is being created.
- `active`: an implementation baseline exists, and ongoing work changes,
  extends, reviews, or realigns the project.
- `conflicting`: the project's artifacts disagree about its phase, history, or
  implementation state, so the implementer cannot safely treat the project as
  being in one of the normal phases without definer clarification.

The normal phase progression is `specification` to `bootstrapping` to `active`.
Once a project is active, multiple workflows may happen over time and may
occasionally overlap.

`conflicting` is not a normal development destination. It is a temporary
recovery state used when project files imply incompatible histories or phases.
The implementer should move a project out of `conflicting` only after the
definer and implementer agree on the intended state and the required recovery
work has been recorded.

During `specification`, multiple `Initial specification` workflows may be open
at the same time when different parts of the intended baseline are being shaped.
`Project scaffolding` workflows may also be open during `specification` when
repository or tooling setup is useful before the specification baseline is
complete.

During `active`, `Initial specification`, `Project scaffolding`, and `Project
bootstrapping` workflows should not be opened. Use the other workflow types for
ongoing changes, reviews, documentation refreshes, and realignment work.

Phase changes are deliberate. The implementer must warn the definer before a
workflow changes the project phase and must confirm that the definer wants to
proceed.

## Subprojects

A subproject is a bounded project-like unit that lives inside a parent project.

Subprojects may exist for many reasons: vendored libraries, generated
components, independently maintained modules, examples, tools, documentation
sites, infrastructure areas, or other parts of a repository whose lifecycle is
partly separate from the parent project.

A subproject may follow this specification-driven process, a different process,
or no explicit local process at all. It may have its own specifications,
implementation documentation, workflow records, or none of those artifacts.

When a subproject has its own rules, specifications, lifecycle, or maintenance
metadata, those local rules should be respected for subproject-internal work.
The parent project's specifications and process still govern how the subproject
is integrated, tracked, and changed within the parent repository.

The implementer does not need to read a subproject's internal specifications
merely because the parent project uses that subproject. When the requested work
only consumes the subproject through its public interface, use the subproject as
a dependency or component. Read public usage material such as its `README.md`,
examples, or API documentation when needed, but read internal specifications
only when changing files inside the subproject or when the requested work
depends on the subproject's own lifecycle rules.

Changing files inside a subproject is still changing files in the parent
project. Therefore, the parent project must still have an open workflow record
that covers the work unless another higher-authority specification explicitly
defines a different parent-level tracking mechanism.

Subprojects may sometimes be worked on while the parent project is in a
different phase. For example, a subproject may be specified or implemented while
the parent project is still in its own initial specification phase. In that
case, the implementer should follow the subproject's local lifecycle when one
exists, while also maintaining the parent project's workflow record and
integration state.

## Workflow types

Specification-driven development uses several workflows. Each workflow has
different permissions, expected outputs, and reasons to ask for definer input.

### Initial specification

Initial specification defines the desired system before a full implementation
exists.

Use this workflow while the project phase is `specification`. If no
implementation baseline exists and the definer is still shaping the intended
behavior or process baseline, use `Initial specification` even when editing
existing specification files.

Multiple initial specification workflows may be open at the same time while the
project phase is `specification`.

The definer owns intent, scope, priorities, and requirement choices. The
implementer may help draft, organize, and edit specification files because
specification work is the explicit task.

The implementer should keep changes focused on specifications and should not
implement behavior unless the definer explicitly changes the task.

If the work shifts from shaping specifications to preparing repository files,
tooling, or empty project structure, use `Project scaffolding` rather than
stretching an initial specification workflow.

Ask the definer when a requirement choice materially affects product behavior,
compatibility, safety, operations, or future implementation cost.

### Project scaffolding

Project scaffolding prepares the repository or development tooling while the
project remains in the `specification` phase.

Use this workflow when the definer wants useful setup before the specification
baseline is complete. Examples include initializing Git, updating
repository-root operational Markdown files such as `README.md` or `AGENTS.md`,
creating `.gitignore`, creating reserved directories, adding placeholder files
needed to keep directories tracked, or creating tool configuration files already
required by selected specification packages.

Project scaffolding does not change the project phase to `bootstrapping` and
does not create an accepted implementation baseline. It is a preparation
workflow, not the first implementation of product behavior.

The implementer may create or update repository and tooling artifacts needed for
future bootstrapping, but must keep the scope bounded. Do not implement domain
behavior, create application logic, or make irreversible architecture choices
unless the applicable specifications already require them or the definer
explicitly confirms them.

If scaffolding requires adding dependencies, choosing between materially
different tools, or creating files whose meaning is not settled by the
specifications, ask the definer before proceeding.

### Project bootstrapping

Project bootstrapping is the first comprehensive implementation of an existing
specification set.

Starting project bootstrapping changes the project phase from `specification` to
`bootstrapping`. The implementer must warn the definer about this phase change
and confirm before proceeding.

The implementer should read broadly enough to understand the full specification
composition, then implement autonomously in coherent steps. The implementer
should create or update code, tests, implementation documentation, decision
records, and non-authoritative documentation as needed by the applicable rules.

The implementer must not edit specifications during bootstrapping unless the
definer explicitly asks for specification work.

Ask the definer when specifications are contradictory, when authority rules do
not resolve a conflict, or when an ambiguity materially changes required
behavior.

Bootstrapping may include varied specification and implementation changes while
the first implementation baseline is being formed. The project remains in
`bootstrapping` until the definer accepts the first implementation baseline as
good enough. Only then should the implementer change the project phase to
`active`.

If bootstrapping reveals that the initial specification has substantial gaps or
problems, the definer may ask to revert the project to `specification`. In that
case, the implementer should remove or unwind the partial implementation as
directed, preserve workflow records, and change the project phase back to
`specification`.

### Implementation amendment

An implementation amendment changes the current implementation. It usually
preserves intended behavior, as with bug fixes, refactors, missing behavior,
test improvements, and cleanup. It may also reveal that the specifications need
to change: the definer may recognize that the implementation needed amendment
because the specified behavior was incomplete or should have been different.

The implementer should read the relevant specifications and current
implementation documentation, make the smallest coherent change, test it, and
update implementation documentation or decision records when needed.

The implementer must not edit specifications unless the definer explicitly asks
for a specification change.

Ask the definer when the requested amendment appears to conflict with the
specifications or would require changing intended behavior.

Before closing an implementation amendment, the implementer must ask the
definer whether a specification update should reflect the implementation
changes and, if so, to what extent. Record the definer's decision in the
workflow record and open or continue an explicit specification update workflow
if requested. Reflect the agreed intended behavior and constraints, without
unnecessarily prescribing private implementation details.

### Specification update

A specification update adds to or revises specifications after an accepted
specification baseline exists. It may define additional requirements or
functionality, change intended behavior, or reflect definer-approved changes
already made during an implementation amendment.

The definer owns the desired change. The implementer may help inspect current
specifications, identify affected areas, and edit specification files because
specification work is the explicit task.

The implementer should not implement the changed behavior unless the definer
explicitly asks for implementation work. A specification update may
intentionally create an implementation gap, but need not do so. When it reflects
an implementation amendment that already satisfies the updated specifications,
it creates no gap and requires no implementation update.

After closing a specification update, the implementer should recommend a
`Review or gap assessment` workflow to the definer when it would help determine
whether an implementation update is needed. Make this recommendation only when
the assessment would be useful, such as when the effect on existing
implementation is unclear.

Ask the definer when the update conflicts with existing specifications and
authority rules do not resolve the conflict.

### Implementation update

An implementation update brings the system back into alignment after a
specification update that creates a misalignment between the implementation and
the specifications.

The implementer should read the changed specifications and affected
implementation documentation, then update code, tests, implementation
documentation, decision records, and non-authoritative documentation as needed.

The implementer must not edit specifications during implementation update unless
the definer explicitly asks for specification work.

Ask the definer when implementation reveals a new ambiguity or conflict in the
specifications that materially affects behavior.

### Review or gap assessment

A review or gap assessment compares specifications, implementation
documentation, code, tests, and other relevant artifacts.

The implementer should report findings such as implemented behavior, missing
behavior, conflicts, ambiguities, obsolete documentation, missing tests, and
residual risk.

The implementer should not touch files unless the definer explicitly asks for
edits.

Ask the definer before expanding the review scope beyond the requested area when
doing so would materially increase time, cost, or noise.

### Documentation refresh

A documentation refresh updates non-authoritative documentation after behavior,
commands, generated references, or repository usage have changed.

The implementer should follow the rules of the specification package that owns
that documentation type. Some documentation can be edited directly; other
documentation may require changing an authoritative source and regenerating
derived files.

The implementer must not change specifications or implementation merely to match
non-authoritative documentation.

Ask the definer before creating new documentation files, splitting existing
documentation, or changing documentation ownership conventions.

### Exception

An exception workflow records work that must proceed even though the request
does not fit the normal process cleanly.

Use an exception workflow only when the definer explicitly asks for something
that skips, ignores, or contradicts the process and no ordinary workflow type can
honestly contain the work.

Also use an exception workflow when project state recovery is needed before
ordinary work can safely continue.

Read `annex_exceptions.md` before executing an exception workflow.
