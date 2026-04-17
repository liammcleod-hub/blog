# Implementation Plan — SEO Handle From Collection Title (MANUAL→SMART upgrades)

## Goal

When we upgrade a MANUAL collection to SMART (`replace_with_smart`), we should end up with a **final** collection handle that is:

- derived from the **collection title**
- SEO-friendly (lowercase slug, ASCII; umlauts removed)
- correctly referenced by the MAIN menu after the upgrade
- protected by redirects from the old handle(s)

SEO meta fields (`seo.title`, `seo.description`, `descriptionHtml`) remain a separate step.

## Non-goals

- No automatic generation of SEO title/description/HTML.
- No catalog-wide leakage estimation (still out of scope).

## Design (KISS)

### 1) Slugify rule

Compute `seo_handle = slugify(title)`:

- lowercase
- replace German umlauts: `ä→a`, `ö→o`, `ü→u`, `ß→ss`
- replace non `[a-z0-9]` sequences with `-`
- trim leading/trailing `-`
- collapse repeated `-`

### 2) Proposal shape changes

For any proposal action `replace_with_smart`, add:

- `final_handle`: the `seo_handle` computed from title

### 3) Apply behavior changes (write path)

Extend `replace_with_smart` apply flow to include an optional “post-promote handle normalization” step:

1. Create SMART temp collection (`smart_handle_temp`)
2. Rename old MANUAL to `legacy_handle`
3. Promote SMART to original handle
4. If `final_handle` is present and differs from the current promoted handle:
   - update the SMART collection handle to `final_handle`
   - create redirects:
     - `/collections/<old_handle>` → `/collections/<final_handle>`
     - `/en/collections/<old_handle>` → `/en/collections/<final_handle>`
   - rewrite MAIN menu URLs (best-effort) from `<old_handle>` → `<final_handle>`

Menu resource-id rewriting remains the primary safety mechanism; URL-handle rewriting is supplemental for menus that encode URLs.

### 4) Evidence / tests

After implementation:

- Run `python shopify_api_work/collections_cleanup_runner.py orchestrate --mode propose`
  - verify proposals include `final_handle` for `replace_with_smart`
- Run `python shopify_api_work/collections_cleanup_runner.py propose --handle <some-manual> --menu-only`
  - verify single-handle proposal includes `final_handle`

No live writes will be executed without explicit user approval.

