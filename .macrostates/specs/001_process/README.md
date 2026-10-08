# Process specification package

This package describes how specification-driven work should proceed. It is
intended to be reusable across projects.

## Macrostates

This package is part of [Macrostates](https://github.com/orgs/Macrostates), a
project for composing reusable specification packages into specs-driven
development projects.

## Quick reference

This section summarizes rules expanded in the package documents below. Use it
for orientation, but apply the detailed rules in the referenced documents when
doing the work.

Implementation entrypoints and topic documents describe the current architecture,
behavior, rationale and gaps. Workflow chronology, decision history and dated
validation retain their separate roles; do not accumulate release notes in the
current-state overview. See [Artifacts](002_artifacts.md#implementation-documents).

Before changing any project file, the implementer must check workflow records
and ensure an open workflow record covers the change. See
[Artifacts](002_artifacts.md) for workflow record structure and
[Execution](003_execution.md) for when and how to use workflow records.

New workflow filenames use `YYYY-MM-DD__<time-id>__short-descriptive-name.md`,
with the UTC date followed by a six-character Base32 ID encoding only milliseconds
since midnight. Existing legacy filenames remain valid. See
[Workflow records](002_artifacts.md#workflow-records) for encoding and collisions.

On every request, compare its objective with the workflow's original scope.
Track distinct objectives separately, even when they share a screen or origin.
An instruction to perform new work authorizes its tracking record; closure is a
separate decision. Show `Delivery state: awaiting_acceptance` when implementation
and applicable checks are finished. See
[Scope check for every request](003_execution.md#scope-check-for-every-request).

Workflow closure requires explicit definer confirmation, including completion,
abandonment, and supersession. When work appears done, suggest closure and keep
the workflow open until the definer confirms. See [Execution](003_execution.md).

The implementer maintains contract versions automatically: compositions use
`spec-MAJOR.MINOR.REVISION`, implementations use `MAJOR.MINOR.REVISION`, with
independent revisions. Direct primary-branch development is supported; committed
integrated states must have matching Major.Minor and actual contract coverage.
Development branches may hold provisional gaps. See [Concepts](001_concepts.md#contract-based-versioning),
[Version declarations](002_artifacts.md#version-declarations) and
[Versioning and integration](003_execution.md#versioning-and-integration).
Existing projects must complete the documented adoption before committing an
aligned baseline; changing numbers alone does not establish conformance.

The Macrostates CLI is strongly recommended for supported specification checks
and remains optional. Use relevant manual equivalents when needed, preserving
the selected requirements and reporting coverage. Meta owns tool guidance;
[Specification verification](003_execution.md#specification-verification) defines
when checks fit a workflow and a proposed commit.

Development branch creation and merge are optional, explicit workflow types.
On a definer-requested merge request or merge, check readiness first; if required
checks fail or remain unavailable, clearly warn and do not perform that operation.
See [Development branch merge](003_execution.md#development-branch-merge).

Specification edits stay within the project context of the request. After
committing, inspect other package copies and suggest applicable pulls; obtain
explicit definer approval before updating another context. See
[Execution](003_execution.md) for scope and synchronization rules.

## Core and annexes

This package uses progressive disclosure. Core documents are mandatory reading
at the beginning of each working session because they describe the normal path
and the checks needed before changing files.

Annex documents describe rare branches, recovery procedures, and extended
handling. Read an annex only when a core document says the situation applies.

## Scope

- Core specification-driven development concepts.
- Definer and implementer responsibilities.
- Definer support during process execution.
- Documentation ownership and authority.
- Common workflows and workflow continuity.
- Contract-based composition/implementation versioning and release declarations.
- Optional development branch creation and validated integration workflows.
- Project scaffolding during specification.
- Workflow execution against specifications.
- Subproject coordination inside a parent project.
- Discovery of directory-scoped specifications and identification of subprojects.
- Gaps, decisions, completion checks, and quality expectations.
- Proportionate specification verification with optional CLI assistance.

Project-specific requirements belong in a project package, not here.

## Reading order

Read the core documents in this order:

1. [Concepts](001_concepts.md)
2. [Artifacts](002_artifacts.md)
3. [Execution](003_execution.md)

Conditional annexes:

- [Project state](annex_project-state.md): read when project phase or project
  artifacts appear inconsistent.
- [Conflicts](annex_conflicts.md): read when ambiguity, authority conflict, or
  workflow conflict is found.
- [Exceptions](annex_exceptions.md): read when an `Exception` workflow is
  needed.

## License

This specification package, including its documentation, metadata, and bundled
resources, is licensed under the [MIT License](LICENSE).

Copyright (c) 2026 Lucas Lopez.

## AI assistance

This project was developed with AI assistance.
