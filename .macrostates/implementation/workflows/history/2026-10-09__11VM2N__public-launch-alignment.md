# Public launch alignment

Anonymized historical summary. Dates, recorded states and measurements are retained historical observations. This rewrite does not rerun checks or grant acceptance. Commit IDs and artifact fingerprints describe the original observed sources or artifacts, not this edited document. Omitted evidence locations are unavailable through this summary; no substitute evidence is invented.

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: completed
- Delivery state: accepted
- Change depth: large
- Branch: release/public-launch-alignment
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-09 09:51 UTC
- Last updated at: 2026-10-09 10:35 UTC

## Technical objective and scope

Prepare compatible CLI policy support and verified canonical snapshot adoption for implementation 0.3.0 and specification spec-0.3.0. Preserve prior formats, releases and authorization boundaries.

## Objective and scope

Support Meta 2.1 and Process 4.0/4.1 while retaining all earlier supported behavior; publish eight existing canonical main versions, adopt the verified release snapshots in the CLI, update fixtures/contracts and prepare CLI 0.3.0.

Preserve repository URLs, existing tags, old supported formats/policies and unrelated work. Do not publish to PyPI, change project phase, or close workflows without explicit confirmation.

## Version classification

CLI policy support is an additive public capability with retained old behavior. New composition and implementation contract: spec-0.3.0 / 0.3.0. Local CLI package: 0.5.0. The PR-only development rule was already applicable; selecting its now-published policy does not introduce a new public API incompatibility. Upstream Major versions do not dictate the CLI's Major. Canonical package versions on main are already assigned and reviewed; release tagging changes no package bytes or dependency minimums.

## Work done

Reviewed current composition, code, current-main package policy differences and open records. The authorized scope includes latest-policy support and self-composition updates. Existing onboarding, AI disclosure and dependency-default records retain their original scopes and pending closure.

## Acceptance and validation

Verify the newest and previous release policies, unknown-policy refusal, modern-layout and declaration checks. Preserve all 45 existing package tags and all historical metadata fixtures. Validate real tagged package archives, own working/staged checks, Ruff/Pyright, supported-Python tests, wheel/sdist and installed library/command. Scan the proposed release. Check PR integration, remote tag identities, public visibility, main protection including administrators, and anonymous installation/setup.

## Recorded pre-closure gates

Code, package adoption and local checks are delivered. Integration/publication is tracked separately. Definer acceptance and explicit closure remain.

## Blockers

None. Private-repository protection becomes available after the explicitly authorized visibility change.

## Local validation and release preparation

- Published all eight reviewed main package versions as annotated tags. Verified
  their remote object/commit identities and preserved all 45 earlier tags.
- Adopted the latest five applicable canonical packages through the protected
  production installer. The new self-composition and inventory check pass.
- All 190 tests pass on Python 3.14.7, and from the installed wheel in isolated
  Python 3.12.15 and 3.13.16 environments with locked dependencies.
- Ruff lint/format and Pyright pass. Built wheel and sdist in isolation; the wheel
  was built from that sdist and reports implementation 0.3.0.
- Reproduced stale development version metadata because the release declaration
  was outside uv's default cache inputs. Explicit release/README cache keys fix
  rebuilding after declaration changes; no contributor dependency version changed.
  See uv dynamic-metadata guidance (external evidence location omitted).
- Earlier fixtures retain all 45 published package metadata snapshots. The latest
  eight snapshots are additional fixtures, with unchanged numeric dependency
  minimums and authored at_least constraints.

The exact staged self-check and whitespace check pass. The complete staged tree,
wheel and sdist have zero Gitleaks findings. Implementation commit 055d18208be3acf9d0af1ec803142862caa1e6f4
passed GitHub CI on all three Python versions (external evidence location omitted).
This delivery record changes tracking only; the validated implementation and
specification contract remain unchanged. Integration and public setup continue
in the separate launch integration workflow. No workflow closure or phase
transition is implied.

## Definer-confirmed closure

The Definer explicitly confirmed acceptance and closure for this workflow's recorded technical scope. This preserves the existing closed state; it does not grant new acceptance or publication authority.

Historical confirmation dates: 2026-10-13.
