# Python library

## Supported surface and imports

Export `Project`, `Diagnostic`, `Report`, `MacrostatesError`, `SourceProvider`
and `GitSource` at the package root. Preserve the legacy provider export described
under [Source boundary](#source-boundary). Expose `__version__` on explicit access.
Private modules and normalized internal models are not supported caller interfaces.
Construct projects through the factories below; their filesystem locations are
available as `root`, `specs`, `manifest` and `implementation` paths.

Ordinary imports perform no network or project-local file access, credential
lookup, subprocess execution or logging configuration. Explicit version access
reads installed distribution metadata, with `0+uninstalled` when absent; it does
not read a project's release declaration. Library calls return data or raise
exceptions rather than printing CLI output or configuring application logging.

## Project factories and operations

These signatures describe supported arguments, not internal storage:

```python
Project.open(path=".", *, source=None) -> Project
Project.initialize(root, *, name=None, packages=(), manifest=None,
                   layout="modern", source=None) -> Project
project.install(*, locked=False) -> Report
project.lock() -> Report
project.verify() -> Report
project.lint() -> Report
project.check(*, staged=False) -> Report
project.info() -> dict
project.identity(*, work=None) -> dict
project.start_work(identifier, *, origin_commit=None) -> Path
project.deliverables() -> dict
project.create_change(identifier, summary, *, specification, implementation,
                      deliverables=None, requirements=None, evidence=None,
                      gaps=None, work=None, origin_commit=None) -> Path
project.check_changes() -> Report
project.closure_request() -> dict
project.branch_status(*, target=None) -> dict
project.sync_branch(*, target, strategy, primary=None, fetch_remote=None) -> dict
project.check_integration(*, target=None, expected_target=None) -> Report
project.plan_release(*, target=None) -> dict
project.prepare_release(plan, *, date) -> dict
project.check_release(*, target=None, publication=False) -> Report
project.migrate_versioning() -> dict
```

Paths accept strings or filesystem paths. `open` uses [project discovery](004_composition.md).
`initialize` requires an existing directory and accepts either a composition
mapping/path or a name plus ordered `(package_name, version)` pairs. A supplied
manifest cannot be combined with a name or package selections. Copy mapping
input rather than modifying it. Layout is `modern` or `legacy`, subject to selected
policies. Retain an injected source for later operations. Reread configuration
per operation so subsequent manifest edits are observed.

Operation meanings and effects match [the commands](003_commands.md). `info`
returns the inspection mapping defined there. Report-returning methods return
validation results even when checks fail. Invalid configuration or unsafe/failed
operations raise `MacrostatesError`; ordinary filesystem read failures may raise
`OSError`, and invalid text may raise decoding errors. Handle exceptions separately
from unsuccessful reports. After lint succeeds in executing, `check` converts
missing/invalid integrity locks into `lock.invalid` diagnostics.

Development/versioning methods require explicit selection of a supported
Process 5.0 or 5.1 policy; older projects retain their existing behavior until
deliberate adoption. `branch_status` and `sync_branch` use the project's Git repository and
do not rewrite its version declarations or implicitly adopt Process 5. Public
method meanings and data contracts follow
[Development and releases](008_development-and-releases.md). Change arguments
`specification` and `implementation` are impact values, not version strings.
`start_work` and `create_change` return the created record path without committing
it. A closure request returns data and permission-request wording without sending
messages or modifying records.

New Git baseline operations require the shared project composition at its Git
repository root. Monorepo applications share that baseline. Independently
composed nested projects within a parent's Git checkout retain discovery,
lint/integrity, and staged-check behavior, but need separate Git/manual procedures
for independent baseline operations. Identity inspection reports unavailable
computed identity with an explanation in that context.

## Diagnostics and reports

`Diagnostic(code, message, path=None, severity="error")` is immutable. Code is a
machine-readable category; message explains the finding; path is an optional
string. Generated findings use severity `error` or `warning`. Human wording and
finding order are not exact-text guarantees.

`Report(diagnostics=...)` holds a diagnostic list, empty by default. `ok` is true
when no diagnostic is an error; warnings alone succeed.
`add(code, message, path=None, *, warning=False)` appends an error or warning.
Reports do not terminate a caller's process.

## Source boundary

`SourceProvider` defines `resolve(repository: str, tag: str) -> str` and
`download(repository: str, commit: str) -> bytes`. Resolution supplies a full
commit ID; download supplies that commit's tar snapshot with one enclosing
directory. Providers must preserve canonical identity and report expected source
failures with `MacrostatesError`. Injection does not enable unsupported manifest
source types or unsafe payloads.

`GitSource(*, timeout=120)` is the generic tagged Git provider; construction
performs no I/O. Accept explicitly configured credential-free Git URLs, SSH/SCP
remotes, absolute local paths, and relative local paths. Resolve relative local
addresses from the consuming project during package operations. An explicit
`vMAJOR.MINOR.PATCH` tag must be annotated and select a full commit identity.
Download only that resolved commit's archive. Use externally configured Git
authentication, never URL passwords or saved tokens. Failures and diagnostics
must not echo credential-bearing transport output. Source fetching must not
leave an upstream working clone in the installed package.

The legacy `GitHubSource(*, token=None, timeout=30)` remains supported for its
existing archive transport and retained provider export; construction
performs no I/O. Authentication precedence is explicit token, `GH_TOKEN`,
`GITHUB_TOKEN`, then an available GitHub CLI login. An explicit empty token
suppresses fallback. Credential lookup occurs only for source requests. Timeout
configures requests and credential lookup. Never persist credentials in
compositions, locks or URLs or include them in diagnostics. Authenticated redirects
must not forward credentials across hosts. Unsupported redirects and malformed
responses fail safely.
