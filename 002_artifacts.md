# Work artifacts

Work artifacts are the files used to define, implement, explain, and resume
specification-driven work.

## Specification documents

`specs/` contains specification packages as defined by the meta package.
Specification documents describe intended behavior and are definer-owned.

Implementers must not edit specifications unless the definer deliberately asks
for specification work. Routine implementation, testing, cleanup, documentation,
or wrap-up work must not change specifications by default.

Do not edit specifications merely to make incomplete implementation appear
compliant. When the desired behavior changes, update the relevant specification
only as an explicit specification change.

## Implementation documents

`implementation/` contains implementation documents. Implementation documents
describe what the system currently is and are implementer-owned.

Implementers should maintain implementation documentation alongside code and
keep it honest about partial support, known gaps, and important operational
details.

Definers should not normally alter implementation documentation directly. In the
exceptional case where a definer changes implementation without another
implementer, that definer is acting as the implementer and should update
implementation documentation according to the same rules.

Implementation documentation may describe code structure, runtime behavior,
manual verification steps, local limitations, and current deviations from the
specifications.

The main implementation entrypoint should be:

```text
implementation/
  main.md
```

`implementation/main.md` should summarize the current implementation. It should
include:

- Project phase.
- Current implementation summary.
- Implemented capabilities.
- Known gaps.
- Important files or modules.
- Verification guidance.
- Links to topic documents and decision records.

Additional implementation documents may be created when a topic is substantial
enough to deserve its own file. For example, a project that serves an API and
also runs a background data process may document those areas separately.

Topic implementation documents should usually include:

- Current behavior.
- Important files or modules.
- Verification guidance.
- Known gaps.
- Related decisions.

## Subproject artifacts

Subprojects may have their own artifacts, but this process does not require all
subprojects to use the same artifact structure as the parent project.

A subproject may have local `specs/`, `implementation/`, workflow records,
decision records, metadata, generated documentation, or a different lifecycle
defined by another tool or project convention. A subproject may also have no
local specifications or lifecycle artifacts at all.

When subproject artifacts exist, the implementer should inspect and respect
them before changing subproject-internal files. When they do not exist, the
implementer should not invent a full subproject process unless the definer asks
for it or the parent specifications require it.

Parent project workflow records still apply to repository file changes inside
subprojects. If a subproject also has its own workflow or lifecycle records, the
implementer should keep the parent and subproject records coherent enough that
work can be resumed from either context.

## Decision records

`implementation/decisions/` contains ADRs for meaningful implementation choices
not settled by the specifications. ADRs are part of implementation
documentation and follow the same ownership rules.

Decision records should be specific enough that a later maintainer can
understand why the choice was made and what would justify changing it.

An ADR should include:

- Context.
- Decision.
- Consequences.
- Status.

Optional sections may include considered alternatives, follow-up work, and links
to related specifications or implementation notes.

Decision record filenames should use this format:

```text
implementation/
  decisions/
    0001-short-descriptive-name.md
```

Use monotonically increasing zero-padded numbers. Do not renumber existing
decision records.

Use lowercase descriptive words separated by hyphens after the number.

Decision record statuses should be explicit. Common statuses are:

- `proposed`
- `accepted`
- `superseded`
- `deprecated`

Prefer superseding an old decision over rewriting its history.

## Workflow records

Workflow records track active and completed specification-driven workflows so
work can resume coherently across sessions and branches.

Workflow records are implementation documentation. They are implementer-owned and
must not override specifications, code, tests, or the project-local
specification entrypoint.

Any project file change requires an open workflow record. Read-only inspection,
analysis, or explanation may happen without a workflow record, but creating,
editing, moving, renaming, deleting, or generating any file in the project must
first be covered by an open workflow record.

Workflow records live under:

```text
implementation/
  workflows/
    <open-workflow>.md
    history/
      <closed-workflow>.md
```

Open workflows live directly in `./implementation/workflows/`.

Closed workflows live in `./implementation/workflows/history/`.

The `history/` directory may usually be ignored during session startup unless
the definer asks for historical context or an open workflow references a closed
workflow.

Each workflow entry has its own Markdown file. Workflow filenames use this
format:

```text
<yyyy-mm-dd>-<short-descriptive-name>.md
```

The descriptive name must be lowercase words separated by hyphens. It should be
short enough to scan while still identifying the work.

Examples:

```text
2026-08-26-initial-specification.md
2026-08-27-storage-conflict-amendment.md
2026-08-28-api-doc-refresh.md
```

Each workflow entry should include:

- Project phase.
- Workflow type.
- Status.
- Change depth.
- Branch or worktree context when known.
- Requested by.
- Started at.
- Last updated at.
- Original request.
- Objective, scope and acceptance criteria.
- Delivery state.
- Work done.
- Files touched when useful.
- Remaining work.
- Blockers, conflicts, or unresolved questions.
- Suggested next step.

Use the smallest useful amount of detail. The entry should help resume work
without becoming a duplicate implementation log.

`Requested by` should identify the definer as specifically as practical. Prefer
this format:

```text
Name Lastname (email@example.com) - Obtained from <source>
```

A handle or stable local identifier may be used when name or email are
unavailable.

When the project uses Git, prefer repository-local Git identity information when
available. If repository-local Git identity is unavailable, the implementer may
use another confident source, such as explicitly provided definer identity or
global Git configuration. If the implementer cannot identify the definer
confidently, it should ask for a name, email, handle, or preferred identifier
before creating the workflow record.

`Started at` and `Last updated at` should include date and time to minute
precision using this format:

```text
YYYY-MM-DD HH:mm
```

Use these workflow statuses:

- `in_progress`
- `paused`
- `blocked`
- `completed`
- `abandoned`
- `superseded`

Open statuses are `in_progress`, `paused`, and `blocked`.

Closed statuses are `completed`, `abandoned`, and `superseded`. Assigning any
closed status requires explicit definer confirmation for the identified workflow.
Record that confirmation and its scope in the workflow before moving it to
history. An implementer's assessment that the work is done is not confirmation.

While awaiting confirmation, keep the workflow in its open location with an open
status, normally `in_progress`. Record that the requested work and checks are
finished, that definer review and closure confirmation remain, and any suggested
next step. Do not invent a closed or completed status to represent pending review.

Track delivery separately from workflow status using `Delivery state`:

- `implementing`: requested work or applicable implementation checks remain.
- `awaiting_acceptance`: requested work and applicable checks are finished;
  definer review, explicitly listed device acceptance checks or closure remain.
- `accepted`: the definer has accepted the result; closure still requires its
  own explicit confirmation unless already included in that instruction.

Use this field in new records and add it to existing records when resuming or
reviewing them. It supplements the established statuses; it does not introduce
a new closed status or imply acceptance from passing checks. Put delivery state
near status so an open record awaiting review is easy to distinguish from active
implementation. Record remaining acceptance checks and closure separately from
implementation tasks. An open record must not become a catch-all for new work;
apply [the per-request scope check](003_execution.md#scope-check-for-every-request).

Only workflows with open statuses should remain directly under
`./implementation/workflows/`. When a workflow receives a closed status, move
its file to `./implementation/workflows/history/`.

When a workflow is superseded by a broader workflow, the superseding workflow
should identify the superseded record and summarize the inherited work. The
superseded workflow should identify the superseding record, use status
`superseded`, and move to `./implementation/workflows/history/`.

Use these change depths:

- `small`: narrow, localized, and easy to validate.
- `medium`: touches several files, behaviors, or documentation areas, but has a
  bounded scope.
- `large`: introduces or changes a major feature, public behavior, architecture,
  persisted data, or several connected areas.
- `systemic`: affects project-wide structure, authority, compatibility,
  workflow, or assumptions used by many future changes.

When unsure, choose the deeper level until the work is better understood.

Change depth helps decide whether adjacent requests belong in the same
workflow. Several small related requests in the same area may be consolidated
into a broader tuning workflow. A request with a different depth, substantially
different area, or different impact profile should usually get a separate
workflow.

At the beginning of a work session, before touching files, the implementer must
check for open workflow entries in `./implementation/workflows/`.

If open workflows exist, the implementer must summarize them to the definer
before starting new work. The summary should identify:

- The active workflow type and request.
- The change depth.
- What was done.
- What remains.
- Any blockers, conflicts, or unresolved questions.
- Whether the definer's new request appears to continue, interrupt, or conflict
  with the open workflow.
- The recommended next step.

If the definer's new request conflicts with an open workflow, the implementer
should ask the definer whether to continue, pause, close, abandon, or supersede
the open workflow before touching affected files.

If an open workflow has `large` or `systemic` depth, the implementer should warn
more strongly before starting unrelated work. The warning should explain the
likely risk, such as losing context, mixing incompatible changes, leaving broad
work in an unclear state, or making future review harder.

When multiple workflows are open, each prompt should consider how the planned
actions affect all open workflows. If the planned action may conflict with,
obscure, or increase risk for any open workflow, the implementer must warn the
definer again before proceeding.

Implementers should update workflow records when starting, pausing, blocking,
completing, abandoning, or superseding a workflow.

Implementers should also update the relevant workflow entry when meaningful
progress is made, when remaining work changes, or when a conflict or blocker is
found.

Workflow records should not be updated so frequently that they obscure the useful
state of the work.

## Other documentation

Other specification packages may define other documentation types, such as
repository usage documentation, operations guides, reference material, or
generated API documentation.

This package does not grant permission to create or reorganize those documents.
Follow the specification package that owns the documentation type.

Other documentation must not be treated as specification documentation unless an
owning specification package explicitly grants that role. Do not change
implementation or specifications merely to match non-authoritative
documentation.

Code comments should explain local complexity or non-obvious constraints. They
should not be the only place broad product intent or externally observable
behavior is documented.
