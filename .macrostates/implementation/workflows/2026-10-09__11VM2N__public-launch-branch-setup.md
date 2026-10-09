# Public launch branch setup

- Workflow type: Development branch creation
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Change depth: medium
- Branch: release/public-launch-alignment
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), repository-local Git identity and this conversation.
- Implementer: Model GPT-6; exact identifier/revision and effort not exposed; agent Codex; source: session metadata.
- Started at: 2026-10-09 09:51 UTC
- Last updated at: 2026-10-09 09:51 UTC

## Original request

"cool, please do 1, 2 and 3 (make the repositories public first and then enable PR protection for this step)"

## Objective and scope

Establish an isolated branch for the authorized CLI release alignment.

Preserve repository URLs, existing tags, old supported formats/policies and unrelated work. Do not publish to PyPI, change project phase, or close workflows without explicit confirmation.

## Version classification

CLI policy support is an additive public capability with retained old behavior. New composition and implementation contract: spec-0.3.0 / 0.3.0. Local CLI package: 0.5.0. The PR-only development rule was already explicitly requested by the definer; selecting its now-published policy does not introduce a new public API incompatibility. Upstream Major versions do not dictate the CLI's Major. Canonical package versions on main are already assigned and reviewed; release tagging changes no package bytes or dependency minimums.

## Work done

Created release/public-launch-alignment from origin/main 4832b9efa2385ea447641113222d279c3c1ced31. Clean working tree; no unrelated changes transferred. Starting composition spec-0.2.3 and implementation 0.2.0. Setup delivered; related implementation and merge records share this creation prefix.

## Acceptance and validation

Verify the newest and previous release policies, unknown-policy refusal, modern-layout and declaration checks. Preserve all 45 existing package tags and all historical metadata fixtures. Validate real tagged package archives, own working/staged checks, Ruff/Pyright, supported-Python tests, wheel/sdist and installed library/command. Scan the proposed release. Check PR integration, remote tag identities, public visibility, main protection including administrators, and anonymous installation/setup.

## Remaining work

Definer acceptance and explicit closure only for branch setup.

## Blockers

None. Private-repository protection becomes available after the explicitly authorized visibility change.
