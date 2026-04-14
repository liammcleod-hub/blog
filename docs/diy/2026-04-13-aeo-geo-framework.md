# Bastelschachtel AEO/GEO Reference Framework

> **REVERIFIED 2026-04-14:** This is a reference/framework document. The schema examples shown are ASPIRATIONAL (pre-FORTRESS), not the current live state. Key discrepancies vs live:
> - Live uses `ArtSupplyStore` (not plain `Organization`) with `@id` using `#` fragments (not `/`)
> - Live uses `EUR` for priceRange (not `€€`)
> - Live LocalBusiness is `@type: LocalBusiness` (not `ArtSupplyStore`)
> - Live WebSite uses `EntryPoint` + `urlTemplate` pattern for SearchAction (not direct URL)
> - Live has `inLanguage: "de-AT"` on WebSite
> - Live Organization has `legalName`, `vatID`, `taxID`, `founder`, `brand`, `knowsAbout`
> - The canonical live reference is `schema-master-status.md`

**Date:** 2026-04-13  
**Purpose:** Living reference for AI Engine Optimization (AEO) and Generative Engine Optimization (GEO)  
**Related:** [[2026-04-13-schema-master-status]] | [[2026-04-13-schema-session-context]]

---

## Quick Reference Card

| Term | Definition | For Bastelschachtel |
|------|-----------|---------------------|
| **AEO** | Answer Engine Optimization — winning the answer box above links | FAQ schema, Q&A structure |
| **GEO** | Generative Engine Optimization — being named in AI-generated responses | Entity signals, schema, authority |
| **Identity Graph** | Linked @id entities forming one machine-readable knowledge graph | Organization + LocalBusiness + WebSite |
| **NAP** | Name, Address, Phone — must be consistent everywhere | Wattens store info |
| **E-E-A-T** | Experience, Expertise, Authoritativeness, Trustworthiness | DIY content, reviews |

---

## Core Principles (2026)

### 1. Trust = Unambiguous Identity + Extractable Evidence

**What AI answer engines need:**

1. **Unambiguous identity:** One stable entity per real-world thing with durable IDs and reconciled references (sameAs)
2. **Extractable evidence:** Page content that is visible AND structured so machines can lift facts without inventing them

**Google explicitly warns:**
- ❌ Marking up content that isn't visible
- ❌ Misleading or irrelevant markup
- ❌ Out-of-date information

### 2. Build the Graph Around Stable IDs (Identity Spine)

- Use JSON-LD with stable `@id` URIs (canonical, HTTPS)
- Publish them consistently site-wide
- Use `sameAs` to point at authoritative external profiles (social, Wikidata, GMB)
- Keep entity data complete and accurate
- Update time-sensitive attributes (hours, inventory, availability)

### 3. Model as Organization ⇄ LocalBusiness Network

**Core pattern:**

```
Organization (brand) = "who" ← Master Node
    ↓ parentOrganization
LocalBusiness (each store) = "where" ← Connected via branchOf
    ↓ mainEntityOfPage
WebPage (each page) = "what"
    ↓ publisher
HowTo / FAQPage / Product = "how-to / Q&A / products"
```

**Key:** Google notes `branchOf` is superseded by `parentOrganization`. Use `parentOrganization`.

---

## Schema.org Types for Bastelschachtel

### High-Impact Schema Types (AEO Priority Order)

| Rank | Schema Type | Why | Target Pages |
|------|-----------|-----|--------------|
| 1 | **FAQPage** | Highest AI Overview citations | /faq page |
| 2 | **HowTo** | Step extraction for instructional queries | DIY pages, collections |
| 3 | **Organization** | Entity identity in knowledge graphs | Global |
| 4 | **LocalBusiness** | "best [service] near me" voice queries | Homepage, /kontakt |
| 5 | **Product** | Price, availability, reviews | Product pages |
| 6 | **WebSite** | SearchAction for internal search | Homepage |

### Bastelschachtel Specific Types

| Schema | Use | Type |
|--------|-----|------|
| Organization | Brand identity | `ArtSupplyStore` |
| LocalBusiness | Walk-in store | `ArtSupplyStore` |
| HowTo | DIY tutorials | `HowTo` + `HowToStep` |
| FAQ | Business FAQ | `FAQPage` + `Question` |

---

## Identity Graph Architecture

### Master Node: Organization

```json
{
  "@context": "https://schema.org",
  "@type": "ArtSupplyStore",
  "@id": "https://www.bastelschachtel.at/#organization",
  "name": "Bastelschachtel",
  "url": "https://www.bastelschachtel.at",
  "logo": "https://cdn.shopify.com/s/files/.../Logo_RGB.png",
  "knowsAbout": [
    "Bastelbedarf",
    "Korbflechten",
    "Pentart Produkte",
    "Basteln mit Kindern",
    "DIY Handarbeit",
    "Bastelzubehör Österreich"
  ],
  "sameAs": [
    "https://www.youtube.com/channel/UCv8kayedKQE_SwS9wVFnASg",
    "https://www.instagram.com/bastelschachtel_onlineshop/",
    "https://www.facebook.com/bastelschachtel",
    "https://at.pinterest.com/bastelschachtel/",
    "https://www.google.com/maps/place/..."
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+43 664 4564271",
    "contactType": "customer service",
    "availableLanguage": ["German"]
  },
  "priceRange": "€€"
}
```

### Location Node: LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "ArtSupplyStore",
  "@id": "https://www.bastelschachtel.at/#localbusiness",
  "name": "Bastelschachtel",
  "parentOrganization": { "@id": "https://www.bastelschachtel.at/#organization" },
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "Swarovskistraße 3",
    "addressLocality": "Wattens",
    "postalCode": "6112",
    "addressCountry": "AT"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 47.29459740000001,
    "longitude": 11.5928722
  },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "12:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "14:00", "closes": "18:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "12:00" }
  ],
  "telephone": "+43 664 4564271",
  "priceRange": "€€"
}
```

### WebSite Node

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://www.bastelschachtel.at/#website",
  "publisher": { "@id": "https://www.bastelschachtel.at/#organization" },
  "name": "Bastelschachtel",
  "url": "https://www.bastelschachtel.at",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://www.bastelschachtel.at/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

### HowTo Node (DIY Pages)

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "@id": "https://www.bastelschachtel.at/pages/handykette/#howto",
  "name": "Handykette selbst gestalten",
  "mainEntityOfPage": "https://www.bastelschachtel.at/pages/handykette/",
  "publisher": { "@id": "https://www.bastelschachtel.at/#organization" },
  "step": [
    { "@type": "HowToStep", "name": "1. Perlen auswählen", "text": "..." },
    { "@type": "HowToStep", "name": "2. Faden vorbereiten", "text": "..." }
  ],
  "tool": [
    { "@type": "HowToTool", "name": "Zange" }
  ],
  "supply": [
    { "@type": "HowToSupply", "name": "Perlen" },
    { "@type": "HowToSupply", "name": "Faden" }
  ]
}
```

### FAQPage Node

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
        "text": "Genauere Informationen über die Versandkosten finden Sie hier Versandkosten."
      }
    }
  ]
}
```

---

## @graph Implementation (Recommended)

Use `@graph` to publish multiple entities on one page:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://www.bastelschachtel.at/#organization", "name": "Bastelschachtel" },
    { "@type": "LocalBusiness", "@id": "https://www.bastelschachtel.at/#localbusiness",
      "parentOrganization": { "@id": "https://www.bastelschachtel.at/#organization" },
      "name": "Bastelschachtel", "address": {...} },
    { "@type": "WebSite", "@id": "https://www.bastelschachtel.at/#website",
      "publisher": { "@id": "https://www.bastelschachtel.at/#organization" } }
  ]
}
```

---

## Extractable Content Structures

### For Every Entity Page (Brand, Store, HowTo)

Add to HTML (not just JSON-LD):

1. **Definition block:** 1-2 sentence "What it is / who it's for / where it applies"
2. **Key facts table:** Hours, address, phone, services
3. **Scannable summary:** 3-7 bullets
4. **For HowTo:** Numbered steps + Requirements section + Safety/limitations
5. **"Last updated" timestamp**
6. **Regional qualifiers:** "Österreich", "EUR", etc.

**CRITICAL:** JSON-LD must match visible HTML content 100%.  
2026 SpamBrain flags mismatches.

---

## NAP Consistency

| Field | Value | Must Match |
|------|-------|-----------|
| **Name** | Bastelschachtel | Everywhere |
| **Address** | Swarovskistraße 3, 6112 Wattens | Everywhere |
| **Phone** | +43 664 4564271 | Everywhere |
| **Hours** | Di-Fr 9-12 & 14-18, Sa 9-12 | Everywhere |

**NAP must match across:**
- Website schema
- Google Business Profile
- Social profiles
- Directory listings
- Review sites

---

## GDPR Compliance (EU Retail)

- ❌ No PII in schema (names, emails in schema = compliance risk)
- ✅ Use `ContactPoint` for phone/email (not personal)
- ✅ Keep business data in schema, personal data in forms only
- ✅ Include `availableLanguage: ["German"]`

---

## E-E-A-T Signals

| Signal | Implementation |
|--------|---------------|
| **Experience** | DIY content from real crafters, product photos, tutorial videos |
| **Expertise** | Pentart product expertise, craft technique guides |
| **Authoritativeness** | Google Business Profile 5.0★ (27 reviews), social presence |
| **Trustworthiness** | HTTPS, clear contact info, return policy, GDPR compliance |

---

## Validation & Monitoring

| Tool | Purpose |
|------|---------|
| [Google Rich Results Test](https://search.google.com/test/rich-results) | Validate schema |
| [schema.org Validator](https://validator.schema.org) | Check syntax |
| [Google Search Console](https://search.google.com/search-console) | Monitor performance |
| **Monthly:** Re-validate after any schema change |

---

## Key Statistics (2025-2026)

| Metric | Value | Source |
|--------|-------|--------|
| FAQ schema pages earn | **0x more AI Overview citations** | YOOM Digital, 2025 |
| Schema completeness boosts | **3x AI citations** | Industry research |
| Voice search results come from | **featured snippets** | Search Engine Journal |
| ChatGPT weekly users | **100M+** | OpenAI, 2024 |
| Google searches with AI Overviews | **~40%** | Industry estimate |

---

## Implementation Checklist

### Phase 1: Identity Graph
- [ ] Organization schema (Master Node) — ArtSupplyStore, knowsAbout, sameAs
- [ ] LocalBusiness schema (Store) — parentOrganization, geo, hours
- [ ] WebSite schema (Search) — publisher link

### Phase 2: Content Schema
- [ ] FAQPage schema — Verbatim match to visible content
- [ ] HowTo schema — DIY tutorials mapped to metaobjects
- [ ] Product schema — AVADA handles

### Phase 3: Graph Enhancement
- [ ] @graph on key pages (homepage, kontakt, diy pages)
- [ ] sameAs external profiles (GMB, social, directories)
- [ ] E-E-A-T signals in content

### Phase 4: Monitoring
- [ ] Rich Results Test validation
- [ ] GSC performance tracking
- [ ] AI citation monitoring

---

<!-- audit-date: 2026-04-14 -->

---
← [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO — Master Index]]

## Sources Referenced

| Source | Key Insight |
|--------|------------|
| YOOM Digital AEO | FAQPage = highest impact schema for AI citations |
| YOOM Digital GEO | Entity clarity + NAP consistency = AI trust |
| 18th DigiTech | GEO = retrieving + believing + citing information |
| ImmortalSEO | Dual-optimization (SEO + AEO + GEO) |
| Google Developers | Structured data policies, LocalBusiness, HowTo |
| schema.org | @id linking, sameAs, parentOrganization |

---

## Related Documents

- [[2026-04-13-schema-master-status]] — Start here (current status)
- [[2026-04-13-schema-session-context]] — Quick reference for new sessions
- [[2026-04-13-schema-live-gap-analysis]] — Live gap analysis
- [[2026-04-13-diy-faq-implementation-notes]] — DIY FAQ plan (for HowTo phase)
- [[2026-04-13-metadata-forgery-audit-bing-duplicate-descriptions]] — Metadata forensics: Bing duplicate description audit (AEO/SGE identity graph impact)
