# Development And Releases

## Policy And Responsibility

These operations implement the supported Process 5.0, 5.1 and 6.0 policies with the
same technical formats and structural readiness checks. Core behavior uses
Git repositories, refs, commits, and reviewed integration without requiring a
particular hosting platform or external changeset product. Projects define their
integration/review policy and may define independent application release policies.
The CLI never infers semantic impact from changed files or treats a matching
version pair as proof of conformance.

Process 5.1 and 6.0 do not require separate definer approval solely for a Major impact
classification or baseline increase within authorized work. This does not close
a workflow or authorize additional scope, integration, tags, or publication.
Apply the selected authority rules in
[Versioning and compatibility](006_versioning.md#release-selected-policies).

Application policy is optional. The default stable application version is the
numeric part of its selected finalized implementation baseline. A monorepo can
share one specification/implementation baseline while releasing independently
versioned applications. The CLI inspects declared policies but does not assign
versions under independent application schemes or publish their artifacts.

Git baseline operations require the shared composition at the Git repository
root. This supports applications in a common-baseline monorepo. An independently
composed nested project inside another checkout retains existing discovery,
lint/integrity, and staged checks, but uses separate Git or manual procedures for
its independent baselines. Reject unsafe nested baseline mutations; identity
inspection reports unavailable computed identity with an explanation instead of
accidentally using the parent repository's snapshot.

## Captured Work And Development Identity

Work, change, and deliverable IDs are portable lowercase ASCII identifiers.
`start_work` captures a unique work ID, original full commit identity, original
specification baseline, and original implementation baseline or explicit null.
Store the schema-1 record under `.macrostates/implementation/work/<id>.yaml`.
Capture immediately after creating the development branch, before subsequent
commits or synchronization can obscure its starting point.

Automatic origin capture is allowed only at a known starting commit. Late work
requires an explicit original full commit; read its declarations and reject
missing, ambiguous, or malformed provenance. Preserve already captured origins
and refuse duplicate work IDs. Do not replace original provenance with the newest
primary-branch state when merging or rebasing upstream changes.

`identity(work=...)` can select a captured work record or pending/historical
change record. Its specification and implementation identities derive from that
origin and the current commit, for example:

```text
specs-0.3.0-branch.feature-x.gabc123
imp-0.3.1-branch.feature-x.gabc123
```

Compute suffixes without committing the current commit's own hash into tracked
declarations. Without a selected work record, unfinalized source exposes an
unreleased identity based on recorded declarations. Report candidate, finalized,
development, unreleased, dirty, and unavailable states honestly. A dirty tree
must not claim a clean finalized snapshot. A source archive without Git reports
unavailable computed identity rather than fabricating a commit.

Identity output contains `state`, computed `specification`/`implementation`,
`baselines`, `commit`, `branch`, `dirty`, chosen `work`, and `pending_changes`.
Missing implementation identity remains null. A finalized claim requires the
exact finalized source relationship, not merely numeric syntax or the absence
of pending records. Readiness verification remains a separate operation.

## Change Records And Evidence

`create_change` writes a unique schema-1
`.macrostates/implementation/changes/<id>.yaml` record. Capture or reference its
original work provenance and declare `specification` and `implementation` impact
independently as `none`, `patch`, `minor`, or `major`. Reuse captured work by
explicit `work` ID, or by the matching change ID when present. Otherwise require
safe automatic or explicit late origin capture. Reject conflicting origin inputs
and duplicate IDs across pending and historical records.

The record contains summary, origin, both impacts, affected deliverable IDs,
requirement coverage, evidence, and gaps. Required collections are explicit,
including empty ones. Requirement coverage maps each changed requirement to
implementation evidence and verification. Preserve supported extension fields.

Work-in-progress records may have incomplete evidence or documented gaps.
`check_changes` readiness requires evidence for every version-affecting record,
coverage for contract changes, no unresolved required gaps, and valid baseline
provenance. Implementation impacts require an established implementation baseline.
Tracking-only changes explicitly declare `none` on both sides and do not allocate
an official version. Integration requires a new or updated scope record even for
no-bump decisions, or a validated release-preparation plan that consumes records.

Change records remain pending after their work is accepted. They are distinct
from open workflows and can await baseline finalization on the primary branch.
Included records move to `changes/history/` with their content preserved during
release preparation; history must not hide duplicate IDs or altered evidence.

## Deliverable Inspection

Optional `.macrostates/implementation/deliverables.yaml` schema 1 maps stable
deliverable IDs to entries under `deliverables`. An absent document returns an
empty mapping and does not invent applications. Entries default to
`strategy: implementation` or explicitly choose `independent`.

An implementation-derived entry receives the numeric selected `imp-*` baseline,
using its explicit historical baseline when supplied or the current declared
baseline otherwise. A competing explicit version is invalid. Independent entries
must provide a nonempty version; their version scheme and bump decisions belong
to effective application specifications. Extension fields remain inspectable.

Validate provided baseline syntax and contract relation, canonical calendar
dates, Android integer counters, and explicit source identity shapes. A dated
application release needs exact specification and implementation references.
Source provenance can use a known full commit or an immutable tag, allowing a
future candidate tag to be declared without storing a commit's self-hash. Resolve
required source references before publication; a tag and supplied commit must
agree.

Android defaults its version name to the numeric selected implementation version
while retaining a separate tracked increasing version code. Compare declared
Android release ordering against the integration target: prevent counter
decreases and require a higher code for a changed application version. Do not
allocate counters during inspection or baseline preparation. Unchanged apps can
retain prior versions and exact historical provenance.

## Branch Synchronization

`branch_status` reports current branch/commit, requested or configured target,
target commit, ahead/behind counts, and cached remote freshness without fetching.
A target defaults to an unambiguous configured primary branch or remote/local
default. Ambiguity requires explicit configuration or input.

`sync_branch` performs only the explicitly requested merge or rebase against a
resolved target. Optional fetching uses an explicitly named configured remote.
Require an attached development branch, clean index/worktree, and no active
merge/rebase/cherry-pick. Refuse the detected primary branch, including qualified
local references; an additional caller-supplied primary name cannot bypass that
guard. Reject unsafe option/control-character refs.

Preserve conflict state for manual resolution. Do not force-push, stash,
discard work, switch branches, or resolve semantic conflicts automatically.
Successful output includes divergence information, previous commit, strategy,
and whether a remote was fetched. Keep original work/change origins unchanged.
The implementer reviews inherited requirements and reruns affected checks;
synchronization invalidates stale validation and release plans.

Updating a fork's primary mirror is a separate repository-policy operation.
It does not change the feature branch until upstream changes are incorporated
there. The CLI does not author changes or synchronize a primary branch directly.

## Closure And Local Integration Preparation

`closure_request` lists every workflow needing definer-authorized closure,
including records in workflow history and malformed statuses. Return both the
records and a short numbered permission request stating that closure is required
before preparing the integration proposal. It must not send messages, infer
approval, close records, or fabricate confirmation.

The implementer obtains explicit authorization and records completed, abandoned,
or superseded outcomes with preserved confirmation evidence. Empty authorization
headings or placeholders do not establish closure. In-progress, paused, blocked,
missing/duplicate/unknown statuses, and unconfirmed closed records block local
preparation. Renaming a record to an index filename or placing it in history
cannot bypass the gate. Ordinary index documents without record status remain
permitted. A documentary check cannot prove approval authenticity.

Close the integration-preparation workflow itself after its local work and
required acceptance are complete. The resulting tree must have no open
workflows. Later review corrections open and close their own workflows on the
development branch before integration. Workflow closure does not claim external
review approval, integration, baseline finalization, or application publication.

## Exact Integration Readiness

`check_integration` resolves explicit source and cached target commits, requires
committed source contents, and checks their exact proposed combined tree without
changing the checkout/index or creating a merge commit. Validate project
structure/integrity, change coverage/evidence/gaps, workflow closure, declared
application metadata, and applicable Android ordering in that combined tree.
Conflicts and missing scope records fail readiness.

An optional expected full target commit must match. Source/target movement or
worktree changes during checking invalidate the result. Report the validated
source and cached target; remote freshness is not implied. The implementer must
refresh the authoritative remote state and obtain the project's required
external checks/reviews before integration. External checks may be pending when
the proposal is opened, but remain a separate final integration gate.

## Baseline Release Planning And Preparation

Prepare a dedicated release branch from current integrated target contents.
`plan_release(target=...)` accepts an explicit authoritative cached Git ref, such
as `origin/main`, or defaults to the configured primary branch. It is read-only
and requires committed, readiness-valid pending records and established
declarations. Fetching is separate; the planned source must incorporate the
selected target's current contents. Bind the proposal to the target ref, current
source and target commits, the exact planned source tree, declaration hashes, included and
historical record IDs/hashes, proposed baselines, combined impacts, and affected
deliverables. A specification-only project may plan specification changes;
never infer its first implementation. Tracking-only records do not allocate a
new baseline version.

Aggregate the highest Major or Minor contract impact once across included work,
update shared Major.Minor, and reset lower numbers. With unchanged contract
Major.Minor, advance each side's Patch once when its included records require it.
Leave the other side unchanged. An implementation release references the exact
specification baseline it implements. Preserve an unchanged implementation's
earlier specification reference when a later editorial specification patch is
finalized separately.

`prepare_release` accepts an exact reviewed plan and explicit calendar date on
a safe development branch. Reject changed HEAD/target/tree, declarations,
included or historical record bytes/set, unresolved gaps, an existing
unintegrated candidate recorded in the workspace, and altered calculations.
Repository review policy coordinates a single active finalization per version
line; the CLI does not inspect a hosting service's proposal catalog.
Update candidate baseline declarations,
archive consumed records, and record the candidate plan through recoverable
tracked writes. Independent application versions and counters remain untouched.
Never create commits, proposals, tags, or publications implicitly.

## Application-Only Release Preparation

An application release policy may prepare a new release at source commit
`A` after its referenced baseline was finalized at `B`. Permitted differences
are application identity/provenance metadata and required change/workflow
bookkeeping; behavior, effective specifications, and build logic remain unchanged.
Declare `none` impact on both sides with actual verification evidence and no
required gaps. Complete definer-authorized workflow closure and reviewed
integration against the exact combined result.

Keep the referenced baseline declarations, annotated tags, previous baseline plan,
and consumed record hashes unchanged. The new no-impact record remains pending
for a later genuine baseline release. Do not consume it into the old plan,
manufacture a no-bump plan, or move a baseline tag to `A`. Record the application's
new version/source identity separately from the exact `specs-*`/`imp-*`
references at `B`. Pending version-affecting work or unapproved source changes
prevent publication as metadata-only bookkeeping.

The application's policy must permit the new immutable identity. An index that
already has the default numeric implementation version cannot receive changed
artifacts under that same version. An independent numbering policy, or an
applicable technology-owned additional identity such as Android's version code,
can distinguish another release.

## Release Readiness And Publication Boundaries

`check_release` validates candidate declarations, original tree/declaration
binding, archived records and evidence, impact calculations, permitted
finalization changes, closed workflows, and source ancestry. New unplanned
behavior or source changes require returning that work to pending state and
replanning. Changed target state invalidates an unintegrated candidate.

Candidate checks allow new baseline tags to be absent, but reject existing
conflicting or lightweight tags. An unchanged referenced baseline must already
have its correct annotated identity; an unchanged specification must identify
the candidate's actual specification snapshot. Verified legacy aliases preserve
published references during migration.

Baseline publication checking additionally requires the candidate source to be
integrated into the target and every newly finalized baseline to have an
annotated tag at that exact source. For a later application-only release, verify
the referenced historical baseline at its integrated annotated tag and preserve
its original plan, declarations, consumed records, and specification/source
binding. Independently validate the new application source, allowed metadata
delta, ready no-impact records, closed workflows, required checks, and declared
source references. A valid historical tag is not required to move to current
HEAD. Source tags and recorded commits must agree where both are supplied.

These checks do not create tags, upload packages, publish every application, or
obtain external authorization. Project-specific artifact checks and application
release procedures remain necessary.

Treat candidate preparation, reviewed integration, local tagging, remote tagging,
and artifact distribution as separate states. Retain published identities during
partial-release recovery, and use a new identity if released contents change.
