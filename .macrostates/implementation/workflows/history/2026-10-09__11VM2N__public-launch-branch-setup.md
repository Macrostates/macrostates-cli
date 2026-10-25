# Public launch branch setup

Anonymized historical summary. Dates, recorded states and measurements are retained historical observations. This rewrite does not rerun checks or grant acceptance. Commit IDs and artifact fingerprints describe the original observed sources or artifacts, not this edited document. Omitted evidence locations are unavailable through this summary; no substitute evidence is invented.

- Workflow type: Development branch creation
- Project phase: bootstrapping
- Status: completed
- Delivery state: accepted
- Change depth: medium
- Branch: release/public-launch-alignment
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-09 09:51 UTC
- Last updated at: 2026-10-09 09:51 UTC

## Technical objective and scope

Establish an isolated release-alignment branch from the recorded primary baseline without transferring unrelated edits, changing versions or claiming integration.

## Objective and scope

Establish an isolated branch for the authorized CLI release alignment.

Preserve repository URLs, existing tags, old supported formats/policies and unrelated work. Do not publish to PyPI, change project phase, or close workflows without explicit confirmation.

## Version classification

CLI policy support is an additive public capability with retained old behavior. New composition and implementation contract: spec-0.3.0 / 0.3.0. Local CLI package: 0.5.0. The PR-only development rule was already applicable; selecting its now-published policy does not introduce a new public API incompatibility. Upstream Major versions do not dictate the CLI's Major. Canonical package versions on main are already assigned and reviewed; release tagging changes no package bytes or dependency minimums.

## Work done

Created release/public-launch-alignment from origin/main 4832b9efa2385ea447641113222d279c3c1ced31. Clean working tree; no unrelated changes transferred. Starting composition spec-0.2.3 and implementation 0.2.0. Setup delivered; related implementation and merge records share this creation prefix.

## Acceptance and validation

Verify the newest and previous release policies, unknown-policy refusal, modern-layout and declaration checks. Preserve all 45 existing package tags and all historical metadata fixtures. Validate real tagged package archives, own working/staged checks, Ruff/Pyright, supported-Python tests, wheel/sdist and installed library/command. Scan the proposed release. Check PR integration, remote tag identities, public visibility, main protection including administrators, and anonymous installation/setup.

## Recorded pre-closure gates

Definer acceptance and explicit closure only for branch setup.

## Blockers

None. Private-repository protection becomes available after the explicitly authorized visibility change.

## Definer-confirmed closure

The Definer explicitly confirmed acceptance and closure for this workflow's recorded technical scope. This preserves the existing closed state; it does not grant new acceptance or publication authority.

Historical confirmation dates: 2026-10-13.
