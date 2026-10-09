# PyPI release integration

- Workflow type: Development branch merge
- Project phase: bootstrapping
- Status: in_progress
- Delivery state: awaiting_acceptance
- Change depth: medium
- Branch: release/pypi-distribution
- Requested by: Lucas Lopez (713375+lucaslopez@users.noreply.github.com), repository-local Git identity and this conversation.
- Implementer: Model GPT-6; exact revision/identifier and effort not exposed; agent Codex; source: session metadata.
- Started at: 2026-10-09 10:52 UTC
- Last updated at: 2026-10-09 11:13 UTC

## Objective and authorization

The definer requests updating, building and publishing the CLI and its pip instructions. Complete that release through feature-branch PR integration, preserving protected main and required checks. Submit and merge only verified changes as the necessary integration step for the authorized release. No direct main push or administrator bypass. Track the CLI PR, separate organization-profile PR, reviewed commits, required checks, release tag and actual index publication. The definer completed account and pending-publisher setup.

## Readiness

Candidate implementation 0.3.1 references existing spec-0.3.0. Review against current main, validate staged content and clean distributions, and require all protected-main checks before integration. PR 4 is merged at 07119d69cc324b3793ecb377926b232538efdb86 with exact candidate-tree agreement and all main CI checks passing. Annotated v0.3.1 is published, retaining spec-0.3.0. The OIDC publishing workflow succeeded, and public pip installation plus artifact checksum verification passed. No workflow closure or phase change is authorized.

[Release PR](https://github.com/Macrostates/macrostates-cli/pull/4), [organization installation PR](https://github.com/Macrostates/.github/pull/1), [PyPI](https://pypi.org/project/macrostates-cli/0.3.1/) and [publication CI](https://github.com/Macrostates/macrostates-cli/actions/runs/37922032084) identify the delivery. The follow-up PR records evidence only and leaves product/specification versions and released tags unchanged. Acceptance and explicit workflow closure remain.

Organization profile PR 1 merged at 9fb46ec546f3218a281513c0357b333ae009ee0b after PyPI installation verification. Main protection remains enforced; no bypass or direct primary-branch push was used.
