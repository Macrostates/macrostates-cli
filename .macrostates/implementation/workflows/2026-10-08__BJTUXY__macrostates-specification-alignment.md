# Macrostates specification alignment

- Workflow type: Specification update
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

Align all eight official specification packages and this CLI with the agreed
.macrostates/specs and .macrostates/implementation structure. Update every required
and optional dependency to the latest published package version in dependency
order. Explicit definer authorization includes necessary major package releases,
existing tag preservation, private remote publication and CLI self-adoption.
Only the eight Macrostates package repositories and macrostates-cli are in scope.

## Scope decision and related work

This is a distinct migration from [initial CLI bootstrapping](2026-10-08-cli-bootstrapping.md).
That workflow remains open awaiting acceptance; its implementation evidence is
preserved. This migration does not accept the first baseline or close prior work.
Earlier optional CLI-guidance work also remains open awaiting acceptance; this
migration preserves its recommendation and manual-verification requirements.
The specification changes create a CLI support/adoption gap, covered by
[CLI alignment](2026-10-08__BJTUXY__macrostates-cli-alignment.md). External package work is tracked by this scoped
record, outside portable package distributions.

## Plan and acceptance

Publish coherent new package releases in dependency order, with safe tracked
archive imports and lock semantics, modern directory scopes, consistent kickoff
and artifact paths. Migrate only this CLI's own specification composition.
Keep prior release tags and compatibility fixtures. Validate all package metadata,
links, dependency edges and exact release provenance before reporting completion.

## Version classification

Required project layout and dependency-major compatibility change package contracts.
The definer explicitly approved necessary package Major changes. Each affected
package receives one bump for this coherent change set. CLI composition adoption
and new supported release policies require an aligned new CLI contract baseline;
its numbers will reflect actual behavior, not upstream Major numbers.


## Delivered and verified

Published and verified annotated package releases in dependency order: Meta 2.0.0,
Process 3.0.0, Repository 2.0.0, Docker 2.0.0, Python 2.0.0, Python-project 2.0.0,
Python-library 1.0.0 and Android-app 4.0.0. All repositories remain private.
Validated all eight metadata documents, every one of the 15 required/optional
dependency edges against the latest selected version, and 103 local links and
anchors. Existing 21 annotated tag object identities are unchanged.

Meta defines modern tracked artifacts, composition format 1, archive snapshots
and integrity lock format 1. Updated Process locations/scope/synchronization,
Repository tracking rules and technology layout/build/version references. Package
repositories remain portable at their roots. The CLI self-composition uses the
latest five appropriate external packages plus local CLI 0.2.0 requirements.
Real authenticated CLI installation verified the new release contents and lock.
Gitleaks found no credentials in any of the eight package working trees.
The linked CLI implementation update closes the support/adoption gap.

## Remaining work

Definer review and explicit workflow closure. Earlier workflows remain open.
