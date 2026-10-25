# CLI specification capture

Anonymized historical summary. Dates, recorded states and measurements are retained historical observations. This rewrite does not rerun checks or grant acceptance. Commit IDs and artifact fingerprints describe the original observed sources or artifacts, not this edited document. Omitted evidence locations are unavailable through this summary; no substitute evidence is invented.

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: completed
- Change depth: substantive
- Branch: main
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-08 12:49 UTC
- Last updated at: 2026-10-08 13:00 UTC

## Technical objective and scope

Describe the existing public CLI and library behavior in a multi-document local specification. Separate observable contracts from implementation choices, verify conformance and preserve the existing runtime and canonical dependency snapshots.

## Plan and acceptance

Inspect public API, commands, composition/metadata/lock formats, source transport,
integrity transactions, version policies, tests and existing documentation.
Reorganize the local specification with a clear reading order and concrete
public contracts; keep internal algorithms and historical evidence in
implementation documentation. Record a conformance map, run relevant checks,
then archive completed records with explicit closure evidence and publish.

## Version classification

Local package 0.2.0 → 0.3.0: compatible clarification of existing public
behavior under Meta. Composition spec-0.2.0 → spec-0.2.1: specification
restructuring with no effective product contract change under Process.
Implementation remains 0.2.0; release baseline remains exactly spec-0.2.0.
External package selections and verified inventories remain untouched.

## Delivered and verified

Replaced the one-file local contract with seven core topic documents, a concise
README reading order and a recovery annex. Topics cover concepts, public library,
commands/JSON/exits, discovery/composition, installation/integrity, independent
version identities and verification expectations. Added an implementation-owned
conformance map after detailed source/test/build/CI review. Corrected ambiguous
locked-install wording; no runtime correction was needed.

- 140 tests pass independently on Python 3.12.15, 3.13.16 and 3.14.7.
- Ruff lint/format and Pyright pass; working-tree CLI check has no diagnostics.
- Additional public API probes pass: all exports, immutable Diagnostic,
  mutable Report and warning semantics, explicit version metadata, factory
  signature, mapping preservation, offline local operations, inspection fields,
  CLI flags on either side, human/JSON/usage results and reread configuration.
- Explicit empty authentication suppresses environment/CLI fallback.
- Legacy missing orders warn; incomplete format-1 orders fail before files appear.
- No source, test, dependency, build or external package contents changed.
  Prior isolated build/wheel and real canonical-source evidence remains applicable
  and is preserved in the earlier history records.

- The previously built independent Python 3.12 installed-wheel environment also
  passes all 140 tests and verifies the new self-composition with unchanged
  runtime version 0.2.0.
- All 49 local documentation links in the changed specification/implementation
  context and repository README resolve. Four records are completed in history;
  no open CLI workflows remain. Working integrity checks verify external copies.
- Final exact staged self-check and whitespace validation passed. Commit/push
  and remote CI verification are the final publication steps authorized by the
  definer; no runtime/package release is created.

## Recorded pre-closure gates

No product specification/implementation gap remained in this scope. Baseline
acceptance is a distinct phase decision and is not inferred from workflow closure.

## Definer-confirmed closure

The Definer explicitly confirmed closure for this workflow's recorded technical scope. Acceptance remains limited to the distinctions already recorded below. This preserves the existing closed state; it does not grant new acceptance or publication authority.

Historical confirmation dates: 2026-10-08 13:00 UTC.
