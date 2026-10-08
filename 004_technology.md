# Repository technology

The repository uses Git for version control.

## Branches

The repository should have one primary branch that represents the current
integrated state. Common names are `main` or `trunk`.

Work may happen on short-lived topic branches when that helps review,
experimentation, or collaboration. Branch names should be concise and describe
the work.

Long-lived divergent branches should be avoided unless the repository has an
explicit release or maintenance policy that requires them.

## Autonomous implementer Git behavior

Autonomous implementers should work on the currently checked-out branch unless
the definer explicitly asks them to create or switch branches.

Autonomous implementers must not create, switch, merge, rebase, delete, or push
branches unless the definer explicitly asks for that Git operation.

Autonomous implementers may inspect Git state when it is relevant to the work.
If an autonomous implementer believes a branch operation would help, it should
suggest the operation and ask before performing it.

Merge strategy, release branch policy, and remote publishing are project or
definer decisions unless explicitly delegated.

## Commits

Commits should be coherent, reviewable units of change.

Use conventional, descriptive commit messages. A commit message should make the
reason for the change understandable without requiring the reader to inspect the
entire diff first.

Do not mix unrelated behavior changes, cleanup, generated output, and
documentation updates in one commit unless they are part of the same coherent
change.

Before committing, avoid staging local-only files, generated files, temporary
files, secrets, credentials, or real account data.

## Tags and releases

Use Git tags for release points when the project publishes versions or stable
snapshots.

Release identifiers should be stable once published. If a published release has
a problem, prefer a follow-up release over rewriting history.

Release notes should describe user-facing or operator-facing changes, migration
notes, compatibility breaks, and known limitations relevant to the release.

## History

Do not rewrite shared history unless the project has explicitly agreed to do so.

Prefer preserving understandable history over making history artificially tidy
after work has been shared.

When a repository publishes subtrees or other split histories to external
repositories, treat those published split histories as shared history too. Do
not amend, rebase, replace, or otherwise rewrite commits that were used to
publish a subtree unless the workflow explicitly accounts for the downstream
subtree repositories and the definer approves the history rewrite.

After publishing a subtree for the first time, prefer follow-up commits over
amending the source commit. If a correction is needed after publication, make a
new commit and publish that new commit through the same subtree mechanism.

If subtree history has already diverged, do not force-push the subtree
repository by default. First prefer repairing the relationship by pulling or
merging the current subtree repository history back into the parent repository,
then continue with normal subtree pulls and pushes. Force-push only when the
definer explicitly accepts rewriting the subtree repository history.
