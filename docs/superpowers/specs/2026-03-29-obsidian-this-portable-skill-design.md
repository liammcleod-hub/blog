# Obsidian This Portable Skill Design

Date: 2026-03-29
Status: Draft v1

## Purpose

Define a portable skill named `obsidian-this` that can be copied to other repos and make their markdown graph usable in Obsidian with minimal repo-specific setup.

The skill should start bare, learn the repo structure, create a small local config, and then maintain the graph over time without turning into a heavy PKM system.

The framework must remain agent-agnostic.

It should be usable from Codex, Claude, Gemini, or another CLI agent as long as that agent can:

- read markdown instructions
- run a local command
- work against a repo-local config file

## Core Goal

After installing the skill in a new repo, the user should be able to run:

- `$obsidian-this init`
- `$obsidian-this check`
- `$obsidian-this fix`

And get a repo-local Obsidian maintenance workflow that:

- identifies the markdown notes that should participate in the graph
- identifies folders and files that should stay out of the graph
- seeds a minimal navigation structure where needed
- keeps visible notes linkable and filterable
- applies only deterministic fixes

## Portable Design Principle

The skill must be global and reusable.

The repo-specific behavior must live in a small local config generated during `init`.

`obsidian-this` does not self-learn in the background.

Its only durable "learning" is the repo-local config it produces and then reuses.

That config becomes the basis for ongoing obsidianification in that repo.

That means:

- the skill logic is portable
- the repo config is local
- the repo can evolve without forking the skill

## What The Skill Should Manage

### 1. Navigation Structure

The skill should help repos converge on a lightweight structure:

- folder entrypoint notes where useful, usually `README.md`
- selective Obsidian wikilinks between visible notes
- plain-text paths for hidden or non-clickable targets

### 2. Graph Hygiene

The skill should detect and optionally fix:

- missing folder entrypoint notes in configured roots
- missing upward links to local entrypoints
- visible note targets written as non-clickable plain paths in navigation docs
- hidden or non-clickable targets written as fake clickable note links
- inconsistent tag placement in configured graph-facing docs

These checks should be enforced only in explicitly configured repo-facing navigation docs and approved graph-fixable notes, not indiscriminately across every markdown file in the repo.

### 3. Tag Hygiene

The skill should support a lightweight tag system for graph filtering.

It should not invent a large taxonomy.

Instead, it should:

- allow a repo-local approved tag list
- support per-zone default tags
- support special placement rules such as:
  - normal notes: tag line directly below H1
  - skill notes: bottom-only `#skills`
- refuse automatic top-tag insertion for notes that do not already have an H1

If a note has no H1, the skill should report that as a placement ambiguity rather than inventing a title or forcing a tag position.

### 4. Optional Markdown-Normalization Awareness

The skill should be able to scan for non-markdown docs that might be candidates for conversion, but it must not assume everything should be converted to `.md`.

This is repo-sensitive.

Some repos may have:

- `.txt` research or documentation notes that should become markdown
- `.html` or other files that are functional artifacts, fixtures, outputs, or pipeline inputs and must stay as they are

So the skill must distinguish:

- `candidate_for_markdown_normalization`
- `must_not_reformat_to_markdown`

This decision must be config-driven after repo scanning, not hardcoded globally.

In v1, this should remain primarily a reporting and classification surface, not an automatic rewrite surface.

## Non-Goals

The skill does not aim to:

- build a full second-brain system
- force every markdown file into the graph
- auto-tag everything in a repo
- blindly convert `.txt`, `.html`, or other file types into markdown
- rewrite prose for style
- create hidden-folder workarounds
- make repo-specific business decisions without config

## Commands

### 1. `init`

Bootstrap mode.

This should:

- scan the visible repo tree
- identify likely markdown-bearing zones
- identify likely forbidden zones such as generated output or templates
- identify obvious navigation docs such as root `README.md` and folder `README.md`
- create a local config file for this repo
- optionally propose a minimal first-wave setup

Output should include:

- proposed graph roots
- proposed forbidden roots
- proposed repo-facing navigation docs
- proposed tag zones
- proposed normalization exclusions

### 2. `check`

Read-only audit mode.

This should:

- load repo-local config
- audit link hygiene
- audit tag placement and approved-tag usage
- audit forbidden-zone safety
- optionally report markdown-normalization candidates and exclusions

It must not edit files.

### 3. `fix`

Deterministic maintenance mode.

This should:

- load repo-local config
- apply only approved deterministic fixes
- never expand into broad rewrites
- never touch forbidden zones
- never perform file-format normalization in v1

`fix` is for graph hygiene only.

If format normalization is ever added later, it should be a separate command surface with stricter review gates.

## Repo-Local Config

Each repo should get a small local config, for example:

- `.obsidian-this/config.json`

The config should be explicit and easy to diff.

This config is the only durable repo lesson the skill keeps.

After `init`, ongoing behavior should come from this config rather than repeated fresh guesswork.

Suggested fields:

- `graph_roots`
- `forbidden_roots`
- `repo_facing_navigation_docs`
- `tag_rules`
- `skill_note_rules`
- `normalization_candidates`
- `normalization_exclusions`
- `fix_permissions`

Example shape:

```json
{
  "graph_roots": [
    "docs/seo",
    "docs/reference",
    ".codex/memories/project"
  ],
  "forbidden_roots": [
    "output/generated",
    "templates"
  ],
  "repo_facing_navigation_docs": [
    "README.md",
    "docs/reference/README.md"
  ],
  "tag_rules": {
    "default_note_position": "below_h1",
    "allowed_tags": ["seo", "blog", "reference", "memory"],
    "zone_defaults": {
      "docs/seo": ["seo"],
      "docs/reference/skill-guides": ["skills"]
    }
  },
  "skill_note_rules": {
    "roots": ["repo-skills"],
    "bottom_only_tag": "#skills"
  },
  "normalization_candidates": [
    "docs/**/*.txt"
  ],
  "normalization_exclusions": [
    "output/**",
    "tests/fixtures/**",
    "**/*.html"
  ],
  "fix_permissions": {
    "allow_link_fixes": true,
    "allow_tag_fixes": true,
    "allow_format_normalization": false
  }
}
```

## Scope Model

The portable skill should use four classes:

### 1. Graph-Fixable Notes

Visible markdown notes the repo wants to maintain as part of the Obsidian graph.

This class should be bounded by explicit config.

### 2. Report-Only Notes

Notes that may be audited but must not be auto-fixed.

This includes cases like mirrored skill libraries.

### 3. Forbidden Zones

Areas that must not be touched by graph fixes.

Examples:

- generated outputs
- templates
- fixtures
- copied job bundles

### 4. Format-Normalization Candidates

Non-markdown docs that might be converted to markdown if the repo config explicitly allows it.

This class is separate from graph-fixable notes.

Being a candidate does not mean the skill should convert it automatically.

In v1, candidate status should only affect reporting and config proposals.

## Link Classification Model

The skill should enforce three link classes in graph-facing docs:

### 1. Visible Note Target

Use Obsidian wikilink syntax.

Example:

- `[[docs/seo/README]]`

### 2. Hidden Or Non-Clickable Target

Use plain path text or code formatting.

Example:

- `.agents/product-marketing-context.md`

### 3. Reference Syntax

Use plain code when the note is describing implementation or syntax rather than navigation.

This enforcement should run only in:

- `repo_facing_navigation_docs`
- approved graph-fixable notes that already participate in navigation structures such as related-doc sections

## Deterministic Fixes Allowed In v1

The portable framework should allow only small, explicit fixes:

- add missing upward link to configured local entrypoint
- add minimal related-doc block in deterministic cases
- normalize visible note references to wikilinks in repo-facing navigation docs
- downgrade fake clickable hidden targets to plain paths
- normalize tag placement according to repo config
- add configured bottom-only skill tag to visible skill notes

Tag placement normalization is allowed only when:

- the note already has an H1 and the configured rule is `below_h1`
- or the note matches configured bottom-only skill-note rules

## Forbidden Fixes In v1

The framework must never:

- infer broad topic relationships automatically
- mass-rewrite links across an entire repo
- convert file formats as part of `fix`
- rewrite generated artifacts
- touch hidden folders just to make them graph-visible
- change code, tests, or pipeline behavior as part of graph maintenance
- insert top tags into titleless notes

## Init Heuristics

`init` may use heuristics to propose config, but it must present them as proposals.

Reasonable signals:

- root or folder `README.md`
- markdown-heavy folders under `docs/`
- memory or notes folders
- output/template/test/fixture folders that should likely be forbidden
- visible skill-note trees
- non-markdown text docs that look documentation-like

But after `init`, the actual behavior must be config-driven.

## Review Surfaces

The skill should make its decisions inspectable.

`check` should clearly report:

- what roots were scanned
- what roots were forbidden
- what note classes were found
- what tag rules were applied
- what non-markdown files are only candidates versus excluded

## Portable Deliverables

The reusable package should contain:

- `SKILL.md`
- a small script entrypoint
- config template or config schema
- tests or fixtures for the generic behavior

It should not ship with Bastelschachtel-specific roots or tags baked in.

It also should not depend on a single agent vendor's command surface.

`obsidian-this` should be implementable as:

- repo-readable markdown instructions
- a neutral script entrypoint
- optional thin agent-specific wrappers, if desired later

## Bastelschachtel-Specific Note

The earlier markdown-reformat request about `.html` article files was repo-specific and should not be generalized into the portable skill.

In the portable framework, format normalization must always be:

- scanned
- classified
- explicitly approved by repo-local config

Never assumed from file extension alone.

## Bottom Line

`obsidian-this` should be a portable repo bootstrapper plus maintenance checker.

It should start with almost no assumptions, create a small explicit config, and then keep the repo’s Obsidian graph healthy without dragging in files or formats that do not belong there.
