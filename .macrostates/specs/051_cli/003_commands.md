# Commands and output

## Common interface

Provide `--help`, `--version`, and `init`, `install`, `lock`, `verify`, `lint`,
`info`, `check`, and the flat development/release commands below. Version output
is `macrostates <installed-version>`. Every
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
| Development inspection/preparation success | 0 | The operation's data mapping, or created-record path/message |

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
known older Process contract-version policies receive `spec-0.1.0` initially.
Process 5.0, 5.1 and 6.0 receive the provisional `specs-0.1.0` specification seed
instead.
Initialization does not invent or accept an implementation baseline. Establish
the first baseline under Process with explicit definer acceptance; release tools
do not infer it from the presence of code or an initial phase label.

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

## Development And Release Commands

Use these commands under a supported Process 5.0, 5.1 or 6.0 policy, except Git branch
inspection/synchronization, which also serve older selected policies. Their
contracts and prerequisites are in
[Development and releases](008_development-and-releases.md).

| Command | Arguments and outcome |
| --- | --- |
| `identity` | Optional `--work ID`; return computed source identity, recorded baselines, current commit/branch, dirty state, and pending change IDs. |
| `start-work` | Required `--id ID`, optional `--origin-commit SHA`; capture starting provenance in a new work record. |
| `deliverables` | Return `{"deliverables": {...}}` with normalized declared application policies and effective default versions. |
| `change-create` | Required `--id`, `--summary`, `--specification-impact`, `--implementation-impact`; create a change record. Each impact is `none`, `patch`, `minor`, or `major`. |
| `change-check` | Return a report for change schema, coverage, evidence, and gaps. |
| `closure-request` | Return workflows requiring closure authorization and a short numbered permission request; never change their status. |
| `branch-status` | Optional `--target REF`; inspect ahead/behind counts and cached source/target commits without fetching. |
| `branch-sync` | Required `--target REF` and `--strategy merge\|rebase`; optional `--primary BRANCH` and `--fetch-remote NAME`; synchronize a safe development branch. |
| `integration-check` | Optional `--target REF`, `--expected-target SHA`; check exact combined contents and local integration readiness. |
| `release-plan` | Optional `--target REF`; return a read-only plan bound to the exact source/target state, records, declarations, and proposed versions. |
| `release-prepare` | Required `--plan PATH`, `--date YYYY-MM-DD`; apply a reviewed current plan as candidate files on a development branch. |
| `release-check` | Optional `--target REF`, `--publication`; check candidate readiness, optionally requiring integrated annotated baseline tags and declared application source references. |
| `migrate-versioning` | Explicitly convert supported legacy baseline declaration spelling and preserve migration provenance. |

`change-create` also accepts repeatable `--deliverable ID`, `--evidence TEXT`,
and `--gap TEXT`; `--requirements PATH` reads a YAML mapping containing the
requirement-coverage list. Use optional `--work ID` to reference captured work,
or `--origin-commit SHA` for explicit late starting provenance. These origin
forms cannot be combined. Without `--work`, a captured work record sharing the
change ID is reused. Otherwise automatic capture is available only at a known
starting commit; late capture requires an explicit original full commit ID.

Plans printed as JSON can be read as YAML input. `release-prepare` accepts the
plan mapping directly or a mapping containing `plan`. Saving a plan must not
dirty the tree needed for preparation; use an ignored location or a path outside
the repository. It does not create a branch, commit, integration proposal, tag,
or publication.
