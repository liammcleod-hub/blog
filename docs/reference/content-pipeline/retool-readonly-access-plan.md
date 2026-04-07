# Retool Read-Only Access Plan
#content-pipeline #blog

This document defines the first safe integration path between Codex and Retool-backed data.

## Goal

Allow Codex to read the most valuable persisted artifacts without adding write-back complexity.

## Why Read-Only First

- lower operational risk
- no accidental mutation of production data
- enough value for dossier-grounded QA
- simpler implementation and permissions

## Priority Data Sources

### 1. `research_dossiers`

Purpose:

- fetch the dossier parent artifact
- retrieve `topic`, `locale`, `research_type`, and `result_json`

Why first:

- it is the strongest persisted research artifact in the current system

### 2. `product_keyword_approvals`

Purpose:

- fetch product approvals by keyword
- validate allowed product links

### 3. `product_catalog`

Purpose:

- validate product handles
- validate product URLs and images
- enrich product context when approvals are incomplete

### 4. Optional supporting tables

Useful later:

- `product_facts`
- `keyword_data`
- `competitor_posts`

## Still Manual in the First Connection

Even after read-only access is added, these may remain manual until persisted:

- generated brief
- final article markdown

## Access Options

### Option A: direct Retool Database read

Best when:

- you have a connection string
- the environment can reach the database
- you want simple SQL reads

Pros:

- straightforward
- minimal extra application layer

Cons:

- tighter coupling to schema details
- credentials and network need care

### Option B: thin read-only API or workflow wrapper

Best when:

- you want stable fetch endpoints
- you want to hide schema complexity from the skill
- you want easier future evolution

Pros:

- cleaner abstraction
- easier to change DB schema later

Cons:

- one more integration layer to maintain

## Recommended Sequence

1. Keep the repo docs as canonical process references.
2. Use the v1 ingest contract as the skill boundary.
3. Add read-only access for dossier and product data.
4. Keep brief and article markdown manual until stable persistence exists.
5. Only then consider broader automation.

## Recommended First Fetches

For one article QA task, the first connection should support:

- fetch dossier by `research_dossiers.id`
- fetch approvals by `keyword`
- fetch product catalog rows by `handle` or title match

That is enough to make the skill materially useful without redesigning the current Retool workflow.

