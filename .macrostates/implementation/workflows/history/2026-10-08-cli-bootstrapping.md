# CLI bootstrapping

Anonymized historical summary. Dates, recorded states and measurements are retained historical observations. This rewrite does not rerun checks or grant acceptance. Commit IDs and artifact fingerprints describe the original observed sources or artifacts, not this edited document. Omitted evidence locations are unavailable through this summary; no substitute evidence is invented.

- Project phase: bootstrapping
- Workflow type: Project bootstrapping
- Status: completed
- Change depth: systemic
- Branch: main
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-08 11:15 UTC
- Last updated at: 2026-10-08 13:00 UTC

## Technical objective and scope

Establish the console command and supported Python library, versioned composition readers, canonical specification imports, integrity checking, tests and repository documentation. Verify the initialized repository and authorized source publication without claiming a distribution-index release or first-baseline acceptance.

## Scope and acceptance

Implement init, install, verify, lint, info and combined check. Preserve numbered,
committed packages, support existing compositions without implicit migration,
use versioned adapters, test public API and installed commands, and verify the
private remote after publishing. Authorized scope included initial bootstrapping, local Git setup, commits and source publication. Distribution-index publication and unrelated changes were excluded.

## Work done

The supported surface includes both a console command and Python library; Python-library remains selected. Imported five compatible released packages
as verified Git subtrees. Added MIT licensing. Implemented versioned composition/metadata readers, a separate lock
format, release-selected Process validation, injectable GitHub downloads, safe
archive extraction, file rollback, offline checks, staged checks and public API.
Added user documentation, examples, architecture and adapter decision record.

## Validation

- 111 tests pass on Python 3.12, 3.13 and 3.14, including metadata from all 21
  existing release tags, legacy/modern discovery and Process policy isolation.
- Ruff lint and formatting checks pass; Pyright reports zero errors/warnings.
- Authenticated GitHub archive comparison verified every vendored package;
  the generated integrity lock and the CLI's own combined check pass.
- A new disposable project completed CLI init/install/check against actual
  private Meta 1.7.0 and Process 2.3.0 releases. Its generated files remain outside
  this repository. Fixed and regression-tested the shorthand YAML alias issue.
- uv built a wheel and sdist. Both include py.typed and exclude specification,
  workflow, test, temporary and environment files. The built wheel's console
  command and public API passed in a separate Python 3.12 environment.
- Gitleaks 8.30.1 found no credentials in the working tree.
- Coverage reports 78%; subprocess console tests run separately from that
  in-process measurement. No percentage threshold substitutes for behavior tests.

## Publication verification

Published implementation commit 162e99959c91c059e3428bc2cf32fef9217bca3a to main.
GitHub confirms the release repository used the recorded visibility and main default branch. A fresh SSH clone matches that implementation. GitHub Actions run
37771631616 completed successfully across Python 3.12, 3.13 and 3.14. Gitleaks
also found no credentials in the committed history after publication.

## Recorded pre-closure gates

None within this workflow; completed work and validation are recorded above.
Baseline acceptance remains a separate project-phase decision.

## Blockers

None.

## Definer-confirmed closure

The Definer explicitly confirmed closure for this workflow's recorded technical scope. Acceptance remains limited to the distinctions already recorded below. This preserves the existing closed state; it does not grant new acceptance or publication authority.

Historical confirmation dates: 2026-10-08 13:00 UTC.
