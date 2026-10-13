# Macrostates CLI Implementation

Project phase: bootstrapping.

The source branch develops independent application version `0.4.0.dev0`, declared
in [application.yaml](application.yaml). The current tracked composition and
[release.yaml](release.yaml) have been explicitly migrated to the preserved
historical `specs-0.3.0` and `imp-0.3.1` identities. This spelling migration
retains the original implementation release date, `2026-10-09`, and published
legacy tags; it does not finalize the changed development source. The proposed
next baseline finalization is `specs-1.0.0`/`imp-1.0.0`, with a separate independent
CLI application release `0.4.0`. Those upcoming identities are not integrated or
published. First-baseline phase acceptance and closure of the current implementation
and integration-preparation workflows have not been granted; the project remains
in bootstrapping. The nine earlier requested workflow closures are explicitly
recorded in their historical artifacts.

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

The current feature is ordinary pending Major specification and implementation
work. Its [captured work record](work/versioning-system.yaml) explicitly preserves
origin commit `96a467c448f6fc5abf3ca9f8b19a29d976725c93`, with the original
`specs-0.3.0`/`imp-0.3.1` identities. The
[change record](changes/versioning-system.yaml) declares Major impact for both
baselines, requirement/implementation/verification coverage, evidence, and no open
gaps. It is not a prepared release candidate. A later reviewed baseline
finalization will consume the pending record.

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
adoption of that format is explicit and preserves the preceding baseline numbers,
original release date, and legacy refs. The independent application declaration
identifies the CLI distribution version and development/candidate/finalized state.
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
and 3.14, retaining the legacy regression suite; all 393 tests passed again on
Python 3.14 after canonical adoption. Ruff checks and formatting passed across
114 Python files, and Pyright reported zero errors. Rebuilt development wheel and
source-distribution artifacts passed clean API/command installation probes,
shipped-source byte checks, and Twine metadata checks.

Dated verification and adoption evidence belongs to
[the implementation workflow](workflows/2026-10-13__1A1GXH__versioning-system.md).
Only that workflow and
[integration preparation](workflows/2026-10-13__1RPQX8__integration-preparation.md)
remain open. Closure must precede the final closed-source/staged checks and
feature proposal. Remote CI, feature integration, the new global baseline,
stable application publication, and first-baseline phase acceptance remain
separate pending outcomes.

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
