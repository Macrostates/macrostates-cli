# PyPI distribution and pip instructions

- Workflow type: Implementation amendment
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Change depth: medium
- Branch: release/pypi-distribution
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), repository-local Git identity and this conversation.
- Implementer: Model GPT-6; exact revision/identifier and effort not exposed; agent Codex; source: session metadata.
- Started at: 2026-10-09 10:52 UTC
- Last updated at: 2026-10-09 11:13 UTC

## Original request and scope

Update the CLI repository, build and publish it, then change CLI installation references to pip. Prepare a verified wheel and sdist, add GitHub trusted publishing and update the CLI README and organization-profile README. Existing Meta guidance delegates installation to the CLI README and contains no obsolete Git installation command. No canonical package edit or consumer migration is needed.

The earlier onboarding, AI disclosure, dependency-default and launch workflows are delivered and awaiting their own acceptance/closure. This request introduces a new distribution channel and is tracked separately without closing them or changing project phase.

## Version classification

The existing contract already requires ordinary Python distributions and an installed console entrypoint. Index publication realizes that distribution requirement and adds release infrastructure without changing library/command/schema behavior. Prepare implementation 0.3.1 as a delivery revision against unchanged spec-0.3.0; local CLI package 0.5.0 and imported snapshots remain unchanged. Do not move previous tags.

## Plan and verification

Use a PyPI pending trusted publisher bound to Macrostates/macrostates-cli, publish.yaml and the pypi environment. Build and validate isolated artifacts, check distribution metadata/rendering, exercise pip installation outside the checkout, run relevant required quality checks and stage/self-check, then integrate through a passing PR. Release only the integrated, validated commit with a matching annotated v0.3.1 tag. Upload through a separate OIDC publishing job without long-lived tokens. Verify public PyPI artifacts and pip installation after publication.

## Remaining work and blockers

All requested implementation, package publication and verification is delivered. Definer acceptance and explicit workflow closure remain. The definer created their personal PyPI account and configured the pending publisher. No API token is requested or recorded. Publication evidence below identifies the delivered release. Workflow closure and phase acceptance are separate decisions.

## Candidate validation

Prepared implementation 0.3.1 against unchanged spec-0.3.0. Updated pip/PyPI instructions and optional pipx/uv commands, absolute README links for index rendering, useful project URLs and the separate checked-build/OIDC-publish workflow. The pypi GitHub environment permits only v* tags. Third-party actions are pinned to verified commits.

Ruff lint/format, Pyright, all 190 tests on Python 3.14.7 and working self-check pass. Isolated sdist and wheel builds pass; Twine 7.0.0 strict metadata/rendering checks pass. Actionlint 1.7.12 validates both CI workflows. The initial installed-version test failed because it hard-coded 0.3.0; it now checks console output against installed distribution metadata, preserving the observable version contract across subsequent releases. No runtime source or selected package is changed.

The definer configured the personal-account pending publisher with the exact GitHub repository, publish.yaml and pypi environment. No token or private account email is recorded. The successful upload converted it to a normal publisher.

Both wheel and sdist install through real pip in separate clean Python 3.12.15 environments outside the checkout. Installed help, version and public API imports pass; MIT, typing marker, minimum Python, README metadata and sdist release declaration are present. The exact staged self-check passes.

Gitleaks 8.30.1 scanned the exact staged source and unpacked wheel/sdist contents with zero findings. Existing launch tag identities and immutable installed package snapshots are preserved.

## Delivered publication

[Release PR 4](https://github.com/Macrostates/macrostates-cli/pull/4) merged as 07119d69cc324b3793ecb377926b232538efdb86. Its tree matches the reviewed d8ef1ef17d725c4df8bdf124fef82fe87db86a01 candidate. The [main checks](https://github.com/Macrostates/macrostates-cli/actions/runs/37921917348) passed on Python 3.12, 3.13 and 3.14. Published annotated v0.3.1 at that integrated commit, with unchanged spec-0.3.0 tag and specification snapshot. [GitHub release](https://github.com/Macrostates/macrostates-cli/releases/tag/v0.3.1).

The [publishing workflow](https://github.com/Macrostates/macrostates-cli/actions/runs/37922032084) completed both build and publish successfully. [PyPI now provides version 0.3.1](https://pypi.org/project/macrostates-cli/0.3.1/), with wheel and source distribution matching the exact CI artifacts by SHA-256. Different archive timestamps from local builds do not change this published-artifact verification.

Real pip installed macrostates-cli==0.3.1 from the public PyPI index in a fresh Python 3.12.15 environment without local package/cache fallback. Installed help/version and public API import checks passed. With GitHub credential variables removed and GitHub CLI lookup suppressed for the test process, a fresh project using Meta 2.1.0 initialized, installed and checked successfully. No real login/configuration was changed.

The organization profile's pip guidance is integrated through its own PR after actual publication. Workflow closure and first-baseline phase acceptance remain separate; no canonical specification files or consumers were changed.
