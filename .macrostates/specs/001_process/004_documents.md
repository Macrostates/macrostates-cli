# Public document authoring

## Scope and responsibility

Every document produced by an implementer must be suitable for public distribution
from its first draft. Apply this contract before writing, not as an optional
publication cleanup. It covers specifications, implementation overviews,
workflows, decisions, validation receipts, reports, plans, handoffs, generated
documentation and document-like tool output retained as evidence. Markdown,
structured data, plain text and embedded media are included. Ignored locations,
temporary reports, drafts and archive members have the same requirements.

This is the central authoring contract for all Process artifacts. Artifact-specific
fields and lifecycle rules still apply. Document authoring does not authorize a
specification change, cleanup outside the requested scope, workflow closure,
integration or publication. Existing technical identifiers and dates do not prove
acceptance. Missing personal information must never block authorized work.

## Neutral content and role attribution

Write technical objectives, requirements, decisions, reasons, outcomes and limits.
Do not quote, reproduce or closely paraphrase a user's message as a transcript.
Do not retain prompt fragments, complaints, personal preferences, conversational
chronology, chat links, message identifiers or session identifiers. Preserve the
technical meaning and authorized scope without narrating its conversational origin.

Attribute work by role: `Definer`, `Implementer`, `Reviewer` or
`AI-assisted implementation`. Do not obtain identities from Git configuration,
environment variables, account profiles or filesystem paths. Do not request a
name, email or handle to fill a record. Do not retain identity sources, individual
contributor identifiers or model-session metadata. Relevant tool versions and
qualification environments may be recorded as technical evidence, independently
of role attribution, without private prompts or identifying configuration.

For handoffs or multiple contributors, retain dates, roles, technical scope and
observed results. Do not create pseudonym maps or replace one identifiable
contributor with another. Scope, acceptance and closure decisions remain explicit
role decisions; anonymous attribution does not grant permission to invent them.

## Paths, references and identifying material

Use repository-relative paths and commands rooted in a documented working
directory. For intentionally variable external locations use a descriptive
placeholder such as `<artifact-root>`, or an operator-supplied environment
variable. Never expand that location to a machine-specific value in a retained
document. Review home locations, temporary directories, mounts, Windows drive
and UNC paths, encoded file URIs and embedded command output as well as prose.

Do not include contextual references to other projects, repositories, customers,
organizations or workspaces. Do not name a consuming application, describe its
private layout, link its files or depend on access to it. Use generic integration
fixtures and describe the relevant interface. Prefer repository-local evidence
links. Keep the actual technical decision and its reason in the document rather
than linking a conversation, personal note, private ticket, attachment or
inaccessible external receipt. Remove irrelevant context instead of retaining a
recognizable pseudonym. Mark unavailable evidence honestly; never invent a link.

Exclude secrets and identifying configuration, including credentials, real
tokens, credential-bearing URLs, personal emails, account or tenant identifiers,
actual hostnames, private endpoints and filesystem usernames. Review filenames,
structured keys and values, commands, stack traces, artifact URIs, image names,
screenshots, metadata and archive contents. Neutral prose alone is insufficient.

### Narrow technical and legal exceptions

Preserve required copyright and license notices, immutable upstream provenance,
declared dependency identities, public protocol names and technical sources
strictly necessary to substantiate a compatibility or security claim. External
references under these exceptions must be public, directly relevant and free of
private context. These exceptions do not permit cross-project narrative or
conversational provenance. Repository-local component identifiers needed to
describe the current contract are technical identifiers, not permission to copy
another project's context into a reusable package.

Runtime configuration and documented container paths must remain executable and
accurate. Do not replace intentional paths inside a container with placeholders
solely because they are absolute. Distinguish such technical paths from host
locations. Preserve required user-facing product strings as technical requirements
when they satisfy this contract; do not present conversational text as product copy.

## Evidence handling before writing

Before running a tool or generating a document, decide which results are needed
and how they will be retained safely. Prefer an allowlist such as check name,
tool version, relevant environment, exit status, counts, relative artifact paths,
technical source identity, failures and qualification limits. Avoid retaining
raw stdout, stderr, stack traces or environment/configuration dumps.

Inspect and redact captured output in memory before serialization. Do not write a
raw private copy first, including in an ignored or temporary location, and then
sanitize it. Configure generators to use neutral names and safe output fields
before they write. If a tool cannot produce safe retained output, choose another
method or report the missing evidence; a required readiness check is not waived.
Do not retain original transcripts, private raw logs, reversible sidecars,
identity maps, backup copies or alternative private editions.

A redaction must preserve technical truth. Retain relevant measurements, failure
states and limits; use stable generic labels only when equality or path relations
matter. An edited historical receipt must say `Anonymized historical summary`
and explain any reproducibility limit. Do not invent successful checks or
fabricate evidence about actual runs. Do not imply that unavailable source
inputs remain reproducible. Clearly labelled synthetic integration and validation
fixtures are allowed: they may model prohibited forms using invented safe or
reserved data, never real identifying values, secrets or reconstructions of
private contexts. Retain synthetic inputs and results under this document
contract; never present them as unavailable original inputs or historical results.
If an original hash is retained, label it as a historical observation, not a digest of
the redacted document. A digest of a current sanitized artifact must identify that
artifact separately. Do not hash fabricated replacement inputs and present the
result as an original measurement.

New change records and evidence must comply before their hashes are bound into a
plan. Ordinary consumption still preserves those records unchanged. Authorized
legacy cleanup does not rewrite original commits, published tags or historical
baseline byte bindings; use the scoped procedure in
[Legacy document cleanup](annex_document-cleanup.md) for current documentation.

## Pre-write and completion review

Before every retained write, check the proposed content, destination name, links,
structured keys and values, and embedded material against this contract. Design
generated output so this review happens before serialization. Review archive
members recursively and inspect media or metadata that a text scan cannot see.

At completion, inventory all generated artifacts in scope, including ignored and
temporary outputs, nested archives and generated documentation. Parse structured
formats, verify local links and review meaning and indirect identifiers. A pattern
scan supports this review; it cannot guarantee anonymity. Diagnostics identify
the safe repository-relative document or a generic artifact label and the violated
rule, without echoing the identifying value, unsafe key, filename or matched text
into another log. If a location itself is identifying, use a neutral label.

Verify that acceptance, closure, qualification limits, technical requirements,
license notices and necessary provenance remain accurate. Report unreviewed or
unavailable evidence explicitly. Do not claim full anonymity, successful checks
or readiness merely because a scan has no matches. Review the synthetic cases in
[the acceptance matrix](resources/document-authoring-acceptance.md); the matrix
does not itself record a passed executable test.

## Legacy adoption

The policy applies immediately to new retained material in a selected project.
Adopting the package does not automatically authorize cleanup of existing
documents, changes to consumers or Git history rewriting. When legacy cleanup is
requested, read [Legacy document cleanup](annex_document-cleanup.md), establish
its document scope and preserve truthful technical decisions and lifecycle state.
Required current artifacts cannot be made compliant by moving a private edition
to an ignored directory. Report any unmet authoring or integrity requirement.
