# Commands and output

## Common interface

Provide `--help`, `--version`, and `init`, `install`, `lock`, `verify`, `lint`,
`info`, `check`. Version output is `macrostates <installed-version>`. Every
command accepts `--project PATH` and `--json` before or after its name. The
project defaults to the current directory: initialization uses it as the target;
other commands use it as the discovery starting point.

Human output explains results and diagnostics. JSON output is one value on
standard output. Expected operation errors are controlled without tracebacks.
Usage errors retain standard text usage/help even with `--json`.

| Outcome | Exit | JSON shape |
| --- | --- | --- |
| Successful report | 0 | `{"ok": true, "diagnostics": [...]}` |
| Failed validation | 1 | `{"ok": false, "diagnostics": [...]}` |
| Invalid input/operation | 2 | `{"ok": false, "error": {"code": "operation.invalid", "message": "..."}}` |
| Initialization success | 0 | `{"ok": true, "message": "..."}` |
| Inspection success | 0 | Inspection mapping below |

Diagnostics contain `code`, `message`, `path` (string or null) and `severity`.
Interruption exits 130 with an interruption message; usage errors and interruption
do not promise operation-error JSON. Warnings alone succeed.

## Initialization

`init --name NAME --package NAME@VERSION ...` explicitly selects official
packages: meta, process, repository-1, docker-1, python-1, python-project-1,
python-library-1 and android-app-1. Use their Macrostates repositories and
conventional numbered destinations. Input order becomes reading and authority
order (highest authority first); ask the user to review these in the scaffold.

`init --from PATH` copies a supplied composition with extension fields/orders;
use it for custom packages/sources. Do not combine selection forms.
`--layout modern|legacy` defaults to modern. New shorthand uses format 1;
known Process contract-version policies also receive `spec-0.1.0` initially.

Create the composition, its specification entrypoint and implementation `main.md`
in phase `specification`. Create root `AGENTS.md` only when absent; preserve
existing instructions. Refuse existing compositions in either layout, overwrites,
unsafe paths, unknown formats and selected modern-policy/legacy-layout conflicts
before replacing project files. Do not install packages or create an integrity
lock. Roll back created files on ordinary write failures.

## Package operations

`install` downloads selected archives, validates selected metadata/dependencies
and writes external copies and their lock. `install --locked` requires an existing
lock and an unchanged exact external selection. Apply [integrity rules](005_integrity.md).

`lock` compares present external copies with canonical releases before writing
a lock, without installing or altering package contents. It supports archive
and tagged subtree sources and must not bless edits.

`verify` checks external inventories offline: added, missing or changed files,
executable flags, stale/missing selections and, when external packages are
selected, extra lock records. Entirely local compositions do not need a lock.
An absent/invalid required lock is an operation error for this command.

## Structural checks

`lint` checks metadata/selection agreement, dependency constraints and cycles,
entrypoints, orders, local specification links and supported release policies.
Unsafe/unparseable configuration is an operation error; findings in parsed
structures are diagnostics. Missing legacy machine-readable orders warn and
require manual inspection.

`check` combines lint and verification; missing/invalid locks become failed-check
diagnostics. `check --staged` checks an exact Git index snapshot, including partial
staging, rather than working-tree content. Require a readable Git repository/index,
refuse unresolved merges, preserve executable flags, and do not mutate Git.
Submodules are outside the snapshot. Document resource and discovery exclusions.

## Inspection

`info` reads available metadata offline and reports selection before installation.
Missing metadata is not itself an inspection failure; malformed available metadata
is. Inspection does not establish validity.

JSON/library output contains `project` (name), `schema_version`, `specs` (relative
directory), `packages`, `authority_order`, `reading_order`, `directory_specifications`.
Orders contain package names. Packages contain `name`, `version`, `path`,
`entrypoint`, `source`, plus `dependencies` and `optional_dependencies` when
metadata exists. Dependencies contain `name`, `version`, `constraint`. Directory
specifications contain project-relative `scope` and `entrypoint`. Human output
presents packages, sources, required dependencies, orders and scope entrypoints.
