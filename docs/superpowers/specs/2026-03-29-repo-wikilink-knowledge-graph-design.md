# Repo Wikilink Incorporation Design

Date: 2026-03-29
Status: Draft v3

## Purpose

Define how targeted folders and files in this repo should gain simple Obsidian wikilinks so they reference each other clearly.

This spec is only about adding and maintaining those wikilinks.

## Problem

Important markdown docs exist across the repo, but many of the high-value files and folder entrypoints do not explicitly reference each other.

That makes related material harder to navigate and easier to miss.

## Goal

For the targeted folders and files:

- add explicit wikilinks between related notes
- ensure folder entrypoints point to their important child docs
- ensure important child docs point back to their folder entrypoints
- add a small number of high-signal cross-links between adjacent notes
- do all of this additively, without restructuring the repo around a larger system

## Non-Goals

This spec does not aim to:

- convert the whole repo at once
- force every markdown file in the repo into this system immediately
- rely on Obsidian-specific features beyond normal wikilinks

## Target Scope

Initial target folders:

- `docs/seo/`
- `docs/customer reviews/`
- `docs/superpowers/specs/`
- `output/content-jobs/`
- `.codex/memories/bastelschachtel/`

Initial target standalone files:

- `.agents/product-marketing-context.md`

More files can be included later, but this spec only requires link work inside the targeted set.

## Core Model

The model is simple:

- targeted folder `README.md` files link to relevant docs in that folder and to closely related entrypoints outside the folder
- targeted docs link back to their governing folder `README.md` when one exists
- targeted docs also link to a few directly related sibling or adjacent docs when the relationship is real and useful

That is enough.

No extra abstraction should be added to the spec.

## Wikilink Format

Use Obsidian wikilinks as the default internal link format in the targeted markdown:

- `[[target-note]]`
- `[[path/to/target-note]]`
- `[[path/to/target-note#Heading]]`
- `[[path/to/target-note|Display Text]]`

Markdown links remain fine for:

- external URLs
- non-note file downloads where the literal extension matters

## Link Shape Rules

### Path-Qualified By Default In Entrypoints

Use path-qualified wikilinks in:

- folder `README.md` files
- shared entrypoint docs
- any place where target ambiguity is possible

### Bare Links Only When Clearly Safe

Bare wikilinks are acceptable only when the target is obviously unique and local.

### Display Text Sparingly

Use `[[target|display text]]` only when prose needs it.

Do not hide the underlying target unnecessarily.

### Heading Links Only When Stable

Use heading links when they point to stable sections that are likely to remain valid.

## Additive Linking Logic

This is the main rule set for implementation.

### 1. Add, Do Not Re-Architect

The task is to add links to existing files and folder entrypoints.

Do not introduce a new taxonomy or conceptual system just to justify the links.

### 2. Prefer Existing Structure

If a note already has a suitable section such as:

- `Related Docs`
- `See Also`
- `Canonical Docs`
- `Context`

add the new wikilinks there instead of inventing a new structure.

If no suitable section exists, add a small neutral section such as `Related Docs` or `See Also`.

### 3. Folder README First

For each targeted folder with a `README.md`:

- add links to the most important docs inside that folder
- add links to nearby related entrypoints outside that folder when that relationship is useful
- keep the README readable and selective

The folder `README.md` is the primary local hub, not an exhaustive directory dump.

### 4. Child Docs Link Back Up

For each targeted child doc under a targeted folder:

- link back to the local folder `README.md`

This creates obvious upward navigation and prevents isolated notes.

### 5. Add Lateral Links Only When The Relationship Is Direct

Add note-to-note links only when one of these is true:

- one note depends on the other for context
- one note is a direct continuation or refinement of the other
- both notes are routinely used together
- one note is the nearest relevant reference for the reader of the other

Do not add lateral links just because two files live near each other.

### 6. Keep Links Sparse And High-Signal

Each targeted note should usually gain:

- one upward link to its folder `README.md` when applicable
- a small number of sideways links to directly related notes

Avoid dense link dumps that make every note reference everything nearby.

### 7. Add Links Reciprocally When It Helps

If file A clearly points to file B, consider whether file B should also point back to file A.

Reciprocal links are good when they improve navigation.

They are not required when the reverse link would be noisy or redundant.

### 8. Preserve Existing Meaning

Do not rewrite a note's purpose just to make it fit a link structure.

Add links around the existing meaning of the document.

### 9. Do Not Promote Incidental Files

Not every markdown file deserves new links.

Only add links for the targeted folders and files, plus the directly related notes needed to connect them cleanly.

### 10. Avoid Link Stuffing

If a link does not help a real reader move to the next likely note, do not add it.

## Minimum Linking Expectations

For a targeted folder with a `README.md`:

- the `README.md` should link to its key docs
- key docs should link back to the `README.md`

For a targeted standalone file:

- it should link to the most relevant folder entrypoint or closely related note
- at least one targeted note should link back to it when that relationship is meaningful

The aim is not perfect symmetry.

The aim is that targeted notes no longer sit alone.

## Authoring Guidance

### Folder READMEs

Use them to expose:

- what the folder is for
- which docs matter most
- which adjacent folders or entrypoints are most relevant

Prefer path-qualified links here.

### Canonical Or Important Docs

Add:

- a link back to the folder `README.md`
- a few high-signal related note links

Do not turn them into directories.

### Artifact-Like Docs

If a targeted artifact-style note is included, it should mainly link:

- back to its local entrypoint
- to the source context that explains why it exists

It should not become a hub unless that is its actual role.

## Rollout

### Phase 1

- approve this narrow wikilink-only spec

### Phase 2

- add or update wikilinks in the targeted folder `README.md` files

### Phase 3

- add reciprocal and lateral wikilinks in the targeted child docs

### Phase 4

- review for noise, ambiguity, and missing backlink paths

## Review Checklist

When editing a targeted note or folder entrypoint, check:

- does this file now link to the most relevant related notes
- does it link upward to its folder `README.md` when applicable
- are the added links selective rather than exhaustive
- are ambiguous links path-qualified
- was the linking added without inventing extra machinery

## Bottom Line

This spec is only about adding simple Obsidian wikilinks between the targeted folders and files so they reference each other cleanly.

The implementation work is additive linking, nothing more.

## Related Docs

- [[docs/superpowers/specs/README]]
- [[docs/reference/skill-guides/blogs|Blogs]]
