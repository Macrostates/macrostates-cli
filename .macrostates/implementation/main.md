# Macrostates CLI Implementation

Project phase: active.

Current source develops application version `0.6.0.dev0`, recorded in
[application.yaml](application.yaml). The specification and implementation
numbers remain the last finalized `specs-2.0.0` and `imp-2.0.0` while this work
is pending. A later reviewed release plan will select new candidate baselines.
Published releases and their exact source provenance remain unchanged.

## Current Behavior And Adoption

The command and public Python API share package composition, source installation,
integrity, structural verification, captured work origins, change evidence,
branch synchronization, combined integration and baseline release operations.
The new work adds explicit Process 6 policy support while retaining older selected
policies and refusing unreviewed future families. Process 6 keeps the technical
baseline formats and changes document authoring to neutral roles, self-contained
technical objectives, safe evidence retention and scoped historical cleanup.

The selected composition adopts the published canonical Process 6.0.0 snapshot
through source installation and verified provenance. Meta 3.0.0,
Repository 4.0.0, Python 2.1.1 and Python-library 2.0.0 remain selected. The local
CLI contract records the new policy minimum and output-retention boundaries.
External package copies and lock inventories must match their exact releases.

Current work is captured in [its original provenance](work/public-document-authoring.yaml).
It does not inherit closure authorization from earlier completed work. Historical
workflow summaries are anonymized without changing observed acceptance, closure,
measurements or qualification limits. Original released source remains in its
existing immutable commits and tags; no published Git history is rewritten.
The project's previously accepted active phase is preserved.

## Architecture

| Area | Implementation Responsibility |
| --- | --- |
| `_models.py` | Normalized package/composition models, public diagnostics, reports, and controlled errors |
| `_formats/` and `_io.py` | Explicit composition/metadata readers, strict YAML, field/path primitives, and retained formats |
| `_validation.py` | Metadata/dependency/link checks and explicit Meta 2.0/2.1/2.2/3.0 and Process 2.3/2.4/3.0/4.0/4.1/5.0/5.1/6.0 policy adapters |
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

Core project/versioning operations have no hosting API dependency. Reviews,
branch protection, CI scheduling and artifact distribution use repository and
application procedures. The existing trusted-publisher workflow verifies the
application tag, linked baselines, source completeness and publication readiness,
then builds, tests and uploads the same verified artifact set. Its existing
publisher identifiers are preserved.

Ordinary imports have no project/network/subprocess side effects. Explicit
version access uses installed distribution metadata. Git synchronization only
fetches or changes history when requested. Checks and planning do not commit,
close workflows, tag, submit proposals or publish.

## Build And Release Identity

[Composition](../specs/composition.yaml) owns the specification baseline;
[release.yaml](release.yaml) identifies implementation and exact implemented
specification. [Application metadata](application.yaml) independently supplies
the Python distribution version. Development source uses a development identity;
prepared or finalized builds bind their shipped inputs with a verified fingerprint.
Published tags and distributions remain immutable.

The standalone build reader validates version, state, baseline relation, date and
candidate fingerprint. Shipped inputs include README, license, pyproject,
manifest, implementation release declaration and package source bytes/executable
identity. The application declaration itself and unshipped specification/workflow
documents are excluded to avoid a self-hash. Source archives rebuild without Git,
installed specification snapshots or release lookup. Ordinary builds never finalize,
allocate, tag or publish.

## Extension And Compatibility

See [versioned format adapters](decisions/0001-versioned-format-adapters.md) and
[modern adoption](decisions/0002-modern-package-adoption.md) for earlier decisions.
New policies and formats receive explicit adapters and regression coverage.
Unknown future policies fail clearly. Existing public commands, APIs, legacy
formats and old release policies remain supported. Migrations are explicit and
preserve published provenance. The application's 0.x version does not justify
silently breaking documented interfaces.

## Verification And Limits

[Specification conformance](specification-conformance.md) maps the current contract
to implementation and qualification. New policy coverage must include Process 6
initialization and baseline operations, role-only workflows without identity
lookup, preserved closure gates, retained earlier policies and future-policy
refusal. Applicable tests and static/package checks must complete before delivery
is described as qualified. Dated results belong in the current workflow and
reviewed verification receipt.

Structural checks cannot establish semantic anonymity, truthful consent or
requirement coverage. CLI results may contain operator-supplied names or paths;
select necessary fields and review them in memory before retaining evidence.
Never write an unreviewed raw output edition. Document scans support semantic
review and do not guarantee that indirect identifiers are absent.

Cached refs do not establish remote freshness. Combined-tree checks and required
external reviews precede integration. Ordinary-failure rollback does not promise
crash atomicity. Historical workflow anonymization does not requalify old results
or rewrite exact baseline declarations, consumed change records, tags or packages.

## Current Workflow Acceptance

Current work remains in progress and its workflow is open. Completion, acceptance,
closure, integration and publication remain distinct. Closure requires explicit
Definer authorization; no new acceptance or successful release is inferred from
historical summaries or passing structural checks.
