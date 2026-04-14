# Bastelschachtel AEO Schema â€” Session Context

**Date:** 2026-04-13 (final)  
**Status:** FORTRESS LIVE â€” 14/14 checks passed âœ… | **Internal Validator: 5/5 PASSED** âœ…

---

## START HERE: [[2026-04-13-schema-master-status]]

Full status, all details, and remaining work are there.

---

## FORTRESS Quick Reference

> **REVERIFIED 2026-04-14:** Core FORTRESS claims verified. New issues: HowTo not rendering (wrong Liquid condition), Bastelbedarf page has broken duplicate schema, collections missing H1.

### Identity Graph
```
#organization  [ArtSupplyStore]  â† MASTER (hardcoded CDN logo + image)
#localbusiness [LocalBusiness]   â† parentOrganization â†’ #organization
#website       [WebSite]         â† publisher â†’ #organization
```

### Theme Renders (layout/theme.liquid)
```liquid
{# <head> #}
{{ content_for_header }}
{%- render "schema-main-graph" -%}
<link rel="canonical" href="{{ canonical_url }}">

{# <body> #}
{%- if template.name == 'page' and page.handle == 'faq-haufig-fragen' -%}
  {%- render "schema-faq" -%}           {# 5 HTML links in acceptedAnswer.text #}
{%- endif -%}
{%- if template.suffix contains 'metaobject' and closest.metaobject.diy_experience -%}
  {%- render "schema-howto" -%}          {# HowTo rich results #}
{%- endif -%}

{# AVADA suppression JS (defense-in-depth) #}
```

### sameAs â€” 8 Googlebot-Verified URLs
shop.app Â· YouTube Â· FirmenABC Â· Instagram Â· Facebook Â· Pinterest (Ã—2) Â· WKO (firmaid)

### Transactional Bridge
- 5 `<a href>` links in FAQ acceptedAnswer.text âœ…
- Product URL: dynamic `all_products['glasaetzungspaste-50ml'].url` âœ…
- FAQ page body_html synced via API âœ…
- Internal Validator confirmed: `/products/glasaetzungspaste-50ml` â€” no `pentart-` prefix âœ…

### AVADA Ghost Nuked
- `{% include 'avada-seo-social' %}` â€” **PERMANENTLY REMOVED** from theme.liquid
- Internal Validator confirmed: **0** `"@type": "Organization"` in 5.03 MB HTML âœ…
- 49 AVADA occurrences: 28 Firebase CDN + 21 non-schema (zero schema entities) âœ…

### Internal Validator Status (2026-04-13)
**Full report:** `[[2026-04-13-internal-validator-raw-evidence-report]]`

| Proof Point | Result |
|-------------|--------|
| Raw Extract: @graph structure | âœ… ArtSupplyStore + LocalBusiness + WebSite confirmed |
| Ghost Audit: No AVADA Organization | âœ… Zero ghosts |
| ID Integrity: @id character match | âœ… 4/4 checks passed |
| Transactional Bridge: correct product URL | âœ… `/products/glasaetzungspaste-50ml` |
| Canonical Tag: present in `<head>` | âœ… Both homepage and FAQ page |

### Webmaster Verification
- Google âœ… DNS
- Facebook âœ…
- Pinterest âœ…
- **Bing âœ… via GSC Import â€” no meta-tag needed**

---

## GSC Priority Data

**File:** `Code/gsc_analysis/gsc_analysis.json`  
**Range:** 2025-10-01 to 2026-04-13  
**Top products:** Pentart GlasÃ¤tzungspaste (199 clicks) Â· Reispapier (133) Â· Uhrwerk (51)

**DIY HowTo expansion targets:** schattenbox (16) Â· korb flechten (13) Â· reispapier basteln (32)

---

## Credentials
- Store: bastelschachtel.at / bastelschachtel.myshopify.com
- Theme: Maerz 2026 (ID: 196991385938, role: main)
- Shopify Token: `$SHOPIFY_ACCESS_TOKEN` (stored in `.env`, do not commit)
- FAQ Page ID: `65850998941`

---

<!-- audit-date: 2026-04-14 -->


---
â† [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO â€” Master Index]]


## Related Docs
- [[2026-04-13-schema-master-status]] â€” **START HERE**
- [[2026-04-13-schema-live-architecture]] â€” Architecture reference
- [[2026-04-13-schema-session-success]] â€” Session success summary
- [[2026-04-13-aeo-geo-framework]] â€” AEO/GEO reference
- [[2026-04-13-diy-faq-implementation-notes]] â€” HowTo + FAQ notes
- [[2026-04-13-internal-validator-raw-evidence-report]] â€” Raw evidence report
