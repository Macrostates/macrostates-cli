# Verification expectations

Follow Python-library for dependencies, formatting, linting, types, packaging,
tests, examples and documentation. Commit contributor dependency locks and run
relevant quality checks in CI. Verify these CLI-specific observable outcomes:

- Public factories/exports, reports/diagnostics, source injection and imports
  without project/network/logging side effects.
- Installed help/version/commands, human/JSON results, success/check/error exits,
  and command/API agreement.
- Modern/legacy discovery, ambiguity refusal, historical metadata and selected
  policy isolation, including unknown future formats/policies.
- Explicit initialization, preserved extensions/instructions, safe paths and no
  unintended application or Git changes.
- Dependencies, cycles, entrypoints, orders, links and independent scope boundaries.
- Canonical install/lock, offline integrity and executable flags, clean upgrades,
  missing-copy restoration, moved-tag refusal, edit preservation and rollback.
- Exact staged-index checks rather than working-tree contents.
- Release declarations, build isolation and installed API/wheel behavior outside
  the checkout across supported Python versions.

The CLI's own composition uses the latest compatible selected official releases
as unchanged tracked archives with a verified lock, plus editable local CLI
requirements. Working/staged self-checks exercise the supported behavior. Keep
historical fixtures; new upstream adoption never silently migrates other projects.

Maintain conformance mapping and dated evidence in implementation documentation,
distinguishing tests, manual review and coverage limitations. Structural checks
or a coverage percentage alone do not establish implementation conformance.
This expectation does not add an automatic semantic-conformance command.
