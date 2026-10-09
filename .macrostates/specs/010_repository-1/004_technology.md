# Repository technology

The repository uses Git for version control.

## Branches

The repository should have one primary branch that represents the current
integrated state. Common names are `main` or `trunk`.

All changes must be developed on topic branches. Changes enter the primary
branch only through pull requests (PRs). Direct commits, pushes and local merges
into the primary branch are prohibited. Branch names should be concise and
describe the work. Prefer short-lived branches containing a coherent set of
related changes; a branch need not correspond to each individual request.

Long-lived divergent branches should be avoided unless the repository has an
explicit release or maintenance policy that requires them.

## Autonomous implementer Git behavior

Autonomous implementers must identify the actual primary branch and verify that
the current branch is a suitable topic branch before applying any file change,
including documentation, workflow records, generated files and new files. They
must never apply changes while checked out on the primary branch. Read-only
inspection there is allowed. A detached checkout is not a topic branch.

Reuse a suitable existing topic branch for related work. When a new branch or a
switch is needed, suggest it to the definer and create or switch to it once
authorized. The implementer performs the operation; the definer need not do it
manually. Preserve existing work and do not silently stash, discard or transfer
unrelated changes. Establish the topic branch before making any file changes.

Autonomous implementers must not create, switch, merge, rebase, delete, or push
branches unless the definer explicitly authorizes that Git operation, including
through a previously authorized workflow. Do not ask again for authorization
already provided.

Autonomous implementers may inspect Git state when it is relevant to the work.
If a required branch operation is not authorized, suggest it and obtain the
definer's decision before proceeding. A request to implement changes alone does
not authorize remote publication.

When the definer requests pushing or publishing changes, push the topic branch
and submit a PR to the primary branch, or update that branch's existing PR.
An explicitly requested development target may be used instead. Never interpret
a request to push as permission to update the primary branch directly. PR
creation does not authorize merging it; an authorized primary-branch merge must
merge the PR. Release publication and branch deletion require their own scope.

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

Subtree publication must also respect the primary-branch PR rule. Publish the
split history to a topic branch and submit a PR when the destination is a primary
branch; subtree commands do not authorize bypassing that review path.

If subtree history has already diverged, do not force-push the subtree
repository by default. First prefer repairing the relationship by pulling or
merging the current subtree repository history back into the parent repository,
then continue with normal subtree pulls and pushes. Force-push only when the
definer explicitly accepts rewriting the subtree repository history.
