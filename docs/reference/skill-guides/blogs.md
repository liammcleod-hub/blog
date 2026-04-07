# Blogs
#skills #blog

Use this guide when the end goal is a Bastelschachtel blog post.

## First Read Rule

Before using any Bastelschachtel reference folder, read that folder's `README.md` first when it exists.

This keeps the workflow stable even when dated files change.

Priority:
- read the folder `README.md`
- then use the rest of the folder as directed by that README
- do not hard-code one dated file as the permanent entrypoint when the folder is intended to evolve

## Core Bastelschachtel Flow

- `.agents/skills/blog-seo-pipeline/SKILL`
  Use this as the repo-specific anchor. It is built for the Bastelschachtel blog workflow, especially ingesting Retool research dossiers, briefs, and article markdown, validating SEO and logic quality, checking product-link integrity, and refining drafts.

## Bastelschachtel-Specific Inputs To Use First

Before drafting, pull from the docs that already contain real customer language and SEO direction.

- [[docs/customer reviews/README]]
  Read this first when it exists.
  Then use this folder for VOC, phrasing, pain points, confidence triggers, product quality language, review themes, category-level VOC priority, and product-family wording.

- [[docs/seo/README]]
  Read this first when it exists.
  Then use this folder for Bastelschachtel's SEO direction, article priorities, category support strategy, master-article planning, category intros, copy framing, and linking logic.

## Before Writing

- `.agents/marketingskills/skills/product-marketing-context/SKILL.md`
  Use this first if product positioning, ICP, or messaging context is fuzzy. It keeps the post aligned with Bastelschachtel's actual audience and value prop.

- `.agents/marketingskills/skills/content-strategy/SKILL.md`
  Use this when the question is what to write, which topic to prioritize, which keyword cluster matters, or how the article fits into the broader content roadmap.

- `.agents/marketingskills/skills/seo-audit/SKILL.md`
  Use this when the real problem is diagnosing ranking or SEO issues, not drafting the next article.

- `.agents/marketingskills/skills/ai-seo/SKILL.md`
  Use this when the post should be structured to perform well in AI search and LLM citation workflows, not just traditional search.

## Writing And Improving The Article

- `.agents/marketingskills/skills/copywriting/SKILL.md`
  Use this for drafting or rewriting the article.

- `.agents/marketingskills/skills/copy-editing/SKILL.md`
  Use this for tightening an existing draft, sharpening phrasing, improving readability, and cleaning up weak sections.

## If The Post Is A Specific Type

- `.agents/marketingskills/skills/competitor-alternatives/SKILL.md`
  Use this for comparison posts, "alternative" pages, and head-to-head competitor content.

- `.agents/marketingskills/skills/programmatic-seo/SKILL.md`
  Use this for template-driven article or landing-page systems at scale.

- `.agents/marketingskills/skills/schema-markup/SKILL.md`
  Use this if the finished post should ship with structured data support.

## Recommended Sequence

1. Read `README.md` in the relevant Bastelschachtel reference folders first
2. Read the relevant materials in [[docs/customer reviews/README]]
3. Read the relevant planning materials in [[docs/seo/README]]
4. `.agents/marketingskills/skills/content-strategy/SKILL.md`
5. `.agents/skills/blog-seo-pipeline/SKILL`
6. `.agents/marketingskills/skills/copywriting/SKILL.md`
7. `.agents/marketingskills/skills/copy-editing/SKILL.md`
8. `.agents/marketingskills/skills/ai-seo/SKILL.md` or `.agents/marketingskills/skills/schema-markup/SKILL.md` if relevant

## Short Version

If you want the shortest answer: for Bastelschachtel specifically, start with the folder `README.md` files in the relevant reference folders, then use the VOC and SEO docs in those folders, then use `.agents/skills/blog-seo-pipeline/SKILL`, and use `.agents/marketingskills/skills/copywriting/SKILL.md` and `.agents/marketingskills/skills/copy-editing/SKILL.md` around it.

## Graph Anchor

This note is part of the skill-guide graph. Start from [[docs/reference/skill-guides/README|Skill Guides]] when you need the master entrypoint.

