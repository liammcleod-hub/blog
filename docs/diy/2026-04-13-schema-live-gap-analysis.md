# Bastelschachtel Schema Live Gap Analysis

> **REVERIFIED 2026-04-14:** This document is now STALE. All issues described as ⏳ have been resolved by the FORTRESS deployment. Homepage now shows our @graph correctly. Bing verification completed via GSC Import. HowTo schema deployed but NOT rendering due to wrong Liquid condition (see schema-live-architecture.md).

**Date:** 2026-04-13  
**Status:** FAQ GOLDEN ✅ | Homepage ⏳ AVADA App Embed

---

## Current State

### ✅ FAQ Page — GOLDEN (2026-04-13 Confirmed)
| Field | Value |
|-------|-------|
| `logo` | HIGH-RES PNG (da10333d...) |
| `priceRange` | €€ |
| `sameAs` | 8 links incl. TikTok |
| `legalName` | Bastel-Kreativ GmbH |
| `vatID` | ATU80189369 |
| `knowsAbout` | 6 items |
| `FAQPage` | 7 verbatim Q&As |

### ⏳ Homepage — BLOCKED
- AVADA app embed injects Organization via `content_for_header`
- Our `@graph` in theme.liquid is blocked
- Cache expires naturally (24-48 hours)

---

## Root Cause

**AVADA App Embed System**

AVADA injects schema via Shopify's app embed mechanism (`content_for_header`).
This is SEPARATE from theme files — toggles control the setting, not the cache.

The Organization on homepage comes from AVADA, NOT from our theme.

---

## What We Did

1. ✅ Commented out Organization schema in `sections/header.liquid`
2. ✅ Deployed GOLDEN schema-main-graph.liquid to Shopify
3. ✅ Confirmed FAQ page shows our @graph correctly
4. ⏳ Homepage waiting for AVADA cache to clear

---

## Webmaster Verification

| Code | Service | Status |
|------|---------|--------|
| `google-site-verification=wkZy0...` | Google | ✅ Hetzner DNS |
| `google-site-verification=dTpA...` | Google | ✅ Hetzner DNS |
| `facebook-domain-verification=3or7...` | Facebook | ✅ Hetzner DNS |
| `pinterest-site-verification=0c30...` | Pinterest | ✅ Hetzner DNS |
| `msvalidate.01` | Bing | ⏳ Needed |

---

## Next Steps

1. ⏳ Homepage @graph will show when AVADA cache clears
2. ⏳ Get Bing verification code
3. 📋 HowTo schema for DIY pages

---

<!-- audit-date: 2026-04-14 -->


---
← [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO — Master Index]]


## Related
- [[2026-04-13-schema-master-status]] — Current master status
- [[2026-04-13-schema-session-context]] — Quick reference
