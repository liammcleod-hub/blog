# DIY FAQ + HowTo Plan

**Date:** 2026-04-13 (final)  
**HowTo Schema Status:** ✅ DONE — LIVE FORTRESS  
**Product FAQ Schema:** 📋 Growth Phase

---

## HowTo Schema — DONE ✅

> ⚠️ **REVERIFIED 2026-04-14:** HowTo schema is deployed in `snippets/schema-howto.liquid` but **NOT rendering** on live DIY pages. Root cause: the render condition in theme.liquid is `template.suffix contains 'metaobject'`, but for metaobject routes, `template.suffix = 'diy_experience'` (not `'metaobject'`). The condition never matches. Fix: change to `template.name == 'metaobject'`. Verified by fetching both `/pages/diy-experience/handykette` and `/pages/diy-experience/batik-tshirt` — only ArtSupplyStore @graph appears, no HowTo.

**Deployed:** `snippets/schema-howto.liquid` + theme.liquid render

### What was built
- HowTo rich results for `/handykette` and `/batik-tshirt`
- 8 steps each, mapped from `diy_experience` metaobjects
- `HowToSupply` (products), `HowToTool` (primary product), `HowToStep` (steps)
- Entity-linked: `"provider": {"@id": "https://www.bastelschachtel.at/#organization"}`

### Trigger Condition
```liquid
{%- if template.suffix contains 'metaobject' and closest.metaobject.diy_experience -%}
  {%- render "schema-howto" -%}
{%- endif -%}
```

### DIY Pages
| Page | Handle | Steps | Status |
|------|--------|-------|--------|
| Handykette / Handyarmband DIY | `handykette` | 8 | ✅ LIVE |
| Batik T-Shirt DIY | `batik-tshirt` | 8 | ✅ LIVE |

### DIY Metaobject Structure
```
diy_experience
├── title           → HowTo.name
├── subtitle        → HowTo.description
├── hero_image      → HowTo.image
├── steps[]         → list[diy_individual_step] → HowToStep[]
│   ├── title       → "Schritt 1: Vorbereitung der Basis"
│   ├── description  → step instructions (rich text)
│   └── image       → step image
├── materials_products[] → List[Product] → HowToSupply[]
└── primary_product     → Product → HowToTool[]
```

### HowTo Expansion (GSC-Informed)
GSC query data shows clear DIY intent with traffic:
- `reispapier basteln` (32 clicks, pos 6.36) → new DIY page or blog post
- `schattenbox selber machen` (16 clicks, pos 5.0) → new DIY page
- `korb selber flechten material` (13 clicks, pos 7.67) → expand korbflechten collection + DIY

**Action:** Create new `diy_experience` metaobject entries + `diy_individual_step` entries. HowTo schema deploys automatically via existing template logic.

---

## Product FAQ — Growth Phase

### What Exists
- `product_faq` metaobject type with `question` + `answer` fields
- 9 FAQs exist for Pentart Glasätzungspaste
- Need to attach to product pages via metafield reference

### GSC Priority (Top Product Pages)
| Product | Clicks | Position | FAQ Status |
|---------|--------|----------|------------|
| Pentart Glasätzungspaste 50ml | 199 | 8.12 | Has metaobjects (9 Q&As), needs schema |
| Reispapier A4 weiß | 133 | 6.96 | No FAQ |
| Pentart Tauchfarbe | 46 | 6.36 | No FAQ |
| Pentart Wachspaste Gold | 42 | 5.29 | No FAQ |

### Plan
1. Create product-level metafield reference to `product_faq` metaobjects
2. Create `snippets/schema-product-faq.liquid`
3. Render on product template via `product.metafields` conditional
4. FAQ links use dynamic product URL logic (same pattern as FAQ page):
   ```liquid
   {%- assign product_faqs = product.metafields.custom.product_faq.value -%}
   {%- for faq in product_faqs -%}
     { "@type": "Question", "name": "{{ faq.question }}", "acceptedAnswer": { "text": "{{ faq.answer }}" }}
   {%- endfor -%}
   ```

---

## DIY Page FAQ Expansion — Growth Phase

### Recommendation
Add `faq_items` field to `diy_experience` metaobject:
- Key: `faq_items`
- Type: `list.metaobject_reference` (references `product_faq`)

This lets each DIY page have curated FAQs separate from the product FAQ.

### Rendering
Render visible FAQ accordion + `FAQPage` JSON-LD from same `faq_items` list.

### AEO Notes
- First sentence should directly answer the question
- Use real `<a href>` links in answers (Transactional Bridge pattern)
- FAQs should target: substitutions, troubleshooting, safety/care
- Avoid auto-generating FAQs from steps

---

## Transactional Bridge (FAQ Page) — LIVE ✅

FAQ page `/pages/faq-haufig-fragen` has 5 HTML `<a href>` links in `acceptedAnswer.text`:
- `/pages/versandkosten`
- `/pages/widerrufsrecht`
- `/products/glasaetzungspaste-50ml` (dynamic, via `all_products`)
- `/pages/zahlungsmethoden`
- `/pages/kontakt`

<!-- audit-date: 2026-04-14 -->

---
← [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO — Master Index]]

**Pattern used:**
```liquid
"text": "... <a href=\"{{ shop.url }}/pages/versandkosten\">Versandkosten</a> ..."
```
