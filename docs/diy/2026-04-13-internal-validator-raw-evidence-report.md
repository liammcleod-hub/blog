# INTERNAL VALIDATOR PROTOCOL — RAW EVIDENCE REPORT
**Date:** 2026-04-13  
**Validator:** Internal (bypass external validator.schema.org + Google Rich Results Test due to 5.03 MB HTML fetch limit)  
**Purpose:** Confirm FORTRESS architecture is live, Ghost schema is gone, and Transactional Bridge is functional.

---

## VERDICT: FORTRESS IS LIVE. ALL SYSTEMS OPERATIONAL. ✅

> **REVERIFIED 2026-04-14:** Core FORTRESS claims still hold (1 JSON-LD on homepage, 0 AVADA ghosts, @id integrity, Transactional Bridge, canonicals). However, new issues discovered:
> - ❌ HowTo schema NOT rendering on DIY pages (wrong Liquid condition)
> - ❌ Bastelbedarf page has 6 JSON-LD blocks including broken duplicates with unrendered Liquid
> - ❌ Collection pages have no H1 tag (title renders as H3)
> - 🟡 Bing CSV "40 pages with duplicate canonical" is FALSE — all tested pages have exactly 1 canonical

---

## SECTION 1 — The Raw Extract

### HOMEPAGE: 1 JSON-LD block (5.03 MB HTML → 3,916 chars)

```
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ArtSupplyStore",
      "@id": "https://www.bastelschachtel.at#organization",
      "name": "Bastelschachtel",
      "url": "https://www.bastelschachtel.at",
      "logo": "https://cdn.shopify.com/s/files/1/0422/5397/5709/files/Logo_RGB_da10333d-960f-47eb-b812-40e6eb98ebd1.png?v=1776104155",
      "image": "https://cdn.shopify.com/s/files/1/0422/5397/5709/files/Logo_RGB_da10333d-960f-47eb-b812-40e6eb98ebd1.png?v=1776104155",
      "legalName": "Bastel-Kreativ GmbH",
      "vatID": "ATU80189369",
      "taxID": "FN 618806 i",
      "brand": {
        "@type": "Brand",
        "name": "Bastelschachtel"
      },
      "founder": {
        "@type": "Person",
        "name": "Bernhard-Stefan Muller",
        "@id": "https://www.bastelschachtel.at#founder"
      },
      "knowsAbout": [
        "Bastelbedarf",
        "Korbflechten",
        "Pentart Produkte",
        "Basteln mit Kindern",
        "DIY Handarbeit",
        "Bastelzubehoer Oesterreich"
      ],
      "sameAs": [
        "https://shop.app/m/hd7u6tg4c2",
        "https://www.youtube.com/@bastelschachtelonlineshop4280/featured",
        "https://www.firmenabc.at/bastel-kreativ-gmbf_BBFgz",
        "https://www.instagram.com/bastelschachtel_onlineshop/",
        "https://www.facebook.com/bastelschachtel",
        "https://at.pinterest.com/bastelschachtel/",
        "https://www.pinterest.com/bastelschachtel/",
        "https://firmen.wko.at/bastel-kreativ-gmbh/tirol/?firmaid=2f56586f-96e9-4a35-9c0c-9161219ff42a&suchbegriff=bastel%20kreativ"
      ],
      "contactPoint": {
        "@type": "ContactPoint",
        "telephone": "+43 664 4564271",
        "contactType": "customer service",
        "availableLanguage": ["German"],
        "areaServed": "AT"
      },
      "priceRange": "EUR",
      "address": {
        "@type": "PostalAddress",
        "name": "Bastel-Kreativ GmbH",
        "streetAddress": "Swarovskistrasse 3",
        "addressLocality": "Wattens",
        "addressRegion": "Tirol",
        "postalCode": "6112",
        "addressCountry": "AT"
      }
    },
    {
      "@type": "LocalBusiness",
      "@id": "https://www.bastelschachtel.at#localbusiness",
      "name": "Bastelschachtel",
      "url": "https://www.bastelschachtel.at",
      "parentOrganization": {
        "@id": "https://www.bastelschachtel.at#organization"
      },
      "image": "https://cdn.shopify.com/s/files/1/0422/5397/5709/files/Logo_RGB_da10333d-960f-47eb-b812-40e6eb98ebd1.png?v=1776104155",
      "telephone": "+43 664 4564271",
      "email": "info@bastelschachtel.at",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Swarovskistrasse 3",
        "addressLocality": "Wattens",
        "addressRegion": "Tirol",
        "postalCode": "6112",
        "addressCountry": "AT"
      },
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 47.2946067,
        "longitude": 11.5928755
      },
      "servesLocation": {
        "@type": "Country",
        "name": "Austria",
        "countryCode": "AT"
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
      "sameAs": [
        "https://www.google.com/maps/place/Swarovskistrasse+3+6112+Wattens"
      ],
      "priceRange": "EUR"
    },
    {
      "@type": "WebSite",
      "@id": "https://www.bastelschachtel.at#website",
      "publisher": {
        "@id": "https://www.bastelschachtel.at#organization"
      },
      "name": "Bastelschachtel",
      "url": "https://www.bastelschachtel.at",
      "inLanguage": "de-AT",
      "potentialAction": {
        "@type": "SearchAction",
        "target": {
          "@type": "EntryPoint",
          "urlTemplate": "https://www.bastelschachtel.at/search?q={search_term_string}"
        },
        "query-input": "required name=search_term_string"
      }
    }
  ]
}
```

### FAQ PAGE: 2 JSON-LD blocks

**Block 1** — ArtSupplyStore @graph (duplicated for page context):
```
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ArtSupplyStore",
      "@id": "https://www.bastelschachtel.at#organization",
      ... (same ArtSupplyStore as homepage)
    }
  ]
}
```

**Block 2** — FAQPage (2,813 chars, 7 questions):
```
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Wie hoch sind die Versandkosten?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Genauere Informationen über die Versandkosten finden Sie hier <a href=\"https://www.bastelschachtel.at/pages/versandkosten\">Versandkosten</a>."
      }
    },
    {
      "@type": "Question",
      "name": "Wie kann ich die Ware zurücksenden?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bei Bastelschachtel bestellen Sie ganz ohne Risiko. Unsere Ware kann, im Rahmen unserer Vorschriften, problemlos zurückgesandt werden. Weitere Informationen erhalten Sie hier <a href=\"https://www.bastelschachtel.at/pages/widerrufsrecht\">Widerrufsrecht</a>."
      }
    },
    {
      "@type": "Question",
      "name": "Ist der Artikel sofort ab Lager lieferbar?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Ja, die Lagerverfügbarkeit wird direkt in der Produktbeschreibung unterhalb des Preises angezeigt. Beliebte Artikel wie <a href=\"/products/glasaetzungspaste-50ml\">Pentart Glasätzungspaste</a> sind in der Regel sofort lieferbar."
      }
    },
    {
      "@type": "Question",
      "name": "Wie kann ich bezahlen?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Alles Rund ums Bezahlen finden Sie unter folgendem Link <a href=\"https://www.bastelschachtel.at/pages/zahlungsmethoden\">Zahlungsmethoden</a>."
      }
    },
    {
      "@type": "Question",
      "name": "Sind meine Kreditkarten- und Bankdaten sicher?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bei Bastelschachtel.at werden alle persönlichen Daten und Kreditkarteninformationen verschlüsselt übertragen. Wir verwenden eine sichere SSL-Verschlüsselung – Unbefugte haben keinen Zugriff auf Ihre Daten."
      }
    },
    {
      "@type": "Question",
      "name": "Bieten Sie auch Expressversand an?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Bestellungen, die bis 12 Uhr bei uns eingehen, werden noch am selben Tag versendet – eine Expresslieferung ist daher in der Regel nicht nötig. Sollten Sie dennoch Bedenken haben, wenden Sie sich bitte an unseren <a href=\"https://www.bastelschachtel.at/pages/kontakt\">Kundenservice</a>."
      }
    },
    {
      "@type": "Question",
      "name": "Wie kommt der Kaufvertrag zustande?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Durch Lieferung der Ware entsteht der Kaufvertrag. Dieser wird zwischen Ihnen und Bastelschachtel.at geschlossen. Unsere Bestellungen werden ausschließlich in deutscher Sprache abgewickelt."
      }
    }
  ]
}
```

---

## SECTION 2 — The Ghost Audit

| Check | Homepage | FAQ Page | Result |
|-------|----------|----------|--------|
| Total JSON-LD blocks | 1 | 2 | ✅ |
| `"@type": "Organization"` in HTML | 0 | 0 | ✅ NO GHOSTS |
| AVADA inside JSON-LD blocks | 0 | 0 | ✅ |
| AVADA in full HTML | 49 total | 49 total | ✅ |
| — in Firebase CDN URLs | 28 | 28 | ✅ (non-schema) |
| — in script tag attribute | 1 | 1 | ✅ (`data-schema-authority="bastelschachtel"`, not schema content) |
| — elsewhere | 20 | 20 | ✅ (non-schema) |

**AVADA occurrences are all Firebase storage image CDN paths and the script tag's own attribute — zero actual AVADA schema entities remain.**

---

## SECTION 3 — ID Integrity Check

| Entity | @id | Reference |
|--------|-----|-----------|
| ArtSupplyStore (master) | `https://www.bastelschachtel.at#organization` | MASTER |
| LocalBusiness | `https://www.bastelschachtel.at#localbusiness` | — |
| LocalBusiness `parentOrganization` | `https://www.bastelschachtel.at#organization` | **EXACT MATCH** ✅ |
| WebSite | `https://www.bastelschachtel.at#website` | — |
| WebSite `publisher` | `https://www.bastelschachtel.at#organization` | **EXACT MATCH** ✅ |

**Character-for-character comparison:**

| Check | Result |
|-------|--------|
| Org == LocalBusiness.parentOrganization | `True` ✅ |
| Org == WebSite.publisher | `True` ✅ |
| All @ids start with `https://` | `True` ✅ |
| No `//#` double-slash | `True` ✅ |

**NO SLASH INCONSISTENCY. No `/organization` vs `#organization` drift.**

---

## SECTION 4 — Transactional Bridge Proof

**Question:** *"Ist der Artikel sofort ab Lager lieferbar?"*

**Exact `acceptedAnswer.text` raw value (Python repr):**
```
'Ja, die Lagerverfügbarkeit wird direkt in der Produktbeschreibung unterhalb des Preises angezeigt. Beliebte Artikel wie <a href="/products/glasaetzungspaste-50ml">Pentart Glasätzungspaste</a> sind in der Regel sofort lieferbar.'
```

| Check | Result |
|-------|--------|
| `<a href>` tag present | ✅ |
| URL handle | `/products/glasaetzungspaste-50ml` |
| Correct (non-pentart-) handle | ✅ |
| No redirect-inducing prefix | ✅ |

---

## SECTION 5 — Canonical Tag

| Page | Tag | URL |
|------|-----|-----|
| Homepage | `<link rel="canonical" href="https://www.bastelschachtel.at/">` | ✅ |
| FAQ Page | `<link rel="canonical" href="https://www.bastelschachtel.at/pages/faq-haufig-fragen">` | ✅ |

---

## PROOF POINT SUMMARY

| # | Proof Point | Status |
|---|-------------|--------|
| 1 | Raw Extract: @graph structure present | ✅ ArtSupplyStore + LocalBusiness + WebSite |
| 2 | Ghost Audit: No AVADA Organization or stray schema | ✅ Zero ghosts |
| 3 | ID Integrity: @id character-for-character match | ✅ 4/4 checks passed |
| 4 | Transactional Bridge: Correct product URL in FAQ | ✅ `/products/glasaetzungspaste-50ml` |
| 5 | Canonical Tag: Present in `<head>` | ✅ Both pages |

**No breaches. No conflicts. The JSON speaks.**

---

## Validation Script

Saved at: `Code/validate_raw.py`

Run with:
```bash
python3 Code/validate_raw.py
```

Requires: `requests`, `re`, `json` (stdlib)

Output: Full raw JSON dumps for all JSON-LD blocks found on homepage and FAQ page, plus structured checks for Ghost Audit, ID Integrity, Transactional Bridge, and Canonical Tag.

---

## Related Documents

| Doc | Purpose |
|-----|---------|
| [[2026-04-13-schema-master-status]] | FORTRESS architecture status |
| [[2026-04-13-metadata-forgery-audit-bing-duplicate-descriptions]] | Bing duplicate meta description audit |
| [[2026-04-13-aeo-geo-framework]] | AEO/GEO reference framework |

<!-- audit-date: 2026-04-14 -->

---
← [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO — Master Index]]
