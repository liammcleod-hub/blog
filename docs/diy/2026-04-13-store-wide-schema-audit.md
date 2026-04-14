# Bastelschachtel Store-Wide Schema Audit

Date: 2026-04-13
Store: bastelschachtel.at / bastelschachtel.myshopify.com
Theme: **Maerz 2026** (ID: 196991385938, role: main)

Related: [[2026-04-13-schema-session-context]] | [[2026-04-13-metadata-forgery-audit-bing-duplicate-descriptions]]

> **REVERIFIED 2026-04-14:** Several findings in this audit are now STALE or SUPERSEDED by the FORTRESS deployment. Key updates:
> - âŒ "AVADA SEO Suite â€” Already Installed!" â†’ AVADA is now UNINSTALLED. All AVADA snippet renders are inert.
> - âŒ "AVADA-Managed Schema" section â†’ AVADA no longer manages any schema. FORTRESS handles it.
> - âŒ "HobbyShop" schema â†’ No longer appears live. AVADA suppression JS + permanent removal working.
> - âŒ "hasMap key=undefined" â†’ No longer present in any live JSON-LD.
> - âš ï¸ "Bastelbedarf page" still has **4 JSON-LD blocks in body_html** with unrendered Liquid (`{{ shop.url }}`, etc.) â€” creating duplicate/broken schema alongside FORTRESS.
> - âŒ "Product schema MISSING" â†’ Shopify auto-injects Product JSON-LD via content_for_header (confirmed live on product pages).
> - âŒ "Wrong opening hours in AVADA" â†’ Now irrelevant; FORTRESS LocalBusiness has correct hours.
> - ðŸŸ¡ "378 broken links" â†’ Not re-verified in this session.

---

## Overview

This document audits the current state of structured data (JSON-LD schema) across the Bastelschachtel Shopify store, organized by schema type and recommended placement.

---

## Schema Placement Strategy

| Schema | Recommended Location | Scope |
|--------|---------------------|-------|
| Organization | `theme.liquid` (global head) | Global |
| WebSite | Homepage (`index`) | Homepage |
| LocalBusiness | Homepage or `/pages/kontakt` | Page-specific |
| FAQPage | `/pages/faq` only | Page-specific |
| HowTo | DIY tutorial pages only | Page-specific |

---

## 1. Organization Schema

**Purpose:** Brand/store identity that applies everywhere.
**Recommended location:** `theme.liquid` (global, in `<head>`)

### Current State âœ… PARTIAL

**Location:** Page "Bastelbedarf" (ID: 158177132882, handle: `bastelbedarf`)

**Found JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "{{ shop.url }}#organization",
  "name": "{{ shop.name }}",
  "url": "{{ shop.url }}",
  "logo": "{{ settings.logo | img_url: '600x' }}",
  "sameAs": []
}
```

**Issues:**
- âŒ Only exists on page-level, NOT global (theme.liquid)
- âŒ Uses Shopify template variables (`{{ shop.name }}`) â€” not rendered properly
- âŒ `sameAs` is empty â€” no social links
- âŒ Missing `contactPoint` with phone, email, hours
- âŒ Missing `address` data

### Recommended Fields (for theme.liquid)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Bastelschachtel",
  "url": "https://www.bastelschachtel.at",
  "logo": "https://www.bastelschachtel.at/cdn/logo.png",
  "sameAs": [
    "https://www.facebook.com/bastelschachtel",
    "https://www.instagram.com/bastelschachtel",
    "https://www.pinterest.com/bastelschachtel"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+43-664-4564271",
    "contactType": "customer service",
    "availableLanguage": ["German"]
  }
}
```

---

## 2. WebSite Schema

**Purpose:** Site-wide search action for Google Search Console.
**Recommended location:** Homepage (`index.liquid` or `theme.liquid`)

### Current State âœ… PARTIAL

**Location:** Page "Bastelbedarf" (ID: 158177132882)

**Found JSON-LD:**
```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "{{ shop.url }}#website",
  "url": "{{ shop.url }}",
  "name": "{{ shop.name }}",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "{{ shop.url }}/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

**Issues:**
- âŒ Only exists on page-level, NOT on homepage
- âŒ Uses Shopify template variables â€” not rendered properly

### Recommended Fields (for theme.liquid or homepage)

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Bastelschachtel",
  "url": "https://www.bastelschachtel.at",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "https://www.bastelschachtel.at/search?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  }
}
```

---

## 3. LocalBusiness Schema

**Purpose:** Physical store presence, hours, contact.
**Recommended location:** Homepage or `/pages/kontakt`

### Current State âŒ MISSING

**No LocalBusiness schema found anywhere.**

**Contact info exists on `/pages/kontakt`:**
- Company: Bastel-Kreativ GmbH
- Address: SwarovskistraÃŸe 3, 6112 Wattens, Ã–sterreich
- Phone: +43 664 456 4271
- Email: info@bastelschachtel.at
- Hours: Di.-Fr. 9-12 & 14-18 Uhr, Sa. 9-12 Uhr

### Recommended JSON-LD (for homepage or kontakt page)

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Bastelschachtel",
  "image": "https://www.bastelschachtel.at/cdn/shop-logo.jpg",
  "telephone": "+43-664-4564271",
  "email": "info@bastelschachtel.at",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "SwarovskistraÃŸe 3",
    "addressLocality": "Wattens",
    "postalCode": "6112",
    "addressCountry": "AT"
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "09:00",
      "closes": "12:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "14:00",
      "closes": "18:00"
    },
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": "Saturday",
      "opens": "09:00",
      "closes": "12:00"
    }
  ],
  "priceRange": "â‚¬â‚¬"
}
```

---

## 4. FAQPage Schema

**Purpose:** FAQ content rich results in Google.
**CRITICAL:** Must only appear on `/pages/faq` â€” not globally!

### Current State âš ï¸ WRONG LOCATION

> **REVERIFIED 2026-04-14:** The Bastelbedarf page (`/pages/bastelbedarf`, ID: 158177132882) still has FAQPage JSON-LD in its `body_html` â€” **3 Q&As with unrendered Liquid IDs** (`{{ shop.url }}{{ page.url }}#faq`). Meanwhile, the FORTRESS FAQ schema on `/pages/faq-haufig-fragen` correctly outputs 7 Q&As with rendered URLs. The Bastelbedarf FAQ is a **duplicate + broken**.

**Found:**
- âœ… JSON-LD exists on **"Bastelbedarf" page** (ID: 158177132882) with **3 Q&As**:
  1. Was gehÃ¶rt alles zu Bastelbedarf?
  2. Wo Bastelbedarf online in Ã–sterreich kaufen?
  3. Welcher Bastelbedarf eignet sich fÃ¼r AnfÃ¤nger und Kinder?
- âŒ **Missing** on dedicated **FAQ page** (`/pages/faq-haufig-fragen`) â€” only HTML, no JSON-LD

**Main FAQ page** (`/pages/faq-haufig-fragen`, ID: 65850998941) has **7 HTML questions** but **NO structured data**:
1. Wie hoch sind die Versandkosten?
2. Wie kann ich die Ware zurÃ¼cksenden?
3. Ist der Artikel sofort ab Lager lieferbar?
4. Wie kann ich bezahlen?
5. Sind meine Kreditkarten- und Bankdaten sicher?
6. Bieten Sie auch Expressversand an?
7. Wie kommt der Kaufvertrag zustande?

### Recommended JSON-LD (for `/pages/faq-haufig-fragen` ONLY)

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Wie hoch sind die Versandkosten?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Genauere Informationen Ã¼ber die Versandkosten finden Sie hier Versandkosten."
      }
    },
    {
      "@type": "Question",
      "name": "Wie kann ich die Ware zurÃ¼cksenden?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bei Bastelschachtel bestellen Sie ganz ohne Risiko. Unsere Ware kann, im Rahmen unserer Vorschriften, problemlos zurÃ¼ckgesandt werden. Weitere Informationen erhalten Sie hier Widerrufsrecht."
      }
    },
    {
      "@type": "Question",
      "name": "Ist der Artikel sofort ab Lager lieferbar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bei der Produktbeschreibung sehen Sie unterhalb des Preises sofort, ob dieser Artikel lagernd ist oder ob Sie mit einer lÃ¤ngeren Wartezeit rechnen mÃ¼ssen."
      }
    },
    {
      "@type": "Question",
      "name": "Wie kann ich bezahlen?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Alles Rund ums Bezahlen finden Sie unter folgenden Link Zahlungsmethoden."
      }
    },
    {
      "@type": "Question",
      "name": "Sind meine Kreditkarten- und Bankdaten sicher?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bei Bastelschachtel.at werden alle persÃ¶nlichen Daten und Kreditkarteninformationen verschlÃ¼sselt Ã¼bertragen. Wir verwenden eine spezielle VerschlÃ¼sselung, mit der es Unbefugten nicht mÃ¶glich ist, auf Ihre Daten zuzugreifen."
      }
    },
    {
      "@type": "Question",
      "name": "Bieten Sie auch Expressversand an?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bestellungen, die bis 12 Uhr bei uns eingehen, werden noch am selben Tag versendet, daher ist eine Expresslieferung nicht notwendig. Sollen Sie dennoch Bedenken haben, wenden Sie sich bitte an unseren Kundenservice."
      }
    },
    {
      "@type": "Question",
      "name": "Wie kommt der Kaufvertrag zustande?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Durch Lieferung der Ware entsteht der Kaufvertrag. Dieser wird zwischen Ihnen und Bastelschachtel.at geschlossen. Unsere Bestellungen werden ausschlieÃŸlich in deutscher Sprache abgewickelt."
      }
    }
  ]
}
```

### Cleanup Needed
- Remove FAQPage JSON-LD from "Bastelbedarf" page (wrong location)
- Add FAQPage JSON-LD to `/pages/faq-haufig-fragen`

---

## 5. HowTo Schema

**Purpose:** Step-by-step DIY instructions for rich results.
**Recommended location:** Individual DIY tutorial pages (via `diy_experience` metaobject)

### Current State âŒ MISSING

**Found:**
- `diy_experience` metaobjects exist (2 entries):
  1. Handykette / Handyarmband DIY
  2. Batik T-Shirt DIY
- `diy_individual_step` metaobjects exist (steps linked)
- `materials_products` field exists (product references)
- âŒ **NO HowTo schema** on any DIY pages

### Metaobject Fields (diy_experience)

| Field | Type | Usage |
|-------|------|-------|
| title | single_line_text_field | HowTo.name |
| intro | rich_text | HowTo.description |
| steps | list.metaobject_reference | HowTo.step[] |
| materials_products | list.product_reference | HowTo.supply[] / tool[] |
| seo_title | single_line_text_field | Meta |
| seo_description | single_line_text_field | Meta |

### Missing Fields (per 2026-04-13-diy-faq-implementation-notes.md)
- `faq_items` field not yet added to `diy_experience`

---

## 6. Product FAQ Schema (via Metaobjects)

**Purpose:** Product-specific FAQs.
**Location:** `product_faq` metaobjects

### Current State âœ… EXISTS

**Found 9 `product_faq` metaobjects** (questions about Pentart Konturenfarbe):
- Auf welchen Materialien kann ich die Konturenfarbe verwenden?
- Wie gelingen mir perfekte "Perlen" oder Punkte (Dotting)?
- Kann ich die Pentart Konturenfarbe fÃ¼r klassische Glasmalerei verwenden?
- Wie lange muss die Pentart Konturenfarbe trocknen?
- Ist die 3D-Konturenfarbe nach dem Trocknen wasserfest?
- Was kann ich tun, wenn die feine DosierdÃ¼se verstopft ist?
- Wie nutze ich die Konturenfarbe fÃ¼r die Serviettentechnik (Decoupage)?
- Kann man die Universal Konturenfarbe auch auf Stoff verwenden?
- Wie lassen sich Fehler beim Auftragen korrigieren?

**Note:** These are product-specific, not store-wide FAQ.

---

## Implementation Checklist

| Schema | Status | Priority | Action Required |
|--------|--------|----------|-----------------|
| **AVADA LocalBusiness** | âš ï¸ Partial | HIGH | Fix Google Maps key, add hours, social links, image in AVADA settings |
| **Organization** | âš ï¸ Partial | MEDIUM | Enhance via AVADA or add via custom snippet |
| **WebSite** | âš ï¸ Partial | MEDIUM | Enhance via AVADA settings |
| **FAQPage** | âš ï¸ Wrong location | HIGH | Remove from Bastelbedarf, add to /faq page (AVADA can manage) |
| **HowTo** | âŒ Missing | MEDIUM | DIY metaobjects exist, need schema implementation |
| **Product FAQ** | âœ… Exists | LOW | Already via metaobjects |
| **Product schema** | â“ Unknown | HIGH | Check if products have JSON-LD (AVADA may handle) |

---

## AVADA SEO Suite â€” Already Installed!

**Status:** âœ… ACTIVE â€” AVADA SEO Suite is installed and managing some schema output.

### AVADA-Managed Schema Snippets Found

| Snippet | What It Does |
|---------|-------------|
| `snippets/avada-seo.liquid` | Main include, calls others |
| `snippets/avada-seo-local-business.liquid` | LocalBusiness schema |
| `snippets/avada-seo-meta.liquid` | Meta tags (OG, Twitter) |
| `snippets/avada-seo-social.liquid` | Social meta |
| `snippets/avada-seo-other.liquid` | Speed optimization, canonical |

### Current AVADA LocalBusiness Output

```json
{
  "@context": "https://schema.org",
  "@type": "HobbyShop",
  "url": "https://www.bastelschachtel.at",
  "name": "Bastelschachtel",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "SwarovskistraÃŸe 3",
    "addressLocality": "Wattens",
    "postalCode": "6112",
    "addressCountry": "AT"
  },
  "hasMap": "https://www.google.com/maps/embed/v1/place?key=undefined&q=...",
  "telephone": "00436644564271"
}
```

### Issues with AVADA LocalBusiness

- âŒ `@type: "HobbyShop"` â€” Non-standard type. Better: `Store` or `LocalBusiness`
- âŒ `hasMap` key is "undefined" â€” Google Maps embed broken
- âŒ Missing: `openingHours`, `image`, `priceRange`, `aggregateRating`, `sameAs`
- âŒ Missing social profiles from GMB (Instagram, Facebook, Pinterest, YouTube)

### Recommendation

**Don't add manual LocalBusiness schema!** Instead:
1. Configure AVADA SEO Suite settings in Shopify Admin â†’ Apps â†’ AVADA SEO Suite
2. Add missing fields: hours, image, social links, Google Maps API key
3. Or: Replace AVADA's HobbyShop with enhanced LocalBusiness via custom snippet

---

## Additional Findings

### BreadcrumbList Schema
âœ… Exists on "Bastelbedarf" page (but wrong location, should be on relevant pages)

### Theme Status
- Active theme: **Maerz 2026** (updated: 2026-04-13)
- theme.liquid is clean (no JSON-LD currently)

### Pages with Schema
| Page | Schemas Found |
|------|---------------|
| Bastelbedarf | WebPage, FAQPage (3 Q&A), BreadcrumbList, Organization |
| /faq-haufig-fragen | âŒ None (HTML only) |
| /kontakt | âŒ None |

---

## API Queries Used

```bash
# Store info
curl -X POST "https://bastelschachtel.myshopify.com/admin/api/2026-01/graphql.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -d '{"query":"{ shop { name url description } }"}'

# Pages list
curl -X GET "https://bastelschachtel.myshopify.com/admin/api/2026-01/pages.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"

# Theme list
curl -X GET "https://bastelschachtel.myshopify.com/admin/api/2026-01/themes.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"

# Theme liquid
curl -X GET "https://bastelschachtel.myshopify.com/admin/api/2026-01/themes/196991385938/assets.json?asset[key]=layout/theme.liquid" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"

# Page body (FAQ page)
curl -X GET "https://bastelschachtel.myshopify.com/admin/api/2026-01/pages/65850998941.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"

# Page body (Bastelbedarf)
curl -X GET "https://bastelschachtel.myshopify.com/admin/api/2026-01/pages/158177132882.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN"
```

---

## Next Steps

1. [ ] **Check AVADA SEO Suite settings** in Shopify Admin â€” configure LocalBusiness fields
2. [ ] **Fix Google Maps embed** in AVADA (API key needed)
3. [ ] **Add social profiles** to AVADA (sameAs array from GMB data)
4. [ ] **Check product schema** â€” does AVADA handle Product JSON-LD?
5. [ ] **FAQPage**: 
   - [ ] Remove from "Bastelbedarf" page (wrong location)
   - [ ] Add to `/pages/faq-haufig-fragen` via AVADA or manually
6. [ ] **HowTo**: Implement on DIY tutorial pages via diy_experience metaobject
7. [ ] **Test all with Google Rich Results Test**
8. [ ] **Validate with schema.org validator**

---

## Live Site Schema Audit (Crawled 2026-04-13)

### Homepage (bastelschachtel.at)

| Schema | Status | Notes |
|--------|--------|-------|
| Organization | âœ… Present | Name, logo, URL (no sameAs, no contactPoint) |
| LocalBusiness | âŒ Missing | AVADA LocalBusiness NOT appearing on live site! |
| WebSite/SearchAction | âŒ Missing | No search box schema |
| FAQPage | âŒ Missing | â€” |

**Actual output on homepage:**
```json
{
  "@context": "http://schema.org",
  "@type": "Organization",
  "name": "Bastelschachtel",
  "logo": "https://www.bastelschachtel.at/cdn/shop/files/Logo_Schmall.png",
  "url": "https://www.bastelschachtel.at"
}
```

### FAQ Page (/pages/faq-haufig-fragen)

| Schema | Status | Notes |
|--------|--------|-------|
| Organization | âœ… Present | Duplicated 2x |
| FAQPage | âŒ Missing | HTML Q&As exist but NO JSON-LD! |
| LocalBusiness | âŒ Missing | â€” |

### Product Page (/products/handy-armband-handgemacht)

| Schema | Status | Notes |
|--------|--------|-------|
| Organization | âœ… Present | Duplicated 2x |
| Product | âŒ **MISSING** | â— No Product JSON-LD at all! |
| LocalBusiness | âŒ Missing | â€” |

### Collection Page (/collections/perlen)

| Schema | Status | Notes |
|--------|--------|-------|
| Organization | âœ… Present | â€” |
| Collection/ProductListing | âŒ Missing | â€” |

---

## Installed Apps (from settings_data.json)

| App | Purpose |
|-----|---------|
| AVADA SEO Suite | SEO, schema, meta tags |
| Judge.me Reviews | Reviews (may provide Product schema) |
| Simprosys Google Shopping Feed | Google Shopping feed |
| Klaviyo Email Marketing SMS | Email marketing |
| Joy Loyalty Program | Loyalty program |
| Appstle Bundles | Product bundles |
| One Click Upsell | Upsells |
| Essential Free Shipping | Free shipping bar |
| GemPages Builder | Page builder |
| Various others | Various |

---

## Missing from AVADA (Manual Implementation Needed)

| Schema | Priority | Where |
|--------|---------|-------|
| **Product schema** | ðŸ”´ CRITICAL | Every product page |
| **FAQPage** | ðŸŸ¡ HIGH | /pages/faq-haufig-fragen |
| **LocalBusiness (enhanced)** | ðŸŸ¡ HIGH | Homepage (fix AVADA) |
| **WebSite/SearchAction** | ðŸŸ¢ MEDIUM | Homepage |
| **HowTo** | ðŸŸ¢ MEDIUM | DIY tutorial pages |
| **Article/BlogPosting** | ðŸŸ¢ MEDIUM | Blog posts |

---

## Next Steps

1. [ ] **Check AVADA SEO Suite settings** in Shopify Admin â†’ Apps â†’ AVADA SEO Suite
2. [ ] **Fix LocalBusiness** â€” Enable output, add Google Maps API key, hours, social profiles
3. [ ] **Check Judge.me** â€” Does it provide Product schema with reviews?
4. [ ] **Add Product schema** â€” Either via AVADA settings or manual
5. [ ] **Add FAQPage** to /pages/faq-haufig-fragen
6. [ ] **Add WebSite/SearchAction** to homepage
7. [ ] **Test all with Google Rich Results Test**

---

## AVADA SEO Suite Full Audit (from AVADA Dashboard)

### ðŸš¨ SEO Scores â€” ALL CRITICAL

| Type | Count | Avg Score | Status |
|------|-------|-----------|--------|
| Products | 10 sampled | 37-44 | ðŸ”´ Kritisch |
| Collections | 10 sampled | 36-43 | ðŸ”´ Kritisch |
| Blog Posts | 10 sampled | 20-44 | ðŸ”´ Kritisch |
| Pages | 10 sampled | 18-40 | ðŸ”´ Kritisch |

### ðŸš¨ SEO Checklist Summary

| Metric | Value |
|--------|-------|
| Overall Score | **55/100** |
| Rating | Medium |
| Unsolved Tasks | 8 |
| Critical Problems | **7** |
| Improvements | 1 |
| Good Results | 19 |

**Critical Issues:**
1. Bild alt: 1 Seite fehlt (Image alt: 1 page missing)
2. Inhalt der After-List-Sammlung fehlt (After-list collection content missing)
3. Strukturierte Daten zu Bewertungen fehlen (**Structured data for reviews missing!**)
4. 378 defekte Links (378 broken links)
5. Beschleunigen: Nie durchgefÃ¼hrt (Speed optimization never done)
6. Geschwindigkeitspunktzahl: Langsamer als Ã¤hnliche Shops (Speed: Slower than similar shops)

### âš¡ Speed Performance â€” VERY BAD

| Metric | Value | Rating |
|--------|-------|--------|
| Overall Score | **30/100** | ðŸ”´ Arm (Poor) |
| Loading Speed | **8.6 seconds** | ðŸ”´ Very slow |
| CLS (Visual Stability) | 0.002 | âœ… Good |
| Total Blocking Time | **2,820 ms** | ðŸ”´ Very high |
| Interactivity | 320 ms | ðŸŸ¡ OK |

**Acceleration Mode:** Custom/Aktuell (Not optimized)

### ðŸ“ Meta Tags Templates (AVADA Configured)

**Product Template:**
```
Title: {{ product.title }}
Description: Entdecken Sie {{ product.title }} bei {{ shop.name }} â€“ kreative Bastelmaterialien mit Liebe ausgewÃ¤hlt in {{ shop.address.country }}. Ideal fÃ¼r DIY-Projekte, Geschenke und Dekoration. âœ” Schneller Versand âœ” PersÃ¶nlicher Service.
```

**Collection Template:**
```
Title: {{ collection.title }}
Description: Entdecke {{ collection.title }} bei {{ shop.name }} â€“ kreative Bastelkollektionen mit sorgfÃ¤ltig ausgewÃ¤hlten Produkten aus {{ shop.address.country }}. Inspiration fÃ¼r DIY-Projekte, Geschenke und Dekoration. âœ” Schneller Versand âœ” PersÃ¶nlicher Service.
```

### ðŸ”‘ Instant Indexing â€” ðŸ”´ API KEYS MISSING

| Service | Status |
|---------|--------|
| Google API Key | âŒ **Missing** (JSON upload required) |
| Bing API Key | âŒ Missing |
| Google Daily Limit | Max 0/100 URLs (should be up to 200/day) |

### ðŸ• Local Business Hours (AVADA Configured)

| Day | Hours |
|-----|-------|
| Monday | 09:00 - 18:00 |
| Tuesday | 09:00 - 18:00 |
| Wednesday | 09:00 - 18:00 |
| Thursday | 09:00 - 18:00 |
| Friday | 09:00 - 18:00 |
| Saturday | 09:00 - 12:00 |
| Sunday | Closed |

âš ï¸ **WRONG HOURS!** AVADA has Mon-Fri 9-18, but actual hours are:
- Di.-Fr. 9-12 & 14-18 Uhr
- Sa. 9-12 Uhr

### ðŸ”— Broken Links â€” 378 Unresolved

| Status | Count |
|--------|-------|
| Unresolved 404s | **378** |
| Resolved 404s | 8,321 |
| Auto-redirect | Enabled âœ… |

**Top broken links by traffic:**
1. `/weihnachtsoffnungszeiten-767` (4 visits)
2. `/undefined` (136 visits!) ðŸ”´ HIGH TRAFFIC 404!

### ðŸ“± Social Networks (OG Preview)

```
Bastelbedarf aus Ã–sterreich: Pentart, Reispapier, Korbflechten, Bastelsets und kreative Spezialprodukte. 4,88â˜…, persÃ¶nliche Beratung und Versand ab 70â‚¬ frei.
```

---

## â— CRITICAL ACTIONS FROM AVADA AUDIT

### Priority 1: Fix These NOW

| Issue | Impact | Fix |
|-------|--------|-----|
| **Google API Key Missing** | Can't submit URLs for indexing | Get API key from Google Search Console |
| **Reviews Schema Missing** | No stars in search results | Enable Judge.me review schema |
| **`/undefined` 404 (136 visits)** | Losing traffic | Find what's causing undefined URLs |
| **Wrong opening hours** | Local search confusion | Update in AVADA settings |
| **Speed 8.6s** | High bounce rate | Run AVADA speed optimization |

### Priority 2: Fix Within 1 Week

| Issue | Impact | Fix |
|-------|--------|-----|
| **378 broken links** | SEO crawl budget waste | Fix via AVADA Broken Link Manager |
| **Speed optimization never done** | Poor UX, low rankings | Run AVADA acceleration mode |
| **All pages score 18-44** | Poor visibility | Improve meta descriptions, add schema |

### Priority 3: Schema Implementation

| Schema | Status | Notes |
|--------|--------|-------|
| Product (AVADA) | âŒ Not working | Check settings |
| LocalBusiness | âš ï¸ Wrong hours | Update in AVADA |
| FAQPage | âŒ Missing | Add to FAQ page |
| Reviews | âŒ Missing | Judge.me may need config |
| HowTo | âŒ Missing | DIY pages |

<!-- audit-date: 2026-04-14 -->

---
â† [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO â€” Master Index]]
