# Operation Clean Sweep — Handoff Document

**Date:** 2026-04-14
**Purpose:** Single-source-of-truth for a new agent session.
**Status:** Audit complete. Implementation pending.

---

## HOW THIS DOCUMENT WAS PRODUCED

Sources read:
- 8 forensic audit MD files from `docs/core tech seo/`
- 5 collection JSON template files from `Code/` (uploaded by operator)
- 3 collection JSON templates from audit docs
- Operator confirmations (product count, Markets setup, GSC data)
- Shopify REST API — fully verified against LIVE and BACKUP themes

**CRITICAL UPDATE:** All 9 templates were read directly from Shopify API for BOTH themes. The findings are fully verified.

---

## LIVE VERIFICATION RESULTS

Both themes scanned via Shopify REST API on 2026-04-14.

| Theme | ID | Webrex Status | Liquid Files |
|-------|----|-------------|-------------|
| **BACKUP** | `199264305490` | **0 of 10 infected — ALL CLEAN** | Identical to LIVE |
| **LIVE** | `196991385938` | **9 of 10 infected — NEEDS NUKES** | Identical to BACKUP |

### Key Discovery

The local files I analyzed were from the LIVE theme's pre-cleanup state. The block IDs in the audit docs and local files were correct — they accurately describe the LIVE theme. The BACKUP theme (`Kopie von Maerz 2026`) was either created after a partial cleanup, or the operator already removed Webrex from it.

**My audit was correct. It was just from the LIVE theme's state. The backup is already clean.**

---

## GROUND TRUTH — OPERATOR CONFIRMATIONS

| Fact | Confirmed By |
|------|-------------|
| Shopify Admin active products: **4,942** | Operator |
| Multiple Markets (DE, AT, International) mapped to `www.bastelschachtel.at` with **NO subfolders** | Operator |
| GSC shows **0 clicks/impressions** for `/search` URLs | Operator |
| Infinite Scroll **disabled site-wide** — Standard Pagination everywhere | Operator (new state) |
| Backup theme ID: `199264305490` | Shopify API |
| Live theme ID: `196991385938` | Shopify API |

---

## SHOPIFY API ACCESS

```
Store: bastelschachtel.myshopify.com
Access Token: [REDACTED - stored in secure env vars]
API Version: 2026-01
Backup Theme ID: 199264305490
Live Theme ID: 196991385938

Read template:
  GET /admin/api/2026-01/themes/{ID}/assets.json?asset[key]=templates/collection.{name}.json

Write template (PUT):
  PUT /admin/api/2026-01/themes/{ID}/assets.json
  Body: { "asset": { "key": "templates/collection.{name}.json", "value": "<json_string>" } }
```

---

## IMPLEMENTATION PATH (CORRECTED)

Two parallel tracks:

1. **BACKUP THEME** — Write Liquid edits (meta-tags, theme.liquid, reispapiere disabled block)
2. **LIVE THEME** — Nuke 9 Webrex zombies from the infected templates
3. **OPERATOR** — Publish backup theme to live (or merge changes)

---

## MOVE 1 — WEBREX ZOMBIE NUKE (LIVE THEME ONLY — 9 Templates)

The LIVE theme has 9 infected templates. The BACKUP theme is already clean.

### Block IDs — Verified from LIVE Theme Shopify API

| # | Template (LIVE) | Section ID | Block ID to Remove | Action |
|---|-------------|-----------|------------------|--------|
| 1 | `collection.schulbedarf.json` | `section_YGVLax` | `webrex_seo_ai_optimizer_schema_breadcrumb_section_RGqQdG` | Remove entire section |
| 2 | `collection.winter.json` | `section_fcf83Y` | `webrex_seo_optimizer_breadcrumb_section_Qhzwkj` | Remove entire section |
| 3 | `collection.glasaetzpaste-gravuren.json` | `17593090354e14f55c` | `webrex_seo_optimizer_breadcrumb_section_BzP9mH` | Remove block from blocks[] and block_order[] |
| 4 | `collection.korbboeden-flechtarbeite.json` | `17593090354e14f55c` | `webrex_seo_optimizer_breadcrumb_section_BzP9mH` | Remove block from blocks[] and block_order[] |
| 5 | `collection.wachspasten-veredelung.json` | `17593090354e14f55c` | `webrex_seo_optimizer_breadcrumb_section_BzP9mH` | Remove block from blocks[] and block_order[] |
| 6 | `collection.saisonale-deko.json` | `17593090354e14f55c` | `webrex_seo_optimizer_breadcrumb_section_BzP9mH` | Remove block from blocks[] and block_order[] |
| 7 | `collection.papiere.json` | `17593090354e14f55c` | `webrex_seo_optimizer_breadcrumb_section_BzP9mH` | Remove block from blocks[] and block_order[] |
| 8 | `collection.gem-1763984916-template.json` | `section_fcf83Y` | `webrex_seo_optimizer_breadcrumb_section_Qhzwkj` | Remove entire section (same as winter) |
| 9 | `collection.gem-backup-default.json` | `section_fcf83Y` | `webrex_seo_optimizer_breadcrumb_section_Qhzwkj` | Remove entire section (same as winter) |

### Pattern A — Remove Entire Section (Templates 1, 2, 8, 9)

For templates where the Webrex block is the ONLY block in its section:

**BEFORE (schulbedarf.json):**
```json
"section_YGVLax": {
  "type": "section",
  "blocks": {
    "webrex_seo_ai_optimizer_schema_breadcrumb_section_RGqQdG": {
      "type": "shopify://apps/webrex-ai-seo-optimizer/blocks/breadcrumbSection/b26797ad-bb4d-48f5-8ef3-7c561521049c",
      ...
    }
  }
}
```

**AFTER:** Delete the entire `section_YGVLax` entry from the `sections` object. Also remove `section_YGVLax` from the top-level `order` array.

**Same pattern for winter, gem1, gem2** (all have `section_fcf83Y` containing only the Webrex block).

### Pattern B — Remove Block Only (Templates 3–7)

For templates where `17593090354e14f55c` has multiple blocks:

**BEFORE (glasaetzpaste, korbboeden, wachspasten, saisonale, papiere):**
```json
"17593090354e14f55c": {
  "type": "_blocks",
  "blocks": {
    "text_mhR9RB": { "type": "text", ... },
    "custom_liquid_UTWfAj": { "type": "custom-liquid", ... },
    "webrex_seo_optimizer_breadcrumb_section_BzP9mH": {
      "type": "shopify://apps/webrex-ai-seo-optimizer/blocks/breadcrumbSection/b26797ad-bb4d-48f5-8ef3-7c561521049c",
      ...
    }
  },
  "block_order": [
    "text_mhR9RB",
    "custom_liquid_UTWfAj",
    "webrex_seo_optimizer_breadcrumb_section_BzP9mH"
  ]
}
```

**AFTER — Remove Webrex from blocks AND block_order:**
```json
"17593090354e14f55c": {
  "type": "_blocks",
  "blocks": {
    "text_mhR9RB": { "type": "text", ... },
    "custom_liquid_UTWfAj": { "type": "custom-liquid", ... }
  },
  "block_order": [
    "text_mhR9RB",
    "custom_liquid_UTWfAj"
  ]
}
```

### Breadcrumb Safety

In templates 3–7, `custom_liquid_UTWfAj` contains working Liquid breadcrumb code (not from Webrex). Removing the Webrex block does NOT remove the breadcrumbs — they are in a SEPARATE block. The breadcrumbs continue to work.

### Template 10 — reispapiere

`collection.reispapiere.json` — NO Webrex. Clean. But see Move 3.

---

## MOVE 2 — PAGINATION METADATA GUARD (Both Themes)

### File: `snippets/meta-tags.liquid`

Both themes have identical content (2,535 chars). Current state confirmed from Shopify API.

**Find and replace the `<title>` and `<meta name="description">` blocks:**

```liquid
{# === BEGIN OPERATION CLEAN SWEEP === #}
{# Title: Fix to German "Seite" instead of English "Page" #}
<title>
  {{ page_title }}
  {%- if current_tags %} &ndash; tagged "{{ current_tags | join: ', ' }}"{% endif -%}
  {%- if current_page != 1 %} &ndash; Seite {{ current_page }}{% endif -%}
  {%- unless page_title contains shop.name %} &ndash; {{ shop.name }}{% endunless -%}
</title>

{# Description: Add current_page guard to eliminate duplicate descriptions #}
{% if page_description %}
  {% if current_page > 1 %}
    <meta name="description" content="{{ page_description | escape }} – Seite {{ current_page }}">
  {% else %}
    <meta name="description" content="{{ page_description | escape }}">
  {% endif %}
{% endif %}
{# === END OPERATION CLEAN SWEEP === #}
```

**Note:** Canonical is already self-referential (Shopify native) — DO NOT CHANGE.

---

## MOVE 3 — REISPAPIERE DISABLED BREADCRUMB (BACKUP Theme)

### File: `collection.reispapiere.json` (BACKUP Theme)

The backup theme has this block with `disabled: true`. The live theme's reispapiere is clean.

**Find in backup theme:**
```json
"custom_liquid_kjyDMg": {
  "type": "custom-liquid",
  "name": "t:names.custom_liquid",
  "disabled": true,   ← FIX THIS
  "settings": { ... }
}
```

**Fix:** Change `"disabled": true` to `"disabled": false`.

---

## MOVE 4 — NOINDEX + HREFLANG PERIMETER (BACKUP Theme)

### File: `layout/theme.liquid` (Both Themes — Identical)

Both themes have identical content (6,533 chars). `<head>` structure confirmed from Shopify API:

```liquid
<head>
  ... renders, stylesheets, fonts ...
  {{ content_for_header }}          ← line 30 — insert AFTER this
  {%- render "schema-main-graph" -%}  ← line 32
  ...
</head>
```

**Insert AFTER `{{ content_for_header }}` on line 30:**

```liquid
{# === BEGIN NOINDEX PERIMETER === #}
{% comment %}Second defense: noindex, follow for low-value pages.
   robots.txt blocks well-behaved bots. This catches AI bots ignoring it.
   Homepage (index) is EXCLUDED.{% endcomment %}
{%- if request.page_type == 'search' or request.page_type == 'cart' or request.page_type == '404' or request.page_type == 'account' -%}
  <meta name="robots" content="noindex, follow">
{%- endif -%}
{# === END NOINDEX PERIMETER === #}

{# === BEGIN DACH HREFLANG INJECTION === #}
{% comment %}Markets maps to .at domain with no subfolders = no auto-injection.
   We manually signal de-AT authority and de-DE relevance.{% endcomment %}
<link rel="alternate" hreflang="de-AT" href="{{ canonical_url }}">
<link rel="alternate" hreflang="de-DE" href="{{ canonical_url }}">
<link rel="alternate" hreflang="de" href="{{ canonical_url }}">
<link rel="alternate" hreflang="x-default" href="{{ canonical_url }}">
{# === END DACH HREFLANG INJECTION === #}
```

---

## MOVE 5 — ACRYLFARBEN SELF-RESOLUTION

The acrylfarben template is clean in both themes (verified from Shopify). It will automatically load in the Theme Editor once the 9 Webrex zombies are removed from the LIVE theme.

---

## MASTER RECORD — FINAL STATE

| Field | Value |
|-------|-------|
| Backup theme ID | `199264305490` — **CLEAN** |
| Live theme ID | `196991385938` — **9 templates infected** |
| Shopify Admin active products | **4,942** |
| Sitemap product URLs | **4,458** |
| Pagination mode | **100% Standard Paginated** |
| Infinite scroll | **DISABLED site-wide** |
| `current_page` available everywhere | **YES** |
| Markets hreflang | **NONE (no subfolders)** |
| `/search` GSC value | **0 impressions** |

---

## EXECUTION ORDER

| # | Action | Target | Notes |
|---|--------|--------|-------|
| 1 | Nuke 9 Webrex zombies | **LIVE** theme (9 templates) | Block IDs in table above |
| 2 | Write meta-tags.liquid | **BACKUP** theme | Title + description blocks |
| 3 | Write layout/theme.liquid | **BACKUP** theme | Noindex + hreflang |
| 4 | Enable reispapiere breadcrumbs | **BACKUP** theme | disabled: true → false |
| 5 | Publish backup theme | Operator action | Or merge to live |

---

*Operation Clean Sweep handoff complete: 2026-04-14*
*All findings verified directly from Shopify REST API.*
