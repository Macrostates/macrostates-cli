# Public onboarding and CLI specification synchronization

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Change depth: coordinated editorial update
- Branch: main
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), supplied in this conversation.
- Implementer: Codex, GPT-6; exact revision and effort not exposed.
- Started at: 2026-10-08 17:13 UTC
- Last updated at: 2026-10-08 17:30 UTC

## Original request

Make the public onboarding documentation changes recommended in the readiness
review and update every repository's specification dependencies to the latest
versions. Also explain conventions for disclosing AI assistance; that question
does not request adding a new attribution policy or rewriting commit identities.

## Authorized scope

Eight canonical Macrostates specification repositories and macrostates-cli.
Change public setup wording, create the required compatible patch releases,
refresh required and optional dependencies in dependency order, and synchronize
the CLI's selected snapshots/lock and compatibility fixtures. Commit/push the
verified updates and release tags needed to make canonical package selections
installable. Preserve all existing tags and history. Repository visibility,
PyPI publication, unrelated consumers and organization profile content are
outside this change. Existing workflow records retain their status.

## Version classification

Meta public HTTPS/download guidance changes delivery instructions, preserving
package content/selection requirements. Use editorial package Patch releases.
Dependent minimum versions advance to the same compatible latest Patch releases.
No new behavior, required files, policy Major.Minor or compatibility boundary.
CLI local package 0.3.0 → 0.3.1; composition spec-0.2.1 → spec-0.2.2;
implementation remains 0.2.0 against its exact release baseline spec-0.2.0.

## Plan and acceptance

Record current refs, edit public startup guidance, validate package metadata,
all dependency edges and links/anchors. Commit and publish eight releases in
dependency order without moving tags. Adopt the latest five selected official
releases using the CLI's protected canonical installation and inventory lock.
Retain previous metadata fixtures and exercise the latest set. Run appropriate
static checks, supported-Python tests, own working/staged checks, source/secret
verification and remote CI. Report completed versions and attribution guidance.

## Delivered and related follow-up

Changed Meta kickoff/resource/catalog and CLI installation instructions to public
HTTPS/download defaults. Initially published eight editorial .1 patch releases.
The subsequent explicit AI README request is tracked separately in
[its workflow](2026-10-08__1VJQE4__ai-assistance-readme-note.md). New .2 snapshots preserve those already published .1
and earlier tags. The final dependency selections and canonical copies adopt
the .2 releases. No repository visibility changes are part of these requests.

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
