# Blog Cluster Engine Briefing Model

Date: 2026-03-29

## Core Decision

The future second plugin should not generate bloated, self-contained article briefs.

It should generate **lean, structured briefs** that reference canonical repo context.

## Why

This keeps the system:
- easier to maintain
- less repetitive
- less likely to drift
- more aligned with the latest Bastelschachtel strategy and VOC

Instead of copying the same brand, SEO, and VOC context into every brief, the brief should point the writing workflow to the right repo sources.

## System Boundary

### Repo docs own the truth

Canonical context should live in repo docs such as:
- folder `README.md` files
- `docs/customer reviews/`
- `docs/seo/`
- `.agents/product-marketing-context.md`
- relevant category, master-article, and template-library docs

### Plugin 2 owns orchestration

The future `blog-cluster-engine` should:
- expand a topic or master article into spinoff article opportunities
- assign cluster role
- choose the right template/style
- sequence execution
- create lean article briefs

### Writing skills own drafting

The actual article draft should then be created through:
- `copywriting`
- then improved through `copy-editing`

### Plugin 1 owns QA/refinement

`blog-seo-pipeline` remains the single-job quality engine for:
- QA
- revision
- product-link checks
- structured output discipline

## What A Lean Brief Should Include

A generated brief should include only the article-specific assignment data:

- topic
- primary intent
- target reader stage
- cluster role
- chosen template/style
- page purpose
- required internal-link targets
- required source folders/docs to read first
- article-specific constraints

## What A Lean Brief Should Not Include

Do not repeat:
- full brand context
- full VOC banks
- full SEO strategy dumps
- large copied sections from repo docs

That context should be referenced, not duplicated.

## Practical Workflow

1. Repo docs provide the stable context and template library.
2. `blog-cluster-engine` creates a lean brief for one spinoff article.
3. The writing workflow reads the referenced repo context first.
4. `copywriting` drafts the article.
5. `copy-editing` tightens it.
6. `blog-seo-pipeline` checks and refines the result when needed.

## Bottom Line

The second plugin should generate **minimal, structured, context-referencing briefs**.

It should not try to embed the entire Bastelschachtel operating system inside every article assignment.
