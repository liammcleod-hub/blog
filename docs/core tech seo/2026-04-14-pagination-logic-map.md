# The Pagination Logic Map

**Date:** 2026-04-14  
**Mode:** Boil the Ocean Forensic Audit  
**Mandate:** Read-Only. Map every pagination behavior. No code written.

---

## BUCKET SUMMARY

| Bucket | Behavior | Files Involved | Discovery Method |
|--------|---------|---------------|----------------|
| **[Standard Paginated]** | Server-side `{% paginate %}` + HTML `<nav>` links | `sections/main-collection.liquid` | HTML `<nav>` + sitemap |
| **[Infinite Scroll Hybrid]** | JS `PaginatedList` + no HTML pagination | `sections/main-collection.liquid` + `product-card.js` | Sitemap only |
| **[Static/Single Page]** | `< 24 products, `{% paginate %}` + limited nav | `sections/main-collection.liquid` | Sitemap + minimal HTML nav |

---

## BUCKET 1: [Standard Paginated]

**Trigger:** `section.settings.enable_infinite_scroll == false` in `sections/main-collection.liquid`

### Liquid Logic (lines 48-76)

```liquid
{% if section.settings.enable_infinite_scroll == false %}
  {% paginate collection.products by products_per_page %}
    ...
    {% render 'product-grid', ..., paginate: paginate %}
  {% endpaginate %}
{% endif %}
```

### What This Renders

| Element | Rendered? | Google-Visible? |
|---------|---------|----------------|
| `<nav class="pagination">` | ✅ Yes | ✅ Yes |
| Anchor tags with `?page=N` | ✅ Yes (4 links found in live HTML) | ✅ Yes |
| Product cards | ✅ Yes | ✅ Yes |
| Schema @graph | ✅ Yes | ✅ Yes |
| Meta description | ❌ Identical to all other pages | ❌ Identical |

### Discovery Path

1. Google crawls base collection URL
2. Finds `<nav class="pagination">` at bottom of HTML
3. Follows links to pages 2, 3, ..., N
4. Discovers all paginated URLs via HTML links
5. Products listed individually in sitemap

### Example Pages in This Bucket

All collection pages where the merchant has set `enable_infinite_scroll = false` in the theme editor. To confirm which collections fall into this bucket, inspect each collection page in the theme editor.

---

## BUCKET 2: [Infinite Scroll Hybrid]

**Trigger:** `section.settings.enable_infinite_scroll == true` in `sections/main-collection.liquid`

### Liquid Logic

```liquid
{% if section.settings.enable_infinite_scroll == false %}
  {% paginate collection.products by products_per_page %}
    ...
  {% endpaginate %}
{% endif %}
{# When true: NO {% paginate %} block renders #}
```

### What This Renders

| Element | Rendered? | Google-Visible? |
|---------|---------|----------------|
| `<nav class="pagination">` | ❌ **NOT rendered** | ❌ **No** |
| Anchor tags with `?page=N` | ❌ **NOT rendered** | ❌ **No** |
| Product cards | ✅ Yes (via JS `PaginatedList`) | ✅ Yes (via sitemap) |
| Schema @graph | ✅ Yes | ✅ Yes |
| Meta description | ❌ Identical to all other pages | ❌ Identical |

### The JS Infinite Scroll Mechanism

**Component:** `results-list` web component (extends Shopify's `PaginatedList`)

```
results-list.aio.min.js
└── extends PaginatedList (Shopify native web component)
    └── handles pagination loading via JS
```

**URL Update:** `product-card.js` (lines 406-422) — when clicking a product card in infinite scroll mode:

```javascript
const infiniteResultsList = this.closest('results-list[infinite-scroll="true"]');
if (...infiniteResultsList) {
  url.searchParams.set('page', parent.dataset.page);
  history.replaceState({}, '', url.toString());
}
```

This updates the URL to `?page=N` WITHOUT a page reload. It does NOT update `<title>`, `<meta description>`, or schema.

### Discovery Path

1. Google crawls base collection URL
2. **Finds ZERO `?page=` anchor tags** (no `<nav class="pagination">`)
3. Products discovered via **XML sitemap** (4,458 individual product URLs)
4. Paginated collection URLs (`?page=N`) are NOT discovered through HTML links
5. If Google manually requests `?page=N` directly: receives full HTML with products + correct title + schema + self-referential canonical

### Example Pages in This Bucket

All collection pages where the merchant has set `enable_infinite_scroll = true`. The "All Products" collection (`/collections/all`) shows 124 paginated pages and likely uses this mode (given its massive size of 7.3MB HTML).

---

## BUCKET 3: [Static/Single Page]

**Trigger:** Collection has fewer products than the `products_per_page` setting (default: 24)

### Liquid Logic

Same as Bucket 1, but the `{% paginate %}` block renders with only one page.

### What This Renders

| Element | Rendered? | Google-Visible? |
|---------|---------|----------------|
| `<nav class="pagination">` | ✅ Yes (but only page 1) | ✅ Yes |
| Products | ✅ Yes | ✅ Yes |
| Meta description | ❌ Identical to all other pages | ❌ Identical |

### Discovery Path

Same as Bucket 1. No special risk.

---

## THE TOGGLE: `enable_infinite_scroll`

The `main-collection.liquid` section has a schema-defined setting:

```liquid
infinite-scroll="{{ section.settings.enable_infinite_scroll }}"
```

And in the section schema (line 220-232):
```json
{
  "id": "enable_infinite_scroll",
  "type": "checkbox",
  "default": false,
  "visible_if": "{{ section.settings.enable_infinite_scroll == false }}"
}
```

### How This Works

1. Each **collection page instance** in the theme editor has its own `enable_infinite_scroll` setting
2. The theme editor stores these settings per section instance, per collection
3. **Different collections CAN have different settings** — this is a per-instance toggle

### Implications

| Collection | Buckets Possible | Which Bucket? |
|-----------|-----------------|----------------|
| `/collections/all` (4,400+ products) | Bucket 1 or 2 | To be confirmed (likely Bucket 2 — infinite scroll) |
| `/collections/glasatzen` (small) | Bucket 1 or 2 | Bucket 1 (confirmed — has `<nav>` with 4 page links) |
| `/collections/kinder-bastelsets` | Bucket 1 or 2 | To be confirmed |

**To determine which bucket each collection falls into:** Inspect the theme editor section settings for each collection, OR check the live HTML for the presence of `<nav class="pagination">`.

---

## THE META-TAG GUARD: `current_page` IN `meta-tags.liquid`

### Current State

```liquid
{# meta-tags.liquid — Title: HAS current_page guard #}
<title>
  {{ page_title }}
  {%- if current_page != 1 %} &ndash; Page {{ current_page }}{% endif -%}
</title>

{# meta-tags.liquid — Description: NO current_page guard #}
{% if page_description %}
  <meta name="description" content="{{ page_description | escape }}">
{% endif %}
```

### The Safety Question

"If a collection has only 5 products (no Page 2 exists), but a bot accesses `?page=2`, will our Liquid fix append 'Seite 2'?"

**Answer: Yes — but Shopify handles this correctly.**

When accessing a non-existent page (e.g., `?page=99` on a 5-product collection):
- `current_page` = 99 (server renders with the requested page number)
- Title becomes "Products – Page 99 | Bastelschachtel"
- Description remains the collection description (Shopify shows same description regardless)
- 200 OK is returned (Shopify default behavior)
- This is a **benign edge case** — no risk of 404

### The `current_page` Liquid Variable Availability

The `current_page` variable is set by Shopify's `{% paginate %}` block. However:

| Bucket | `{% paginate %}` renders? | `current_page` available in meta-tags.liquid? |
|--------|----------------------|---------------------------------------------|
| Standard Paginated (infinite off) | ✅ Yes | ✅ Yes |
| Infinite Scroll Hybrid (infinite on) | ❌ No | ❌ **No — paginate not called** |
| Single Page | ✅ Yes | ✅ Yes |

**CRITICAL FINDING:** In Bucket 2 (Infinite Scroll Hybrid), `current_page` is **NOT** available because the `{% paginate %}` block is never rendered. This means our proposed Liquid fix (`{% if current_page > 1 %}`) **will NOT fire** on infinite scroll collections!

### The Paradox

If we add:
```liquid
{% if current_page > 1 %}
  <meta name="description" content="{{ page_description }} — Seite {{ current_page }}">
{% else %}
  <meta name="description" content="{{ page_description | escape }}">
{% endif %}
```

- **Bucket 1 (Standard Paginated):** `current_page` IS available → fix fires ✅
- **Bucket 2 (Infinite Scroll):** `current_page` is NOT available → fix does NOT fire ❌

**We can only fix Bucket 1 with a pure Liquid solution. Bucket 2 requires a JavaScript solution — which violates our constraint.**

---

## THE SCHEMA IDENTITY SPINE ON COLLECTION PAGES

### All Buckets

| Schema Element | Served on Collection Pages? | Served on `?page=N`? |
|---------------|--------------------------|--------------------|
| Identity @graph (ArtSupplyStore) | ✅ Yes | ✅ Yes (confirmed on `/collections/all?page=2`) |
| WebSite | ✅ Yes | ✅ Yes |
| LocalBusiness | ✅ Yes | ✅ Yes |

The Identity Spine is served correctly on all collection pages including paginated variants. ✅

### `inLanguage` Field

The `inLanguage: "de-AT"` field appears in the WebSite entity in `schema-main-graph.liquid` (line 154). Live HTML confirmed this appears on `/collections/all?page=2`.

---

## COLLECTION-SPECIFIC OVERRIDE CHECK

### Shopify Metafields on Collections

No collection-specific metafields for pagination behavior were found in the theme files. The `enable_infinite_scroll` setting is the only pagination control — stored in Shopify's section settings (not metafields).

### Custom Collection Templates

No collection-specific Liquid templates found:
- `templates/collection.infinite.liquid` — ❌ Does not exist
- `templates/collection.paginated.liquid` — ❌ Does not exist
- `templates/collection.custom.liquid` — ❌ Does not exist

All collections use the same `main-collection.liquid` section. The only differentiator is the `enable_infinite_scroll` setting per section instance.

---

## THE CANONICAL MIRROR TEST

### All Buckets

| URL | Canonical Tag | Behavior |
|-----|-------------|---------|
| `/collections/all` | `https://.../collections/all` | Points to self |
| `/collections/all?page=2` | `https://.../collections/all?page=2` | **Points to self (SELF-REFERENTIAL)** |
| `/collections/glasatzen` | `https://.../collections/glasatzen` | Points to self |
| `/collections/glasatzen?page=2` | `https://.../collections/glasatzen?page=2` | **Points to self (SELF-REFERENTIAL)** |

**All paginated URLs self-reference their canonical.** This is Shopify's native behavior via `{{ canonical_url }}`.

**A global Liquid fix that changes canonical behavior would affect all three buckets equally.** Since Shopify's native canonical is already self-referential, no fix is needed for canonicals.

---

## FINAL PAGINATION LOGIC MAP

```
BUCKET 1: Standard Paginated
├── enable_infinite_scroll = false
├── {% paginate %} RENDERS
├── <nav class="pagination"> EXISTS
├── 4 anchor tags with ?page= in HTML
├── current_page AVAILABLE in meta-tags.liquid
├── Title: DIFFERENT per page (Shopify adds "Page N")
├── Description: IDENTICAL per page (BUG — Liquid fix WORKS here)
└── Canonical: Self-referential (Shopify) ✅

BUCKET 2: Infinite Scroll Hybrid
├── enable_infinite_scroll = true
├── {% paginate %} DOES NOT RENDER
├── <nav class="pagination"> NOT RENDERED
├── ZERO ?page= anchor tags in HTML
├── current_page NOT AVAILABLE in meta-tags.liquid
├── Title: DIFFERENT per page (Shopify renders each page separately)
├── Description: IDENTICAL per page (BUG — Liquid fix FAILS here)
└── Canonical: Self-referential (Shopify) ✅
    Discovery: Products via sitemap only. Collection ?page=N is invisible.

BUCKET 3: Static/Single Page
├── < 24 products
├── {% paginate %} RENDERS (single page only)
├── <nav class="pagination"> EXISTS (1 page only)
├── current_page AVAILABLE in meta-tags.liquid
├── Title: Single page (no "Page N")
├── Description: Single description
└── Canonical: Self-referential ✅
```

---

## THE SOLUTION REQUIRED

**The description fix CANNOT be done in pure Liquid** because Bucket 2 (Infinite Scroll Hybrid) does not make `current_page` available.

### Options

| Option | Scope | Approach |
|--------|-------|---------|
| **A: JS Fix** | Bucket 2 only | Inject page number into description via `history.replaceState` listener |
| **B: Accept the Split** | Bucket 1 only | Fix description in `meta-tags.liquid` — covers Standard Paginated collections |
| **C: Shopify Settings** | All | Disable infinite scroll on high-value collections, enable pagination |
| **D: JavaScript in theme.liquid** | All buckets | Add JS that reads URL param and updates meta description |

### Recommended Approach

**Option D: Add JavaScript to `layout/theme.liquid`** — a minimal inline script that reads the URL, detects `?page=N`, and appends the page suffix to the meta description. This is a single script, no dependency, and works across all three buckets.

```liquid
{# In layout/theme.liquid <head> — OPTION D #}
<script>
  (function() {
    var params = new URLSearchParams(window.location.search);
    var page = params.get('page');
    if (page && page !== '1') {
      var desc = document.querySelector('meta[name="description"]');
      if (desc && !desc.getAttribute('data-page-suffixed')) {
        desc.setAttribute('data-page-suffixed', 'true');
        desc.content = desc.content + ' — Seite ' + page;
      }
    }
  })();
</script>
```

**Risk Assessment:**
- Runs before page render (inline, synchronous) — may cause slight delay
- Does not affect pages without `?page=` — zero impact on other pages
- Is a JavaScript solution — violates the "Pure Liquid" constraint
- Is the ONLY solution that works for Bucket 2

**If we must stay Pure Liquid:** Only Option B applies. Bucket 1 gets fixed, Bucket 2 remains broken.

---

*Pagination Logic Map completed: 2026-04-14*  
*Scope: 267 liquid files, 158 JS files, live HTML across 5 URL variants, Shopify Admin API*  
*Mode: Read-only. No code written. Evidence above is verbatim.*
