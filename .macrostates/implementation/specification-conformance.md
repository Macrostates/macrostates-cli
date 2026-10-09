# CLI specification conformance

## Reviewed baseline and scope

The local CLI package 0.5.0 and composition spec-0.3.0 define the implementation
0.3.0 contract. The additive change supports Meta 2.1 and Process 4.0/4.1, keeps
all earlier supported formats/policies, and adopts the latest canonical packages.
The implementation declaration records this exact validated baseline. Branch/PR
compliance remains manual; no command performs Git publication or migration.
Canonical package adoption retains numeric minimums and explicit at_least rules.

Reviewed every source module, public root exports, command parser/rendering,
project operations, formats, metadata/dependencies, scopes/links, Git index,
source/authentication, archives/inventories/locks, transactions and build version
reader. Reviewed existing tests, fixtures, examples, packaging and CI. Internal
registries, algorithms, exact limits and historical setup facts remain outside
the normative local package. Persisted lock encoding and public signatures are
specified because callers/interoperating readers depend on them.

## Contract map

Paths below are repository-relative. Each row combines code inspection with the
listed evidence; it does not claim every edge has an independent automated test.

| Specification section | Implementation | Evidence |
| --- | --- | --- |
| [Concepts](../specs/051_cli/001_concepts.md): identity, ownership, effects | pyproject.toml; __init__, _cli, _project | Installed command/import contracts; offline/local-package integration tests; command-path review |
| [Library](../specs/051_cli/002_library.md): exports, version/import boundary | __init__, _models | test_import_has_no_filesystem_network_or_logging_side_effects; installed version contract; explicit public-value/API probe |
| Library factories and live configuration | _project.Project.open/initialize/_composition | nested/yml discovery, extension preservation, clean-upgrade tests; factory signature review |
| Library errors, Report and Diagnostic | _models; _project.check; _cli.main | CLI structured errors; integrity reports; explicit report/value probe; exception-path review |
| Library injectable SourceProvider/GitHubSource | _sources; _project | FakeSource install/offline cases; annotated tag, explicit credentials and redirect tests; empty-token probe |
| [Commands](../specs/051_cli/003_commands.md): flags/help/version/exits/JSON | _cli parser/main/display | tests/contract/test_cli.py; installed human/JSON/usage and flags probe; interruption path review |
| Commands initialization and side effects | _project.initialize | init CLI; extension/AGENTS preservation; shorthand roundtrip; unsupported package/format/layout tests; overwrite/rollback review |
| Commands install/lock/verify | _project._synchronize/verify | clean-upgrade, missing-copy, modified-copy, moved-tag and subtree tests |
| Commands lint/check/inspection | _project.lint/check/info | failed-check JSON, malformed info metadata, missing-link, offline and staged-index tests; output fields probe |
| [Composition](../specs/051_cli/004_composition.md): discovery and scope boundaries | _project.open; _scopes | competing layouts, duplicate manifests, nested discovery, component and separate-composition tests |
| Composition strict documents and safe paths | _io; _formats; _project._validate_paths | unsafe YAML/path, overlapping selection, credential URL and unknown schema tests; reserved-path review |
| Composition orders and extension preservation | _formats.common/v0/v1; initialize/info | format preservation and shorthand tests; explicit incomplete legacy/format-1 order probe |
| Composition sources/metadata | _formats; _sources; _validation.validate_packages | 45 prior plus eight current metadata fixtures; source spelling/credentials; metadata mismatch review |
| Composition dependencies | _validation.validate_packages | exact/compatible/at_least, missing/optional dependency, cycles and full current graph tests |
| Composition conservative local links | _validation.check_links; _scopes | missing/fenced-link and component tests; reference/anchor/escape behavior review |
| [Integrity](../specs/051_cli/005_integrity.md): source resolution and archives | _sources; _integrity.extract_archive | annotated tags, malformed transport, unsafe links/devices/traversal archives; duplicate/root/limit code review |
| Integrity lock binding/encoding/verification | _integrity; _project.verify | inventory bytes/add/remove/executable tests; unknown lock rejection; canonical/hash record review |
| Integrity updates, lock-only and local ownership | _project._synchronize | edited copies not blessed/overwritten, clean upgrade, restore missing, moved tag, local and subtree tests |
| Integrity competition/rollback | _project._synchronize; _mutations | concurrent edits/new destination/marker and simulated write rollback tests; rollback-failure/crash boundary review |
| [Versioning](../specs/051_cli/006_versioning.md): retained/unknown formats | _formats; _integrity.parse_lock | composition 0/1 and 53 release metadata cases, future metadata/manifest/lock refusal |
| Versioning Meta/Process isolation | _validation; _project.initialize | tests/integration/test_process_policies.py and test_latest_policies.py |
| Versioning distribution declaration/runtime metadata | _build_version; pyproject; MANIFEST.in; __init__ | tests/unit/test_build_version.py; installed --version; prior isolated sdist/wheel validation |
| [Verification](../specs/051_cli/007_verification.md): quality and self-use | pyproject; uv.lock; .github/workflows/checks.yaml | full supported-Python test matrix, static tools, own working/staged checks, prior canonical self-install and installed-wheel evidence |
| [Recovery](../specs/051_cli/annex_recovery.md) | transaction and source failure paths; README | edit preservation/subtree/tag/marker tests; manual review of recoverable workspace retention |

## Review findings and limits

The release adds known policy adapters and corresponding initialization checks.
Regression fixtures retain all prior release metadata; current fixtures cover the
eight newly published canonical versions. Tests exercise new policy declarations,
modern-layout refusal, patch ranges and unknown future-policy refusal as well as
existing behavior. Real canonical self-install, staged checks, supported-Python
checks and isolated distributions provide delivery evidence in the launch workflow.
No persisted schema, command, diagnostic category or supported root export changes.

Automated lint checks file targets, not Markdown anchors or semantics. Directory
scope discovery omits hidden/tool/build/cache/temp directories and independent
compositions. Index snapshots omit submodules and are bounded. Inventories omit
empty directories, ownership and non-executable permission differences. Locks are
not signatures. Process active-state checks recognize an explicit phase line;
they do not infer baseline acceptance. Interrupted operations require manual
recovery and arbitrary external writes are not fully isolated. These limits are
explicit in the specs and existing user documentation.

Exact current bounds: YAML/API documents 2 MiB; compressed archives 32 MiB;
extracted archives/index snapshots 128 MiB; archives 10,000 entries; annotated
release tag resolution eight levels. These are implementation limits rather
than requirements fixing the algorithms forever.

Dated validation results belong to their owning workflows, including the current
public onboarding/dependency update and closed specification-capture history.
Earlier installed-wheel/canonical-source evidence remains in the prior records.
