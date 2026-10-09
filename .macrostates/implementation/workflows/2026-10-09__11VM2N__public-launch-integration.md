# Public launch integration

- Workflow type: Development branch merge and release publication
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

Validate, submit and merge the CLI PR to publish the aligned release; create annotated CLI implementation/composition tags; make all nine product repositories public and immediately enable PR protection for main; verify anonymous public onboarding.

Preserve repository URLs, existing tags, old supported formats/policies and unrelated work. Do not publish to PyPI, change project phase, or close workflows without explicit confirmation.

## Version classification

CLI policy support is an additive public capability with retained old behavior. New composition and implementation contract: spec-0.3.0 / 0.3.0. Local CLI package: 0.5.0. The PR-only development rule was already explicitly requested by the definer; selecting its now-published policy does not introduce a new public API incompatibility. Upstream Major versions do not dictate the CLI's Major. Canonical package versions on main are already assigned and reviewed; release tagging changes no package bytes or dependency minimums.

## Work done

The definer explicitly requested review steps 1, 2 and 3, including making repositories public before configuring their protection. Delivery includes an integrated, tagged CLI implementation, using a PR rather than a main push. Existing published package tags must remain unchanged.

## Acceptance and validation

Verify the newest and previous release policies, unknown-policy refusal, modern-layout and declaration checks. Preserve all 45 existing package tags and all historical metadata fixtures. Validate real tagged package archives, own working/staged checks, Ruff/Pyright, supported-Python tests, wheel/sdist and installed library/command. Scan the proposed release. Check PR integration, remote tag identities, public visibility, main protection including administrators, and anonymous installation/setup.

## Remaining work

Implementation and publication checks, then definer acceptance and explicit closure.

## Blockers

None. Private-repository protection becomes available after the explicitly authorized visibility change.
