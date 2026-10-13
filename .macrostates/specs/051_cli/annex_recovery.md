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

Release preparation similarly preserves recoverable files when ordinary rollback
fails. A `.release-operation` marker and `.macrostates-release-*` directory can
remain after an interrupted preparation. Verify the exact plan, declarations,
pending/history records, and Git state before retrying; never delete evidence to
make an altered plan appear current.

## Development And Release Recovery

Inspect and resolve synchronization conflicts on the development branch, then
rerun affected readiness checks. The CLI does not automatically stash, discard,
abort, or force-push work. Preserve captured origins when incorporating upstream
changes. If provenance was not captured before development, supply the actual
original full commit explicitly instead of guessing it from today's target.

An open or unconfirmed historical workflow needs explicit definer-authorized
closure; moving or renaming it does not bypass integration readiness. Review
corrections create their own workflows and scope records before integration.

Changed release inputs or target state require a fresh reviewed plan. A prepared
candidate must not be silently retargeted to changed source. Preserve consumed
records when returning work to pending state under the project procedure.
Baseline finalization, tags, and application distribution may complete separately;
report partial publication accurately and preserve already published identities.

Explicit version migration preserves original refs and records verified aliases.
Repair mixed/invalid declaration state separately; do not move old tags or overwrite
migration provenance to force success. Application source-validation failures need
reviewed preparation of the actual candidate, not a fallback to an old stable
distribution version.

## Coverage limits

Resolve index conflicts before staged checks; check submodules separately.
Consult implementation resource limits for rejected snapshots. Inspect excluded
scopes, heading links, semantic authority, workflows and actual implementation
requirements manually. Unsupported policies require explicit support or manual
equivalents, rather than optimistic success.
