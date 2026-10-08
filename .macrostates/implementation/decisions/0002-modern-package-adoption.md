# Modern package and declaration adoption

Status: adopted for the 0.2.0 candidate. Related decision:
[versioned adapters](0001-versioned-format-adapters.md).

## Context and choice

The definer requested modern artifact locations, current dependencies throughout
all official packages, and CLI support plus self-adoption. The original subtree
composition selected Process 1.8 to satisfy Python-library 0.3's 1.x constraint.
Python-library 1.0 now selects Process 3 and Meta 2; the new set is compatible.

Move the CLI's specs and implementation documentation together into .macrostates.
Retain original workflow records and pending acceptance. Replace current subtree
source selections with tracked release archives through an explicit migration.
The old lock inventories verify preserved package copies before install replaces
them with the new canonical releases. Historical subtree commits remain history.

Keep composition/metadata/lock format 1. A new package major does not itself change
file schemas. Add release-selected Meta 2.0, Process 2.4 and Process 3.0 policy
adapters, retaining earlier rules and refusing unknown future policies. Component
scopes belong to the implementation directory containing .macrostates, and
independent compositions form traversal boundaries.

Adopt spec-0.2.0 / 0.2.0 explicitly. Process's release.yaml is the single version
source. Setuptools evaluates a standalone helper during build isolation, without
importing the application or needing Git/network release metadata. Include only
that declaration from implementation docs in the sdist. The wheel's distribution
metadata provides the version lazily on explicit __version__ access, preserving
side-effect-free ordinary imports and avoiding project file access at runtime.

## Consequences

Own install/check exercises production package transport and validation. Canonical
package edits happen upstream; local CLI requirements remain editable. Consumers
retain older selections/layouts until they deliberately migrate. New policies
need explicit adapters and regressions; successful structural checks do not prove
semantic conformance. Building a wheel from its sdist must retain the declaration.
