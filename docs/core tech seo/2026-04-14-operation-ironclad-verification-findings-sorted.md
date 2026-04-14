# Operation Ironclad — Verification Findings (Sorted)

**Date:** 2026-04-14 | **Status:** Read-Only Verification Complete | **Theme:** `196991385938`

**Strategic Context:** This audit verifies implementation against the **AEO/GEO Framework** ([[2026-04-13-aeo-geo-framework]]), which defines the identity graph architecture for DACH dominance. All fixes must align with AEO (Answer Engine Optimization) and GEO (Generative Engine Optimization) principles.

**Implementation Governance:** All fixes must follow the **Scientific Methodology (LAW)** defined in [[OPERATION-IRONCLAD-SCIENTIFIC-METHODOLOGY]].

---

## Executive Summary

Live verification of all 11 documents in `docs/diy/` uncovered **3 new critical failures** that were not caught in the original FORTRESS validation. The FORTRESS core architecture is intact, but schema bleed and structural SEO gaps exist.

---

## 🔴 CRITICAL PRIORITY (Fix Now)

### #1: Bastelbedarf Page — Broken Duplicate Schema
**AEO/GEO Impact:** ❌ **Directly violates "Trust = Unambiguous Identity" principle**
**Risk:** Schema Pollution, Google Penalty Risk, Unrendered Liquid

**Framework Violation:** The AEO/GEO framework requires **one stable entity per real-world thing with durable IDs**. The Bastelbedarf page creates:
- Duplicate `Organization` entities (one broken with unrendered Liquid)
- Competing `FAQPage` (3 Q&As vs FORTRESS 7)
- Unlinked `HowTo` (no provider link to `#organization`)

**AI Impact:** Search engines must reconcile conflicting entity data, undermining authority scoring.

| Aspect | Finding |
|--------|---------|
| **Location** | `/pages/bastelbedarf` (ID: 158177132882) |
| **JSON-LD Blocks** | 6 total (2 from FORTRESS, 4 from `body_html`) |
| **Broken Blocks** | 4 blocks with **unrendered Liquid**:<br>• `Organization` (`{{ shop.url }}#organization`)<br>• `WebPage` (`{{ shop.url }}{{ page.url }}#webpage`)<br>• `FAQPage` (3 Q&As, different from FORTRESS 7)<br>• `BreadcrumbList` |
| **Extra HowTo** | 1 HowTo block ("Decoupage") injected by unknown source (no provider link to `#organization`) |
| **Impact** | Google sees duplicate Organization schemas (one broken), competing FAQPage, and unparsable Liquid variables. |
| **Root Cause** | Schema snippets manually pasted into page `body_html` in Shopify Admin (not theme Liquid). |
| **Fix** | Edit page in Shopify Admin, remove JSON-LD script tags from body HTML. |

### #2: HowTo Schema — Not Rendering on DIY Pages
**AEO/GEO Impact:** ❌ **Breaks "Extractable Evidence" principle for instructional content**
**Risk:** Missing Rich Results, Broken Implementation

**Framework Violation:** The AEO/GEO framework ranks `HowTo` as **#2 highest-impact schema type** for AI Overview citations. Without it, DIY tutorials lose:
- Step extraction for instructional queries
- Rich results in Google SGE
- Voice search optimization ("how to make a handykette")

**Strategic Loss:** Bastelschachtel's core value proposition (DIY expertise) remains invisible to AI answer engines.

| Aspect | Finding |
|--------|---------|
| **Location** | `/pages/diy-experience/handykette`, `/pages/diy-experience/batik-tshirt` |
| **Expected** | HowTo JSON-LD with steps, provider linking to `#organization` |
| **Actual** | Only ArtSupplyStore @graph appears; **zero HowTo blocks** |
| **Root Cause** | Wrong Liquid condition in `layout/theme.liquid`:<br>`{%- if template.suffix contains 'metaobject' and closest.metaobject.diy_experience -%}`<br>For metaobject routes, `template.suffix = 'diy_experience'`, not `'metaobject'`. |
| **Correct Condition** | `{%- if template.name == 'metaobject' and template.suffix == 'diy_experience' -%}` |
| **Impact** | No Google HowTo rich snippets for DIY tutorials. |
| **Fix** | Edit `theme.liquid`, change condition, test. |

---

## 🟡 HIGH PRIORITY (Fix This Week)

### #3: Collection Pages — Missing H1 Tags
**AEO/GEO Impact:** ⚠️ **Weakens "Extractable Evidence" for category pages**
**Risk:** SEO Structure Gap, Bing Reports 37 Pages Affected

**Framework Connection:** While not directly schema-related, H1 tags provide **clear topic signaling** to AI crawlers. Collection pages represent major commercial intent ("outdoor farben", "korbboeden"). Missing H1s degrade:
- Topic clarity for AI classification
- Featured snippet eligibility
- Query-to-page relevance scoring

**Bing Confirmation:** 37 pages flagged with "H1 tag missing" — matches our live finding.

| Aspect | Finding |
|--------|---------|
| **Pages** | All collection pages (e.g., `/collections/outdoor-farben`) |
| **Expected** | `<h1>{{ collection.title }}</h1>` |
| **Actual** | Collection title renders as **`<h3>`** inside a heading group |
| **Bing CSV** | `IssueDetailsBySeverity.csv` (2026-04-14) lists 37 pages with "H1 tag missing" |
| **Impact** | Weakened page topic signaling, potential ranking impact. |
| **Root Cause** | Horizon theme uses custom `text` blocks with hardcoded `<h3>`. |
| **Fix** | Modify collection template JSON to output H1 instead of H3. |

### #4: AVADA Script Tags — 404s on Every Page Load
**AEO/GEO Impact:** ⚠️ **Signals poor site hygiene to crawlers**
**Risk:** Performance Latency, Console Errors, Site Hygiene

**Framework Connection:** The AEO/GEO framework emphasizes **technical perfection** as a trust signal. 404s from orphaned app scripts:
- Add latency (browser waits for failed requests)
- Create console errors visible to crawlers
- Contradict the "Fortress" narrative of clean, app-free architecture

**Pure Liquid Goal:** Part of Operation Ironclad's mandate is **zero external JavaScript dependencies**.

| Aspect | Finding |
|--------|---------|
| **Scripts** | 2 AVADA scripts injected via Shopify App Script Tags:<br>1. `avada-seo-installed.js` (404)<br>2. `flying-pages/module.js` (404) |
| **Source** | Shopify Admin `content_for_header` injection (not theme files) |
| **Impact** | Every page load triggers two 404 network requests; adds latency; visible to crawlers. |
| **Fix** | Operator action: remove from Shopify Admin → Apps → AVADA SEO, or contact Shopify Support to purge orphaned script tags. |
| **Cannot Fix via Liquid** | True. |

---

## 🟢 MEDIUM PRIORITY (Queue After High)

### #5: product_faq Metaobjects — Existence Verified, Not Verified on Product Pages
**AEO/GEO Impact:** 📊 **Untapped FAQPage potential for product-level queries**
**Risk:** Underutilized Feature

**Framework Connection:** `FAQPage` is the **#1 highest-impact schema type** for AI Overview citations. Product-specific FAQs could answer:
- "Is Pentart Konturenfarbe waterproof?"
- "How long does Glasätzungspaste take to dry?"
- "Can I use Wachspaste on wood?"

**Current State:** 9 FAQs exist for Pentart Konturenfarbe but may not be rendering on product pages.

| Aspect | Finding |
|--------|---------|
| **Metaobjects** | 9 `product_faq` entries exist (for Pentart Konturenfarbe) |
| **Questions** | Verified via GraphQL API |
| **Unknown** | Whether these render FAQ schema on the actual product page |
| **Action** | Check if `snippets/schema-product-faq.liquid` exists and is called in product template. |

### #6: DIY Metaobjects — `faq_items` Field Empty
**AEO/GEO Impact:** 📊 **Missing FAQPage opportunity on high-value DIY content**
**Risk:** Incomplete Implementation

**Framework Connection:** DIY pages are prime `HowTo` + `FAQPage` combo opportunities. The framework specifies **dual-optimization (SEO + AEO + GEO)**. Empty `faq_items` means:
- No FAQ schema on DIY pages
- Reduced chance of AI citation for common DIY questions
- Less comprehensive entity coverage

| Aspect | Finding |
|--------|---------|
| **Metaobjects** | `diy_experience` entries for `handykette` and `batik-tshirt` |
| **Field** | `faq_items` = `False` (empty) |
| **Impact** | Even if FAQ block renders, it will be empty. |
| **Action** | Populate `faq_items` via Shopify Admin or bulk import. |

---

## ✅ VERIFIED CLAIMS (Still True — Aligns with AEO/GEO Framework)

| # | Claim | AEO/GEO Alignment |
|---|-------|-------------------|
| 1 | Homepage: 1 JSON-LD block (ArtSupplyStore + LocalBusiness + WebSite) | ✅ **Perfect identity graph** — single @graph with linked entities |
| 2 | FAQ page: 2 JSON-LD blocks (ArtSupplyStore + FAQPage with 7 Q&As) | ✅ **AEO priority #1** — FAQPage implemented with 7 extractable Q&As |
| 3 | Zero AVADA Organization schema in JSON-LD | ✅ **Unambiguous identity** — no competing entity definitions |
| 4 | @id spine: all 3 IDs consistent, parentOrganization/publisher match | ✅ **Stable ID references** — critical for GEO entity resolution |
| 5 | Transactional Bridge: `/products/glasaetzungspaste-50ml` → HTTP 200 | ✅ **Entity linking** — products reference main Organization |
| 6 | sameAs: 8 Googlebot-verified URLs | ✅ **External authority signals** — social profiles, GMB, directories |
| 7 | Logo: hardcoded CDN da10333d, not settings.logo | ✅ **Stable asset reference** — consistent across all contexts |
| 8 | Canonical tags: exactly 1 per page | ✅ **Clear content ownership** — no duplicate signals |
| 9 | Pagination Trap: duplicate meta descriptions confirmed | ✅ **Identified for fix** — prevents content duplication penalties |
| 10 | product_faq metaobjects: 9 exist for Konturenfarbe | ✅ **FAQ infrastructure ready** — needs rendering verification |
| 11 | AVADA snippet files: 9 orphaned, inert | ✅ **Clean architecture** — dead code removal aligns with Fortress |
| 12 | Webrex zombies: 14 infected templates (10 collections + 4 products) | ✅ **Identified for cleanup** — aligns with pure Liquid goal |
| 13 | Schema gap: no `shippingDetails` / `MerchantReturnPolicy` | ✅ **Identified DACH gap** — critical for German shopping results |

| # | Claim | Live Proof |
|---|-------|------------|
| 1 | Homepage: 1 JSON-LD block (ArtSupplyStore + LocalBusiness + WebSite) | ✅ Confirmed |
| 2 | FAQ page: 2 JSON-LD blocks (ArtSupplyStore + FAQPage with 7 Q&As) | ✅ Confirmed |
| 3 | Zero AVADA Organization schema in JSON-LD | ✅ Confirmed |
| 4 | @id spine: all 3 IDs consistent, parentOrganization/publisher match | ✅ Confirmed |
| 5 | Transactional Bridge: `/products/glasaetzungspaste-50ml` → HTTP 200 | ✅ Confirmed |
| 6 | sameAs: 8 Googlebot-verified URLs | ✅ Confirmed |
| 7 | Logo: hardcoded CDN da10333d, not settings.logo | ✅ Confirmed |
| 8 | Canonical tags: exactly 1 per page | ✅ Confirmed (Bing CSV was stale) |
| 9 | Pagination Trap: duplicate meta descriptions confirmed | ✅ Confirmed |
| 10 | product_faq metaobjects: 9 exist for Konturenfarbe | ✅ Confirmed via GraphQL |
| 11 | AVADA snippet files: 9 orphaned, inert | ✅ Confirmed |
| 12 | Webrex zombies: 14 infected templates (10 collections + 4 products) | ✅ Confirmed |
| 13 | Schema gap: no `shippingDetails` / `MerchantReturnPolicy` | ✅ Confirmed |

---

## 📊 STALE/FALSE CLAIMS (No Action Needed)

| Claim | Status | AEO/GEO Impact |
|-------|--------|----------------|
| Bing CSV "40 pages with duplicate canonical tags" | ❌ FALSE | No impact — canonical hygiene already achieved |
| AVADA "HobbyShop" schema with `hasMap key=undefined` | ❌ STALE | Historical issue — Fortress suppression working |
| Bastelbedarf page "has old Organization schema" | 🟡 PARTIAL | Actually has OLD + NEW broken duplicates — violates unambiguous identity |
| "AVADA-Managed Schema" section in audit docs | ❌ STALE | AVADA no longer manages schema — Fortress handles it |
| AEO/GEO framework examples using `€€` and plain `Organization` | ❌ STALE | Live uses `EUR` and `ArtSupplyStore` — implementation evolved beyond reference |

| Claim | Status | Reason |
|-------|--------|--------|
| Bing CSV "40 pages with duplicate canonical tags" | ❌ FALSE | All tested pages have exactly 1 canonical. CSV generated before FORTRESS canonical was added. |
| AVADA "HobbyShop" schema with `hasMap key=undefined` | ❌ STALE | No longer appears live. AVADA suppression working. |
| Bastelbedarf page "has old Organization schema" | 🟡 PARTIAL | It has OLD schema **plus** new broken duplicates. |
| "AVADA-Managed Schema" section in audit docs | ❌ STALE | AVADA no longer manages any schema; FORTRESS handles it. |

---

## 🎯 IMMEDIATE ACTION PLAN (Sorted by AEO/GEO Impact)

### Phase 3A — Critical Fixes (Operator + Liquid)
**Goal:** Restore unambiguous identity + enable HowTo rich results

1. **Edit Bastelbedarf page** in Shopify Admin → remove 4 JSON-LD script tags from body HTML. *(Fixes: duplicate entity violation)*
2. **Fix theme.liquid HowTo condition** from `template.suffix contains 'metaobject'` to `template.name == 'metaobject'`. *(Enables: #2 AEO priority schema)*
3. **Test** both DIY pages for HowTo schema appearance. *(Verifies: extractable evidence for AI)*

### Phase 3B — High Priority Fixes
**Goal:** Strengthen topic signaling + clean technical foundation

4. **Operator action**: Remove AVADA script tags from Shopify Admin. *(Achieves: pure Liquid, zero external JS)*
5. **Fix collection H1 tags**: Edit collection template JSONs (10 templates) to output H1. *(Improves: topic clarity for 37 collection pages)*

### Phase 3C — Medium Priority (Post-Implementation)
**Goal:** Maximize FAQ coverage + DACH trust signals

6. **Verify `product_faq` schema renders** on product pages. *(Activates: product-level FAQPage for AI citations)*
7. **Populate `faq_items`** for DIY metaobjects. *(Completes: dual-optimization of DIY content)*
8. **Implement `shippingDetails` + `MerchantReturnPolicy`** schema. *(Addresses: DACH-specific trust gap identified in lateral scan)*

### Phase 3D — AEO/GEO Framework Alignment
**Goal:** Full compliance with reference architecture

9. **Ensure `knowsAbout` array** includes all craft expertise topics from framework.
10. **Verify `sameAs` links** to all 8 external profiles.
11. **Add `availableLanguage: ["German"]`** to ContactPoint.
12. **Validate NAP consistency** across all schema vs Google Business Profile.

### Phase 3A — Critical Fixes (Operator + Liquid)
1. **Edit Bastelbedarf page** in Shopify Admin → remove 4 JSON-LD script tags from body HTML.
2. **Fix theme.liquid HowTo condition** from `template.suffix contains 'metaobject'` to `template.name == 'metaobject'`.
3. **Test** both DIY pages for HowTo schema appearance.

### Phase 3B — High Priority Fixes
4. **Operator action**: Remove AVADA script tags from Shopify Admin.
5. **Fix collection H1 tags**: Edit collection template JSONs (10 templates) to output H1.

### Phase 3C — Medium Priority (Post-Implementation)
6. Verify `product_faq` schema renders on product pages.
7. Populate `faq_items` for DIY metaobjects.
8. Implement `shippingDetails` + `MerchantReturnPolicy` schema (already flagged in lateral report).

---

## 🎯 AEO/GEO Success Metrics Post-Implementation

When Phase 3 is complete, bastelschachtel.at will have:

### Identity Graph Perfection
- ✅ **One unambiguous Organization** (`#organization`) with Austrian legal credentials
- ✅ **All entity references** link back to master node via `@id`
- ✅ **Zero duplicate or broken schema** anywhere on site

### Extractable Evidence Coverage
- ✅ **FAQPage** on `/pages/faq-haufig-fragen` (7 Q&As)
- ✅ **HowTo** on all DIY pages (handykette, batik-tshirt, future)
- ✅ **Product FAQ** on key product pages (Pentart Konturenfarbe)
- ✅ **Clear H1 hierarchy** on all collection pages

### DACH Trust Signals
- ✅ **`shippingDetails`** for German/Austrian delivery expectations
- ✅ **`MerchantReturnPolicy`** for Widerrufsrecht compliance
- ✅ **`priceRange: "EUR"`** (already correct)
- ✅ **`availableLanguage: ["German"]`**

### Technical Fortress
- ✅ **Zero Webrex zombies** in templates
- ✅ **Zero AVADA 404 scripts**
- ✅ **Zero duplicate meta descriptions** (Pagination Trap fixed)
- ✅ **Pure Liquid architecture** with no external JS dependencies

---

## 🧪 Verification Methodology

1. **Live HTML Fetch**: `curl` with Googlebot UA to actual production URLs.
2. **Shopify Admin API**: Direct reads of theme assets (`196991385938`) and pages.
3. **GraphQL Queries**: For metaobjects and deep data.
4. **Regex Parsing**: JSON-LD extraction and Liquid variable detection.
5. **Cross-reference**: Against Bing CSV exports and original audit claims.

**All findings are byte-for-byte live as of 2026-04-14 18:45 UTC.**

---

## 📚 Framework References

- **[[2026-04-13-aeo-geo-framework]]** — Strategic blueprint for AEO/GEO implementation
- **[[2026-04-13-schema-master-status]]** — Current live schema state
- **[[2026-04-13-schema-session-context]]** — Quick reference for implementation sessions
- **[[2026-04-14-operation-ironclad-lateral-extension-report]]** — Full lateral scan findings
- **[[2026-04-14-operation-clean-sweep-handoff]]** — Implementation instructions for Phase 3

---

> **Next Step:** Await authorization to exit read-only mode and begin Phase 3 implementation.