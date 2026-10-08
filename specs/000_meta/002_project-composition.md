# Project composition

A specification project combines multiple specification packages into one
project-specific specification set.

The project composition lives at the root of `specs/` and should contain:

- `main.md`: the human-readable project specification entrypoint.
- `composition.yaml`: the machine-readable package composition.

`composition.yaml` is the conventional filename. `composition.yml` is also
accepted; use exactly one manifest per project. References to `composition.yaml`
in these rules also apply to that alternative spelling.

## Project kickoff

For a new project whose packages have not yet been imported, read
[Project kickoff](annex_project-kick-off.md). It explains how the definer copies
the `resources/project-kickoff.md` resource to `specs/project-kickoff.md` and
points to the copied file from `main.md`. The short resource introduces Macrostates
and its Meta clone source; the annex owns selection, validation and import steps.
When no composition exists yet, the annex requires discussion of the definer's
intent and technologies before preparing a compatible package selection. Read
[Official packages](annex_official-packages.md) when discovering candidates.
The initial entrypoint may contain just that kickoff instruction and any known
project intent. After kickoff, it must satisfy the normal composition rules
below. This temporary starting state does not require copying package folders.

## Repository agent entrypoint

A repository may include a root `AGENTS.md` file for tools or agents that look
for repository-level instructions before reading project files.

When present, root `AGENTS.md` should be extremely small and reusable. It should
point implementers to `specs/main.md` and tell them to follow the specification
composition, reading order, and authority rules defined there.

Root `AGENTS.md` should not describe the project, duplicate package rules, or
contain project-specific implementation instructions. Those belong in the
appropriate specification package or implementation documentation.

## README authority

`README.md` authority depends on where the file lives and what role metadata
assigns to it.

A package-level `README.md` is authoritative for that specification package
when the package's `package.yaml` declares it as the package entrypoint.

A repository-root `README.md` is repository documentation for people and tools
encountering the repository. It should not be treated as a specification
document merely because specification packages use package-level `README.md`
entrypoints.

If a project needs a root `README.md` update because package entrypoints changed,
that update should follow the repository documentation rules selected by the
project.

## Project entrypoint

The root `specs/main.md` describes the project-specific specification set. It
should be readable by humans and implementers before they enter individual
packages.

It should include:

- The project name or purpose.
- The specification packages used by the project.
- The selected version of each package.
- The selected local path of each package.
- The source or provenance of each package when relevant.
- The authority order between packages.
- The project-level reading order.
- The authority placement of directory-scoped specifications when present.
- Any project-specific vocabulary or interpretation rules.

The root `specs/main.md` may summarize package selection, but it should not
duplicate the detailed rules inside each package. When package details matter,
link or point to the package entrypoint.

## Directory-scoped specifications

Any implementation directory inside a repository may contain a `specs/`
subdirectory with `main.md` as its entrypoint. This supports repositories with
multiple packages, applications or other components without requiring a separate
specification package or project composition for every directory.

For example:

```text
specs/
  main.md
  composition.yaml
  000_meta/
apps/
  reporting/
    specs/
      main.md
      interfaces.md
    src/
```

Here, `apps/reporting/specs/main.md` owns specifications only for
`apps/reporting/` and its descendants, not the entire repository. The scope root
is the directory containing `specs/`, not `specs/` itself. A deeper directory may
also have its own `specs/main.md`; each scope remains limited to its own root and
descendants.

### Repository dependence and scope

Directory-scoped specifications belong to their enclosing repository project.
They may rely on its selected packages, vocabulary and requirements, and are not
portable, independently versioned specification packages. Do not list them as
packages in `composition.yaml` or require `package.yaml` or a local composition
manifest. Additional documents may be organized freely inside the local `specs/`;
`main.md` must identify the scope, purpose and reading order, and link to the
documents that carry requirements.

Directory specifications must not define requirements, behavior, ownership,
authority or required changes outside their scope root. They must not govern
ancestor directories, siblings or repository-wide policy. This limit cannot be
expanded by local wording, relative paths, linked documents or filesystem links.
They may reference external interfaces and enclosing specifications as context,
and define how their own component consumes or implements those interfaces;
they must not impose obligations on the external component. Requirements that
span directories belong in specifications with an enclosing scope.

### Discovery and authority

Before changing files, inspect the directories along the path
from the enclosing project root to each target directory for `specs/main.md`.
Read applicable entrypoints from outermost to innermost and follow their local
reading orders. Apply this also to new files and directories through their
existing ancestors. A scope applies only to targets within that scope; do not
load sibling scopes merely because they exist. Work spanning several scopes must
satisfy each applicable set for its own targets.

Directory specifications have the same normative status as selected specification
packages: they are definer-owned intended requirements, not implementation notes
or advisory documentation. The enclosing project entrypoint defines their
placement in its authority order. Local reading order does not establish priority
over enclosing specifications or packages, and a local entrypoint cannot elevate
its own authority or expand its scope. If the enclosing authority rules do not
resolve a conflict, ask the definer rather than assuming the nearest directory
wins. Existing enclosing requirements continue to apply within their scope.

A directory specification does not by itself establish a subproject or grant an
independent lifecycle. An explicitly separate project composition remains a
distinct context, not a directory specification set. The selected project rules
own subproject identification, lifecycle and integration; this directory mechanism
does not replace those rules.

## Composition metadata

The root `specs/composition.yaml` records the same package composition in a
structured form for validation, automation, and comparison across projects.

It should include:

- Project metadata.
- Package names.
- Package versions.
- Package paths.
- Package entrypoints.
- Package sources when relevant.
- Project authority order when it should be machine-readable.
- Project reading order when it should be machine-readable.

### Composition version

Project metadata may include `project.version`, identifying the complete composed
specification snapshot rather than any individual package or its implementation:

```yaml
project:
  name: example
  entrypoint: main.md
  version: "spec-6.4.2"
```

Meta defines the field and its scope, not its versioning policy. A selected package
or the explicit project contract defines whether the field is required, its format,
bump rules and any relationship to an implementation version. The example prefix
is illustrative; Meta does not require it for all compositions. Record the policy
owner in the human-readable project entrypoint so an implementer can locate it.
Meta does not depend on that policy package.

The snapshot includes the project entrypoint, composition, selected package
contents and applicable repository-specific directory specifications. Independently
composed subprojects retain their own specification snapshots; the parent snapshot
includes its requirements for their integration. File edits and package-selection
changes must be assessed under the selected policy even when they do not change
the effective project contract.
The policy defines finalized revision boundaries; Git can identify intermediate
work. A composition version must not replace package versions, dependency
constraints or package source release selectors. Do not use `package_version`
for the composition or derive it from the project-local package's version.

If a composition version is summarized elsewhere, keep the summary synchronized
with `project.version`. Do not infer an implementation's version or conformance
merely from this field. Projects adopting a new policy must identify their
transition and any pending implementation work explicitly.

### Package selection

Package entries should use this shape:

```yaml
packages:
  - name: process
    version: 1.0.0
    path: 001_process/
    entrypoint: README.md
```

`composition.yaml` should not replace package-level `package.yaml` files. It
records which package versions this project selected; each package still owns
its own metadata. Required and optional dependency requirements belong only in
the selected package's `package.yaml`. Do not duplicate `dependencies` or
`optional_dependencies` in new or migrated composition entries.

Read dependency requirements from every selected package's metadata. Every
required dependency must be selected and satisfy its declared version constraint.
Check an optional dependency's constraint only when that package is selected;
an optional declaration does not select a package by itself. Report missing
dependencies, incompatible versions, cycles and inconsistent package metadata.

For backward compatibility, existing compositions may retain matching dependency
copies during migration. These copies are non-authoritative and must never
override package metadata. Report mismatches rather than choosing one silently.
Migration removes those redundant fields after verifying package requirements
against the selected versions; it does not edit package requirements.

The package `path` may include ordering prefixes, grouping prefixes, or any
other project-local browsing convention. The path is the only field needed to
record where the package lives in the project.

## Package sources

A package entry may include `source` metadata that records where the local copy
comes from and how it should be synchronized.

Use `source` in `composition.yaml`, not in package-level `package.yaml`, because
source is a relationship between a specific project and its local package copy.
The same package version may be obtained from different places in different
projects.

Use `source.type: local` for packages owned only by the current project:

```yaml
packages:
  - name: project-local-specs
    version: 1.0.0
    path: 900_project-local-specs/
    entrypoint: README.md
    source:
      type: local
```

Use `source.type: git-subtree` for packages distributed from their own Git
repository and vendored into the current project:

```yaml
packages:
  - name: process
    version: 1.0.0
    path: 001_process/
    entrypoint: README.md
    source:
      type: git-subtree
      repository: https://github.com/example/specs-process.git
      branch: main
      tag: v1.0.0
      prefix: specs/001_process
```

For `git-subtree` sources, `repository`, `branch`, `tag`, and `prefix` are
required. The `prefix` identifies the subtree path used by Git and should usually
match the package path under `specs/`.

`tag` selects the release to import and must be `v<version>`, matching the
package's selected version. Resolve it explicitly as `refs/tags/<tag>` in the
source repository, then verify the tagged `package.yaml` name and version.
`branch` records the development branch used for checking future updates and
publishing authorized changes; it does not select the installed release.

Do not include `source.commit` in composition metadata. Commit IDs may be used
transiently to verify a fetched tag or perform a subtree import, but must not be
written back as an additional selector. A missing tag or mismatched package
version is a release metadata gap: report it and stop the affected import rather
than falling back to a branch or inventing a release tag.

During an approved update, import the selected release tag, validate the result,
and update `version` and `source.tag` together. Changing a selected tag is a
deliberate synchronization operation, not an ordinary kickoff rerun.

When migrating a legacy composition, replace `source.commit` or a branch-only
selection with the corresponding verified release tag. If the release has not
yet been tagged, record the pending publication in workflow documentation; do
not claim the declared tag is available or importable. Local package edits may
select the next planned version and tag during explicit specification work, but
release publication must verify and create that tag before consumers import it.

Package source and package version are separate concepts. The source describes
where the local package files came from and how to update or push them. The
version describes the semantic specification package version selected by the
project.

If a package is intended to be distributed from an external source but that
source does not exist yet, omit `source` until the source is real. Do not invent
placeholder repositories.

A project may select both a package and its optional dependency when it wants
their integration rules to apply. The optional requirement and its constraint
remain in the dependent package's `package.yaml`, not in the composition.

## Consistency

The root `specs/main.md`, root `specs/composition.yaml`, and each package's
`package.yaml` should agree about package names, versions and entrypoints.
Dependency requirements are validated from each `package.yaml` against the
composition's selected versions; missing composition dependency copies are not
a metadata gap. Legacy copies, if present, must agree with package metadata.
Package paths are owned by the project composition and should point to the local
directory that contains the matching `package.yaml`.

Package source metadata is owned only by `composition.yaml`; it is not expected
to appear in package-level `package.yaml`.

When changing a package version, update:

- The package's own `package.yaml`.
- The package entry in root `specs/main.md`.
- The package entry in root `specs/composition.yaml`.
- Any package-level dependency requirement that intentionally changes as a result.

If these files disagree, treat it as a specification metadata gap. Ask the
definer or repair it during explicit specification work before relying on the
inconsistent metadata.

## Package independence

Project composition may combine independent packages, but it should not make a
package depend on another package implicitly.

If one package needs concepts, authority, or rules from another package, record
that dependency in the dependent package's `package.yaml` with a version
constraint.

If packages are merely used together by the project, list them together in
`composition.yaml` without adding package-level dependencies between them.
