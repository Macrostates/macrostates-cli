# Workflow execution

Workflow execution describes how an implementer acts once a definer has made a
request.

The workflow type determines what the implementer may change, what must be
checked first, when workflow records are needed, and when the definer must be
asked before proceeding.

## Quick reference

This checklist summarizes the execution rules for fast orientation. The detailed
sections below define how to apply them.

Before changing files:

- Read the project-local specification entrypoint.
- Check `implementation/workflows/` for open workflow records.
- Decide whether the request starts, continues, switches, closes, or only
  reviews a workflow.
- Create or update the workflow record before editing files.
- Stop and ask the definer when conflicts or material ambiguities cannot be
  resolved by the applicable authority rules.

## Responsibility

The implementer is responsible for maintaining workflow records and for keeping
work inside the process. The definer has authority over intent and direction,
but the implementer must find a process-valid way to reflect that intent before
changing files.

Any project file change requires an open workflow record. Read-only inspection,
analysis, or explanation may happen without a workflow record, but creating,
editing, moving, renaming, deleting, or generating any file in the project must
first be covered by an open workflow record.

The implementer should pay attention to how familiar the definer appears to be
with the process. If the definer repeatedly asks why a process step is needed,
seems lost about workflow state, asks why a requested action is not allowed,
opens many exception workflows, or otherwise appears blocked by the method
itself, the implementer should briefly explain the relevant part of the process
in friendly, human-understandable language.

This explanation should be focused on the current situation. It should usually
include:

- What workflow or phase the project is currently in.
- Why the process requires the next step.
- What a normal workflow would look like from here.
- What the definer is expected to decide, confirm, or review.
- An offer to explain the relevant process rule in more detail.

The implementer should keep this support concise and practical. The goal is to
help the definer participate comfortably, not to recite the full process.

## General flow

### Before acting

Before touching files, the implementer should establish the current work
context:

- Read the project-local specification entrypoint.
- Read relevant package entrypoints and specifications.
- Check for open workflow records.
- Identify whether the request starts, continues, interrupts, closes, or reviews
  a workflow.
- Identify which files the workflow allows the implementer to edit.
- Identify whether any affected files belong to a subproject.
- Identify any ambiguity, conflict, open blocker, or risky overlap with existing
  work.
- Notice whether the definer appears to need a short explanation of the process
  as it applies to the current request.

If the definer asks for work in a way that skips, ignores, or conflicts with the
process, the implementer must still follow the process. When no ordinary
workflow type can honestly contain the request, use an `Exception` workflow
record and read `annex_exceptions.md`.

### Subprojects

When requested work affects a subproject, the implementer should identify both
the parent-project context and the subproject context before changing files.

The parent-project context determines which parent workflow record covers the
file change and how the subproject change affects the parent project.

The subproject context determines which local rules, specifications, lifecycle,
or maintenance expectations apply inside the subproject itself.

When the work only uses a subproject from the parent project, do not read the
subproject's internal specifications by default. Read its public usage material
when helpful, such as `README.md`, examples, or generated API documentation.

Read the subproject's internal specifications, workflow records, or lifecycle
artifacts when changing files inside the subproject, when diagnosing a
subproject lifecycle problem, or when the requested parent-project work depends
on those internal rules.

If the subproject has local specifications or lifecycle rules, follow them for
subproject-internal work unless they conflict with a higher-authority
instruction. If the subproject uses a different process from the parent, respect
that process from the subproject perspective while also maintaining the parent
project workflow required for repository changes.

If the subproject has no local specifications or lifecycle rules, do not assume
it is free of process. The parent project's process still applies to changes
inside the parent repository. Use the active parent workflow, or create one if
needed, before editing subproject files.

If the subproject and parent project give conflicting instructions, summarize
the conflict to the definer and ask how to proceed before touching affected
files unless the applicable authority rules clearly resolve it.

When the parent project is in `specification`, subproject work may still proceed
as a bounded activity if the definer requests it and the parent workflow records
make that scope explicit. This does not bootstrap the parent project unless the
definer explicitly starts parent project bootstrapping.

### Specification package scope and synchronization

A request to update specification packages applies only to the project context
of the request. In the root project, edit only its selected package instances;
in a subproject or vendored project, edit only that project's selected instances.
Determine context from the definer's request and the project being worked on.
If the target context is genuinely unclear, clarify it before editing packages.
Only an explicit request identifying additional contexts expands this scope.

Identical package names, identical files, a shared upstream repository, or a
shared Git subtree source do not authorize changing other copies. Git subtree
copies are independent. Do not propagate edits by copying files, rewriting other
compositions, or updating root/vendor packages in parallel merely to keep them
aligned. Parent workflow tracking does not expand the authorized edit scope.

After committing specification package changes, inspect whether other root,
subproject, or vendor contexts could consume those changes. Compare their
composition selections, source repositories, revision pins, dependency constraints,
and relevant local changes. This is a read-only compatibility check, not permission
to synchronize. Do not publish changes without authorization; if the changes have
not been published, distinguish a local candidate from an upstream update that
can already be pulled.

When an update is available, suggest a specific pull to the definer. Identify the
destination project and package, current and proposed versions or revisions,
source, compatibility implications, and any local changes or missing subtree
history that would require reconciliation. If no applicable update is found,
report that briefly. Never perform the pull until the definer explicitly approves
that destination and update. An already explicit approval remains valid; do not
request it again. Approval to edit, commit, or push the source package alone is
not approval to update another context.

After an approved pull, follow the destination project's workflow and Git rules,
validate the imported package and dependencies, and update its composition and
entrypoint to match the actual imported files. Do not advertise a new selected
version or installed revision before importing it successfully. Record pending
update suggestions in workflow documentation, not as already-installed versions
in the destination composition. Keep workflows open until closure is confirmed.

### Determining project stage

The implementer should identify the current development stage before choosing a
workflow.

Signals may include:

- The project phase recorded in `implementation/main.md`.
- Whether project-local specification files exist.
- Whether package metadata and package composition exist.
- Whether implementation documentation exists.
- Whether source code, tests, generated artifacts, or release artifacts exist.
- Whether workflow records exist.
- Whether existing files appear copied, bootstrapped, partially implemented, or
  actively maintained.

When the stage is unclear and affects what should happen next, summarize the
observed state and ask the definer to confirm the intended starting point.

Before changing project phase, warn the definer that the phase will change and
ask for confirmation.

If the phase signals are inconsistent, treat the project as `conflicting` until
the state is clarified. Read `annex_project-state.md` before repairing the
project state.

The implementer should check for at least these consistency problems:

- `implementation/main.md` is missing, but workflow records exist.
- `implementation/main.md` is missing, but source code, tests, generated
  artifacts, release artifacts, or other implementation files exist.
- `implementation/main.md` records a phase that contradicts the visible project
  contents.
- Workflow records imply an open or past implementation effort, but
  implementation documentation is absent or clearly stale.
- The project appears copied or migrated, but the workflow records, package
  composition, or implementation documentation still describe another project.

### No workflow records exist

If no workflow records exist, do not assume the current project state is already
valid.

The implementer should assess whether the project appears new, copied from
another project, migrated, partially bootstrapped, or developed before workflow
records were introduced.

Before changing files, the implementer should check whether:

- The project-local specification entrypoint exists.
- The package composition exists and is internally consistent.
- Referenced specification packages exist.
- Project-specific specifications appear intentional for this project.
- Existing implementation files suggest prior work not represented by workflow
  records.

When this assessment affects the workflow choice, ask the definer to confirm the
intended state before proceeding.

If `implementation/main.md` does not exist, no workflow records exist, and no
implementation appears to exist, assume the project is in the `specification`
phase. After creating the first workflow record, create `implementation/main.md`
and record at least the current project phase and the absence of an
implementation baseline.

If no workflow records exist but implementation appears to exist, or if
workflow records exist but `implementation/main.md` is missing, the project
state needs recovery. Read `annex_project-state.md`.

### Existing open workflow records

If open workflow records exist, the implementer must summarize them to the
definer before starting new work.

The summary should identify:

- The active workflow type and request.
- The change depth.
- What was done.
- What remains.
- Any blockers, conflicts, or unresolved questions.
- Whether the definer's new request appears to continue, interrupt, or conflict
  with the open workflow.
- The recommended next step.

If the request conflicts with an open workflow or with the applicable
specifications, read `annex_conflicts.md` and ask the definer how to proceed
before touching affected files.

When the project phase is `specification`, multiple open `Initial
specification` workflows may coexist. `Project scaffolding` workflows may also
coexist with specification work when setup is useful before the specification
baseline is complete.

When the project phase is `active`, do not open `Initial specification`,
`Project scaffolding`, or `Project bootstrapping` workflows.

### Starting a workflow

When starting a workflow record, capture enough context to resume later:

- Workflow type.
- Project phase.
- Status.
- Change depth.
- Definer identity.
- Original request.
- Planned scope.
- Initial known risks, conflicts, blockers, or open questions.
- Suggested next step.

Identify the definer as specifically as practical. Prefer repository-local
identity information when available. If identity cannot be determined
confidently, ask the definer how they should be recorded before creating the
workflow record. Use the `Requested by` format defined for workflow records.

Choose the smallest workflow scope that honestly contains the request.

When the scope is unclear, start with the narrower interpretation and ask the
definer before expanding it.

If the definer asks for a small, specific change, the implementer should usually
start with a specific workflow record. If shortly afterward the definer asks for
another small, related change in the same area, the implementer should suggest
a broader tuning workflow when doing so better represents the emerging work.
Obtain explicit definer confirmation before superseding the narrower workflow.

Do not broaden a workflow merely to hide unrelated work. A different change
depth, substantially different area, or changed impact profile is a signal to
apply the scope check below and open separate tracking for a distinct objective.

### Scope check for every request

Before assigning each new request to a workflow, compare its objective and
acceptance criteria with the workflow's original objective and recorded scope.
Continue that workflow only when the request corrects, completes, or validates
that same outcome. Sharing a screen, file, subsystem, conversational thread, or
originating change is not sufficient to establish a shared objective.

When the request introduces a distinct outcome, explain the boundary and open a
separate, appropriately named workflow before changing files. The definer's
instruction to perform that new work authorizes creating its tracking record;
do not require a second permission solely to open the record. Link the related
workflows and record the scope decision without rewriting their original intent
or moving historical work merely to make the scope appear consistent.

For example, replacing text actions with conventional icons and correcting an
icon's placement can share an objective. Changing device-rotation behavior or
making the entire application fullscreen introduces separate acceptance criteria
and should receive separate tracking, even if first noticed during icon review.

An open workflow awaiting acceptance is not a default destination for new work.
Record its delivery state as `awaiting_acceptance` once requested work and
applicable checks are finished; identify remaining device checks or review
explicitly. Corrections within its original scope may resume `implementing`.
A new objective belongs in its own workflow while the earlier one remains open.

Creating the new record does not close, abandon, pause or supersede the earlier
workflow, or authorize additional product scope. Existing conflict, phase-change,
and explicit closure/supersession confirmation rules still apply. Ask only for
an unresolved scope or conflict decision, not for permission already supplied by
the request. Record both the continuing review obligations and the new work.

### Continuing a workflow

When continuing an existing workflow, read its workflow record before acting.

Use the record to identify:

- What the definer requested.
- What has already been done.
- What remains.
- Which files or areas are affected.
- Whether the current request changes the workflow scope.

Update the workflow record when meaningful progress is made, when remaining work
changes, or when a blocker or conflict is discovered.

### Switching workflows

Before switching from one open workflow to another, compare the planned action
with all open workflow records.

Warn the definer when switching may lose context, mix unrelated changes, obscure
review, or leave large or systemic work in an unclear state.

If the switch affects files, assumptions, or decisions owned by another open
workflow, ask the definer whether to pause, close, abandon, or supersede that
workflow before proceeding.

When a new authorized request has a distinct objective and should happen before
the current workflow is finished, open a separate workflow under the scope-check
rules above. Explain any impact on unfinished work. On returning to an earlier
workflow, summarize the separate workflow's delivery and review state. Keep it
open unless the definer explicitly confirms closure.

When several small adjacent requests reveal that a narrow workflow has become a
broader tuning session, the implementer may propose superseding the narrow
workflow with a broader one. Keep the narrow workflow open until the definer
explicitly confirms supersession. After confirmation, the superseding workflow
should summarize the inherited work, and the superseded workflow should record
the confirmation, receive status `superseded`, and move to history.

### Closing a workflow

The implementer must never close an open workflow on its own. Every transition
to `completed`, `abandoned`, or `superseded` requires explicit definer
confirmation identifying the workflow or clearly identified set of workflows.
This applies even when the implementer opened the workflow during the current
turn and believes it has finished all requested work.

When the implementer considers the work done:

1. Verify that the requested work is done, relevant checks were run or consciously
   skipped, required artifacts were updated, and remaining gaps are documented.
2. Summarize the result and suggest closure to the definer.
3. Keep the workflow open, normally `in_progress`, with review and closure
   confirmation recorded as remaining work. Allow the definer to request related
   changes before deciding to close it.
4. Only after explicit confirmation, record the definer's decision, assign the
   appropriate closed status, and move the record to workflow history.

A request to perform work, successful checks, a positive reaction to the result,
silence, or a change of topic does not authorize closure. Acceptance of a result
or an implementation baseline is distinct from confirmation to close a workflow.
If the definer already explicitly requested closure of the identified workflow,
that request is confirmation; do not ask for it again. Still verify the closing
condition and do not mark unfinished work completed.

Abandonment and supersession require the same confirmation. Record why the
workflow is no longer the active path as well as the definer's decision. Other
workflow-specific completion checks remain applicable and do not replace this
closure confirmation.

## Workflow-specific execution

### Initial specification

Use this workflow when defining intended behavior before a full implementation
exists.

Before editing specifications, confirm that specification work is the explicit
request. Keep changes focused on intended behavior and avoid implementing
behavior unless the definer changes the task.

If no implementation baseline exists and the definer is still shaping the
intended behavior or process baseline, use this workflow even when editing
existing specification files.

During the `specification` phase, separate initial specification workflows may
be opened for distinct areas of the intended baseline.

If the request shifts toward repository initialization, tooling configuration,
or project structure setup, use `Project scaffolding`.

### Project scaffolding

Use this workflow during the `specification` phase when preparing repository or
tooling artifacts before the specification baseline is complete.

Before scaffolding, identify which selected specification packages authorize or
motivate the setup. Keep the project phase as `specification` unless the
definer explicitly starts project bootstrapping.

Allowed scaffolding may include:

- Git or repository initialization.
- Minimal repository-root operational Markdown files such as `README.md` or
  `AGENTS.md`.
- `.gitignore`, temporary directory placeholders, and other repository hygiene
  files.
- Empty conventional directories or placeholder files needed to preserve
  intended layout.
- Tool configuration files for already selected tools.
- Lockfiles or generated tool metadata only when the selected package rules
  require or clearly allow them.

Project scaffolding must not implement domain behavior, create application
logic, or treat generated structure as an accepted implementation baseline.

Ask the definer before adding dependencies, selecting among materially different
tooling options, creating non-obvious architecture, or expanding the scaffold
into product implementation.

Update implementation documentation to make clear that scaffolding exists but no
implementation baseline has been accepted.

### Project bootstrapping

Use this workflow when implementing an existing specification set for the first
time.

Before bootstrapping, confirm that the selected specification packages and
project-specific specifications are the intended starting point. Check whether
existing files indicate prior implementation work that should be preserved,
explained, or reconciled.

Before starting bootstrapping, warn the definer that the project phase will
change from `specification` to `bootstrapping` and ask for confirmation.

After bootstrapping begins, keep the project phase as `bootstrapping` across
prompts and workflow steps. Do not change the project phase to `active` merely
because the first bootstrapping prompt has completed.

Change the project phase to `active` only when the definer accepts the first
implementation baseline as good enough.

If the definer decides during bootstrapping that the specification baseline has
substantial gaps or problems, the project may return to `specification`. In that
case, preserve workflow records, remove or unwind the partial implementation as
directed, update implementation documentation, and record the phase change.

### Implementation amendment

Use this workflow when amending current implementation, usually while preserving
intended behavior. Amendment work may reveal that the specifications need to
change, as described in `001_concepts.md`.

Before changing files, read the relevant specifications and current
implementation documentation. If the requested amendment would change intended
behavior, ask whether the workflow should become a specification update.

Before closing the amendment, summarize the implementation changes and ask the
definer whether a specification update should reflect them and to what extent.
Wait for and record the definer's decision before closing. If requested, open
or continue an explicit specification update workflow for the agreed scope.
Document any remaining mismatch between implementation and specifications;
closing the amendment does not make that mismatch compliant.

### Specification update

Use this workflow when adding to or revising specifications, whether to define
more requirements or functionality, change intended behavior, or reflect
definer-approved changes already made during an implementation amendment.

Use this workflow after an accepted specification baseline exists, especially
after implementation exists or implementation work has begun. Before editing
specifications, confirm the change is deliberate specification work. Determine
whether the update creates an implementation gap and make any gap visible.
When the implementation already satisfies the updated specifications, such as
after an implementation amendment, record that no gap was created and no
implementation update is needed.

After closing the specification update, consider whether a `Review or gap
assessment` workflow would help evaluate the need for an implementation update.
If so, recommend it to the definer and briefly explain what it would resolve.
Do not recommend it routinely when there is no implementation to assess, when
alignment is already verified, or when the need and scope of an implementation
update are already clear.

### Implementation update

Use this workflow when bringing implementation back into alignment after a
specification update that creates a misalignment between implementation and
specifications.

Before changing implementation, identify which specifications changed, what
current behavior no longer matches, and which implementation artifacts need to
be updated.

### Review or gap assessment

Use this workflow when comparing intended behavior, current behavior, and
supporting artifacts.

Do not touch files unless the definer explicitly asks for edits and an open
workflow record covers those edits. Report findings, risks, and suggested next
steps clearly.

### Documentation refresh

Use this workflow when updating non-authoritative documentation after behavior,
commands, generated references, or repository usage have changed.

Follow the specification package that owns the documentation type. Do not create
or reorganize documentation files unless the definer asks or the owning package
allows it.

### Exception

Use this workflow when the definer explicitly asks for something that skips,
ignores, or contradicts the process and no ordinary workflow type can honestly
contain the work.

Also use this workflow to recover from a `conflicting` project phase.

Read `annex_exceptions.md` before executing an exception workflow.

## Cross-cutting rules

### Ambiguity and conflicts

When ambiguity, authority conflict, or workflow conflict is found, read
`annex_conflicts.md`.

### Completion checks

Completion checks should match the workflow type, risk, and surface area. They
answer whether the current workflow step is coherent enough to report as done.

For `Initial specification` and `Specification update`, check that the edited
specifications are internally consistent, preserve package independence, follow
the package reading order, update package versions when needed, and make any
known implementation gap visible.

For `Project scaffolding`, check that the project phase remains
`specification`, the created files are limited to repository/tooling setup, no
domain behavior or application logic was implemented, required definer
confirmations were obtained, and implementation documentation still makes clear
that no implementation baseline has been accepted.

For `Project bootstrapping`, check that implemented behavior matches the
selected specifications, required implementation documents and decision records
exist, relevant tests or manual checks were run, and any unresolved
specification gap is reported to the definer.

For `Implementation amendment` and `Implementation update`, check that the
implementation still matches the applicable specifications, relevant tests or
manual checks were run, implementation documents or decision records were
updated when needed, and no specification was changed without an explicit
specification workflow.

For `Review or gap assessment`, check that the reviewed scope is clear, findings
separate facts from recommendations, and any suggested file change is left for a
future workflow unless the definer requested edits.

For `Documentation refresh`, check that the owning specification package allows
the documentation update, any generated documentation was refreshed through its
required source or build step, and non-authoritative documentation does not
override specifications or implementation truth.

For `Exception`, check that the exception record explains why ordinary workflow
handling was not enough, what safeguards were preserved, what risk remains, and
what condition will return the project to normal workflow handling.

If a relevant check cannot be run or completed, say what was not checked and
why.

### Final response

At the end of a workflow step, the implementer should report:

- What changed.
- What was checked.
- What remains.
- Any workflow record, implementation document, decision record, or
  non-authoritative documentation update that was made.
- Any ambiguity, conflict, blocker, or gap the definer should know about.
