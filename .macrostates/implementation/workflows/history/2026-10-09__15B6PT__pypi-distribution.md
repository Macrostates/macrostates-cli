# PyPI distribution and pip instructions

Anonymized historical summary. Dates, recorded states and measurements are retained historical observations. This rewrite does not rerun checks or grant acceptance. Commit IDs and artifact fingerprints describe the original observed sources or artifacts, not this edited document. Omitted evidence locations are unavailable through this summary; no substitute evidence is invented.

- Workflow type: Implementation amendment
- Project phase: bootstrapping
- Status: completed
- Delivery state: accepted
- Change depth: medium
- Branch: release/pypi-distribution
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-09 10:52 UTC
- Last updated at: 2026-10-09 11:13 UTC

## Technical objective and scope

Prepare ordinary Python wheel and source distributions, verify clean installation and metadata, publish the integrated 0.3.1 release through trusted publishing, and document practical pip installation.

## Version classification

The existing contract already requires ordinary Python distributions and an installed console entrypoint. Index publication realizes that distribution requirement and adds release infrastructure without changing library/command/schema behavior. Prepare implementation 0.3.1 as a delivery revision against unchanged spec-0.3.0; local CLI package 0.5.0 and imported snapshots remain unchanged. Do not move previous tags.

## Plan and verification

Use a PyPI pending trusted publisher bound to the release repository, publish.yaml and the pypi environment. Build and validate isolated artifacts, check distribution metadata/rendering, exercise pip installation outside the checkout, run relevant required quality checks and stage/self-check, then integrate through a passing PR. Release only the integrated, validated commit with a matching annotated v0.3.1 tag. Upload through a separate OIDC publishing job without long-lived tokens. Verify public PyPI artifacts and pip installation after publication.

## Recorded pre-closure gates and limits

All requested implementation, package publication and verification is delivered. Definer acceptance and explicit workflow closure remain. Trusted-publisher setup was completed. No API token is requested or recorded. Publication evidence below identifies the delivered release. Workflow closure and phase acceptance are separate decisions.

## Candidate validation

Prepared implementation 0.3.1 against unchanged spec-0.3.0. Updated pip/PyPI instructions and optional pipx/uv commands, absolute README links for index rendering, useful project URLs and the separate checked-build/OIDC-publish workflow. The pypi GitHub environment permits only v* tags. Third-party actions are pinned to verified commits.

Ruff lint/format, Pyright, all 190 tests on Python 3.14.7 and working self-check pass. Isolated sdist and wheel builds pass; Twine 7.0.0 strict metadata/rendering checks pass. Actionlint 1.7.12 validates both CI workflows. The initial installed-version test failed because it hard-coded 0.3.0; it now checks console output against installed distribution metadata, preserving the observable version contract across subsequent releases. No runtime source or selected package is changed.

The trusted publisher was bound to the release repository, publish.yaml and pypi environment. No token or private account email is recorded. The successful upload converted it to a normal publisher.

Both wheel and sdist install through real pip in separate clean Python 3.12.15 environments outside the checkout. Installed help, version and public API imports pass; MIT, typing marker, minimum Python, README metadata and sdist release declaration are present. The exact staged self-check passes.

Gitleaks 8.30.1 scanned the exact staged source and unpacked wheel/sdist contents with zero findings. Existing launch tag identities and immutable installed package snapshots are preserved.

## Delivered publication

Release PR 4 (external evidence location omitted) merged as 07119d69cc324b3793ecb377926b232538efdb86. Its tree matches the reviewed d8ef1ef17d725c4df8bdf124fef82fe87db86a01 candidate. The main checks (external evidence location omitted) passed on Python 3.12, 3.13 and 3.14. Published annotated v0.3.1 at that integrated commit, with unchanged spec-0.3.0 tag and specification snapshot. GitHub release (external evidence location omitted).

The publishing workflow (external evidence location omitted) completed both build and publish successfully. PyPI now provides version 0.3.1 (external evidence location omitted), with wheel and source distribution matching the exact CI artifacts by SHA-256. Different archive timestamps from local builds do not change this published-artifact verification.

Real pip installed macrostates-cli==0.3.1 from the public PyPI index in a fresh Python 3.12.15 environment without local package/cache fallback. Installed help/version and public API import checks passed. With GitHub credential variables removed and GitHub CLI lookup suppressed for the test process, a fresh project using Meta 2.1.0 initialized, installed and checked successfully. No real login/configuration was changed.

Public pip guidance was verified after actual package availability; its separate evidence location is omitted here. Workflow closure and first-baseline phase acceptance remain separate; no canonical specification files or consumers were changed.

## Definer-confirmed closure

The Definer explicitly confirmed acceptance and closure for this workflow's recorded technical scope. This preserves the existing closed state; it does not grant new acceptance or publication authority.

Historical confirmation dates: 2026-10-13.
