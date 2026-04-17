# Shopify collections cleanup runner (local)

This repo includes a small runner to **audit + propose + apply** Shopify collection cleanups with an approval gate.

## Credentials (do not store in this file)

Do **not** put tokens in this markdown file or commit them to git.

Create (or reuse) a local `.env` file at:

- `Code/shopify_api_work/.env`

Required keys:

```
SHOPIFY_STORE_URL=bastelschachtel.myshopify.com
SHOPIFY_API_VERSION=2026-01
SHOPIFY_ACCESS_TOKEN=shpat_...
```

## Config (curated vs taxonomy)

Copy the example config and edit locally:

- `Code/shopify_api_work/collections_cleanup_config.example.json`
- to `Code/shopify_api_work/collections_cleanup_config.json`

Current repo default `collections_cleanup_config.json` is checked in as a starting point. Adjust it for your store.

## Commands

List collections (id/handle/title + smart/manual + product count):

`python Code/shopify_api_work/collections_cleanup_runner.py list`

Inspect one collection:

`python Code/shopify_api_work/collections_cleanup_runner.py inspect --handle farben-veredelung`

Create a proposal JSON (no writes):

`python Code/shopify_api_work/collections_cleanup_runner.py propose --handle farben-veredelung`

Apply an approved proposal (writes):

`python Code/shopify_api_work/collections_cleanup_runner.py apply --proposal Code/shopify_api_work/out/proposal_farben-veredelung.json --yes`

Generate a MAIN-menu question queue (read-only):

`python Code/shopify_api_work/collections_cleanup_runner.py menu-audit`

## Umbrella verify suggestions

Some SMART collections are “umbrella” categories and should be verified against their ruleSet conditions (instead of strict title-keyword matching).

`python Code/shopify_api_work/collections_cleanup_runner.py umbrella-suggest`

Then copy the suggested handles into `verify_umbrella_handles` in `Code/shopify_api_work/collections_cleanup_config.json`.
