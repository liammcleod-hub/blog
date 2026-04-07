# Blog SEO Pipeline Plugin V1 Current State

Date: `2026-03-28`

## Purpose

This file captures the current implemented state of the `blog-seo-pipeline` plugin so work can resume cleanly in a later session.

## Implemented

- repo-local plugin scaffold exists under `plugins/blog-seo-pipeline/`
- plugin manifest exists and no longer contains placeholder TODO values
- `blog me this` entrypoint exists and runs locally
- local discovery exists for:
  - job folders
  - direct article markdown paths
- external discovery boundary exists and is now HTTP-backed
- mode selection exists for:
  - `qa-article`
  - `revise-article`
  - `audit-brief`
- v1 family classification exists for:
  - `deep-dive-guide`
  - `product-comparison`
  - `curation-listicle`
- structured QA analysis exists
- revision engine exists with validation-gated rewrite approval
- QA report and revision plan rendering exists
- revised HTML writing exists for `revise-article`
- template proposal generation exists
- plugin-owned base and family templates exist

## External Adapter State

The external adapter lives at:

- `plugins/blog-seo-pipeline/scripts/external_sources.py`

It is ready for a real read-only API, but no live Bastelschachtel content-pipeline HTTP API exists yet in the repo context used so far.

The adapter currently supports provisional lookup kinds:

- `external_dossier`
- `external_latest_keyword`
- `external_topic`

Current normalization rules:

- dossier output normalizes to `dossier_id`, `topic`, `locale`, `dossier`
- dossier payload prefers `result_json`, then falls back to `dossier_json`
- topic prefers `topic`, then falls back to legacy `keyword`
- product approval payloads normalize to `selected_products`

## Verification Status

Last verified on `2026-03-28`:

- `pytest plugins/blog-seo-pipeline/tests -q -p no:cacheprovider`
- result: `31 passed`

Verified command paths:

- QA path through `blog_me_this.py`
- revise path through `blog_me_this.py`

## Important Limitation

There is still no live HTTP endpoint set available for:

- base URL
- auth token
- known-good dossier id
- known-good topic query
- known-good latest-keyword endpoint

So the adapter is contract-aligned and tested, but not yet live-verified against deployed infrastructure.

## Next Correct Step

Build or expose the read-only Retool/API wrapper, then verify the adapter against real endpoints and real payloads.

The most likely canonical endpoints remain:

- `GET /content/research-dossiers/{id}`
- `GET /content/research-dossiers?topic=...`
- `GET /content/product-approvals?keyword=...`
- `GET /content/products?handles=...`
- optional `GET /content/product-facts?topic=...`

## Related Files

- `docs/superpowers/specs/2026-03-27-blog-seo-pipeline-plugin-v1-design.md`
- `docs/superpowers/plans/2026-03-27-blog-seo-pipeline-plugin-v1-implementation-plan.md`
- `docs/reference/content-pipeline/2026-03-28-retool-api-reality-check.md`
- `plugins/blog-seo-pipeline/README.md`

