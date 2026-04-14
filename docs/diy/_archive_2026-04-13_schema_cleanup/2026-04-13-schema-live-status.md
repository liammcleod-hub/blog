# Bastelschachtel Schema Live Status

**Date:** 2026-04-13  
**Status:** FAQ LIVE ✅ | Homepage ⏳ Pending AVADA Cache Clear

---

## Live Results (CONFIRMED WORKING)

### FAQ Page ✅ LIVE

```json
{
  "@type": "ArtSupplyStore",
  "legalName": "Bastel-Kreativ GmbH",
  "knowsAbout": ["Bastelbedarf", "Korbflechten", "Pentart Produkte", "Basteln mit Kindern", "DIY Handarbeit", "Bastelzubehor Österreich"],
  "sameAs": [
    "https://www.bastelschachtel.at",
    "https://shop.app/m/hd7u6tg4c2",
    "https://www.youtube.com/channel/UCv8kayedKQE_SwS9wVFnASg",
    "https://www.instagram.com/bastelschachtel_onlineshop/",
    "https://www.facebook.com/bastelschachtel",
    "https://at.pinterest.com/bastelschachtel/",
    "https://firmen.wko.at/bastel-kreativ-gmbh/tirol/",
    "https://www.firmen.at/bastelschachtel"
  ]
}
+ FAQPage with 7 verbatim Q&As
```

### Homepage ⏳ PENDING (AVADA Cache Clearing)

- AVADA cache still clearing
- Our @graph is IN THEME but AVADA's cached Organization is still showing
- User turned OFF AVADA Organization toggle
- Expected: Full @graph once cache clears (15-30 min typical)

---

## AVADA Site Verification (Turned OFF)

⚠️ **Important:** AVADA Site Verification was also turned OFF when disabling AVADA SEO Suite.

### Verification Tags Found in AVADA (Now OFF)

| Service | Meta Tag | Importance | Status |
|---------|----------|------------|--------|
| Google Search Console | `google-site-verification` | ✅ HIGH | ✅ Already in Hetzner DNS |
| Bing Webmaster Tools | `msvalidate.01` | ✅ HIGH | ⏳ Need code |
| Pinterest | `p:domain_verify` | ✅ HIGH | ✅ Already in Hetzner DNS |
| Baidu | `baidu-site-verification` | ⚠️ Optional | - |
| Yandex | `yandex-verification` | ⚠️ Optional | - |

### Action Needed: Get Bing Verification Code

User has Bing Webmaster account + API key, but needs the actual `msvalidate.01` code.
Options:
1. Get fresh code from bingwebmastercenter.com
2. Or provide API key so we can retrieve it programmatically

---

## DNS Verification Codes (Already Active in Hetzner)

| Code | Type | Location |
|------|------|----------|
| `google-site-verification=wkZy0Cug9ihzq1UVCSRdlN0B3MVATK-bmm8TqAO_G8g` | TXT | Hetzner DNS ✅ |
| `google-site-verification=dTpAPx9fGnphUv7vQYokVa_H0TeVLA0NfWfsl_uYKB8` | TXT | Hetzner DNS ✅ |
| `facebook-domain-verification=3or7yqxhp5su4hm0xdm39ubkm9x5pf` | TXT | Hetzner DNS ✅ |
| `pinterest-site-verification=0c30dac949855b17edc477db4767ea59` | TXT | Hetzner DNS ✅ |
| `msvalidate.01` (Bing) | TXT | ⏳ Needed |

---

## Quick Tests User Can Try NOW

1. **Hard refresh browser:** `Ctrl + Shift + R` (Windows) / `Cmd + Shift + R` (Mac)
2. **Incognito/private window** to bypass browser cache
3. **URL variant:** `https://www.bastelschachtel.at/?_x=1` (bypasses some caches)

---

## Active Snippets in Shopify

| File | Purpose | Status |
|------|---------|--------|
| `snippets/schema-main-graph.liquid` | Identity Graph @graph (enhanced) | ✅ IN THEME |
| `snippets/schema-faq.liquid` | FAQPage with 7 Q&As | ✅ LIVE ON FAQ PAGE |

---

## What's Confirmed Working

### Organization Node (on FAQ page)
- ✅ `legalName`: "Bastel-Kreativ GmbH"
- ✅ `knowsAbout`: 6 topics
- ✅ `sameAs`: 8 external links including WKO, Firmen.at, shop.app
- ✅ `brand`: Bastelschachtel
- ✅ `founder`: Bernhard-Stefan Muller
- ✅ `vatID`, `taxID`

### FAQPage Node (on FAQ page)
- ✅ All 7 questions present
- ✅ Verbatim answer text matches visible HTML

### LocalBusiness Node
- Ready with geo coordinates, opening hours, Tirol region
- Will activate on homepage after cache clear

### WebSite Node
- Ready with inLanguage: "de-AT"
- Will activate on homepage after cache clear

---

## Theme.liquid Render Structure

```liquid
{%- render "schema-main-graph" -%}

{%- if template.name == 'page' and page.handle == 'faq-haufig-fragen' -%}
  {%- render "schema-faq" -%}
{%- endif -%}
```

---

## Webmaster Verification (DNS Records)

| Service | Status | Location |
|---------|--------|----------|
| Google | ✅ Verified | Hetzner DNS TXT |
| Facebook | ✅ Verified | Hetzner DNS TXT |
| Pinterest | ✅ Verified | Hetzner DNS TXT |
| Bing | ⏳ Need code | - |

---

## Implementation Log

| Date | Action | Result |
|------|--------|--------|
| 2026-04-13 | Created schema-organization.liquid | ✅ |
| 2026-04-13 | Created schema-local-business.liquid | ✅ |
| 2026-04-13 | Created schema-website.liquid | ✅ |
| 2026-04-13 | REFACTOR to schema-main-graph.liquid | ✅ |
| 2026-04-13 | ENHANCED with legal identifiers | ✅ |
| 2026-04-13 | Created schema-faq.liquid | ✅ |
| 2026-04-13 | Turned OFF AVADA Organization | ✅ |
| 2026-04-13 | Turned OFF AVADA Site Verification | ✅ |
| 2026-04-13 | **FAQ page @graph LIVE** | ✅ |
| 2026-04-13 | Homepage @graph BLOCKED | ⏳ AVADA cache |

---

## Next Steps

1. Homepage @graph will show after AVADA cache clears (15-30 min)
2. ⏳ **Get Bing verification code** (msvalidate.01) — user has API key
3. Optionally add web verification meta tags to theme.liquid manually
4. Plan HowTo schema for DIY pages

---

## Related Docs

- [[2026-04-13-schema-master-plan]] — Full implementation plan
- [[2026-04-13-aeo-geo-framework]] — AEO/GEO reference
- [[2026-04-13-schema-live-gap-analysis]] — Gap analysis
- [[2026-04-13-schema-session-context]] — Quick reference
