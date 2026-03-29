# Blog SEO Pipeline Plugin Next-Step Memo

Date: 2026-03-29

## Current State

The `blog-seo-pipeline` plugin is locally real and mostly not the blocker anymore.

What is already true:
- repo-local plugin scaffold exists under `plugins/blog-seo-pipeline/`
- plugin manifest exists
- local runtime exists for discovery, mode selection, family classification, QA, revision, output rendering, and template proposals
- plugin-owned templates exist
- local tests pass:
  - `pytest plugins/blog-seo-pipeline/tests -q -p no:cacheprovider`
  - result: `31 passed`

The plugin is therefore ready as a local single-job engine.

## What Is Still Blocked

The unresolved piece is not the plugin scaffold.

The unresolved piece is the live read-only integration target.

Right now, the external adapter is:
- contract-aligned
- tested locally
- not live-verified

Because there is still no real deployed read-only content-pipeline API with:
- base URL
- auth method
- exact live routes
- known-good live IDs/topics/keywords

## The Right Decision

Do not keep refactoring the plugin locally as if that will unblock it.

The next real decision is:

`Where will the read-only wrapper live, and what exact base URL + auth contract will the plugin use?`

## Recommended Integration Shape

The proposed contract in `docs/reference/content-pipeline/` is already good enough to adopt.

Recommended live endpoints:

- `GET /content/research-dossiers/{dossier_id}`
- `GET /content/research-dossiers?topic={topic}&locale={locale}`
- `GET /content/product-approvals?keyword={keyword}`
- `GET /content/products?handles=a,b,c`
- optional: `GET /content/product-facts?topic={topic}`

## Recommended Access Strategy

Prefer:
- thin read-only API or workflow wrapper

Do not prefer:
- direct DB reads from the plugin

Why:
- keeps the plugin decoupled from raw schema quirks
- makes later schema changes easier
- matches the current plugin design assumptions
- lowers operational risk

## What Needs To Be Decided Or Built

One of these must happen next:

1. Expose a real thin read-only wrapper
   - choose where it runs
   - define base URL
   - define auth format
   - expose the agreed endpoints

2. Or explicitly decide that the plugin will use direct DB reads instead
   - this is less preferred
   - if chosen, the design docs should be updated because it changes the integration boundary materially

## Minimum Information The Plugin Still Needs

Before the adapter can be live-verified, it needs:
- real base URL
- auth header format or token mechanism
- one known-good dossier ID
- one known-good topic query
- one known-good keyword for product approvals

## Best Practical Next Step

The next correct step is not more plugin-local engineering.

The next correct step is:

1. decide the live integration target
2. expose the read-only wrapper
3. test the plugin adapter against real endpoints and real payloads

## Bottom Line

The plugin is locally ready enough.

The blocker is external integration definition, not internal plugin architecture.

Until the live read-only wrapper exists, further local plugin work should stay limited to:
- small cleanup
- documentation
- maybe manifest/runtime validation

But not major architecture changes.
