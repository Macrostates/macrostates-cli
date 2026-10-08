# Macrostates CLI alignment

- Workflow type: Implementation update
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Change depth: systemic
- Branch: main
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), supplied in this conversation.
- Implementer: Codex — GPT-6; exact revision and effort not exposed.
- Started at: 2026-10-08 12:07 UTC
- Last updated at: 2026-10-08 12:36 UTC

## Original request and scope

Implement the latest official package policies, preserve older supported projects,
and use the latest packages in this CLI's own modern composition. Update public
CLI/API documentation, tests, build metadata and current-state documentation.
No other consuming project is authorized for migration.

## Related specification work

[Specification alignment](2026-10-08__BJTUXY__macrostates-specification-alignment.md) owns the approved contract changes and
external package releases. [Initial bootstrapping](2026-10-08-cli-bootstrapping.md)
remains open awaiting acceptance; this record does not close or supersede it.

## Acceptance and planned validation

CLI and public Python API support modern Meta/Process packages, prior metadata
and composition formats and older layout discovery. Own imports are canonical
latest tagged releases with inventory locks. Process release declarations and
Python distribution versions agree. Run meaningful regression tests, static
checks, own working/staged checks, real private archive installation, installed
wheel tests, supported Python matrix and private remote verification.

## Version classification and adoption

Previous implementation version: 0.1.0, without a Process release declaration.
New compatible CLI/API capabilities target 0.2.0 / spec-0.2.0. Adopt Process's
contract versioning explicitly: declarations and Python builds must consume one
authoritative release version; validate actual coverage before primary-branch
integration. Retain older selected policies without applying new requirements.


## Delivered and verified

Added release-scoped Meta 2.0, Process 2.4 and Process 3.0 checks, retaining prior
formats/policies/layouts. Modern-policy initialization refuses legacy locations.
Component scope discovery reports the containing implementation directory and
stops at separate compositions. Migrated this repository's docs/specs together,
preserving prior records and acceptance state. Canonical archive installation
replaced the prior snapshots only after their old inventories matched.

Adopted spec-0.2.0 / 0.2.0 with one authoritative release declaration. Setuptools
reads it in isolated builds; ordinary imports retain their I/O boundary. Explicit
version access reads installed distribution metadata. Added current metadata
fixtures alongside 21 historical releases and maintained regression tests.

- 140 tests pass on Python 3.12.15, 3.13.16 and 3.14.7.
- All 140 tests also pass against the installed wheel in a separate Python 3.12
  environment outside the source checkout.
- Ruff lint/format and Pyright pass. Working-tree and exact staged own CLI checks pass.
- Built sdist and wheel from the sdist; verified py.typed, version metadata,
  one release declaration in the sdist, and exclusion of specs/workflows/tests.
- Installed wheel API verifies the real self-composition. A fresh disposable
  project completed init/install/check against actual private latest releases.
- Gitleaks found no credentials in the CLI working tree. Historical sources are
  retained; only the explicitly requested Macrostates repositories are modified.
- Measured coverage is 76%; console subprocesses and the isolated build-helper
  copies are exercised separately from that in-process coverage measurement.

Published implementation commit 1eacc30db0299694e1b02e5db134a1c00dfa2478.
[GitHub CI run 37777622784](https://github.com/Macrostates/macrostates-cli/actions/runs/37777622784)
passed all three Python jobs. A fresh remote clone matches the implementation and
passes both working-tree and exact staged checks with the independently installed
wheel. Live GitHub API reads verify private visibility, current main metadata and
all latest dependency requirements across all nine repositories. Gitleaks also
found no credentials in the CLI's committed history.

The CLI update is published on main with distribution version 0.2.0. Package
release tags were explicitly authorized and published; no CLI implementation or
composition release tag was requested. That distinction does not affect source
installation from main or the package snapshots consumed here.

## Remaining work

Definer review and explicit workflow closure. Earlier workflows remain open.
