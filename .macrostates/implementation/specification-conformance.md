# CLI Specification Conformance

This review maps the current local CLI contract and reviewed policy adoption to
source and verification. The composition, [implementation declaration](release.yaml),
[application declaration](application.yaml) and [bound release plan](release-plan.yaml)
retain their distinct identity and provenance roles. Read the
[implementation entrypoint](main.md) for current source, phase and delivery state.

## Policy Adoption And Compatibility

The selected released Meta 3.0.0 and Process 5.1.0 use the existing modern layouts,
composition format 1, prefixed implementation declaration schema 2 and Process
record schema 1. Both clarify impact-based Major assignment within authorized
work. No Major-specific approval flag is introduced. The implementer still
reviews intent and compatibility, and workflow closure, reviewed integration,
publication and scope authorization remain independent requirements.

Explicit adapters preserve earlier Meta/Process policies and reject unreviewed
future versions. Initialization seeds, declaration readers and new public baseline
operations share the reviewed prefixed-baseline capability. Package contents and
provenance remain immutable external releases; metadata owns dependencies.

## Contract Map

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
| [Verification](../specs/051_cli/007_verification.md) | Contributor tooling, tests, build and CI | All 407 tests pass on Python 3.12/3.13/3.14 after actual adoption; canonical install/reinstall, offline/readiness, Ruff/formatting and Pyright pass; candidate artifacts and external checks have separate release evidence |
| [Recovery](../specs/051_cli/annex_recovery.md) | Transport, synchronization, migration and replacement boundaries | Preserved package edits/conflicts/provenance, stale plans, markers/recovery-data review |

## Current Adoption Coverage

| Requirement | Implementation | Verification |
| --- | --- | --- |
| Meta 3.0 keeps the modern technical policy while removing separate Major consent | Explicit Meta 3.0 adapter and unchanged canonical released package | New selection/schema/layout tests, canonical snapshot/lock verification and semantic review |
| Process 5.1 keeps schema-2 baselines and new operations | Explicit Process 5.1 adapter with consistent initialization, declaration and method gates | Initialization and baseline-operation tests with the new policy |
| Major impact is classified without a new permission gate | Existing change records, aggregation and release planning | Major plan coverage without consent field; required evidence and workflow closure still checked |
| Previous selected policies remain supported | Retained explicit adapters and historic formats | Regression fixtures and earlier-policy tests |
| Unknown future policies are refused | Explicit reviewed policy registration | Future Meta/Process refusal tests beyond the newly supported versions |
| CLI self-adoption uses exact immutable releases | Composition sources and verified inventory lock | Actual generic Git install, locked reinstall and offline project checks |

The [original work record](work/major-version-authority.yaml) preserves the full
starting commit and baselines. [Change records](changes/) preserve impact,
requirements, evidence and original provenance before and after consumption.
[Workflows](workflows/) preserve dated verification and actual scoped closure.
Previously released source and provenance stay in immutable tags and historical
records; they do not provide automatic acceptance of the current work.

## Verification And Release Gates

Run affected policy tests and the complete regression suite, static checks,
package integrity and exact staged/combined-tree gates. Candidate release checks
must cover bound inputs, original and consumed record bytes, baseline relation,
source fingerprint and the exact current target. Clean wheel and source-distribution
installation and strict metadata checks verify independent application builds.
Required external checks and normal reviewed integration precede immutable tags
and application publication. Do not infer workflow consent from passing checks.

## Limits

The CLI verifies documentary states, declared coverage, technical consistency and
source provenance; it cannot prove semantic compatibility, truthful consent or
adequate implementation coverage. Core operations do not enforce hosting-service
reviews or branch protection, and cached refs do not prove freshness. Shared
baseline operations require the composition at its Git root. Independently
composed nested contexts retain their own package checks and release procedures.
Application policies and separately released applications need their own evidence.
Transactions provide ordinary-failure recovery rather than crash atomicity.
