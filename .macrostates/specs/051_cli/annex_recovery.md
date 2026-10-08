# Recovery and legacy maintenance

Read when an operation fails, external files change, a tag moves, or legacy
sources need maintenance. Preserve useful work before retrying; never repair
integrity by locking unverified edits.

## Modified or missing packages

Use `verify` to locate added/missing/changed files. Preserve useful edits
separately, restore intended content, or deliberately move project-specific
requirements into a local package. Restore missing unchanged selections with
`install --locked`. Clean upgrades require deliberate version/tag edits and
`install`, then checks. Review meaning and authority separately from integrity.

## Tags and subtrees

Moved tags are source conflicts: inspect upstream and lock before selecting a
new release/migration. Deleting a lock to silently adopt movement is not routine
recovery. Branch-only/commit selectors need explicit tag migration. Maintain
subtrees with Git; archive install refuses conversion. Canonical lock requires
copies matching the selected tagged release.

## Interrupted operations

A crash may leave `.macrostates-operation` in specs and a nearby
`.macrostates-install-*` recovery directory. Confirm no operation is running,
inspect backups and package/lock state, and preserve recoverable data before
removing a stale marker or retrying. Rollback failure identifies retained data;
initialization can retain `.macrostates-init-*` files. Automatic crash recovery
and power-loss atomicity are not promised.

## Coverage limits

Resolve index conflicts before staged checks; check submodules separately.
Consult implementation resource limits for rejected snapshots. Inspect excluded
scopes, heading links, semantic authority, workflows and actual implementation
requirements manually. Unsupported policies require explicit support or manual
equivalents, rather than optimistic success.
