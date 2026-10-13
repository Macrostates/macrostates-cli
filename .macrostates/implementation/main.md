# Macrostates CLI Implementation

Project phase: active.

Current source prepares independent application version `0.5.0`, with development
state recorded in [application.yaml](application.yaml). The composition and
[release.yaml](release.yaml) retain finalized `specs-1.0.0` / `imp-1.0.0` during
ordinary feature work. The immutable 0.4.0 release identifies source
`fe6e36989b0a3c5c274b9fe2a03f7a7673ffff09`; its baselines, provenance and published
artifacts remain unchanged. New source is unreleased until its reviewed baseline
and application procedures complete.

## Current Behavior And Adoption

The console command and public Python API share project initialization,
installation, locking, inspection, structural checks and exact staged-index
checks. Git-based baseline operations capture work origins, record independent
change impacts and evidence, inspect optional applications, synchronize branches,
verify combined integration snapshots and prepare bound release candidates.

The current selection adopts released Meta 3.0.0 and Process 5.1.0 alongside
Repository 4.0.0, Python 2.1.1 and Python-library 2.0.0. The local CLI contract is
listed in its [package metadata](../specs/051_cli/package.yaml). External packages
remain unchanged tagged Git snapshots under the exact integrity lock. The new
policies retain the modern layouts and technical record formats. They remove the
separate Major-number consent requirement within authorized work; ordinary
workflow closure, integration, publication and scope authorization remain distinct.

Explicit adapters support Meta 3.0 and Process 5.1 without accepting unreviewed
future versions. Process capabilities consistently select initialization seeds,
record declarations and public baseline operations. Earlier selected policies
retain their original validation and source-format behavior. Major changes use
the existing impact/evidence aggregation; the CLI does not invent a Major-specific
permission token or automatically authorize any operation.

The [captured work origin](work/major-version-authority.yaml) retains finalized
starting commit and baselines. Pending scope and later consumed records live under
[changes](changes/). Current work and scoped acceptance belong to
[workflow records](workflows/); no historical closure grants this new scope.
The project's previously accepted active phase is preserved.

## Architecture

| Area | Implementation Responsibility |
| --- | --- |
| `_models.py` | Normalized package/composition models, public diagnostics, reports, and controlled errors |
| `_formats/` and `_io.py` | Explicit composition/metadata readers, strict YAML, field/path primitives, and retained formats |
| `_validation.py` | Metadata/dependency/link checks and explicit Meta 2.0/2.1/2.2/3.0 and Process 2.3/2.4/3.0/4.0/4.1/5.0/5.1 policy adapters |
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

[Specification conformance](specification-conformance.md) maps requirements to
implementation and verification. The new policy tests cover exact new selections,
initialization, Major release planning without a consent flag, retained closure
requirements, older policies and refusal of unreviewed future versions. Dated
results, package adoption and release checks belong to the current workflow;
new verification is not inferred from the previously released 393-test suite.

Structural checks cannot prove semantic classification, truthful consent or
requirement coverage. Cached refs do not establish current remote state. Final
proposal checks cover the actual combined tree, and required external checks
precede integration. Transactions recover ordinary failures but do not guarantee
power-loss atomicity or isolation from arbitrary external writes. Integrity locks
are reviewable baselines rather than signatures. Scope discovery and staged
snapshots have documented exclusions; separately composed subprojects and
submodules need their own review. Source archives honestly report unavailable
Git identity rather than inventing a release claim.
