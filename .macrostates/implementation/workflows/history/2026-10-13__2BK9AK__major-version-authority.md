# Major version authority and CLI policy adoption

- Project phase: active
- Workflow type: Specification update; Implementation update (one adoption outcome)
- Status: completed
- Delivery state: accepted
- Change depth: targeted
- Branch: feature/major-version-authority
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com) - Repository-local Git identity and current conversation
- Implementer: Model: GPT-6; exact revision/effort: not exposed; agent: Codex; source: runtime instructions
- Started at: 2026-10-13 22:01:15 UTC
- Last updated at: 2026-10-13 22:01:15 UTC

## Original request and objective

The definer requested removing the separate approval requirement for Major version increases. Canonical Meta 3.0.0 and Process 5.1.0 implement that request through normal protected PRs and immutable releases. The definer explicitly chose “Update the CLI too” when asked whether to adopt those packages and add policy support. This workflow implements that approved CLI adoption and retains earlier selected-policy behavior.

## Scope and acceptance criteria

Explicitly support the unchanged technical Meta 3.0 and Process 5.1 policies, including initialization and baseline operations. Adopt exact released snapshots and regenerate the verified integrity lock. Align the local CLI specification, current implementation documentation and meaningful new/legacy/future-policy tests. Preserve official baselines and published tags during ordinary development. Record compatible specification and implementation impacts, coverage and original work provenance. Keep scope, workflow closure, reviewed integration, tagging/publication and phase consent distinct; removing the Major-number gate does not remove those requirements.

## Work done and evidence

Work starts from the finalized clean CLI 0.4.0 main snapshot fe6e36989b0a3c5c274b9fe2a03f7a7673ffff09, with specs-1.0.0 / imp-1.0.0 and active phase. New source behavior remains development until its separate reviewed release procedure completes.

## Remaining work

Implement the reviewed adapters and tests, adopt released copies, align specifications and current documentation, record change evidence and perform proportionate verification. Track integration and release preparation separately when their procedures begin. Request explicit closure with a short numbered summary of every open workflow once their actual local outcomes are ready.

## Blockers and unresolved questions

No unresolved architecture decision identified. Workflow closure and subsequent external integration/release outcomes are not inferred from this implementation request.

## Impact classification

The local CLI package is 2.0.0 and the pending project scope is Major/Major. The changed implementer-authority boundary and raised dependency minima reject earlier package compositions; this classification is not inferred solely from an upstream Major number. Reviewed release preparation aggregates once from specs-1.0.0 / imp-1.0.0 to specs-2.0.0 / imp-2.0.0. The independent Python application 0.5.0 retains compatibility with its public API and older selected-policy behavior. No separate Major-number approval is required. Ordinary feature declarations retain 1.0.0 until separate release preparation.

## Delivered implementation and verification

Explicit Meta 3.0 and Process 5.1 adapters now consistently govern initialization, internal baseline declaration reading and public baseline operations, preserving earlier selected policies and refusing unreviewed future ones. The CLI adopts exact released snapshots, local CLI 2.0.0 metadata and verified external inventories. Actual installation and locked reinstallation returned zero diagnostics. All 407 tests passed independently on Python 3.12.15, 3.13.16 and 3.14.7. Ruff lint/format across 117 files, Pyright, project/readiness and whitespace checks passed. The change record retains original finalized source fe6e369 and its 1.0.0 baselines, explicit Major/Major rationale, coverage/evidence and no gaps. The complete source remains an unmerged feature; no new stable application, baseline or workflow closure is claimed.

## Definer-confirmed closure

At 2026-10-14 00:23:44 Europe/Madrid (2026-10-13 22:23:44 UTC), Lucas Lopez explicitly replied “Close all three and finish the release” to the numbered petition naming policy adoption, release preparation and integration preparation. This confirms completion and scoped closure of this record, accepts its completed local outcome and authorizes archival. The user also explicitly authorizes finishing the reviewed CLI release through passing protected checks, normal integration, immutable tags and verified PyPI publication. No external result is claimed in advance. The existing active phase is unchanged; no separate Major-version consent is needed.
