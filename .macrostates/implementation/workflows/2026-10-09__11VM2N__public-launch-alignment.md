# Public launch alignment

- Workflow type: Specification update and implementation update
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: implementing
- Change depth: large
- Branch: release/public-launch-alignment
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), repository-local Git identity and this conversation.
- Implementer: Model GPT-6; exact identifier/revision and effort not exposed; agent Codex; source: session metadata.
- Started at: 2026-10-09 09:51 UTC
- Last updated at: 2026-10-09 09:51 UTC

## Original request

"cool, please do 1, 2 and 3 (make the repositories public first and then enable PR protection for this step)"

## Objective and scope

Support Meta 2.1 and Process 4.0/4.1 while retaining all earlier supported behavior; publish eight existing canonical main versions, adopt the verified release snapshots in the CLI, update fixtures/contracts and prepare CLI 0.3.0.

Preserve repository URLs, existing tags, old supported formats/policies and unrelated work. Do not publish to PyPI, change project phase, or close workflows without explicit confirmation.

## Version classification

CLI policy support is an additive public capability with retained old behavior. New composition and implementation contract: spec-0.3.0 / 0.3.0. Local CLI package: 0.5.0. The PR-only development rule was already explicitly requested by the definer; selecting its now-published policy does not introduce a new public API incompatibility. Upstream Major versions do not dictate the CLI's Major. Canonical package versions on main are already assigned and reviewed; release tagging changes no package bytes or dependency minimums.

## Work done

Reviewed current composition, code, current-main package policy differences and open records. This request explicitly authorizes the proposed latest-policy support and self-composition updates. Existing onboarding, AI disclosure and dependency-default records retain their original scopes and pending closure.

## Acceptance and validation

Verify the newest and previous release policies, unknown-policy refusal, modern-layout and declaration checks. Preserve all 45 existing package tags and all historical metadata fixtures. Validate real tagged package archives, own working/staged checks, Ruff/Pyright, supported-Python tests, wheel/sdist and installed library/command. Scan the proposed release. Check PR integration, remote tag identities, public visibility, main protection including administrators, and anonymous installation/setup.

## Remaining work

Implementation and publication checks, then definer acceptance and explicit closure.

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
  See [uv dynamic-metadata guidance](https://docs.astral.sh/uv/concepts/cache/#dynamic-metadata).
- Earlier fixtures retain all 45 published package metadata snapshots. The latest
  eight snapshots are additional fixtures, with unchanged numeric dependency
  minimums and authored at_least constraints.

Remaining technical steps: staged verification, release scan, PR/remote CI and
publication verification. No workflow closure or phase transition is implied.
