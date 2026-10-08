# CLI bootstrapping

- Project phase: bootstrapping
- Workflow type: Project bootstrapping
- Status: completed
- Change depth: systemic
- Branch: main
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), explicitly supplied in this conversation.
- Implementer: Model — GPT-6; exact revision and effort not exposed; agent: Codex; source: session metadata.
- Started at: 2026-10-08 11:15 UTC
- Last updated at: 2026-10-08 13:00 UTC

## Original request

Create Macrostates/macrostates-cli as a private repository, implement the CLI,
and push it. Follow the Python and Python-library specifications. Design for
different specification versions and future backward-compatible extensions.

## Scope and acceptance

Implement init, install, verify, lint, info and combined check. Preserve numbered,
committed packages, support existing compositions without implicit migration,
use versioned adapters, test public API and installed commands, and verify the
private remote after publishing. The request authorizes initial bootstrapping,
local Git setup, commits and publication to this repository. It authorizes no
changes to other repositories and no package publication to PyPI.

## Work done

Confirmed the definer wants both a CLI and a supported public Python API, so
Python-library remains selected. Imported five compatible released packages
as verified Git subtrees. Added MIT licensing and the chosen public noreply Git
identity. Implemented versioned composition/metadata readers, a separate lock
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
- Gitleaks 8.30.1 found no credentials in the working tree. Git commit identities
  use Lucas Lopez and the explicitly supplied GitHub noreply address.
- Coverage reports 78%; subprocess console tests run separately from that
  in-process measurement. No percentage threshold substitutes for behavior tests.

## Publication verification

Published implementation commit 162e99959c91c059e3428bc2cf32fef9217bca3a to main.
GitHub confirms Macrostates/macrostates-cli is private and main is the default
branch. A fresh SSH clone matches that implementation. GitHub Actions run
37771631616 completed successfully across Python 3.12, 3.13 and 3.14. Gitleaks
also found no credentials in the committed history after publication.

## Remaining work

None within this workflow; completed work and validation are recorded above.
Baseline acceptance remains a separate project-phase decision.

## Blockers

None.


## Authorized closure

Closed at 2026-10-08 13:00 UTC under the definer's explicit instruction:
“you can then close all open workflows in the cli project and commit and push
the repository.” The identified set is all four open CLI-project records,
including specification capture. Earlier delivery evidence was reviewed, and
current conformance verification passed before closure. Earlier statements about
open related workflows describe their historical state; this closure supersedes
that tracking state. No external workflow record is closed.

Workflow closure is distinct from accepting the first implementation baseline;
project phase remains bootstrapping pending that separate decision.
