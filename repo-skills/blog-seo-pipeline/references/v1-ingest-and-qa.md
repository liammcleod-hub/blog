# V1 Ingest and QA

This reference defines the first practical scope of `blog-seo-pipeline`.

## Goal

Make Codex immediately useful without waiting for full Retool persistence.

## Inputs Expected in V1

Required minimum:

- research dossier
- brief
- article HTML

Useful addition:

- selected products

## Normalized Working Shape

The skill should normalize incoming work into this conceptual shape:

```json
{
  "topic": "",
  "locale": "",
  "format": "",
  "archetype": "",
  "research_dossier": {},
  "brief": "",
  "article_html": "",
  "selected_products": []
}
```

## What V1 Should Do

- read the dossier for grounding
- read the brief for intent and structure
- read the HTML for actual output
- compare output against the brief and dossier
- identify unsupported claims
- identify weak or missing product-link logic
- identify format and SEO mismatches
- propose or apply revisions

## What V1 Should Not Depend On

- persisted article HTML in Retool DB
- guaranteed persisted brief storage
- write access to Retool DB

## Acceptance Standard

V1 is successful if Codex can review one article run and reliably answer:

- Is this article actually supported by the research?
- Does it follow the brief?
- Are the product links coherent?
- Is it structurally strong enough to publish after revision?
