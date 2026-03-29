# Blog SEO Pipeline Plugin

Single-job content operating system for Bastelschachtel.

## V1 Scope

- discover content-job state from local or external hints
- normalize one job state
- choose `qa-article`, `revise-article`, or `audit-brief`
- classify one of the v1 canonical families
- write structured local outputs
- generate template-learning proposals

## V1 Canonical Families

- `deep-dive-guide`
- `product-comparison`
- `curation-listicle`

## Local Write Behavior

The plugin writes only to local job folders and plugin-owned templates.

## Retool Read-Only Adapter

External lookup is HTTP-backed and remains read-only.

The adapter is ready for a real API, but the Bastelschachtel content-pipeline HTTP layer is not yet live in this repo. Until that exists, external lookup remains contract-aligned rather than live-verified.

Supported provisional lookup kinds:

- `external_dossier`
- `external_latest_keyword`
- `external_topic`

Configuration:

- `BLOG_SEO_PIPELINE_RETOOL_BASE_URL`
- `BLOG_SEO_PIPELINE_RETOOL_API_TOKEN`
- `BLOG_SEO_PIPELINE_RETOOL_ROUTES_JSON`

`BLOG_SEO_PIPELINE_RETOOL_ROUTES_JSON` may override the provisional route map, for example:

```json
{
  "external_latest_keyword": "/content/keywords/latest-approved",
  "external_dossier": "/content/research-dossiers/{value}"
}
```

Canonical normalized output rules:

- dossiers normalize to `dossier_id`, `topic`, `locale`, `dossier`
- dossier payload prefers `result_json`, then falls back to `dossier_json`
- topic prefers `topic`, then falls back to legacy `keyword`
- latest-keyword/product-approval lookups normalize product rows under `selected_products`

## Templates

Plugin-owned templates live under:

- `templates/base/`
- `templates/families/`

These are seeded from repo references, but they are the operational source of truth for the plugin.

## Dry Run

Example:

```powershell
python plugins/blog-seo-pipeline/scripts/blog_me_this.py "blog me this output/content-jobs/peddigrohr-anfaenger-guide-de-at"
```
