# Macrostates CLI Implementation

Project phase: active.

The release branch prepares independent application version `0.4.0`, declared
with candidate status in [application.yaml](application.yaml). The tracked
composition and [release.yaml](release.yaml) now declare the linked candidate
baselines `specs-1.0.0` and `imp-1.0.0`, dated `2026-10-13`, under the bound
[release plan](release-plan.yaml). Application source tag `v0.4.0` is a declared
future immutable source identity; it does not yet exist as a published release.
No new baseline tag or application publication is claimed.

Explicit earlier migration preserved the historical `specs-0.3.0`/`imp-0.3.1`
numbers, original implementation release date `2026-10-09`, and legacy tags before
this separate finalization proposal. The definer accepted closure of the feature
implementation and integration-preparation scopes. On 2026-10-13 the definer separately accepted the verified implementation
represented by the imp-1.0.0 candidate as the first baseline good enough and
authorized moving to active. The release/integration preparation workflow is
completed with explicit closure confirmation. Numerical finalization still
requires the passing release proposal integration; publication remains separate.

## Current Behavior And Adoption State

The console command and public Python API support package initialization,
installation, canonical locking, inspection, structural checks, inventory checks,
and exact staged-index checks. Legacy persisted formats, source adapters, and
selected-policy behavior remain supported.

New source behavior adds generic `git-archive` transport and public `GitSource`.
It fetches an explicit annotated package tag into temporary Git storage and
archives the resolved commit. Package destinations contain tracked source files,
not upstream Git metadata. Existing selections reject moved locked commits and
edited inventories. The prior transport remains available for older selections.

The development API additionally implements captured work origins, change impact
records, optional deliverable inspection, documentary workflow closure requests,
Git synchronization, exact combined integration checks, bound baseline release
planning/preparation/checking, and explicit declaration migration. Process 5.0
selection gates the versioning-specific operations. Git synchronization inspects
configured refs and optionally fetches, merges, or rebases only when requested.
It preserves original work provenance and unresolved conflicts.

The eight canonical specification repositories have been reviewed, merged, and
released as Meta 2.2.0, Process 5.0.0, Repository-1 4.0.0, Python 2.1.1,
Python-project-1 3.0.0, Python-library-1 2.0.0, Android-app-1 5.0.0, and Docker-1
3.0.0. Their previously published tags remain unchanged.

The verified CLI adoption uses Meta 2.2.0, Process 5.0.0, Repository-1 4.0.0,
Python 2.1.1, Python-library-1 2.0.0, and local CLI 1.0.0, with canonical
`git-archive` sources for external packages. Actual canonical installation and
locked reinstallation both returned zero diagnostics. The exact composition,
entrypoint, and integrity lock reflect those releases. Offline project checks and
change-readiness checks also returned zero diagnostics after adoption and
explicit identity migration.

The versioning feature was integrated through PR #6 after all six feature
push/PR checks passed, producing main commit
`32c1cf2a993fadd2ce152c02e1e946e9218c2ea4`. Its
[captured work record](work/versioning-system.yaml) preserves
origin commit `96a467c448f6fc5abf3ca9f8b19a29d976725c93`, with the original
`specs-0.3.0`/`imp-0.3.1` identities. The
[archived change record](changes/history/versioning-system.yaml) declares Major
impact for both baselines, requirement/implementation/verification coverage,
evidence, and no open gaps. Candidate preparation preserves its consumed bytes in
history.

The separate [release work record](work/baseline-release-1-0-0.yaml) captures
the merged main commit as its origin. Its
[archived bookkeeping record](changes/history/baseline-release-1-0-0.yaml)
declares no additional baseline impact. The candidate plan binds source commit
`4e4ab0601524371215b91d37916e90e5abe9f924`, cached integration target
`32c1cf2a993fadd2ce152c02e1e946e9218c2ea4`, declaration hashes, and both
consumed record hashes. Reviewed aggregate Major/Major scope determines the
1.0.0 candidates; ordinary feature work did not reserve those official versions.

## Architecture

| Area | Implementation Responsibility |
| --- | --- |
| `_models.py` | Normalized package/composition models, public diagnostics, reports, and controlled errors |
| `_formats/` and `_io.py` | Explicit composition/metadata readers, strict YAML, field/path primitives, and retained formats |
| `_validation.py` | Metadata/dependency/link checks and explicit Meta 2.0/2.1/2.2 and Process 2.3/2.4/3.0/4.0/4.1/5.0 policy adapters |
| `_scopes.py` | Visible directory-scoped specification discovery and independent-composition boundaries |
| `_sources.py` | Injectable transport boundary, generic Git provider, and retained legacy HTTP provider/authentication |
| `_integrity.py` | Bounded archive extraction, inventories, content identities, and integrity lock reader |
| `_project.py` | Public orchestration, live configuration reads, policy gating, and transport selection |
| `_git.py` and `_sync.py` | Credential-safe Git argument vectors, ref/primary/state guards, cached divergence, and explicit synchronization |
| `_changes.py` and `_versioning.py` | Captured origin/change records, impact/evidence checks, baseline declarations, aggregation, and computed identities |
| `_deliverables.py` | Optional independent/default application policies, Android metadata/order checks, and declared source-reference validation |
| `_integration.py` | Workflow/history documentary gates, numbered closure requests, exact combined-tree validation, and stale-state detection |
| `_release.py` | Commit/tree/record-bound plans, guarded candidate preparation, preserved history, tag/snapshot checks, and publication readiness |
| `_migration.py` | Explicit legacy identity spelling conversion with retained original-tag provenance |
| `_mutations.py` | Recoverable replacement and ordinary-failure rollback |
| `_staged.py` | Exact Git index export without changing the checkout/index |
| `_build_version.py` | Standalone application-version reader, shipped-source validation, and retained legacy build declaration support |
| `_cli.py` | Flat command arguments, public method calls, human/JSON rendering, and exit-code translation |

Core project/versioning operations have no hosting API dependency. External
reviews, protection, CI scheduling, tagging, and artifact distribution belong to
repository/application procedures. The repository's existing publication workflow
is provider-specific infrastructure. It now checks the application version
against the publication tag, checks its declared global baseline identities,
and invokes publication readiness checks before building and uploading artifacts.
It has not published application `0.4.0`. Core CLI portability does not depend on
that provider.

Ordinary imports have no project/network/subprocess side effects. Explicit
`__version__` access reads installed distribution metadata. Only package source
operations and explicitly requested remote fetch access remote sources.
Synchronization can update Git history under the requested merge/rebase strategy;
planning/checks do not commit, tag, submit proposals, or publish. No operation
automatically closes a workflow or infers definer approval.

## Version And Build Sources

The project composition identifies its Macrostates specification baseline.
Process 5's schema-2 `release.yaml` identifies the implementation baseline;
the current candidate links it to exactly `specs-1.0.0`. Earlier explicit migration
preserved historical baseline numbers/date and legacy refs. The application
candidate independently declares `0.4.0`, matching baseline references, its future
source tag, and the shipped-source fingerprint. The independent application
declaration identifies the CLI distribution version and development/candidate/finalized state.
Source-only projects do not gain an invented implementation from initialization.

The standalone build reader validates application version syntax, state,
baseline relation, and canonical calendar date. Development source uses a Python
development representation. Candidate/finalized builds require `source_sha256`
to match shipped inputs. The current fingerprint covers README, license,
pyproject, manifest, implementation release declaration, and package source,
including executable identity while excluding caches and the application
declaration's own bytes. Workflow/specification-only artifacts are not shipped
inputs. This avoids a self-hash and permits isolated source-archive rebuilding.

The source distribution includes both application and implementation declarations.
It needs no installed CLI, selected package snapshots, Git, or release lookup to
derive its build version. The wheel reports its installed distribution metadata.
Builds do not edit declarations, allocate versions, tag, or publish. Normal
dependency installation may still require package indexes.

## Extension And Compatibility

Read [the adapter decision](decisions/0001-versioned-format-adapters.md) and
[modern package adoption](decisions/0002-modern-package-adoption.md) as historical
design records. New persisted formats need explicit readers and normalization;
retain old readers and regression fixtures. New source types need explicit
validation and transport support. New Process policies need release-selected
adapters rather than modifying prior projects' rules in place.

Public exports/signatures, command options/results, persisted artifact shapes,
and source authentication interfaces are compatibility surfaces. Exact internal
algorithms, module layout, resource limits, and diagnostic wording remain
implementation choices. Initial 0.x application versioning does not justify
silently breaking existing documented use. Migrations remain explicit and
preserve published refs; baseline finalization does not assign independent app
versions or replace unchanged application provenance.

## Verification And Limits

Use the README's contributor checks and artifact probes. Coverage includes
legacy fixtures, local canonical Git remotes/tags, captured provenance,
independent counters, exact integration snapshots, stale targets, documentary
workflow/history gates, migrations, plans/candidates, and isolated application
build metadata. The full 393-test suite passed separately on Python 3.12, 3.13,
and 3.14 against the prepared 0.4.0 candidate, retaining the legacy regression
suite. Ruff checks and formatting passed across 115 Python files; Pyright reported
zero errors and warnings. The candidate wheel and source distribution passed clean
API/command/version installation probes, shipped-source byte checks, and strict
Twine metadata checks.

Dated verification and adoption evidence belongs to
[the implementation workflow](workflows/history/2026-10-13__1A1GXH__versioning-system.md).
That workflow and
[integration preparation](workflows/history/2026-10-13__1RPQX8__integration-preparation.md)
are closed with explicit confirmation. The closed feature source/index was
verified, and all six feature checks passed before its normal PR integration.
Candidate-specific local tests and build verification are recorded in
[release preparation](workflows/history/2026-10-13__26SXA5__baseline-release-preparation.md).
The definer confirmed its completion and closure and separately accepted the
first implementation baseline. Final proposed-tree checks, release PR
CI/integration, immutable new baseline/application tags and application
publication remain separate outcomes; no future delivery is claimed.

Structural checks cannot prove semantic classification, truth of approval,
requirement coverage, or independent application policy decisions. External
checks/reviews and fresh remote state remain separate gates. Workflow checks
inspect status and recorded confirmation; they do not authorize closure.
Declarative source references and artifact metadata need project-specific release
review in addition to structural validation.

Transactions roll back ordinary failures, with retained recovery files on rollback
failure. They do not guarantee power-loss/crash atomicity or complete isolation
from arbitrary external writes. Locks are reviewable baselines, not signatures.
Local link checks target files rather than full Markdown semantics/heading
anchors. Scope discovery omits hidden/tool/cache/build/temp directories and
separately composed subprojects. Index snapshots omit submodule contents.

Current resource bounds remain implementation choices: YAML/API documents 2 MiB,
archive inputs 32 MiB, extracted archives/index snapshots 128 MiB, and archive
entries 10,000. The legacy HTTP tag resolver bounds annotation nesting.
Interrupted package/release operations require inspection and manual recovery.

See [specification conformance](specification-conformance.md) for the current
contract map and remaining integration/release checks. Historical workflows retain
their dated evidence and individual statuses; a history location does not imply
definer-authorized closure.

## Workflow State

The definer explicitly accepted closure of the versioning implementation and
feature-integration preparation scopes. Both records remain completed in history
with their scoped confirmation. The separate release/integration preparation
workflow is completed in history with the definer's 2026-10-13 confirmation.
The same response explicitly accepted the verified first implementation baseline
and authorized the active phase. These decisions do not substitute for passing
external checks, normal integration, immutable tags or actual publication.
