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

Preferred file-bundle location:

- `output/content-jobs/<job-slug>/`

Preferred files:

- `job.json`
- `research-dossier.json`
- `brief.md`
- `article.html`
- `selected-products.json`
- `qa-report.md`
- `revision-plan.md`

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
- read the Bastelschachtel SEO audit and relevant SEO skill references when the topic depends on content-structure inference
- compare output against the brief and dossier
- compare output against the site's known content gaps and the query-type expectations implied by the SEO skills
- identify unsupported claims
- identify weak or missing product-link logic
- identify format and SEO mismatches
- propose or apply revisions

## Recommended Workflow

1. Create a new folder under `output/content-jobs/` using the `_template/` structure.
2. Drop the Retool dossier, brief, article, and selected products into that folder.
3. Run `qa-article` or `revise-article` against the bundle.
4. Save outputs back into `qa-report.md` and `revision-plan.md`.

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
