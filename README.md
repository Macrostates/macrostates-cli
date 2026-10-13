# Macrostates CLI

Install, inspect, and check reusable specification packages. Prepare development
change records, synchronize Git branches, and review integration and baseline
release readiness. Packages stay readable in numbered, version-controlled
directories such as `000_meta/` and `001_process/`.

The `macrostates` command and public `macrostates` Python API share the same
operations. Requires Python 3.12 or newer. Distribution name: `macrostates-cli`.
Import package and executable name: `macrostates`.
Licensed under [MIT](https://github.com/Macrostates/macrostates-cli/blob/main/LICENSE).

Application version `0.5.0` supports Meta 3.0 and Process 5.1 alongside earlier
selected policies. Its own composition uses released Meta 3.0.0, Process 5.1.0,
Repository 4, Python 2.1.1 and Python-library 2 packages. Within requested work,
implementers choose version impact without a separate Major-number approval.
The CLI application version is independent from its Macrostates specification
and implementation baselines. Older projects retain their selected formats and
policies until explicitly adopted and migrated.

## Installation

Install the published package from
[PyPI](https://pypi.org/project/macrostates-cli/) with pip in a Python 3.12 or
newer environment:

```bash
python -m pip install "macrostates-cli>=0.5.0"
macrostates --help
```

Use `python -m pip install macrostates-cli==0.5.0` to select this release, or
`python -m pip install --upgrade macrostates-cli` to update. The older `0.3.1` and `0.4.0`
releases remain available for projects that deliberately retain it. A virtual environment can be created with
`python -m venv .venv`; activate it before installing when your environment
requires one. For a command outside a project environment, use
`pipx install macrostates-cli` or `uv tool install macrostates-cli`.

To work from source, clone the repository and run `uv sync --locked`.
Use `uv run macrostates ...` from that environment. Installed version reporting
uses distribution metadata; source development identities are inspected through
the separate `identity` command.

## Start A Project

Supply a composition with explicit package versions, sources, authority, and
reading orders. The
[minimal composition](https://github.com/Macrostates/macrostates-cli/blob/main/examples/composition.yaml)
selects only Meta; add Process and the technology packages appropriate to your
project.

```bash
macrostates init --from /path/to/composition.yaml
macrostates install
macrostates info
macrostates check
```

The shorthand `macrostates init --name my-project --package meta@3.0.0`
creates a composition. Repeat `--package NAME@VERSION` for additional packages.
Input order supplies both reading order and authority, highest first; review them
before installation. No dependency or latest release is selected automatically.
Use `--from` for custom sources and deliberate orders.

The default layout is:

```text
AGENTS.md
.macrostates/
  specs/
    main.md
    composition.yaml
    composition.lock.yaml
    000_meta/
    ...
  implementation/
    main.md
```

Commit the composition, lock, package copies, and local requirements. Initialization
preserves existing agent instructions, refuses overwrites, and creates
specification scaffolding. Process 5 initialization supplies a provisional
specification seed; it never invents an accepted implementation baseline. Establish
the first baseline explicitly under the selected Process policy before using
ordinary release planning.

The CLI is strongly recommended and optional. Structural checks and recorded
evidence assist specification reading; semantic requirements, truthful approval,
and implementation conformance still need review. Existing projects keep their
selected policies until deliberately adopted and migrated.

## Package Commands

| Command | Purpose | Effects |
| --- | --- | --- |
| `init` | Prepare selected specification files | Local writes |
| `install` | Download and validate selected package releases | Source access and package/lock writes |
| `install --locked` | Restore an unchanged locked selection | Source access and package/lock writes |
| `lock` | Compare copies with canonical releases and record integrity | Source access and lock write |
| `verify` | Check external inventories and executable flags | Offline, read-only |
| `lint` | Check metadata, dependencies, orders, links, and selected policies | Offline, read-only |
| `info` | Inspect selections, provenance, dependencies, and scopes | Offline, read-only |
| `check` | Combine lint and integrity verification | Offline, read-only |
| `check --staged` | Check the exact Git index | Offline, read-only |

All commands accept `--project PATH` and `--json` before or after the command.
Discovery uses the nearest composition and stops at a Git root. Ambiguous
manifests/layouts fail clearly. Exit codes are **0** for success, **1** for failed
checks, and **2** for invalid input/operations. Usage errors retain standard text
help. Reports include diagnostic codes, messages, paths, and severity.

Local packages use `source: {type: local}`. They remain editable and linted;
external inventory checks exclude them. Exact composition selections and verified
locks preserve downloaded package identities.

## Git Package Sources And Recovery

This version supports `source.type: git-archive` with an explicitly
configured Git URL, SSH remote, or local repository and an annotated
`vMAJOR.MINOR.PATCH` tag. It materializes the exact resolved commit as tracked
files, using externally configured Git authentication. Installed packages are
readable snapshots and do not contain upstream working clones.

The legacy `github-archive` transport and public `GitHubSource` provider remain
available for existing compositions. That provider retains explicit token,
`GH_TOKEN`/`GITHUB_TOKEN`, and existing GitHub CLI login authentication precedence.
The generic `GitSource` provider uses configured Git authentication. Credentials
are never stored in compositions/locks or echoed in transport errors.

For updates, deliberately change selected `version` and `source.tag`, review the
human entrypoint and dependencies, then run `install`. It replaces a previous
copy only when that copy matches its locked inventory. Modified content is
preserved. Use `install --locked` to restore a missing unchanged copy.

Locks record full commit IDs and SHA-256 inventories of bytes and executable
flags. Reinstallation refuses a tag moved to another commit. Offline `verify`
cannot discover remote tag movement or establish the trustworthiness of an edited
lock; review locks with their package changes.

Package and release preparation roll back ordinary replacement failures and
retain recovery data when rollback itself fails. Interrupted operations require
inspection before retrying. See
[recovery guidance](https://github.com/Macrostates/macrostates-cli/blob/main/.macrostates/specs/051_cli/annex_recovery.md).

## Development And Baseline Releases

The following development commands require explicit selection of supported
Process 5.0 or 5.1. `branch-status` and `branch-sync` also serve projects retaining older
version policies. Core operations work with Git refs and commits; your repository
policy defines the review/integration mechanism and required external checks.

New baseline tooling uses a shared composition at the Git repository root,
including monorepos with several applications. Independently composed nested
projects within another checkout keep existing package checks, but need separate
Git or manual procedures for independent baselines. Identity inspection explains
when computed source identity is unavailable.

| Command | Purpose |
| --- | --- |
| `start-work --id ID` | Capture starting commit and baseline provenance before development or synchronization |
| `identity --work ID` | Inspect the work's computed development identity |
| `deliverables` | Inspect optional application policies and effective default versions |
| `change-create` | Declare separate specification/implementation impact, coverage, evidence, and gaps |
| `change-check` | Check those records for readiness |
| `closure-request` | List workflows and produce a numbered request for definer-authorized closure |
| `branch-status --target REF` | Inspect divergence against cached target state |
| `branch-sync --target REF --strategy merge\|rebase` | Incorporate upstream changes on a safe development branch |
| `integration-check --target REF` | Validate exact proposed combined contents and local readiness |
| `release-plan --target REF` | Calculate a reviewed, target/tree-bound baseline plan |
| `release-prepare --plan PATH --date YYYY-MM-DD` | Prepare candidate declarations and consume included records |
| `release-check` | Check candidate consistency and baseline identities |
| `release-check --publication` | Additionally require integrated annotated baseline tags and declared release source identities |
| `migrate-versioning` | Explicitly convert legacy declarations and preserve original refs/provenance |

Create development and release branches through the repository's policy. The CLI
does not create branches, submit integration proposals, approve reviews, tag,
push, or upload artifacts. Synchronization may merge or rebase commits only when
explicitly requested. It refuses the primary branch, dirty/detached states, and
existing operations, and leaves conflicts for the implementer to resolve. Add
`--fetch-remote NAME` to explicitly fetch a configured remote first.

After creating a branch, capture work before adding commits:

```bash
macrostates start-work --id offline-mode
macrostates identity --work offline-mode
```

If work started earlier, use `--origin-commit` with its actual full original
commit ID. The original provenance remains unchanged when upstream updates are
incorporated. A computed identity can look like
`imp-0.3.1-branch.feature-x.gabc123`; it does not reserve the next release number.

When preparing completed work, declare its impact explicitly:

```bash
macrostates change-create --id offline-mode --work offline-mode \
  --summary "Support the specified offline operation" \
  --specification-impact minor --implementation-impact minor \
  --requirements /path/to/coverage.yaml \
  --evidence "Offline behavior checks passed"
macrostates change-check
macrostates closure-request
```

The coverage document contains a `requirements` list with `requirement`,
`implementation`, and `verification` entries. Use explicit `none` impacts for
tracking-only changes. Semantic classification remains the implementer's
responsibility. Obtain the definer's required closure authorization and record
it; the CLI never closes workflows automatically.

Commit the completed preparation, then run `integration-check` against the
current target. Optional `--expected-target` binds the check to a full target
commit. The combined result must have valid scope/evidence and no open or
unconfirmed workflows, including history. Required external reviews and CI may
begin after a proposal is created, but still block final integration.

Accepted change records accumulate on the primary branch as unreleased work.
When finalization is requested, create a release branch from current integrated
state, refresh and incorporate the authoritative target, and review
`release-plan --target origin/main` when that is the configured authoritative
ref. The command uses cached state without fetching automatically. Save its
output outside the checkout or in an
ignored location. `release-prepare` applies that exact plan without committing it.
Changed source, records, declarations, or target require reassessment. Close the
release-preparation workflow, commit and check the candidate, then follow the
project's reviewed integration procedure. Tagging and publication remain separate
authorized operations.

Applications can release independently of the shared `specs-*` and `imp-*`
baselines. Without an application policy, their stable version is the numeric
selected implementation version. Android can use that default version name and
retain its own increasing version code. A new repository baseline does not
automatically release every application. Preserve exact source and baseline
provenance for each published deliverable.

An application policy may permit a later release of identity metadata, such as its
version/date or an Android counter, against an existing finalized baseline.
Review a ready `none`/`none` change record with evidence and no gaps, close its
workflows, and validate that only permitted metadata/bookkeeping changed. The
record stays pending; the old baseline plan, consumed records, and tags remain
unchanged. The application release identifies its new source commit separately
from those exact baseline references. No no-bump baseline plan is created.
Runtime, contract, or build-logic changes require ordinary impact classification.

The application still needs a new identity accepted by its distribution policy.
The numeric implementation default cannot be reused to upload changed artifacts
under an already published immutable package version. Independent numbering or
a technology-specific additional identity distinguishes another release.

## Python API

```python
from macrostates import Project

project = Project.open("/path/to/project")
report = project.check()
for diagnostic in report.diagnostics:
    print(diagnostic.code, diagnostic.message, diagnostic.path)
assert report.ok
```

Supported root exports include `Project`, `Report`, `Diagnostic`,
`MacrostatesError`, `GitSource`, and `SourceProvider`, with the retained legacy
transport provider documented above. `Project.open` and `Project.initialize`
construct projects. The package and development operations in the tables have
matching public methods, including `start_work`, `create_change`, `sync_branch`,
`check_integration`, `plan_release`, and `prepare_release`.

Pass `source=GitSource()` or an injected `SourceProvider` for explicit transport
control. Report-returning checks return unsuccessful diagnostics rather than
terminating the caller. Invalid operations raise `MacrostatesError`; ordinary
file reads may raise `OSError`. Imports perform no project/network I/O or logging
configuration. Explicit `__version__` access reads installed distribution metadata.
See the
[public library contract](https://github.com/Macrostates/macrostates-cli/blob/main/.macrostates/specs/051_cli/002_library.md)
for signatures and the
[development contract](https://github.com/Macrostates/macrostates-cli/blob/main/.macrostates/specs/051_cli/008_development-and-releases.md)
for data and readiness boundaries.

## Compatibility And Contributing

Retain composition formats 0/1, package metadata format 1, inventory lock format
1, modern and legacy locations, and previously supported release-policy adapters.
New Process operations require deliberate policy adoption; reading an older
project never migrates it. Tagged legacy subtrees remain maintainable through Git
and canonical locking; archive installation does not convert them implicitly.
Unknown future formats/policies fail clearly.

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest --cov=macrostates --cov-report=term-missing
uv build
```

Contributor dependencies are locked. Build output goes to ignored `dist/` and
temporary work to `tmp/<activity>/`. Optional hooks can run `check --staged`;
integration-preparation checks belong at their dedicated gate, since ordinary
development commits legitimately contain open workflows. Index checks preserve
partial staging, have documented resource limits, and exclude submodule contents.

The CLI tracks its own composition under `.macrostates/specs/`. Adoption of the
new official releases, exact selections, lock, and final baseline declarations
will be verified separately. This development branch uses an independent
[application declaration](https://github.com/Macrostates/macrostates-cli/blob/main/.macrostates/implementation/application.yaml)
for independent build version `0.5.0`; the Macrostates implementation declaration is a
separate identity. Candidate/finalized builds bind verified shipped source and
rebuild from source distributions without Git. Builds do not mutate declarations
or publish artifacts.

See
[implementation documentation](https://github.com/Macrostates/macrostates-cli/blob/main/.macrostates/implementation/main.md)
and
[conformance mapping](https://github.com/Macrostates/macrostates-cli/blob/main/.macrostates/implementation/specification-conformance.md)
for architecture, current adoption state, evidence, and limitations.

## AI Assistance

This project was developed with AI assistance.
