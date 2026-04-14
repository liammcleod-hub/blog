# Operation Ironclad — Lateral Extension Report

**Date:** 2026-04-14 | **Mode:** Read-Only | **Theme:** `196991385938` (Maerz 2026, Live)

---

## VECTOR 1: CONTENT BLOAT

### Question: Is `{{ collection.description }}` rendered on ALL paginated pages, or is there a guard?

### Finding: ✅ NO CONTENT BLOAT RISK — Fortress does NOT need to expand here.

| Check | Result |
|-------|--------|
| `collection.description` referenced in ANY Liquid file? | **ZERO** references across 267 Liquid files |
| Collection description rendered in page `<body>`? | **NO** — verified on live collection pages |
| Description appears only in `<meta>` tag + OG tags? | **YES** — via `page_description` in `snippets/meta-tags.liquid` |
| Page 1 vs Page 2 body content identical? | Description not in body at all; only meta differs (and that's the Pagination Trap from Phase 1) |

**Explanation:** This theme (Horizon) uses a block-based architecture. Collection headers are custom `text` blocks with hardcoded content like `<h3>{{ closest.collection.title }}</h3>`. The `{{ collection.description }}` object is never called in the body — it only feeds `page_description` which populates the `<meta name="description">` tag. There is no visible description paragraph to bloat paginated pages.

**The real bloat is in the `<meta>` tag, not the body.** That's already covered by the Pagination Trap fix (Move 2 of the handoff).

---

## VECTOR 2: ASSET ROT

### Question: Are there leftover Webrex/AVADA JS/CSS files causing 404s?

### Finding: 🟡 MIXED — Theme files are dead but inert. App script tags are LIVE and 404ing.

### 2a. Theme-Level Asset Rot (LOW RISK — dead code, no 404s)

| Category | Items | Risk Level | Explanation |
|----------|-------|------------|-------------|
| AVADA snippet files | 9 files: `avada-seo.liquid`, `avada-seo-meta.liquid`, `avada-seo-structured.liquid`, `avada-seo-local-business.liquid`, `avada-seo-other.liquid`, `avada-seo-redirect.liquid`, `avada-seo-social.liquid`, `avada-seo-status.liquid`, `avada-defer-css.liquid` | 🟡 LOW | **Never rendered.** Zero `{% render 'avada-seo' %}` calls in any live Liquid file. The `{% render 'avada-seo' %}` was removed from theme.liquid (replaced by `<!-- AVADA SEO Suite include REMOVED -->` comment). These are dead code that should be cleaned up but cause no user-facing harm. |
| AVADA search template | `templates/search.avada-seo.liquid` (8,043 chars) | 🟡 LOW | Alternate template. Only used if a resource is explicitly assigned the `avada-seo` template suffix. Not the default. No resource is assigned this suffix. Dead code. |
| `data-avada-lazy` attribute | Found in 3 GemPages sections (`gp-section-596721051690337254.liquid`, `gp-section-596721051690337254.liquid`, `master-diy-anleitung.liquid`) | 🟡 LOW | AVADA's lazy-load attribute on `<img>` tags. Since AVADA's JS is no longer loaded, these attributes are **inert** — they're ignored by the browser. The images still have `src` attributes, so they load normally. No visual breakage. |
| Webrex JS/CSS files | **ZERO** in assets/ | ✅ NONE | No Webrex JavaScript or CSS files exist in the theme's `assets/` folder |
| Webrex app embed in `settings_data.json` | `webrex-announcement/blocks/app-embed` (`disabled: false`) | ✅ INERT | Despite `disabled: false`, **zero Webrex resources load on the live site**. The app is uninstalled — Shopify doesn't inject the embed's code. The `disabled: false` is a config zombie, not a runtime zombie. |

### 2b. App Script Tag 404s (🔴 MEDIUM RISK — active 404s on every page load)

Two AVADA SEO scripts are **injected by Shopify's `content_for_header`** (via App Script Tags in the Shopify Admin, not from theme files). They return **HTTP 404** on every single page load:

| Script URL | HTTP Status | Source | Fixable via Theme? |
|------------|-------------|--------|-------------------|
| `https://seo.apps.avada.io/scripttag/avada-seo-installed.js?shop=bastelschachtel.myshopify.com` | **404** | Shopify App Script Tags (Admin) | ❌ No — must be removed from Shopify Admin → Apps → AVADA SEO |
| `https://cdn1.avada.io/flying-pages/module.js?shop=bastelschachtel.myshopify.com` | **404** | Shopify App Script Tags (Admin) | ❌ No — must be removed from Shopify Admin → Apps → AVADA SEO |
| `https://joy.avada.io/scripttag/avada-joy-points-calculator.min.js?shop=bastelschachtel.myshopify.com` | **200** | Joy Loyalty App (still active) | N/A — this is working correctly |

**Impact:** Every page load triggers two 404 network requests. This:
- Adds latency (browser waits for failed requests)
- May cause console errors visible to crawlers
- Is a signal of poor site hygiene to search engines

**Fortress Expansion Required?** ❌ No Liquid fix possible. These are injected via Shopify's App Script Tags infrastructure. The operator must manually remove them from the Shopify Admin (Settings → Apps → AVADA SEO → Remove script tags, or contact Shopify Support to purge orphaned script tags).

---

## VECTOR 3: MERCHANT IDENTITY (DACH)

### Question: Does the schema contain `shippingDetails` or `MerchantReturnPolicy` nodes?

### Finding: 🔴 NO — Fortress MUST expand here.

| Schema Block | @type | `shippingDetails`? | `MerchantReturnPolicy`? |
|-------------|-------|---------------------|------------------------|
| Homepage Schema (`schema-main-graph.liquid`) | `ArtSupplyStore`, `LocalBusiness`, `WebSite` | ❌ No | ❌ No |
| Product Page Schema (Shopify auto-injected) | `Product` → `Offers` | ❌ No | ❌ No |

### What's Currently in the Product Offers:

```json
{
  "@type": "Offer",
  "@id": "...",
  "availability": "...",
  "price": "...",
  "priceCurrency": "EUR",
  "url": "..."
}
```

### What's Missing for DACH Legitimacy:

Google Germany heavily weighs **shipping and return trust signals** for local merchants. The schema lacks:

1. **`shippingDetails`** (`OfferShippingDetails`) — Tells Google: "This product ships to Germany from Austria with X delivery time and Y cost." Critical for:
   - Google Shopping organic results
   - Google Merchant Center trust
   - AI search engines citing shipping info in answers
   - German buyers seeing delivery estimates in SERPs

2. **`hasMerchantReturnPolicy`** (`MerchantReturnPolicy`) — Tells Google: "We accept returns within X days." Critical for:
   - Google's merchant trust scoring
   - Rich results showing return policy
   - German consumer law compliance signals (Widerrufsrecht)

### Fortress Expansion Required? ✅ YES — HIGH PRIORITY

**Implementation path:** Add `shippingDetails` and `hasMerchantReturnPolicy` to the Product schema via Liquid. This should be a new snippet (e.g., `snippets/schema-shipping-returns.liquid`) injected on product pages only.

**Estimated schema addition:**
```json
// Inside the Product's Offers object:
"shippingDetails": {
  "@type": "OfferShippingDetails",
  "shippingDestination": {"@type": "DefinedRegion", "addressCountry": ["AT", "DE"]},
  "deliveryTime": {
    "@type": "ShippingDeliveryTime",
    "handlingTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 2, "unitCode": "DAY"},
    "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY"}
  },
  "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "EUR"}
},
"hasMerchantReturnPolicy": {
  "@type": "MerchantReturnPolicy",
  "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
  "merchantReturnDays": 14,
  "returnMethod": "https://schema.org/ReturnByMail",
  "returnFees": "https://schema.org/FreeReturn"
}
```

---

## VECTOR 4: PARAMETER EXPLOSION

### Question: Do filtered/sorted collection URLs create new indexable URLs?

### Finding: 🟡 PARTIAL RISK — Canonicals are clean, but single-filter URLs are unguarded.

### Canonical Tag Behavior (VERIFIED LIVE):

| URL Pattern | Canonical Points To | Indexable? | Risk |
|-------------|---------------------|------------|------|
| `/collections/x` | `/collections/x` | ✅ Yes | None — correct |
| `/collections/x?page=2` | `/collections/x?page=2` | ✅ Yes | ⚠️ Pagination Trap (meta desc duplicate — already covered) |
| `/collections/x?filter.p.m.custom.farbe=weiss` | `/collections/x` | ✅ Yes (canonical clean) | 🟡 LOW — canonical strips filter, but page is indexable |
| `/collections/x?filter.p.m.custom.farbe=weiss&page=2` | `/collections/x?page=2` | ✅ Yes | 🟡 LOW — canonical strips filter but keeps page param |
| `/collections/x?filter.p.m.custom.farbe=weiss&filter.p.m.custom.masse=5cm` | `/collections/x` | ✅ Yes | ✅ SAFE — blocked by robots.txt |
| `/collections/x?sort_by=price-ascending` | `/collections/x` | ✅ Yes (canonical clean) | ✅ SAFE — blocked by robots.txt |

### robots.txt Protection:

| Pattern | Blocked? | Coverage |
|---------|----------|----------|
| `*/collections/*sort_by*` | ✅ Yes | Sort URLs fully blocked |
| `*/collections/*filter*&*filter*` | ✅ Yes | **Double-filter** URLs blocked |
| Single-filter URLs (`?filter.p.m.X=Y`) | ❌ **NOT BLOCKED** | Gap — single filter URLs are crawlable |
| Paginated URLs (`?page=N`) | ❌ **NOT BLOCKED** | By design — these should be indexed |

### The Single-Filter Gap:

A single-filter URL like `/collections/x?filter.p.m.custom.farbe=weiss`:
- ✅ Has a clean canonical (points to base collection) — Google should deduplicate
- ❌ Has no `noindex` meta tag — Google CAN index it
- ❌ Not blocked by robots.txt — Bing CAN crawl it
- ❌ Has the SAME meta description as the base collection — another duplicate description source

**However**, in practice:
- Google honors canonical tags and will typically consolidate filter URLs
- Bing is less reliable about canonical consolidation
- The real risk is Bing seeing `?filter=...` URLs as separate pages with identical descriptions

### Fortress Expansion Required? 🟡 OPTIONAL — LOW-MEDIUM PRIORITY

**Option A (Pure Liquid, minimal):** Add a `noindex, follow` meta tag to filtered collection pages:
```liquid
{%- if request.page_type == 'collection' and request.url contains 'filter.p.' -%}
  <meta name="robots" content="noindex, follow">
{%- endif -%}
```

**Option B (Shopify Admin):** Add a robots.txt rule for single-filter URLs. This requires a `robots.txt.liquid` template override.

**Option C (Do nothing):** The canonical tag already consolidates these. The risk is primarily for Bing, which may ignore canonicals. Given that 90% of revenue comes from Germany (primarily Google), this is a lower priority.

---

## EXPANSION DECISION MATRIX

| Vector | Fortress Expansion? | Priority | Implementation Path | Pure Liquid? |
|--------|--------------------| ---------|--------------------|--------------|
| **1. Content Bloat** | ❌ No | N/A | Not applicable — no risk found | N/A |
| **2a. Theme Asset Rot** | 🟡 Cleanup only | LOW | Delete 10 AVADA Liquid files + 1 template in backup theme | ✅ Yes |
| **2b. App Script Tag 404s** | ⚠️ Admin action | MEDIUM | Operator must remove AVADA script tags from Shopify Admin | ❌ No — Admin only |
| **3. Shipping/Return Schema** | ✅ **YES** | **HIGH** | New `schema-shipping-returns.liquid` snippet on product pages | ✅ Yes |
| **4. Parameter Explosion** | 🟡 Optional | LOW-MED | `noindex, follow` on filtered pages via Liquid | ✅ Yes |

---

## UPDATED FORTRESS SCOPE

**Phase 1 (Handoff Doc — 9 → 14 Zombie Nukes):**
- 9 collection template Webrex nukes (handoff) → **10** (add marken.json)
- 4 product template Webrex nukes (**NEW**)
- 1 config/settings_data.json webrex-announcement embed cleanup (**NEW**)
- 10 AVADA Liquid file deletions (**NEW**)
- Meta-tags.liquid pagination fix (handoff — unchanged)
- theme.liquid noindex perimeter (handoff — unchanged)
- theme.liquid hreflang injection (handoff — unchanged)
- Reispapiere breadcrumb enable (handoff — unchanged)

**Phase 2 (Lateral Extensions — NEW):**
- `schema-shipping-returns.liquid` — OfferShippingDetails + MerchantReturnPolicy for DACH (**HIGH**)
- Filtered collection noindex guard (**OPTIONAL**)
- AVADA script tag removal from Shopify Admin (**OPERATOR ACTION**)

**Total new actions discovered:** 6 theme-level + 1 admin action

---

*Operation Ironclad Lateral Extension Report complete: 2026-04-14*
*All findings verified via live Shopify API and live HTML fetch. Read-only mode maintained.*
