# Blogs

Use this guide when the end goal is a Bastelschachtel blog post.

## First Read Rule

Before using any Bastelschachtel reference folder, read that folder's `README.md` first when it exists.

This keeps the workflow stable even when dated files change.

Priority:
- read the folder `README.md`
- then use the rest of the folder as directed by that README
- do not hard-code one dated file as the permanent entrypoint when the folder is intended to evolve

## Core Bastelschachtel Flow

- `blog-seo-pipeline`
  Use this as the repo-specific anchor. It is built for the Bastelschachtel blog workflow, especially ingesting Retool research dossiers, briefs, and article HTML, validating SEO and logic quality, checking product-link integrity, and refining drafts.

## Bastelschachtel-Specific Inputs To Use First

Before drafting, pull from the docs that already contain real customer language and SEO direction.

- `docs/customer reviews/`
  Read `docs/customer reviews/README.md` first when it exists.
  Then use this folder for VOC, phrasing, pain points, confidence triggers, product quality language, review themes, category-level VOC priority, and product-family wording.

- `docs/seo/`
  Read `docs/seo/README.md` first when it exists.
  Then use this folder for Bastelschachtel's SEO direction, article priorities, category support strategy, master-article planning, category intros, copy framing, and linking logic.

## Before Writing

- `product-marketing-context`
  Use this first if product positioning, ICP, or messaging context is fuzzy. It keeps the post aligned with Bastelschachtel's actual audience and value prop.

- `content-strategy`
  Use this when the question is what to write, which topic to prioritize, which keyword cluster matters, or how the article fits into the broader content roadmap.

- `seo-audit`
  Use this when the real problem is diagnosing ranking or SEO issues, not drafting the next article.

- `ai-seo`
  Use this when the post should be structured to perform well in AI search and LLM citation workflows, not just traditional search.

## Writing And Improving The Article

- `copywriting`
  Use this for drafting or rewriting the article.

- `copy-editing`
  Use this for tightening an existing draft, sharpening phrasing, improving readability, and cleaning up weak sections.

## If The Post Is A Specific Type

- `competitor-alternatives`
  Use this for comparison posts, "alternative" pages, and head-to-head competitor content.

- `programmatic-seo`
  Use this for template-driven article or landing-page systems at scale.

- `schema-markup`
  Use this if the finished post should ship with structured data support.

## Recommended Sequence

1. Read `README.md` in the relevant Bastelschachtel reference folders first
2. Read the relevant materials in `docs/customer reviews/`
3. Read the relevant planning materials in `docs/seo/`
4. `content-strategy`
5. `blog-seo-pipeline`
6. `copywriting`
7. `copy-editing`
8. `ai-seo` or `schema-markup` if relevant

## Short Version

If you want the shortest answer: for Bastelschachtel specifically, start with the folder `README.md` files in the relevant reference folders, then use the VOC and SEO docs in those folders, then use `blog-seo-pipeline`, and use `copywriting` and `copy-editing` around it.
