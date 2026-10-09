# Public launch integration

- Workflow type: Development branch merge
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Change depth: large
- Branch: release/public-launch-alignment
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), repository-local Git identity and this conversation.
- Implementer: Model GPT-6; exact identifier/revision and effort not exposed; agent Codex; source: session metadata.
- Started at: 2026-10-09 09:51 UTC
- Last updated at: 2026-10-09 10:35 UTC

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

All requested release, visibility, protection and anonymous-access work is delivered. Definer acceptance and explicit workflow closure remain. Publication evidence is being integrated through a documentation-only PR; no product version change.

## Blockers

None. Private-repository protection becomes available after the explicitly authorized visibility change.

## Delivered release and integration

- [Release PR 2](https://github.com/Macrostates/macrostates-cli/pull/2) merged as
  040585e1c50f1e3d899a6f86732912df33858af0. Its tree exactly matches the reviewed
  candidate. [Main CI passed all three Python versions](https://github.com/Macrostates/macrostates-cli/actions/runs/37916640563).
- Published annotated spec-0.3.0 and v0.3.0 tags on that merged release commit.
  [CLI release](https://github.com/Macrostates/macrostates-cli/releases/tag/v0.3.0)
  supplies the fixed installation revision; no PyPI publication occurred.
- Published all eight canonical releases with GitHub release notes: Meta 2.1.0,
  Process 4.1.0, Repository 3.1.0, Docker/Python/Python-project 2.1.0,
  Python-library 1.1.0 and Android-app 4.1.0. All 45 earlier tags are unchanged.
- Made each of the nine product repositories public, then immediately enabled
  main protection for that repository. Verified the already-public profile too.
  All ten require PRs and include administrators, with no PR bypass actors,
  force pushes or main deletion. Zero approving reviews permit solo maintenance.
- The CLI additionally requires passing check (3.12), check (3.13) and
  check (3.14), with an up-to-date branch. Other repositories have no CI checks.

## Anonymous public verification

Removed GitHub token variables, suppressed authenticated GitHub CLI lookup and
isolated Git configuration for the test process without changing the real login.
The README's Git installation at v0.3.0 succeeds in an isolated Python 3.12 tool
environment and reports macrostates 0.3.0. The default downloader has no token.
Fresh CLI init/install/check passes against all eight actual public release
archives; the public Python library checks that same composition successfully.
A real Meta 2.0.2/Process 3.0.2 selection still installs and checks, then an explicit
update to Meta 2.1.0/Process 4.1.0 installs and checks with the protected inventory.
These are structural/integrity checks, not a claim of application semantics.

A request with no Authorization header receives a public repository response
with the anonymous rate limit of 60 and private=false. The public organization
homepage returns HTTP 200 and contains its start-project prompt and package/CLI
links. No credentials, raw repository API captures or machine paths are published
as verification evidence.

The follow-up delivery record changes tracking only. Implementation 0.3.0,
composition spec-0.3.0, the local CLI package 0.5.0, imported archives and all
published release tags remain unchanged. No primary-branch file edits or pushes
were used. Project phase and workflow closure remain separate definer decisions.
