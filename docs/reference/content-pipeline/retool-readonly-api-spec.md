# Retool Read-Only API Spec
#content-pipeline #blog

This document proposes a thin read-only API surface for the future `blog-seo-pipeline`.

It is intentionally narrower than the raw Retool schema. The goal is to give Codex stable objects to fetch even if the underlying Retool tables evolve.

## Design Goal

Expose only the minimum endpoints needed for article QA and refinement.

## Recommended Endpoints

### 1. Get research dossier

`GET /content/research-dossiers/{dossier_id}`

Returns:

```json
{
  "id": "text",
  "topic": "text",
  "research_type": "text",
  "locale": "de-AT",
  "model": "text",
  "max_sources": 10,
  "status": "complete",
  "created_at": "timestamp",
  "updated_at": "timestamp",
  "result_json": {}
}
```

### 2. List research dossiers by topic

`GET /content/research-dossiers?topic={topic}&locale={locale}`

Returns:

- dossier summaries
- enough metadata to choose the right dossier

### 3. Get approved products by keyword

`GET /content/product-approvals?keyword={keyword}`

Returns:

```json
{
  "keyword": "text",
  "products": [
    {
      "approval_id": "text",
      "product_handle": "text",
      "product_name": "text",
      "image_url": "text",
      "product_url": "text",
      "search_url": "text",
      "status": "Use Product Link",
      "updated_at": "date"
    }
  ]
}
```

### 4. Get product catalog entries

`GET /content/products?handles=a,b,c`

Returns:

```json
{
  "products": [
    {
      "handle": "text",
      "title": "text",
      "display_title": "text",
      "image_src": "text",
      "image_alt_text": "text",
      "variant_price_cents": 0,
      "canonical_id_url": "text"
    }
  ]
}
```

### 5. Optional topic facts

`GET /content/product-facts?topic={topic}`

Returns:

- normalized fact rows useful for grounding product and topic claims

## Optional Future Endpoints

These are not required for v1, but become useful once persistence improves.

### Get saved brief

`GET /content/briefs/{brief_id}`

### Get article run

`GET /content/article-runs/{run_id}`

### Get full content job

`GET /content/jobs/{job_id}`

This future endpoint would ideally return:

- dossier
- brief
- article markdown
- selected products
- run metadata

## Why an API Wrapper Is Attractive

Compared with direct DB reads, this wrapper:

- hides schema quirks such as text-serialized JSON
- abstracts legacy fallback fields
- reduces skill coupling to raw table structure
- makes later persistence changes easier

## Mapping to Current Tables

Recommended initial mappings:

- `GET /content/research-dossiers/{dossier_id}` -> `research_dossiers`
- `GET /content/product-approvals?keyword=...` -> `product_keyword_approvals`
- `GET /content/products?...` -> `product_catalog`
- `GET /content/product-facts?topic=...` -> `product_facts`

## V1 Implementation Principle

If you build a thin read-only wrapper, keep it boring:

- read-only
- explicit endpoint shapes
- no transformation beyond normalization
- no write-back side effects

