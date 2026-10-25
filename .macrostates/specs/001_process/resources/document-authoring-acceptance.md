# Document authoring acceptance matrix

These are synthetic review cases for
[Public document authoring](../004_documents.md) and
[Legacy document cleanup](../annex_document-cleanup.md). They do not contain a
real incident or private input. The expected result is a review criterion, not a
claim that an executable check ran or that a product is anonymous.

| Case | Review condition | Expected result |
| --- | --- | --- |
| Workflow attribution | A new workflow uses Definer and Implementer roles without identity lookup or a personal-data request. | Role fields are sufficient; missing personal information is no blocker. |
| Technical objective | A change is documented as a technical requirement, scope and reason. | No user quotation, prompt fragment or conversational chronology is retained. |
| Host locations | Prose, JSON keys, file URIs, stack traces and generated commands may contain host-specific locations, including Windows and network forms. | Review all locations in memory; retain relative paths or unexpanded descriptive placeholders only. |
| Cross-project context | A filename, image tag, artifact prefix or link can reveal a consuming project. | Use a generic fixture and safe name before serialization; remove unnecessary context. |
| Ignored report | An ignored validation report has the same content as a tracked report. | Apply the same pre-write and completion review to both. |
| Nested output | Structured keys, values, media metadata and an archive within another archive require review. | Inspect nested contents and names; an unavailable format is an explicit coverage limit. |
| Historical receipt | An authorized cleanup replaces identifying context in an old receipt while retaining its original measured count and failure state. | Mark it Anonymized historical summary; do not claim a fresh run or retain an original copy or reversal map. |
| Digest meaning | A receipt contains an old recorded hash and a newly sanitized document. | Label the old hash a historical observation; identify any new digest separately. Never claim identical bytes. |
| Unavailable fixture | Historical evidence refers to inputs no longer available for reproduction. | State that limit without a fictional link, fabricated fixture or invented successful result. |
| Required exceptions | Legal notices, public dependency provenance, relative paths and intentional runtime container paths are necessary. | Keep them accurate under the narrow exceptions; remove unrelated contextual narrative. |
| Lifecycle state | A completed implementation still awaits Definer acceptance or closure. | Preserve open status and awaiting_acceptance; sanitization grants no acceptance or closure. |
| Qualification limits | A report describes only structural checks. | Do not turn the result into semantic-conformance or anonymity certification. |
| Diagnostics | A finding's original key or filename would disclose private context. | Use a neutral artifact label and rule without echoing the matched content. |

Review parsing and local links after rewriting structured or linked documents.
Inventory all generated material in scope; do not exclude drafts, temporary
outputs or ignored directories. Record actual results and limits in a neutral
receipt when these cases are exercised. Pattern checks support semantic review.
