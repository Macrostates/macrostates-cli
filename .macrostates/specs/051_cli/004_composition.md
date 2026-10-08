# Composition and discovery

## Discovery and scope

From a directory, or a supplied file's parent, find the nearest enclosing
composition under `.macrostates/specs/` or legacy `specs/`, named
`composition.yaml` or `composition.yml`. Reject competing manifests/layouts at
one candidate root. Stop after checking a Git root; nested Git projects must not
inherit a parent's composition. Never move artifacts during discovery.

Report component `main.md` specification entrypoints using the project's layout;
the component containing the artifacts is the scope root. Lint their local file
links. A component composed independently in either layout is checked separately;
do not traverse its internals as parent scopes. Specification resources, hidden
implementation directories and tool/cache/build/temporary directories are outside
ordinary scope discovery. Document exclusions and inspect these scopes manually
when needed. Do not infer authority or semantic coverage from paths.

## Documents and paths

YAML documents are mappings with unique string keys; reject malformed documents,
duplicates and aliases. Keep metadata dates as strings. Schema versions are
integers, excluding booleans; [Versioning](006_versioning.md) lists supported ones.

Composition requires a project name and entrypoint (default `main.md`), nonempty
selection, and orders as required by its format. Packages require unique portable
names, exact three-part versions, destinations and entrypoints (default `README.md`).
Destinations are relative to specs; entrypoints to the project/package specs root.
Orders reference selected names or destination/entrypoint paths, preserving order
and normalizing references to names for inspection. Reject duplicates and
unselected references. Format 1 requires every selected package once in each
order. Legacy format 0 permits missing/partial orders without inferring precedence.

Use safe relative POSIX paths within the project. Reject traversal, absolute
paths, managed symlinks, Git metadata, overlapping/case-colliding destinations
and overlaps with control files or project entrypoints. Keep credentials outside
source data. Preserve extension fields on initialization from a manifest without
interpreting them as support for new formats/source types.

## Sources, metadata and dependencies

`local` means project-owned content. `github-archive` requires credential-free
GitHub HTTPS/SSH repository URL and `tag: v<selected-version>`. Tagged
`git-subtree` also records `branch` and a project-relative `prefix` matching its
destination. Branch-only/commit-selected legacy sources need explicit migration.
Missing source type can be inspected but cannot establish a canonical lock.

Package `package.yaml` requires name, three-part version, nonempty description,
calendar-valid `versioned_at: YYYY-MM-DD HH:mm`, and safe entrypoint. Selected
name/version/entrypoint must match metadata; the entrypoint must exist. Metadata
owns dependencies; legacy selection copies, if present, must agree with it.

Dependencies have name/version and constraint `exact`, `compatible` or `at_least`.
Exact means equality; at_least means equal/higher numeric version; compatible
additionally means the same Major. Reject duplicate names within each dependency
list. Require selected required dependencies; check optional constraints only
when selected, without selecting them automatically. Detect applicable cycles.

## Link coverage

Check local Markdown file targets, including reference links, within the project
boundary. Skip fenced examples and remote/anchor-only targets. Report missing
files and escaping targets. Heading anchors and complete Markdown semantics are
outside this conservative check; manual reading remains necessary.
