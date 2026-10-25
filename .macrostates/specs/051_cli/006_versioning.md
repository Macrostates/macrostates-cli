# Versioning and compatibility

## Independent Identities

Distinguish reusable package releases, persisted schemas, selected Meta/Process
policies, project specification baselines, implementation baselines, computed
development identities, and application distribution versions. New package
releases do not imply new schemas or dictate the CLI application's Major number.
Meta owns reusable and local specification package versioning.

Process 5 and 6 own finalized `specs-MAJOR.MINOR.PATCH` and
`imp-MAJOR.MINOR.PATCH` baselines. They share contract Major.Minor and retain
independent patch counters. Ordinary development branches preserve recorded
starting baselines and expose computed suffixes; release preparation assigns
official numeric baseline versions. Read
[Development and releases](008_development-and-releases.md) for the state and
impact contracts. Matching numbers do not prove implemented requirement coverage.

Applications may have explicit independent version/release policies. Without
one, a stable application release uses the numeric part of its selected finalized
implementation baseline. Baseline finalization does not automatically publish
every application. Unchanged published applications retain their exact original
versions and provenance.

An application policy may permit a later release of reviewed identity metadata
against those same finalized baselines. Its source commit can
differ from the baseline commit without moving the baseline tags or inventing a
no-bump baseline release. Preserve exact baseline references and separately
verify the new source's permitted metadata-only delta, no-impact evidence, and
application policy under [Development and releases](008_development-and-releases.md).
Published application versions remain immutable: the numeric implementation
default does not permit uploading changed artifacts under an already published
distribution version. Technology-owned additional release identities follow
their declared policy.

## Formats And Layouts

| Surface | Interpretation |
| --- | --- |
| Composition without schema, or explicit 0 | Legacy composition format 0 |
| Composition schema 1 | Explicit orders and archive-capable format 1 |
| Package metadata without schema, or explicit 1 | Package metadata format 1 |
| Integrity lock schema 1 | Inventory lock format 1 |
| Process 5/6 implementation declaration schema 2 | Prefixed implementation/specification baselines |
| Work, change, deliverable, migration, and release-plan records schema 1 | Their explicitly defined Process 5/6 artifact formats |
| CLI application declaration schema 1 | Independent application build version and source validation |
| Locations | Modern and legacy, subject to selected policies |

New shorthand uses composition format 1; supplied manifests retain their format
and extension fields. Unknown formats fail clearly without replacing installed
packages or rewriting documents. Reading or checking a legacy context never
migrates it. Existing commands, APIs, transports, and historical fixtures retain
their selected behavior. New support must not silently reinterpret older policies.

## Release-Selected Policies

Meta 2.0.x, 2.1.x, 2.2.x, and 3.0.x require `.macrostates/specs/` and composition
format 1. Meta 2.2 adds generic tagged Git archives without changing that format.
Meta 3.0 retains the same technical formats and source mechanisms.
Explicit dependency constraints remain required; an authoring default does not
select latest packages or make an omitted constraint valid. Earlier releases
retain their own checks. Unknown later Meta layout policies receive unsupported
diagnostics; initialization refuses them.

Process 2.3.x, 2.4.x, 3.0.x, 4.0.x, and 4.1.x retain their numeric implementation
and `spec-MAJOR.MINOR.REVISION` declaration rules. Validate their exact baseline,
calendar date, shared Major.Minor, and independent revisions. The implemented
specification revision cannot exceed the composition's current revision. Their
explicit active phase requires an implementation declaration. Process 3.0.x and
4.x also require `.macrostates/implementation/`. Retain these old names and
rules while those releases are selected.

Process 5.0.x, 5.1.x and 6.0.x require modern locations, a `specs-*` composition
declaration, and a schema-2 `imp-*` implementation declaration when an implementation baseline
exists. Validate shared Major.Minor, exact implemented specification reference,
independent patches, and a quoted valid calendar date. A specification-only
project has no invented implementation baseline. Initialization creates a
provisional specification seed; the first implementation must be established
with explicit acceptance under Process before ordinary baseline release planning.

Process 5/6 structural checks permit incomplete development evidence to remain
documented while work proceeds. Dedicated change/integration/release checks
enforce readiness. They inspect documentary workflow status and authorization,
but do not establish truthful definer approval or semantic coverage automatically.
Process 1.x and 2.0 through 2.2 keep their earlier checks. Unsupported future
policies receive clear diagnostics instead of guessed requirements.

Under selected Meta 3.0, implementers classify and apply the required package
version increment within requested specification work. Under selected Process
5.1 and 6.0, they classify baseline impact and prepare the corresponding versions within
authorized release work. A Major increment or classification alone requires no
separate definer approval under these policies. Explain the impact in the change
record or proposal, and ask when requirements or compatibility expectations are
unclear. Older selected policies retain their own authority rules.

This version authority does not authorize additional scope, workflow closure,
reviewed integration, tagging, or application publication. Their existing
acceptance and authorization requirements remain separate. Readiness checks
inspect documentary evidence rather than proving truthful consent.

Process 6.0 retains the technical baseline and record schemas of Process 5.1.
Its public-document authoring contract replaces personal workflow attribution and
conversational request records with role attribution and neutral objectives.
Explicitly register that policy; do not infer support for future families.
Role-only workflow records retain the same status and documentary authorization
gates. Adopting it does not rewrite other projects or published history, and
legacy selected policies keep their previous interpretation. The CLI does not
provide a general anonymization scanner; retained output needs the selected
Process authoring review.

## Explicit Migration

`migrate-versioning` requires deliberate selection of supported Process 5 or 6 and an attached
development branch. It converts supported legacy `spec-*` specification and
numeric implementation declarations to `specs-*` and schema-2 `imp-*` names,
preserving numbers, dates, extension fields, and existing Git history/tags.
Record the old names and available original commits in migration provenance.
It does not invent missing tags or acceptance, move published refs, assign new
application versions, or select/install specification packages.

Repeated migration of already converted declarations reports no change. Reject
mixed or malformed declarations and conflicting existing provenance for explicit
repair. Preserved legacy tag aliases can be used for baseline verification only
when their recorded commit still agrees with an annotated original tag. Migration
is spelling/provenance conversion, not a claim that current development contents
are a finalized release. Review package adoption, pending work, and application
policies separately.

## CLI Application Build Version

This CLI application uses an explicit independent Python distribution policy.
Its authoritative declaration is
`.macrostates/implementation/application.yaml`, schema 1. It identifies the
application version, `development`, `candidate`, or `finalized` state, exact
`specs-*`/`imp-*` references, and calendar release date. The declared application
version need not share Major.Minor with the repository baselines.

Accept the CLI policy's three-part Python versions with supported prerelease,
development, and local suffixes. A development declaration must use a prerelease
or development representation; changed development source must not emit an old
stable application version. Raw Macrostates identity suffixes are not Python
distribution versions.

Candidate and finalized application declarations additionally bind a verified
`source_sha256` fingerprint of shipped inputs. A changed or missing fingerprint
blocks their build. Version bookkeeping must not hash its own declaration into
an impossible self-reference. Unshipped workflow changes do not alone invalidate
the application source fingerprint. Preserve the verified identity across source
archive rebuilding without Git. This is a build-validation contract; the exact
fingerprinting implementation belongs to implementation documentation.

Isolated builds read application metadata without importing the CLI, looking up
installed application metadata, accessing selected specs, consulting Git, or
fetching release information. Include the authoritative application resource in
source distributions. Missing/invalid application data must fail without silently
falling back to an older stable version. Preserve the prior standalone numeric
`release.yaml` build behavior when no application declaration exists in a legacy
source context.

Installed API/command version reporting uses distribution metadata without source
checkout access. Builds never change declarations, create tags, or publish.
Ordinary dependency installation may require a package index. Review and document
deliberate public API, command, and persisted-format compatibility changes.
