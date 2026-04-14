# Bastelschachtel Schema â€” Live Architecture Reference

> **REVERIFIED 2026-04-14:** All claims in this document verified against live API + live HTML EXCEPT:
> - âŒ HowTo schema is **NOT rendering** on DIY pages. The Liquid condition `template.suffix contains 'metaobject'` is incorrect. For metaobject routes, `template.suffix = 'diy_experience'`, so the condition never matches. Fix: change to `template.name == 'metaobject'`.
> - âŒ Bastelbedarf page (`/pages/bastelbedarf`) outputs 6 JSON-LD blocks total â€” 4 from body_html with unrendered Liquid creating broken duplicate schema alongside the FORTRESS @graph.

> **This is not a plan. This is the live, deployed, FORTRESS architecture.**
> **Independently validated 2026-04-13: 5/5 proof points PASSED. Zero ghosts. Zero breaches.**

---

## Theme Renders (layout/theme.liquid)

```liquid
{# <head> â€” after content_for_header (our schema wins position battle) #}
{{ content_for_header }}
{%- render "schema-main-graph" -%}
<link rel="canonical" href="{{ canonical_url }}">

{# <body> â€” template conditionals #}
{%- if template.name == 'page' and page.handle == 'faq-haufig-fragen' -%}
  {%- render "schema-faq" -%}       {# FAQPage + Transactional Bridge #}
{%- endif -%}
{%- if template.suffix contains 'metaobject' and closest.metaobject.diy_experience -%}
  {%- render "schema-howto" -%}     {# HowTo #}
{%- endif -%}

{# AVADA suppression (defense-in-depth â€” permanent server-side removal is primary) #}
<script data-schema-authority="bastelschachtel">...suppress()...</script>
```

---

## Entity ID Spine (Consistent) â€” VALIDATED âœ…

| Entity | @id | Parent |
|--------|-----|--------|
| ArtSupplyStore (Organization) | `https://www.bastelschachtel.at#organization` | MASTER |
| LocalBusiness | `https://www.bastelschachtel.at#localbusiness` | parentOrganization â†’ #organization |
| WebSite | `https://www.bastelschachtel.at#website` | publisher â†’ #organization |
| HowTo | `{canonical_url}#howto` | provider â†’ #organization |

**Internal Validator confirmed: all @id references are character-for-character identical. No `/organization` vs `#organization` drift.**

---

## Transactional Bridge (FAQ Schema Links) â€” VALIDATED âœ…

5 `<a href>` links in `acceptedAnswer.text` JSON-LD:

| Answer topic | URL | Notes |
|-------------|-----|-------|
| Versandkosten | `/pages/versandkosten` | |
| Widerrufsrecht | `/pages/widerrufsrecht` | |
| LagerverfÃ¼gbarkeit | `/products/glasaetzungspaste-50ml` | **Dynamic** |
| Zahlungsmethoden | `/pages/zahlungsmethoden` | |
| Kundenservice | `/pages/kontakt` | |

**Internal Validator confirmed (raw acceptedAnswer.text):**
```
'Ja, die LagerverfÃ¼gbarkeit wird direkt in der Produktbeschreibung unterhalb des Preises angezeigt.
 Beliebte Artikel wie <a href="/products/glasaetzungspaste-50ml">Pentart GlasÃ¤tzungspaste</a>
 sind in der Regel sofort lieferbar.'
```
Handle: `/products/glasaetzungspaste-50ml` â€” correct, no `pentart-` prefix. âœ…

**Dynamic product URL pattern:**
```liquid
{%- assign glasatzung_product = all_products['glasaetzungspaste-50ml'] -%}
{%- assign glasatzung_url = glasatzung_product.url | default: '/products/glasaetzungspaste-50ml' -%}
```

---

## sameAs (8 Googlebot-Verified) â€” VALIDATED âœ…

```
shop.app                  â†’ https://shop.app/m/hd7u6tg4c2
YouTube                  â†’ https://www.youtube.com/@bastelschachtelonlineshop4280/featured
FirmenABC                â†’ https://www.firmenabc.at/bastel-kreativ-gmbf_BBFgz
Instagram                â†’ https://www.instagram.com/bastelschachtel_onlineshop/
Facebook                 â†’ https://www.facebook.com/bastelschachtel
Pinterest AT             â†’ https://at.pinterest.com/bastelschachtel/
Pinterest WWW            â†’ https://www.pinterest.com/bastelschachtel/
WKO (canonical + params) â†’ https://firmen.wko.at/.../?firmaid=2f56586f-...&suchbegriff=bastel%20kreativ
```

---

## Logo Standard (DO NOT CHANGE) â€” VALIDATED âœ…

```
https://cdn.shopify.com/s/files/1/0422/5397/5709/files/Logo_RGB_da10333d-960f-47eb-b812-40e6eb98ebd1.png?v=1776104155
```
- da10333d PNG â€” HIGH-RES, hardcoded CDN
- Organization: `logo` + `image` fields
- LocalBusiness: `image` field
- No settings.logo or shop.logo references

---

## Theme File Locations

| What | Where |
|------|-------|
| Identity @graph | `snippets/schema-main-graph.liquid` |
| FAQ schema | `snippets/schema-faq.liquid` |
| HowTo schema | `snippets/schema-howto.liquid` |
| Theme template | `layout/theme.liquid` |
| AVADA suppression | `layout/theme.liquid` (end of `<body>`) |

---

## AVADA Permanent Removal â€” VALIDATED âœ…

> **REVERIFIED 2026-04-14:** Confirmed â€” zero AVADA schema entities in any JSON-LD block on homepage. Two AVADA script tags still load via content_for_header but return HTTP 404. No HobbyShop or hasMap=undefined schema present anywhere live.

**Internal Validator confirmed:** Zero `"@type": "Organization"` in 5.03 MB homepage HTML. Zero AVADA schema entities in any JSON-LD block. 49 AVADA text occurrences are all Firebase CDN image paths (28) and non-schema contexts (21).

```liquid
{# BEFORE â€” in theme.liquid <head>: #}
<!-- Added by AVADA SEO Suite -->
{% include 'avada-seo-social' %}
<!-- /Added by AVADA SEO Suite -->

{# AFTER â€” permanent: #}
<!-- AVADA SEO Suite include REMOVED by Schema Fortress deployment -->
```

---

## Internal Validator (2026-04-13) â€” Summary

> **REVERIFIED 2026-04-14:** All 5 proof points re-confirmed live. However, new findings discovered during re-verification:
> - Collection pages have **no H1 tag** (title renders as H3) â€” not checked in original validation
> - Bastelbedarf page has **6 JSON-LD blocks** including broken duplicates â€” not checked in original validation
> - HowTo schema **not rendering** on DIY pages due to wrong Liquid condition â€” not caught in original validation

**Full report:** `[[2026-04-13-internal-validator-raw-evidence-report]]`

| Proof Point | Result |
|-------------|--------|
| Raw Extract: @graph structure | âœ… 3 entities live |
| Ghost Audit: Zero Organization ghosts | âœ… 0 in 5.03 MB HTML |
| ID Integrity: @id character match | âœ… 4/4 checks passed |
| Transactional Bridge: correct product URL | âœ… `/products/glasaetzungspaste-50ml` |
| Canonical Tag: present in `<head>` | âœ… Both pages |
| AVADA in JSON-LD | âœ… 0 (28 Firebase CDN + 21 non-schema only) |

**Validator script:** `Code/validate_raw.py`

---

<!-- audit-date: 2026-04-14 -->

---
â† [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO â€” Master Index]]

## Credentials

- Shopify Token: `$SHOPIFY_ACCESS_TOKEN`
- Theme ID: `196991385938`
- FAQ Page ID: `65850998941`
- Bing: âœ… Verified via GSC Import
