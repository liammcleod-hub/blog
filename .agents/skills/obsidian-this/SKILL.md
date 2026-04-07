---
name: obsidian-this
description: Use when making a repo Obsidian-friendly, bootstrapping repo-local graph config, auditing wikilinks and tags, or applying small deterministic graph-hygiene fixes without turning the repo into a full PKM system.
---

# Obsidian This

Portable Obsidian graph bootstrapper and maintenance skill.

This skill does not self-learn in the background.

Its only durable repo lesson is the local config it creates and then reuses.

This file is a Codex-friendly wrapper.

The actual portable execution surface is the local script plus repo-local config, so the same bundle can be used from Claude, Gemini, or another CLI agent too.

## Commands

- `init`
  Scan the visible repo, propose graph roots and exclusions, and write `.obsidian-this/config.json`.
- `check`
  Audit graph hygiene, link classes, tag placement, and forbidden-zone safety from config.
- `fix`
  Apply only deterministic graph-hygiene fixes from config. No file-format normalization in v1.

## Use This Skill For

- making a markdown-heavy repo usable in Obsidian
- bootstrapping folder entrypoints and repo-facing navigation docs
- checking visible-note links versus hidden-path references
- maintaining lightweight hashtag placement rules
- keeping visible skill notes on a bottom-only `#skills` convention
- classifying markdown-normalization candidates versus exclusions

## Do Not Use This Skill For

- broad knowledge-management architecture work
- style rewriting
- blind `.txt` or `.html` to `.md` conversion
- changing generated artifacts
- exposing hidden folders just for graph visibility

## Portable Rule

The skill logic is reusable.

The repo-specific behavior lives in `.obsidian-this/config.json`.
