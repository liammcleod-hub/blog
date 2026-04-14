# Bastelschachtel Schema Implementation Status

**Date:** 2026-04-13  
**Status:** COMPLETE (Identity Graph + FAQ)  
**Theme:** Maerz 2026 (ID: 196991385938)

---

## Active Snippets in Shopify

| File | Purpose | Pages |
|------|---------|-------|
| `snippets/schema-main-graph.liquid` | Identity Graph @graph | Global (homepage = full, other = org only) |
| `snippets/schema-faq.liquid` | FAQPage Q&A | /pages/faq-haufig-fragen only |

## Archived Snippets

| File | Reason | Archive Location |
|------|--------|-----------------|
| `schema-organization.liquid` | Consolidated into @graph | `snippets/archive/` |
| `schema-local-business.liquid` | Consolidated into @graph | `snippets/archive/` |
| `schema-website.liquid` | Consolidated into @graph | `snippets/archive/` |

---

## Architecture Summary

### @graph Structure

```
schema-main-graph.liquid
├── Organization (#organization) — ArtSupplyStore — ALWAYS
│   ├── knowsAbout: [Bastelbedarf, Korbflechten, Pentart, ...]
│   ├── sameAs: [YouTube, Instagram, Facebook, Pinterest, WKO, Firmen.at]
│   ├── contactPoint
│   └── address
│
├── LocalBusiness (#localbusiness) — ArtSupplyStore — HOMEPAGE ONLY
│   ├── parentOrganization → #organization
│   ├── geo: 47.2946067, 11.5928755
│   ├── openingHoursSpecification (split shifts: 9-12 & 14-18)
│   └── priceRange: €€
│
└── WebSite (#website) — HOMEPAGE ONLY
    └── publisher → #organization
        └── potentialAction: SearchAction
```

### FAQ Structure

```
schema-faq.liquid (/faq page only)
├── 7 Questions with verbatim answers
│   ├── Versandkosten
│   ├── Rücksendung
│   ├── Lagerverfügbarkeit
│   ├── Zahlungsmethoden
│   ├── Datensicherheit
│   ├── Expressversand
│   └── Kaufvertrag
```

---

## Theme.liquid Render Structure

```liquid
{%- comment %} Schema: Identity Graph @graph (AEO Optimized) {%- endcomment -%}
{%- render "schema-main-graph" -%}

{%- comment %} FAQPage (/faq only) {%- endcomment -%}
{%- if template.name == 'page' and page.handle == 'faq-haufig-fragen' -%}
  {%- render "schema-faq" -%}
{%- endif -%}
```

---

## Implementation Log

| Date | Action | Result |
|------|--------|--------|
| 2026-04-13 | Created schema-organization.liquid | ✅ |
| 2026-04-13 | Added to theme.liquid | ✅ |
| 2026-04-13 | Created schema-local-business.liquid | ✅ |
| 2026-04-13 | Created schema-website.liquid | ✅ |
| 2026-04-13 | **REFACTOR:** Consolidated to schema-main-graph.liquid | ✅ |
| 2026-04-13 | Archived old unused snippets | ✅ |
| 2026-04-13 | Created schema-faq.liquid | ✅ |
| 2026-04-13 | Added FAQ render to theme.liquid | ✅ |
| 2026-04-13 | Deleted unused snippets from Shopify | ✅ |

---

## Next Steps (Deferred)

| Schema | Status | Notes |
|--------|--------|-------|
| HowTo | ⏳ Waiting | DIY metaobjects exist; needs template mapping |
| Product FAQ | ⏳ Waiting | GSC data needed for top products |
| Collection FAQ | ⏳ Waiting | GSC data needed for top collections |

---

## Related Documents

- [[2026-04-13-schema-master-plan]] — Full implementation roadmap
- [[2026-04-13-schema-master-summary]] — Strategy overview
- [[2026-04-13-aeo-geo-framework]] — AEO/GEO reference
- [[2026-04-13-store-wide-schema-audit]] — Technical audit

---

## CRITICAL: Live Site Gap Analysis (2026-04-13)

### Root Cause

**AVADA SEO Suite overrides our schema via `content_for_header`**

AVADA outputs Organization schema AFTER our theme.liquid renders. The old Organization wins.

### Current Live State

| Source | Output | Status |
|--------|--------|--------|
| AVADA (content_for_header) | Old Organization only | OVERRIDING |
| Our theme snippets | Full @graph | READY but IGNORED |

### What Live Site Shows NOW

```json
{
  "@context": "http://schema.org",
  "@type": "Organization",
  "name": "Bastelschachtel",
  "logo": "...",
  "url": "https://www.bastelschachtel.at"
}
```

### What Our Snippets Have (Ready but Blocked)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "ArtSupplyStore", "knowsAbout": [...], "sameAs": [...], "contactPoint": {...} },
    { "@type": "ArtSupplyStore", "parentOrganization": {...}, "geo": {...}, "openingHours": [...] },
    { "@type": "WebSite", "publisher": {...} }
  ]
}
```

### Solution: Turn OFF AVADA Organization

1. Go to AVADA SEO Suite
2. Toggle OFF "Organization"
3. Wait 2-3 minutes
4. Test with Rich Results Test

### Related Doc

- [[2026-04-13-schema-live-gap-analysis]] — Full gap analysis

---

## Live Verification (2026-04-13)

### FAQ Page CONFIRMED LIVE ✅

```json
{
  "@type": "ArtSupplyStore",
  "legalName": "Bastel-Kreativ GmbH",
  "knowsAbout": [...],
  "sameAs": [...],
  "vatID": "ATU80189369"
}
+ FAQPage (7 Q&As)
```

### Homepage WAITING ⏳

AVADA cache clearing - will show full @graph soon

---

## Webmaster Verification

- Google: ✅ Hetzner DNS
- Facebook: ✅ Hetzner DNS  
- Pinterest: ✅ Hetzner DNS
- Bing: ⏳ Need code

---

## Status: FAQ MISSION ACCOMPLISHED ✅

All critical schema elements working on FAQ page.
Homepage @graph ready in Shopify.
Bing verification code still needed.

**Note:** AVADA Site Verification app also turned OFF — all critical codes already in Hetzner DNS.
