# Retool and Codex Integration Contract
#retool #content-pipeline

This document defines the current bridge between the Bastelschachtel Retool app and the future `blog-seo-pipeline` skill or plugin.

The goal is to preserve the current Retool operating model while making its artifacts fetchable and usable by Codex.

## Principle

Use a hybrid system:

- repo docs remain the canonical operating manual
- Retool Database remains the operational memory for generated content artifacts and approvals

This means:

- process, architecture, contracts, and workflow rules live in the repo
- live research runs, approvals, and future article-run records may live in Retool

## Why This Contract Exists

We do not want to connect Codex directly to whatever data happens to exist today without first defining what the integration expects.

This contract defines:

- which artifacts matter
- where they currently live
- how they are linked
- what the minimum useful fetch is for QA and refinement
- what is persisted today versus only held in Retool state

## Canonical Split of Responsibility

### Repo docs

Canonical for:

- workflow documentation
- operating process
- architecture
- content-generation rules
- QA expectations
- future skill behavior

### Retool / Retool Database

Canonical for:

- research dossiers
- saved approvals by keyword
- product catalog rows
- optional intelligence-hub artifacts
- future persisted briefs
- future persisted article markdown
- future run snapshots

## Current Integration Target

The immediate integration target is not full automation.

The first useful integration is:

1. retrieve a research dossier
2. retrieve or receive a generated brief
3. retrieve or receive generated article markdown
4. retrieve selected products
5. run Codex QA and refinement

## Artifact Inventory

### 1. Research dossier

Current canonical store:

- `research_dossiers`

One record maps to:

- one dossier
- one research run for a topic and `research_type`
- optionally scoped by competitor URL

Known fields:

- `id`
- `topic`
- `research_type`
- `competitor_url`
- `locale`
- `model`
- `max_sources`
- `prompt_override`
- `result_json`
- `status`
- `created_at`
- `updated_at`

Notes:

- `result_json` is a stringified JSON blob stored as `TEXT`
- app logic is legacy-compatible with `keyword` and `dossier_json` fallbacks

### 2. Brief

Current state is mixed.

Possible DB store:

- `content_briefs`

Known fields:

- `id`
- `title`
- `primary_keyword`
- `awareness_stage`
- `word_count`
- `brief_text`
- `created_at`

But current Content Factory behavior appears to keep the active brief primarily in Retool state and UI:

- `contentFactoryBriefJson`
- `strategicBriefMarkdown`

There is also browser-local fallback storage:

- `localStorage.savedBriefs`

Current conclusion:

- a brief may exist in DB, local browser storage, or only in live Retool state
- there is not yet a fully reliable persisted brief contract for generated Content Factory briefs

### 3. Article HTML

Current state:

- not persisted in DB

Current location:

- `rawArticleHtml`
- `postProcessArticleHtml`
- `articleResultTextArea.value`

Current conclusion:

- article markdown is currently an ephemeral artifact
- future integration should either persist it or expose it through a narrow API/workflow layer

### 4. Selected products

This exists in three forms.

#### Product catalog source of truth

Store:

- `product_catalog`

Known fields:

- `id`
- `handle`
- `title`
- `tags`
- `type`
- `vendor`
- `variant_sku`
- `variant_price_cents`
- `image_src`
- `image_alt_text`
- `display_title`
- `canonical_id_url`

#### Ephemeral editor lock-in set

Retool state:

- `lockedRelevantProducts`

Known fields:

- `include`
- `name`
- `handle`
- `image_url`
- `price`
- `score`

This is the product set used directly by the brief generator during an active run.

#### Persisted approvals by keyword

Store:

- `product_keyword_approvals`

Known fields:

- `approval_id`
- `keyword`
- `product_handle`
- `product_name`
- `image_url`
- `product_url`
- `search_url`
- `status`
- `updated_at`

Important identity rule:

- `approval_id = ${keyword}|${product_handle}`

### 5. Run metadata

There is no single dedicated runs table yet.

Current metadata is split across:

- `research_dossiers` for research-run metadata
- ephemeral article generation return payload for article-run metadata

Known article generation return shape:

```json
{
  "ok": true,
  "rawChars": 0,
  "finalChars": 0,
  "allowedProductLinks": 0,
  "citationsProvided": 0,
  "allowedSource": "selected",
  "archetype": "listicle",
  "model": "anthropic/claude-3.5-sonnet"
}
```

## Record Identity

Identity depends on artifact type.

### Research dossier identity

Primary key:

- `research_dossiers.id`

Natural key-like fields:

- `topic`
- `research_type`
- `locale`
- `competitor_url`

### Brief identity

Possible identities:

- `content_briefs.id`
- `brief.id` in browser local storage

### Selected product identity

Primary persisted identity:

- `product_keyword_approvals.approval_id`

Natural key:

- `keyword + product_handle`

### Article job identity

No persisted durable article ID exists yet.

Current implicit article-job identity is approximately:

- dossier id or dossier topic
- keyword
- format
- archetype
- selected products

If a durable job identifier is introduced later, it should likely include:

- dossier id
- keyword
- format
- archetype
- locale

or use a dedicated UUID with those fields attached.

## Lifecycle of Persistence

### Research Lab lifecycle

1. run live research
2. display result JSON in the UI
3. save dossier into `research_dossiers`
4. optionally route portions into Intelligence Hub tables

Known downstream routing targets:

- `keyword_data`
- `competitor_posts`
- `product_facts`

### Content Factory lifecycle

1. select dossier from `research_dossiers`
2. load dossier JSON into Retool state
3. search `product_catalog`
4. create and edit `lockedRelevantProducts`
5. generate brief into Retool state
6. optionally approve products into `product_keyword_approvals`
7. generate full article markdown into Retool state

Current limitation:

- brief and article are not yet fully persisted as stable DB artifacts in the observed implementation

## Linking Keys

### Dossier to downstream stages

Cleanest current linking key:

- `research_dossiers.id`

This is the best current parent key for a content job.

### Brief to dossier

No explicit DB-level foreign key is currently visible.

In practice the linkage is by:

- selected dossier in state
- topic or keyword inside the generated brief payload

### Article to dossier and brief

Current linkage is in-memory only:

- selected dossier
- selected topic
- selected brief state
- selected products state
- current format and archetype UI selections

### Selected products to keyword

Persisted link:

- `product_keyword_approvals.keyword`
- `product_keyword_approvals.product_handle`

## Minimum Useful Fetch for Codex QA

For Codex to QA one article end-to-end, the minimum useful retrieval set is:

1. research dossier row from `research_dossiers`
2. dossier JSON from `result_json`
3. generated brief
4. final article markdown
5. selected products used for the article

Useful optional additions:

6. `product_facts` rows for the dossier topic
7. citations list used to generate the source section
8. article-generation metadata such as model and char counts

## Current Practical Reality

Today, this means:

- dossier can be reliably fetched from DB
- selected keyword approvals can be fetched from DB
- product catalog can be fetched from DB
- brief may need to be passed manually unless we add persistence
- article markdown may need to be passed manually unless we add persistence

## Recommended Integration Phases

### Phase 1: manual-plus-fetch hybrid

Codex reads:

- repo docs
- dossier from Retool DB
- product approvals from Retool DB

The user provides:

- brief text
- final article markdown

This is enough to build the first QA-oriented version of `blog-seo-pipeline`.

### Phase 2: persist missing artifacts

Add stable storage for:

- generated brief
- final article markdown
- article run snapshots

At that point Codex can fetch a whole job with much less manual handoff.

### Phase 3: unified content-job layer

Introduce a single durable content-job record that links:

- dossier
- brief
- article
- selected products snapshot
- run metadata

## Suggested Normalized Future Schema

Not required yet, but likely desirable later:

- `content_runs`
- `content_run_products`
- `content_run_outputs`

Potential parent shape:

```json
{
  "run_id": "uuid",
  "dossier_id": "text",
  "topic": "text",
  "locale": "de-AT",
  "format": "listicle",
  "archetype": "listicle",
  "brief_model": "deepseek/...",
  "article_model": "anthropic/claude-3.5-sonnet",
  "status": "generated"
}
```

## Immediate Design Decision

We should not connect Codex directly to the DB before the `blog-seo-pipeline` knows which artifacts it expects.

This contract is the basis for that future connection.

## What the Future Skill Should Assume

For v1, the future `blog-seo-pipeline` should assume:

- process docs are read from the repo
- dossier can be fetched from Retool
- selected products can be fetched from Retool
- brief and article may still be supplied manually

That keeps the first version useful without waiting for full storage normalization.

## Status

Initial integration contract created on `2026-03-27` from the current Retool implementation summary, without direct database access.

