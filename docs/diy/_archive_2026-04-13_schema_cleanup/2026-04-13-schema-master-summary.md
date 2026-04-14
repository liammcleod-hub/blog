# Bastelschachtel Schema Master Summary

**Date:** 2026-04-13  
**Focus:** Schema/Structured Data ONLY (not SEO, not speed, not GSC)

---

## What We Know

### Your Store Has:

| Asset | Status | Schema Relevance |
|-------|--------|-----------------|
| Walk-in store in Wattens | ✅ Yes | LocalBusiness needed |
| Google Business Profile | ✅ Yes (5.0★, 27 reviews) | LocalBusiness needed |
| DIY tutorials (metaobjects) | ✅ Yes (Handykette, Batik T-Shirt) | HowTo schema possible |
| AVADA SEO Suite | ✅ Installed | Should handle schema |
| FAQ page | ✅ Yes | FAQPage possible |
| Products | ✅ Many | Product schema needed |
| Collection pages | ✅ Many | HowTo + FAQ possible |
| Blog | ✅ Yes | Article schema possible |

---

## Schema Strategy (Agreed)

### HowTo = DIY Pages AND Collection Pages!

- DIY tutorials (Handykette, Batik T-Shirt) → HowTo schema
- Collection pages like "Grundmaterial für Korbflechten" → HowTo schema ("Wie startet man mit Korbflechten")
- HowTo steps can be: **Generic intro steps OR derived from DIY tutorials**

### FAQ Tiers (3 Levels)

| Type | Scope | Where Entered |
|------|-------|---------------|
| **Business FAQ** | Store-wide | /faq page only |
| **Collection FAQ** | Per collection | Collection metafield |
| **Product FAQ** | Per product | Product metafield |

### Priority Order

1. **LocalBusiness** (walk-in store + GMB) ← HIGHEST
2. **HowTo** (DIY + collection pages)
3. **Business FAQ** (store-wide)
4. **Collection FAQ**
5. **Product FAQ** (top impressions first ← **GSC data needed**)
6. **Organization** (enrich existing)
7. **WebSite**

---

## Current Schema State (Live Site)

| Schema Type | Should Be On | Currently On Site | Google Rich Results |
|-------------|--------------|-------------------|--------------------|
| **Product** | Every product page | ❌ MISSING | ❌ No Product rich results |
| **LocalBusiness** | Homepage | ❌ MISSING | ❌ No LocalBusiness rich results |
| **FAQPage** | /faq page | ❌ MISSING | ❌ No FAQ rich results |
| **HowTo** | DIY + collection pages | ❌ MISSING | ❌ No HowTo rich results |
| **Organization** | Every page | ✅ YES (incomplete) | ⚪ Organization doesn't generate rich results |
| **WebSite/SearchAction** | Homepage | ❌ MISSING | ❌ No Sitelinks |

### Google Rich Results Test (Homepage) — 13 Apr 2026

```
info
No items detected
No rich results detected in this URL.

Crawled successfully on 13 Apr 2026, 16:28:15
```

**This confirms:** Zero rich result schemas on the homepage. All schema exists but generates no visible benefit in Google.

**Bottom line:** Only Organization exists, and it doesn't create rich results.

---

## What Can Be Implemented NOW (No GSC Data Needed)

### 1. LocalBusiness (Fix AVADA Settings)

**Problem:** AVADA has code but it's broken:
- Google Maps key = "undefined"
- Wrong opening hours (Mon-Fri 9-18, Sat 9-12)
- Missing sameAs (social profiles)
- Type is "HobbyShop" instead of "Store"

**Fix:** Go to AVADA SEO Suite → Local Business settings:
- Add Google Maps API key
- Fix opening hours: **Di-Fr 9-12 & 14-18, Sa 9-12**
- Add social profiles from GMB
- Change type to "Store" or "LocalBusiness"

### 2. Business FAQPage Schema

**Status:** /faq page exists with 7 HTML Q&As but NO JSON-LD.

**Q&As we know:**
1. Wie hoch sind die Versandkosten?
2. Wie kann ich die Ware zurücksenden?
3. Ist der Artikel sofort ab Lager lieferbar?
4. Wie kann ich bezahlen?
5. Sind meine Kreditkarten- und Bankdaten sicher?
6. Bieten Sie auch Expressversand an?
7. Wie kommt der Kaufvertrag zustande?

**Action:** Add FAQPage JSON-LD to /faq page (manual or AVADA).

### 3. HowTo Schema on DIY Tutorial Pages

**What exists:**
- `diy_experience` metaobject with:
  - `title`, `intro`, `steps` (list of `diy_individual_step`)
  - `materials_products` (list of product references)
- 2 DIY tutorials: Handykette, Batik T-Shirt

**Action:** 
1. Create HowTo JSON-LD from `diy_experience` fields
2. Add to DIY page template
3. Map steps → HowToStep, materials → HowToSupply

### 4. Organization Schema (Enrich Existing)

**Current:** Name, logo, URL only.

**Missing:** sameAs, contactPoint

**Action:** Add via AVADA settings or custom snippet:
```json
"sameAs": [
  "https://www.youtube.com/channel/UCv8kayedKQE_SwS9wVFnASg",
  "https://www.instagram.com/bastelschachtel_onlineshop/",
  "https://www.facebook.com/bastelschachtel",
  "https://at.pinterest.com/bastelschachtel/"
],
"contactPoint": {
  "@type": "ContactPoint",
  "telephone": "+43-664-4564271",
  "contactType": "customer service",
  "availableLanguage": ["German"]
}
```

---

## What Requires GSC/GA4 Data

### Product FAQ Schema (Per Product)

**Question:** Which products should get FAQ schema first?

**Answer:** Products with most impressions in Google.

**Needed:**
- Top 20 products by impressions (GSC export)
- Or top 20 products by traffic (GA4)

**Implementation:** 
- Add `product_faq` metaobject references to product metafields
- Use existing `product_faq` metaobject structure (question + answer)

### Collection FAQ Schema (Per Collection)

**Same logic:** Collections with most impressions get FAQ schema first.

**Implementation:**
- Add `collection_faq` metaobject or reuse `product_faq`
- Add collection metafield for FAQ references

### Collection HowTo Schema

**Which collections have HowTo?**
- "Grundmaterial für Korbflechten" → yes
- Others?

**GSC would show:** Which collection pages get search traffic for "how to X" queries.

---

## Implementation Roadmap

### Phase 1: NOW (No GSC Needed) ✅

| # | Task | Method | Effort |
|---|------|--------|--------|
| 1 | Fix AVADA LocalBusiness settings | AVADA dashboard | 10 min |
| 2 | Add Business FAQPage to /faq | Manual JSON-LD or AVADA | 15 min |
| 3 | HowTo on DIY pages (Handykette, Batik) | Theme template | 1-2 hours |
| 4 | Enrich Organization schema | AVADA or custom snippet | 10 min |

### Phase 2: AFTER GSC Data 📊

| # | Task | GSC Data Needed |
|---|------|-----------------|
| 5 | Product FAQ on top 20 products | Top products by impressions |
| 6 | Collection FAQ on top collections | Top collections by impressions |
| 7 | Collection HowTo on traffic-driving collections | "How to X" query data |
| 8 | Product FAQ on remaining products | Full product list |

---

## Business FAQs (Store-Wide)

Your 7 FAQs + suggested additions:

1. Wie hoch sind die Versandkosten?
2. Wie kann ich die Ware zurücksenden?
3. Ist der Artikel sofort ab Lager lieferbar?
4. Wie kann ich bezahlen?
5. Sind meine Kreditkarten- und Bankdaten sicher?
6. Bieten Sie auch Expressversand an?
7. Wie kommt der Kaufvertrag zustande?

**Suggested additions:**
- Wie kann ich euch kontaktieren?
- Bietet ihr auch telefonische Beratung?
- Kann ich im Geschäft vorbeikommen?
- Versendet ihr auch ins Ausland?

---

## Questions Answered

1. ✅ DIY pages should rank → HowTo schema planned
2. ✅ Collection pages can have HowTo → Strategy defined
3. ✅ Local search is a target → LocalBusiness priority confirmed
4. ✅ FAQ strategy: Business + Collection + Product tiers
5. ✅ Product FAQ priority = GSC data needed

---

## Questions Still Open

1. **Collection HowTo steps** — Generic intro steps OR derived from DIY tutorials?
2. **Metafield structure** — Reuse `product_faq` for collections OR new `collection_faq`?
3. **Business FAQ additions** — Any other questions to add?
4. **GSC data** — Will share when ready

---

## Related Docs

- [[2026-04-13-schema-master-plan]] — **IMPLEMENTATION PLAN** (steps, tasks, decision log)
- [[2026-04-13-store-wide-schema-audit]] — Full technical audit
- [[2026-04-13-avada-seo-audit-data]] — Raw AVADA data
- [[2026-04-13-store-wide-schema-adversarial-review]] — Strategic review

---

## Google Rich Results Test Confirmed

**Tested:** Homepage (bastelschachtel.at)
**Date:** 13 Apr 2026, 16:28:15
**Result:** ❌ **No items detected** — No rich results detected in this URL.

**This is the smoking gun:** Zero rich result schemas despite AVADA being installed.

### What This Means

| Schema Type | Code Exists? | Generates Rich Results? |
|-------------|--------------|------------------------|
| Organization | ✅ Yes | ⚪ No (brand signal only) |
| LocalBusiness | ⚠️ Broken | ❌ No |
| Product | ❌ No | ❌ No |
| FAQPage | ❌ No | ❌ No |
| HowTo | ❌ No | ❌ No |
| WebSite | ❌ No | ❌ No |

**Action required:** Implement the schemas that generate visible rich results in Google.

---

## Crawler Access & AIO Optimization (Related, Not Schema)

**Scope:** Not schema, but affects whether AI crawlers can access your content.

### AI/LLM Crawlers to Allow

| Crawler | Why | Where to Allow |
|---------|-----|---------------|
| **Google-Extended** | Google's Gemini uses your content for AI answers | Shopify Crawler Settings |
| **GPTBot / OAI-SearchBot** | ChatGPT/OpenAI recommendations | Shopify Crawler Settings |
| **ClaudeBot** | Anthropic ecosystem | Shopify Crawler Settings |
| **PerplexityBot** | Answer engine visibility | Shopify Crawler Settings |
| **Applebot** | Siri/Apple Maps local results | Shopify Crawler Settings |

### Shopify Crawler Config Location
**Shopify Admin → Settings → Search and social preview → Crawler settings**

### For Austrian Market
- **Geizhals / Idealo** — If you list on these price aggregators

### Action Required
1. Go to **Shopify Admin → Settings → Search and social preview**
2. Look for **Crawler settings** or **Allowed bots**
3. Add signatures for: Google-Extended, GPTBot, ClaudeBot, PerplexityBot, Applebot

### Alternative: robots.txt
You can also configure crawler access via `robots.txt`:
```
User-agent: Google-Extended
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

### Questions About Current Screen
- What service is this signature for?
- Screenshot or more context on what you're trying to achieve?

---

## Status: Needs Clarification

This section needs more info from the user before we can implement.

---

## Crawler Access — VERIFIED ✅

**Status:** No action needed. Your robots.txt allows all AI crawlers.

### robots.txt Analysis

| Rule | Status |
|------|--------|
| Default (User-agent: *) | ✅ Allows all crawlers |
| Products, Collections, Blogs | ✅ Allowed |
| Checkout, Cart, Admin | ❌ Correctly blocked |
| Sitemap | ✅ Present |

### AI Crawlers Allowed

| Crawler | Access |
|---------|--------|
| Google-Extended (Gemini) | ✅ Allowed |
| GPTBot (ChatGPT) | ✅ Allowed |
| ClaudeBot | ✅ Allowed |
| PerplexityBot | ✅ Allowed |
| Applebot | ✅ Allowed |

**No configuration needed.** AI crawlers can access your public content.

### What About That Signature Screen?
The "Neue Signatur erstellen" screen in Shopify Admin is likely for **AVADA verification** — not crawler access. You probably don't need to create a signature unless AVADA specifically asks for one.
