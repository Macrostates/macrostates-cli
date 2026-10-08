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
- Discover and read applicable directory-scoped specifications before edits.
- Check `.macrostates/implementation/workflows/` for open workflow records.
- Decide whether the request starts, continues, switches, closes, or only
  reviews a workflow.
- Create or update the workflow record before editing files.
- Stop and ask the definer when conflicts or material ambiguities cannot be
  resolved by the applicable authority rules.

## Responsibility

The implementer is responsible for maintaining workflow records, following the
versioning rules, and keeping work inside the process. It must classify changes,
maintain declarations and check alignment without waiting for the definer to ask
for a version bump. The definer has authority over intent and direction,
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
- Discover directory-scoped specifications applicable to each target path.
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

### Directory-scoped specifications

Follow the selected Meta package's `002_project-composition.md`, section
`Directory-scoped specifications`, to discover applicable local
`.macrostates/specs/main.md` entrypoints along each target path, including
existing ancestors of new files. Read from outermost to innermost, follow each
entrypoint's reading order, and respect the enclosing composition's authority
placement and strict scope limits. Directory specifications are authoritative
even without package metadata or an independent lifecycle. They remain part of
the enclosing project's contract, phase, versioning and workflow context.

This discovery is needed for internal edits, including specification edits; it
does not require reading a component's internal specifications merely to consume
its public interface. A local specification set does not make the directory a
subproject. Identify separately composed or maintained units under
[Subprojects](001_concepts.md#subprojects) before choosing lifecycle or tracking
rules. Do not treat a separately composed subproject's
`.macrostates/specs/main.md` as an ordinary directory entrypoint in the parent's
composition.

### Subprojects

When requested work affects a subproject, the implementer should identify both
the parent-project context and the subproject context before changing files. Use
the identification rules in [Concepts](001_concepts.md#subprojects), not the
presence of a `.macrostates/specs/` directory alone. Ask only when an unresolved
boundary materially changes the applicable authority, lifecycle or maintenance
rules.

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
of the request. In the root project, target only its selected package instances;
in a subproject or vendored project, work only within that selected context.
For immutable archive packages, propose changes in the canonical source under
an explicit specification request and import a verified new release after
publication. Do not edit installed snapshots or rewrite locks to accept changes.
Project-owned local specifications remain directly editable.
Determine context from the definer's request and the project being worked on.
If the target context is genuinely unclear, clarify it before editing packages.
Only an explicit request identifying additional contexts expands this scope.

Identical package names, identical files, a shared upstream repository, or a
shared Git subtree source do not authorize changing other copies. Package copies are independent, whether archive snapshots or Git subtrees. Do not propagate edits by copying files, rewriting other
compositions, or updating root/vendor packages in parallel merely to keep them
aligned. Parent workflow tracking does not expand the authorized edit scope.

After committing specification package changes, inspect whether other root,
subproject, or vendor contexts could consume those changes. Compare their
composition selections, source repositories, revision pins, dependency constraints,
and relevant local changes. This is a read-only compatibility check, not permission
to synchronize. Do not publish changes without authorization; if the changes have
not been published, distinguish a local candidate from an upstream update that
can already be pulled.

When an update is available, suggest a specific update to the definer. Identify the
destination project and package, current and proposed versions or revisions,
source, compatibility implications, and local modifications, stale locks or
missing subtree history requiring reconciliation. Use the selected source
mechanism: verified archive installation or explicit Git-subtree maintenance. If no applicable update is found,
report that briefly. Never perform the update until the definer explicitly approves
that destination and update. An already explicit approval remains valid; do not
request it again. Approval to edit, commit, or push the source package alone is
not approval to update another context.

After an approved update, follow the destination project's workflow and Git rules,
validate the imported package and dependencies, and update its composition and
entrypoint to match the actual imported files. Do not advertise a new selected
version or installed revision before importing it successfully. Record pending
update suggestions in workflow documentation, not as already-installed versions
in the destination composition. Keep workflows open until closure is confirmed.

### Determining project stage

The implementer should identify the current development stage before choosing a
workflow.

Signals may include:

- The project phase recorded in `.macrostates/implementation/main.md`.
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

- `.macrostates/implementation/main.md` is missing, but workflow records exist.
- `.macrostates/implementation/main.md` is missing, but source code, tests, generated
  artifacts, release artifacts, or other implementation files exist.
- `.macrostates/implementation/main.md` records a phase that contradicts the visible project
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

If `.macrostates/implementation/main.md` does not exist, no workflow records
exist, and no implementation appears to exist, assume the project is in the
`specification` phase. After creating the first workflow record, create
`.macrostates/implementation/main.md` and record at least the current project
phase and the absence of an implementation baseline.

If no workflow records exist but implementation appears to exist, or if workflow
records exist but `.macrostates/implementation/main.md` is missing, the project
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

When starting a workflow record, capture enough context to resume later.

Allocate its filename using the UTC date and compact time-ID rules in
[Workflow records](002_artifacts.md#workflow-records), checking both open records
and `history/` before creating the file.

Record:

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
implementation update is needed. A specification update may leave an explicit
implementation gap in the working tree or a development branch; after an
implementation baseline exists, do not commit that gap to the primary branch.
See [Versioning and integration](#versioning-and-integration), including adoption
of this policy by an existing project.

After closing the specification update, consider whether a `Review or gap
assessment` workflow would help evaluate the need for an implementation update.
If so, recommend it to the definer and briefly explain what it would resolve.
Do not recommend it routinely when there is no implementation to assess, when
alignment is already verified, or when the need and scope of an implementation
update are already clear.

#### Maintaining coherent specifications

During authorized specification work, update each requirement in its authoritative
section. Reconcile affected summaries, cross-references, defaults, messages and
acceptance criteria in the selected project context. Integrate a changed rule
with its exceptions; do not append a replacement while leaving contradictory
historical wording active elsewhere. Authority rules resolve already-decided
changes; unresolved choices remain explicit for the definer.

Each topic should have an identifiable owner. Prefer concise links from other
sections to competing normative copies. Keep exact user messages, dynamic
placeholders, icons and their triggers in the corresponding feature sections.
Use a consistent feature structure where helpful: behavior, states and failures,
messages/actions, safety and lifecycle constraints, and acceptance criteria.
A package entrypoint should help a reader locate those owners and dependencies.
Do not reorganize a curated package merely to enforce a template.

When reorganization is requested, inventory existing requirements and map their
new locations before removing or moving text. Preserve substantive requirements,
exceptions, exact copy, compatibility and verification obligations. Record why a
clause is consolidated or superseded; do not discard it solely because it is old.
A refactor must not silently change product behavior, authority or permissions.
Preserve useful reference routes or update affected references explicitly.

Implementation can reveal missing specification detail. Inspect observable
behavior and relevant tests when reproducing an established product is the goal,
but do not promote an implementation accident or current defect into intended
behavior. Record unresolved implementation/specification differences separately.
Private mechanisms belong in decision records unless they are required constraints.
Historical decisions, temporary testing deferrals, device results and current
progress belong in implementation records, not permanent product requirements.

Before reporting the update complete, check requirement coverage, contradictory
or superseded wording, links/anchors, reading order, package independence and
composition/version metadata. Keep an old-to-new requirement map for substantial
reorganizations. Run checks appropriate to the changed artifacts; a specification
refactor alone does not require an application release or comprehensive runtime
retest. Record any implementation gap and follow the existing publication rules.

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

When refreshing implementation documentation, follow
[the current-state and history boundary](002_artifacts.md#current-state-and-historical-records).
Compare claims with the relevant source, configuration and tests; distinguish
implemented behavior from intended behavior and historical validation. Consolidate
obsolete descriptions, check decision supersession and links, and retain current
gaps. Put the refresh findings and checks in its workflow record, not as a new
chronological section in the implementation entrypoint. A documentation-only
refresh does not by itself require a new application release or runtime retest.

### Development branch creation

1. Establish the definer-authorized objective, starting branch and repository.
   Read current Git state and the applicable repository rules. A request to create
   a branch and implement a feature authorizes both scopes; do not ask again for
   already authorized operations. Track setup separately from feature work.
2. Inspect the starting commit, existing branch names and uncommitted changes.
   Preserve existing work. Do not silently stash, discard, commit, or carry unrelated
   edits into the new branch. Resolve material uncertainty about which work belongs
   there before changing its context.
3. Choose a concise descriptive branch name unless the definer supplied one.
   Check for an existing branch; do not reset or overwrite it. Create and switch
   to the authorized branch from the agreed baseline.
4. Record its name, starting branch and commit, composition version, implementation
   version if present, and any deliberately carried uncommitted work. Explicitly
   record unavailable legacy declarations or incomplete bootstrapping state.
5. Link the specification/implementation workflows that will use it. Mark branch
   setup delivered once established; propose closure under the normal rules.

Branch creation alone does not bump versions, authorize feature implementation,
publish a branch, or create release tags. Follow repository authorization rules
for each operation; prior explicit authorization remains valid.

### Development branch merge

Use this workflow for a definer-requested merge request/pull request or merge.

1. Identify source and target branches, repository/remote, the exact requested
   operation, related work and intended scope. Inspect the latest target state;
   if its currency cannot be established, report the missing readiness evidence.
2. Review the whole proposed change relative to that target, including selected
   packages, effective contract changes, implementation coverage, data/format
   compatibility, declarations, documentation and unresolved work. Do not trust
   a branch's provisional version, earlier intention, or old review in place of
   assessing the actual combined result.
3. Resolve conflicts within authorized scope without discarding unrelated work
   or weakening specifications to make incomplete behavior appear compliant.
   Follow repository permissions for branch, rebase and publishing operations.
   Recalculate version impact against the latest target; avoid reusing an already
   finalized version for different implementation or specification contents.
4. Validate the proposed merged tree, not just the source branch alone. Check
   aligned Major.Minor for primary-branch integration, an accurate specification
   baseline reference, applicable tests/builds, metadata, and compatibility.
   Missing required checks, unresolved conflicts or implementation gaps block
   readiness. Record what ran and its source/target commit IDs. Apply required
   checks proportionately; do not invent a comprehensive release qualification
   requirement for a narrow documentation change.
5. If not ready, clearly state **Not ready to merge**, identify blockers and
   consequences, and explain the work needed. Do not create the merge request
   (including a draft as a workaround), perform the merge, create a release tag,
   or claim readiness. Continue authorized corrective work when possible. A
   request to merge is not evidence that checks passed or permission to ignore
   them. Record the failed gate in the workflow.
6. When ready, perform only the requested operation. A merge request includes a
   concrete summary, version changes, validation and relevant limitations. Creating
   it does not authorize merging it. Conversely, an authorized direct merge need
   not create a remote request unless repository policy requires one. Do not add
   redundant approval steps for operations already explicitly authorized.
7. Before the actual merge, confirm that the source and target still match the
   reviewed commits and that required reviews/checks remain satisfied. Reassess
   changed commits and rerun affected checks if either moved. After merging,
   verify the resulting target state and record the request link or merge commit,
   versions, checks and remaining authorized steps. Publication, release tagging,
   branch deletion and workflow closure follow their own applicable rules.

For an intermediate development target, explicitly record its permitted gaps;
do not present integration there as primary-branch or release readiness. Required
checks for the agreed scope still apply.

### Exception

Use this workflow when the definer explicitly asks for something that skips,
ignores, or contradicts the process and no ordinary workflow type can honestly
contain the work.

Also use this workflow to recover from a `conflicting` project phase.

Read `annex_exceptions.md` before executing an exception workflow.

## Cross-cutting rules

### Versioning and integration

#### Automatic classification and updates

Apply [Concepts](001_concepts.md#contract-based-versioning) and maintain
[Version declarations](002_artifacts.md#version-declarations) during ordinary
authorized work. Classify semantic contract changes separately from textual
specification changes and implementation-only changes. Assess compatibility of
the effective composition, not an upstream package's version number alone.

Use one version bump per coherent finalized change set, relative to the previous
finalized version on that line of work. Edits, retries, build runs and fixes during
validation of that same uncommitted change set do not each receive another bump.
If scope changes, recalculate the highest impact against the same baseline. A
later distinct version-affecting change needs a new version even when the earlier
version was committed but not tagged or published. Do not mechanically increment
both independent revision counters.

For a new contract Major or Minor, reset each side's revision to zero when that
side first finalizes it. A development branch may then advance specification
revisions before the first conforming implementation is finalized; implementation
`6.5.0` can therefore implement `spec-6.5.3`. Do not require both revision counters
to be zero at integration. Assign the new release date when finalizing an
implementation version; rebuilding or tagging the same candidate retains it.

For an unchanged contract, specification revisions distinguish finalized edits to
the authoritative root entrypoint, composition, selected package contents and
applicable repository-specific directory specifications.
Only implementation changes affecting the delivered result require an implementation
revision. Keep workflow/test-only and non-authoritative documentation changes in
Git history without manufacturing product releases.

The implementer performs required version bookkeeping automatically within
authorized work, including Major project contract bumps for approved incompatible
changes. This is not permission to change product requirements, bypass Meta's
package-Major approval, or perform unrequested Git operations. Record the baseline,
classification and any no-bump decision in the relevant workflow.

#### Working directly on the primary branch

Support solo and small projects that work directly on `main`. No branch-creation
or branch-merge workflow is required for that approach. For a contract change,
update specifications, implement the change, validate it, and commit both aligned
declarations and their corresponding work together under the applicable commit
authorization. Never create separate primary-branch commits that first introduce
a contract gap and later repair it.

Temporary working-tree mismatches are allowed. Before every primary-branch commit,
the implementer must inspect the proposed committed tree, including the staged
versions and actual scope, to ensure composition and implementation Major.Minor
match, declarations are valid, and the implementation satisfies the contract.
This responsibility remains even if no automated hook or CI check is installed.

If intermediate incomplete states need to be committed, use a development branch.
If creation or switching has not already been authorized, explain the need and
obtain authorization for that operation. Otherwise continue authorized work toward
an aligned commit without requiring a branch. Do not discard work or change a
version number solely to pass alignment checks.

Projects should automate declaration, alignment and release checks in their
normal validation, and protect the primary branch with required checks when
their hosting setup permits. Such checks verify bookkeeping; tests and review
establish conformance. Local checks supplement the implementer's responsibility.
The Macrostates CLI is strongly recommended for the policies its installed
version supports. CLI installation and CLI-specific pre-commit hooks and CI wiring
remain optional; apply the required checks manually or through other suitable
automation when needed. See [Specification verification](#specification-verification).

An editorial composition revision can enter the primary branch while the unchanged
implementation declaration references an earlier exact revision at the same
Major.Minor. Verify that the intervening specification changes do not change the
contract. Do not rewrite a historical release's baseline.

#### Release commits, tags and publication

Committing a versioned change does not automatically create or publish a release.
Create release tags only when the definer requests a release or an explicitly
selected release policy authorizes them, after applicable validation and primary
branch integration. Ordinary builds never create commits, tags or versions.

Use annotated `spec-MAJOR.MINOR.REVISION` tags for finalized composition snapshots
and annotated `vMAJOR.MINOR.REVISION` tags for finalized implementation releases
in the project's main repository. An implementation tag contains its declaration,
corresponding implementation and verification evidence; the referenced composition
tag must identify the exact validated specification snapshot. When both snapshots
are finalized together, both tags may point to the same commit. Reuse an existing
verified composition tag for an unchanged baseline. An editorial-only specification
release does not require an implementation tag.

Check declaration/tag agreement, tagged source completeness, snapshot identity,
Major.Minor alignment, required checks and conflicts with existing tags before
creating tags. Never move, replace or reuse a published tag for different content;
prefer a new version. An existing tag at the same verified release commit needs
no recreation. Distinguish a local candidate, a local tag, a published tag, and a
distributed build in reports. Follow repository permissions for commits and remote
publication; when publication is authorized, publish the relevant commits and tags
together, atomically where supported, then verify their remote identities.

Package tags continue following Meta in each package's own source repository.
Projects releasing multiple independently versioned implementations, or also
publishing a package in the same Git tag namespace, must define unambiguous tag
prefixes before release. Do not silently repurpose historical tags.

Release/tag creation does not close a workflow or substitute for explicit closure
confirmation. Missing required checks block a release; report them honestly.

#### Adopting this policy in an existing project

Inventory existing package, composition and implementation versions, declarations,
build sources and published tags. Preserve their history. During authorized
specification adoption, document the new requirements and the implementation gap;
do not claim the build already consumes a declaration that does not exist.

During the corresponding implementation update, reconcile specifications with
implemented behavior, introduce the release declaration and its build consumers,
remove competing hand-edited metadata, and add applicable validation. Select an
explicit first aligned contract baseline with versions that avoid existing release
identities and preserve platform update ordering. Package Major versions do not
by themselves select the application's new Major.

Until that migration is implemented and checked, keep the specification changes
as an explicitly incomplete local candidate or on an authorized development branch.
Do not commit an unaligned adoption state on the primary branch or tag it as an
aligned release. This permits specifications to be prepared before implementation
without weakening the primary-branch rule. A specification-only project without
an implementation declares only the composition version; a new implementation
normally starts at `0.1.0` / `spec-0.1.0` unless another baseline is defined.

### Ambiguity and conflicts

When ambiguity, authority conflict, or workflow conflict is found, read
`annex_conflicts.md`.

### Specification verification

Prefer the Macrostates CLI when it is available and supports the selected
composition, package releases and policy versions. Meta's `annex_cli.md` owns
command guidance and manual equivalents; locate it through the selected Meta
package's entrypoint. CLI installation and use remain optional. Continue with
relevant manual verification when it is unavailable or incompatible, or when
additional inspection is necessary. The same selected requirements apply with
either method. Tool absence alone does not block work that can be verified.

Apply specification checks at these points:

- During setup and after importing or deliberately updating packages, validate
  the resulting selection, dependencies, metadata, paths and entrypoints. Check
  imported package integrity against the verified selected source.
- After changing the composition, package metadata, specification entrypoints,
  reading/authority orders or local specification references, check the affected
  structure and dependency relationships.
- When installed external package files or their provenance/lock baseline change,
  or unexplained modification is suspected, check the relevant package integrity.
  Authorized project-owned specification edits remain ordinary specification work.
- Before committing specification-affecting changes, inspect the proposed staged
  tree and apply the affected checks. CLI `check --staged` can assist where
  supported; an equivalent manual inspection is valid. Earlier working-tree
  results alone do not verify differently staged files.
- At a workflow's completion or requested review, confirm that the relevant
  verification evidence covers the delivered state. Apply release and primary-
  branch gates separately when those operations are in scope.

Choose the smallest scope that covers the change and its dependencies. Reuse
relevant evidence for unchanged package contents when its baseline and provenance
remain valid. Starting a new session or changing unrelated implementation files
alone does not require rereading every package or repeating a full integrity
comparison. Existing before-commit version/alignment responsibilities still apply.

Record the CLI version and relevant commands, or the manual checks and compared
baseline, with results and coverage limits in the workflow. Distinguish tool
incompatibility from a failing check. Investigate reported modifications and
metadata errors; using a manual method does not excuse an unresolved failure.
If required verification cannot be completed, report the missing evidence and
preserve the applicable readiness gate. A passing structural or integrity check
does not establish semantic consistency or implementation conformance.

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

For `Development branch creation`, check that the authorized branch exists at the
intended baseline, local work was preserved, starting versions/commit are recorded,
and linked feature workflows retain their own scope. Do not require feature
completion or remote publication to deliver branch setup.

For `Development branch merge`, check that the requested operation was authorized,
readiness was evaluated against the actual source/target commits and combined
result, version alignment and applicable checks passed, and the request/merge
outcome is recorded. If blocked, no merge request or merge was performed and the
definer received the specific blockers and consequences.

For all version-affecting work, verify the classification, declarations and
primary-branch invariant before committing. For release work, verify the exact
specification baseline, tags and any authorized remote publication separately.

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
