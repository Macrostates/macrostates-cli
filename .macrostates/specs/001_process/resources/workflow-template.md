# Neutral workflow template

Use this template under [Workflow records](../002_artifacts.md#workflow-records)
and [Public document authoring](../004_documents.md). Allocate the real filename
using the established UTC time-ID rules. Replace technical placeholders with
actual neutral content before retaining a workflow; never collect personal data.
This resource is a template, not a started or completed workflow.

```markdown
# <technical workflow outcome>

- Project phase: <actual phase>
- Workflow type: <applicable named type and explicit scopes>
- Status: in_progress
- Delivery state: implementing
- Change depth: <small, medium, large or systemic>
- Branch: <repository-local technical branch>
- Requested by: Definer
- Implementer: Implementer
- Started at: <YYYY-MM-DD HH:mm UTC>
- Last updated at: <YYYY-MM-DD HH:mm UTC>

## Technical objective and scope

<Neutral requirements, authorized scope and exclusions. No transcript or
conversational provenance.>

## Acceptance criteria

<Observable technical conditions and required verification.>

## Work done and evidence

<Actual actions, role attribution, safe repository-relative artifacts, relevant
tool versions, measured results and limits. No raw private output.>

## Remaining work

<Implementation, verification and acceptance items still outstanding. Explicit
Definer confirmation of closure remains required.>

## Blockers and unresolved questions

<Technical blockers or None identified; never imply unperformed checks passed.>

## Suggested next step

<Next technical action or review decision.>
```

Use `AI-assisted implementation` for that role when relevant. Record a dated
technical handoff or changed scope without personal identifiers. When local work
is finished, use `Delivery state: awaiting_acceptance` with an open status until
the actual Definer decision. Only after explicit confirmation, record a neutral
dated closure decision identifying the authorized scope and outcome, set the
appropriate closed status and move the workflow to history. Do not add an empty
or fabricated closure authorization field merely to satisfy a checker.
