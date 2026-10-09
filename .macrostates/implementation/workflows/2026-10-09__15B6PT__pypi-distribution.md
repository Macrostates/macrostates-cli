# PyPI distribution and pip instructions

- Workflow type: Implementation amendment
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: implementing
- Change depth: medium
- Branch: release/pypi-distribution
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), repository-local Git identity and this conversation.
- Implementer: Model GPT-6; exact revision/identifier and effort not exposed; agent Codex; source: session metadata.
- Started at: 2026-10-09 10:52 UTC
- Last updated at: 2026-10-09 10:52 UTC

## Original request and scope

Update the CLI repository, build and publish it, then change CLI installation references to pip. Prepare a verified wheel and sdist, add GitHub trusted publishing and update the CLI README and organization-profile README. Existing Meta guidance delegates installation to the CLI README and contains no obsolete Git installation command. No canonical package edit or consumer migration is needed.

The earlier onboarding, AI disclosure, dependency-default and launch workflows are delivered and awaiting their own acceptance/closure. This request introduces a new distribution channel and is tracked separately without closing them or changing project phase.

## Version classification

The existing contract already requires ordinary Python distributions and an installed console entrypoint. Index publication realizes that distribution requirement and adds release infrastructure without changing library/command/schema behavior. Prepare implementation 0.3.1 as a delivery revision against unchanged spec-0.3.0; local CLI package 0.5.0 and imported snapshots remain unchanged. Do not move previous tags.

## Plan and verification

Use a PyPI pending trusted publisher bound to Macrostates/macrostates-cli, publish.yaml and the pypi environment. Build and validate isolated artifacts, check distribution metadata/rendering, exercise pip installation outside the checkout, run relevant required quality checks and stage/self-check, then integrate through a passing PR. Release only the integrated, validated commit with a matching annotated v0.3.1 tag. Upload through a separate OIDC publishing job without long-lived tokens. Verify public PyPI artifacts and pip installation after publication.

## Remaining work and blockers

All local candidate checks are complete; PR integration and PyPI publication remain. The definer is creating their personal PyPI account and will configure the pending publisher. No API token is requested or recorded. Do not claim that a candidate has been published. Workflow closure and phase acceptance are separate decisions.

## Candidate validation

Prepared implementation 0.3.1 against unchanged spec-0.3.0. Updated pip/PyPI instructions and optional pipx/uv commands, absolute README links for index rendering, useful project URLs and the separate checked-build/OIDC-publish workflow. The pypi GitHub environment permits only v* tags. Third-party actions are pinned to verified commits.

Ruff lint/format, Pyright, all 190 tests on Python 3.14.7 and working self-check pass. Isolated sdist and wheel builds pass; Twine 7.0.0 strict metadata/rendering checks pass. Actionlint 1.7.12 validates both CI workflows. The initial installed-version test failed because it hard-coded 0.3.0; it now checks console output against installed distribution metadata, preserving the observable version contract across subsequent releases. No runtime source or selected package is changed.

The definer is creating a personal PyPI account. Macrostates in the publisher form means the GitHub organization, not a separate PyPI account. Actual publication and index installation are still pending; no token or private account email is recorded.

Both wheel and sdist install through real pip in separate clean Python 3.12.15 environments outside the checkout. Installed help, version and public API imports pass; MIT, typing marker, minimum Python, README metadata and sdist release declaration are present. The exact staged self-check passes.

Gitleaks 8.30.1 scanned the exact staged source and unpacked wheel/sdist contents with zero findings. Existing launch tag identities and immutable installed package snapshots are preserved.
