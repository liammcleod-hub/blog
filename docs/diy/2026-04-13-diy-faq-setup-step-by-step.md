# DIY FAQ Setup (Metaobjects + Theme Wiring)

Date: 2026-04-13
Theme: `Maerz 2026` (role: `main`)

## Confirmed Shopify Data Model

### Metaobject: `product_faq` (Product FAQ)

- Type: `product_faq`
- Fields:
  - `question` (single line text)
  - `answer` (multi line text)

### Metaobject: `diy_experience` (DIY Experience)

- Type: `diy_experience`
- Important existing fields (already in use on the DIY pages):
  - `steps` (list of metaobject references, to `diy_individual_step`)
  - `materials_products` (list of product references)
- Missing (as of 2026-04-13):
  - No field that links to `product_faq` entries yet.

## What Was Changed In The Theme (Already Done)

> **REVERIFIED 2026-04-14:** The `custom_liquid_faq` block was added to the `diy_experience.json` metaobject template (confirmed in theme assets). However, since HowTo schema is not rendering due to the wrong Liquid condition in theme.liquid (see diy-faq-implementation-notes.md), the FAQ rendering may also be affected. Neither handykette nor batik-tshirt pages show any FAQPage JSON-LD. Additionally, `faq_items` field has NOT been populated in either diy_experience entry (confirmed via GraphQL: both have `Has faq_items: False`).

In the published theme `Maerz 2026`, the metaobject template asset was updated:

- `templates/metaobject/diy_experience.json`
  - Added a new Custom Liquid block: `custom_liquid_faq`
  - The block renders:
    - A visible FAQ accordion
    - Matching `FAQPage` JSON-LD
  - Both are driven from:
    - `closest.metaobject.diy_experience.faq_items`

## What You Need To Do In Shopify Admin (One Time)

Add a new field to the `DIY Experience` metaobject definition:

1. Shopify Admin → Content → Metaobjects → `DIY Experience` (`diy_experience`)
2. Add field:
   - Key: `faq_items`
   - Name: `FAQ Items` (or similar)
   - Type: **List of metaobject references**
   - Reference type: `product_faq`

## What You Need To Do Per DIY Experience Entry

For each `DIY Experience` entry (e.g. Handykette, Batik):

1. Open the metaobject entry
2. Populate `faq_items` with 1..N `product_faq` entries

## Expected Result (Once `faq_items` Has Values)

On each DIY Experience page:

- Visible FAQ section appears (accordion)
- `FAQPage` JSON-LD appears and matches the visible Q/A content

<!-- audit-date: 2026-04-14 -->

---
← [[docs/core tech seo/MASTER|Bastelschachtel SEO & AEO/GEO — Master Index]]

This keeps SEO/AEO/GEO data synchronized with what customers see.

