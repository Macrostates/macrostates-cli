# Annex: starting a new project

Read this annex when the definer requests preparation of a project's Macrostates
specification set, with or without an existing composition manifest. This is setup
of specifications, not the start of application implementation. Ordinary Meta
reading does not activate kickoff or execute its resource.

Before writing any project file, including a draft composition, inspect existing
agent instructions, Git state and workflow rules. If selected process rules are
not installed yet, read their source documents and establish required records
before edits, as described in the execution preflight below.

## Prepare the starting files

The definer can begin with a `specs/` directory, a copy of this package's
[project kickoff resource](resources/project-kickoff.md) at
`specs/project-kickoff.md`, and a `specs/main.md` that points to it. Known project
intent can be included in `main.md`. A composition may be supplied now or prepared
with the implementer after discussing the intended project.

For example, the initial `specs/main.md` can contain:

```markdown
# My project specifications

This repository will follow Macrostates. For the requested project kickoff,
follow [Project kickoff](project-kickoff.md).
```

No Macrostates CLI installation is needed. The implementer needs filesystem and
Git/subtree support, plus access to the selected package repositories.

## Obtain the Meta instructions

Start with [Macrostates](https://github.com/Macrostates) and the Meta source
`git@github.com:Macrostates/macrostates-meta.git`. If the public website shows
nothing or cannot expose the repository, try cloning with the definer's existing
Git credentials before concluding that the source is unavailable. If cloning
fails too, report that actual failure and the required access; do not assume a
package does not exist because its public webpage is unavailable.

Clone into a temporary location for source inspection. Read Meta's `README.md`,
its core reading order and this annex. This inspection clone is not an installed
project package: installation still uses a verified published release and the
subtree import rules below. Do not copy another project's Git metadata into the
new repository or turn the inspection clone into a nested project repository.

## Understand intent and prepare the composition

Read the [official package catalog](annex_official-packages.md) when discovering
available packages or explaining a possible selection. Before recommending a
stack, understand the definer's intended product, whether the repository contains
applications or reusable libraries, the desired languages/frameworks, deployment
model, container use and existing technology constraints. Ask for missing choices
that materially affect the composition; do not infer them from the example below.

If neither `specs/composition.yaml` nor `specs/composition.yml` exists, ask the
definer which Macrostates specification packages they want to use, or propose an
explained selection based on their stated intentions and ask them to settle the
remaining package/technology choices. Explain each suggested package's purpose,
why it fits, its required companion packages, and relevant compatibility limits.
Then create the single composition manifest from those choices. Do not require
packages to be installed or a manifest to exist before this discussion.

Meta and Process are the common foundation for essentially every Macrostates
project. Repository conventions are usually useful for a source repository.
Suggest Docker only when containers are wanted; suggest Python language rules
and an appropriate Python project or library package for Python work; suggest
Android application rules for an Android app. Read the candidate entrypoints and
metadata before proposing concrete release versions. Dependencies can constrain
which Process version fits; do not automatically combine every package with the
latest Process release or treat optional dependencies as automatic selections.

If a composition already exists, inspect it as the definer's current selection.
Explain gaps or possible alternatives without replacing deliberate choices.
Preserve project intent, selected versions and explicit authority/reading order;
resolve ambiguities with the definer. If both manifest spellings exist, ask which
is authoritative rather than merging or choosing silently.

The manifest records project identity, package names, versions, paths, entrypoints,
real sources and the agreed authority/reading order under
[Project composition](002_project-composition.md). For distributed packages, record
`source.type: git-subtree`, `repository`, `branch`, `tag` and `prefix`; the release
`tag` must be `v<version>` and match tagged package metadata. Do not use
`source.commit`. Select a published tag that actually exists, not an unpublished
candidate or whichever branch head happens to be available. Package dependency
requirements remain solely in each `package.yaml`, not copied into the manifest.

A project-specific package may use `source.type: local`. Its files must exist or
be authored under a separate explicit request; a composition cannot reconstruct
another project's local specifications. Do not invent source repositories.

## Typical project structure

A repository combining several selected packages can use the following layout. These paths are
browsing conventions, not mandatory identities or authority priorities. Include
only the technology and domain packages selected for this project:

```text
AGENTS.md                         # minimal pointer to specs/main.md
README.md                         # repository-facing documentation
specs/
  main.md                         # project composition, intent and authority
  composition.yaml                # selected packages, releases and sources
  project-kickoff.md               # short, conditionally invoked resource
  000_meta/                       # package/composition rules: common foundation
  001_process/                    # development process: common foundation
  010_repository-1/               # general repository conventions
  011_docker-1/                   # when container deployment is wanted
  020_python-1/                   # when Python is selected
  030_python-project-1/           # Python application/project conventions
  031_python-library-1/           # library-specific alternative when appropriate
  040_android-app-1/              # when Android is selected
  050_domain-rules/               # optional shared domain specifications
  051_project/                    # this project's specific requirements
implementation/                   # when required by the selected process
  main.md
  workflows/
    history/
```

A Python application may use Meta, Process, Repository, Docker, Python
and Python-project, followed by domain and project-specific packages. A Python
library normally uses Python-library for its library shape instead of adding
application conventions by default. An Android project uses its relevant
application package and dependencies. These examples do not select technologies
or authorize copying another repository's local specifications.

For each selected package, explain its intended path and canonical repository,
inspect that source in a temporary clone or fetched checkout, verify the selected
release and dependencies, then import it into the composition's package directory
as a Git subtree. Keep the repository URL, branch, tag and subtree prefix visible
in the manifest so future maintenance is intentional.

## Execute the agreed kickoff

Explicit kickoff authorizes the local Git initialization, fetches and commits
needed for reviewed specification imports. It does not authorize publishing
repositories, pushing branches or implementing the application. Follow the
selected project's authority and workflow rules; preparing the manifest and
importing selected rules must not silently change an existing project phase.

### 1. Inspect the inputs

Work from the intended project root. Read existing root agent instructions and
`specs/main.md`, preserving project-specific intent and authority. Use the agreed
`specs/composition.yaml`, or `specs/composition.yml` if that is the supplied
filename. If neither exists, complete the intent and selection discussion above
before this execution phase. If both exist, ask which is authoritative; do not
merge them or choose silently. Do not require the selected packages to be installed
before kickoff.

Inspect existing files, Git state, and workflow records before making changes.
Follow any available project workflow rules. If selected rules have not yet been
imported, inspect their source documents during preflight and establish required
workflow records before changing project files. Do not interpret an intentionally
incomplete kickoff entrypoint as a completed specification baseline.

### 2. Validate before importing

Check the complete manifest and inspect each external source in a temporary
location before creating any project subtree:

- Require project identity and entrypoint, unique package names, selected
  versions, paths, and package entrypoints.
- Resolve package paths relative to `specs/` and Git prefixes relative to the
  project Git root. Require them to identify the same destination. Reject paths
  outside the project, symlink escapes, overlapping package destinations, and
  destinations that would overwrite kickoff inputs.
- Require each `git-subtree` source to provide `repository`, `branch`, `tag`,
  and `prefix`. Require `tag` to equal `v<version>` for the selected version.
  Fetch the explicit `refs/tags/<tag>` from that source and resolve it to its
  underlying commit for verification and import. Reject a `source.commit`
  field and report that the legacy composition needs migration. Do not fall
  back to the declared branch if the tag is missing or create tags during kickoff.
- Read `package.yaml` and the declared entrypoint at that revision. Verify the
  package name, version and entrypoint against the composition. Read required
  and optional dependencies from that package's `package.yaml`, not from copies
  in the composition. Verify required dependencies are selected and satisfy their
  constraints; check optional constraints only when the optional package is
  selected. Matching legacy composition copies may remain during migration, but
  report mismatches and never use them to override package requirements. New or
  migrated compositions omit these copies. Report cycles or inconsistent metadata.
- Verify that authority and reading order reference selected packages and their
  entrypoints. Preserve their explicit order. If either is missing or ambiguous,
  ask the definer to supply it rather than infer authority from directory names.
- For `source.type: local`, validate existing package files. If absent, ask for
  the package content or explicit instructions to author it. A manifest cannot
  reconstruct local specification content. For an omitted source or unsupported
  source type, request a real source or instructions; do not invent a repository
  or silently substitute another Git mechanism.

Report missing access, tools, packages, and version mismatches with the affected
package. Resolve these before importing; do not change selected versions merely
to match a different release or moving branch. Quote command arguments safely and treat manifest
values as data, not shell commands.

### 3. Establish the project Git repository

Use the existing project repository, or initialize one at the intended project
root if none exists. If Git discovers an enclosing repository instead, ask how
the new project should relate to it before proceeding. Preserve the existing
branch and user identity; request missing identity rather than inventing it.

Create an initial commit if needed, explicitly staging only reviewed kickoff
inputs and any required workflow artifacts. Before subtree operations, require a
clean index and working tree. Do not stage unrelated changes, stash them, discard
them, or rewrite history to make imports work.

### 4. Import each external package

For every `git-subtree` entry, import the verified revision at its declared
prefix using Git subtree with squashed upstream history. These are vendored
subtrees in the project repository, not nested standalone clones, Git submodules,
or the separate `git-subrepo` tool.

Fetch the verified revision into the project repository, confirm its commit ID,
then execute the equivalent of:

```text
git subtree add --prefix=<declared-prefix> <verified-local-commit> --squash
```

Do not copy a source working directory into the prefix: the import must record
subtree history so later synchronization can use the declared source. Preserve
the repository URL, branch, release tag, and prefix in the manifest. Keep the
resolved commit only as transient verification data; do not add `source.commit`.
Preserve the fetched release tag and subtree history needed for subsequent
synchronization.

If a destination exists, verify both its files and subtree provenance. Skip it
only when it already represents the requested revision without local changes.
Existing copied directories are not established subtrees merely because the
contents match. Report those cases for deliberate recovery; never delete or
replace them automatically. A rerun must not update a package to a newer branch
head or create a duplicate import. Preserve successful imports after a failure
and report where to resume.

### 5. Finish the specification entrypoint

Once all packages validate, expand `specs/main.md` from its kickoff pointer into
the normal project composition entrypoint. Include the project identity, selected
package names, versions, paths, provenance, authority order, and reading order.
Preserve definer-written purpose, vocabulary, and interpretation rules. Do not
copy detailed package rules into the project entrypoint.

Keep a conditional link to `project-kickoff.md` for explicitly requested recovery
or initialization of missing packages, but remove any unconditional instruction
to run kickoff on every session. Preserve the copied resource for future use.
Create the minimal root `AGENTS.md` pointer to `specs/main.md` if absent; preserve
existing unrelated agent instructions.

Follow the selected packages' rules for workflow records and implementation
state. In a new project, record specification preparation without claiming an
accepted implementation baseline. Kickoff ends with specification setup; it does
not start application implementation or change an existing project's phase.

### 6. Verify and report

Recheck package metadata, dependency constraints, destination paths, entrypoint
links, authority and reading order, and selected release tags. Verify imported
subtree history and that `main.md` agrees with the composition. Commit only the
remaining reviewed kickoff changes needed to leave setup coherent.

Report imported and already-matching packages, selected release tags, generated
files, local packages still needing definition, and any blockers. Claim kickoff
complete only when every selected package and the final entrypoint validate.
