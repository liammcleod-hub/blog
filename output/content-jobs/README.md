# Content Jobs

This folder stores standardized job bundles for the `blog-seo-pipeline`.

Each job bundle represents one article workflow instance and gives Codex a predictable place to read dossier, brief, article, product, and QA artifacts.

## Purpose

Use this folder when moving a Retool-generated content job into the Codex-side QA and refinement workflow.

## Structure

Create one folder per job:

- `output/content-jobs/<job-slug>/`

Each job folder should contain:

- `job.json`
- `research-dossier.json`
- `brief.md`
- `article.html`
- `selected-products.json`
- `qa-report.md`
- `revision-plan.md`
- `notes.md`

## Naming

Use a short stable slug, for example:

- `peddigrohr-listicle-de-at`
- `basteln-mit-kindern-ostern-deep-dive`

## Current Rule

For v1:

- `research-dossier.json`, `brief.md`, and `article.html` are the minimum useful files
- `selected-products.json` is strongly recommended
- `qa-report.md` and `revision-plan.md` are outputs created by Codex

## Template

Use `_template/` as the starter structure for a new content job.
