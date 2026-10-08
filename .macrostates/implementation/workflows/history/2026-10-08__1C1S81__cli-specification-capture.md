# CLI specification capture

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: completed
- Change depth: substantive
- Branch: main
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), supplied in this conversation.
- Implementer: Codex — GPT-6; exact revision and effort not exposed.
- Started at: 2026-10-08 12:49 UTC
- Last updated at: 2026-10-08 13:00 UTC

## Request and scope

Inspect the CLI and supported Python library in detail; replace the monolithic
local CLI specification with several coherent behavior-oriented documents.
Capture observable implemented behavior while leaving private implementation
choices to implementers. Verify agreement between specification and code.
After verification, close all open workflows in this CLI project, commit and
push this repository. The definer explicitly authorizes that conditional closure
for this identified set, including this request's workflow; no further closure
confirmation is required. Other repositories and external workflow records are
outside scope. Baseline acceptance and project phase are distinct from closure.

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

## Remaining work

No product specification/implementation gap remains in this request. Baseline
acceptance is a distinct phase decision and is not inferred from workflow closure.


## Authorized closure

Closed at 2026-10-08 13:00 UTC under the definer's explicit instruction:
“you can then close all open workflows in the cli project and commit and push
the repository.” The identified set is all four open CLI-project records,
including specification capture. Earlier delivery evidence was reviewed, and
current conformance verification passed before closure. Earlier statements about
open related workflows describe their historical state; this closure supersedes
that tracking state. No external workflow record is closed.

Workflow closure is distinct from accepting the first implementation baseline;
project phase remains bootstrapping pending that separate decision.
