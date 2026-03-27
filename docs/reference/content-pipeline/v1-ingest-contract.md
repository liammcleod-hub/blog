# Blog SEO Pipeline V1 Ingest Contract

This document defines the first narrow contract for running the `blog-seo-pipeline` skill.

The goal is to make the skill useful immediately without waiting for full Retool persistence or a live database integration.

## V1 Purpose

V1 is a QA and refinement layer for content already generated in Retool.

It does not yet own the whole content production process.

## Inputs

### Required

- `research_dossier`
- `brief`
- `article_html`

### Recommended

- `selected_products`

### Optional

- `format`
- `archetype`
- `locale`
- `dossier_id`
- `brief_model`
- `article_model`

## Accepted Sources

### Research dossier

Accepted as either:

- raw JSON payload
- `research_dossiers.id` plus fetched `result_json`

### Brief

Accepted as either:

- markdown brief text
- JSON brief payload
- `brief_text` from a persisted brief, if available

### Article HTML

Accepted as:

- final generated HTML string

### Selected products

Accepted as either:

- explicit selected product list for the run
- approved product list for the keyword

## Normalized Working Object

Internally, the pipeline should normalize the job to this shape:

```json
{
  "topic": "",
  "locale": "de-AT",
  "format": "",
  "archetype": "",
  "dossier_id": "",
  "research_dossier": {},
  "brief": "",
  "article_html": "",
  "selected_products": [],
  "brief_model": "",
  "article_model": ""
}
```

## Required Validation Tasks

V1 should perform these checks:

1. Dossier grounding
Verify the article’s claims and assertions are supported by the research dossier or clearly framed as opinion or recommendation.

2. Brief alignment
Verify the final article matches the intended angle, format, outline logic, key takeaways, and SEO targets.

3. Product integrity
Verify product names, handles, URLs, and image usage align with selected or approved products.

4. Structure and format integrity
Verify the article format matches the selected mode such as listicle or deep dive.

5. SEO coverage
Verify primary keyword alignment, reasonable secondary coverage, meta coherence if present, and useful section structure.

6. Source integrity
Verify the source section and citations remain coherent with the dossier’s available citations.

## Outputs

The pipeline may return one or more of:

- QA report
- prioritized findings list
- revision plan
- improved HTML article
- optional plain-language summary for the operator

## Non-Goals for V1

V1 does not require:

- write-back to Retool DB
- automatic article persistence
- automatic brief persistence
- full keyword planning or content calendar orchestration

## Operating Assumption

Until persistence improves, the user may still provide the brief and final article manually even if the dossier and product data are fetched from Retool-backed systems.
