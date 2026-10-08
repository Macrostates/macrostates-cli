# at_least dependency authoring default

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Branch: spec/at-least-dependency-default in macrostates-cli
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), supplied in this conversation.
- Implementer: Codex, GPT-6; exact revision and effort not exposed.
- Started at: 2026-10-08 17:55 UTC

## Original request

Make at_least the dependency default so project composition can select latest
releases more freely. Clarify that a numeric minimum does not guarantee that a
future Major preserves all previous rules. The CLI still uses exact composition
selections and validates them; this request does not introduce automatic solving.

## Scope and open work

Prepare the Meta authoring policy and composition guidance first. The definer explicitly confirmed changing existing official-package constraints. Existing
branch/PR and earlier publication workflows remain open for acceptance.

## Version classification

Changing the recommended authoring default expands acceptable dependency versions
without changing explicit-constraint syntax, old releases or existing consumers.
Meta receives a backward-compatible Minor, proposed 2.1.0. The constraint field
remains explicit and required. Compatible and exact remain valid deliberate choices.

## Validation plan

Check metadata, Markdown links, constraints and composition semantics; preserve
main and all release tags. Use a feature branch and a PR for publication. Record
consumer and CLI policy compatibility separately from numeric constraints.

## Remaining work

Definer acceptance, authorized merge/release and explicit closure. All requested edits and PR submission are delivered.

## Confirmed scope

The definer chose changing both the default and existing official dependencies.
Change all 15 canonical package dependency edges and the CLI local package's
three authored edges from compatible to at_least, retaining numeric minimums.
External CLI archive snapshots remain immutable on their selected published
releases; they are imported only after new releases and an authorized adoption.

The prior Process 4.0.0 and Repository-1 3.0.0 PRs were merged externally during
this work. Their branches were fast-forwarded to the new target merge commits,
preserving all dependency edits. Separate Process 4.1.0 and Repository-1 3.1.0
Minor candidates receive new dependency PRs. Other changed
canonical packages receive Minor versions: Meta 2.1.0, Docker 2.1.0, Python 2.1.0,
Python-project 2.1.0, Python-library 1.1.0 and Android-app 4.1.0. Their constraints
expand accepted selections while retaining existing formats and minimum rules.
The CLI local package becomes 0.4.0; the self-composition revision becomes
spec-0.2.3 because its selected rules and runtime behavior are unchanged.
Implementation 0.2.0 and its exact spec-0.2.0 release baseline remain unchanged.

## Local verification

All 18 authored dependencies now use explicit at_least constraints. The 15
canonical minimum references identify real published package releases and retain
the earlier numeric floors. Compatible and exact remain accepted explicit choices.
All 102 canonical Markdown links/anchors validate. CLI working-tree check passes
and 156 tests pass on Python 3.14. Runtime source, release declaration, lockfile
and all downloaded snapshots are unchanged. All target branches were refreshed.

The new canonical release candidates are not selected in the CLI yet. Its Meta
2.0 and Process 3.0 policy adapters remain unchanged; Meta 2.1 and Process 4.x
policy support is required before automated adoption of those future releases.
At_least validation itself already accepts later Majors numerically.

## PR delivery

- meta 2.1.0: https://github.com/Macrostates/macrostates-meta/pull/1
- process 4.1.0: https://github.com/Macrostates/macrostates-process/pull/2
- repository-1 3.1.0: https://github.com/Macrostates/macrostates-repository-1/pull/2
- docker-1 2.1.0: https://github.com/Macrostates/macrostates-docker-1/pull/1
- python-1 2.1.0: https://github.com/Macrostates/macrostates-python-1/pull/1
- python-project-1 2.1.0: https://github.com/Macrostates/macrostates-python-project-1/pull/1
- python-library-1 1.1.0: https://github.com/Macrostates/macrostates-python-library-1/pull/1
- android-app-1 4.1.0: https://github.com/Macrostates/macrostates-android-app-1/pull/1
- cli local 0.4.0: https://github.com/Macrostates/macrostates-cli/pull/1

All nine PRs target main and are open and mergeable at verification. Package
repositories have no configured PR checks. CLI CI run 37821403654 passed its
Python 3.12, 3.13 and 3.14 checks for implementation commit 44d7435. A final
workflow-only commit records delivery without changing specifications or runtime.
PRs are attached to the chat. No direct primary-branch push or new release tag
was performed. Earlier Process/Repository PR merges were external target updates.

## Follow-up after acceptance

Merge and tag accepted package candidates when release publication is requested.
New selections remain deliberate. Before adopting Meta 2.1 or Process 4.x through
CLI checks, add the corresponding release-policy adapters and fixtures while
preserving older selected policies. No installed project snapshot was rewritten
to adopt an unpublished package. Explicit workflow closure remains outstanding.
