---
created: 2026-04-13
modified: 2026-04-13
status: active
source: Shopify Admin API + live storefront inspection
---

# DIY Shopify Live Findings

## Store confirmation

- Shop name: `Bastelschachtel`
- Shop domain: `bastelschachtel.myshopify.com`
- Main theme: `Maerz 2026`
- Main theme ID: `196991385938`

## Core rendering chain

The DIY implementation is not currently wired through a standard Shopify Page template.

It is rendered through a dedicated metaobject template:

- `templates/metaobject/diy_experience.json`

That template renders a single section:

- `sections/master-diy-anleitung.liquid`

This means the actual customer-facing DIY experience is currently a metaobject template flow, not a normal `templates/page.<suffix>.json` page flow.

## Metaobject definitions found

### Main definition

- Name: `DIY Experience`
- Type: `diy_experience`
- Storefront access: `PUBLIC_READ`
- Admin access: `PUBLIC_READ_WRITE`

### Supporting definition

- Name: `DIY Individual Step`
- Type: `diy_individual_step`
- Display name key: `title`
- Storefront access: `PUBLIC_READ`
- Admin access: `PUBLIC_READ_WRITE`

## Live DIY Experience entries found

### Entry 1

- Handle: `diy-experience-8jsy7ngj`
- Updated: `2026-04-10T17:17:46Z`
- Title: `Handykette / Handyarmband DIY`
- Subtitle: `Praktisch, modisch und individuell für Alltag, Schule und Festival`
- Difficulty: `Einfach bis mittel`
- Download button label present: yes
- Download file present: yes
- Hero image present: yes
- Primary product present: yes
- Materials products present: yes
- SEO title present: yes
- SEO description present: yes
- Steps linked: 8

### Entry 2

- Handle: `diy-experience-y8igvhsi`
- Updated: `2026-04-10T17:18:18Z`
- Title: `Batik T‑Shirt DIY`
- Subtitle: `Batik T‑Shirt selber machen – kreatives Upcycling‑Fashion‑Projekt`
- Difficulty: `Einfach`
- Download button label present: no
- Download file present: no
- Hero image present: yes
- Primary product present: no
- Materials products present: no
- SEO title present: no
- SEO description present: no
- Steps linked: 9

## Observed DIY Experience field keys

The live `diy_experience` entries currently use these field keys:

- `title`
- `subtitle`
- `difficulty`
- `intro`
- `hero_image`
- `download_file`
- `download_button_label`
- `primary_product`
- `materials_products`
- `midpage_cta_heading`
- `midpage_cta_image`
- `midpage_cta_text`
- `tip`
- `seo_title`
- `seo_description`
- `steps`

The rendering section also expects or falls back to additional legacy or alternate keys:

- `diffuculty` (misspelled fallback)
- `intro_text`
- `steps_list`
- `materials_list`
- `midpage_heading`
- `midpage_subheading`
- `midpage_text`
- `pdf_guide`
- `download_url`
- `step_title`
- `step_body`
- `step_image`

This indicates the section is trying to support multiple historical shapes instead of one clean contract.

## Observed DIY Individual Step field keys

The live `diy_individual_step` entries currently use:

- `title`
- `image`
- `description`

This is much cleaner than the parent object.

## Theme assets directly related to DIY

Confirmed relevant assets in the live main theme:

- `templates/metaobject/diy_experience.json`
- `sections/master-diy-anleitung.liquid`

Likely SEO-relevant shared snippets also present:

- `snippets/meta-tags.liquid`
- `snippets/avada-seo.liquid`
- `snippets/avada-seo-meta.liquid`
- `snippets/avada-seo-other.liquid`
- `snippets/avada-seo-social.liquid`

## Public storefront check

Live URL checked:

- `https://www.bastelschachtel.at/pages/diy-experience/diy-experience-8jsy7ngj`

Observed:

- HTTP status: `200`
- HTML title: `DIY Handykette selbst gestalten | Handyarmband mit Perlen – Bastelschachtel`
- H1: `Handykette / Handyarmband DIY`
- HowTo schema present: yes
- FAQ schema present: no

## Current section behavior

`master-diy-anleitung.liquid` currently renders:

1. Hero area
2. Optional midpage text area
3. Step-by-step section
4. Interactive materials checklist with add-to-cart behavior
5. PDF download CTA

It also emits a `HowTo` JSON-LD block that derives:

- `name` from `title`
- `description` from `intro`
- `image` from `hero_image`
- `step` entries from linked `steps`
- `supply` entries from `materials_products`

This is the right general direction because visible content and structured data are already partially derived from the same source.

## Structural issues already visible

### 1. Mixed field contract

The section uses too many fallback keys from older naming schemes. This weakens the source-of-truth model and makes future maintenance riskier.

### 2. Metaobject-page routing is easy to miss

Because the implementation lives under `templates/metaobject/diy_experience.json`, anyone looking only at Shopify Pages or page templates could miss the real rendering chain.

### 3. SEO fields are inconsistent across entries

The Handykette entry has `seo_title` and `seo_description`, but the Batik entry does not. That means SEO quality is not yet enforced at the data-model level.

### 4. FAQ schema is absent

The live page currently exposes `HowTo` schema but not `FAQPage` schema.

### 5. Midpage naming is not semantically clean

The current parent object uses CTA-style names such as `midpage_cta_heading` and `midpage_cta_text`, but the section treats them as instructional or explanatory content. This naming mismatch will create confusion as the model expands.

### 6. Section styling is functional but not systematized

The section is usable, but the CSS is still ad hoc and utility-light. It reads like a working prototype rather than a stable visual system for a reusable DIY library.

## Immediate implications

The current implementation is already close to the right architecture:

- metaobject data drives visible content
- the same data also drives `HowTo` schema

But it needs tightening so the contract becomes explicit and durable:

- one canonical parent field model
- one canonical step field model
- explicit support for SEO and FAQ fields
- clearer naming between instructional content, CTA content, and schema content

## Recommended next audit targets

Before editing the live theme implementation, inspect these next:

1. The exact field definitions for `diy_experience`
2. The exact field definitions for `diy_individual_step`
3. Whether FAQ content should live on the parent object or as a separate repeatable metaobject
4. Whether SEO title/description should be rendered into page meta tags from the DIY object
5. Whether the current section output visually matches the intended premium DIY page design
