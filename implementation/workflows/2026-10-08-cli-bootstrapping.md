# CLI bootstrapping

- Project phase: bootstrapping
- Workflow type: Project bootstrapping
- Status: in_progress
- Delivery state: implementing
- Change depth: systemic
- Branch: main
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), explicitly supplied in this conversation.
- Implementer: Model — GPT-6; exact revision and effort not exposed; agent: Codex; source: session metadata.
- Started at: 2026-10-08 11:15 UTC
- Last updated at: 2026-10-08 11:15 UTC

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

Inspected compatible package requirements. Selected Process 1.8.0 because
Python-library 0.3.0 requires compatible Process 1.x. Created the private remote.

## Remaining work

Implementation, tests, tooling checks, packaging validation, documentation and
private push. Definer acceptance and workflow closure remain separate.

## Blockers

None.
