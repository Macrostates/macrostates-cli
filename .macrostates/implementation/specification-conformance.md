# CLI Specification Conformance

## Scope And Current State

This document maps the revised local CLI contract to current source and
verification. The current application declaration is candidate `0.4.0`, separately
linked to candidate baselines `specs-1.0.0` and `imp-1.0.0`, dated `2026-10-13`.
The bound [release plan](release-plan.yaml) records the reviewed source, target,
declarations, and consumed records. The application declares future source tag
`v0.4.0` and its shipped-source fingerprint; neither a new tag nor publication
has occurred. Earlier explicit migration preserved the historical 0.3.0/0.3.1
baseline numbers, implementation date `2026-10-09`, and legacy tags before this
separate finalization proposal.

The approved canonical releases are published: Meta 2.2.0, Process 5.0.0,
Repository-1 4.0.0, Python 2.1.1, Python-project-1 3.0.0, Python-library-1 2.0.0,
Android-app-1 5.0.0, and Docker-1 3.0.0. Their older tags remain unchanged. Verified
CLI adoption selects Meta 2.2.0, Process 5.0.0, Repository-1 4.0.0, Python 2.1.1,
Python-library-1 2.0.0, and local CLI 1.0.0, using canonical external
`git-archive` sources and the approved dependency minima. Actual canonical
installation and locked reinstallation both returned zero diagnostics, as did
offline project checks and change-readiness checks after migration.

The feature was integrated through PR #6 after all six feature push/PR checks
passed, producing main commit `32c1cf2a993fadd2ce152c02e1e946e9218c2ea4`.
Its [work record](work/versioning-system.yaml) explicitly captures original commit
`96a467c448f6fc5abf3ca9f8b19a29d976725c93`; the
[archived change record](changes/history/versioning-system.yaml) preserves the
original baseline identities, declares Major/Major impacts, records requirements
and verification evidence, and has no open gaps. The separate
[release work record](work/baseline-release-1-0-0.yaml) captures merged main as its
origin; its [archived bookkeeping record](changes/history/baseline-release-1-0-0.yaml)
adds no baseline impact. The plan binds source
`da4287ece3cd689ed207e05638c2168528b1487f` and cached target
`32c1cf2a993fadd2ce152c02e1e946e9218c2ea4`, preserves both consumed record
hashes, and derives 1.0.0 candidates from aggregate Major/Major scope.

The release proposal and application publication have not been integrated or
completed. The project remains in bootstrapping; first-baseline phase acceptance
remains pending. The definer confirmed closure of both feature scopes, preserved
in history. The new combined release/integration workflow remains open.

The preceding published application remains valid under its earlier selected
policies. New APIs and flat commands implement Process 5's captured provenance,
change/evidence records, independent application policies, integration gates,
and reviewed baseline preparation. Meta 2.2 adds generic tagged Git source
transport without changing composition format 1. Retained formats/providers and
earlier Meta/Process adapters preserve their existing behavior.

Code review covers public factories/exports, command dispatch, persisted records,
source authentication/archives, strict configuration, Git guards/synchronization,
combined snapshots, workflow evidence, candidate plans, exact tags, migration,
and independent build metadata. Specification requirements describe observable
behavior. Internal algorithms/module names in this map are implementation
references, not additional normative architectural constraints.

## Contract Map

Paths are repository-relative. Listed tests and inspection identify evidence;
they do not imply every conceivable edge has independent automated coverage.

| Specification | Implementation | Evidence Or Required Check |
| --- | --- | --- |
| [Concepts](../specs/051_cli/001_concepts.md): identities, ownership, effects | `_project`, `_cli`, domain modules | Existing import/offline/command contracts and side-effect review; synchronization is the explicit Git-mutation exception |
| [Library](../specs/051_cli/002_library.md): root exports and public API | `__init__`, `_models`, `_project` | Existing public report/factory contracts; new Project API tests and signature review |
| Library generic/legacy source boundary | `_sources`, `_project` | `test_git_sources.py`, retained `test_sources.py`, injected providers, exact local Git tag/inventory checks |
| [Commands](../specs/051_cli/003_commands.md): flags, data, reports, errors | `_cli`, `_project` | Retained command contracts, `test_cli_versioning.py` flat-command/data/origin/option checks, and rebuilt development-artifact installed-command probes |
| [Composition](../specs/051_cli/004_composition.md): discovery, formats, paths, dependencies | `_formats`, `_io`, `_scopes`, `_validation` | Historical/current metadata fixtures, dependency/link/scope tests, generic source validation |
| [Integrity](../specs/051_cli/005_integrity.md): canonical snapshots and locks | `_integrity`, `_project`, `_sources` | Existing rollback/inventory tests; moved/lightweight/missing local tags, executable files, dirty-copy preservation |
| [Versioning](../specs/051_cli/006_versioning.md): selected-policy isolation | `_validation`, `_project` | Retained Process/Meta policy tests and new Process 5 domain fixtures; unknown future policies fail explicitly |
| Versioning explicit migration | `_migration`, `_release` alias verification | `test_version_migration.py`: no implicit conversion, idempotence, source-only projects, primary refusal, preserved refs/history and invalid metadata |
| Versioning application/build source separation | `_build_version`, application declaration, pyproject, manifest | `test_application_build.py`, retained `test_build_version.py`, rebuilt development wheel/sdist clean installs, shipped-source bytes and Twine metadata checks |
| [Development](../specs/051_cli/008_development-and-releases.md): captured work and explicit impact | `_changes`, `_versioning`, `_project` | Domain record/identity tests and original-origin review; explicit late capture and work references |
| Development application/default inspection | `_deliverables`, `_project` | `test_deliverables.py`: independent Python versions, Android default/code, historical provenance, ordering and malformed metadata |
| Development synchronization and primary guards | `_git`, `_sync` | `test_integration_sync.py`: merge/rebase, full refs, main/master/custom primary, dirty/detached/active state, explicit fetch and preserved conflicts |
| Development closure requests/history gates | `_integration` | Open/closed statuses, confirmation evidence, index-renaming refusal, archived records and no automatic closure |
| Development exact combined readiness | `_integration`, project/domain checks | Explicit scope records, inherited target workflows, gaps, merge conflicts, stale expected/during-check targets |
| Development release plans/preparation | `_release`, `_versioning`, `_mutations` | `test_release_records.py`: aggregation, explicit target refs, commit/tree/record binding, candidate/history checks and retained baseline plans/tags for metadata-only application release |
| Development release identity/publication checks | `_release`, `_deliverables` | `test_deliverable_sources.py`: declared source tags/commits, agreement, source declarations/baselines and custom-source manual warnings; final artifacts and external authorization remain separate |
| [Verification](../specs/051_cli/007_verification.md) | Contributor tooling, tests, build and CI | Full 393-test suite passed on Python 3.12/3.13/3.14 and again on 3.14 after adoption; self-install/reinstall, offline/readiness, Ruff/formatting, Pyright and development artifact probes passed; all six feature push/PR checks passed; current release candidate checks are recorded separately |
| [Recovery](../specs/051_cli/annex_recovery.md) | Transport, synchronization, migration and replacement boundaries | Preserved package edits/conflicts/provenance, stale plans, markers/recovery-data review |

## Verified Development Evidence

The full 393-test suite passed separately on Python 3.12, 3.13, and 3.14, including
the retained legacy regression suite. All 393 tests passed again on Python 3.14
after adoption. Ruff lint and formatting checks passed across 114 Python files;
Pyright reported zero errors. Generic-source, synchronization, migration,
release and deliverable integration tests use temporary local Git
repositories/remotes and synthetic metadata, with no package-source network
calls.

These tests exposed and verified repairs for empty closure authorization headings,
invalid legacy migration dates, and noncanonical application dates. They also
verify that a finalized application build binds shipped source while excluding
self-referential application metadata, and that source archives preserve the
verified build identity without Git.

Actual canonical install/reinstall and offline/readiness checks passed after
adoption. All 393 tests passed separately on Python 3.12, 3.13 and 3.14 against the
prepared candidate. Its 0.4.0 wheel and source distribution passed clean
API/command/version installation probes, shipped-source byte comparisons, and
strict Twine metadata checks. These local candidate artifacts do not finalize or
publish application `0.4.0`.

Dated verification and adoption evidence belongs in
[the implementation workflow](workflows/history/2026-10-13__1A1GXH__versioning-system.md)
and [integration preparation](workflows/history/2026-10-13__1RPQX8__integration-preparation.md).
Both local scopes are explicitly closed. Final source/staged verification
preceded feature proposal submission; all six feature push/PR checks passed before
normal integration. Current candidate-specific local test and build verification
is recorded in
[release preparation](workflows/2026-10-13__26SXA5__baseline-release-preparation.md).
That workflow is open; release proposal closure/CI/integration, stable baseline and
application tags/publication, and phase acceptance remain pending. Historical
publication evidence stays in its original records.

## Integration And Release Work Still Required

- Verify the exact committed candidate and combined target tree with its bound
  plan, declarations, source fingerprint and archived records.
- Obtain explicit closure of the release/integration preparation workflow and
  verify its closed proposed source/index against the current primary target.
- Submit the candidate proposal and require remote checks before normal
  integration, then verify immutable baseline/application tags and independently
  publish application `0.4.0` through the authorized procedure.
- Retain bootstrapping until the definer explicitly accepts the first-baseline
  phase transition.

## Limits

New Git baseline operations require the shared composition at its Git root.
Common-baseline monorepos are supported; independently composed nested contexts
retain existing package/discovery checks and use separate Git/manual baseline
procedures. Identity inspection explains unavailable computed identity rather
than attributing a parent snapshot to the nested project.

Matching baseline numbers and documentary evidence are necessary checks, not
proof of semantic impact or implemented coverage. Workflow markers cannot prove
truthful approval. Core checks do not obtain remote reviews, enforce a hosting
service's protection settings, or assign independently versioned application
releases. Cached Git refs do not claim current remote freshness.

Link checks are conservative file-target checks. Directory scope discovery and
index snapshots have explicit exclusions; subprojects/submodules may require
separate checks. Inventories omit empty directories, ownership, and permission
bits other than executable identity. Locks are not signatures. Transactions
provide ordinary-failure recovery, not power-loss atomicity or arbitrary-writer
isolation. Source archives use declared build metadata and honestly report
unavailable computed Git identity.

## Workflow State

Feature implementation and integration preparation are explicitly closed in
history. The separate release/integration workflow remains open. Its candidate
gates and actual outcomes belong in that workflow, without changing normative
specifications to describe operational progress. Closure, phase acceptance and
publication are separate evidenced decisions; bootstrapping remains unchanged.
