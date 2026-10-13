# Versioning system implementation

- Project phase: bootstrapping
- Workflow type: Specification update; Implementation update (one definer-authorized outcome, scopes below)
- Status: completed
- Delivery state: accepted
- Change depth: systemic
- Branch: feature/versioning-system
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com) - Obtained from approved repository Git identity and current conversation
- Implementer: Model: GPT-6; exact revision/effort: not exposed; agent: Codex; source: runtime instructions
- Started at: 2026-10-13 12:14 UTC
- Last updated at: 2026-10-13 20:30 UTC

## Original request and objective

Implement the definer-approved baseline/development/change-record/release-preparation system across official packages and this CLI, preserving older projects and published identities. Add arbitrary Git-remote tagged specification downloads. Definers retain workflow closure authority; integration preparation asks for closure using a short numbered summary. The nine identified earlier delivered workflows were explicitly accepted for closure on 2026-10-13.

## Acceptance criteria

Implement prefixed specs/imp baselines, original development provenance and computed identities, committed independent impact records, integration and release planning/preparation/checks, explicit branch synchronization, independent deliverable declarations, optional manual equivalents, old-policy compatibility, and archive-safe application builds. Validate with meaningful temporary Git repositories, supported Python versions and artifact installations.

## Progress

Specification drafts and CLI implementation are complete locally in isolated feature branches across all ten repositories. They include independent specification/implementation baselines, immutable work origins, change records, integration and release gates, explicit synchronization, deliverable policies, and arbitrary tagged Git sources. Earlier accepted workflows are archived with their explicit closure evidence. At that local checkpoint the current workflow remained open; confirmed closure is recorded below.

Verification completed:

- All 393 tests pass independently on Python 3.12, 3.13, and 3.14.
- Formatting, lint, type checks, current-project conformance, and all repository whitespace checks pass.
- Clean wheel and source-distribution installs expose the expected application identity, public API, and commands. Both distribution metadata checks pass.
- CI workflow syntax checks pass.
- A publishable-file secret scan found no leaks.
- Temporary canonical snapshots with prospective metadata pass a dependency graph audit, 235 local link/anchor checks across 129 Markdown documents, fresh generic Git installation and locked reinstallation of all eight official packages, and the CLI's six-package selection. These are scratch-only snapshots, not real releases.

A final independent review found and corrected the application-only release continuation: immutable finalized baseline tags/plan/history are verified separately from later application metadata, evidenced no-impact records stay pending, and work-origin controls remain validated. The complete lifecycle and rejection cases pass; no new architecture decision remains.

At the pre-approval verification checkpoint, actual package versions, dependency minima, external self-selection, global baseline declarations, and annotated release tags remained unchanged. Application 0.4.0.dev0 is explicitly a local development build. No remote integration or publication has occurred.

## Remaining work

The requested source implementation, canonical releases and actual CLI self-adoption are complete and locally verified. Obtain explicit definer closure of this workflow and the related integration-preparation workflow, verify the closed committed source tree, and submit the authorized feature proposal. External CI and reviewed feature integration precede the separately tracked baseline/application release proposal. No new CLI baseline, phase acceptance or application publication is claimed.

## Version decision resolved

The definer explicitly approved the proposed versions and releases on 2026-10-13: the seven Major package targets, the CLI specs-1.0.0 / imp-1.0.0 release proposals, application 0.4.0, dependency adoption, integration through passing PRs, immutable Git tags and PyPI publication. The earlier pause is resolved. Workflow closure remains a separate request and is not inferred from this authorization. Canonical metadata, package releases and CLI adoption are complete. The separate CLI integrations and publication remain.

## Authorized specification scope

Update local CLI requirements and their metadata; deliberately adopt unchanged canonical releases, composition selections, integrity locks and approved version policy. Related canonical source-package work is published separately, not authored in the installed external copies.

## Authorized implementation scope

Implement the CLI/public API transport, origin/change/integration/release/synchronization/deliverable/migration/build behavior and align tests, CI and implementation documentation with the local requirements.

## Canonical release progress

Meta 2.2.0, Process 5.0.0, Repository 4.0.0, Python 2.1.1, Docker 3.0.0, Python-project 3.0.0, Python-library 2.0.0 and Android 5.0.0 are now integrated through their normal PRs and published as annotated tags on merged snapshots. Every prior remote tag was verified preserved. CLI adoption, locked reinstall and offline checks completed with zero diagnostics; no CLI feature integration, new global baseline, application publication or phase acceptance is claimed.

## Blockers and unresolved questions

No architecture blocker remains. Actual adoption and verification are complete. Obtain the separate definer closure decision before preparing the CLI proposal. Bootstrapping remains unchanged until explicit phase acceptance.

## Suggested next step

Present the two current workflows with their completed outcomes and request explicit closure before proposal preparation. Preserve bootstrapping. After closure, verify the proposed source, submit the feature PR and require remote checks before merging.

## Final local adoption evidence

Actual generic-Git installation and locked reinstall of Meta 2.2.0, Process 5.0.0, Repository 4.0.0, Python 2.1.1 and Python-library 2.0.0 passed with zero diagnostics. Local CLI 1.0.0 metadata uses current at_least minima. Offline project and change-readiness checks pass. [Original work](../../work/versioning-system.yaml) and [Major/Major change](../../changes/history/versioning-system.yaml) preserve the full original 96a467c448f6fc5abf3ca9f8b19a29d976725c93 provenance, requirements/evidence and no gaps. Existing annotated aliases and the original release date remain preserved.

All 393 tests passed again on Python 3.14 after actual adoption; the prior 3.12/3.13/3.14 matrix passed. Ruff/formatting of 114 files and Pyright pass. Rebuilt development wheel/sdist clean installations, public API/command/version probes, source-byte checks and strict Twine metadata checks pass. Semantic conformance and documentary review completed; external review/CI and closure remain separate gates. Related [integration preparation](2026-10-13__1RPQX8__integration-preparation.md) records final local source/target checks.

## Definer-confirmed closure

At 2026-10-13 20:30 UTC, Lucas Lopez explicitly approved closing both named workflows as completed in response to the numbered closure petition. This accepts the local implementation and integration-preparation outcomes and authorizes their archival. It does not grant first-baseline phase acceptance or close the later release-preparation workflow. External checks and the already authorized reviewed integration remain separate.
