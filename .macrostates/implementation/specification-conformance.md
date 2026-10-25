# CLI Specification Conformance

This map relates the current CLI contract to implementation and verification.
Composition, implementation declarations, application metadata and release plans
retain independent identity and provenance roles. Current qualification and
acceptance are recorded separately from historical observations.

## Policy Adoption And Compatibility

Process 6.0 keeps modern layouts, prefixed baseline schema 2 and record schema 1.
Its required public-document authoring contract replaces personal attribution and
conversational request records with roles and neutral objectives. The explicit
adapter must preserve earlier selected policies and reject unknown future ones.
Role-only workflow records keep all existing status and closure-evidence gates.
No general anonymity validator or automatic workflow closure is claimed.

## Contract Map

| Specification | Implementation | Evidence Or Required Check |
| --- | --- | --- |
| [Concepts](../specs/051_cli/001_concepts.md): identities, ownership, effects | `_project`, `_cli`, domain modules | Existing import/offline/command contracts and side-effect review; synchronization is the explicit Git-mutation exception |
| [Library](../specs/051_cli/002_library.md): root exports and public API | `__init__`, `_models`, `_project` | Existing public report/factory contracts; new Project API tests and signature review |
| Library generic/legacy source boundary | `_sources`, `_project` | `test_git_sources.py`, retained `test_sources.py`, injected providers, exact local Git tag/inventory checks |
| [Commands](../specs/051_cli/003_commands.md): flags, data, reports, errors | `_cli`, `_project` | Retained command contracts, `test_cli_versioning.py` flat-command/data/origin/option checks, and rebuilt development-artifact installed-command probes |
| [Composition](../specs/051_cli/004_composition.md): discovery, formats, paths, dependencies | `_formats`, `_io`, `_scopes`, `_validation` | Historical/current metadata fixtures, dependency/link/scope tests, generic source validation |
| [Integrity](../specs/051_cli/005_integrity.md): canonical snapshots and locks | `_integrity`, `_project`, `_sources` | Existing rollback/inventory tests; moved/lightweight/missing local tags, executable files, dirty-copy preservation |
| [Versioning](../specs/051_cli/006_versioning.md): selected-policy isolation | `_validation`, `_project` | Retained Process/Meta policy tests and Process 5/6 domain fixtures; unknown future policies fail explicitly |
| Versioning explicit migration | `_migration`, `_release` alias verification | `test_version_migration.py`: no implicit conversion, idempotence, source-only projects, primary refusal, preserved refs/history and invalid metadata |
| Versioning application/build source separation | `_build_version`, application declaration, pyproject, manifest | `test_application_build.py`, retained `test_build_version.py`, rebuilt development wheel/sdist clean installs, shipped-source bytes and Twine metadata checks |
| [Development](../specs/051_cli/008_development-and-releases.md): captured work and explicit impact | `_changes`, `_versioning`, `_project` | Domain record/identity tests and original-origin review; explicit late capture and work references |
| Development application/default inspection | `_deliverables`, `_project` | `test_deliverables.py`: independent Python versions, Android default/code, historical provenance, ordering and malformed metadata |
| Development synchronization and primary guards | `_git`, `_sync` | `test_integration_sync.py`: merge/rebase, full refs, main/master/custom primary, dirty/detached/active state, explicit fetch and preserved conflicts |
| Development closure requests/history gates | `_integration` | Open/closed statuses, confirmation evidence, index-renaming refusal, archived records and no automatic closure |
| Development exact combined readiness | `_integration`, project/domain checks | Explicit scope records, inherited target workflows, gaps, merge conflicts, stale expected/during-check targets |
| Development release plans/preparation | `_release`, `_versioning`, `_mutations` | `test_release_records.py`: aggregation, explicit target refs, commit/tree/record binding, candidate/history checks and retained baseline plans/tags for metadata-only application release |
| Development release identity/publication checks | `_release`, `_deliverables` | `test_deliverable_sources.py`: declared source tags/commits, agreement, source declarations/baselines and custom-source manual warnings; final artifacts and external authorization remain separate |
| [Verification](../specs/051_cli/007_verification.md) | Contributor tooling, tests, build and CI | Run the full supported Python matrix, canonical install/reinstall, offline checks, Ruff, formatting and Pyright; retain actual reviewed results and separate candidate/external release evidence |
| [Recovery](../specs/051_cli/annex_recovery.md) | Transport, synchronization, migration and replacement boundaries | Preserved package edits/conflicts/provenance, stale plans, markers/recovery-data review |

## Current Adoption Coverage

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Explicit Process 6 technical capability | Registered policy adapter and shared prefixed-baseline capability | New selection, initialization and public baseline-operation tests |
| Role attribution without identity lookup | Existing documentary workflow/status handling | Synthetic role-only closure and no-identity-lookup cases |
| Closure authority remains required | Existing integration workflow/history gates | Missing and present authorization cases |
| Prior policies remain supported | Retained adapters and historical formats | Regression suite and future-policy refusal |
| Canonical self-adoption | Exact released composition selection and verified lock | Source installation, locked restoration and offline checks |
| Public document output handling | Selected Process contract and local authoring/output guidance | Reviewed synthetic acceptance matrix and current/historical document inspection |
| Honest historical evidence | Anonymized historical workflow summaries | Unchanged measurements, dates and acceptance/closure state; unavailable evidence marked |

Current source tests and document review do not retroactively rerun historical
checks. Edited historical summaries remain explicit summaries of old observations.
Consumed technical records, original work origins and immutable baseline/source
provenance retain their original identities.

Actual allowlisted adoption results are retained in the
[qualification receipt](validation/public-document-adoption.json). It distinguishes
executed checks from reviewed synthetic acceptance conditions.

## Qualification And Release Gates

Run affected tests, the complete supported regression matrix and static checks.
Verify package metadata, local links, canonical inventories, staged contents and
combined integration readiness. Candidate qualification additionally verifies
bound release inputs, source fingerprint, rebuilt distributions, clean installed
behavior and archive rebuilding without Git. Retain reviewed allowlisted results
with relative paths; do not save raw logs or private intermediate editions.

## Limits

The CLI checks documentary status, declared coverage and technical consistency.
It cannot establish semantic anonymity, truthful approval or complete conformance.
Before retaining reports, the implementer reviews required fields, names, keys,
values and embedded content in memory under Process. Full anonymity needs semantic
review, including ignored outputs and nested archives. External checks, accepted
closure, reviewed integration and publication each retain their own authority.
