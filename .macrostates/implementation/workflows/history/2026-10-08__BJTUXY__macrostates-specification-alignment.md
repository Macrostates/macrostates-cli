# Macrostates specification alignment

Anonymized historical summary. Dates, recorded states and measurements are retained historical observations. This rewrite does not rerun checks or grant acceptance. Commit IDs and artifact fingerprints describe the original observed sources or artifacts, not this edited document. Omitted evidence locations are unavailable through this summary; no substitute evidence is invented.

- Workflow type: Specification update
- Project phase: bootstrapping
- Status: completed
- Change depth: systemic
- Branch: main
- Requested by: Definer
- Implementer: AI-assisted implementation
- Started at: 2026-10-08 12:07 UTC
- Last updated at: 2026-10-08 13:00 UTC

## Technical objective and scope

Align reusable specification packages with modern tracked artifact locations, tagged snapshot imports and integrity locks. Preserve released identities, validate dependency compatibility and record the separate CLI support gap.

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
The recorded authorization covered the necessary breaking package releases. Each affected
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

## Recorded pre-closure gates

None within this workflow. Baseline acceptance remains a separate phase decision.

## Definer-confirmed closure

The Definer explicitly confirmed closure for this workflow's recorded technical scope. Acceptance remains limited to the distinctions already recorded below. This preserves the existing closed state; it does not grant new acceptance or publication authority.

Historical confirmation dates: 2026-10-08 13:00 UTC.
