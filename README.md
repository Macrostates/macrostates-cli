# Macrostates CLI

Install, inspect and check reusable specification packages. Packages stay in
numbered, version-controlled directories such as `000_meta/` and `001_process/`.
The `macrostates` command and the `macrostates` Python API share the same core.

Requires Python 3.12 or newer. Distribution name: `macrostates-cli`.
Import package and executable name: `macrostates`. Version 0.2.0 is an initial
API; compatibility changes will be documented. Licensed under [MIT](LICENSE).

## Installation

The repository is currently private and the package is **not published to PyPI**.
With GitHub SSH access and [uv](https://docs.astral.sh/uv/):

```bash
uv tool install 'git+ssh://git@github.com/Macrostates/macrostates-cli.git'
macrostates --help
```

Alternatively, clone the repository and install from its directory with
`uv tool install .` or `pipx install .`. A user installation exposes the command
without activating a project environment. Select a Git revision with the normal
package install URL syntax when a team needs a fixed CLI version.

## Start a project

Supply a composition whose package versions, authority and reading orders you
have selected. [The minimal composition](examples/composition.yaml) selects only
Meta; add Process and the technology packages appropriate to your project.

```bash
macrostates init --from /path/to/composition.yaml
macrostates install
macrostates info
macrostates check
```

For a short setup, `macrostates init --name my-project --package meta@2.0.0`
creates a composition. Repeat `--package NAME@VERSION` for additional packages.
This shorthand uses the order you supplied for both reading and authority
(highest first); review those orders before installation. It does not select
dependencies automatically or replace versions with the latest releases.
Use `--from` for custom sources or deliberate orders.

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

Commit the manifest, lockfile, package directories and project specifications.
Initialization preserves existing agent instructions and refuses to overwrite
project files. It prepares specification files; it does not implement an app.
Meta 2.0 and Process 3.0 define this layout. Their numbered packages and locks
remain tracked in Git. The CLI is strongly recommended and optional; reading
specifications and manual checks remain necessary for requirements beyond its
coverage. Existing projects keep their selected policies until explicitly migrated.

## Commands

| Command | Purpose | Network / writes |
| --- | --- | --- |
| `init` | Prepare selected specification files | Local writes |
| `install` | Download and validate selected archive releases | Network and package/lock writes |
| `install --locked` | Restore an unchanged, locked selection | Network and package/lock writes |
| `lock` | Compare existing copies with canonical releases, then record integrity | Network and lock write |
| `verify` | Detect modified, missing or additional package files and executable changes | Offline, read-only |
| `lint` | Check metadata, dependencies, cycles, entrypoints, orders and local links | Offline, read-only |
| `info` | Display packages, provenance and dependency/order information | Offline, read-only |
| `check` | Combine lint and verify | Offline, read-only |
| `check --staged` | Check the Git index, including partially staged edits | Offline, read-only |

All commands accept `--project PATH` and `--json` before or after the command.
Project discovery selects the nearest composition and stops at the Git root.
It rejects competing `.yaml`/`.yml` manifests and ambiguous legacy/modern layouts.
Exit codes: **0** success, **1** failed checks, **2** invalid input/operation.
Argparse usage errors use its standard text output and exit code 2.

Local packages use `source: {type: local}` and are freely editable. Their metadata
and links are linted; they are excluded from downloaded-package integrity checks.
Every external package needs a real source to establish a lock. `lock` never
accepts local modifications as the baseline: it compares against the release.

### Updating and recovering

Updates are deliberate manifest edits: change the
selected `version` and `source.tag` together, update the human entrypoint, then
run `install`. It replaces an old package only if its files still match its
previous locked inventory. Modified packages are left intact. A missing package
directory can be restored with `install --locked`.

Locks record full commit IDs and SHA-256 hashes of extracted file contents and
executable flags. ZIP/tar compression is not part of identity. Reinstallation
checks that the tag still selects its locked commit and fails if the tag moved.
The lock is a reviewable integrity baseline, not a digital signature: review its
changes together with package changes. `verify` is offline and cannot determine
whether a tag moved remotely.

Package operations validate all downloads and dependencies before replacing
files and roll back ordinary filesystem failures. A simultaneous CLI operation
is refused. An unexpected process termination may leave `.macrostates-operation`
and a `.macrostates-install-*` recovery directory; inspect those before removing
the marker or attempting recovery. Power-loss/crash-atomic filesystem commits
are not promised.

### Private packages

The downloader accepts credential-free GitHub HTTPS or SSH repository URLs.
It uses an explicit Python API token, then `GH_TOKEN`/`GITHUB_TOKEN`, then an
existing GitHub CLI login. Tokens are never stored in composition or lockfiles.
Initialization and offline commands do not look up credentials. Package imports
do not execute downloaded code.

### Checks before commits

Add the following entry to an existing pre-commit configuration after arranging
installation of the selected CLI version:

```yaml
repos:
  - repo: local
    hooks:
      - id: macrostates
        name: Check staged Macrostates specifications
        entry: macrostates check --staged
        language: system
        pass_filenames: false
        always_run: true
```

Run `macrostates check` in CI too. The CLI does not install hooks or change Git
settings automatically. Staged snapshots currently have a 128 MiB size limit
and exclude submodule contents. Structural checks do not prove semantic
consistency or implementation conformance. The local Markdown link checker
checks file targets, skips fenced code, and does not validate heading anchors
or implement a complete Markdown parser.

## Python API

```python
from macrostates import Project

project = Project.open("/path/to/project")
print(project.info())
report = project.check()
for diagnostic in report.diagnostics:
    print(diagnostic.code, diagnostic.message, diagnostic.path)
assert report.ok
```

Supported root exports: `Project`, `Report`, `Diagnostic`, `MacrostatesError`,
`GitHubSource`, and `SourceProvider`. `Project.open` and `Project.initialize`
construct projects; `install`, `lock`, `verify`, `lint`, `check`, and `info` are
the supported operations. `initialize` accepts a composition dictionary/path
or a `name` plus ordered `(package_name, version)` selections and a `layout`
of `modern` or `legacy`. Pass `source=GitHubSource(token=...)` for explicit
authentication or a `SourceProvider` implementation for another test transport.
`install(locked=True)` requires unchanged locked selections; `check(staged=True)`
checks the index. Expected configuration/operation errors raise
`MacrostatesError`; check failures are returned in `Report.diagnostics`.
Ordinary file read failures can raise `OSError`. Imports perform no project-local
or network I/O and do not configure logging. Accessing `__version__` explicitly
reads installed distribution metadata; it does not read a project declaration. The CLI configures standard logging when explicitly invoked.

## Compatibility and development

Unversioned compositions use the retained legacy reader. New compositions use
`schema_version: 1`. Both legacy `specs/` and `.macrostates/specs/` layouts are
recognized. Existing `git-subtree` compositions can be inspected, linted and
given an upstream-verified integrity lock without changing subtree history.
Archive `install` refuses subtree sources; use Git subtree maintenance until an
explicit migration is requested. Old branch-only/commit selectors need explicit
tag migration and are reported instead of being silently reinterpreted.

Package release versions are independent of format versions. Existing package
metadata is format 1, as is an explicit `schema_version: 1`. Unknown manifest,
metadata or lock formats fail clearly. Release policy adapters support Meta
2.0.x and Process 2.3.x, 2.4.x and 3.0.x. Modern policies require the modern
layout; Meta 2 also requires composition format 1. Earlier Meta releases and
Process 1.x/2.0–2.2 retain their existing checks. Future policy releases receive
explicit unsupported diagnostics rather than guessed requirements.

`info` lists directory-scoped specifications under visible component directories;
`lint` checks their local file links. The scope root is the component containing
`.macrostates/`. Separately composed subprojects are checked independently.
Tool/cache/build/temporary and hidden implementation directories are excluded
from this discovery; inspect their applicable scopes manually. Scope authority,
semantic requirements and workflow conformance always need specification reading.
See [architecture](.macrostates/implementation/main.md) for adapter extension guidance and
[project specifications](.macrostates/specs/main.md) for this repository's working rules.

```bash
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest --cov=macrostates --cov-report=term-missing
uv build
```

The contributor `uv.lock` is committed for repeatable development and CI.
Builds go to ignored `dist/`; temporary work goes to `tmp/<activity>/`.
Automated update planning, workflow commands, release publishing and migrations
are future features.

## This repository's specifications and version

The CLI manages its own specification composition under `.macrostates/specs/`,
using Meta 2.0.0, Process 3.0.0, Repository 2.0.0, Python 2.0.0 and Python-library
1.0.0 as canonical archive snapshots. Its local CLI requirements remain editable.
`macrostates check` and `check --staged` validate the same files contributors use.
This is also a real integration test of the supported package installation path.

The implementation's single version declaration is
[release.yaml](.macrostates/implementation/release.yaml); the specification baseline
is `project.version` in the composition. Setuptools reads the declaration during
isolated builds. The sdist includes that one declaration, while the wheel reports
its installed distribution version. Builds do not edit declarations, create tags
or require Git/network access to obtain release metadata. Ordinary dependency
installation may still require access to package indexes.
