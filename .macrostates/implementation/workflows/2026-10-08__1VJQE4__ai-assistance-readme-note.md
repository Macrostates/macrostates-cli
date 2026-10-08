# AI assistance README note

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Branch: main
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), supplied in this conversation.
- Implementer: Codex, GPT-6; exact revision and effort not exposed.
- Started at: 2026-10-08 17:21 UTC
- Last updated at: 2026-10-08 17:30 UTC

## Original request and scope

“maybe just make a note in readme, short one, about the AI aided”

Add a brief factual note to the eight specification repository READMEs, the CLI
README and the organization profile README: “This project was developed with AI
assistance.” This is disclosure, not a new contribution policy, a claim of human
line-by-line review, commit attribution rewriting or a license change.

## Related publication work

The public-onboarding patch releases are already published. Preserve those tags;
new README contents receive another editorial package Patch. The dependency
synchronization workflow will adopt the final releases instead of the intermediate
ones. Its uncommitted CLI composition/local package bumps remain one coherent
change set. Organization profile changes have no package dependencies/version.

## Validation and acceptance

Check exact note wording, existing links, compatible metadata/dependencies,
release identities, retained fixtures, protected canonical self-install and
working/staged checks. Verify published README contents. Explicit closure remains
separate from delivery; the new request does not close workflows.

## Delivered

Added the exact one-sentence AI note to ten READMEs: eight specification package
entrypoints, the CLI README and the organization profile. The profile is pushed
at commit 1df20b0. This factual disclosure adds no contribution attribution policy,
model badge, human line-by-line review claim or license change. Package Patch
releases include the note; the [dependency workflow](2026-10-08__1V3M9F__public-onboarding-and-dependencies.md) adopts their
latest metadata, snapshots and verified lock.

## Final package releases

meta v2.0.2, process v3.0.2, repository-1 v2.0.2, docker-1 v2.0.2, python-1 v2.0.2, python-project-1 v2.0.2, python-library-1 v1.0.2, android-app-1 v4.0.2.

## Validation

- Final 156 tests pass on Python 3.12.15, 3.13.16 and 3.14.7.
- The independent installed Python 3.12 wheel environment passes the same 156
  tests and completes protected init/install/check and upgrade against all eight
  actual tagged GitHub archives. Resolved commit identities match published tags.
- Ruff lint/format and Pyright pass. CLI working and exact staged checks pass.
- All 15 canonical package dependency edges and three local CLI edges reference
  the latest final releases; required and optional constraints are retained.
- All 99 local package document links/anchors validate. Existing/intermediate
  tag object identities are preserved: 37 tags before the final wave.
- Package and final CLI staged secret scans report zero findings. Whitespace
  checks pass; final tracked snapshots have no unexplained integrity differences.
- No runtime source, build declaration, build configuration or contributor
  dependency lock changes. Runtime 0.2.0 and its exact spec-0.2.0 release baseline
  remain unchanged. CLI local package is 0.3.1; composition is spec-0.2.2.

## Publication verification

Published CLI commit 8ff6f6dd89995d5e5ec1abbccad5456f366e6ad7. Live GitHub API reads confirm
all eight final package versions/dependencies, the CLI composition, public HTTPS
setup text and all ten README disclosures. Package repositories retain their
private visibility and MIT licenses; profile content is public.
[GitHub CI](https://github.com/Macrostates/macrostates-cli/actions/runs/37816784942) passed Python 3.12, 3.13 and 3.14 for the published
change. Both working-tree and exact staged self-checks pass after publication.
A follow-up documentation commit records this evidence without changing the
implementation, specification versions, package snapshots or existing tags.

## Remaining work

Definer acceptance and explicit workflow closure. No requested content,
dependency or publication work remains. No workflow was closed by these requests;
earlier closed records remain in history.
