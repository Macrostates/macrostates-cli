# Python library

## Supported surface and imports

Export `Project`, `Diagnostic`, `Report`, `MacrostatesError`, `SourceProvider`
and `GitHubSource` at the package root. Expose `__version__` on explicit access.
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

`GitHubSource(*, token=None, timeout=30)` is the supplied provider; construction
performs no I/O. Authentication precedence is explicit token, `GH_TOKEN`,
`GITHUB_TOKEN`, then an available GitHub CLI login. An explicit empty token
suppresses fallback. Credential lookup occurs only for source requests. Timeout
configures requests and credential lookup. Never persist credentials in
compositions, locks or URLs or include them in diagnostics. Authenticated redirects
must not forward credentials across hosts. Unsupported redirects and malformed
responses fail safely.
