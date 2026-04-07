# Obsidian Check Skill Design

Date: 2026-03-29
Status: Draft v1

## Purpose

Define a maintenance skill named `obsidian-check` that can be run anytime to inspect the current state of the Bastelschachtel Obsidian-facing markdown graph and report link health across visible skill libraries and mirrors.

This skill should be safe to run repeatedly.

If the checked areas are already good, it should leave them unchanged.

## Why This Skill Exists

The repo now has a first-wave Bastelschachtel wikilink structure in the approved knowledge-bearing locations.

That structure needs a lightweight maintenance pass that can:

- confirm the graph remains healthy as docs evolve
- repair only the most deterministic small wikilink issues
- avoid rewriting documents unnecessarily
- separately expose dead-link problems in visible skill-library trees

Without this, the graph will slowly drift as new notes are added or edited.

## Goal

Build a skill that:

- checks the approved Bastelschachtel wikilink zones for hygiene problems
- optionally auto-fixes only the safest deterministic issues there
- reports broken relative links in visible skill-library trees
- never auto-fixes any skill-library tree
- exits cleanly with no edits when nothing is wrong

## Link Classification Model

For v1, `obsidian-check` should enforce three simple link classes.

### 1. Visible Obsidian Note Targets

If a path is meant to be opened inside Obsidian and the target note is visible in the vault, it should be written as an Obsidian wikilink.

Examples:

- `[[README]]`
- `[[docs/seo/README]]`
- `[[docs/reference/retool/architecture]]`

### 2. Hidden Or Non-Clickable Paths

If a path points to a hidden dotfolder target, a non-vault target, or any location that is not reliably clickable in Obsidian, it must not be presented as a clickable note link.

Examples:

- `.agents/product-marketing-context.md`
- `.agents/marketingskills/skills/paid-ads/SKILL.md`

These should be rendered as plain code paths or plain text paths, not as wikilinks.

### 3. Reference Syntax Mentions

If a document is describing a path, command, or implementation detail rather than trying to provide Obsidian navigation, it may use plain code formatting.

This is normal in specs, plans, and implementation notes.

## Non-Goals

This skill does not aim to:

- build or manage a full Obsidian vault architecture
- rewrite docs for style or content quality
- mass-convert plain markdown links to wikilinks everywhere
- auto-fix ambiguous note relationships
- touch generated or copied workflow artifacts
- auto-fix `repo-skills/marketing-library`
- solve hidden-dotfolder limitations in Obsidian

## Modes

The skill should support two modes:

### 1. `check`

Read-only mode.

The skill scans the target areas, reports findings, and makes no edits.

### 2. `check --fix`

Constrained auto-fix mode.

The skill may apply only the explicitly approved deterministic fixes in the Bastelschachtel wikilink zones.

It must still treat `repo-skills/marketing-library` as report-only.

## Scope Model

The skill operates across three separate domains with different permissions.

### A. Bastelschachtel Wikilink Zones

These are the only locations where auto-fix is allowed:

- `docs/seo/`
- `docs/customer reviews/`
- `docs/superpowers/specs/`
- `.codex/memories/bastelschachtel/`
- selected repo-owned `.agents/*.md` files such as:
  - `.agents/product-marketing-context.md`
- specific non-hidden entrypoint docs such as:
  - `output/content-jobs/README.md`
  - `docs/reference/skill-guides/blogs.md`
  - `docs/reference/skill-guides/README.md`

These are the knowledge-bearing zones the repo wants to keep Obsidian-friendly.

### B. Skill Library Audit Zones

These zones are report-only:

- `repo-skills/marketing-library/`
- other visible skill-library trees that may be added later

The skill may inspect and report broken relative links here, but must not edit files there in v1.

### C. Forbidden Artifact Zones

These zones are also report-only:

- `output/content-jobs/_template/`
- copied/generated content-job bundle notes

The skill may inspect these only through the separate forbidden-zone scan and must never edit them.

## File Types

### In Scope

- `.md`
- `SKILL.md`

### Out Of Scope

- `.json`
- `.html`
- `.csv`
- `.txt`
- `.docx`
- copied/generated content-job artifacts inside bundle folders
- files inside `output/content-jobs/_template/`

## Core Output Structure

The skill output should always be split into two report sections.

### Section 1: Graph Hygiene

This covers the approved Bastelschachtel wikilink zones.

The report should include:

- checked paths
- findings count by type
- whether any auto-fixes were applied
- any residual manual-review items

### Section 2: Skill Library Link Health

This covers visible skill-library trees such as `repo-skills/marketing-library`.

The report should include:

- broken relative links found
- whether the missing target is:
  - local reference missing
  - shared tools path missing
  - repo-root context path mismatch
- a short summary of whether each audited skill-library tree is currently safe for Obsidian browsing

### Section 3: Auto-Fix Summary

Only present this section in `check --fix` mode and only if a fix was actually applied.

Include:

- file touched
- exact class of fix
- whether verification passed after the edit

## Bastelschachtel Checks

These checks apply to the approved wikilink zones.

### 1. Folder Entrypoint Presence

If a target folder is supposed to have a `README.md`, verify it exists.

Target folders for v1:

- `docs/seo/`
- `docs/customer reviews/`
- `docs/superpowers/specs/`
- `.codex/memories/bastelschachtel/`

### 2. Upward Link Check

For important child docs inside a target folder, verify they link back to the local `README.md` when appropriate.

### 3. Entrypoint Link Quality

For entrypoint docs such as folder `README.md` files, verify:

- they contain explicit internal wikilinks
- they use path-qualified wikilinks for the main linked docs
- they do not use plain code formatting for visible markdown note targets that are clearly meant for navigation

### 4. Hidden Target Clickability Check

Flag repo-facing navigation docs that present hidden or non-clickable targets as if they were Obsidian-clickable notes.

Examples:

- `[[.agents/product-marketing-context]]`
- `[[.agents/marketingskills/skills/paid-ads/SKILL]]`

These should be reported as wrong link class usage.

### 5. Isolated Note Check

Flag approved in-scope notes that have no meaningful internal wikilinks at all.

This is a report-only condition unless the missing relationship is deterministic.

### 6. Link Density Sanity Check

Flag notes whose related-doc blocks look obviously stuffed or mechanically overlinked.

This is report-only in v1.

### 7. Out-Of-Scope Artifact Protection

Flag if wikilinks appear to have been added to locations that are intentionally excluded, such as:

- `output/content-jobs/_template/`
- copied job-bundle notes

This is report-only in v1.

## Mirror Checks

These checks apply only to visible skill-library trees.

### 1. Broken Relative Markdown Links

Scan markdown links and relative references inside `SKILL.md` files.

Flag links whose targets do not exist from the note's real path.

### 2. Shared Tools Dependency Gaps

Specifically detect the known class of mirror breakage where:

- a skill links to `../../tools/REGISTRY.md`
- or `../../tools/integrations/*.md`
- but the mirror does not include the `tools/` tree

This should be summarized separately because it is a structural skill-library issue, not an isolated bad link.

### 3. Local Reference Availability

Differentiate between:

- local `references/*.md` that resolve correctly
- mirror-shared links that fail because the mirror is incomplete

This helps avoid over-reporting healthy local references.

### 4. Skill Note Wikilink Opportunity Reporting

If a visible skill note contains no Obsidian wikilinks at all, the skill may report it as a future graph-enrichment opportunity.

This remains report-only in v1.

### 5. Hidden Skill Target Misclassification

If Bastelschachtel docs or visible skill-library notes present hidden `.agents/...` paths as if they were clickable Obsidian note links, report that mismatch.

This remains report-only in v1.

## Allowed Auto-Fixes In `check --fix`

Only these fixes are allowed in v1.

### 1. Add Missing Upward Link To Local README

When:

- the file is inside an approved target folder
- the corresponding folder `README.md` exists
- the backlink is clearly expected

The skill may add a small `Related Docs` block or append the missing upward link to an existing related-doc section.

### 2. Add Missing Related-Docs Block In A Deterministic Case

When:

- a target entrypoint clearly governs a child note
- or a current canonical pair already exists elsewhere in the repo pattern

The skill may add a minimal `Related Docs` block with only the deterministic links.

### 3. Normalize Entrypoint Links To Path-Qualified Wikilinks

When:

- the file is an approved entrypoint doc
- the link target is already known
- the only issue is that the entrypoint link is not path-qualified

The skill may rewrite just that link.

### 4. Downgrade Hidden Fake Click Targets To Plain Paths

When:

- the file is inside the approved Bastelschachtel fixable zones
- the target is under a hidden dotfolder such as `.agents/`
- the current syntax wrongly presents that target as clickable
- the replacement plain path is deterministic

The skill may rewrite only that target from clickable note syntax to plain code path syntax.

## Forbidden Auto-Fixes

The skill must never auto-fix:

- visible skill-library trees such as `repo-skills/marketing-library`
- `output/content-jobs/_template/`
- copied/generated content-job bundle files
- any relationship that requires interpretation or editorial judgment
- broad link rewrites across a whole document
- note-body prose unrelated to the missing link itself
- hidden-folder exposure workarounds

## Detection Heuristics

### Entrypoint Docs

Treat these as entrypoint docs:

- folder `README.md` files in approved target folders
- `docs/reference/skill-guides/README.md`
- `docs/reference/skill-guides/blogs.md`
- `output/content-jobs/README.md`

Treat these as repo-facing navigation docs for link-class enforcement:

- all approved entrypoint docs
- approved Bastelschachtel notes that already contain `Related Docs` or similar navigation sections
- other explicitly configured docs that serve as stable navigation surfaces

For implementation, this set should be explicit in config rather than inferred heuristically at runtime.

### Important Child Docs

For v1, treat these as important child docs:

- the explicitly linked notes from entrypoint docs
- the current first-wave canonical planning and synthesis docs already wired in the repo

The skill should not try to infer importance from every markdown file in scope.

## Verification After Auto-Fix

If a fix is applied, the skill must immediately re-run the relevant check on the touched file.

A fix only counts as successful if:

- the expected link now exists
- the link syntax is valid
- no forbidden files were touched

## Failure Behavior

If the skill encounters ambiguity, it should:

- report the issue
- skip the fix
- explain briefly why it was not safe to auto-fix

If the scan finds no issues, it should say so clearly and make no changes.

## Recommended Implementation Shape

The eventual implementation should be narrow and deterministic.

Suggested flow:

1. discover files in approved zones
2. classify files by scope and role
3. run Bastelschachtel hygiene checks
4. run skill-library link checks
5. optionally apply allowed fixes in Bastelschachtel zones only
6. re-verify touched files
7. print the structured report

## Open Questions

The implementation should validate these before expanding scope:

- whether `docs/reference/skill-guides/` should become a formal approved zone in the same class as `docs/seo/`
- whether the first-wave canonical child-doc list should be explicit in config rather than inferred from entrypoints
- whether `check --fix` should stage nothing and remain purely working-tree local
- whether skill-library link reporting should group identical structural failures to reduce noise

## Bottom Line

`obsidian-check` should be a repeatable maintenance skill, not a doc-rewrite engine.

It should keep the approved Bastelschachtel Obsidian-facing markdown graph healthy, apply only the safest fixes there, and separately expose link-health and wikilink-opportunity issues in visible skill-library trees without touching those trees.
