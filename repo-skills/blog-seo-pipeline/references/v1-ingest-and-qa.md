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

For tutorial-heavy topics, explicitly verify that the article teaches the reader how to start, not just what to buy.

For article HTML, also verify layout rhythm at the markup level:

- the first major heading after a special block like `.ai-summary` should not rely on naked theme defaults
- special sections should use explicit classes instead of bare `<section>` tags when spacing consistency matters
- major sections should keep consistent vertical rhythm relative to both the previous paragraph and the next heading
- no malformed HTML causes a link to swallow following paragraphs or sections
- German output is free of mojibake and UTF-8 corruption
- anchor text truthfully matches the linked product or set
- visible source sections are optional in publishable output; internal provenance can stay in repo artifacts instead
- if multiple product showcase images appear, verify that they render consistently and do not crop important product content

## Recommended Workflow

1. Create a new folder under `output/content-jobs/` using the `_template/` structure.
2. Drop the Retool dossier, brief, article, and selected products into that folder.
3. Run `qa-article` or `revise-article` against the bundle.
4. Save outputs back into `qa-report.md` and `revision-plan.md`.

## Link Placement Check

For commerce-tutorial guides, do not stop at verifying whether links work.

Also verify whether links are placed where the reader naturally needs them:

- link key material phrases inline when matching approved products exist
- link first meaningful mentions of sizes or variants like `2mm` and `3mm` when those are product-relevant
- prefer 2-4 useful inline links over an end-of-article link dump

If repeated key phrases remain unlinked while a matching selected product exists, flag that as a revision opportunity.

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
