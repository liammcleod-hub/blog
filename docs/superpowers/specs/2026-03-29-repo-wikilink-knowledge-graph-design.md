# Repo Wikilink Knowledge Graph Design

Date: 2026-03-29
Status: Draft v1

## Purpose

Define a repo-native markdown knowledge graph that works well for both:

- human navigation in Obsidian
- deterministic plugin context discovery inside this repo

This spec does not yet finalize Obsidian-specific style details. A follow-up research pass will refine link syntax and best practices using current Obsidian community guidance.

## Problem

The repo is gaining more strategy docs, SEO docs, VOC docs, content-job artifacts, memory docs, and plugin-related specs.

Right now, plugin discovery depends too much on:

- direct file references inside `SKILL.md`
- remembered file names
- manual repo navigation

That creates drift. New high-value docs can be added to the repo without becoming visible to the workflows that should use them.

## Goal

Create a lightweight, structured markdown graph so that:

- humans can navigate the repo in Obsidian using wiki links
- plugins can discover relevant newer docs without hardcoding every filename
- canonical docs stay distinct from generated artifacts
- `README.md` files remain the stable entrypoints

## Non-Goals

This phase does not aim to:

- convert every markdown file in the repo immediately
- make generated outputs equal in authority to canonical docs
- replace `SKILL.md` files with free-form graph traversal
- make plugins depend on the Obsidian desktop app or Obsidian CLI

## Core Decisions

### 1. README-first remains the entry model

Every important knowledge-bearing folder should have a `README.md`.

Plugins should start there before traversing deeper into the graph.

### 2. Wikilinks will be used in the knowledge-bearing markdown layers

The primary target areas are:

- `docs/`
- `.codex/memories/`
- selected `.agents/` markdown docs
- `output/content-jobs/` as an artifact layer

This is not a repo-wide mandate for all markdown files immediately.

### 3. Canonical docs and artifacts are both in the graph, but not equal

The repo needs two graph layers:

- `truth zone`: canonical strategy, context, research, operating docs
- `artifact zone`: generated outputs, content-job bundles, live execution artifacts

Artifacts must be discoverable, but plugins should prefer canonical docs first unless the task is explicitly artifact-oriented.

### 4. Plugins should use traversal rules, not filename memory

The long-term plugin behavior should be:

1. read the nearest relevant `README.md`
2. read linked canonical docs first
3. read related docs next
4. enter artifact docs only when task-relevant
5. stop at a bounded traversal depth

### 5. Obsidian compatibility is a feature, not a runtime dependency

This repo should be pleasant to use in Obsidian, but the plugin system must remain repo-native and markdown-native.

No plugin should require:

- Obsidian desktop to be running
- Obsidian CLI
- vault-only features that cannot be interpreted from plain markdown

## Information Architecture Model

### Truth Zone

These are the main candidate truth-zone areas:

- `docs/customer reviews/`
- `docs/seo/`
- `docs/reference/`
- `docs/strategy/`
- `docs/superpowers/`
- `.codex/memories/bastelschachtel/`
- `.agents/product-marketing-context.md`

Truth-zone documents should be treated as the preferred source of current reasoning, strategy, and workflow context.

### Artifact Zone

These are the main candidate artifact-zone areas:

- `output/content-jobs/`
- other generated output directories that may later be added

Artifact-zone documents are still valuable because they can feed:

- blog QA and revision
- repurposing into email and lead magnets
- cluster expansion
- future derivative workflows

But artifact-zone docs should not silently override canonical strategy docs.

## Folder README Contract

Every important folder `README.md` should eventually standardize these sections:

- `Purpose`
- `Canonical Docs`
- `Related Docs`
- `Generated Artifacts`
- `See Also`

Not every folder needs every section immediately, but this is the target shape.

### Section Intent

#### Purpose

Explains what the folder is for and what kind of material belongs there.

#### Canonical Docs

Links to the highest-trust documents in that folder or adjacent folders.

These should be the first documents plugins read after the `README.md`.

#### Related Docs

Links to adjacent supporting docs that add nuance, detail, or neighboring context.

#### Generated Artifacts

Links to outputs, work products, or execution artifacts that may be useful later but are not the authoritative source of strategy.

#### See Also

Links outward to other folders or systems that often pair with this one.

## Traversal Rules For Plugins

This section defines the intended future behavior for plugin and skill discovery logic.

### Default Priority Order

1. directly user-referenced document or folder
2. nearest folder `README.md`
3. `Canonical Docs`
4. `Related Docs`
5. `Generated Artifacts`
6. broader `See Also` links

### Default Preference Rules

- prefer truth-zone docs before artifact-zone docs
- treat artifacts as first-class only for:
  - QA
  - revision
  - repurposing
  - publishing
  - explicit job-specific tasks
- do not traverse the graph indefinitely

### Bounded Traversal

The final traversal rules will be refined later, but the system should include:

- a maximum hop depth
- a maximum number of loaded docs
- a preference for high-signal sections before free exploration

This prevents plugins from over-reading low-value material.

## Minimal Metadata Direction

Wikilinks alone are not enough for deterministic plugin behavior.

The repo should gradually adopt lightweight machine-readable metadata for important documents.

Possible fields:

- `title`
- `type`
- `status`
- `priority`
- `aliases`
- `canonical_for`
- `related`

This will be refined after the Obsidian best-practices review.

## Initial Scope

The first implementation wave should target the highest-value folders:

- `docs/seo/`
- `docs/customer reviews/`
- `docs/superpowers/specs/`
- `output/content-jobs/`
- `.codex/memories/bastelschachtel/`

Then selected files such as:

- `.agents/product-marketing-context.md`

## Proposed Rollout

### Phase 1: Convention Spec

- write and approve this design spec
- research Obsidian-style wikilink best practices
- refine naming, metadata, and linking conventions

### Phase 2: README Standardization

- update folder `README.md` files to the target section model
- ensure key folders expose canonical docs and artifact links clearly

### Phase 3: Link Conversion

- add wiki links to the highest-value docs first
- avoid bulk converting low-value or generated material without a reason

### Phase 4: Plugin Traversal Adoption

- update relevant skills/plugins to use `README.md` plus graph traversal
- keep traversal bounded and priority-driven

## Risks

### Graph Noise

If too many low-value files become equally linked, plugin context quality will get worse.

### Authority Drift

If artifacts are treated the same as canonical docs, stale execution outputs may override current strategy.

### Naming Drift

If filenames and note names vary wildly, wiki links become brittle and aliases become harder to maintain.

### Over-Implementation

Trying to convert the entire repo in one pass will create low-quality linking and unnecessary churn.

## Current Recommendation

Proceed with:

- `README-first`
- wiki links in the knowledge-bearing markdown layers
- explicit truth-zone vs artifact-zone distinction
- structured folder `README.md` sections
- bounded plugin traversal

Do not proceed with:

- repo-wide indiscriminate conversion
- Obsidian-only assumptions
- unbounded graph traversal

## Open Items For The Next Research Pass

The following still need to be refined using current Obsidian community guidance:

- exact wiki link syntax conventions
- filename vs title conventions
- alias usage rules
- frontmatter field shape
- whether headings and block references should be used routinely
- how much backlink-style linking is worth standardizing

## Bottom Line

The repo should become an Obsidian-friendly, plugin-traversable markdown knowledge graph.

The stable model is:

- `README.md` first
- canonical docs before artifacts
- wiki links for navigation and discovery
- lightweight metadata for determinism
- bounded traversal for plugin quality
